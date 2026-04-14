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


from dataclasses import dataclass
from typing import Dict


@dataclass
class Ipv4Info:
    src_prefix : str = ''
    dst_prefix : str = ''
    src_port   : str = ''
    dst_port   : str = ''
    vlan       : str = ''


def extract_match_criterion_ipv4_info(match_criterion : Dict) -> Ipv4Info:
    ipv4_info = Ipv4Info()

    for type_value in match_criterion['match-type']:
        match_type = type_value['type']
        value = type_value['value'][0]

        if match_type == 'ietf-network-slice-service:source-ip-prefix':
            ipv4_info.src_prefix = value
        elif match_type == 'ietf-network-slice-service:destination-ip-prefix':
            ipv4_info.dst_prefix = value
        elif match_type == 'ietf-network-slice-service:source-tcp-port':
            ipv4_info.src_port = value
        elif match_type == 'ietf-network-slice-service:destination-tcp-port':
            ipv4_info.dst_port = value
        elif match_type == 'ietf-network-slice-service:vlan':
            ipv4_info.vlan = value

    return ipv4_info
