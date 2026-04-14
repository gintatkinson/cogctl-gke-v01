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

from typing import Dict, List, Tuple

def compose_resources(
    storage : Dict[Tuple, Dict], config_struct : List[Tuple[str, List[str]]]
) -> List[Dict]:
    expected_config = list()

    for resource_key_fields, resource_value_data in storage.items():
        for resource_key_template, resource_key_field_names in config_struct:
            if isinstance(resource_key_fields, (str, int, float, bool)): resource_key_fields = (resource_key_fields,)
            resource_key = resource_key_template.format(*resource_key_fields)
            resource_value = {
                field_name : resource_value_data[field_name]
                for field_name in resource_key_field_names
                if field_name in resource_value_data and resource_value_data[field_name] is not None
            }
            expected_config.append((resource_key, resource_value))

    return expected_config
