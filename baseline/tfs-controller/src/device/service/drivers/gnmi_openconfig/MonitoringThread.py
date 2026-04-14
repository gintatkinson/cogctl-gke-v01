# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Ref: https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md
# Ref: https://github.com/openconfig/gnmi/blob/master/proto/gnmi/gnmi.proto

from __future__ import annotations
import grpc, logging, queue, re, threading
from collections.abc import Iterator
from datetime import datetime
from typing import Dict
from common.tools.grpc.Tools import grpc_message_to_json_string
from .gnmi.gnmi_pb2 import ( # pylint: disable=no-name-in-module
    QOSMarking, SubscribeRequest, Subscription, SubscriptionList, SubscriptionMode
)
from .gnmi.gnmi_pb2_grpc import gNMIStub
from .tools.Path import path_from_string, path_to_string
from .DeltaSampleCache import DeltaSampleCache


LOGGER = logging.getLogger(__name__)

# SubscriptionList Mode: Mode of the subscription.
#  STREAM = 0: Values streamed by the target. gNMI Specification Section 3.5.1.5.2
#  ONCE   = 1: Values sent once-off by the target. gNMI Specification Section 3.5.1.5.1
#  POLL   = 2: Values sent in response to a poll request. gNMI Specification Section 3.5.1.5.3
GNMI_SUBSCRIPTION_LIST_MODE = SubscriptionList.Mode.STREAM

# Path Prefix: Prefix used for paths.
GNMI_PATH_PREFIX = None

# QOS MArking: DSCP marking to be used.
GNMI_QOS_MARKING = None

# Allow Aggregation: Whether elements of the schema that are marked as eligible for aggregation
# should be aggregated or not.
GNMI_ALLOW_AGGREGATION = False

# Encoding: The encoding that the target should use within the Notifications generated
# corresponding to the SubscriptionList.
GNMI_ENCODING = 'JSON'

#Subscription Mode: The mode of the subscription, specifying how the target must return values
# in a subscription. gNMI Specification Section 3.5.1.3
#  TARGET_DEFINED = 0: The target selects the relevant mode for each element.
#  ON_CHANGE      = 1: The target sends an update on element value change.
#  SAMPLE         = 2: The target samples values according to the interval.
GNMI_SUBSCRIPTION_MODE = SubscriptionMode.SAMPLE

# Suppress Redundant: Indicates whether values that have not changed should be sent in a SAMPLE
# subscription. gNMI Specification Section 3.5.1.3
GNMI_SUPPRESS_REDUNDANT = False

# Heartbeat Interval: Specifies the maximum allowable silent period in nanoseconds when
# suppress_redundant is in use. The target should send a value at least once in the period
# specified. gNMI Specification Section 3.5.1.3
GNMI_HEARTBEAT_INTERVAL = 10 # seconds

GNMI_SUBSCRIPTION_TIMEOUT = None

