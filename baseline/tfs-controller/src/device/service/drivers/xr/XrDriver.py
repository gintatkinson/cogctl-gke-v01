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
#pylint: disable=invalid-name, missing-function-docstring, line-too-long, logging-fstring-interpolation, missing-class-docstring, missing-module-docstring

import logging
import threading
import json
from typing import Any, Iterator, List, Optional, Set, Tuple, Union
import urllib3
from common.DeviceTypes import DeviceTypeEnum
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import DeviceDriverEnum, DeviceOperationalStatusEnum
from common.type_checkers.Checkers import chk_type
from device.service.driver_api.ImportTopologyEnum import ImportTopologyEnum, get_import_topology
from device.service.driver_api._Driver import _Driver
from .cm.cm_connection import CmConnection, ConsistencyMode
from .cm import tf

# Don't complain about non-verified SSL certificate. This driver is demo only
# and CM is not provisioned in demos with a proper certificate.
urllib3.disable_warnings()

LOGGER = logging.getLogger(__name__)

DRIVER_NAME = 'xr'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class XrDriver(_Driver):
    def __init__(self, address: str, port: int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.__timeout = int(self.settings.get('timeout', 120))
        self.__cm_address = self.address
        # Mandatory key, an exception will get thrown if missing
        self.__hub_module_name = self.settings["hub_module_name"]

        tls_verify = False # Currently using self signed certificates
        username = self.settings.get("username", "xr-user-1")
        password = self.settings.get("password", "xr-user-1")

        # Options are:
        #    disabled --> just import endpoints as usual
        #    devices  --> imports sub-devices but not links connecting them.
        #                 (a remotely-controlled transport domain might exist between them)
        #    topology --> imports sub-devices and links connecting them.
        #                 (not supported by XR driver)
        self.__import_topology = get_import_topology(self.settings, default=ImportTopologyEnum.DISABLED)

        # Options are:
        #    asynchronous --> operation considered complete when IPM responds with suitable status code,
        #                     including "accepted", that only means request is semantically good and queued.
        #    synchronous  --> operation is considered complete once result is also reflected in GETs in REST API.
        #    lifecycle    --> operation is considered successfull once IPM has completed pluggaable configuration
        #                     or failed in it. This is typically unsuitable for production use
        #                     (as some optics may be transiently unreachable), but is convenient for demos and testin.
        consistency_mode = ConsistencyMode.from_str(self.settings.get("consistency-mode", "asynchronous"))

        self.__cm_connection = CmConnection(self.address, int(self.port), username, password, self.__timeout, tls_verify = tls_verify, consistency_mode=consistency_mode)
        self.__constellation = None

        LOGGER.info(f"XrDriver instantiated, cm {self.address}:{self.port}, consistency mode {str(consistency_mode)}, {self.settings=}")

    def __str__(self):
        return f"{self.__hub_module_name}@{self.__cm_address}"

    def Connect(self) -> bool:
        LOGGER.info(f"Connect[{self}]")
        with self.__lock:
            if self.__started.is_set():
                return True
            if not self.__cm_connection.Connect():
                return False
            else:
                self.__started.set()
                return True

    def Disconnect(self) -> bool:
        LOGGER.info(f"Disconnect[{self}]")
        with self.__lock:
            self.__cm_connection.stop_monitoring_errors()
            self.__terminate.set()
            return True

    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        LOGGER.info(f"GetInitialConfig[{self}]")
        with self.__lock:
            return []

    #pylint: disable=dangerous-default-value
    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        LOGGER.info(f"GetConfig[{self}]: {resource_keys=}")
        chk_type('resources', resource_keys, list)

        # Empty resource_keys means all resources. As we only have endpoints, we ignore parameter and always
        # return everything.

        with self.__lock:
            constellation = self.__cm_connection.get_constellation_by_hub_name(self.__hub_module_name)
            if constellation:
                self.__constellation = constellation
                if self.__import_topology == ImportTopologyEnum.DISABLED:
                    return [
                        (f"/endpoints/endpoint[{ifname}]", {'uuid': ifname, 'type': 'optical', 'sample_types': {}})
                        for ifname in constellation.ifnames()
                    ]
                elif self.__import_topology == ImportTopologyEnum.DEVICES:
                    devices : Set[str] = set()
                    pluggables : Set[str] = set()
                    devices_and_endpoints = []
                    for ifname in constellation.ifnames():
                        device_name,pluggable_name = ifname.split('|')

                        if device_name not in devices:
                            device_url = '/devices/device[{:s}]'.format(device_name)
                            device_data = {
                                'uuid': device_name, 'name': device_name,
                                'type': DeviceTypeEnum.EMULATED_PACKET_ROUTER.value,
                                'status': DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED,
                                'drivers': [DeviceDriverEnum.DEVICEDRIVER_UNDEFINED],
                            }
                            devices_and_endpoints.append((device_url, device_data))

                            for copper_if_index in range(4):
                                copper_ifname = '1/{:d}'.format(copper_if_index + 1)
                                endpoint_url = '/endpoints/endpoint[{:s}]'.format(copper_ifname)
                                endpoint_data = {
                                    'device_uuid': device_name, 'uuid': copper_ifname, 'name': copper_ifname,
                                    'type': 'copper/internal', 'sample_types': {}
                                }
                                devices_and_endpoints.append((endpoint_url, endpoint_data))

                            devices.add(device_name)

                        if ifname not in pluggables:
                            endpoint_url = '/endpoints/endpoint[{:s}]'.format(ifname)
                            if 'hub' in ifname.lower():
                                endpoint_type = 'optical/xr-hub'
                            elif 'leaf' in ifname.lower():
                                endpoint_type = 'optical/xr-leaf'
                            else:
                                endpoint_type = 'optical/xr'
                            endpoint_data = {
                                'device_uuid': device_name, 'uuid': pluggable_name, 'name': pluggable_name,
                                'type': endpoint_type, 'sample_types': {}
                            }
                            devices_and_endpoints.append((endpoint_url, endpoint_data))

                    return devices_and_endpoints
                else:
                    raise Exception('Unsupported import_topology mode: {:s}'.format(str(self.__import_topology)))
            else:
                return []

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        LOGGER.info(f"SetConfig[{self}]: {resources=}")
        # Logged config seems like:
        # Pre-February 2023
        #[('/service[52ff5f0f-fda4-40bd-a0b1-066f4ff04079:optical]', '{"capacity_unit": "GHz", "capacity_value": 1, "direction": "UNIDIRECTIONAL", "input_sip": "XR HUB 1|XR-T4", "layer_protocol_name": "PHOTONIC_MEDIA", "layer_protocol_qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC", "output_sip": "XR LEAF 1|XR-T1", "uuid": "52ff5f0f-fda4-40bd-a0b1-066f4ff04079:optical"}')]
        # Post February 2023
        #[('/services/service[e1b9184c-767d-44b9-bf83-a1f643d82bef]', '{"capacity_unit": "GHz", "capacity_value": 50.0, "direction": "UNIDIRECTIONAL", "input_sip": "XR LEAF 1|XR-T1", "layer_protocol_name": "PHOTONIC_MEDIA", "layer_protocol_qualifier": "tapi-photonic-media:PHOTONIC_LAYER_QUALIFIER_NMC", "output_sip": "XR HUB 1|XR-T4", "uuid": "e1b9184c-767d-44b9-bf83-a1f643d82bef"}')]
        with self.__lock:
            if self.__constellation is None:
                self.__constellation = self.__cm_connection.get_constellation_by_hub_name(self.__hub_module_name)

            if self.__constellation is None:
                LOGGER.error("SetConfig: no valid constellation")
                return [False] * len(resources)

            results = []
            if len(resources) == 0:
                return results

            for key, config in resources:
                service_uuid = self.__cm_connection.service_uuid(key)
                if service_uuid:
                    config = json.loads(config)
                    results.append(tf.set_config_for_service(self.__cm_connection, self.__constellation, service_uuid, config))
                else:
                    results.append(False)

            return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        LOGGER.info(f"DeleteConfig[{self}]: {resources=}")

        # Input looks like:
        #  resources=[('/service[c8a35e81-88d8-4468-9afc-a8abd92a64d0:optical]', '{"uuid": "c8a35e81-88d8-4468-9afc-a8abd92a64d0:optical"}')]

        with self.__lock:
            results = []
            if len(resources) == 0:
                return results

            # Temporary dummy version
            for key, _config in resources:
                service_uuid = self.__cm_connection.service_uuid(key)
                if service_uuid:
                    connection = self.__cm_connection.get_connection_by_teraflow_uuid(service_uuid)
                    if connection is None:
                        LOGGER.info(f"DeleteConfig: Connection {service_uuid} does not exist, delete is no-op")
                        results.append(True)
                    else:
                        was_deleted = self.__cm_connection.delete_connection(connection.href)
                        if was_deleted:
                            LOGGER.info(f"DeleteConfig: Connection {service_uuid} deleted (was {str(connection)})")
                        else:
                            LOGGER.info(f"DeleteConfig: Connection {service_uuid} delete failure (was {str(connection)})")

                        if connection.is_vti_mode():
                            active_tc = self.__cm_connection.get_transport_capacity_by_teraflow_uuid(service_uuid)
                            if active_tc is not None:
                                if self.__cm_connection.delete_transport_capacity(active_tc.href):
                                    LOGGER.info(f"DeleteConfig: Transport Capacity {active_tc} deleted")
                                else:
                                    LOGGER.error(f"DeleteConfig: Transport Capacity {active_tc} delete failure")

                        results.append(was_deleted)
                else:
                    results.append(False)

            return results

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # Not supported
        return [False for _ in subscriptions]

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions : List[Tuple[str, float, float]]) -> List[Union[bool, Exception]]:
        # Not supported
        return [False for _ in subscriptions]

    def GetState(
        self, blocking=False, terminate : Optional[threading.Event] = None
    ) -> Iterator[Tuple[float, str, Any]]:
        # Not supported
        return []
