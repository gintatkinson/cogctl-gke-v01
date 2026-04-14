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

import functools
from typing import Any, Dict, List, Optional, Tuple
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from service.service.service_handler_api.AnyTreeTools import TreeNode

def get_settings_containers(
    service_settings : TreeNode, device_settings : TreeNode, endpoint_settings : TreeNode
) -> List[Dict]:
    settings_containers : List[Dict] = list()

    # highest priority settings container
    if endpoint_settings is not None:
        json_endpoint_settings : Dict = endpoint_settings.value
        settings_containers.append(json_endpoint_settings)

    if device_settings is not None:
        json_device_settings : Dict = device_settings.value
        settings_containers.append(json_device_settings)

    # lowest priority settings container
    if service_settings is not None:
        json_service_settings : Dict = service_settings.value
        settings_containers.append(json_service_settings)

    return settings_containers

def get_value(containers : List[Dict], field_name : str, **kwargs) -> Optional[Any]:
    if len(containers) == 0: raise Exception('No containers specified')

    for container in containers:
        if field_name not in container: continue
        return container[field_name]

    if 'default' in kwargs:
        return kwargs['default']

    MSG = 'Field({:s}) not found in containers specified({:s}) and no default value specified'
    # pylint: disable=broad-exception-raised
    raise Exception(MSG.format(str(field_name), str(containers)))

