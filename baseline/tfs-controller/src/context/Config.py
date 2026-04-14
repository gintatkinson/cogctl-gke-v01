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

TRUE_VALUES = {'Y', 'YES', 'T', 'TRUE', 'E', 'ENABLE', 'ENABLED'}
def is_enabled(setting_name : str, default_value : bool) -> bool:
    _is_enabled = get_setting(setting_name, default=None)
    if _is_enabled is None: return default_value
    str_is_enabled = str(_is_enabled).upper()
    return str_is_enabled in TRUE_VALUES

DEFAULT_VALUE = False
ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY = is_enabled('ALLOW_EXPLICIT_ADD_DEVICE_TO_TOPOLOGY', DEFAULT_VALUE)
ALLOW_EXPLICIT_ADD_LINK_TO_TOPOLOGY   = is_enabled('ALLOW_EXPLICIT_ADD_LINK_TO_TOPOLOGY',   DEFAULT_VALUE)
