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

import copy,grpc,json, logging, queue, threading
from typing import Any, Dict, List, Optional, Tuple, Union
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.type_checkers.Checkers import chk_float, chk_length, chk_string, chk_type
from device.service.drivers.gnmi_nokia_srlinux.handlers.Tools import get_schema
from .gnmi.gnmi_pb2_grpc import gNMIStub
from .gnmi.gnmi_pb2 import Encoding, GetRequest, SetRequest, UpdateResult   # pylint: disable=no-name-in-module
from .handlers import ALL_RESOURCE_KEYS, compose, get_path, parse
from .tools.Capabilities import get_supported_encodings
from .tools.Channel import get_grpc_channel
from .tools.Path import path_from_string, path_to_string #, compose_path
from .tools.Subscriptions import Subscriptions
from .tools.Value import decode_value #, value_exists
from .MonitoringThread import MonitoringThread


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class GnmiSessionHandler:
    def __init__(self, address : str, port : int, settings : Dict, logger : logging.Logger) -> None:
        self._address   = address
        self._port      = port
        self._settings  = copy.deepcopy(settings)
        self._logger    = logger
        self._lock      = threading.Lock()
        self._connected = threading.Event()
        self._username  = settings.get('username')
        self._password  = settings.get('password')
        self._use_tls   = settings.get('use_tls', False)
        self._channel : Optional[grpc.Channel] = None
        self._stub : Optional[gNMIStub] = None
        self._monit_thread = None
        self._supported_encodings = None
        self._subscriptions = Subscriptions()
        self._in_subscriptions = queue.Queue()
        self._out_samples = queue.Queue()

    @property
    def subscriptions(self): return self._subscriptions

    @property
    def in_subscriptions(self): return self._in_subscriptions

    @property
    def out_samples(self): return self._out_samples

    def connect(self):
        with self._lock:
            self._channel = get_grpc_channel(self._address, self._port, self._use_tls, self._logger)
            self._stub = gNMIStub(self._channel)
            self._supported_encodings = get_supported_encodings(
                self._stub, self._username, self._password, timeout=120)
            self._monit_thread = MonitoringThread(
                self._stub, self._logger, self._settings, self._in_subscriptions, self._out_samples)
            self._monit_thread.start()
            self._connected.set()

    def disconnect(self):
        if not self._connected.is_set(): return
        with self._lock:
            self._monit_thread.stop()
            self._monit_thread.join()
            self._channel.close()
            self._connected.clear()

    def get(self, resource_keys : List[str]) -> List[Tuple[str, Union[Any, None, Exception]]]:
        if len(resource_keys) == 0: resource_keys = ALL_RESOURCE_KEYS
        chk_type('resources', resource_keys, list)

        parsing_results = []
        map_paths_to_resource_keys : Dict[str, List[str]] = {}

        get_request = GetRequest()
        get_request.type = GetRequest.DataType.ALL
        get_request.encoding = Encoding.JSON_IETF
        #get_request.use_models.add() # kept empty: return for all models supported
        for i,resource_key in enumerate(resource_keys):
            str_resource_name = 'resource_key[#{:d}]'.format(i)
            try:
                chk_string(str_resource_name, resource_key, allow_empty=False)
                self._logger.debug('[GnmiSessionHandler:get] resource_key = {:s}'.format(str(resource_key)))
                str_path = get_path(resource_key)
                map_paths_to_resource_keys.setdefault(get_schema(str_path), list()).append(resource_key)
                self._logger.debug('[GnmiSessionHandler:get] str_path = {:s}'.format(str(str_path)))
                get_request.path.append(path_from_string(str_path))
            except Exception as e: # pylint: disable=broad-except
                MSG = 'Exception parsing {:s}: {:s}'
                self._logger.exception(MSG.format(str_resource_name, str(resource_key)))
                parsing_results.append((resource_key, e)) # if validation fails, store the exception

        if len(parsing_results) > 0:
            return parsing_results

        metadata = [('username', self._username), ('password', self._password)]
        timeout = None # GNMI_SUBSCRIPTION_TIMEOUT = int(sampling_duration)
        get_reply = self._stub.Get(get_request, metadata=metadata, timeout=timeout)
        #self._logger.info('get_reply={:s}'.format(grpc_message_to_json_string(get_reply)))

        results = []
        #results[str_filter] = [i, None, False]  # (index, value, processed?)

        for notification in get_reply.notification:
            #for delete_path in notification.delete:
            #    self._logger.info('delete_path={:s}'.format(grpc_message_to_json_string(delete_path)))
            #    str_path = path_to_string(delete_path)
            #    resource_key_tuple = results.get(str_path)
            #    if resource_key_tuple is None:
            #        # pylint: disable=broad-exception-raised
            #        MSG = 'Unexpected Delete Path({:s}); requested resource_keys({:s})'
            #        raise Exception(MSG.format(str(str_path), str(resource_keys)))
            #    resource_key_tuple[2] = True

            for update in notification.update:
                #self._logger.info('update.path={:s}'.format(grpc_message_to_json_string(update.path)))
                str_path = path_to_string(update.path)
                #self._logger.info('str_path is ={:s}'.format(str(str_path)))
                #resource_key_tuple = results.get(str_path)
                #if resource_key_tuple is None:
                #    # pylint: disable=broad-exception-raised
                #    MSG = 'Unexpected Update Path({:s}); requested resource_keys({:s})'
                #    raise Exception(MSG.format(str(str_path), str(resource_keys)))
                try:
                    value = decode_value(update.val)
                    #self._logger.info('value is ={:s}'.format(str(value))) # uncomment to see decoded message from the device
                    #resource_key_tuple[1] = value
                    #resource_key_tuple[2] = True
                    #results.extend(parse(str_path, value))
                    _str_path = '/{:s}'.format(list(value.keys())[0]) if str_path == '/' else str_path
                    _str_path = get_schema(_str_path)
                    resource_keys = map_paths_to_resource_keys.get(_str_path, list())
                    self._logger.debug('[GnmiSessionHandler:get] _str_path is = {:s}'.format(_str_path))
                    if len(resource_keys) == 0:
                        MSG = 'No resource_keys found for str_path({:s})/_str_path({:s}). map_paths_to_resource_keys={:s}'
                        self._logger.error(MSG.format(str(str_path), str(_str_path), str(map_paths_to_resource_keys)))
                    else:
                        MSG = 'resource_keys for str_path({:s})/_str_path({:s}): {:s}'
                        self._logger.info(MSG.format(str(str_path), str(_str_path), str(resource_keys)))
                    for resource_key in resource_keys:
                        results.extend(parse(resource_key, str_path, value))
                except Exception as e: # pylint: disable=broad-except
                    MSG = 'Exception processing notification {:s}'
                    self._logger.exception(MSG.format(grpc_message_to_json_string(notification)))
                    results.append((str_path, e)) # if validation fails, store the exception

        #_results = sorted(results.items(), key=lambda x: x[1][0])
        #results = list()
        #for resource_key,resource_key_tuple in _results:
        #    _, value, processed = resource_key_tuple
        #    value = value if processed else Exception('Not Processed')
        #    results.append((resource_key, value))
        return results

    def set(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        #resource_keys = [key for key,_ in resources]
        #current_values = self.get(resource_keys)

        #resource_tuples = {
        #    resource_key : [i, value, value_exists(value), None]
        #    for i,(resource_key,value) in enumerate(current_values)
        #}

        #self._logger.info('---0')
        #self._logger.info(str(resource_tuples))

        set_request = SetRequest()
        #for resource_key in resource_keys:
        for resource_key, resource_value in resources:
            self._logger.info('Resource from test script:')
            self._logger.info('  resource_key   = ' + str(resource_key))
            self._logger.info('  resource_value = ' + str(resource_value))

            #resource_tuple = resource_tuples.get(resource_key)
            #if resource_tuple is None: continue
            #_, value, exists, operation_done = resource_tuple
            if isinstance(resource_value, str): resource_value = json.loads(resource_value)
            str_path, str_data = compose(resource_key, resource_value, delete=False)

            self._logger.info('Request being sent to device:')
            self._logger.info('  path = ' + str(str_path))
            self._logger.info('  data = ' + str(str_data))

            set_request_list = set_request.update #if exists else set_request.replace
            set_request_entry = set_request_list.add()
            set_request_entry.path.CopyFrom(path_from_string(str_path))
            set_request_entry.val.json_ietf_val = str_data.encode('UTF-8')


        self._logger.info('set_request={:s}'.format(grpc_message_to_json_string(set_request)))
        metadata = [('username', self._username), ('password', self._password)]
        timeout = None # GNMI_SUBSCRIPTION_TIMEOUT = int(sampling_duration)
        set_reply = self._stub.Set(set_request, metadata=metadata, timeout=timeout)
        self._logger.info('set_reply={:s}'.format(grpc_message_to_json_string(set_reply)))

        results = []
        for (resource_key, resource_value), update_result in zip(resources, set_reply.response):
            operation = update_result.op
            if operation == UpdateResult.UPDATE:
                results.append((resource_key, True))
            else:
                results.append((resource_key, Exception('Unexpected')))

            #str_path = path_to_string(update_result.path)
            #resource_tuple = resource_tuples.get(str_path)
            #if resource_tuple is None: continue
            #resource_tuple[3] = operation

        #resource_tuples = sorted(resource_tuples.items(), key=lambda x: x[1][0])
        #results = list()
        #for resource_key,resource_tuple in resource_tuples:
        #    _, _, exists, operation_done = resource_tuple
        #    desired_operation = 'update' if exists else 'replace'
        #
        #    if operation_done == UpdateResult.INVALID:
        #        value = Exception('Invalid')
        #    elif operation_done == UpdateResult.DELETE:
        #        value = Exception('Unexpected Delete')
        #    elif operation_done == UpdateResult.REPLACE:
        #        value = True if desired_operation == 'replace' else Exception('Failed')
        #    elif operation_done == UpdateResult.UPDATE:
        #        value = True if desired_operation == 'update' else Exception('Failed')
        #    else:
        #        value = Exception('Unexpected')
        #    results.append((resource_key, value))
        return results

    def delete(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        #resource_keys = [key for key,_ in resources]
        #current_values = self.get(resource_keys)

        #resource_tuples = {
        #    resource_key : [i, value, value_exists(value), None]
        #    for i,(resource_key,value) in enumerate(current_values)
        #}

        #self._logger.info('---0')
        #self._logger.info(str(resource_tuples))

        set_request = SetRequest()
        #for resource_key in resource_keys:
        for resource_key, resource_value in resources:
            self._logger.info('---1')
            self._logger.info(str(resource_key))
            self._logger.info(str(resource_value))
            #resource_tuple = resource_tuples.get(resource_key)
            #if resource_tuple is None: continue
            #_, value, exists, operation_done = resource_tuple
            #if not exists: continue
            if isinstance(resource_value, str): resource_value = json.loads(resource_value)
            str_path, str_data = compose(resource_key, resource_value, delete=True)
            self._logger.info('---3')
            self._logger.info(str(str_path))
            self._logger.info(str(str_data))
            set_request_entry = set_request.delete.add()
            set_request_entry.CopyFrom(path_from_string(str_path))

        self._logger.info('set_request={:s}'.format(grpc_message_to_json_string(set_request)))
        metadata = [('username', self._username), ('password', self._password)]
        timeout = None # GNMI_SUBSCRIPTION_TIMEOUT = int(sampling_duration)
        set_reply = self._stub.Set(set_request, metadata=metadata, timeout=timeout)
        self._logger.info('set_reply={:s}'.format(grpc_message_to_json_string(set_reply)))

        results = []
        for (resource_key, resource_value), update_result in zip(resources, set_reply.response):
            operation = update_result.op
            if operation == UpdateResult.DELETE:
                results.append((resource_key, True))
            else:
                results.append((resource_key, Exception('Unexpected')))

            #str_path = path_to_string(update_result.path)
            #resource_tuple = resource_tuples.get(str_path)
            #if resource_tuple is None: continue
            #resource_tuple[3] = operation

        #resource_tuples = sorted(resource_tuples.items(), key=lambda x: x[1][0])
        #results = list()
        #for resource_key,resource_tuple in resource_tuples:
        #    _, _, exists, operation_done = resource_tuple
        #    if operation_done == UpdateResult.INVALID:
        #        value = Exception('Invalid')
        #    elif operation_done == UpdateResult.DELETE:
        #        value = True
        #    elif operation_done == UpdateResult.REPLACE:
        #        value = Exception('Unexpected Replace')
        #    elif operation_done == UpdateResult.UPDATE:
        #        value = Exception('Unexpected Update')
        #    else:
        #        value = Exception('Unexpected')
        #    results.append((resource_key, value))
        return results

    def subscribe(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        results = []
        for i,subscription in enumerate(subscriptions):
            str_subscription_name = 'subscriptions[#{:d}]'.format(i)
            try:
                chk_type(str_subscription_name, subscription, (list, tuple))
                chk_length(str_subscription_name, subscription, min_length=3, max_length=3)
                resource_key, sampling_duration, sampling_interval = subscription
                chk_string(str_subscription_name + '.resource_key', resource_key, allow_empty=False)
                chk_float(str_subscription_name + '.sampling_duration', sampling_duration, min_value=0)
                chk_float(str_subscription_name + '.sampling_interval', sampling_interval, min_value=0)
            except Exception as e: # pylint: disable=broad-except
                MSG = 'Exception validating {:s}: {:s}'
                self._logger.exception(MSG.format(str_subscription_name, str(resource_key)))
                results.append(e) # if validation fails, store the exception
                continue

            #resource_path = resource_key.split('/')
            #self._subscriptions.add(resource_path, sampling_duration, sampling_interval, reference)
            subscription = 'subscribe', resource_key, sampling_duration, sampling_interval
            self._in_subscriptions.put_nowait(subscription)
            results.append(True)
        return results

    def unsubscribe(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        results = []
        for i,subscription in enumerate(subscriptions):
            str_subscription_name = 'subscriptions[#{:d}]'.format(i)
            try:
                chk_type(str_subscription_name, subscription, (list, tuple))
                chk_length(str_subscription_name, subscription, min_length=3, max_length=3)
                resource_key, sampling_duration, sampling_interval = subscription
                chk_string(str_subscription_name + '.resource_key', resource_key, allow_empty=False)
                chk_float(str_subscription_name + '.sampling_duration', sampling_duration, min_value=0)
                chk_float(str_subscription_name + '.sampling_interval', sampling_interval, min_value=0)
            except Exception as e: # pylint: disable=broad-except
                MSG = 'Exception validating {:s}: {:s}'
                self._logger.exception(MSG.format(str_subscription_name, str(resource_key)))
                results.append(e) # if validation fails, store the exception
                continue

            #resource_path = resource_key.split('/')
            #reference = self._subscriptions.get(resource_path, sampling_duration, sampling_interval)
            #if reference is None:
            #    results.append(False)
            #    continue
            #self._subscriptions.delete(reference)
            subscription = 'unsubscribe', resource_key, sampling_duration, sampling_interval
            self._in_subscriptions.put_nowait(subscription)
            results.append(True)
        return results
