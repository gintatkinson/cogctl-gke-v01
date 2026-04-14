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
    service_settings : TreeNode, device_settings : TreeNode, endpoint_settings : TreeNode, endpoint_acls : List [Tuple]
) -> List[Dict]:

    if service_settings  is None: return []
    if device_settings   is None: return []
    if endpoint_settings is None: return []

    json_settings          : Dict = service_settings.value
    json_device_settings   : Dict = device_settings.value
    json_endpoint_settings : Dict = endpoint_settings.value

    mtu                       = json_settings.get('mtu',                          1450     )  # 1512
    #address_families         = json_settings.get('address_families',             []       )  # ['IPV4']
    bgp_as                    = json_device_settings.get('bgp_as',                       65000    )  # 65000

    router_id                 = json_device_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    route_distinguisher       = json_device_settings.get('route_distinguisher',          '65000:101'    )  # '60001:801'
    sub_interface_index       = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    vlan_id                   = json_endpoint_settings.get('vlan_id',             1        )  # 400
    address_ip                = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    address_prefix            = json_endpoint_settings.get('address_prefix',      24       )  # 30

    policy_import             = json_device_settings.get('policy_AZ',            '2'     )  # 2
    policy_export             = json_device_settings.get('policy_ZA',            '7'     )  # 30
    #network_interface_desc    = '{:s}-NetIf'.format(service_uuid)
    network_interface_desc    = json_endpoint_settings.get('ni_description','')
    #network_subinterface_desc = '{:s}-NetSubIf'.format(service_uuid)
    network_subinterface_desc = json_endpoint_settings.get('subif_description','')
    #service_short_uuid       = service_uuid.split('-')[-1]
    #network_instance_name    = '{:s}-NetInst'.format(service_short_uuid)
    network_instance_name     = json_endpoint_settings.get('ni_name',          service_uuid.split('-')[-1])  #ELAN-AC:1

    self_bgp_if_name          = json_device_settings.get('self_bgp_interface_name', '')
    self_bgp_address_ip       = json_device_settings.get('self_bgp_interface_address_ip', '')
    bgp_address_prefix        = json_device_settings.get('bgp_interface_address_prefix', '')
    bgp_sub_interface_index   = json_device_settings.get('self_bgp_sub_interface_index', 0)
    neighbor_bgp_if_address_ip= json_device_settings.get('neighbor_bgp_interface_address_ip', '0.0.0.0')  # '2.2.2.1' 

    # if_subif_name       = '{:s}.{:d}'.format(endpoint_name, 0)
    if_subif_name       = '{:s}'.format(endpoint_name[5:])

    json_config_rules = [
        # Configure Interface (not used)
        #json_config_rule_set(
        #    '/interface[{:s}]'.format(endpoint_name), {
        #        'name': endpoint_name, 
        #        'description': network_interface_desc, 
        #        'mtu': mtu,
        #}),

        #Create network instance
        json_config_rule_set(
            '/network_instance[{:s}]'.format(network_instance_name), {
                'name': network_instance_name, 
                'description': network_interface_desc, 
                'type': 'L3VRF',
                'route_distinguisher': route_distinguisher,
                'router_id': router_id,
                #'address_families': address_families,
        }),

        #Add BGP protocol to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/protocols[BGP]'.format(network_instance_name), {
                'name': network_instance_name, 
                'protocol_name': bgp_as, 
                'identifier': 'BGP', 
                'type': 'L3VRF',
                'as': bgp_as,
                'router_id': router_id, 
                'neighbors': [{'ip_address': neighbor_bgp_if_address_ip, 'remote_as': bgp_as}]
        }),

        #Add DIRECTLY CONNECTED protocol to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/protocols[DIRECTLY_CONNECTED]'.format(network_instance_name), {
                'name': network_instance_name, 
                'identifier': 'DIRECTLY_CONNECTED', 
                'protocol_name': 'DIRECTLY_CONNECTED',
        }),

        #Add STATIC protocol to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/protocols[STATIC]'.format(network_instance_name), {
                'name': network_instance_name, 
                'identifier': 'STATIC', 
                'protocol_name': 'STATIC',
        }),

        #Create interface with subinterface (without IP address)
        json_config_rule_set(
            '/interface[{:s}]/subinterface[{:d}]'.format(if_subif_name, sub_interface_index), {
                'name'       : if_subif_name,
                'type'       :'ethernetCsmacd',
                'mtu'        : mtu,
                'index'      : sub_interface_index,
                'description': network_subinterface_desc, 
                'vlan_id'    : vlan_id,
        }),

        #Associate interface to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, if_subif_name), {
                'name'          : network_instance_name, 
                'type'          : 'L3VRF',
                'id'            : if_subif_name, 
                'interface'     : if_subif_name,
                'subinterface'  : sub_interface_index,
                'address_ip'    : address_ip, 
                'address_prefix': address_prefix,
        }), 

        #Create interface with subinterface (with IP address)
        json_config_rule_set(
            '/interface[{:s}]/subinterface[{:d}]'.format(if_subif_name, sub_interface_index), {
                'name'          : if_subif_name,
                'type'          :'ethernetCsmacd',
                'mtu'           : mtu,
                'index'         : sub_interface_index,
                'description'   : network_subinterface_desc, 
                'vlan_id'       : vlan_id,
                'address_ip'    : address_ip, 
                'address_prefix': address_prefix,
        }),

        json_config_rule_set(
            '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, self_bgp_if_name), {
                'name'        : network_instance_name, 
                'type'        : 'L3VRF',
                'id'          : self_bgp_if_name, 
                'interface'   : self_bgp_if_name,
                'subinterface': bgp_sub_interface_index,
                'address_ip'    : self_bgp_address_ip, 
                'address_prefix': bgp_address_prefix,
        }), 

        #Create routing policy
        json_config_rule_set(
            '/routing_policy/bgp_defined_set[{:s}_rt_import][{:s}]'.format(policy_import,route_distinguisher), {
                'ext_community_set_name': 'set_{:s}'.format(policy_import),
                'ext_community_member'  : route_distinguisher,
        }),
        json_config_rule_set(
            # pylint: disable=duplicate-string-formatting-argument
            '/routing_policy/policy_definition[{:s}_import]/statement[{:s}]'.format(policy_import, policy_import), {
                'policy_name'           : policy_import,
                'statement_name'        : 'stm_{:s}'.format(policy_import), # OCNOS: '10',
                'ext_community_set_name': 'set_{:s}'.format(policy_import),
                'policy_result'         : 'ACCEPT_ROUTE',
        }),

        #Associate routing policy to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/inter_instance_policies[{:s}]'.format(network_instance_name, policy_import), {
                'name'         : network_instance_name,
                'import_policy': policy_import,
        }),

        #Create routing policy
        json_config_rule_set(
            '/routing_policy/bgp_defined_set[{:s}_rt_export][{:s}]'.format(policy_export, route_distinguisher), {
                'ext_community_set_name': 'set_{:s}'.format(policy_export),
                'ext_community_member'  : route_distinguisher,
        }),
        json_config_rule_set(
            # pylint: disable=duplicate-string-formatting-argument
            '/routing_policy/policy_definition[{:s}_export]/statement[{:s}]'.format(policy_export, policy_export), {
                'policy_name'           : policy_export,
                'statement_name'        : 'stm_{:s}'.format(policy_export), # OCNOS: '10',
                'ext_community_set_name': 'set_{:s}'.format(policy_export),
                'policy_result'         : 'ACCEPT_ROUTE',
        }),

        #Associate routing policy to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/inter_instance_policies[{:s}]'.format(network_instance_name, policy_export),{
                'name'         : network_instance_name,
                'export_policy': policy_export,
        }),

        #Create table connections
        json_config_rule_set(
            '/network_instance[{:s}]/table_connections[DIRECTLY_CONNECTED][BGP][IPV4]'.format(network_instance_name), {
                'name'                 : network_instance_name,
                'src_protocol'         : 'DIRECTLY_CONNECTED',
                'dst_protocol'         : 'BGP',
                'address_family'       : 'IPV4',
                'default_import_policy': 'ACCEPT_ROUTE',
                'as'                   : bgp_as,
        }),

        json_config_rule_set(
            '/network_instance[{:s}]/table_connections[STATIC][BGP][IPV4]'.format(network_instance_name), {
                'name'                 : network_instance_name,
                'src_protocol'         : 'STATIC',
                'dst_protocol'         : 'BGP',
                'address_family'       : 'IPV4',
                'default_import_policy': 'ACCEPT_ROUTE',
                'as'                   : bgp_as,
        }),

    ]

    for res_key, res_value in endpoint_acls:
        json_config_rules.append(
               {'action': 1, 'acl': res_value}
            )
    return json_config_rules

