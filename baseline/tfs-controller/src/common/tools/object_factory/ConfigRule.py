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

import json
from typing import Any, Dict, Union
from common.proto.context_pb2 import ConfigActionEnum

def json_config_rule(
    action : ConfigActionEnum, resource_key : str, resource_value : Union[str, Dict[str, Any]]
) -> Dict:
    if not isinstance(resource_value, str): resource_value = json.dumps(resource_value, sort_keys=True)
    return {'action': action, 'custom': {'resource_key': resource_key, 'resource_value': resource_value}}

def json_config_rule_set(resource_key : str, resource_value : Union[str, Dict[str, Any]]) -> Dict:
    return json_config_rule(ConfigActionEnum.CONFIGACTION_SET, resource_key, resource_value)

def json_config_rule_delete(resource_key : str, resource_value : Union[str, Dict[str, Any]]) -> Dict:
    return json_config_rule(ConfigActionEnum.CONFIGACTION_DELETE, resource_key, resource_value)
