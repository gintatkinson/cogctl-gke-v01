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


import copy, ipaddress, netifaces
from flask_restful import Api, Resource

BASE_URL = '/restconf/data/openconfig-interfaces:interfaces'

class Interfaces(Resource):
    def get(self):
        if_list = list()
        for if_name in netifaces.interfaces():
            if if_name.startswith('lo'):
                if_type = 'iana-if-type:softwareLoopback'
            else:
                if_type = 'iana-if-type:ethernetCsmacd'

            if_config = {'name': if_name, 'type': if_type, 'enabled': True}
            if_state = copy.deepcopy(if_config)
            if_state.update({'admin-status': 'UP', 'oper-status': 'UP'})
            if_data = {'name': if_name, 'config': if_config, 'state': if_state}
            if_list.append(if_data)

            sif_index = 1
            sif_config = {'index': sif_index, 'enabled': True}
            sif_state = copy.deepcopy(sif_config)
            sif_state.update({'admin-status': 'UP', 'oper-status': 'UP'})
            sif_data = {'index': sif_index, 'config': sif_config, 'state': sif_state}
            sifs = {'subinterface': [sif_data]}
            if_data['subinterfaces'] = sifs

            if_addresses = netifaces.ifaddresses(if_name)

            # MAC
            link_addresses = if_addresses.get(netifaces.AF_LINK, list())
            if not if_name.startswith('lo') and len(link_addresses) > 0:
                mac_address = link_addresses[0].get('addr')
                eth_config = {'mac-address': mac_address}
                eth_state = copy.deepcopy(eth_config)
                eth_state.update({'hw-mac-address': mac_address})
                eth_data = {'config': eth_config, 'state': eth_state}
                if_data['openconfig-if-ethernet:ethernet'] = eth_data

            # IPv4
            ipv4_addresses = if_addresses.get(netifaces.AF_INET, list())
            oc_addrs = list()
            for ipv4_address in ipv4_addresses:
                address = ipv4_address['addr']
                netmask = ipv4_address['netmask']
                ipv4n = ipaddress.ip_network(f'{address}/{netmask}', strict=False)
                prefix_len = ipv4n.prefixlen
                addr_config = {'ip': address, 'prefix-length': prefix_len}
                addr_state = copy.deepcopy(addr_config)
                ipv4_addr_data = {'ip': address, 'config': addr_config, 'state': addr_state}
                oc_addrs.append(ipv4_addr_data)
            if len(oc_addrs) > 0:
                sif_data['openconfig-if-ip:ipv4'] = {'addresses': {'address': oc_addrs}}

            # IPv6
            ipv6_addresses = if_addresses.get(netifaces.AF_INET6, list())
            oc_addrs = list()
            for ipv6_address in ipv6_addresses:
                address = ipv6_address['addr']
                netmask = ipv6_address['netmask']
                ipv6n = ipaddress.ip_network(netmask, strict=False)
                prefix_len = ipv6n.prefixlen
                addr_config = {'ip': address, 'prefix-length': prefix_len}
                addr_state = copy.deepcopy(addr_config)
                ipv6_addr_data = {'ip': address, 'config': addr_config, 'state': addr_state}
                oc_addrs.append(ipv6_addr_data)
            if len(oc_addrs) > 0:
                sif_data['openconfig-if-ip:ipv6'] = {'addresses': {'address': oc_addrs}}

        return {'openconfig-interfaces:interfaces': {'interface': if_list}}, 200

def register_restconf_openconfig_interfaces(api : Api):
    api.add_resource(Interfaces, BASE_URL)