def teardown_config_rules(
    service_uuid : str, connection_uuid : str, device_uuid : str, endpoint_uuid : str, endpoint_name : str,
    service_settings : TreeNode, device_settings : TreeNode, endpoint_settings : TreeNode
) -> List[Dict]:

    if service_settings  is None: return []
    if device_settings   is None: return []
    if endpoint_settings is None: return []

    json_settings          : Dict = service_settings.value
    json_device_settings   : Dict = device_settings.value
    json_endpoint_settings : Dict = endpoint_settings.value

    service_short_uuid        = service_uuid.split('-')[-1]
    # network_instance_name     = '{:s}-NetInst'.format(service_short_uuid)
    network_instance_name     = json_endpoint_settings.get('ni_name', service_short_uuid)  #ELAN-AC:1
    #network_interface_desc    = '{:s}-NetIf'.format(service_uuid)
    # network_subinterface_desc = '{:s}-NetSubIf'.format(service_uuid)
    network_subinterface_desc = ''

    mtu                 = json_settings.get('mtu',                          1450     )  # 1512
    #address_families  = json_settings.get('address_families',             []       )  # ['IPV4']
    #bgp_as              = json_device_settings.get('bgp_as',                       65000    )  # 65000
    route_distinguisher = json_device_settings.get('route_distinguisher',          '0:0'    )  # '60001:801'
    sub_interface_index = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    #router_id           = json_device_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    vlan_id             = json_endpoint_settings.get('vlan_id',             1        )  # 400
    address_ip          = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    address_prefix      = json_endpoint_settings.get('address_prefix',      24       )  # 30
    policy_import       = json_device_settings.get('policy_AZ',            '2'      )  # 2
    policy_export       = json_device_settings.get('policy_ZA',            '7'      )  # 30

    self_bgp_if_name          = json_device_settings.get('self_bgp_interface_name', '')
    self_bgp_address_ip       = json_device_settings.get('self_bgp_interface_address_ip', '')
    bgp_address_prefix        = json_device_settings.get('bgp_interface_address_prefix', '')
    bgp_sub_interface_index   = json_device_settings.get('self_bgp_sub_interface_index', 0)

    # if_subif_name             = '{:s}.{:d}'.format(endpoint_name, vlan_id)
    if_subif_name             = '{:s}'.format(endpoint_name[5:])

    json_config_rules = [
        #Delete export routing policy 
        json_config_rule_delete(
            # pylint: disable=duplicate-string-formatting-argument
            '/routing_policy/policy_definition[{:s}_export]/statement[{:s}]'.format(policy_export, policy_export), {
                'policy_name'           : policy_export,
                'statement_name'        : 'stm_{:s}'.format(policy_export), # OCNOS: '10',
                'ext_community_set_name': 'set_{:s}'.format(policy_export),
                'policy_result'         : 'ACCEPT_ROUTE',
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_export][{:s}]'.format(policy_export, route_distinguisher), {
                'ext_community_set_name': 'set_{:s}'.format(policy_export),
                'ext_community_member'  : route_distinguisher,
        }),

        #Delete import routing policy 
        json_config_rule_delete(
            # pylint: disable=duplicate-string-formatting-argument
            '/routing_policy/policy_definition[{:s}_import]/statement[{:s}]'.format(policy_import, policy_import), {
                'policy_name'           : policy_import,
                'statement_name'        : 'stm_{:s}'.format(policy_import), # OCNOS: '10',
                'ext_community_set_name': 'set_{:s}'.format(policy_import),
                'policy_result'         : 'ACCEPT_ROUTE',
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_import][{:s}]'.format(policy_import, route_distinguisher), {
                'ext_community_set_name': 'set_{:s}'.format(policy_import),
                'ext_community_member'  : route_distinguisher,
        }),

        #Delete interface; automatically deletes:
        # - /interface[]/subinterface[]
        # json_config_rule_delete('/interface[{:s}]/subinterface[0]'.format(if_subif_name),
        # {
        #     'name': if_subif_name,
        # }),

        #Delete network instance; automatically deletes:
        # - /network_instance[]/interface[]
        # - /network_instance[]/protocols[]
        # - /network_instance[]/inter_instance_policies[]

        #Associate interface to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/interface[{:s}]'.format('default', if_subif_name), {
                'name'        : 'default', 
                'id'          : if_subif_name, 
                'interface'   : if_subif_name,
                'subinterface': sub_interface_index,
                'address_ip'    : address_ip, 
                'address_prefix': address_prefix,
        }), 
        json_config_rule_set(
            '/network_instance[{:s}]/interface[{:s}]'.format('default', self_bgp_if_name), {
                'name'        : 'default', 
                'id'          : self_bgp_if_name, 
                'interface'   : self_bgp_if_name,
                'subinterface': bgp_sub_interface_index,
                'address_ip'    : self_bgp_address_ip, 
                'address_prefix': bgp_address_prefix,
        }), 
        json_config_rule_delete('/network_instance[{:s}]'.format(network_instance_name),
        {
            'name': network_instance_name
        }),
    ]
    return json_config_rules
