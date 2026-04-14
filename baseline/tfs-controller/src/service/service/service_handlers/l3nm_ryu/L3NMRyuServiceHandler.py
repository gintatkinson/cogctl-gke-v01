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

import json, logging, re
from typing import List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, Device, DeviceId, EndPoint, Service
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api.Tools import get_device_endpoint_uuids, get_endpoint_matching
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.task_scheduler.TaskExecutor import TaskExecutor

logging.basicConfig(level=logging.DEBUG)  
LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'l3nm_ryu'})

class L3NMRyuServiceHandler(_ServiceHandler):
    def __init__(   # pylint: disable=super-init-not-called
        self, service : Service, task_executor : TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(service.service_config, **settings)

    def _get_endpoint_details(
        self, endpoint : Tuple[str, str, Optional[str]]
    ) -> Tuple[Device, EndPoint]: #Dict]:
        device_uuid, endpoint_uuid = get_device_endpoint_uuids(endpoint)
        device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
        endpoint_obj = get_endpoint_matching(device_obj, endpoint_uuid)
        device_name = device_obj.name
        endpoint_name = endpoint_obj.name
        return device_obj, endpoint_obj 

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('endpoints = {:s}'.format(str(endpoints)))
        chk_type('endpoints', endpoints, list)

        if len(endpoints) < 2:
            LOGGER.warning('nothing done: not enough endpoints')
            return []
        
        service_uuid = self.__service.service_id.service_uuid.uuid
        service_name= self.__service.name
        service_configuration_rules=self.__service.service_config.config_rules
        LOGGER.debug('service_configuration_rules = {:s}'.format(str(service_configuration_rules)))
        ip_addresses = []
        flow_rules = []

        for rule in service_configuration_rules:
            try:
                custom_field = rule.custom
                resource_value_str = custom_field.resource_value
                resource_value = json.loads(resource_value_str)
                resource_key_str = custom_field.resource_key
                LOGGER.debug(f"resource_key_str = {resource_key_str}")
                match = re.search(r"/device\[(.*?)\]/", resource_key_str)
                if match:
                    device_name = match.group(1)
                    flow_rules.append(device_name)
                ip_address = resource_value.get("ip_address")
                ip_addresses.append(ip_address)

            except Exception as e:
                LOGGER.exception("Error in Rules")

        LOGGER.debug('ip_address = {:s}'.format(str(ip_addresses)))
        LOGGER.debug('flow_rules = {:s}'.format(str(flow_rules)))
        if len(flow_rules) < 2:
            LOGGER.warning('Not enough devices to construct flow rules')
            return []
        if len(ip_addresses) < 2:
            LOGGER.warning('Not enough IP addresses found')
            return []
        
        results = []
        try:
            src_device, src_endpoint,  = self._get_endpoint_details(endpoints[0])
            dst_device, dst_endpoint,  = self._get_endpoint_details(endpoints[-1])
            src_controller = self.__task_executor.get_device_controller(src_device)
            del src_controller.device_config.config_rules[:] 
            
            for index in range(len(endpoints) - 1):
                current_device, current_endpoint = self._get_endpoint_details(endpoints[index])
                next_device, next_endpoint = self._get_endpoint_details(endpoints[index + 1])
                if current_device.name == next_device.name:
                    in_port_forward = current_endpoint.name  
                    out_port_forward = next_endpoint.name 
                    dpid_src = int(current_device.name)
                    LOGGER.debug(f"DPID source: {dpid_src}")
                    dpid_dst = int(next_device.name)
                    LOGGER.debug(f"DPID destination: {dpid_dst}")
                    flow_rule_forward = f"{flow_rules[0]}-{flow_rules[1]}"  
                    flow_rule_reverse = f"{flow_rules[1]}-{flow_rules[0]}"
                    ip_address_source = ip_addresses[0]
                    ip_address_destination = ip_addresses[1]
                    forward_resource_value = ({"dpid": current_device.name, 
                                               "in-port": in_port_forward, 
                                               "out-port": out_port_forward,
                                                "ip_address_source": ip_address_source,
                                                "ip_address_destination": ip_address_destination,
                                               })
                    forward_rule = json_config_rule_set (
                            resource_key=f"/device[{current_endpoint.name.split('-')[0]}]/flow[{flow_rule_forward}]",
                            resource_value=forward_resource_value
                        )
                    LOGGER.debug(f"Forward configuration rule: {forward_rule}")
                    src_controller.device_config.config_rules.append(ConfigRule(**forward_rule))
                    in_port_reverse = next_endpoint.name         
                    out_port_reverse = current_endpoint.name 
                    reverse_resource_value = {
                        "dpid": current_device.name,
                        "in-port": in_port_reverse,
                        "out-port": out_port_reverse,
                        "ip_address_source": ip_address_destination,
                        "ip_address_destination": ip_address_source,
                    }
                    reverse_rule = json_config_rule_set(
                            resource_key=f"/device[{current_endpoint.name.split('-')[0]}]/flow[{flow_rule_reverse}]",
                            resource_value=reverse_resource_value
                        )
                    LOGGER.debug(f"Reverse configuration rule: {reverse_rule}")
                    src_controller.device_config.config_rules.append(ConfigRule(**reverse_rule))       
                    self.__task_executor.configure_device(src_controller)
                    results.append(True)

            def get_config_rules(controller):
                try:
                    config_rules = controller.device_config.config_rules
                    for rule in config_rules:
                        if rule.HasField("custom"):
                            resource_key = rule.custom.resource_key
                            resource_value = rule.custom.resource_value
                            LOGGER.debug(f"Resource key in config: {resource_key}, Resource value in config: {resource_value}")
                except Exception as e:
                    LOGGER.exception("Error in Configuration Rules")
            get_config_rules(src_controller)
            LOGGER.debug(f"Configuration rules: {src_controller.device_config.config_rules}")
            return results

        except Exception as e:
            LOGGER.exception("Error in SetEndpoint")
            return [e]
        
    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('endpoints_delete = {:s}'.format(str(endpoints)))
        chk_type('endpoints', endpoints, list)
        if len(endpoints) < 2:
            LOGGER.warning('nothing done: not enough endpoints')
            return []
        service_uuid = self.__service.service_id.service_uuid.uuid
        service_name= self.__service.name
        service_configuration_rules=self.__service.service_config.config_rules
        LOGGER.debug('service_configuration_rules = {:s}'.format(str(service_configuration_rules)))
        ip_addresses = []
        flow_rules = []
        for rule in service_configuration_rules:
            try:
                custom_field = rule.custom
                resource_value_str = custom_field.resource_value
                resource_value = json.loads(resource_value_str)
                resource_key_str = custom_field.resource_key
                LOGGER.debug(f"resource_key_str = {resource_key_str}")
                match = re.search(r"/device\[(.*?)\]/", resource_key_str)
                if match:
                    device_name = match.group(1)
                else:
                    device_name = None
                    flow_rules.append(device_name)
                ip_address = resource_value.get("ip_address")
                ip_addresses.append(ip_address)

            except Exception as e:
                LOGGER.exception("Error in Rules")
        LOGGER.debug('ip_address = {:s}'.format(str(ip_addresses)))
        LOGGER.debug('flow_rules = {:s}'.format(str(flow_rules)))
        results = []
        try:
            src_device, src_endpoint,  = self._get_endpoint_details(endpoints[0])
            dst_device, dst_endpoint,  = self._get_endpoint_details(endpoints[-1])
            src_controller = self.__task_executor.get_device_controller(src_device)
            del src_controller.device_config.config_rules[:]
            for index in range(len(endpoints) - 1):
                current_device, current_endpoint = self._get_endpoint_details(endpoints[index])
                next_device, next_endpoint = self._get_endpoint_details(endpoints[index + 1])
                if current_device.name == next_device.name:
                    in_port_forward = current_endpoint.name  
                    out_port_forward = next_endpoint.name 
                    dpid_src = int(current_device.name)
                    LOGGER.debug(f"DPID source: {dpid_src}")
                    dpid_dst = int(next_device.name)
                    LOGGER.debug(f"DPID destination: {dpid_dst}")
                    flow_rule_forward = f"{flow_rules[0]}-{flow_rules[1]}"  
                    flow_rule_reverse = f"{flow_rules[1]}-{flow_rules[0]}"
                    ip_address_source = ip_addresses[0]
                    ip_address_destination = ip_addresses[1]

                    forward_resource_value = ({"dpid": current_device.name, 
                                               "in-port": in_port_forward, 
                                               "out-port": out_port_forward,
                                                "ip_address_source": ip_address_source,
                                                "ip_address_destination": ip_address_destination,
                                               })
                    forward_rule = json_config_rule_delete (
                            resource_key=f"/device[{current_endpoint.name.split('-')[0]}]/flow[{flow_rule_forward}]",
                            resource_value=forward_resource_value
                        )
                    
                    LOGGER.debug(f"Forward configuration rule: {forward_rule}")
                    in_port_reverse = next_endpoint.name         
                    out_port_reverse = current_endpoint.name 
                    reverse_resource_value = {
                        "dpid": current_device.name,
                        "in-port": in_port_reverse,
                        "out-port": out_port_reverse,
                        "ip_address_source": ip_address_destination,
                        "ip_address_destination": ip_address_source,
                    }
                    reverse_rule = json_config_rule_delete(
                            resource_key=f"/device[{current_endpoint.name.split('-')[0]}]/flow[{flow_rule_reverse}]",
                            resource_value=reverse_resource_value
                        )
                    LOGGER.debug(f"Reverse configuration rule: {reverse_rule}")
                    src_controller.device_config.config_rules.append(ConfigRule(**reverse_rule))
                    src_controller.device_config.config_rules.append(ConfigRule(**forward_rule))    

            json_config_rule_delete_1 = json_config_rule_delete('/services/service[{:s}]'.format(service_uuid), {
                'uuid': service_uuid
            })
            src_controller.device_config.config_rules.append(ConfigRule(**json_config_rule_delete_1))
            self.__task_executor.configure_device(src_controller)
            results.append(True)

            def get_config_rules(controller):
                try:
                    config_rules = controller.device_config.config_rules
                    for rule in config_rules:
                        if rule.HasField("custom"):
                            resource_key = rule.custom.resource_key
                            resource_value = rule.custom.resource_value
                            LOGGER.debug(f"Resource key in config: {resource_key}, Resource value in config: {resource_value}")
                except Exception as e:
                    print(f"Error accessing config rules: {e}")

            get_config_rules(src_controller)
            LOGGER.debug(f"Configuration rules: {src_controller.device_config.config_rules}")
            return results
        
        except Exception as e:
            LOGGER.exception(f"Error in DeleteEndpoint")
            return [e] 