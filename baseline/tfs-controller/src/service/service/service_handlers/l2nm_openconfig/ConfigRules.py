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

    mtu                     = json_settings.get('mtu',                 1450 )    # 1512
    #address_families       = json_settings.get('address_families',    []   )    # ['IPV4']
    #bgp_as                 = json_settings.get('bgp_as',              0    )    # 65000
    #bgp_route_target       = json_settings.get('bgp_route_target',    '0:0')    # 65000:333

    #router_id              = json_endpoint_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    #route_distinguisher    = json_endpoint_settings.get('route_distinguisher', '0:0'    )  # '60001:801'
    sub_interface_index     = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    vlan_id                 = json_endpoint_settings.get('vlan_id',             1        )  # 400
    #address_ip             = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    #address_prefix         = json_endpoint_settings.get('address_prefix',      24       )  # 30
    remote_router           = json_endpoint_settings.get('remote_router',       '5.5.5.5')  # '5.5.5.5'
    network_instance_name   = json_endpoint_settings.get('ni_name',             'ELAN-AC:{:s}'.format(str(vlan_id)))  #ELAN-AC:1
    # virtual_circuit_id      = json_endpoint_settings.get('vc_id',               '111'    )  # '111'
    connection_point        = json_endpoint_settings.get('conn_point',          '1'       ) # '111'
    #network_interface_desc    = '{:s}-NetIf'.format(service_uuid)
    network_interface_desc    = json_endpoint_settings.get('ni_description','')
    #network_subinterface_desc = '{:s}-NetSubIf'.format(service_uuid)
    network_subinterface_desc = json_endpoint_settings.get('subif_description','')
    
    if_cirid_name           = '{:s}.{:d}'.format(endpoint_name, vlan_id)
    connection_point_id     = 'VC-{:s}'.format(str(connection_point))                   #Provisionalmente comentado, en principio se deberia usar asi
    #connection_point_id     = 'VC-1'                                                   #Uso provisional
    virtual_circuit_id      = vlan_id

    json_config_rules = [

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
            {'name': network_instance_name, 'connection_point': connection_point_id, 'VC_ID': virtual_circuit_id,
             'remote_system': remote_router}),
    ]
    for res_key, res_value in endpoint_acls:
        json_config_rules.append(
               {'action': 1, 'acl': res_value}
            )
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
    vlan_id             = json_endpoint_settings.get('vlan_id',             1        )  # 400
    #address_ip          = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    #address_prefix      = json_endpoint_settings.get('address_prefix',      24       )  # 30
    #remote_router       = json_endpoint_settings.get('remote_router',       '0.0.0.0')  # '5.5.5.5'
    #circuit_id          = json_endpoint_settings.get('circuit_id',          '000'    )  # '111'

    if_cirid_name         = '{:s}.{:d}'.format(endpoint_name, vlan_id)
    network_instance_name = 'ELAN-AC:{:s}'.format(str(vlan_id))
    connection_point_id   = 'VC-1'

    json_config_rules = [

        #json_config_rule_delete(
        #    '/network_instance[{:s}]/connection_point[{:s}]'.format(network_instance_name, connection_point_id),
        #    {'name': network_instance_name, 'connection_point': connection_point_id, 'VC_ID': circuit_id}),

        #json_config_rule_delete(
        #    '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, if_cirid_name),
        #    {'name': network_instance_name, 'id': if_cirid_name, 'interface': if_cirid_name,
        #     'subinterface': sub_interface_index}),

        json_config_rule_delete(
            '/network_instance[{:s}]'.format(network_instance_name),
            {'name': network_instance_name}),

        json_config_rule_delete(
            '/interface[{:s}]/subinterface[{:d}]'.format(if_cirid_name, sub_interface_index),
            {'name': if_cirid_name, 'index': sub_interface_index}),

    ]
    return json_config_rules
