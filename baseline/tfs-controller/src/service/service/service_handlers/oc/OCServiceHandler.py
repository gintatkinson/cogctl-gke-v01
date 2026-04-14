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

import json, logging
from typing import Any, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, DeviceId, Service
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from common.DeviceTypes import DeviceTypeEnum
from service.service.service_handler_api.Tools import get_device_endpoint_uuids, get_endpoint_matching
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from .ConfigRules import setup_config_rules, teardown_config_rules
from .OCTools import (
    endpoints_to_flows, convert_endpoints_to_flows, convert_or_endpoints_to_flows
)

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'oc'})

class OCServiceHandler(_ServiceHandler):
    def __init__(   # pylint: disable=super-init-not-called
        self, service : Service, task_executor : TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(service.service_config, **settings)

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
   
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []
    
        results = []
        for endpoint in endpoints:
            try:
                device_uuid, endpoint_uuid = get_device_endpoint_uuids(endpoint)

                device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
                endpoint_obj = get_endpoint_matching(device_obj, endpoint_uuid)
                endpoint_ip_link = self.__settings_handler.get_endpoint_ip_link(device_obj, endpoint_obj)
                endpoint_name = endpoint_obj.name
                json_config_rules = setup_config_rules(
                    endpoint_name, endpoint_ip_link)

                if len(json_config_rules) > 0:
                    del device_obj.device_config.config_rules[:]
                    for json_config_rule in json_config_rules:
                        device_obj.device_config.config_rules.append(ConfigRule(**json_config_rule))
                    self.__task_executor.configure_device(device_obj)

                results.append(True)
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Unable to SetEndpoint({:s})'.format(str(endpoint)))
                results.append(e)


        return results
    
    
    @metered_subclass_method(METRICS_POOL)
    def SetOpticalConfig(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []
        is_opticalband =False
        #service_uuid = self.__service.service_id.service_uuid.uuid
        settings=None
        results = []
        if self.__settings_handler.get('/settings-ob_{}'.format(connection_uuid)):
            is_opticalband=True
            settings = self.__settings_handler.get('/settings-ob_{}'.format(connection_uuid))
        else:
            settings = self.__settings_handler.get('/settings')
       
        bidir = settings.value.get("bidir")
        ob_expansion =settings.value.get('ob-expanded',None) 
        if ob_expansion : 
            if not is_opticalband: 
                LOGGER.info(f"ob-expanded bvalue is: {ob_expansion} and is_opticalband {is_opticalband}")
                return results
        
        flows = endpoints_to_flows(endpoints, bidir, is_opticalband)
        
        #new cycle for setting optical devices
        for device_uuid, dev_flows in flows.items():
            try:
                device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
                if settings is not None:
                    self.__task_executor.configure_optical_device(device_obj, settings, dev_flows
                                                                  , is_opticalband ,connection_uuid)
                results.append(True)
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Unable to configure Device({:s})'.format(str(device_uuid)))
                results.append(e) 

        return results


    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        is_opticalband =False
        is_openroadm =False
        service_uuid = self.__service.service_id.service_uuid.uuid  
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []
       
        if self.__settings_handler.get('/settings-ob_{}'.format(connection_uuid)):
            is_opticalband =True
            settings = self.__settings_handler.get('/settings-ob_{}'.format(connection_uuid))
        else:
            settings = self.__settings_handler.get('/settings')  

        bidir = settings.value.get("bidir",None)

        results = []
        for endpoint in endpoints:
            try:
                device_uuid, endpoint_uuid = get_device_endpoint_uuids(endpoint)
                device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
                
                # temporarily until updating convert to flow , cause it doesn't support openroadm endpoints flows
                if device_obj.device_type ==  DeviceTypeEnum.OPEN_ROADM._value_ : 
                    if not is_openroadm: is_openroadm=True
                device_settings = self.__settings_handler.get_device_settings(device_obj)
                endpoint_obj = get_endpoint_matching(device_obj, endpoint_uuid)
                endpoint_settings = self.__settings_handler.get_endpoint_settings(device_obj, endpoint_obj)
                endpoint_name = endpoint_obj.name

                json_config_rules = teardown_config_rules(
                    service_uuid, connection_uuid, device_uuid, endpoint_uuid, endpoint_name,
                    settings, device_settings, endpoint_settings)

                if len(json_config_rules) > 0:
                    del device_obj.device_config.config_rules[:]
                    for json_config_rule in json_config_rules:
                        device_obj.device_config.config_rules.append(ConfigRule(**json_config_rule))
                    self.__task_executor.configure_device(device_obj)

                results.append(True)
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Unable to DeleteEndpoint({:s})'.format(str(endpoint)))
                results.append(e)

        if is_openroadm:
            flows = convert_or_endpoints_to_flows(endpoints, bidir)
        else:
            flows = endpoints_to_flows(endpoints, bidir, is_opticalband)

        for device_uuid, dev_flows in flows.items():
            try:
                channel_indexes= []
                device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))

                if (device_obj.device_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_):
                    for endpoint in dev_flows:
                        src , dst = endpoint
                        src_enpoint_name='0'
                        dist_enpoint_name='0'
                        if src !="0":
                           src_endponit_obj =get_endpoint_matching(device_obj, src)
                           src_enpoint_name=src_endponit_obj.name
                        if dst !="0":
                           dst_endpoint_obj = get_endpoint_matching(device_obj, dst) 
                           dist_enpoint_name=dst_endpoint_obj.name
                        channel_indexes.append((src_enpoint_name,dist_enpoint_name))   
                elif(device_obj.device_type == DeviceTypeEnum.OPTICAL_ROADM._value_):
                    if not is_opticalband:
                        if 'flow_id' in settings.value:
                            channel_indexes.append(settings.value["flow_id"])
                    elif is_opticalband:
                        if "ob_id" in settings.value:
                            channel_indexes.append(settings.value["ob_id"])
                elif (device_obj.device_type == DeviceTypeEnum.OPEN_ROADM._value_):    
                       channel_indexes.append(settings.value["flow_id"])            
                if len(channel_indexes) > 0:
                    errors = self.__task_executor.deconfigure_optical_device(
                        device=device_obj, channel_indexes=channel_indexes,
                        is_opticalband=is_opticalband, dev_flow=dev_flows,
                        bidir=bidir
                    )

                results.append(True)
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Unable to DeleteEndpoint({:s})'.format(str(endpoint)))
                results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConstraint(self, constraints : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []

        msg = '[SetConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConstraint(self, constraints : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []

        msg = '[DeleteConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []

        results = []
        for resource in resources:
            try:
                resource_value = json.loads(resource[1])
                self.__settings_handler.set(resource[0], resource_value)
                results.append(True)
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Unable to SetConfig({:s})'.format(str(resource)))
                results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        results = []
        for resource in resources:
            try:
                self.__settings_handler.delete(resource[0])
                # self.__task_executor.delete_setting(service_id,"/settings","value")
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Unable to DeleteConfig({:s})'.format(str(resource)))
                results.append(e)

        return results

    def check_media_channel(self,connection_uuid):
        if self.__settings_handler.get('/settings-ob_{}'.format(connection_uuid)):
            return False
        else:
            return True
