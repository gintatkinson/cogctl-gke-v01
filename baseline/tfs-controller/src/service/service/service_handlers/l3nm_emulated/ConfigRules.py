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

from typing import Dict, List
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from service.service.service_handler_api.AnyTreeTools import TreeNode

def setup_config_rules(
    service_uuid : str, connection_uuid : str, device_uuid : str, endpoint_uuid : str, endpoint_name : str,
    service_settings : TreeNode, endpoint_settings : TreeNode
) -> List[Dict]:

    if service_settings  is None: return []
    if endpoint_settings is None: return []

    json_settings          : Dict = service_settings.value
    json_endpoint_settings : Dict = endpoint_settings.value

    service_short_uuid        = service_uuid.split('-')[-1]
    network_instance_name     = '{:s}-NetInst'.format(service_short_uuid)
    network_interface_desc    = '{:s}-NetIf'.format(service_uuid)
    network_subinterface_desc = '{:s}-NetSubIf'.format(service_uuid)

    mtu                 = json_settings.get('mtu',                 1450 )    # 1512
    #address_families    = json_settings.get('address_families',    []   )    # ['IPV4']
    bgp_as              = json_settings.get('bgp_as',              0    )    # 65000
    bgp_route_target    = json_settings.get('bgp_route_target',    '0:0')    # 65000:333

    #router_id           = json_endpoint_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    route_distinguisher = json_endpoint_settings.get('route_distinguisher', '0:0'    )  # '60001:801'
    sub_interface_index = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    vlan_id             = json_endpoint_settings.get('vlan_id',             1        )  # 400
    address_ip          = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    address_prefix      = json_endpoint_settings.get('address_prefix',      24       )  # 30
    if_subif_name       = '{:s}.{:s}'.format(endpoint_name, str(vlan_id))

    json_config_rules = [
        json_config_rule_set(
            '/network_instance[{:s}]'.format(network_instance_name), {
                'name': network_instance_name, 'description': network_interface_desc, 'type': 'L3VRF',
                'route_distinguisher': route_distinguisher,
                #'router_id': router_id, 'address_families': address_families,
        }),
        json_config_rule_set(
            '/interface[{:s}]'.format(endpoint_name), {
                'name': endpoint_name, 'description': network_interface_desc, 'mtu': mtu,
        }),
        json_config_rule_set(
            '/interface[{:s}]/subinterface[{:s}]'.format(endpoint_name, str(sub_interface_index)), {
                'name': endpoint_name, 'index': sub_interface_index,
                'description': network_subinterface_desc, 'vlan_id': vlan_id,
                'address_ip': address_ip, 'address_prefix': address_prefix,
        }),
        json_config_rule_set(
            '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, if_subif_name), {
                'name': network_instance_name, 'id': if_subif_name, 'interface': endpoint_name,
                'subinterface': sub_interface_index,
        }),
        json_config_rule_set(
            '/network_instance[{:s}]/protocols[BGP]'.format(network_instance_name), {
                'name': network_instance_name, 'identifier': 'BGP', 'protocol_name': 'BGP', 'as': bgp_as,
        }),
        json_config_rule_set(
            '/network_instance[{:s}]/table_connections[STATIC][BGP][IPV4]'.format(network_instance_name), {
                'name': network_instance_name, 'src_protocol': 'STATIC', 'dst_protocol': 'BGP',
                'address_family': 'IPV4', #'default_import_policy': 'REJECT_ROUTE',
        }),
        json_config_rule_set(
            '/network_instance[{:s}]/table_connections[DIRECTLY_CONNECTED][BGP][IPV4]'.format(
                network_instance_name), {
                'name': network_instance_name, 'src_protocol': 'DIRECTLY_CONNECTED', 'dst_protocol': 'BGP',
                'address_family': 'IPV4', #'default_import_policy': 'REJECT_ROUTE',
        }),
        json_config_rule_set(
            '/routing_policy/bgp_defined_set[{:s}_rt_import]'.format(network_instance_name), {
                'ext_community_set_name': '{:s}_rt_import'.format(network_instance_name),
        }),
        json_config_rule_set(
            '/routing_policy/bgp_defined_set[{:s}_rt_import][route-target:{:s}]'.format(
                network_instance_name, bgp_route_target), {
                'ext_community_set_name': '{:s}_rt_import'.format(network_instance_name),
                'ext_community_member'  : 'route-target:{:s}'.format(bgp_route_target),
        }),
        json_config_rule_set(
            '/routing_policy/policy_definition[{:s}_import]'.format(network_instance_name), {
                'policy_name': '{:s}_import'.format(network_instance_name),
        }),
        json_config_rule_set(
            '/routing_policy/policy_definition[{:s}_import]/statement[{:s}]'.format(
                network_instance_name, '3'), {
                'policy_name': '{:s}_import'.format(network_instance_name), 'statement_name': '3',
                'ext_community_set_name': '{:s}_rt_import'.format(network_instance_name),
                'match_set_options': 'ANY', 'policy_result': 'ACCEPT_ROUTE',
        }),
        json_config_rule_set(
            # pylint: disable=duplicate-string-formatting-argument
            '/network_instance[{:s}]/inter_instance_policies[{:s}_import]'.format(
                network_instance_name, network_instance_name), {
                'name': network_instance_name, 'import_policy': '{:s}_import'.format(network_instance_name),
        }),
        json_config_rule_set(
            '/routing_policy/bgp_defined_set[{:s}_rt_export]'.format(network_instance_name), {
                'ext_community_set_name': '{:s}_rt_export'.format(network_instance_name),
        }),
        json_config_rule_set(
            '/routing_policy/bgp_defined_set[{:s}_rt_export][route-target:{:s}]'.format(
                network_instance_name, bgp_route_target), {
                'ext_community_set_name': '{:s}_rt_export'.format(network_instance_name),
                'ext_community_member'  : 'route-target:{:s}'.format(bgp_route_target),
        }),
        json_config_rule_set(
            '/routing_policy/policy_definition[{:s}_export]'.format(network_instance_name), {
                'policy_name': '{:s}_export'.format(network_instance_name),
        }),
        json_config_rule_set(
            '/routing_policy/policy_definition[{:s}_export]/statement[{:s}]'.format(
                network_instance_name, '3'), {
                'policy_name': '{:s}_export'.format(network_instance_name), 'statement_name': '3',
                'ext_community_set_name': '{:s}_rt_export'.format(network_instance_name),
                'match_set_options': 'ANY', 'policy_result': 'ACCEPT_ROUTE',
        }),
        json_config_rule_set(
            # pylint: disable=duplicate-string-formatting-argument
            '/network_instance[{:s}]/inter_instance_policies[{:s}_export]'.format(
                network_instance_name, network_instance_name), {
                'name': network_instance_name, 'export_policy': '{:s}_export'.format(network_instance_name),
        }),
    ]

    return json_config_rules

