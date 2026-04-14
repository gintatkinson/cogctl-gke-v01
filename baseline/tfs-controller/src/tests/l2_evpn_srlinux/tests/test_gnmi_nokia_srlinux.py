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

import logging, os, time,csv
from typing import Dict, Tuple

os.environ['DEVICE_EMULATED_ONLY'] = 'YES'
from device.service.drivers.gnmi_nokia_srlinux.GnmiNokiaSrLinuxDriver import GnmiNokiaSrLinuxDriver # pylint: disable=wrong-import-position
from device.service.driver_api._Driver import (
    RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES,
    RESOURCE_ROUTING_POLICIES, RESOURCE_SERVICES
)


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def interface(
    name, admin_state, sub_index, sub_ipv4_admin_state, sub_ipv4_address, sub_ipv4_prefix
) -> Tuple[str, Dict]:
    str_path = f'/interface[name={name}]'
    str_data = {
        'name': name,
        'admin_state': admin_state,
        'sub_index': sub_index,
        'sub_ipv4_admin_state': sub_ipv4_admin_state,
        'sub_ipv4_address': sub_ipv4_address,
        'sub_ipv4_prefix': sub_ipv4_prefix,
    }
    return str_path, str_data

def vlan_interface(
    name, vlan_tagging, sub_index, sub_type, sub_vlan_admin_state, sub_vlan_encap
) -> Tuple[str, Dict]:
    str_path = f'/interface[name={name}]'
    str_data = {
        'name':name,
        'vlan_tagging': vlan_tagging,
        'sub_index': sub_index,
        'sub_type': sub_type,
        'sub_vlan_admin_state': sub_vlan_admin_state,
        'sub_vlan_encap': sub_vlan_encap,
    }
    return str_path, str_data

def routing_policy(name, policy_result) -> Tuple[str, Dict]: 
    str_path = f'/routing-policy' 
    str_data = {'name': name,'if_policy_result': policy_result}
    return str_path, str_data

def network_instance_default(
    name, interface1, interface2, admin_state_bgp, afi_safi_name_bgp, autonomous_system_bgp,
    export_policy, group_name, import_policy, peer_as, admin_state_group, afi_safi_name_group,
    admin_state_group_2, afi_safi_name_group_2, export_policy_2, group_name_2, import_policy_2,
    as_number, peer_as_2, minimum_advertisement_interval, admin_state_neighbor,
    peer_address_neighbor, peer_group_neighbor, local_address_neighbor, peer_address_neighbor_2,
    peer_group_neighbor_2, router_id
) -> Tuple[str, Dict]:
    str_path = f'/network-instance[name={name}]' 
    str_data = {    
        'name': name,
        'interface1': interface1,
        'interface2': interface2,
        'admin_state_bgp': admin_state_bgp, 
        'afi_safi_name_bgp': afi_safi_name_bgp,
        'autonomous_system_bgp': autonomous_system_bgp,
        'export_policy': export_policy, 
        'group_name': group_name, 
        'import_policy':import_policy, 
        'peer_as': peer_as,
        'admin_state_group': admin_state_group, 
        'afi_safi_name_group': afi_safi_name_group,
        'admin_state_group_2': admin_state_group_2, 
        'afi_safi_name_group_2': afi_safi_name_group_2,
        'export_policy_2': export_policy_2,
        'group_name_2': group_name_2,
        'import_policy_2': import_policy_2,
        'as_number': as_number,
        'peer_as_2': peer_as_2,
        'minimum_advertisement_interval': minimum_advertisement_interval,
        'admin_state_neighbor':  admin_state_neighbor,
        'peer_address_neighbor': peer_address_neighbor,
        'peer_group_neighbor': peer_group_neighbor,
        'local_address_neighbor': local_address_neighbor,
        'peer_address_neighbor_2': peer_address_neighbor_2,
        'peer_group_neighbor_2': peer_group_neighbor_2,
        'router_id': router_id,
    }
    return str_path, str_data

