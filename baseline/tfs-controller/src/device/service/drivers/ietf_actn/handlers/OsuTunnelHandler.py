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

import enum, logging
from typing import Dict, List, Optional, Union
from common.tools.rest_conf.client.RestConfClient import RestConfClient


LOGGER = logging.getLogger(__name__)


class EndpointProtectionRoleEnum(enum.Enum):
    WORK = 'work'

class LspProtectionTypeEnum(enum.Enum):
    UNPROTECTED = 'ietf-te-types:lsp-protection-unprotected'

class LspRestorationTypeEnum(enum.Enum):
    NOT_APPLICABLE = 'ietf-te-types:lsp-restoration-not-applicable'

class TunnelAdminStateEnum(enum.Enum):
    UP = 'ietf-te-types:tunnel-admin-state-up'

class OduTypeEnum(enum.Enum):
    OSUFLEX = 'osuflex'

def compose_osu_tunnel_endpoint(
    node_id : str, tp_id : str, ttp_channel_name : str,
    protection_role : EndpointProtectionRoleEnum = EndpointProtectionRoleEnum.WORK
) -> Dict:
    return {
        'node-id': node_id, 'tp-id': tp_id, 'ttp-channel-name': ttp_channel_name,
        'protection-role': protection_role.value
    }

def compose_osu_tunnel_te_bandwidth_odu(odu_type : OduTypeEnum, number : int) -> Dict:
    return {'layer': 'odu', 'odu-type': odu_type.value, 'number': number}

def compose_osu_tunnel_protection(
    type_ : LspProtectionTypeEnum = LspProtectionTypeEnum.UNPROTECTED, reversion_disable : bool = True
) -> Dict:
    return {'protection-type': type_.value, 'protection-reversion-disable': reversion_disable}

def compose_osu_tunnel_restoration(
    type_ : LspRestorationTypeEnum = LspRestorationTypeEnum.NOT_APPLICABLE, restoration_lock : bool = False
) -> Dict:
    return {'restoration-type': type_.value, 'restoration-lock': restoration_lock}

def compose_osu_tunnel(
    name : str,
    src_node_id : str, src_tp_id : str, src_ttp_channel_name : str,
    dst_node_id : str, dst_tp_id : str, dst_ttp_channel_name : str,
    odu_type : OduTypeEnum, osuflex_number : int,
    delay : int, bidirectional : bool = True,
    admin_state : TunnelAdminStateEnum = TunnelAdminStateEnum.UP
) -> Dict:
    return {'ietf-te:tunnel': [{
        'name': name,
        'title': name.upper(),
        'admin-state': admin_state.value,
        'delay': delay,
        'te-bandwidth': compose_osu_tunnel_te_bandwidth_odu(odu_type, osuflex_number),
        'bidirectional': bidirectional,
        'source-endpoints': {'source-endpoint': [
            compose_osu_tunnel_endpoint(src_node_id, src_tp_id, src_ttp_channel_name),
        ]},
        'destination-endpoints': {'destination-endpoint': [
            compose_osu_tunnel_endpoint(dst_node_id, dst_tp_id, dst_ttp_channel_name),
        ]},
        'restoration': compose_osu_tunnel_restoration(),
        'protection': compose_osu_tunnel_protection(),
    }]}


class OsuTunnelHandler:
    def __init__(self, rest_conf_client : RestConfClient) -> None:
        self._rest_conf_client = rest_conf_client
        self._subpath_root = '/ietf-te:te/tunnels'
        self._subpath_item = self._subpath_root + '/tunnel={osu_tunnel_name:s}'


    def get(self, osu_tunnel_name : Optional[str] = None) -> Union[Dict, List]:
        if osu_tunnel_name is None:
            subpath_url = self._subpath_root
        else:
            subpath_url = self._subpath_item.format(osu_tunnel_name=osu_tunnel_name)

        data = self._rest_conf_client.get(subpath_url)

        if not isinstance(data, dict): raise ValueError('data should be a dict')
        if 'ietf-te:tunnel' not in data: return list()
        data = data['ietf-te:tunnel']
        if not isinstance(data, list): raise ValueError('data[ietf-te:tunnel] should be a list')

        osu_tunnels : List[Dict] = list()
        for item in data:
            src_endpoints = item['source-endpoints']['source-endpoint']
            if len(src_endpoints) != 1:
                MSG = 'OsuTunnel({:s}) has zero/multiple source endpoints'
                raise Exception(MSG.format(str(item)))
            src_endpoint = src_endpoints[0]

            dst_endpoints = item['destination-endpoints']['destination-endpoint']
            if len(dst_endpoints) != 1:
                MSG = 'OsuTunnel({:s}) has zero/multiple destination endpoints'
                raise Exception(MSG.format(str(item)))
            dst_endpoint = dst_endpoints[0]

            osu_tunnel = {
                'name'                : item['name'],
                'src_node_id'         : src_endpoint['node-id'],
                'src_tp_id'           : src_endpoint['tp-id'],
                'src_ttp_channel_name': src_endpoint['ttp-channel-name'],
                'dst_node_id'         : dst_endpoint['node-id'],
                'dst_tp_id'           : dst_endpoint['tp-id'],
                'dst_ttp_channel_name': dst_endpoint['ttp-channel-name'],
                'odu_type'            : item['te-bandwidth']['odu-type'],
                'osuflex_number'      : item['te-bandwidth']['number'],
                'delay'               : item['delay'],
                'bidirectional'       : item['bidirectional'],
            }
            osu_tunnels.append(osu_tunnel)

        return osu_tunnels


    def update(self, parameters : Dict) -> bool:
        name                 = parameters['name'                ]

        src_node_id          = parameters['src_node_id'         ]
        src_tp_id            = parameters['src_tp_id'           ]
        src_ttp_channel_name = parameters['src_ttp_channel_name']

        dst_node_id          = parameters['dst_node_id'         ]
        dst_tp_id            = parameters['dst_tp_id'           ]
        dst_ttp_channel_name = parameters['dst_ttp_channel_name']

        odu_type             = parameters.get('odu_type',       OduTypeEnum.OSUFLEX.value)
        osuflex_number       = parameters.get('osuflex_number', 1                        )
        delay                = parameters.get('delay',          20                       )
        bidirectional        = parameters.get('bidirectional',  True                     )

        odu_type = OduTypeEnum._value2member_map_[odu_type]

        data = compose_osu_tunnel(
            name, src_node_id, src_tp_id, src_ttp_channel_name, dst_node_id, dst_tp_id, dst_ttp_channel_name,
            odu_type, osuflex_number, delay, bidirectional=bidirectional
        )
        return self._rest_conf_client.post(self._subpath_root, body=data) is not None


    def delete(self, osu_tunnel_name : str) -> bool:
        if osu_tunnel_name is None: raise Exception('osu_tunnel_name is None')
        subpath_url = self._subpath_item.format(osu_tunnel_name=osu_tunnel_name)
        return self._rest_conf_client.delete(subpath_url)
