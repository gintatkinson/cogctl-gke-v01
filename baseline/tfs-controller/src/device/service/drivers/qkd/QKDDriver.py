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

import json, logging, requests, threading
from requests.auth import HTTPBasicAuth
from typing import Any, Iterator, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import _Driver
from . import ALL_RESOURCE_KEYS
from .Tools import find_key, config_getter, create_connectivity_link

LOGGER = logging.getLogger(__name__)

DRIVER_NAME = 'qkd'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})


class QKDDriver(_Driver):
    def __init__(self, address: str, port: int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        username = self.settings.get('username')
        password = self.settings.get('password')
        self.__auth = HTTPBasicAuth(username, password) if username is not None and password is not None else None
        scheme = self.settings.get('scheme', 'http')
        self.__qkd_root = '{:s}://{:s}:{:d}'.format(scheme, self.address, int(self.port))
        self.__timeout = int(self.settings.get('timeout', 120))
        self.__node_ids = set(self.settings.get('node_ids', []))
        token = self.settings.get('token')
        self.__headers = {'Authorization': 'Bearer ' + token}
        self.__initial_data = None

    def Connect(self) -> bool:
        url = self.__qkd_root + '/restconf/data/etsi-qkd-sdn-node:qkd_node'
        with self.__lock:
            if self.__started.is_set(): return True
            r = None
            try:
                LOGGER.info(f'requests.get("{url}", timeout={self.__timeout}, verify=False, auth={self.__auth}, headers={self.__headers})')
                r = requests.get(url, timeout=self.__timeout, verify=False, auth=self.__auth, headers=self.__headers)
                LOGGER.info(f'R: {r}')
                LOGGER.info(f'Text: {r.text}')
                LOGGER.info(f'Json: {r.json()}')
            except requests.exceptions.Timeout:
                LOGGER.exception('Timeout connecting {:s}'.format(str(self.__qkd_root)))
                return False
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception('Exception connecting {:s}'.format(str(self.__qkd_root)))
                return False
            else:
                self.__started.set()
                self.__initial_data = r.json()
                return True

    def Disconnect(self) -> bool:
        with self.__lock:
            self.__terminate.set()
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return self.__initial_data

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
                    self.__qkd_root, resource_key, timeout=self.__timeout, auth=self.__auth,
                    node_ids=self.__node_ids, headers=self.__headers))
        return results


    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0:
            return results
        with self.__lock:
            for resource_key, resource_value in resources:
                LOGGER.info('resource = {:s}'.format(str(resource_key)))

                if resource_key.startswith('/link'):
                    try:
                        resource_value = json.loads(resource_value)
                        link_uuid = resource_value['uuid']

                        node_id_src      = resource_value['src_qkdn_id']
                        interface_id_src = resource_value['src_interface_id']
                        node_id_dst      = resource_value['dst_qkdn_id']
                        interface_id_dst = resource_value['dst_interface_id']
                        virt_prev_hop    = resource_value.get('virt_prev_hop')
                        virt_next_hops   = resource_value.get('virt_next_hops')
                        virt_bandwidth   = resource_value.get('virt_bandwidth')


                        data = create_connectivity_link(
                            self.__qkd_root, link_uuid, node_id_src, interface_id_src, node_id_dst, interface_id_dst, 
                            virt_prev_hop, virt_next_hops, virt_bandwidth,
                            timeout=self.__timeout, auth=self.__auth, headers=self.__headers
                        )

                        #data = create_connectivity_link(
                        #    self.__qkd_root, link_uuid, node_id_src, interface_id_src, node_id_dst, interface_id_dst, 
                        #    timeout=self.__timeout, auth=self.__auth
                        #)
                        results.append(True)
                    except Exception as e: # pylint: disable=broad-except
                        LOGGER.exception('Unhandled error processing resource_key({:s})'.format(str(resource_key)))
                        results.append(e)
                else:
                    results.append(True)

        LOGGER.info('Test keys: ' + str([x for x,y in resources]))
        LOGGER.info('Test values: ' + str(results))
        return results

    '''
    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            for resource in resources:
                LOGGER.info('resource = {:s}'.format(str(resource)))
                uuid = find_key(resource, 'uuid')
                results.extend(delete_connectivity_service(
                    self.__qkd_root, uuid, timeout=self.__timeout, auth=self.__auth))
        return results
    '''

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: QKD API Driver does not support monitoring by now
        LOGGER.info(f'Subscribe {self.address}: {subscriptions}')
        return [True for _ in subscriptions]

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: QKD API Driver does not support monitoring by now
        return [False for _ in subscriptions]

    def GetState(
        self, blocking=False, terminate : Optional[threading.Event] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        # TODO: QKD API Driver does not support monitoring by now
        LOGGER.info(f'GetState {self.address} called')
        return []