def network_instance_vrf(
    name, type, admin_state_vrf, interface1_name, vxlaninterface_name, bgp_evpn_instance_id,
    bgp_evpn_instance_admin_state, bgp_evpn_instance_vxlan_interface, bgp_evpn_instance_evi,
    bgp_vpn_instance_id, bgp_vpn_instance_export_rt, bgp_vpn_instance_import_rt
) -> Tuple[str, Dict]:
    str_path = f'/network-instance[name={name}]'
    str_data = {
        'name': name,
        'type': type,
        'admin_state_vrf': admin_state_vrf,
        'interface1_name': interface1_name,
        'vxlaninterface_name': vxlaninterface_name,
        'bgp_evpn_instance_id':  bgp_evpn_instance_id,
        'bgp_evpn_instance_admin_state': bgp_evpn_instance_admin_state,
        'bgp_evpn_instance_vxlan_interface': bgp_evpn_instance_vxlan_interface,
        'bgp_evpn_instance_evi': bgp_evpn_instance_evi,
        'bgp_vpn_instance_id': bgp_vpn_instance_id,
        'bgp_vpn_instance_export_rt': bgp_vpn_instance_export_rt,
        'bgp_vpn_instance_import_rt': bgp_vpn_instance_import_rt,
    }
    return str_path, str_data

def tunnel_interface(name, index, type_tunnel, vni_tunnel) -> Tuple[str, Dict]:
    str_path = f'/tunnel-interface[name={name}]'
    str_data = {
        'name': name,
        'index': index,
        'type_tunnel': type_tunnel,
        'vni_tunnel': vni_tunnel,
    }
    return str_path, str_data

def network_instance_interface(ni_name, name)-> Tuple[str, Dict]:
    str_path=f'/network-instance[name={ni_name} /interface{name}'
    str_data = {'name': ni_name,'name': name}
    return str_path, str_data

def network_instance_Vxlaninterface(ni_name, name)-> Tuple[str, Dict]:
    str_path=f'/network-instance[name={ni_name} /vxlan-interface{name}'
    str_data = {'name': ni_name, 'name': name}
    return str_path, str_data

def network_instance_default_spine(
    interface1_spine, interface2_spine, interface3_spine, name, admin_state_spine,
    afi_safi_name_bgp_spine, autonomous_system_bgp_spine, export_policy_spine,
    group_name_spine, import_policy_spine, peer_address_neighbor_spine,
    peeras_group_neighbor_spine, peer_group_neighbor_spine, peer_address2_neighbor_spine,
    peeras_group_neighbor2_spine, peer_group_neighbor2_spine, router_id_spine
)-> Tuple[str, Dict]:
    str_path = f'/network-instance[name={name}]'
    str_data = {
        'interface1_spine': interface1_spine,
        'interface2_spine': interface2_spine,
        'interface3_spine': interface3_spine,
        'name': name,
        'admin_state_spine': admin_state_spine,
        'afi_safi_name_bgp_spine': afi_safi_name_bgp_spine,
        'autonomous_system_bgp_spine': autonomous_system_bgp_spine,
        'export_policy_spine': export_policy_spine,
        'group_name_spine': group_name_spine,
        'import_policy_spine': import_policy_spine,
        'peer_address_neighbor_spine': peer_address_neighbor_spine,
        'peeras_group_neighbor_spine': peeras_group_neighbor_spine,
        'peer_group_neighbor_spine': peer_group_neighbor_spine,
        'peer_address2_neighbor_spine': peer_address2_neighbor_spine,
        'peeras_group_neighbor2_spine': peeras_group_neighbor2_spine,
        'peer_group_neighbor2_spine': peer_group_neighbor2_spine,
        'router_id_spine': router_id_spine,
    }
    return str_path, str_data

