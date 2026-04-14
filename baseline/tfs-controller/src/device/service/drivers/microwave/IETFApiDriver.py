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

import logging, requests, threading
from requests.auth import HTTPBasicAuth
from typing import Any, Iterator, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import _Driver
from . import ALL_RESOURCE_KEYS
from .Tools import create_connectivity_service, find_key, config_getter, delete_connectivity_service

LOGGER = logging.getLogger(__name__)

DRIVER_NAME = 'microwave'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class IETFApiDriver(_Driver):
    def __init__(self, address: str, port: int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        username = self.settings.get('username')
        password = self.settings.get('password')
        self.__auth = HTTPBasicAuth(username, password) if username is not None and password is not None else None
        scheme = self.settings.get('scheme', 'http')
        self.__ietf_root = '{:s}://{:s}:{:d}'.format(scheme, self.address, int(self.port))
        self.__timeout = int(self.settings.get('timeout', 120))
        self.__node_ids = set(self.settings.get('node_ids', []))

    def Connect(self) -> bool:
        url = self.__ietf_root + '/nmswebs/restconf/data/ietf-network:networks'
        with self.__lock:
            if self.__started.is_set(): return True
            try:
                requests.get(url, timeout=self.__timeout, verify=False, auth=self.__auth)
            except requests.exceptions.Timeout:
                LOGGER.exception('Timeout connecting {:s}'.format(str(self.__ietf_root)))
                return False
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception('Exception connecting {:s}'.format(str(self.__ietf_root)))
                return False
            else:
                self.__started.set()
                return True

    def Disconnect(self) -> bool:
        with self.__lock:
            self.__terminate.set()
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return []

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = []
        with self.__lock:
            if len(resource_keys) == 0: resource_keys = ALL_RESOURCE_KEYS
            for i, resource_key in enumerate(resource_keys):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                chk_string(str_resource_name, resource_key, allow_empty=False)
                results.extend(config_getter(
                    self.__ietf_root, resource_key, timeout=self.__timeout, auth=self.__auth,
                    node_ids=self.__node_ids))
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0:
            return results
        with self.__lock:
            for resource in resources:
                LOGGER.info('resource = {:s}'.format(str(resource)))

                node_id_src = find_key(resource, 'node_id_src')
                tp_id_src = find_key(resource, 'tp_id_src')
                node_id_dst = find_key(resource, 'node_id_dst')
                tp_id_dst = find_key(resource, 'tp_id_dst')
                vlan_id = find_key(resource, 'vlan_id')
                uuid = find_key(resource, 'uuid')

                data = create_connectivity_service(
                    self.__ietf_root, uuid, node_id_src, tp_id_src, node_id_dst, tp_id_dst, vlan_id,
                    timeout=self.__timeout, auth=self.__auth)
                results.extend(data)
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            for resource in resources:
                LOGGER.info('resource = {:s}'.format(str(resource)))
                uuid = find_key(resource, 'uuid')
                results.extend(delete_connectivity_service(
                    self.__ietf_root, uuid, timeout=self.__timeout, auth=self.__auth))
        return results

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: IETF API Driver does not support monitoring by now
        return [False for _ in subscriptions]

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: IETF API Driver does not support monitoring by now
        return [False for _ in subscriptions]

    def GetState(
        self, blocking=False, terminate : Optional[threading.Event] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        # TODO: IETF API Driver does not support monitoring by now
        return []
