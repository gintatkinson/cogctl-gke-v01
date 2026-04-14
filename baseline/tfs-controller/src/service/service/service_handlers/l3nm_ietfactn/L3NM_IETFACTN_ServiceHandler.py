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

import json, logging, netaddr
from typing import Any, Dict, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, Device, DeviceId, EndPoint, Service
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api.Tools import get_device_endpoint_uuids, get_endpoint_matching
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.task_scheduler.TaskExecutor import TaskExecutor
from .Constants import ETHT_SERVICE_SETTINGS, OSU_TUNNEL_SETTINGS, VPN_VLAN_TAGS_TO_SERVICE_NAME

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'l3nm_ietf_actn'})

class L3NM_IETFACTN_ServiceHandler(_ServiceHandler):
    def __init__(   # pylint: disable=super-init-not-called
        self, service : Service, task_executor : TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(service.service_config, **settings)

    def _get_endpoint_details(
        self, endpoint : Tuple[str, str, Optional[str]]
    ) -> Tuple[Device, EndPoint, Dict]:
        device_uuid, endpoint_uuid = get_device_endpoint_uuids(endpoint)
        device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
        device_name = device_obj.name
        device_prefix = '/device[{:s}]/'.format(device_name)
        for config_rule in device_obj.device_config.config_rules:
            if config_rule.WhichOneof('config_rule') != 'custom': continue
            rw_config_rule = ConfigRule()
            rw_config_rule.CopyFrom(config_rule)
            resource_key = str(config_rule.custom.resource_key)
            if resource_key.startswith('/endpoints/endpoint['):
                resource_key = resource_key.replace('/endpoints/', device_prefix)
            rw_config_rule.custom.resource_key = resource_key
            self.__settings_handler.update_config_rule(rw_config_rule)
        endpoint_obj = get_endpoint_matching(device_obj, endpoint_uuid)
        endpoint_settings = self.__settings_handler.get_endpoint_settings(device_obj, endpoint_obj)
        endpoint_name = endpoint_obj.name
        if endpoint_settings is None:
            MSG = 'Settings not found for Endpoint(device=[uuid={:s}, name={:s}], endpoint=[uuid={:s}, name={:s}])'
            raise Exception(MSG.format(device_uuid, device_name, endpoint_uuid, endpoint_name))
        endpoint_settings_dict : Dict = endpoint_settings.value
        return device_obj, endpoint_obj, endpoint_settings_dict

    def _get_service_names(
        self,
        src_endpoint_details : Tuple[Device, EndPoint, Dict],
        dst_endpoint_details : Tuple[Device, EndPoint, Dict]
    ) -> Tuple[str, str]:
        _, _, src_endpoint_settings_dict = src_endpoint_details
        src_vlan_tag = src_endpoint_settings_dict['vlan_tag']

        _, _, dst_endpoint_settings_dict = dst_endpoint_details
        dst_vlan_tag = dst_endpoint_settings_dict['vlan_tag']

        service_names = VPN_VLAN_TAGS_TO_SERVICE_NAME.get((src_vlan_tag, dst_vlan_tag))
        if service_names is None:
            MSG = 'Unable to find service names from VLAN tags(src={:s}, dst={:s})'
            raise Exception(MSG.format(str(src_vlan_tag), str(dst_vlan_tag)))
        return service_names

    def _compose_osu_tunnel(
        self, osu_tunnel_name : str,
        src_endpoint_details : Tuple[Device, EndPoint, Dict],
        dst_endpoint_details : Tuple[Device, EndPoint, Dict],
        is_delete : bool = False
    ) -> ConfigRule:
        osu_tunnel_resource_key = '/osu_tunnels/osu_tunnel[{:s}]'.format(osu_tunnel_name)
        osu_tunnel_resource_value = {'name' : osu_tunnel_name}
        if is_delete:
            osu_tunnel_config_rule = json_config_rule_delete(osu_tunnel_resource_key, osu_tunnel_resource_value)
        else:
            src_device_obj, src_endpoint_obj, _ = src_endpoint_details
            dst_device_obj, dst_endpoint_obj, _ = dst_endpoint_details

            osu_tunnel_settings = OSU_TUNNEL_SETTINGS[osu_tunnel_name]
            ttp_channel_names = osu_tunnel_settings['ttp_channel_names']
            src_ttp_channel_name = ttp_channel_names[(src_device_obj.name, src_endpoint_obj.name)]
            dst_ttp_channel_name = ttp_channel_names[(dst_device_obj.name, dst_endpoint_obj.name)]

            osu_tunnel_resource_value.update({
                'odu_type'            : osu_tunnel_settings['odu_type'],
                'osuflex_number'      : osu_tunnel_settings['osuflex_number'],
                'bidirectional'       : osu_tunnel_settings['bidirectional'],
                'delay'               : osu_tunnel_settings['delay'],
                'src_node_id'         : src_device_obj.name,
                'src_tp_id'           : src_endpoint_obj.name,
                'src_ttp_channel_name': src_ttp_channel_name,
                'dst_node_id'         : dst_device_obj.name,
                'dst_tp_id'           : dst_endpoint_obj.name,
                'dst_ttp_channel_name': dst_ttp_channel_name,
            })
            osu_tunnel_config_rule = json_config_rule_set(osu_tunnel_resource_key, osu_tunnel_resource_value)
        LOGGER.debug('osu_tunnel_config_rule = {:s}'.format(str(osu_tunnel_config_rule)))
        return ConfigRule(**osu_tunnel_config_rule)

    def _compose_static_routing(
        self, src_vlan_tag : int, dst_vlan_tag : int
    ) -> Tuple[List[Dict], List[Dict]]:
        static_routing = self.__settings_handler.get('/static_routing')
        static_routing_dict : Dict = dict() if static_routing is None else static_routing.value
        src_static_routes = list()
        dst_static_routes = list()
        for _, static_route in static_routing_dict.items():
            vlan_id     = static_route['vlan-id']
            ipn_cidr    = netaddr.IPNetwork(static_route['ip-network'])
            ipn_network = str(ipn_cidr.network)
            ipn_preflen = int(ipn_cidr.prefixlen)
            next_hop = static_route['next-hop']
            if vlan_id == src_vlan_tag:
                src_static_routes.append([ipn_network, ipn_preflen, next_hop])
            elif vlan_id == dst_vlan_tag:
                dst_static_routes.append([ipn_network, ipn_preflen, next_hop])
        return src_static_routes, dst_static_routes

    def _compose_etht_service(
        self, etht_service_name : str, osu_tunnel_name : str,
        src_endpoint_details : Tuple[Device, EndPoint, Dict],
        dst_endpoint_details : Tuple[Device, EndPoint, Dict],
        is_delete : bool = False
    ) -> ConfigRule:
        etht_service_resource_key = '/etht_services/etht_service[{:s}]'.format(etht_service_name)
        etht_service_resource_value = {'name' : etht_service_name}
        if is_delete:
            etht_service_config_rule = json_config_rule_delete(etht_service_resource_key, etht_service_resource_value)
        else:
            src_device_obj, src_endpoint_obj, src_endpoint_details = src_endpoint_details
            src_vlan_tag = src_endpoint_details['vlan_tag']
            dst_device_obj, dst_endpoint_obj, dst_endpoint_details = dst_endpoint_details
            dst_vlan_tag = dst_endpoint_details['vlan_tag']
            src_static_routes, dst_static_routes = self._compose_static_routing(src_vlan_tag, dst_vlan_tag)
            etht_service_resource_value.update({
                'osu_tunnel_name'  : osu_tunnel_name,
                'service_type'     : ETHT_SERVICE_SETTINGS[etht_service_name]['service_type'],
                'src_node_id'      : src_device_obj.name,
                'src_tp_id'        : src_endpoint_obj.name,
                'src_vlan_tag'     : src_vlan_tag,
                'src_static_routes': src_static_routes,
                'dst_node_id'      : dst_device_obj.name,
                'dst_tp_id'        : dst_endpoint_obj.name,
                'dst_vlan_tag'     : dst_vlan_tag,
                'dst_static_routes': dst_static_routes,
            })
            etht_service_config_rule = json_config_rule_set(etht_service_resource_key, etht_service_resource_value)
        LOGGER.debug('etht_service_config_rule = {:s}'.format(str(etht_service_config_rule)))
        return ConfigRule(**etht_service_config_rule)

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
        LOGGER.debug('service_uuid = {:s}'.format(str(service_uuid)))
        LOGGER.debug('self.__settings_handler = {:s}'.format(str(self.__settings_handler.dump_config_rules())))

        results = []
        try:
            src_endpoint_details = self._get_endpoint_details(endpoints[0])
            src_device_obj, _, _ = src_endpoint_details
            src_controller = self.__task_executor.get_device_controller(src_device_obj)
            if src_controller is None: src_controller = src_device_obj

            dst_endpoint_details = self._get_endpoint_details(endpoints[-1])
            dst_device_obj, _, _ = dst_endpoint_details
            dst_controller = self.__task_executor.get_device_controller(dst_device_obj)
            if dst_controller is None: dst_controller = dst_device_obj

            if src_controller.device_id.device_uuid.uuid != dst_controller.device_id.device_uuid.uuid:
                raise Exception('Different Src-Dst devices not supported by now')
            controller = src_controller

            osu_tunnel_name, etht_service_name = self._get_service_names(
                src_endpoint_details, dst_endpoint_details
            )

            osu_tunnel_config_rule = self._compose_osu_tunnel(
                osu_tunnel_name, src_endpoint_details, dst_endpoint_details,
                is_delete=False
            )

            etht_service_config_rule = self._compose_etht_service(
                etht_service_name, osu_tunnel_name, src_endpoint_details,
                dst_endpoint_details, is_delete=False
            )

            del controller.device_config.config_rules[:]
            controller.device_config.config_rules.append(osu_tunnel_config_rule)
            controller.device_config.config_rules.append(etht_service_config_rule)
            self.__task_executor.configure_device(controller)
            results.append(True)
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Unable to SetEndpoint for Service({:s})'.format(str(service_uuid)))
            results.append(e)

        LOGGER.debug('results = {:s}'.format(str(results)))
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('endpoints = {:s}'.format(str(endpoints)))
        chk_type('endpoints', endpoints, list)
        if len(endpoints) < 2:
            LOGGER.warning('nothing done: not enough endpoints')
            return []
        service_uuid = self.__service.service_id.service_uuid.uuid
        LOGGER.debug('service_uuid = {:s}'.format(str(service_uuid)))
        LOGGER.debug('self.__settings_handler = {:s}'.format(str(self.__settings_handler.dump_config_rules())))

        results = []
        try:
            src_endpoint_details = self._get_endpoint_details(endpoints[0])
            src_device_obj, _, _ = src_endpoint_details
            src_controller = self.__task_executor.get_device_controller(src_device_obj)
            if src_controller is None: src_controller = src_device_obj

            dst_endpoint_details = self._get_endpoint_details(endpoints[-1])
            dst_device_obj, _, _ = dst_endpoint_details
            dst_controller = self.__task_executor.get_device_controller(dst_device_obj)
            if dst_controller is None: dst_controller = dst_device_obj

            if src_controller.device_id.device_uuid.uuid != dst_controller.device_id.device_uuid.uuid:
                raise Exception('Different Src-Dst devices not supported by now')
            controller = src_controller

            osu_tunnel_name, etht_service_name = self._get_service_names(
                src_endpoint_details, dst_endpoint_details
            )

            osu_tunnel_config_rule = self._compose_osu_tunnel(
                osu_tunnel_name, src_endpoint_details, dst_endpoint_details,
                is_delete=True
            )

            etht_service_config_rule = self._compose_etht_service(
                etht_service_name, osu_tunnel_name, src_endpoint_details,
                dst_endpoint_details, is_delete=True
            )

            del controller.device_config.config_rules[:]
            controller.device_config.config_rules.append(etht_service_config_rule)
            controller.device_config.config_rules.append(osu_tunnel_config_rule)
            self.__task_executor.configure_device(controller)
            results.append(True)
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Unable to DeleteEndpoint for Service({:s})'.format(str(service_uuid)))
            results.append(e)

        LOGGER.debug('results = {:s}'.format(str(results)))
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
