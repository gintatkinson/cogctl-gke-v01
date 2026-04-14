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


# Ref: https://osm.etsi.org/wikipub/index.php/WIM
WIM_MAPPING  = [
    {
        'device-id'           : 'dev-1',            # pop_switch_dpid
        #'device_interface_id' : ??,                # pop_switch_port
        'service_endpoint_id' : 'ep-1',             # wan_service_endpoint_id
        'service_mapping_info': {                   # wan_service_mapping_info, other extra info
            'bearer': {'bearer-reference': 'R1-EMU:13/1/2'},
            'site-id': '1',
        },
        #'switch_dpid'         : ??,                # wan_switch_dpid
        #'switch_port'         : ??,                # wan_switch_port
        #'datacenter_id'       : ??,                # vim_account
    },
    {
        'device-id'           : 'dev-2',            # pop_switch_dpid
        #'device_interface_id' : ??,                # pop_switch_port
        'service_endpoint_id' : 'ep-2',             # wan_service_endpoint_id
        'service_mapping_info': {                   # wan_service_mapping_info, other extra info
            'bearer': {'bearer-reference': 'R2-EMU:13/1/2'},
            'site-id': '2',
        },
        #'switch_dpid'         : ??,                # wan_switch_dpid
        #'switch_port'         : ??,                # wan_switch_port
        #'datacenter_id'       : ??,                # vim_account
    },
    {
        'device-id'           : 'dev-3',            # pop_switch_dpid
        #'device_interface_id' : ??,                # pop_switch_port
        'service_endpoint_id' : 'ep-3',             # wan_service_endpoint_id
        'service_mapping_info': {                   # wan_service_mapping_info, other extra info
            'bearer': {'bearer-reference': 'R3-EMU:13/1/2'},
            'site-id': '3',
        },
        #'switch_dpid'         : ??,                # wan_switch_dpid
        #'switch_port'         : ??,                # wan_switch_port
        #'datacenter_id'       : ??,                # vim_account
    },
    {
        'device-id'           : 'dev-4',            # pop_switch_dpid
        #'device_interface_id' : ??,                # pop_switch_port
        'service_endpoint_id' : 'ep-4',             # wan_service_endpoint_id
        'service_mapping_info': {                   # wan_service_mapping_info, other extra info
            'bearer': {'bearer-reference': 'R4-EMU:13/1/2'},
            'site-id': '4',
        },
        #'switch_dpid'         : ??,                # wan_switch_dpid
        #'switch_port'         : ??,                # wan_switch_port
        #'datacenter_id'       : ??,                # vim_account
    },
]

SERVICE_TYPE = 'ELINE'

SERVICE_CONNECTION_POINTS_1 = [
    {'service_endpoint_id': 'ep-1',
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': 1234}},
    {'service_endpoint_id': 'ep-2',
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': 1234}},
]

SERVICE_CONNECTION_POINTS_2 = [
    {'service_endpoint_id': 'ep-3',
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': 1234}},
]
