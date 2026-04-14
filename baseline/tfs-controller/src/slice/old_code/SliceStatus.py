# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum

class SliceStatus(Enum):
    PLANNED = 0
    INIT    = 1
    ACTIVE  = 2
    DEINIT  = 3

ANY_TO_ENUM = {
    0: SliceStatus.PLANNED,
    1: SliceStatus.INIT,
    2: SliceStatus.ACTIVE,
    3: SliceStatus.DEINIT,

    '0': SliceStatus.PLANNED,
    '1': SliceStatus.INIT,
    '2': SliceStatus.ACTIVE,
    '3': SliceStatus.DEINIT,

    'planned': SliceStatus.PLANNED,
    'init': SliceStatus.INIT,
    'active': SliceStatus.ACTIVE,
    'deinit': SliceStatus.DEINIT,
}

def slicestatus_enum_values():
    return {m.value for m in SliceStatus.__members__.values()}

def to_slicestatus_enum(int_or_str):
    if isinstance(int_or_str, str): int_or_str = int_or_str.lower()
    return ANY_TO_ENUM.get(int_or_str)