class MonitoringThread(threading.Thread):
    def __init__(
        self, stub : gNMIStub, logger : logging.Logger, settings : Dict,
        in_subscriptions : queue.Queue, out_samples : queue.Queue
    ) -> None:
        super().__init__(daemon=True)
        self._terminate = threading.Event()
        self._stub = stub
        self._logger = logger
        self._username = settings.get('username')
        self._password = settings.get('password')
        self._in_subscriptions = in_subscriptions
        self._out_samples = out_samples
        self._response_iterator = None
        self._delta_sample_cache = DeltaSampleCache()

    def stop(self) -> None:
        self._terminate.set()
        if self._response_iterator is not None:
            self._response_iterator.cancel()

    def generate_requests(self) -> Iterator[SubscribeRequest]:
        subscriptions = []
        while not self._terminate.is_set():
            try:
                # Some devices do not support to process multiple
                # SubscriptionList requests in a bidirectional channel.
                # Increased timeout to 5 seconds assuming it should
                # bring enough time to receive all the subscriptions in
                # the queue and process them in bulk.
                subscription = self._in_subscriptions.get(block=True, timeout=5.0)
                operation, resource_key, sampling_duration, sampling_interval = subscription   # pylint: disable=unused-variable
                if operation != 'subscribe': continue # Unsubscribe not supported by gNMI, needs to cancel entire connection
                # options.timeout = int(sampling_duration)
                #_path = parse_xpath(resource_key)
                path = path_from_string(resource_key)
                subscription = Subscription(
                    path=path, mode=GNMI_SUBSCRIPTION_MODE, suppress_redundant=GNMI_SUPPRESS_REDUNDANT,
                    sample_interval=int(sampling_interval * 1000000000),
                    heartbeat_interval=int(GNMI_HEARTBEAT_INTERVAL * 1000000000))
                subscriptions.append(subscription)
            except queue.Empty:
                if len(subscriptions) == 0: continue
                self._logger.debug('[generate_requests] process')
                prefix = path_from_string(GNMI_PATH_PREFIX) if GNMI_PATH_PREFIX is not None else None
                qos = QOSMarking(marking=GNMI_QOS_MARKING) if GNMI_QOS_MARKING is not None else None
                subscriptions_list = SubscriptionList(
                    prefix=prefix, mode=GNMI_SUBSCRIPTION_LIST_MODE, allow_aggregation=GNMI_ALLOW_AGGREGATION,
                    encoding=GNMI_ENCODING, subscription=subscriptions, qos=qos)
                subscribe_request = SubscribeRequest(subscribe=subscriptions_list)
                str_subscribe_request = grpc_message_to_json_string(subscribe_request)
                self._logger.debug('[generate_requests] subscribe_request={:s}'.format(str_subscribe_request))
                yield subscribe_request
                subscriptions = []
            except: # pylint: disable=bare-except
                self._logger.exception('[generate_requests] Unhandled Exception')

    def run(self) -> None:
        # Add a dummy subscription to be used as keep-alive
        # usable only with SRLinux native data models
        #subscription = ('/system/name/host-name', None, 1)
        #self._in_subscriptions.put_nowait(subscription)

        try:
            request_iterator = self.generate_requests()
            metadata = [('username', self._username), ('password', self._password)]
            timeout = None # GNMI_SUBSCRIPTION_TIMEOUT = int(sampling_duration)
            self._response_iterator = self._stub.Subscribe(request_iterator, metadata=metadata, timeout=timeout)
            for subscribe_response in self._response_iterator:
                str_subscribe_response = grpc_message_to_json_string(subscribe_response)
                self._logger.debug('[run] subscribe_response={:s}'.format(str_subscribe_response))
                update = subscribe_response.update
                timestamp_device = float(update.timestamp) / 1.e9
                timestamp_local = datetime.timestamp(datetime.utcnow())
                # if difference between timestamp from device and local is lower than 1 second
                if abs(timestamp_device - timestamp_local) <= 1:
                    # assume clocks are synchronized, use timestamp from device
                    timestamp = timestamp_device
                else:
                    # might be clocks are not synchronized, use local timestamp
                    timestamp = timestamp_local
                str_prefix = path_to_string(update.prefix) if len(update.prefix.elem) > 0 else ''
                for update_entry in update.update:
                    str_path = path_to_string(update_entry.path)
                    if len(str_prefix) > 0:
                        str_path = '{:s}/{:s}'.format(str_prefix, str_path)
                        str_path = str_path.replace('//', '/')
                    if str_path.startswith('/interfaces/'):
                        # Add namespace, if missing
                        str_path_parts = str_path.split('/')
                        str_path_parts[1] = 'openconfig-interfaces:interfaces'
                        str_path = '/'.join(str_path_parts)
                    #if str_path != '/system/name/host-name': continue
                    #counter_name = update_entry.path[-1].name
                    value_type = update_entry.val.WhichOneof('value')
                    value = getattr(update_entry.val, value_type)
                    if isinstance(value, str):
                        if re.match(r'^[0-9]+$', value) is not None:
                            value = int(value)
                        elif re.match(r'^[0-9]*\.[0-9]*$', value) is not None:
                            value = float(value)
                        else:
                            value = str(value)
                    delta_sample = self._delta_sample_cache.get_delta(str_path, timestamp, value)
                    if delta_sample is None:
                        sample = (timestamp, str_path, value)
                    else:
                        sample = (delta_sample[0], str_path, delta_sample[1])
                    self._logger.debug('[run] sample={:s}'.format(str(sample)))
                    if sample[2] is not None:
                        # Skip not-a-number (e.g., division by zero) samples
                        self._out_samples.put_nowait(sample)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.CANCELLED: raise                 # pylint: disable=no-member
            if e.details() != 'Locally cancelled by application!': raise    # pylint: disable=no-member
        except: # pylint: disable=bare-except
            self._logger.exception('Unhandled Exception')
