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

import logging, re
from typing import Any, List, Optional, Tuple, Union
from .handlers.EthtServiceHandler import EthtServiceHandler
from .handlers.OsuTunnelHandler import OsuTunnelHandler

LOGGER = logging.getLogger(__name__)

RE_OSU_TUNNEL   = re.compile(r'^\/osu\_tunnels\/osu\_tunnel\[([^\]]+)\]$')
RE_ETHT_SERVICE = re.compile(r'^\/etht\_services\/etht\_service\[([^\]]+)\]$')

def parse_resource_key(resource_key : str) -> Tuple[Optional[str], Optional[str]]:
    re_match_osu_tunnel   = RE_OSU_TUNNEL.match(resource_key)
    osu_tunnel_name = None if re_match_osu_tunnel is None else re_match_osu_tunnel.group(1)

    re_match_etht_service = RE_ETHT_SERVICE.match(resource_key)
    etht_service_name = None if re_match_etht_service is None else re_match_etht_service.group(1)

    return osu_tunnel_name, etht_service_name

def get_osu_tunnels(
    handler_osu_tunnel : OsuTunnelHandler, results : List[Tuple[str, Union[Any, None, Exception]]],
    osu_tunnel_name : Optional[str] = None
) -> None:
    osu_tunnels = handler_osu_tunnel.get(osu_tunnel_name=osu_tunnel_name)
    for osu_tunnel in osu_tunnels:
        osu_tunnel_name = osu_tunnel['name']
        resource_key = '/osu_tunnels/osu_tunnel[{:s}]'.format(osu_tunnel_name)
        results.append((resource_key, osu_tunnel))

def get_etht_services(
    handler_etht_service : EthtServiceHandler, results : List[Tuple[str, Union[Any, None, Exception]]],
    etht_service_name : Optional[str] = None
) -> None:
    etht_services = handler_etht_service.get(etht_service_name=etht_service_name)
    for etht_service in etht_services:
        etht_service_name = etht_service['name']
        resource_key = '/etht_services/etht_service[{:s}]'.format(etht_service_name)
        results.append((resource_key, etht_service))
