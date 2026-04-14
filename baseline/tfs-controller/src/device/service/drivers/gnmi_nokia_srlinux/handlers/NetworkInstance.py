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

class NetworkInstanceHandler(_Handler):
    def get_resource_key(self) -> str : return '/network-instance' 
    def get_path(self) -> str: return '/srl_nokia-network-instance:network-instance'

    def compose(self, resource_key : str, resource_value : Dict, delete : bool = False) -> Tuple[str, str]:
        name = str(resource_value ['name'])
        json_networkinstance = {}

        if delete:
            PATH_TMPL = '/network-instance[name={:s}]'
            str_path = PATH_TMPL.format(name)
            str_data = json.dumps({})
            return str_path, str_data
        
        str_path = '/network-instance[name={:s}]'.format(name)

        if 'interface1' in resource_value:
            interface1 = str(resource_value['interface1'])
            subif_interface_default_list = json_networkinstance.setdefault('interface', list())
            subif_interface1 = {'name': interface1}
            subif_interface_default_list.append(subif_interface1)

        if 'interface2' in resource_value:
             interface2 = str(resource_value['interface2'])
             subif_interface2 = {'name': interface2}
             subif_interface_default_list.append(subif_interface2)

        if 'name'  in resource_value:
            json_networkinstance['name'] = name

        if 'admin_state_bgp' in resource_value:
            bool_admin_state = bool(resource_value['admin_state_bgp'])
            str_admin_state = 'enable' if bool_admin_state else 'disable'
            subif_protocol = json_networkinstance.setdefault('protocols', dict())
            subif_bgp = subif_protocol.setdefault('bgp', dict())
            subif_afisafi = subif_bgp.setdefault('afi-safi', list())
            subif_state = {'admin-state': str_admin_state}

        if 'afi_safi_name_bgp' in resource_value:
            afi_safi_name_bgp = str(resource_value['afi_safi_name_bgp'])
            subif_state['afi-safi-name'] = afi_safi_name_bgp
            subif_afisafi.append(subif_state)


        if 'autonomous_system_bgp' in resource_value:
            autonomous_system_bgp = int(resource_value['autonomous_system_bgp'])
            subif_bgp['autonomous-system'] = autonomous_system_bgp



        if 'export_policy' in resource_value:
            export_policy = str(resource_value['export_policy'])
            subif_group1 = {'export-policy': export_policy}
            subif_group = subif_bgp.setdefault('group', list())
            

        if 'group_name' in resource_value:
            group_name = str(resource_value['group_name'])
            subif_group1['group-name'] = group_name

           

        if 'import_policy' in resource_value:
            import_policy = str(resource_value['import_policy'])
            subif_group1['import-policy'] = import_policy

        if 'peer_as' in resource_value:
            peer_as = int(resource_value['peer_as'])
            subif_group1['peer-as'] = peer_as
            subif_group.append(subif_group1)

        if 'admin_state_group' in resource_value:
            bool_admin_state = bool(resource_value['admin_state_group'])
            str_admin_state = 'enable' if bool_admin_state else 'disable'
            subif_as = {'admin-state': str_admin_state}
            subif_dictonary = {}
            subif_group.append(subif_dictonary)
            afi_safi_list=subif_dictonary.setdefault('afi-safi', list())

            

        if 'afi_safi_name_group' in resource_value:
            afi_safi_name_group = str(resource_value['afi_safi_name_group'])
            subif_as['afi-safi-name'] = afi_safi_name_group
            afi_safi_list.append(subif_as)


        if 'admin_state_group_2' in resource_value:
            bool_admin_state = bool(resource_value['admin_state_group_2'])
            str_admin_state_group2 = 'enable' if bool_admin_state else 'disable'
            subif_dictonary2 = {}
            afi_safi_list.append(subif_dictonary2)
            subif_dictonary2['admin-state'] = str_admin_state_group2

        if 'afi_safi_name_group_2' in resource_value:
            afi_safi_name_group_2 = str(resource_value['afi_safi_name_group_2'])
            subif_dictonary2['afi-safi-name'] = afi_safi_name_group_2

        if 'export_policy_2' in resource_value:
            export_policy_2 = str(resource_value['export_policy_2'])
            subif_dictonary['export-policy'] = export_policy_2

        if 'group_name_2' in resource_value:
            group_name_2 = str(resource_value['group_name_2'])
            subif_dictonary['group-name'] = group_name_2

        if 'import_policy_2' in resource_value:
            import_policy_2 = str(resource_value['import_policy_2'])
            subif_dictonary['import-policy'] = import_policy_2

        if 'as_number' in resource_value:
            as_number = int(resource_value['as_number'])
            subif_dictonary['local-as'] = {}
            subif_dictonary['local-as']['as-number'] = as_number

        if 'peer_as_2' in resource_value:
            peer_as_2 = int(resource_value['peer_as_2'])
            subif_dictonary['peer-as'] = peer_as_2


        if 'minimum_advertisement_interval' in resource_value:
            minimum_advertisement_interval = int(resource_value['minimum_advertisement_interval'])
            subif_dictonary['timers'] = {}
            subif_dictonary['timers']['minimum-advertisement-interval'] = minimum_advertisement_interval



        if 'admin_state_neighbor' in resource_value:
            bool_admin_state = bool(resource_value['admin_state_neighbor'])
            str_admin_state_n = 'enable' if bool_admin_state else 'disable'
            subif_neighbor = subif_bgp.setdefault('neighbor', list())
            subif_state_n = {'admin-state': str_admin_state_n}


        if 'peer_address_neighbor' in resource_value:
            peer_address_neighbor = str(resource_value['peer_address_neighbor'])
            subif_state_n['peer-address'] = peer_address_neighbor
            #subif_protocol=json_networkinstance.setdefault('protocols',dict())
            #subif_bgp=subif_protocol.setdefault('bgp',dict())
            #subif_neighbor=subif_bgp.setdefault('neighbor',list())

        if 'peer_group_neighbor' in resource_value:
            peer_group_neighbor = str(resource_value['peer_group_neighbor'])
            subif_state_n['peer-group'] = peer_group_neighbor
            #subif_protocol=json_networkinstance.setdefault('protocols',dict())
            #subif_bgp=subif_protocol.setdefault('bgp',dict())
            #subif_neighbor=subif_bgp.setdefault('neighbor',list())

        if 'local_address_neighbor' in resource_value:
            local_address_neighbor = str(resource_value['local_address_neighbor'])
            subif_state_n['transport'] = {}
            subif_state_n['transport']['local-address'] = local_address_neighbor
            #subif_protocol=json_networkinstance.setdefault('protocols',dict())
            #subif_bgp=subif_protocol.setdefault('bgp',dict())
            #subif_neighbor=subif_bgp.setdefault('neighbor',list())
            #subif_transport={'transport':subif_lan}
            subif_neighbor.append(subif_state_n)

        if 'peer_address_neighbor_2' in resource_value:
            peer_address_neighbor_2 = str(resource_value['peer_address_neighbor_2'])
            #subif_pan2= {'peer-address':if_peer_address_neighbor_2}
            #subif_protocol=json_networkinstance.setdefault('protocols',dict())
            #subif_bgp=subif_protocol.setdefault('bgp',dict())
            #subif_neighbor=subif_bgp.setdefault('neighbor',list())
            subif_dicneighbor = {}
            subif_dicneighbor['peer-address'] = peer_address_neighbor_2


        if 'peer_group_neighbor_2' in resource_value:
            peer_group_neighbor_2 = str(resource_value['peer_group_neighbor_2'])
            #subifpgn2 = {'peer-group':if_peer_group_neighbor_2}
           # subif_protocol=json_networkinstance.setdefault('protocols',dict())
            #subif_bgp=subif_protocol.setdefault('bgp',dict())
            #subif_neighbor=subif_bgp.setdefault('neighbor',list())
            subif_dicneighbor['peer-group'] = peer_group_neighbor_2
            subif_neighbor.append(subif_dicneighbor) 


        if 'router_id' in resource_value:
            router_id = str(resource_value['router_id'])
            #subif_protocol=json_networkinstance.setdefault('protocols',dict())
            #subif_bgp=subif_protocol.setdefault('bgp',dict())
            subif_bgp['router-id'] = router_id

    ###############VRF###############3


        if 'name' in resource_value and 'type' in resource_value:
            name = str(resource_value['name'])
            type = str(resource_value['type'])
            json_networkinstance = {}
            json_networkinstance['name'] = name
            json_networkinstance['type'] = type


        #if 'if_type' in resource_value:
        #    if_type=str(resource_value['if_type'])
        #    json_networkinstance['type']=if_type

        if 'admin_state_vrf' in resource_value:
            bool_admin_state = bool(resource_value['admin_state_vrf'])
            str_admin_state = 'enable' if bool_admin_state else 'disable'
            json_networkinstance ['admin-state'] = str_admin_state

        if 'interface1_name' in resource_value:
            interface1_name= str(resource_value['interface1_name'])
            if_interface1_list = json_networkinstance.setdefault('interface', list())
            subif_interface_name = {'name': interface1_name}
            if_interface1_list.append(subif_interface_name)

        if 'vxlaninterface_name' in resource_value:
            vxlaninterface_name = str(resource_value['vxlaninterface_name'])
            vxlaninterface_name_list = json_networkinstance.setdefault('vxlan-interface', list())
            subif_vxlaninterface_name = {'name': vxlaninterface_name}
            vxlaninterface_name_list.append(subif_vxlaninterface_name)

            
        if 'bgp_evpn_instance_id' in resource_value:
            bgp_evpn_instance_id = int(resource_value['bgp_evpn_instance_id'])
            subif_protocol = json_networkinstance.setdefault('protocols', dict())
            subif_bgp_evpn = subif_protocol.setdefault('bgp-evpn', dict())
            subif_bgpinstance = subif_bgp_evpn.setdefault('bgp-instance', list())
            subif_dictonary3 = {}
            subif_bgpinstance.append(subif_dictonary3)
            subif_dictonary3['id'] = bgp_evpn_instance_id 


        if 'bgp_evpn_instance_admin_state' in resource_value:
            bool_admin_state = bool(resource_value['bgp_evpn_instance_admin_state'])
            str_admin_state = 'enable' if bool_admin_state else 'disable'
            subif_dictonary3['admin-state'] = str_admin_state


        if 'bgp_evpn_instance_vxlan_interface' in resource_value:
            bgp_evpn_instance_vxlan_interface = str(resource_value['bgp_evpn_instance_vxlan_interface'])
            subif_dictonary3['vxlan-interface'] = bgp_evpn_instance_vxlan_interface

        if 'bgp_evpn_instance_evi' in resource_value:
            bgp_evpn_instance_evi = int(resource_value['bgp_evpn_instance_evi'])
            subif_dictonary3['evi'] = bgp_evpn_instance_evi


        if 'bgp_vpn_instance_id' in resource_value:
            bgp_vpn_instance_id = int(resource_value['bgp_vpn_instance_id'])
            subif_bgp_vpn = subif_protocol.setdefault('bgp-vpn', dict())
            subif_bgpinstance = subif_bgp_vpn.setdefault('bgp-instance', list())
            subif_dictonary4 = {}
            subif_dictonary4['id'] = bgp_vpn_instance_id


        if 'bgp_vpn_instance_export_rt' in resource_value and 'bgp_vpn_instance_import_rt' in resource_value:
            bgp_vpn_instance_export_rt = str(resource_value['bgp_vpn_instance_export_rt'])
            bgp_vpn_instance_import_rt = str(resource_value['bgp_vpn_instance_import_rt'])
            subif_dictonary4['route-target'] = {}
            subif_dictonary4['route-target']['export-rt'] = bgp_vpn_instance_export_rt
            subif_dictonary4['route-target']['import-rt'] = bgp_vpn_instance_import_rt
            subif_bgpinstance.append(subif_dictonary4)

        #if 'if_bgp_vpn_instance_import_rt' in resource_value:
        #    if_bgp_vpn_instance_import_rt = str(resource_value['if_bgp_vpn_instance_import_rt'])
        #    subif_dictonary4['route-target']['import-rt']=if_bgp_vpn_instance_import_rt
        #    subif_bgpinstance.append(subif_dictonary4)

