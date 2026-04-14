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

from typing import Dict, List, Tuple
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from service.service.service_handler_api.AnyTreeTools import TreeNode

def setup_config_rules(
    service_uuid : str, connection_uuid : str, device_uuid : str, endpoint_uuid : str, endpoint_name : str,
    service_settings : TreeNode, endpoint_settings : TreeNode, endpoint_acls : List [Tuple]
) -> List[Dict]:

    if service_settings  is None: return []
    if endpoint_settings is None: return []

    json_settings          : Dict = service_settings.value
    json_endpoint_settings : Dict = endpoint_settings.value

    #mtu                 = json_settings.get('mtu',                 1450 )    # 1512
    #address_families    = json_settings.get('address_families',    []   )    # ['IPV4']
    #bgp_as              = json_settings.get('bgp_as',              0    )    # 65000
    #bgp_route_target    = json_settings.get('bgp_route_target',    '0:0')    # 65000:333

    #router_id           = json_endpoint_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    #route_distinguisher = json_endpoint_settings.get('route_distinguisher', '0:0'    )  # '60001:801'
    sub_interface_index = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    vlan_id             = json_endpoint_settings.get('vlan_id',             None     )  # 400
    #address_ip          = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    #address_prefix      = json_endpoint_settings.get('address_prefix',      24       )  # 30
    remote_router       = json_endpoint_settings.get('remote_router',       '0.0.0.0')  # '5.5.5.5'
    circuit_id          = json_endpoint_settings.get('circuit_id',          None    )  # '111'

    if vlan_id is None: vlan_id = json_settings.get('vlan_id', 1)
    if circuit_id is None: circuit_id = json_settings.get('circuit_id', '000')

    if_cirid_name         = '{:s}.{:s}'.format(endpoint_name, str(circuit_id))
    network_instance_name = 'ELAN-AC:{:s}'.format(str(circuit_id))
    connection_point_id   = 'VC-1'

    json_config_rules = [
        #json_config_rule_set(
        #    '/network_instance[default]',
        #    {'name': 'default', 'type': 'DEFAULT_INSTANCE', 'router_id': router_id}),

        #json_config_rule_set(
        #    '/network_instance[default]/protocols[OSPF]',
        #    {'name': 'default', 'identifier': 'OSPF', 'protocol_name': 'OSPF'}),

        #json_config_rule_set(
        #    '/network_instance[default]/protocols[STATIC]',
        #    {'name': 'default', 'identifier': 'STATIC', 'protocol_name': 'STATIC'}),

        json_config_rule_set(
            '/network_instance[{:s}]'.format(network_instance_name),
            {'name': network_instance_name, 'type': 'L2VSI'}),

        json_config_rule_set(
            '/interface[{:s}]/subinterface[{:d}]'.format(if_cirid_name, sub_interface_index),
            {'name': if_cirid_name, 'type': 'l2vlan', 'index': sub_interface_index, 'vlan_id': vlan_id}),

        json_config_rule_set(
            '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, if_cirid_name),
            {'name': network_instance_name, 'id': if_cirid_name, 'interface': if_cirid_name,
             'subinterface': sub_interface_index}),

        json_config_rule_set(
            '/network_instance[{:s}]/connection_point[{:s}]'.format(network_instance_name, connection_point_id),
            {'name': network_instance_name, 'connection_point': connection_point_id, 'VC_ID': circuit_id,
             'remote_system': remote_router}),
    ]
    return json_config_rules

def teardown_config_rules(
    service_uuid : str, connection_uuid : str, device_uuid : str, endpoint_uuid : str, endpoint_name : str,
    service_settings : TreeNode, endpoint_settings : TreeNode
) -> List[Dict]:

    if service_settings  is None: return []
    if endpoint_settings is None: return []

    #json_settings          : Dict = service_settings.value
    json_endpoint_settings : Dict = endpoint_settings.value

    #mtu                 = json_settings.get('mtu',                 1450 )    # 1512
    #address_families    = json_settings.get('address_families',    []   )    # ['IPV4']
    #bgp_as              = json_settings.get('bgp_as',              0    )    # 65000
    #bgp_route_target    = json_settings.get('bgp_route_target',    '0:0')    # 65000:333

    #router_id           = json_endpoint_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    #route_distinguisher = json_endpoint_settings.get('route_distinguisher', '0:0'    )  # '60001:801'
    sub_interface_index = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    #vlan_id             = json_endpoint_settings.get('vlan_id',             1        )  # 400
    #address_ip          = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    #address_prefix      = json_endpoint_settings.get('address_prefix',      24       )  # 30
    #remote_router       = json_endpoint_settings.get('remote_router',       '0.0.0.0')  # '5.5.5.5'
    circuit_id          = json_endpoint_settings.get('circuit_id',          '000'    )  # '111'

    if_cirid_name         = '{:s}.{:s}'.format(endpoint_name, str(circuit_id))
    network_instance_name = 'ELAN-AC:{:s}'.format(str(circuit_id))
    connection_point_id   = 'VC-1'

    json_config_rules = [
        json_config_rule_delete(
            '/network_instance[{:s}]/connection_point[{:s}]'.format(network_instance_name, connection_point_id),
            {'name': network_instance_name, 'connection_point': connection_point_id}),

        json_config_rule_delete(
            '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, if_cirid_name),
            {'name': network_instance_name, 'id': if_cirid_name, 'interface': if_cirid_name,
            'subinterface': sub_interface_index}),

        json_config_rule_delete(
            '/network_instance[{:s}]'.format(network_instance_name),
            {'name': network_instance_name}),

        json_config_rule_delete(
            '/interface[{:s}]/subinterface[{:d}]'.format(if_cirid_name, sub_interface_index),
            {'name': if_cirid_name, 'index': sub_interface_index}),

        #json_config_rule_delete(
        #    '/network_instance[default]/protocols[STATIC]',
        #    {'name': 'default', 'identifier': 'STATIC', 'protocol_name': 'STATIC'}),

        #json_config_rule_delete(
        #    '/network_instance[default]/protocols[OSPF]',
        #    {'name': 'default', 'identifier': 'OSPF', 'protocol_name': 'OSPF'}),

        #json_config_rule_delete(
        #    '/network_instance[default]',
        #    {'name': 'default', 'type': 'DEFAULT_INSTANCE', 'router_id': router_id}),
    ]
    return json_config_rules
