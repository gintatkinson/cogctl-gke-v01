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

DEFAULT_MTU              = 1512
DEFAULT_ADDRESS_FAMILIES = ['IPV4']
DEFAULT_BGP_AS           = 65000
DEFAULT_BGP_ROUTE_TARGET = '{:d}:{:d}'.format(DEFAULT_BGP_AS, 333)

# TODO: improve definition of bearer mappings

# Bearer mappings:
# device_uuid:endpoint_uuid => (
#   device_uuid, endpoint_uuid, router_id, route_dist, sub_if_index,
#   address_ip, address_prefix, remote_router, circuit_id)

BEARER_MAPPINGS = {
    # OFC'22
    'R1-EMU:13/1/2': ('R1-EMU', '13/1/2', '10.10.10.1', '65000:100', 400, '3.3.2.1', 24, None, None),
    'R2-EMU:13/1/2': ('R2-EMU', '13/1/2', '12.12.12.1', '65000:120', 450, '3.4.2.1', 24, None, None),
    'R3-EMU:13/1/2': ('R3-EMU', '13/1/2', '20.20.20.1', '65000:200', 500, '3.3.1.1', 24, None, None),
    'R4-EMU:13/1/2': ('R4-EMU', '13/1/2', '22.22.22.1', '65000:220', 550, '3.4.1.1', 24, None, None),

    # OECC/PSC'22 - domain 1
    'R1@D1:3/1'    : ('R1@D1', '3/1', '10.0.1.1', '65001:101', 100, '1.1.3.1', 24, None, None),
    'R1@D1:3/2'    : ('R1@D1', '3/2', '10.0.1.1', '65001:101', 100, '1.1.3.2', 24, None, None),
    'R1@D1:3/3'    : ('R1@D1', '3/3', '10.0.1.1', '65001:101', 100, '1.1.3.3', 24, None, None),
    'R2@D1:3/1'    : ('R2@D1', '3/1', '10.0.1.2', '65001:102', 100, '1.2.3.1', 24, None, None),
    'R2@D1:3/2'    : ('R2@D1', '3/2', '10.0.1.2', '65001:102', 100, '1.2.3.2', 24, None, None),
    'R2@D1:3/3'    : ('R2@D1', '3/3', '10.0.1.2', '65001:102', 100, '1.2.3.3', 24, None, None),
    'R3@D1:3/1'    : ('R3@D1', '3/1', '10.0.1.3', '65001:103', 100, '1.3.3.1', 24, None, None),
    'R3@D1:3/2'    : ('R3@D1', '3/2', '10.0.1.3', '65001:103', 100, '1.3.3.2', 24, None, None),
    'R3@D1:3/3'    : ('R3@D1', '3/3', '10.0.1.3', '65001:103', 100, '1.3.3.3', 24, None, None),
    'R4@D1:3/1'    : ('R4@D1', '3/1', '10.0.1.4', '65001:104', 100, '1.4.3.1', 24, None, None),
    'R4@D1:3/2'    : ('R4@D1', '3/2', '10.0.1.4', '65001:104', 100, '1.4.3.2', 24, None, None),
    'R4@D1:3/3'    : ('R4@D1', '3/3', '10.0.1.4', '65001:104', 100, '1.4.3.3', 24, None, None),

    # OECC/PSC'22 - domain 2
    'R1@D2:3/1'    : ('R1@D2', '3/1', '10.0.2.1', '65002:101', 100, '2.1.3.1', 24, None, None),
    'R1@D2:3/2'    : ('R1@D2', '3/2', '10.0.2.1', '65002:101', 100, '2.1.3.2', 24, None, None),
    'R1@D2:3/3'    : ('R1@D2', '3/3', '10.0.2.1', '65002:101', 100, '2.1.3.3', 24, None, None),
    'R2@D2:3/1'    : ('R2@D2', '3/1', '10.0.2.2', '65002:102', 100, '2.2.3.1', 24, None, None),
    'R2@D2:3/2'    : ('R2@D2', '3/2', '10.0.2.2', '65002:102', 100, '2.2.3.2', 24, None, None),
    'R2@D2:3/3'    : ('R2@D2', '3/3', '10.0.2.2', '65002:102', 100, '2.2.3.3', 24, None, None),
    'R3@D2:3/1'    : ('R3@D2', '3/1', '10.0.2.3', '65002:103', 100, '2.3.3.1', 24, None, None),
    'R3@D2:3/2'    : ('R3@D2', '3/2', '10.0.2.3', '65002:103', 100, '2.3.3.2', 24, None, None),
    'R3@D2:3/3'    : ('R3@D2', '3/3', '10.0.2.3', '65002:103', 100, '2.3.3.3', 24, None, None),
    'R4@D2:3/1'    : ('R4@D2', '3/1', '10.0.2.4', '65002:104', 100, '2.4.3.1', 24, None, None),
    'R4@D2:3/2'    : ('R4@D2', '3/2', '10.0.2.4', '65002:104', 100, '2.4.3.2', 24, None, None),
    'R4@D2:3/3'    : ('R4@D2', '3/3', '10.0.2.4', '65002:104', 100, '2.4.3.3', 24, None, None),

    # ECOC'22
    'DC1-GW:CS1-GW1': ('CS1-GW1', '10/1', '5.5.1.1', None, 0, None, None, '5.5.2.1', 111),
    'DC1-GW:CS1-GW2': ('CS1-GW2', '10/1', '5.5.1.2', None, 0, None, None, '5.5.2.2', 222),
    'DC2-GW:CS2-GW1': ('CS2-GW1', '10/1', '5.5.2.1', None, 0, None, None, '5.5.1.1', 111),
    'DC2-GW:CS2-GW2': ('CS2-GW2', '10/1', '5.5.2.2', None, 0, None, None, '5.5.1.2', 222),

    # NetworkX'22
    'R1:1/2': ('R1', '1/2', '5.1.1.2', None, 0, None, None, None, None),
    'R1:1/3': ('R1', '1/3', '5.1.1.3', None, 0, None, None, None, None),
    'R2:1/2': ('R2', '1/2', '5.2.1.2', None, 0, None, None, None, None),
    'R2:1/3': ('R2', '1/3', '5.2.1.3', None, 0, None, None, None, None),
    'R3:1/2': ('R3', '1/2', '5.3.1.2', None, 0, None, None, None, None),
    'R3:1/3': ('R3', '1/3', '5.3.1.3', None, 0, None, None, None, None),
    'R4:1/2': ('R4', '1/2', '5.4.1.2', None, 0, None, None, None, None),
    'R4:1/3': ('R4', '1/3', '5.4.1.3', None, 0, None, None, None, None),

    # OFC'23
    'PE1:1/1': ('PE1', '1/1', '10.1.1.1', None, 0, None, None, None, None),
    'PE1:1/2': ('PE1', '1/2', '10.1.1.2', None, 0, None, None, None, None),
    'PE2:1/1': ('PE2', '1/1', '10.2.1.1', None, 0, None, None, None, None),
    'PE2:1/2': ('PE2', '1/2', '10.2.1.2', None, 0, None, None, None, None),
    'PE3:1/1': ('PE3', '1/1', '10.3.1.1', None, 0, None, None, None, None),
    'PE3:1/2': ('PE3', '1/2', '10.3.1.2', None, 0, None, None, None, None),
    'PE4:1/1': ('PE4', '1/1', '10.4.1.1', None, 0, None, None, None, None),
    'PE4:1/2': ('PE4', '1/2', '10.4.1.2', None, 0, None, None, None, None),

    'R149:eth-1/0/22': ('R149', 'eth-1/0/22', '5.5.5.5', None, 0, None, None, '5.5.5.1', '100'),
    'R155:eth-1/0/22': ('R155', 'eth-1/0/22', '5.5.5.1', None, 0, None, None, '5.5.5.5', '100'),
    'R199:eth-1/0/21': ('R199', 'eth-1/0/21', '5.5.5.6', None, 0, None, None, '5.5.5.5', '100'),
}