######################################SPINE##########################
        if 'interface1_spine' in resource_value:
            interface1_spine = str(resource_value['interface1_spine'])
            subif_interface_default_list = json_networkinstance.setdefault('interface', list())
            subif_interface1_spine = {'name': interface1_spine}
            subif_interface_default_list.append(subif_interface1_spine)

        if 'interface2_spine' in resource_value:
            interface2_spine = str(resource_value['interface2_spine'])
            subif_interface_default_list = json_networkinstance.setdefault('interface', list())
            subif_interface2_spine = {'name': interface2_spine}
            subif_interface_default_list.append(subif_interface2_spine)

        if 'interface3_spine' in resource_value:
            interface3_spine = str(resource_value['interface3_spine'])
            subif_interface_default_list = json_networkinstance.setdefault('interface', list())
            subif_interface3_spine = {'name': interface3_spine}
            subif_interface_default_list.append(subif_interface3_spine)

        if 'name'  in resource_value:
            json_networkinstance['name'] = name

        if 'admin_state_spine' in resource_value:
            bool_admin_state = bool(resource_value['admin_state_spine'])
            str_admin_state = 'enable' if bool_admin_state else 'disable'
            subif_protocol = json_networkinstance.setdefault('protocols', dict())
            subif_bgp = subif_protocol.setdefault('bgp', dict())
            subif_afisafi = subif_bgp.setdefault('afi-safi', list())
            subif_state = {'admin-state': str_admin_state}

        if 'afi_safi_name_bgp_spine' in resource_value:
            afi_safi_name_bgp_spine = str(resource_value['afi_safi_name_bgp_spine'])
            subif_state['afi-safi-name'] = afi_safi_name_bgp_spine
            subif_afisafi.append(subif_state)


        if 'autonomous_system_bgp_spine' in resource_value:
            autonomous_system_bgp_spine = int(resource_value['autonomous_system_bgp_spine'])
            subif_bgp['autonomous-system'] = autonomous_system_bgp_spine



        if 'export_policy_spine' in resource_value:
            export_policy_spine = str(resource_value['export_policy_spine'])
            subif_group_spine = {'export-policy': export_policy_spine}
            subif_group_spine_list = subif_bgp.setdefault('group', list())
            

        if 'group_name_spine' in resource_value:
            group_name_spine = str(resource_value['group_name_spine'])
            subif_group_spine['group-name'] = group_name_spine

           

        if 'import_policy_spine' in resource_value:
            import_policy_spine = str(resource_value['import_policy_spine'])
            subif_group_spine['import-policy'] = import_policy_spine
            subif_group_spine_list.append(subif_group_spine)
    

        if 'peer_address_neighbor_spine' in resource_value:
            peer_address_neighbor_spine = str(resource_value['peer_address_neighbor_spine'])
            subif_neighbor_spine = subif_bgp.setdefault('neighbor', list())
            subif_state_spine = {'peer-address': peer_address_neighbor_spine}


        if 'peeras_group_neighbor_spine' in resource_value:
            peeras_group_neighbor_spine = int(resource_value['peeras_group_neighbor_spine'])
            subif_state_spine['peer-as'] = peeras_group_neighbor_spine

        if 'peer_group_neighbor_spine' in resource_value:
            peer_group_neighbor_spine = str(resource_value['peer_group_neighbor_spine'])
            subif_state_spine['peer-group'] = peer_group_neighbor_spine
            subif_neighbor_spine.append(subif_state_spine)