def teardown_config_rules(
    service_uuid : str, connection_uuid : str, device_uuid : str, endpoint_uuid : str, endpoint_name : str,
    service_settings : TreeNode, endpoint_settings : TreeNode
) -> List[Dict]:

    if service_settings  is None: return []
    if endpoint_settings is None: return []

    json_settings          : Dict = service_settings.value
    json_endpoint_settings : Dict = endpoint_settings.value

    #mtu                 = json_settings.get('mtu',                 1450 )    # 1512
    #address_families    = json_settings.get('address_families',    []   )    # ['IPV4']
    #bgp_as              = json_settings.get('bgp_as',              0    )    # 65000
    bgp_route_target    = json_settings.get('bgp_route_target',    '0:0')    # 65000:333

    #router_id           = json_endpoint_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    #route_distinguisher = json_endpoint_settings.get('route_distinguisher', '0:0'    )  # '60001:801'
    sub_interface_index = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    vlan_id             = json_endpoint_settings.get('vlan_id',             1        )  # 400
    #address_ip          = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    #address_prefix      = json_endpoint_settings.get('address_prefix',      24       )  # 30

    if_subif_name             = '{:s}.{:s}'.format(endpoint_name, str(vlan_id))
    service_short_uuid        = service_uuid.split('-')[-1]
    network_instance_name     = '{:s}-NetInst'.format(service_short_uuid)
    #network_interface_desc    = '{:s}-NetIf'.format(service_uuid)
    #network_subinterface_desc = '{:s}-NetSubIf'.format(service_uuid)

    json_config_rules = [
        json_config_rule_delete(
            '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, if_subif_name), {
                'name': network_instance_name, 'id': if_subif_name,
        }),
        json_config_rule_delete(
            '/interface[{:s}]/subinterface[{:s}]'.format(endpoint_name, str(sub_interface_index)), {
                'name': endpoint_name, 'index': sub_interface_index,
        }),
        json_config_rule_delete(
            '/interface[{:s}]'.format(endpoint_name), {
                'name': endpoint_name,
        }),
        json_config_rule_delete(
            '/network_instance[{:s}]/table_connections[DIRECTLY_CONNECTED][BGP][IPV4]'.format(
                network_instance_name), {
                'name': network_instance_name, 'src_protocol': 'DIRECTLY_CONNECTED', 'dst_protocol': 'BGP',
                'address_family': 'IPV4',
        }),
        json_config_rule_delete(
            '/network_instance[{:s}]/table_connections[STATIC][BGP][IPV4]'.format(network_instance_name), {
                'name': network_instance_name, 'src_protocol': 'STATIC', 'dst_protocol': 'BGP',
                'address_family': 'IPV4',
        }),
        json_config_rule_delete(
            '/network_instance[{:s}]/protocols[BGP]'.format(network_instance_name), {
                'name': network_instance_name, 'identifier': 'BGP', 'protocol_name': 'BGP',
        }),
        json_config_rule_delete(
            # pylint: disable=duplicate-string-formatting-argument
            '/network_instance[{:s}]/inter_instance_policies[{:s}_import]'.format(
                network_instance_name, network_instance_name), {
            'name': network_instance_name,
        }),
        json_config_rule_delete(
            '/routing_policy/policy_definition[{:s}_import]/statement[{:s}]'.format(
                network_instance_name, '3'), {
                'policy_name': '{:s}_import'.format(network_instance_name), 'statement_name': '3',
        }),
        json_config_rule_delete(
            '/routing_policy/policy_definition[{:s}_import]'.format(network_instance_name), {
                'policy_name': '{:s}_import'.format(network_instance_name),
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_import][route-target:{:s}]'.format(
                network_instance_name, bgp_route_target), {
                'ext_community_set_name': '{:s}_rt_import'.format(network_instance_name),
                'ext_community_member'  : 'route-target:{:s}'.format(bgp_route_target),
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_import]'.format(network_instance_name), {
                'ext_community_set_name': '{:s}_rt_import'.format(network_instance_name),
        }),
        json_config_rule_delete(
            # pylint: disable=duplicate-string-formatting-argument
            '/network_instance[{:s}]/inter_instance_policies[{:s}_export]'.format(
                network_instance_name, network_instance_name), {
                'name': network_instance_name,
        }),
        json_config_rule_delete(
            '/routing_policy/policy_definition[{:s}_export]/statement[{:s}]'.format(
                network_instance_name, '3'), {
                'policy_name': '{:s}_export'.format(network_instance_name), 'statement_name': '3',
        }),
        json_config_rule_delete(
            '/routing_policy/policy_definition[{:s}_export]'.format(network_instance_name), {
                'policy_name': '{:s}_export'.format(network_instance_name),
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_export][route-target:{:s}]'.format(
                network_instance_name, bgp_route_target), {
                'ext_community_set_name': '{:s}_rt_export'.format(network_instance_name),
                'ext_community_member'  : 'route-target:{:s}'.format(bgp_route_target),
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_export]'.format(network_instance_name), {
                'ext_community_set_name': '{:s}_rt_export'.format(network_instance_name),
        }),
        json_config_rule_delete(
            '/network_instance[{:s}]'.format(network_instance_name), {
                'name': network_instance_name
        }),
    ]
    return json_config_rules
