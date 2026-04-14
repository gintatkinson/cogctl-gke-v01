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

from common.Settings import get_setting

SETTING_NAME_TOPOLOGY_ABSTRACTOR = 'TOPOLOGY_ABSTRACTOR'
SETTING_NAME_DLT_INTEGRATION = 'DLT_INTEGRATION'
TRUE_VALUES = {'Y', 'YES', 'TRUE', 'T', 'E', 'ENABLE', 'ENABLED'}

def is_topology_abstractor_enabled() -> bool:
    is_enabled = get_setting(SETTING_NAME_TOPOLOGY_ABSTRACTOR, default=None)
    if is_enabled is None: return False
    str_is_enabled = str(is_enabled).upper()
    return str_is_enabled in TRUE_VALUES

def is_dlt_enabled() -> bool:
    is_enabled = get_setting(SETTING_NAME_DLT_INTEGRATION, default=None)
    if is_enabled is None: return False
    str_is_enabled = str(is_enabled).upper()
    return str_is_enabled in TRUE_VALUES
