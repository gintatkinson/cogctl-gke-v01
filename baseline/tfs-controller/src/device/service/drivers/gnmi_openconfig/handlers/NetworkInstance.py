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

import json, libyang, logging
from typing import Any, Dict, List, Tuple
from ._Handler import _Handler
from .Tools import get_str
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

MAP_NETWORK_INSTANCE_TYPE = {
    # special routing instance; acts as default/global routing instance for a network device
    'DEFAULT': 'openconfig-network-instance-types:DEFAULT_INSTANCE',

    # private L3-only routing instance; formed of one or more RIBs
    'L3VRF': 'openconfig-network-instance-types:L3VRF',

    # private L2-only switch instance; formed of one or more L2 forwarding tables
    'L2VSI': 'openconfig-network-instance-types:L2VSI',

    # private L2-only forwarding instance; point to point connection between two endpoints
    'L2P2P': 'openconfig-network-instance-types:L2P2P',

    # private Layer 2 and Layer 3 forwarding instance
    'L2L3': 'openconfig-network-instance-types:L2L3',
}

class NetworkInstanceHandler(_Handler):
    def get_resource_key(self) -> str: return '/network_instance'
    def get_path(self) -> str: return '/openconfig-network-instance:network-instances'

    def compose(
        self, resource_key : str, resource_value : Dict, yang_handler : YangHandler, delete : bool = False
    ) -> Tuple[str, str]:
        ni_name = get_str(resource_value, 'name') # test-svc

        if delete:
            PATH_TMPL = '/network-instances/network-instance[name={:s}]'
            str_path = PATH_TMPL.format(ni_name)
            str_data = json.dumps({})
            return str_path, str_data

        ni_type = get_str(resource_value, 'type') # L3VRF / L2VSI / ...
        ni_type = MAP_NETWORK_INSTANCE_TYPE.get(ni_type, ni_type)

        str_path = '/network-instances/network-instance[name={:s}]'.format(ni_name)
        #str_data = json.dumps({
        #    'name': ni_name,
        #    'config': {'name': ni_name, 'type': ni_type},
        #})

        yang_nis : libyang.DContainer = yang_handler.get_data_path('/openconfig-network-instance:network-instances')
        yang_ni_path = 'network-instance[name="{:s}"]'.format(ni_name)
        yang_ni : libyang.DContainer = yang_nis.create_path(yang_ni_path)
        yang_ni.create_path('config/name', ni_name)
        yang_ni.create_path('config/type', ni_type)

        # 'DIRECTLY_CONNECTED' is implicitly added
        #'protocols': {'protocol': protocols},

        str_data = yang_ni.print_mem('json')
        json_data = json.loads(str_data)
        json_data = json_data['openconfig-network-instance:network-instance'][0]
        str_data = json.dumps(json_data)
        return str_path, str_data

    def parse(
        self, json_data : Dict, yang_handler : YangHandler
    ) -> List[Tuple[str, Dict[str, Any]]]:
        LOGGER.debug('json_data = {:s}'.format(json.dumps(json_data)))

        # Arista Parsing Fixes:
        # - Default instance comes with mpls/signaling-protocols/rsvp-te/global/hellos/state/hello-interval set to 0
        #   overwrite with .../hellos/config/hello-interval
        network_instances = json_data.get('openconfig-network-instance:network-instance', [])
        for network_instance in network_instances:
            if network_instance['name'] != 'default': continue
            mpls_rsvp_te = network_instance.get('mpls', {}).get('signaling-protocols', {}).get('rsvp-te', {})
            mpls_rsvp_te_hellos = mpls_rsvp_te.get('global', {}).get('hellos', {})
            hello_interval = mpls_rsvp_te_hellos.get('config', {}).get('hello-interval', 9000)
            mpls_rsvp_te_hellos.get('state', {})['hello-interval'] = hello_interval

        yang_network_instances_path = self.get_path()
        json_data_valid = yang_handler.parse_to_dict(yang_network_instances_path, json_data, fmt='json', strict=False)

        entries = []
        for network_instance in json_data_valid['network-instances']['network-instance']:
            LOGGER.debug('network_instance={:s}'.format(str(network_instance)))
            ni_name = network_instance['name']

            ni_config = network_instance['config']
            ni_type = ni_config['type'].split(':')[-1]

            _net_inst = {'name': ni_name, 'type': ni_type}
            entry_net_inst_key = '/network_instance[{:s}]'.format(ni_name)
            entries.append((entry_net_inst_key, _net_inst))

            ni_interfaces = network_instance.get('interfaces', {}).get('interface', [])
            for ni_interface in ni_interfaces:
                #ni_if_id     = ni_interface['id']
                ni_if_config = ni_interface['config']
                ni_if_name   = ni_if_config['interface']
                ni_sif_index = ni_if_config['subinterface']
                ni_if_id     = '{:s}.{:d}'.format(ni_if_name, ni_sif_index)

                _interface = {'name': ni_name, 'id': ni_if_id, 'if_name': ni_if_name, 'sif_index': ni_sif_index}
                entry_interface_key = '{:s}/interface[{:s}]'.format(entry_net_inst_key, ni_if_id)
                entries.append((entry_interface_key, _interface))

            ni_protocols = network_instance.get('protocols', {}).get('protocol', [])
            for ni_protocol in ni_protocols:
                ni_protocol_id = ni_protocol['identifier'].split(':')[-1]
                ni_protocol_name = ni_protocol['name']

                _protocol = {'name': ni_name, 'identifier': ni_protocol_id, 'protocol_name': ni_protocol_name}
                entry_protocol_key = '{:s}/protocols[{:s}]'.format(entry_net_inst_key, ni_protocol_id)
                entries.append((entry_protocol_key, _protocol))

                if ni_protocol_id == 'STATIC':
                    static_routes = ni_protocol.get('static-routes', {}).get('static', [])
                    for static_route in static_routes:
                        static_route_prefix = static_route['prefix']
                        for next_hop in static_route.get('next-hops', {}).get('next-hop', []):
                            static_route_metric = next_hop['config']['metric']
                            _static_route = {
                                'prefix'  : static_route_prefix,
                                'index'   : next_hop['index'],
                                'next_hop': next_hop['config']['next-hop'],
                                'metric'  : static_route_metric,
                            }
                            _static_route.update(_protocol)
                            entry_static_route_key = '{:s}/static_route[{:s}:{:d}]'.format(
                                entry_protocol_key, static_route_prefix, static_route_metric
                            )
                            entries.append((entry_static_route_key, _static_route))

            ni_tables = network_instance.get('tables', {}).get('table', [])
            for ni_table in ni_tables:
                ni_table_protocol = ni_table['protocol'].split(':')[-1]
                ni_table_address_family = ni_table['address-family'].split(':')[-1]
                _table = {'protocol': ni_table_protocol, 'address_family': ni_table_address_family}
                entry_table_key = '{:s}/table[{:s},{:s}]'.format(
                    entry_net_inst_key, ni_table_protocol, ni_table_address_family
                )
                entries.append((entry_table_key, _table))

            ni_vlans = network_instance.get('vlans', {}).get('vlan', [])
            for ni_vlan in ni_vlans:
                ni_vlan_id = ni_vlan['vlan-id']

                #ni_vlan_config = ni_vlan['config']
                ni_vlan_state = ni_vlan['state']
                ni_vlan_name = ni_vlan_state['name']

                _members = [
                    member['state']['interface']
                    for member in ni_vlan.get('members', {}).get('member', [])
                ]
                _vlan = {'vlan_id': ni_vlan_id, 'name': ni_vlan_name, 'members': _members}
                entry_vlan_key = '{:s}/vlan[{:d}]'.format(entry_net_inst_key, ni_vlan_id)
                entries.append((entry_vlan_key, _vlan))

        return entries
