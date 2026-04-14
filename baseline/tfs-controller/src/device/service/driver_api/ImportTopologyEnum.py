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

from enum import Enum
from typing import Dict

class ImportTopologyEnum(Enum):
    # While importing underlying resources, the driver just imports endpoints and exposes them directly.
    DISABLED = 'disabled'

    # While importing underlying resources, the driver just imports imports sub-devices but not links
    # connecting them. The endpoints are exposed in virtual nodes representing the sub-devices.
    # (a remotely-controlled transport domain might exist between nodes)
    DEVICES = 'devices'

    # While importing underlying resources, the driver just imports imports sub-devices and links
    # connecting them. The endpoints are exposed in virtual nodes representing the sub-devices.
    # (enables to define constrained connectivity between the sub-devices)
    TOPOLOGY = 'topology'

def get_import_topology(settings : Dict, default : ImportTopologyEnum = ImportTopologyEnum.DISABLED):
    str_import_topology = settings.get('import_topology')
    if str_import_topology is None: return default
    import_topology = ImportTopologyEnum._value2member_map_.get(str_import_topology) # pylint: disable=no-member
    if import_topology is None: raise Exception('Unexpected setting value')
    return import_topology
