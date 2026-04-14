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
from common.proto.context_pb2 import ConfigRule, ConnectionId, DeviceId, Service
from common.tools.object_factory.Connection import json_connection_id
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
#from service.service.service_handler_api.AnyTreeTools import TreeNode
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.service_handler_api.Tools import get_device_endpoint_uuids, get_endpoint_matching
from .MockTaskExecutor import MockTaskExecutor
from service.service.tools.EndpointIdFormatters import endpointids_to_raw
from service.service.service_handlers.l3nm_gnmi_openconfig.ConfigRuleComposer import ConfigRuleComposer
from service.service.service_handlers.l3nm_gnmi_openconfig.StaticRouteGenerator import StaticRouteGenerator

LOGGER = logging.getLogger(__name__)

class MockServiceHandler(_ServiceHandler):
    def __init__(   # pylint: disable=super-init-not-called
        self, service : Service, task_executor : MockTaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(service.service_config, **settings)
        self.__config_rule_composer = ConfigRuleComposer()
        self.__static_route_generator = StaticRouteGenerator(self.__config_rule_composer)
        self.__endpoint_map : Dict[Tuple[str, str], Tuple[str, str]] = dict()

    def _compose_config_rules(self, endpoints : List[Tuple[str, str, Optional[str]]]) -> None:
        if len(endpoints) % 2 != 0: raise Exception('Number of endpoints should be even')

        service_settings = self.__settings_handler.get_service_settings()
        self.__config_rule_composer.configure(self.__service, service_settings)

        #prev_endpoint_obj = None
        #prev_endpoint     = None
        #settings_for_next = None
        #for i,endpoint in enumerate(endpoints):
        for endpoint in endpoints:
            device_uuid, endpoint_uuid = get_device_endpoint_uuids(endpoint)

            device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
            device_settings = self.__settings_handler.get_device_settings(device_obj)
            self.__config_rule_composer.set_device_alias(device_obj.name, device_uuid)
            _device = self.__config_rule_composer.get_device(device_obj.name)
            _device.configure(device_obj, device_settings)

            endpoint_obj = get_endpoint_matching(device_obj, endpoint_uuid)
            endpoint_settings = self.__settings_handler.get_endpoint_settings(device_obj, endpoint_obj)
            _device.set_endpoint_alias(endpoint_obj.name, endpoint_uuid)
            _endpoint = _device.get_endpoint(endpoint_obj.name)
            _endpoint.configure(endpoint_obj, endpoint_settings)

            #if settings_for_next is not None:
            #    _endpoint.configure(endpoint_obj, settings_for_next)
            #    settings_for_next = None

            #if endpoint_settings is not None and 'neighbor_address' in endpoint_settings.value:
            #    _neighbor_settings = {'address_ip': endpoint_settings.value['neighbor_address']}
            #
            #    if 'address_prefix' in endpoint_settings.value:
            #        _neighbor_settings['address_prefix'] = endpoint_settings.value['address_prefix']
            #    elif 'prefix_length' in endpoint_settings.value:
            #        _neighbor_settings['address_prefix'] = endpoint_settings.value['prefix_length']
            #    else:
            #        MSG = 'IP Address Prefix not found. Tried: address_prefix and prefix_length. endpoint_settings.value={:s}'
            #        raise Exception(MSG.format(str(endpoint_settings.value)))
            #
            #    neighbor_settings = TreeNode('.')
            #    neighbor_settings.value = _neighbor_settings
            #    if i % 2 == 0:
            #        # configure in next endpoint
            #        settings_for_next = neighbor_settings
            #    else:
            #        # configure in previous endpoint
            #        prev_endpoint.configure(prev_endpoint_obj, neighbor_settings)

            self.__endpoint_map[(device_uuid, endpoint_uuid)] = (device_obj.name, endpoint_obj.name)

            #prev_endpoint = _endpoint
            #prev_endpoint_obj = endpoint_obj

        self.__static_route_generator.compose(endpoints)
        LOGGER.debug('config_rule_composer = {:s}'.format(json.dumps(self.__config_rule_composer.dump())))

    def _do_configurations(
        self, config_rules_per_device : Dict[str, List[Dict]], endpoints : List[Tuple[str, str, Optional[str]]],
        delete : bool = False
    ) -> List[Union[bool, Exception]]:
        # Configuration is done atomically on each device, all OK / all KO per device
        results_per_device = dict()
        for device_name,json_config_rules in config_rules_per_device.items():
            try:
                device_obj = self.__config_rule_composer.get_device(device_name).objekt
                if len(json_config_rules) == 0: continue
                del device_obj.device_config.config_rules[:]
                for json_config_rule in json_config_rules:
                    device_obj.device_config.config_rules.append(ConfigRule(**json_config_rule))
                self.__task_executor.configure_device(device_obj)
                results_per_device[device_name] = True
            except Exception as e: # pylint: disable=broad-exception-caught
                verb = 'deconfigure' if delete else 'configure'
                MSG = 'Unable to {:s} Device({:s}) : ConfigRules({:s})'
                LOGGER.exception(MSG.format(verb, str(device_name), str(json_config_rules)))
                results_per_device[device_name] = e

        results = []
        for endpoint in endpoints:
            device_uuid, endpoint_uuid = get_device_endpoint_uuids(endpoint)
            device_name, _ = self.__endpoint_map[(device_uuid, endpoint_uuid)]
            if device_name not in results_per_device: continue
            results.append(results_per_device[device_name])
        return results

    def SetEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []
        #service_uuid = self.__service.service_id.service_uuid.uuid
        connection = self.__task_executor.get_connection(ConnectionId(**json_connection_id(connection_uuid)))
        connection_endpoint_ids = endpointids_to_raw(connection.path_hops_endpoint_ids)
        self._compose_config_rules(connection_endpoint_ids)
        #network_instance_name = service_uuid.split('-')[0]
        #config_rules_per_device = self.__config_rule_composer.get_config_rules(network_instance_name, delete=False)
        config_rules_per_device = self.__config_rule_composer.get_config_rules(delete=False)
        LOGGER.debug('config_rules_per_device={:s}'.format(json.dumps(config_rules_per_device)))
        results = self._do_configurations(config_rules_per_device, endpoints)
        LOGGER.debug('results={:s}'.format(str(results)))
        return results

    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []
        #service_uuid = self.__service.service_id.service_uuid.uuid
        connection = self.__task_executor.get_connection(ConnectionId(**json_connection_id(connection_uuid)))
        connection_endpoint_ids = endpointids_to_raw(connection.path_hops_endpoint_ids)
        self._compose_config_rules(connection_endpoint_ids)
        #network_instance_name = service_uuid.split('-')[0]
        #config_rules_per_device = self.__config_rule_composer.get_config_rules(network_instance_name, delete=True)
        config_rules_per_device = self.__config_rule_composer.get_config_rules(delete=True)
        LOGGER.debug('config_rules_per_device={:s}'.format(json.dumps(config_rules_per_device)))
        results = self._do_configurations(config_rules_per_device, endpoints, delete=True)
        LOGGER.debug('results={:s}'.format(str(results)))
        return results

    def SetConstraint(self, constraints : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []

        msg = '[SetConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

    def DeleteConstraint(self, constraints : List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []

        msg = '[DeleteConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

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
