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

# These hardcoded values will be updated with proper logic in second phase of the PoC

VPN_VLAN_TAGS_TO_SERVICE_NAME = {
    (21, 201): ('osu_tunnel_1', 'etht_service_1'),
    (31, 101): ('osu_tunnel_2', 'etht_service_2'),
}

OSU_TUNNEL_SETTINGS = {
    'osu_tunnel_1': {
        'odu_type': 'osuflex',
        'osuflex_number': 40,
        'bidirectional': True,
        'delay': 20,
        'ttp_channel_names': {
            ('O-PE1', '200'): 'och:1-odu2:1-oduflex:1-osuflex:2',
            ('O-PE2', '200'): 'och:1-odu2:1-oduflex:3-osuflex:1',
        }
    },
    'osu_tunnel_2': {
        'odu_type': 'osuflex',
        'osuflex_number': 40,
        'bidirectional': True,
        'delay': 20,
        'ttp_channel_names': {
            ('O-PE1', '200'): 'och:1-odu2:1-oduflex:1-osuflex:2',
            ('O-PE2', '200'): 'och:1-odu2:1-oduflex:3-osuflex:1',
        }
    },
}

ETHT_SERVICE_SETTINGS = {
    'etht_service_1': {
        'service_type': 'op-mp2mp-svc',
    },
    'etht_service_2': {
        'service_type': 'op-mp2mp-svc',
    },
}
