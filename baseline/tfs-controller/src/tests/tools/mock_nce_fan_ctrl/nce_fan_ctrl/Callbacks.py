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


class CallbackQosProfile(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/huawei-nce-app-flow:qos-profiles'
        pattern += r'/qos-profile=(?P<qos_profile_name>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        MSG = '[on_qos_profile] match={:s} path={:s} old_data={:s} new_data={:s}'
        LOGGER.warning(MSG.format(str(match.groupdict()), str(path), str(old_data), str(new_data)))
        return False


class CallbackApplication(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/huawei-nce-app-flow:applications'
        pattern += r'/application=(?P<application_name>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        MSG = '[on_application] match={:s} path={:s} old_data={:s} new_data={:s}'
        LOGGER.warning(MSG.format(str(match.groupdict()), str(path), str(old_data), str(new_data)))
        return False


class CallbackAppFlow(_Callback):
    def __init__(self) -> None:
        pattern = r'/restconf/data'
        pattern += r'/huawei-nce-app-flow:app-flows'
        pattern += r'/app-flow=(?P<app_flow_name>[^/]+)'
        super().__init__(pattern)

    def execute_data_update(
        self, match : re.Match, path : str, old_data : Optional[Dict],
        new_data : Optional[Dict]
    ) -> bool:
        MSG = '[on_app_flow] match={:s} path={:s} old_data={:s} new_data={:s}'
        LOGGER.warning(MSG.format(str(match.groupdict()), str(path), str(old_data), str(new_data)))
        return False
