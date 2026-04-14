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

from typing import Callable, Optional
import grpc, logging, queue, threading, time
from common.proto.dlt_gateway_pb2 import DltRecordEvent, DltRecordSubscription
from common.tools.grpc.Tools import grpc_message_to_json_string
from dlt.connector.client.DltGatewayClient import DltGatewayClient

LOGGER = logging.getLogger(__name__)

# This class accepts an event_handler method as attribute that can be used to pre-process and
# filter events before they reach the events_queue. Depending on the handler, the supported
# behaviors are:
# - If the handler is not set, the events are transparently added to the events_queue.
# - If returns None for an event, the event is not stored in the events_queue.
# - If returns a DltRecordEvent object for an event, the returned event is stored in the events_queue.
# - Other combinations are not supported.

class DltEventsCollector(threading.Thread):
    def __init__(
        self, dltgateway_client : DltGatewayClient,
        log_events_received     : bool = False,
        event_handler           : Optional[Callable[[DltRecordEvent], Optional[DltRecordEvent]]] = None,
    ) -> None:
        super().__init__(name='DltEventsCollector', daemon=True)
        self._dltgateway_client = dltgateway_client
        self._log_events_received = log_events_received
        self._event_handler = event_handler
        self._events_queue = queue.Queue()
        self._terminate = threading.Event()
        self._dltgateway_stream = None

    def run(self) -> None:
        event_handler = self._event_handler
        if event_handler is None: event_handler = lambda e: e
        self._terminate.clear()
        while not self._terminate.is_set():
            try:
                subscription = DltRecordSubscription() # bu default subscribe to all
                self._dltgateway_stream = self._dltgateway_client.SubscribeToDlt(subscription)
                for event in self._dltgateway_stream:
                    if self._log_events_received:
                        LOGGER.info('[_collect] event: {:s}'.format(grpc_message_to_json_string(event)))
                    event = event_handler(event)
                    if event is None: continue
                    if not isinstance(event, DltRecordEvent):
                        # pylint: disable=broad-exception-raised
                        raise Exception('Unsupported return type: {:s}'.format(str(event)))
                    self._events_queue.put_nowait(event)
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAVAILABLE: # pylint: disable=no-member
                    time.sleep(0.5)
                    continue
                elif e.code() == grpc.StatusCode.CANCELLED: # pylint: disable=no-member
                    break
                else:
                    raise # pragma: no cover

    def get_event(self, block : bool = True, timeout : float = 0.1):
        try:
            return self._events_queue.get(block=block, timeout=timeout)
        except queue.Empty: # pylint: disable=catching-non-exception
            return None

    def get_events(self, block : bool = True, timeout : float = 0.1, count : int = None):
        events = []
        if count is None:
            while True:
                event = self.get_event(block=block, timeout=timeout)
                if event is None: break
                events.append(event)
        else:
            for _ in range(count):
                event = self.get_event(block=block, timeout=timeout)
                if event is None: continue
                events.append(event)
        return sorted(events, key=lambda e: e.event.timestamp.timestamp)

    def stop(self):
        self._terminate.set()
        if self._dltgateway_stream is not None: self._dltgateway_stream.cancel()
