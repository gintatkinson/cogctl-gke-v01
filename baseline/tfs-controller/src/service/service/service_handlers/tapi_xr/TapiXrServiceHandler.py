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
from typing import Any, Dict, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, DeviceId, Service
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api.Tools import get_device_endpoint_uuids, get_endpoint_matching
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.task_scheduler.TaskExecutor import TaskExecutor

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'tapi_xr'})

class TapiXrServiceHandler(_ServiceHandler):
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

        # When using regular mode where XR constellation is a single device, we get two endpoints.
        # Convert that representation to a form that is understood by the service handler that
        # expects constellation to be represented as multiple devices.
        if len(endpoints) == 2:
            endpoints = [None, endpoints[0], endpoints[1], None]

        if len(endpoints) != 4: return []

        service_uuid = self.__service.service_id.service_uuid.uuid
        settings = self.__settings_handler.get('/settings')
        json_settings : Dict = {} if settings is None else settings.value
        capacity_value   = json_settings.get('capacity_value', 50.0)
        capacity_unit    = json_settings.get('capacity_unit',  'GHz')

        results = []
        try:
            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[1])
            src_device = self.__task_executor.get_device(DeviceId(**json_device_id(src_device_uuid)))
            src_endpoint = get_endpoint_matching(src_device, src_endpoint_uuid)
            src_controller = self.__task_executor.get_device_controller(src_device)
            if src_controller is None: src_controller = src_device

            dst_device_uuid, dst_endpoint_uuid = get_device_endpoint_uuids(endpoints[2])
            dst_device = self.__task_executor.get_device(DeviceId(**json_device_id(dst_device_uuid)))
            dst_endpoint = get_endpoint_matching(dst_device, dst_endpoint_uuid)
            dst_controller = self.__task_executor.get_device_controller(dst_device)
            if dst_controller is None: dst_controller = dst_device

            if src_controller.device_id.device_uuid.uuid != dst_controller.device_id.device_uuid.uuid:
                raise Exception('Different Src-Dst devices not supported by now')
            controller = src_controller

            # If the special mode that splits XR constellation to multiple modelled devices is used,
            # add the device name to interface name. Otherwise use it as is (it will already contain pipe character
            # end edge device name). This code should be refactored, as interface name structure is internal matter
            # to XR driver and subject to change.
            constellation_unique_src =  src_endpoint.name if "|" in src_endpoint.name else '|'.join([src_device.name, src_endpoint.name])
            constellation_unique_dst =  dst_endpoint.name if "|" in dst_endpoint.name else '|'.join([dst_device.name, dst_endpoint.name])

            json_config_rule = json_config_rule_set('/services/service[{:s}]'.format(service_uuid), {
                'uuid'           : service_uuid,
                'input_sip_name' : constellation_unique_src,
                'output_sip_name': constellation_unique_dst,
                'capacity_unit'  : capacity_unit,
                'capacity_value' : capacity_value,
            })

            del controller.device_config.config_rules[:]
            controller.device_config.config_rules.append(ConfigRule(**json_config_rule))
            self.__task_executor.configure_device(controller)
            results.append(True)
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Unable to SetEndpoint for Service({:s})'.format(str(service_uuid)))
            results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:

        chk_type('endpoints', endpoints, list)
        if len(endpoints) < 2: return []

        service_uuid = self.__service.service_id.service_uuid.uuid

        results = []
        try:
            src_device_uuid, _ = get_device_endpoint_uuids(endpoints[0])
            src_device = self.__task_executor.get_device(DeviceId(**json_device_id(src_device_uuid)))
            src_controller = self.__task_executor.get_device_controller(src_device)
            if src_controller is None: src_controller = src_device

            dst_device_uuid, _ = get_device_endpoint_uuids(endpoints[1])
            dst_device = self.__task_executor.get_device(DeviceId(**json_device_id(dst_device_uuid)))
            dst_controller = self.__task_executor.get_device_controller(dst_device)
            if dst_controller is None: dst_controller = dst_device

            if src_controller.device_id.device_uuid.uuid != dst_controller.device_id.device_uuid.uuid:
                raise Exception('Different Src-Dst devices not supported by now')
            controller = src_controller

            json_config_rule = json_config_rule_delete('/services/service[{:s}]'.format(service_uuid), {
                'uuid': service_uuid
            })
            del controller.device_config.config_rules[:]
            controller.device_config.config_rules.append(ConfigRule(**json_config_rule))
            self.__task_executor.configure_device(controller)
            results.append(True)
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Unable to DeleteEndpoint for Service({:s})'.format(str(service_uuid)))
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
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Unable to DeleteConfig({:s})'.format(str(resource)))
                results.append(e)

        return results
