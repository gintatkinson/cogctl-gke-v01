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
from typing import Dict, Optional
from common.tools.rest_conf.server.restconf_server.Callbacks import _Callback


LOGGER = logging.getLogger(__name__)


class CallbackOsuTunnel(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/ietf-te:te/tunnels'
        pattern += r'/tunnel=(?P<osu_tunnel_name>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        MSG = '[on_osu_tunnel] match={:s} path={:s} old_data={:s} new_data={:s}'
        LOGGER.warning(MSG.format(str(match.groupdict()), str(path), str(old_data), str(new_data)))
        return False


class CallbackEthTService(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/ietf-eth-tran-service:etht-svc'
        pattern += r'/etht-svc-instances=(?P<etht_service_name>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        MSG = '[on_etht_service] match={:s} path={:s} old_data={:s} new_data={:s}'
        LOGGER.warning(MSG.format(str(match.groupdict()), str(path), str(old_data), str(new_data)))
        return False
