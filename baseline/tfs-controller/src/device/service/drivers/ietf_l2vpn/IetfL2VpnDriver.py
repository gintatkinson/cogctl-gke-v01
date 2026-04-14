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
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import _Driver, RESOURCE_ENDPOINTS, RESOURCE_SERVICES
from device.service.driver_api.ImportTopologyEnum import ImportTopologyEnum, get_import_topology
from device.service.drivers.ietf_l2vpn.TfsApiClient import TfsApiClient
from .Tools import connection_point, wim_mapping
from .WimconnectorIETFL2VPN import WimconnectorIETFL2VPN

LOGGER = logging.getLogger(__name__)

def service_exists(wim : WimconnectorIETFL2VPN, service_uuid : str) -> bool:
    try:
        wim.get_connectivity_service_status(service_uuid)
        return True
    except: # pylint: disable=bare-except
        return False

ALL_RESOURCE_KEYS = [
    RESOURCE_ENDPOINTS,
    RESOURCE_SERVICES,
]

SERVICE_TYPE = 'ELINE'

DRIVER_NAME = 'ietf_l2vpn'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class IetfL2VpnDriver(_Driver):
    def __init__(self, address: str, port: int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        username = self.settings.get('username')
        password = self.settings.get('password')
        scheme = self.settings.get('scheme', 'http')
        wim = {'wim_url': '{:s}://{:s}:{:d}'.format(scheme, self.address, int(self.port))}
        wim_account = {'user': username, 'password': password}
        # Mapping updated dynamically with each request
        config = {'mapping_not_needed': False, 'service_endpoint_mapping': []}
        self.tac = TfsApiClient(self.address, int(self.port), scheme=scheme, username=username, password=password)
        self.wim = WimconnectorIETFL2VPN(wim, wim_account, config=config)
        self.conn_info = {} # internal database emulating OSM storage provided to WIM Connectors

        # Options are:
        #    disabled --> just import endpoints as usual
        #    devices  --> imports sub-devices but not links connecting them.
        #                 (a remotely-controlled transport domain might exist between them)
        #    topology --> imports sub-devices and links connecting them.
        #                 (not supported by XR driver)
        self.__import_topology = get_import_topology(self.settings, default=ImportTopologyEnum.DEVICES)

    def Connect(self) -> bool:
        with self.__lock:
            if self.__started.is_set(): return True
            try:
                self.wim.check_credentials()
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
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = []
        with self.__lock:
            self.wim.check_credentials()
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
                        reply = self.wim.get_all_active_connectivity_services()
                        results.extend(reply.json())
                    else:
                        # assume single-service retrieval
                        reply = self.wim.get_connectivity_service(resource_key)
                        results.append(reply.json())
                except Exception as e: # pylint: disable=broad-except
                    LOGGER.exception('Unhandled error processing resource_key({:s})'.format(str(resource_key)))
                    results.append((resource_key, e))
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            self.wim.check_credentials()
            for resource in resources:
                LOGGER.info('resource = {:s}'.format(str(resource)))
                resource_key,resource_value = resource
                try:
                    resource_value = json.loads(resource_value)
                    service_uuid = resource_value['uuid']

                    if service_exists(self.wim, service_uuid):
                        exc = NotImplementedError('IETF L2VPN Service Update is still not supported')
                        results.append((resource[0], exc))
                        continue

                    src_device_name   = resource_value['src_device_name']
                    src_endpoint_name = resource_value['src_endpoint_name']
                    dst_device_name   = resource_value['dst_device_name']
                    dst_endpoint_name = resource_value['dst_endpoint_name']
                    encap_type        = resource_value['encapsulation_type']
                    vlan_id           = resource_value['vlan_id']

                    src_endpoint_id = json_endpoint_id(json_device_id(src_device_name), src_endpoint_name)
                    src_service_endpoint_id, src_mapping = wim_mapping('1', src_endpoint_id)
                    self.wim.mappings[src_service_endpoint_id] = src_mapping

                    dst_endpoint_id = json_endpoint_id(json_device_id(dst_device_name), dst_endpoint_name)
                    dst_service_endpoint_id, dst_mapping = wim_mapping('2', dst_endpoint_id)
                    self.wim.mappings[dst_service_endpoint_id] = dst_mapping

                    connection_points = [
                        connection_point(src_service_endpoint_id, encap_type, vlan_id),
                        connection_point(dst_service_endpoint_id, encap_type, vlan_id),
                    ]

                    self.wim.create_connectivity_service(service_uuid, SERVICE_TYPE, connection_points)
                    results.append((resource_key, True))
                except Exception as e: # pylint: disable=broad-except
                    LOGGER.exception('Unhandled error processing resource_key({:s})'.format(str(resource_key)))
                    results.append((resource_key, e))
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if len(resources) == 0: return results
        with self.__lock:
            self.wim.check_credentials()
            for resource in resources:
                LOGGER.info('resource = {:s}'.format(str(resource)))
                resource_key,resource_value = resource
                try:
                    resource_value = json.loads(resource_value)
                    service_uuid = resource_value['uuid']

                    if service_exists(self.wim, service_uuid):
                        self.wim.delete_connectivity_service(service_uuid)
                    results.append((resource_key, True))
                except Exception as e: # pylint: disable=broad-except
                    LOGGER.exception('Unhandled error processing resource_key({:s})'.format(str(resource_key)))
                    results.append((resource_key, e))
        return results

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: IETF L2VPN does not support monitoring by now
        return [False for _ in subscriptions]

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # TODO: IETF L2VPN does not support monitoring by now
        return [False for _ in subscriptions]

    def GetState(
        self, blocking=False, terminate : Optional[threading.Event] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        # TODO: IETF L2VPN does not support monitoring by now
        return []
