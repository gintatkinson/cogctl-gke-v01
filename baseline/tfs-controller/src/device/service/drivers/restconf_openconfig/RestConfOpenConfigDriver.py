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


import copy, json, logging, re, requests, threading
from typing import Any, Iterator, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import (
    _Driver, RESOURCE_ACL, RESOURCE_ENDPOINTS, RESOURCE_INTERFACES
)
from .handlers.ComponentsHandler import ComponentsHandler
from .handlers.AclRuleSetHandler import AclRuleSetHandler


ALL_RESOURCE_KEYS = [
    RESOURCE_ACL,
    RESOURCE_ENDPOINTS,
    RESOURCE_INTERFACES,
]


RE_ACL_RULESET = re.compile(
    r'^\/device\[([^\]]+)\]\/endpoint\[([^\]]+)\]\/acl\_ruleset\[([^\]]+)\]$'
)

def parse_resource_key(resource_key : str) -> Optional[Tuple[str, str, str]]:
    re_match_acl_ruleset = RE_ACL_RULESET.match(resource_key)
    if re_match_acl_ruleset is None: return None
    device_key, endpoint_key, acl_ruleset_name = re_match_acl_ruleset.groups()
    return device_key, endpoint_key, acl_ruleset_name



DRIVER_NAME = 'restconf_openconfig'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})


class RestConfOpenConfigDriver(_Driver):
    def __init__(self, address : str, port : int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        logger_prefix = '{:s}:[{:s}:{:s}]'.format(
            str(__name__), str(self.address), str(self.port)
        )
        self.__logger = logging.getLogger(logger_prefix)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()

        restconf_settings = copy.deepcopy(settings)
        restconf_settings['logger'] = logging.getLogger(logger_prefix + '.RestConfClient_v1')

        self._rest_conf_client = RestConfClient(address, port=port, **restconf_settings)
        self._handler_components = ComponentsHandler(self._rest_conf_client)
        self._handler_acl_ruleset = AclRuleSetHandler(self._rest_conf_client)

    def Connect(self) -> bool:
        with self.__lock:
            if self.__started.is_set(): return True
            try:
                self._rest_conf_client._discover_base_url()
            except requests.exceptions.Timeout:
                self.__logger.exception('Timeout exception checking connectivity')
                return False
            except Exception:  # pylint: disable=broad-except
                self.__logger.exception('Unhandled exception checking connectivity')
                return False
            else:
                self.__started.set()
                return True

    def Disconnect(self) -> bool:
        with self.__lock:
            self.__terminate.set()
            if not self.__started.is_set(): return True
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return []

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = list()
        with self.__lock:
            if len(resource_keys) == 0: resource_keys = ALL_RESOURCE_KEYS
            for i, resource_key in enumerate(resource_keys):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                try:
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    if resource_key == RESOURCE_ENDPOINTS:
                        results.extend(self._handler_components.get())
                    elif resource_key == RESOURCE_ACL:
                        results.extend(self._handler_acl_ruleset.get())
                    else:
                        parts = parse_resource_key(resource_key)
                        if parts is None: continue
                        device_key, endpoint_key, acl_ruleset_name = parts
                        results.extend(self._handler_acl_ruleset.get(acl_ruleset_name=acl_ruleset_name))
                except Exception as e:
                    MSG = 'Error processing resource_key({:s}, {:s})'
                    self.__logger.exception(MSG.format(str_resource_name, str(resource_key)))
                    results.append((resource_key, e))  # if processing fails, store the exception

        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []

        results = []
        with self.__lock:
            for resource_key, resource_value in resources:
                self.__logger.info('resource: key({:s}) => value({:s})'.format(str(resource_key), str(resource_value)))
                try:
                    if isinstance(resource_value, str): resource_value = json.loads(resource_value)
                    if parse_resource_key(resource_key) is None: continue
                    results.append(self._handler_acl_ruleset.update(resource_value))
                except Exception as e:
                    results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []

        results = []
        with self.__lock:
            for resource_key, resource_value in resources:
                self.__logger.info('resource: key({:s}) => value({:s})'.format(str(resource_key), str(resource_value)))
                try:
                    #if isinstance(resource_value, str): resource_value = json.loads(resource_value)
                    resource_key_parts = parse_resource_key(resource_key)
                    if resource_key_parts is None: continue
                    _, _, acl_ruleset_name = resource_key_parts
                    results.append(self._handler_acl_ruleset.delete(acl_ruleset_name))
                except Exception as e:
                    results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: RESTCONF OPENCONFIG does not support monitoring by now
        return [False for _ in subscriptions]

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: RESTCONF OPENCONFIG does not support monitoring by now
        return [False for _ in subscriptions]

    def GetState(
        self, blocking=False, terminate : Optional[threading.Event] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        # TODO: RESTCONF OPENCONFIG does not support monitoring by now
        return []
