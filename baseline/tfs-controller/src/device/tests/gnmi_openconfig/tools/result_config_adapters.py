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

import re
from typing import Dict, Tuple

def adapt_endpoint(resource_key : str, resource_value : Dict) -> Tuple[str, Dict]:
    return resource_key, resource_value

def adapt_interface(resource_key : str, resource_value : Dict) -> Tuple[str, Dict]:
    return resource_key, resource_value

def adapt_network_instance(resource_key : str, resource_value : Dict) -> Tuple[str, Dict]:
    match = re.match(r'^\/network\_instance\[([^\]]+)\]\/vlan\[([^\]]+)\]$', resource_key)
    if match is not None:
        members = resource_value.get('members')
        if len(members) > 0: resource_value['members'] = sorted(members)
    return resource_key, resource_value