def test_gnmi_nokia_srlinux():
    driver_settings_leaf1 = {
        'protocol': 'gnmi',
        'username': 'admin',
        'password': 'NokiaSrl1!',
        'use_tls': True,
    }
    driver_settings_leaf2 = {
        'protocol': 'gnmi',
        'username': 'admin',
        'password': 'NokiaSrl1!',
        'use_tls': True,
    }
    driver_settings_spine = {
        'protocol': 'gnmi',
        'username': 'admin',
        'password': 'NokiaSrl1!',
        'use_tls': True,
    }

    devices = {
        'leaf1': GnmiNokiaSrLinuxDriver('172.20.20.102', 57400, **driver_settings_leaf1),
        'leaf2': GnmiNokiaSrLinuxDriver('172.20.20.103', 57400, **driver_settings_leaf2),
        'spine': GnmiNokiaSrLinuxDriver('172.20.20.101', 57400, **driver_settings_spine)
    }

    for device in devices.values():
        device.Connect()

    resources = {
        'leaf1': [
            ('routing_policy', routing_policy('', '')),
            ('interface', interface('ethernet-1/49', True, 0, True, '192.168.11.1', '30')),
            ('network_instance', network_instance_default(
                'default', 'ethernet-1/49.0', 'system0.0', True, 'ipv4-unicast', 101, 'all',
                'eBGP-underlay', 'all', 201, True, 'evpn', False, 'ipv4-unicast', 'all',
                'iBGP-overlay', 'all', 100, 100, 1, True, '10.0.0.2', 'iBGP-overlay',
                '10.0.0.1', '192.168.11.2', 'eBGP-underlay', '10.0.0.1',
            )),
            ('interface', interface('system0', True, 0, True, '10.0.0.1', '32')),
            ('vlan_interface', vlan_interface('ethernet-1/1', True, 0, 'bridged', True, 'untagged')),
            ('network_instance_vrf', network_instance_vrf(
                'vrf-1', 'mac-vrf', True, 'ethernet-1/1.0', 'vxlan1.1', 1, True, 'vxlan1.1',
                111, 1, 'target:100:111', 'target:100:111',
            )),
            ('tunnel_interface', tunnel_interface('vxlan1', 1, 'bridged', 1)),
        ],
        'leaf2': [
            ('routing_policy', routing_policy('', '')),
            ('interface', interface('ethernet-1/49', True, 0, True, '192.168.12.1', '30')),
            ('network_instance', network_instance_default(
                'default', 'ethernet-1/49.0', 'system0.0', True, 'ipv4-unicast', 102, 'all',
                'eBGP-underlay', 'all', 201, True, 'evpn', False, 'ipv4-unicast', 'all',
                'iBGP-overlay', 'all', 100, 100, 1, True, '10.0.0.1', 'iBGP-overlay',
                '10.0.0.2', '192.168.12.2', 'eBGP-underlay', '10.0.0.2',
            )),
            ('interface', interface('system0', True, 0, True, '10.0.0.2', '32')),
            ('vlan_interface', vlan_interface('ethernet-1/1', True, 0, 'bridged', True, 'untagged')),
            ('network_instance_vrf', network_instance_vrf(
                'vrf-1', 'mac-vrf', True, 'ethernet-1/1.0', 'vxlan1.1', 1, True, 'vxlan1.1',
                111, 1, 'target:100:111', 'target:100:111',
            )),
            ('tunnel_interface', tunnel_interface('vxlan1', 1, 'bridged', 1)),
        ],
        'spine': [
            ('routing_policy', routing_policy('', '')),
            ('interface', interface('ethernet-1/1', True, 0, True, '192.168.11.2', '30')),
            ('interface', interface('ethernet-1/2', True, 0, True, '192.168.12.2', '30')),
            ('network_instance', network_instance_default_spine(
                'ethernet-1/1.0', 'ethernet-1/2.0', 'system0.0', 'default', True, 'ipv4-unicast',
                201, 'all', 'eBGP-underlay', 'all', '192.168.11.1', 101, 'eBGP-underlay',
                '192.168.12.1', 102, 'eBGP-underlay', '10.0.1.1',
            )),
            ('interface', interface('system0', True, 0, True, '10.0.1.1', 32)),
        ]
    }

    # Initialize dictionary to store timing information
    timing_info = {device: {resource[0]: [] for resource in resources[device]} for device in resources}

    # Perform the configuration 10 times and measure time for each configuration set
    for device_name, device_resources in resources.items():
        for i in range(1000):
            for resource_name, resource in device_resources:
                start_time = time.time()
                devices[device_name].DeleteConfig([resource])
                end_time = time.time()
                elapsed_time = end_time - start_time
                timing_info[device_name][resource_name].append(elapsed_time)
                logging.info(f"Iteration {i+1} for {resource_name} on {device_name}: {elapsed_time:.2f} seconds")

    # Log final timing information
    for device_name, resource_timings in timing_info.items():
        for resource_name, times in resource_timings.items():
            logging.info(f"Timing information for {resource_name} on {device_name}: {times}")

    with open('timing_information_delete.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Device', 'Resource', 'Time(seconds)'])

        for device_name, resource_timings in timing_info.items():
            for resource_name, times in resource_timings.items():
                for time_taken in times:
                    writer.writerow([device_name, resource_name, f"{time_taken:.6f}"])

    for device in devices.values():
        device.Disconnect()
