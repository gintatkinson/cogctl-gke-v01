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


import json, logging
from typing import Any, Dict, List, Tuple
from ._Handler import _Handler

LOGGER = logging.getLogger(__name__)

class RoutingPolicyHandler(_Handler):
    def get_resource_key(self) -> str:
        return '/routing-policy'

    def get_path(self) -> str:
        return '/srl_nokia-routing-policy:routing-policy'

    def compose(self, resource_key: str, resource_value: Dict, delete: bool = False) -> Tuple[str, str]:
        if delete:
            str_path = '/routing-policy'
            str_data = json.dumps({})
            return str_path, str_data
        
        str_path = '/routing-policy'   

        if 'name' in resource_value:
            name = str(resource_value['name'])
            json_routing = {
                'policy': {
                    'name': name,
                    'default-action': {
                        'policy-result': ''
                    }
                }
            }

        if 'policy_result' in resource_value:
            policy_result = str(resource_value['policy_result'])
            if 'policy' not in json_routing:
                json_routing['policy'] = {}
            json_routing['policy']['default-action'] = {
                        'policy-result': policy_result
            }
        return str_path, json.dumps(json_routing)
    
    def parse(self, json_data: Dict) -> List[Tuple[str, Dict[str, Any]]]:
        response = []
        json_policy = json_data.get('policy', [])
        lists = []
        for policy in json_policy:
            policyy = {}
            name = policy.get('name', {})
            default = policy.get('default-action', {}).get('policy-result', {})
            policyy['name'] = str(name)
            policyy['default-action'] = {}
            policyy['default-action']['policy-result'] = str(default)
            lists.append(policyy)  

            if len(lists) == 0:
              continue

            resource_key = '/srl_nokia-routing-policy:routing-policy'
            response.append((resource_key, lists))

        return response
