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


import enum

class TableEnum(enum.Enum):
    FILTER = 'filter'
    MANGLE = 'mangle'
    NAT    = 'nat'
    RAW    = 'raw'
    ROUTE  = 'route'

def get_table_from_str(table : str) -> TableEnum:
    return TableEnum._value2member_map_[table]
