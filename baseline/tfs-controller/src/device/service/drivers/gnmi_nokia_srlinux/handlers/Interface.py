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
from typing import Any, Dict, List, Tuple
from ._Handler import _Handler


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class InterfaceHandler(_Handler):
    def get_resource_key(self) -> str:
        #LOGGER.debug('Getting resource key for InterfaceHandler')
        return '/interface'

    def get_path(self) -> str:
        LOGGER.debug('Getting path for InterfaceHandler')
        return '/srl_nokia-interfaces:interface'

    def compose(self, resource_key: str, resource_value: Dict, delete: bool = False) -> Tuple[str, str]:
        name = str(resource_value['name'])
        index = int(resource_value.get('index'))

        if delete:
            PATH_TMPL = '/interface[name={:s}]/subinterface[index={:d}]'
            str_path = PATH_TMPL.format(name, index)
            str_data = json.dumps({})
            return str_path, str_data
        
        str_path = '/interface[name={:s}]'.format(name)
        json_interface = {}

        if 'name' in resource_value:
            #if_name=str(resource_value['if_name'])
            json_interface['name'] = name


        if 'admin_state' in resource_value:
            bool_admin_state = bool(resource_value['admin_state'])
            str_admin_state = 'enable' if bool_admin_state else 'disable'
            json_interface['admin-state'] = str_admin_state
 
        if 'sub_index' in resource_value:
            sub_index = int(resource_value['sub_index'])
        else:
            sub_index=0
        sub_list = json_interface.setdefault('subinterface', list())
        subif = {'index':sub_index}
        sub_list.append(subif)
            
 
        if 'sub_ipv4_admin_state' in resource_value:
            bool_ipv4_admin_state = bool(resource_value['sub_ipv4_admin_state'])
            str_ipv4_admin_state = 'enable' if bool_ipv4_admin_state else 'disable'
            ipv4 = subif.setdefault('ipv4', dict())
            ipv4['admin-state'] = str_ipv4_admin_state
            


        if 'sub_ipv4_address'  in resource_value and 'sub_ipv4_prefix'  in resource_value:
            sub_ipv4_address = str(resource_value['sub_ipv4_address'])
            sub_ipv4_prefix  = int(resource_value['sub_ipv4_prefix'])
            ipv4 = subif.setdefault('ipv4', dict())
            address_list = ipv4.setdefault('address', list())
            address_list.append({
                'ip-prefix': '{:s}/{:d}'.format(sub_ipv4_address, sub_ipv4_prefix)
            })

        if 'vlan_tagging' in resource_value:
            bool_vlan_tagging = bool(resource_value['vlan_tagging'])
            json_interface['vlan-tagging'] = bool_vlan_tagging
    
   
        if 'sub_type' in resource_value:
            sub_type = str(resource_value['sub_type'])
            subif['type'] = sub_type
 

        if 'sub_vlan_admin_state' in resource_value: 
            bool_vlan_admin_state = bool(resource_value['sub_vlan_admin_state'])
            str_vlan_admin_state = 'enable' if bool_vlan_admin_state else 'disable'
            subif['admin-state'] = str_vlan_admin_state 


        if 'sub_vlan_encap' in resource_value:
            sub_vlan_encap = str(resource_value['sub_vlan_encap'])
            vlan=subif.setdefault('vlan', dict())
            encap=vlan.setdefault('encap', dict())
            encap[sub_vlan_encap] = dict() 

        
        return str_path,json.dumps(json_interface)

    ############################PARSE##############################################################

    def parse(self, json_data: Dict) -> List[Tuple[str, Dict[str, Any]]]:
        #LOGGER.info('json_data = {:s}'.format(json.dumps(json_data)))
        # LOGGER.info('Parsing json_data for InterfaceHandler')
        # LOGGER.debug('json_data = {:s}'.format(json.dumps(json_data)))
        json_interface_list : List[Dict] = json_data.get('srl_nokia-interfaces:interface', [])
        response = []

        for json_interface in json_interface_list:
            #LOGGER.info('json_interface = {:s}'.format(json.dumps(json_interface)))
            interface = {}
            interface_name = json_interface.get('name')
            if interface_name is None:
            #    LOGGER.info('DISCARDED json_interface = {:s}'.format(json.dumps(json_interface)))
                continue
            interface['name'] = interface_name
            #LOGGER.info('json_interface = {:s}'.format(json.dumps(json_interface)))
            admin_state = json_interface.get('admin-state')  
            if admin_state is None:
                continue
            interface['admin_state'] = str(admin_state) 
            ##LOGGER.info('json_interface = {:s}'.format(json.dumps(json_interface)))
            #vlan_tagging = json_interface.get('srl_nokia-interfaces-vlans:vlan-tagging')
            #if vlan_tagging is not None:
            #    continue
            #interface['vlan-tagging']=bool(vlan_tagging)
            #LOGGER.info('interface = {:s}'.format(json.dumps(interface)))

            json_subinterface_list: List[Dict] = json_interface.get('subinterface', [])
            for json_subinterface in json_subinterface_list:
                #LOGGER.info('json_subinterface = {:s}'.format(json.dumps(json_subinterface)))
                subinterface = {}
                subinterface_index = json_subinterface.get('index')
                if subinterface_index is None:
                    continue
                subinterface['index'] = int(subinterface_index)
                subinterface_adminstate = json_subinterface.get('admin-state')
                if subinterface_adminstate is None:
                    continue
                subinterface['admin-state'] = str(subinterface_adminstate)
                vlan_type = json_subinterface.get('type')
                #if vlan_type is None:
                #    continue
                subinterface['type'] = vlan_type
                ipv4_admin_state = json_subinterface.get('ipv4', {}).get('admin-state')
                subinterface['ipv4'] = {'admin-state': bool(ipv4_admin_state)}
                ipv4_address_list = json_subinterface.get('ipv4', {}).get('address', [])
                addresses = []
                if ipv4_address_list:
                    for json_address in ipv4_address_list:
                        #LOGGER.info('json_address = {:s}'.format(json.dumps(json_address)))
                        address_ip_prefix = json_address.get('ip-prefix')
    
                    if address_ip_prefix is not None:
                        addresses.append({'ip-prefix': str(address_ip_prefix)})
                subinterface['ipv4'] = {'address': addresses}
                subinterface['vlan'] = {}
                subinterface['vlan']['encap'] = {}
                json_vlan_encap = json_interface.get('vlan', {}).get('encap', {})
                if json_vlan_encap:
                    if 'vlan' not in subinterface:
                        subinterface['vlan'] = {}

                    if 'encap' not in subinterface['vlan']:
                        subinterface['vlan']['encap'] = {}

                subinterface['vlan']['encap']['untagged'] = json_vlan_encap


                if len(subinterface) == 0:
                   continue
                resource_key = '/interface[{:s}]/subinterface[{:s}]'.format(interface['name'], str(subinterface['index']))
                response.append((resource_key, subinterface))

                
            if len(interface) == 0:
                    continue
            response.append(('/interface[{:s}]'.format(interface['name']), interface))
#                json_protocols = json_data.get('protocols', {})
#                json_bgp_list: List[Dict] = json_protocols.get('bgp', [])
#
#                for json_bgp in json_bgp_list:
#                    json_afi_safi_list: List[Dict] = json_bgp.get('afi-safi', [])
#
#                for json_afi_safi in json_afi_safi_list:
#                    interface['afisafiname'] = json_afi_safi.get('afi-safi-name', '')
#                    response.append((self.compose('/interfaces/interface', interface)))
#
        return response