#######Neighbor2
        if 'peer_address2_neighbor_spine' in resource_value:
            peer_address2_neighbor_spine = str(resource_value['peer_address2_neighbor_spine'])
            subif_neighbor2_spine = {}
            subif_neighbor2_spine['peer-address'] = peer_address2_neighbor_spine


        if 'peeras_group_neighbor2_spine' in resource_value:
            peeras_group_neighbor2_spine = int(resource_value['peeras_group_neighbor2_spine'])
            subif_neighbor2_spine['peer-as'] = peeras_group_neighbor2_spine

        if 'peer_group_neighbor2_spine' in resource_value:
            peer_group_neighbor2_spine = str(resource_value['peer_group_neighbor2_spine'])
            subif_neighbor2_spine['peer-group'] = peer_group_neighbor2_spine
            subif_neighbor_spine.append(subif_neighbor2_spine)

        if 'router_id_spine' in resource_value:
            router_id_spine = str(resource_value['if_router_id_spine'])
            subif_bgp['router-id'] = router_id_spine


        return str_path, json.dumps(json_networkinstance)
    def parse(self, json_data: Dict) -> List[Tuple[str, Dict[str, Any]]]:
        response = []
        json_network_instance_list = json_data.get('srl_nokia-network-instance:network-instance', [])

        for json_network_instance in json_network_instance_list:
            #LOGGER.info('json_networkinstance = {:s}'.format(json.dumps(json_network_instance)))
            network_instance = {}
            json_interface_list = json_network_instance.get('interface', [])
            json_vxlan_list = json_network_instance.get('vxlan-interface', [])
            vxlaninterface_names = [] 
            for json_vxlan in json_vxlan_list:
                #LOGGER.info('json_interface = {:s}'.format(json.dumps(json_interface)))
                # LOGGER.info('json_interface.keys = {:s}'.format(str(json_interface.keys())))
                #interface = {}
                vxlaninterface_name = json_vxlan.get('name')
       
                if vxlaninterface_names is not None:
                    vxlaninterface_names.append(str(vxlaninterface_name))
                else:
                    pass
            interface_names = []
            for json_interface in json_interface_list:
                #LOGGER.info('json_interface = {:s}'.format(json.dumps(json_interface)))
                # LOGGER.info('json_interface.keys = {:s}'.format(str(json_interface.keys())))
                #interface = {}
                interface_name = json_interface.get('name')
       
                if interface_name is not None:
                    interface_names.append(str(interface_name))            

            network_instance_name = json_network_instance.get('name')
            if network_instance is not None:
                    network_instance['name'] = str(network_instance_name)
 
            network_instance_type = json_network_instance.get('type')
            if network_instance_type is not None:
                    network_instance['type'] = str(network_instance_type)

            network_instance_adminstate = json_network_instance.get('admin-state')
            if network_instance_adminstate  is not None:
                    network_instance['admin-state'] = str(network_instance_adminstate)

            #LOGGER.info('json_network_instance.keys = {:s}'.format(str(json_network_instance.keys())))
            json_protocols = json_network_instance.get('protocols', {})
            json_bgp_evpn = json_protocols.get('bgp-evpn', {})
            json_bgp_evpn_instance = json_bgp_evpn.get('srl_nokia-bgp-evpn:bgp-instance', [])
            json_bgp_vpn_instance = json_protocols.get('srl_nokia-bgp-vpn:bgp-vpn', {})
            json_bgp_vpn_2 = json_bgp_vpn_instance.get('bgp-instance', [])
            #LOGGER.info('json_protocols.keys = {:s}'.format(str(json_protocols.keys())))
            bgp_protocols = json_protocols.get('srl_nokia-bgp:bgp', {})
            #LOGGER.info('bgp_protocols.keys = {:s}'.format(str(bgp_protocols.keys())))
            afi_safi_list: List[Dict] = bgp_protocols.get('afi-safi', [])
            #afi_safi_list = bgp_protocols.get('afi-safi', [])
            lists = []
            if afi_safi_list is not None:
                for afi_safi_entry in afi_safi_list:
                   #LOGGER.info('afi_safi_entry = {:s}'.format(json.dumps(afi_safi_entry)))
                   #afi_safi = {}
                    admin_state_afi = afi_safi_entry.get('admin-state')
                    afi_safi_name = afi_safi_entry.get('afi-safi-name')
                   
                    if admin_state_afi is not None and afi_safi_name is not None:
                       #afi_safi['admin-state'] = bool(admin_state_afi)
                       #afi_safi['afi-safi-name'] = bool(afi_safi_name)
                        lists.append({'admin-state': str(admin_state_afi), 'afi-safi-name': str(afi_safi_name)})
                    if afi_safi_entry is not None:
                        network_instance['protocols'] = {}
                        network_instance['bgp'] = {} 
                       #network_instance['protocols']['bgp']={'afi-safi': lists}
                        network_instance['protocols'] = {'bgp': {'afi-safi': afi_safi_entry}}  
  
            
            autonomous_system = bgp_protocols.get('autonomous-system')
            #LOGGER.info('bgp_protocols = {:s}'.format(json.dumps(bgp_protocols))) 

            bgp_protocols['autonomous-system'] = str(autonomous_system)

            group_list = bgp_protocols.get('group', [])
            group_list1 = []
            afi_safi_list_group_2 = []  # Ensure initialization outside the loop
            for group_1 in group_list:
                # LOGGER.info('group = {:s}'.format(json.dumps(group_1)))
                group = {}
                export_policy = group_1.get('export-policy')
                group_name = group_1.get('group-name')
                import_policy = group_1.get('import-policy')
                peer_as_number = group_1.get('peer-as')
                localas = group_1.get('local-as').get('as-number')
                timers = group_1.get('timers').get('minimum-advertisement-interval')
           
                group['export-policy'] = str(export_policy)
                group['group-name'] = str(group_name)
                group['import-policy'] = str(import_policy)
                group['peer-as'] = int(peer_as_number)
                group['local-as'] = {}
                group['local-as']['as-number'] = localas
                group['timers'] = {}
                group['timers']['minimum-advertisement-interval'] = timers
                group_list1.append(group)           
                afi_safi_list_2 = group_1.get('afi-safi', [])
                for afi_safi_group_entry in afi_safi_list_2:
                    group2 = {}
                    admin_state_group = afi_safi_group_entry.get('admin-state')
                    afi_safi_name_group = afi_safi_group_entry.get('afi-safi-name')
                    if afi_safi_list_group_2:  # Check if list is not empty
                         group2['admin-state'] = str(admin_state_group)
                         group2['afi-safi-name'] = str(afi_safi_name_group)
                         afi_safi_list_group_2.append(group2)
                                   
            neighbor_group_list = bgp_protocols.get('neighbor', [])
            neighbor_list_inside = []
            #LOGGER.info('json_neighbor = {:s}'.format(json.dumps(json_interface)))
            for neighbor_group in neighbor_group_list:
                 neighbor1 = {}
                 admin_state_neighbor = neighbor_group.get('admin-state')
                 peeraddress_neighbor = neighbor_group.get('peer-address')
                 peergroup_neighbor = neighbor_group.get('peer-group')
                 local_address_neighbor = neighbor_group.get('transport', {}).get('local-address')
                 neighbor1['admin-state'] = str(admin_state_neighbor)
                 neighbor1['peer-address'] = str(peeraddress_neighbor)
                 neighbor1['peer-group'] = str(peergroup_neighbor)
                 neighbor1['transport'] = {'local-address': str(local_address_neighbor)}

                 neighbor2 = {}
                 peeraddress_neighbor_2 = neighbor_group.get('peer-address')
                 peergroup_neighbor_2 = neighbor_group.get('peer-group')
                 neighbor2['peer-address'] = str(peeraddress_neighbor_2)
                 neighbor2['peer-group'] = str(peergroup_neighbor_2)

                 neighbor_list_inside.append((neighbor1))
                 neighbor_list_inside.append(neighbor2)

            router_id = bgp_protocols.get('router-id')

            bgp_protocols ['router-id'] = str(router_id)
                   
            bgp_instance1_list = []
            for json_bgp_instance in json_bgp_evpn_instance:
                 instance1 = {}
                 id_evpn_bgp_instance = json_bgp_instance.get('id')
                 admin_state_evpn_bgp_instance = json_bgp_instance.get('admin-state')
                 vxlan_interface_evpn_bgp_instance = json_bgp_instance.get('vxlan-interface')
                 evi_evpn_bgp_instance = json_bgp_instance.get('evi', {})
                 instance1['id'] = int(id_evpn_bgp_instance)
                 instance1['admin-state'] = str(admin_state_evpn_bgp_instance)
                 instance1['vxlan-interface'] = str(vxlan_interface_evpn_bgp_instance)
                 instance1['evi'] = int(evi_evpn_bgp_instance)       
                 bgp_instance1_list.append(instance1)  
            bgp_instance2_list = []
            for json_bgp_instance2 in json_bgp_vpn_2:
                 #LOGGER.info('json_bgp_instance2 = {:s}'.format(json.dumps(json_bgp_instance2)))
                 instance2 = {}
                 id_vpn_bgp_instance = json_bgp_instance2.get('id')
                 export_target_evpn_bgp_instance = json_bgp_instance2.get('route-target', {}).get('export-rt')
                 import_target_evpn_bgp_instance = json_bgp_instance2.get('route-target', {}).get('import-rt')
                 instance2['id'] = int(id_vpn_bgp_instance)
                 instance2['route-target'] = {}
                 instance2['route-target']['export-rt'] = str(export_target_evpn_bgp_instance)
                 instance2['route-target']['import-rt'] = str(import_target_evpn_bgp_instance)       
                 bgp_instance2_list.append(instance2)



            if len(network_instance) == 0:
                continue         
                
            #resource_key = '/network-instance[{:s}]'.format(network_instance_name)
            #response.append((resource_key,vxlaninterface_names,network_instance_type,network_instance_adminstate, interface_names,network_instance_name,lists,autonomous_system,group_list1,afi_safi_list_group_2,neighbor_list_inside,router_id,bgp_instance1_list,bgp_instance2_list))
            resource_key = '/network-instance[{:s}]'.format(network_instance_name)
            response.append((resource_key, network_instance))
        return response
