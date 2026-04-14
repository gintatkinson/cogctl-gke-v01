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
from typing import Any, List, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_string, chk_type
from device.service.driver_api._Driver import _Driver, RESOURCE_ENDPOINTS
from device.service.drivers.ryu import ALL_RESOURCE_KEYS
from .RyuApiClient import RyuApiClient

LOGGER = logging.getLogger(__name__)

DRIVER_NAME = 'ryu'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class RyuDriver(_Driver):
    def __init__(self, address: str, port: int, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.rac = RyuApiClient(
            self.address, int(self.port),
            scheme   = self.settings.get('scheme', 'http'),
            username = self.settings.get('username'),
            password = self.settings.get('password'),
            timeout  = self.settings.get('timeout', 30),
        )

    def Connect(self) -> bool:
        with self.__lock:
            connected = self.rac.check_credentials()
            if connected: self.__started.set()
            return connected

    def Disconnect(self) -> bool:
        with self.__lock:
            self.__terminate.set()
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return []
        
    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys: List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = []
        with self.__lock:
            if len(resource_keys) == 0: resource_keys = ALL_RESOURCE_KEYS
            for i, resource_key in enumerate(resource_keys):
                str_resource_name = 'resource_key[#{:d}]'.format(i)
                try:
                    chk_string(str_resource_name, resource_key, allow_empty=False)
                    if resource_key == RESOURCE_ENDPOINTS:
                        results.extend(self.rac.get_devices_endpoints())
                except Exception as e:
                    LOGGER.exception('Unhandled error processing resource_key({:s})'.format(str(resource_key)))
                    results.append((resource_key, e))
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        results = []
        if not resources: return results
        with self.__lock:
            for resource in resources:
                try:
                    resource_key, resource_value = resource
                    if not resource_key.startswith("/device[") or not "/flow[" in resource_key:
                        LOGGER.error(f"Invalid resource_key format: {resource_key}")
                        results.append(Exception(f"Invalid resource_key format: {resource_key}"))
                        continue

                    try:
                        resource_value_dict = json.loads(resource_value)
                        LOGGER.debug('resource_value_dict = {:s}'.format(str(resource_value_dict)))
                        dpid = int(resource_value_dict["dpid"], 16)
                        in_port = int(resource_value_dict["in-port"].split("-")[1][3:])
                        out_port = int(resource_value_dict["out-port"].split("-")[1][3:])
                        ip_src_addr = resource_value_dict.get("ip_address_source", "")
                        ip_dst_addr = resource_value_dict.get("ip_address_destination", "")

                        if "h1-h3" in resource_key:
                            priority = 1000
                        elif "h3-h1" in resource_key:
                            priority = 1000
                        elif "h2-h4" in resource_key:
                            priority = 1500
                        elif "h4-h2" in resource_key:
                            priority = 1500
                        else:
                            priority = 65535
                    except (KeyError, ValueError, IndexError) as e:
                        MSG = "Error processing resource {:s}"
                        LOGGER.exception(MSG.format(str(resource)))
                        results.append(e)
                        continue

                    results.append(self.rac.add_flow_rule(
                        dpid, in_port, out_port, 0x0800, ip_src_addr, ip_dst_addr,
                        priority=priority
                    ))
                except Exception as e:
                    MSG = "Error processing resource {:s}"
                    LOGGER.exception(MSG.format(str(resource)))
                    results.append(e)
        return results
    
    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        LOGGER.info("[DeleteConfig] resources = {:s}".format(str(resources)))
        
        results = []
        if not resources:
            return results
        with self.__lock:
            for resource in resources:
                try:
                    resource_key, resource_value = resource

                    if not resource_key.startswith("/device[") or not "/flow[" in resource_key:
                        LOGGER.error(f"Invalid resource_key format: {resource_key}")
                        results.append(Exception(f"Invalid resource_key format: {resource_key}"))
                        continue

                    try:
                        resource_value_dict = json.loads(resource_value)
                        LOGGER.debug('resource_value_dict = {:s}'.format(str(resource_value_dict)))
                        dpid = int(resource_value_dict["dpid"], 16)
                        in_port = int(resource_value_dict["in-port"].split("-")[1][3:])
                        out_port = int(resource_value_dict["out-port"].split("-")[1][3:])
                        ip_src_addr = resource_value_dict.get("ip_address_source", "")
                        ip_dst_addr = resource_value_dict.get("ip_address_destination", "")

                        if "h1-h3" in resource_key:
                            priority = 1000
                        elif "h3-h1" in resource_key:
                            priority = 1000
                        elif "h2-h4" in resource_key:
                            priority = 1500
                        elif "h4-h2" in resource_key:
                            priority = 1500
                        else:
                            priority = 65535
                    except (KeyError, ValueError, IndexError) as e:
                        MSG = "Error processing resource {:s}"
                        LOGGER.exception(MSG.format(str(resource)))
                        results.append(e)
                        continue

                    results.append(self.rac.del_flow_rule(
                        dpid, in_port, out_port, 0x0800, ip_src_addr, ip_dst_addr,
                        priority=priority
                    ))
                except Exception as e:
                    MSG = "Error processing resource {:s}"
                    LOGGER.exception(MSG.format(str(resource)))
                    results.append(e)

        return results
