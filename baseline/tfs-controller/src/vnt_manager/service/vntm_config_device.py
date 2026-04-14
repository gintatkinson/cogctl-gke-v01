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

from typing import Dict
from common.proto.context_pb2 import ConfigRule
from common.tools.context_queries.Device import get_device
from common.tools.object_factory.ConfigRule import json_config_rule_set, json_config_rule_delete
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient

##### Config Rule Composers ####################################################

def compose_config_rule(resource_key, resource_value, delete) -> Dict:
    json_config_rule = json_config_rule_delete if delete else json_config_rule_set
    return ConfigRule(**json_config_rule(resource_key, resource_value))

def network_instance(ni_name, ni_type, ni_router_id=None, ni_route_distinguisher=None, delete=False) -> Dict:
    path = '/network_instance[{:s}]'.format(ni_name)
    data = {'name': ni_name, 'type': ni_type}
    if ni_router_id is not None: data['router_id'] = ni_router_id
    if ni_route_distinguisher is not None: data['route_distinguisher'] = ni_route_distinguisher
    return compose_config_rule(path, data, delete)

def network_instance_add_protocol_bgp(ni_name, ni_type, ni_router_id, ni_bgp_as, neighbors=[], delete=False)-> Dict:
    path = '/network_instance[{:s}]/protocols[BGP]'.format(ni_name)
    data = {
        'name': ni_name, 'type': ni_type, 'router_id': ni_router_id, 'identifier': 'BGP',
        'protocol_name': ni_bgp_as, 'as': ni_bgp_as
    }
    if len(neighbors) > 0:
        data['neighbors'] = [
            {'ip_address': neighbor_ip_address, 'remote_as': neighbor_remote_as}
            for neighbor_ip_address, neighbor_remote_as in neighbors
        ]
    return compose_config_rule(path, data, delete)

def network_instance_add_protocol_direct(ni_name, ni_type, delete=False) -> Dict:
    path = '/network_instance[{:s}]/protocols[DIRECTLY_CONNECTED]'.format(ni_name)
    data = {
        'name': ni_name, 'type': ni_type, 'identifier': 'DIRECTLY_CONNECTED',
        'protocol_name': 'DIRECTLY_CONNECTED'
    }
    return compose_config_rule(path, data, delete)

def network_instance_add_protocol_static(ni_name, ni_type, delete=False) -> Dict:
    path = '/network_instance[{:s}]/protocols[STATIC]'.format(ni_name)
    data = {
        'name': ni_name, 'type': ni_type, 'identifier': 'STATIC',
        'protocol_name': 'STATIC'
    }
    return compose_config_rule(path, data, delete)

def network_instance_add_table_connection(
    ni_name, src_protocol, dst_protocol, address_family, default_import_policy, bgp_as=None, delete=False
) -> Dict:
    path = '/network_instance[{:s}]/table_connections[{:s}][{:s}][{:s}]'.format(
        ni_name, src_protocol, dst_protocol, address_family
    )
    data = {
        'name': ni_name, 'src_protocol': src_protocol, 'dst_protocol': dst_protocol,
        'address_family': address_family, 'default_import_policy': default_import_policy,
    }
    if bgp_as is not None: data['as'] = bgp_as
    return compose_config_rule(path, data, delete)

def interface(
    name, index, description=None, if_type=None, vlan_id=None, mtu=None, ipv4_address_prefix=None,
    enabled=None, delete=False
) -> Dict:
    path = '/interface[{:s}]/subinterface[{:d}]'.format(name, index)
    data = {'name': name, 'index': index}
    if description is not None: data['description'] = description
    if if_type     is not None: data['type'       ] = if_type
    if vlan_id     is not None: data['vlan_id'    ] = vlan_id
    if mtu         is not None: data['mtu'        ] = mtu
    if enabled     is not None: data['enabled'    ] = enabled
    if ipv4_address_prefix is not None:
        ipv4_address, ipv4_prefix = ipv4_address_prefix
        data['address_ip'    ] = ipv4_address
        data['address_prefix'] = ipv4_prefix
    return compose_config_rule(path, data, delete)