def setup_config_rules(
    service_uuid : str, connection_uuid : str, device_uuid : str, endpoint_uuid : str, endpoint_name : str,
    service_settings : TreeNode, device_settings : TreeNode, endpoint_settings : TreeNode, endpoint_acls : List [Tuple]
) -> List[Dict]:

    settings_containers : Tuple[Dict] = get_settings_containers(
        service_settings, device_settings, endpoint_settings
    )
    get_settings_value = functools.partial(get_value, settings_containers)

    mtu                       = get_settings_value('mtu',                 default=1450       )  # 1512
    #address_families         = get_settings_value('address_families',    default=[]         )  # ['IPV4']
    bgp_as                    = get_settings_value('bgp_as',              default=65000      )  # 65000
    router_id                 = get_settings_value('router_id',           default='0.0.0.0'  )  # '10.95.0.10'
    route_distinguisher       = get_settings_value('route_distinguisher', default='65000:101')  # '60001:801'
    sub_interface_index       = get_settings_value('sub_interface_index', default=0          )  # 1
    vlan_id                   = get_settings_value('vlan_id',             default=1          )  # 400
    address_ip                = get_settings_value('address_ip',          default='0.0.0.0'  )  # '2.2.2.1'
    address_prefix            = get_settings_value('address_prefix',      default=24         )  # 30
    policy_import             = get_settings_value('policy_AZ',           default='2'        )  # 2
    policy_export             = get_settings_value('policy_ZA',           default='7'        )  # 30
    #network_interface_desc    = '{:s}-NetIf'.format(service_uuid)
    network_interface_desc    = get_settings_value('ni_description',      default=''         )
    #network_subinterface_desc = '{:s}-NetSubIf'.format(service_uuid)
    network_subinterface_desc = get_settings_value('subif_description',   default=''         )
    service_short_uuid       = service_uuid.split('-')[-1]
    #network_instance_name    = '{:s}-NetInst'.format(service_short_uuid)
    network_instance_name     = get_settings_value('ni_name',             default=service_short_uuid) #ELAN-AC:1

    if_subif_name       = '{:s}.{:d}'.format(endpoint_name, vlan_id)

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
                #'router_id': router_id,
                #'address_families': address_families,
        }),

        #Add BGP protocol to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/protocols[BGP]'.format(network_instance_name), {
                'name': network_instance_name, 
                'protocol_name': 'BGP', 
                'identifier': 'BGP', 
                'type': 'L3VRF',
                'as': bgp_as,
                'router_id': router_id, 
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

        #Create interface with subinterface
        json_config_rule_set(
            '/interface[{:s}]/subinterface[{:d}]'.format(if_subif_name, sub_interface_index), {
                'name'          : if_subif_name,
                'type'          :'l3ipvlan',
                'mtu'           : mtu,
                'index'         : sub_interface_index,
                'description'   : network_subinterface_desc, 
                'vlan_id'       : vlan_id,
                'address_ip'    : address_ip, 
                'address_prefix': address_prefix,
        }),

        #Associate interface to network instance
        json_config_rule_set(
            '/network_instance[{:s}]/interface[{:s}]'.format(network_instance_name, if_subif_name), {
                'name'        : network_instance_name, 
                'type'        : 'L3VRF',
                'id'          : if_subif_name, 
                'interface'   : if_subif_name,
                'subinterface': sub_interface_index,
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
                'statement_name'        : 'stm_{:s}'.format(policy_import),
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
                'statement_name'        : 'stm_{:s}'.format(policy_export),
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
        }),

        json_config_rule_set(
            '/network_instance[{:s}]/table_connections[STATIC][BGP][IPV4]'.format(network_instance_name), {
                'name'                 : network_instance_name,
                'src_protocol'         : 'STATIC',
                'dst_protocol'         : 'BGP',
                'address_family'       : 'IPV4',
                'default_import_policy': 'ACCEPT_ROUTE',
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

    settings = (json_settings, json_endpoint_settings, json_device_settings)

    service_short_uuid        = service_uuid.split('-')[-1]
    network_instance_name     = '{:s}-NetInst'.format(service_short_uuid)
    #network_interface_desc    = '{:s}-NetIf'.format(service_uuid)
    #network_subinterface_desc = '{:s}-NetSubIf'.format(service_uuid)

    #mtu                       = get_value('mtu', *settings, default=1450)   # 1512
    #address_families    = json_settings.get('address_families',             []       )  # ['IPV4']
    #bgp_as                    = get_value('bgp_as', *settings, default=65000)   # 65000
    route_distinguisher = json_settings.get('route_distinguisher',          '0:0'    )  # '60001:801'
    #sub_interface_index = json_endpoint_settings.get('sub_interface_index', 0        )  # 1
    #router_id           = json_endpoint_settings.get('router_id',           '0.0.0.0')  # '10.95.0.10'
    vlan_id             = json_endpoint_settings.get('vlan_id',             1        )  # 400
    #address_ip          = json_endpoint_settings.get('address_ip',          '0.0.0.0')  # '2.2.2.1'
    #address_prefix      = json_endpoint_settings.get('address_prefix',      24       )  # 30
    policy_import       = json_endpoint_settings.get('policy_AZ',            '2'      )  # 2
    policy_export       = json_endpoint_settings.get('policy_ZA',            '7'      )  # 30

    if_subif_name             = '{:s}.{:d}'.format(endpoint_name, vlan_id)

    json_config_rules = [
        #Delete table connections
        json_config_rule_delete(
            '/network_instance[{:s}]/table_connections[DIRECTLY_CONNECTED][BGP][IPV4]'.format(network_instance_name),{
                'name'          : network_instance_name, 
                'src_protocol'  : 'DIRECTLY_CONNECTED',
                'dst_protocol'  : 'BGP',
                'address_family': 'IPV4', 
        }),

        
        json_config_rule_delete(
            '/network_instance[{:s}]/table_connections[STATIC][BGP][IPV4]'.format(network_instance_name), {
                'name'          : network_instance_name,
                'src_protocol'  : 'STATIC',
                'dst_protocol'  : 'BGP',
                'address_family': 'IPV4',
        }),

        #Delete export routing policy 

        json_config_rule_delete(
            '/routing_policy/policy_definition[{:s}_export]'.format(network_instance_name), {
                'policy_name': '{:s}_export'.format(network_instance_name),
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_export][{:s}]'.format(policy_export, route_distinguisher), {
                'ext_community_set_name': 'set_{:s}'.format(policy_export),
        }),

        #Delete import routing policy 

        json_config_rule_delete(
            '/routing_policy/policy_definition[{:s}_import]'.format(network_instance_name), {
                'policy_name': '{:s}_import'.format(network_instance_name),
        }),
        json_config_rule_delete(
            '/routing_policy/bgp_defined_set[{:s}_rt_import][{:s}]'.format(policy_import, route_distinguisher), {
                'ext_community_set_name': 'set_{:s}'.format(policy_import),
        }),

        #Delete interface; automatically deletes:
        # - /interface[]/subinterface[]
        json_config_rule_delete('/interface[{:s}]/subinterface[0]'.format(if_subif_name),
        {
            'name': if_subif_name,
        }),

        #Delete network instance; automatically deletes:
        # - /network_instance[]/interface[]
        # - /network_instance[]/protocols[]
        # - /network_instance[]/inter_instance_policies[]
        json_config_rule_delete('/network_instance[{:s}]'.format(network_instance_name),
        {
            'name': network_instance_name
        }),
    ]
    return json_config_rules
