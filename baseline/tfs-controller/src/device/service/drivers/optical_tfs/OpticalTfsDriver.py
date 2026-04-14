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


import json, logging, threading
from typing import Any, Iterator, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import _Driver, RESOURCE_ENDPOINTS, RESOURCE_SERVICES
from device.service.driver_api.ImportTopologyEnum import ImportTopologyEnum, get_import_topology
from .TfsApiClient import TfsApiClient
#from .TfsOpticalClient import TfsOpticalClient

LOGGER = logging.getLogger(__name__)

ALL_RESOURCE_KEYS = [
    RESOURCE_ENDPOINTS,
    RESOURCE_SERVICES,
]

DRIVER_NAME = 'optical_tfs'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class OpticalTfsDriver(_Driver):
    def __init__(self, address : str, port : str, **settings) -> None:
        super().__init__(DRIVER_NAME, address, int(port), **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        username = self.settings.get('username')
        password = self.settings.get('password')
        scheme   = self.settings.get('scheme', 'http')
        timeout  = int(self.settings.get('timeout', 60))
        self.tac = TfsApiClient(
            self.address, self.port, scheme=scheme, username=username,
            password=password, timeout=timeout
        )
        #self.toc = TfsOpticalClient(
        #    self.address, int(self.port), scheme=scheme, username=username,
        #    password=password, timeout=timeout
        #)

        # Options are:
        #    disabled --> just import endpoints as usual
        #    devices  --> imports sub-devices but not links connecting them.
        #                 (a remotely-controlled transport domain might exist between them)
        #    topology --> imports sub-devices and links connecting them.
        #                 (not supported by XR driver)
        self.__import_topology = get_import_topology(self.settings, default=ImportTopologyEnum.TOPOLOGY)

    def Connect(self) -> bool:
        with self.__lock:
            if self.__started.is_set(): return True
            try:
                self.tac.check_credentials()
            except:     # pylint: disable=bare-except
                LOGGER.exception('Exception checking credentials')
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
    def GetConfig(
        self, resource_keys : List[str] = []
    ) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = []
        with self.__lock:
            self.tac.check_credentials()
            if len(resource_keys) == 0: resource_keys = ALL_RESOURCE_KEYS
            for i, resource_key in enumerate(resource_keys):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                try:
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    if resource_key == RESOURCE_ENDPOINTS:
                        # return endpoints through TFS NBI API and list-devices method
                        results.extend(self.tac.get_devices_endpoints(self.__import_topology))
                    elif resource_key == RESOURCE_SERVICES:
                        # return all services through
                        results.extend(self.tac.get_services())
                    else:
                        MSG = 'ResourceKey({:s}) not implemented'
                        LOGGER.warning(MSG.format(str(resource_key)))
                except Exception as e:
                    MSG = 'Unhandled error processing {:s}: resource_key({:s})'
                    LOGGER.exception(MSG.format(str_resource_name, str(resource_key)))
                    results.append((resource_key, e))
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(
        self, resources : List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            self.tac.check_credentials()
            for resource in resources:
                LOGGER.info('resource = {:s}'.format(str(resource)))
                resource_key, resource_value = resource
                try:
                    resource_value = json.loads(resource_value)
                    self.tac.setup_service(resource_value)
                    results.append((resource_key, True))
                except Exception as e:
                    MSG = 'Unhandled error processing resource_key({:s})'
                    LOGGER.exception(MSG.format(str(resource_key)))
                    results.append((resource_key, e))
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(
        self, resources : List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            self.tac.check_credentials()
            for resource in resources:
                LOGGER.info('resource = {:s}'.format(str(resource)))
                resource_key,resource_value = resource
                try:
                    resource_value = json.loads(resource_value)
                    self.tac.teardown_service(resource_value)
                    results.append((resource_key, True))
                except Exception as e:
                    MSG = 'Unhandled error processing resource_key({:s})'
                    LOGGER.exception(MSG.format(str(resource_key)))
                    results.append((resource_key, e))
        return results

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(
        self, subscriptions : List[Tuple[str, float, float]]
    ) -> List[Union[bool, Exception]]:
        # TODO: does not support monitoring by now
        return [False for _ in subscriptions]

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(
        self, subscriptions : List[Tuple[str, float, float]]
    ) -> List[Union[bool, Exception]]:
        # TODO: does not support monitoring by now
        return [False for _ in subscriptions]

    def GetState(
        self, blocking=False, terminate : Optional[threading.Event] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        # TODO: does not support monitoring by now
        return []