def network_instance_interface(ni_name, ni_type, if_name, if_index, delete=False) -> Dict:
    path = '/network_instance[{:s}]/interface[{:s}.{:d}]'.format(ni_name, if_name, if_index)
    data = {'name': ni_name, 'type': ni_type, 'id': if_name, 'interface': if_name, 'subinterface': if_index}
    return compose_config_rule(path, data, delete)

# configure('CSGW1', 'xe5', 'CSGW2', 'xe5', 'ecoc2024-1')
# deconfigure('CSGW1', 'xe5', 'CSGW2', 'xe5', 'ecoc2024-1')

def configure(router_a, port_a, router_b, port_b, ni_name):
    context_client = ContextClient()
    device_client = DeviceClient()

    client_if_name       = 'ce1'
    client_if_addr       = {'CSGW1': ('192.168.10.1', 24), 'CSGW2': ('192.168.20.1', 24)}
    bgp_router_addresses = {'CSGW1': '192.168.150.1', 'CSGW2': '192.168.150.2'}

    locations = [
        {'router': router_a, 'port': port_a, 'neighbor': router_b},
        {'router': router_b, 'port': port_b, 'neighbor': router_a},
    ]
    for location in locations:
        router   = location['router']
        port     = location['port']
        neighbor = location['neighbor']

        client_ipv4_address_prefix = client_if_addr[router]
        bgp_router_address         = bgp_router_addresses[router]
        bgp_neighbor_address       = bgp_router_addresses[neighbor]

        config_rules = [
            network_instance(ni_name, 'L3VRF', bgp_router_address, '65001:1'),
            network_instance_add_protocol_direct(ni_name, 'L3VRF'),
            network_instance_add_protocol_static(ni_name, 'L3VRF'),
            network_instance_add_protocol_bgp(ni_name, 'L3VRF', bgp_router_address, '65001', neighbors=[
                (bgp_neighbor_address, '65001')
            ]),
            network_instance_add_table_connection(
                ni_name, 'DIRECTLY_CONNECTED', 'BGP', 'IPV4', 'ACCEPT_ROUTE', bgp_as='65001'
            ),
            network_instance_add_table_connection(
                ni_name, 'STATIC', 'BGP', 'IPV4', 'ACCEPT_ROUTE', bgp_as='65001'
            ),
        
            interface(client_if_name, 0, if_type='ethernetCsmacd', mtu=1500),
            network_instance_interface(ni_name, 'L3VRF', client_if_name, 0),
            interface(client_if_name, 0, if_type='ethernetCsmacd', mtu=1500,
                    ipv4_address_prefix=client_ipv4_address_prefix, enabled=True),

            interface(port, 0, if_type='ethernetCsmacd', mtu=1500),
            network_instance_interface(ni_name, 'L3VRF', port, 0),
            interface(port, 0, if_type='ethernetCsmacd', mtu=1500,
                      ipv4_address_prefix=(bgp_router_address, 24), enabled=True),
        ]

        device = get_device(
            context_client, router, rw_copy=True, include_endpoints=False,
            include_config_rules=False, include_components=False
        )
        device.device_config.config_rules.extend(config_rules)
        device_client.ConfigureDevice(device)


def deconfigure(router_a, port_a, router_b, port_b, ni_name):
    context_client = ContextClient()
    device_client = DeviceClient()

    client_if_name = 'ce1'

    locations = [
        {'router': router_a, 'port': port_a, 'neighbor': router_b},
        {'router': router_b, 'port': port_b, 'neighbor': router_a},
    ]
    for location in locations:
        router   = location['router']
        port     = location['port']
        #neighbor = location['neighbor']

        config_rules = [
            network_instance_interface(ni_name, 'L3VRF', client_if_name, 0, delete=True),
            network_instance_interface(ni_name, 'L3VRF', port, 0, delete=True),
            #interface(client_if_name, 0, delete=True),
            #interface(port, 0, delete=True),
            network_instance(ni_name, 'L3VRF', delete=True),
        ]

        device = get_device(
            context_client, router, rw_copy=True, include_endpoints=False,
            include_config_rules=False, include_components=False
        )
        device.device_config.config_rules.extend(config_rules)
        device_client.ConfigureDevice(device)
