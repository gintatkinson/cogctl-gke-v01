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

import logging
from typing import Any, Dict, List, Optional, Tuple
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from service.service.service_handler_api.AnyTreeTools import TreeNode
LOGGER = logging.getLogger(__name__)

def get_value(field_name : str, *containers, default=None) -> Optional[Any]:
    if len(containers) == 0: raise Exception('No containers specified')
    for container in containers:
        if field_name not in container: continue
        return container[field_name]
    return default

def setup_config_rules(
    endpoint_name : str,  endpoint_tapi_lsp : List [Tuple]
) -> List[Dict]:

    json_config_rules = [
    ]

    for res_key, res_value in endpoint_tapi_lsp:
        json_config_rules.append(
               {'action': 1, 'tapi_lsp': res_value}
            )

    return json_config_rules

def teardown_config_rules(
    service_uuid : str, connection_uuid : str, device_uuid : str, endpoint_uuid : str, endpoint_name : str,
    service_settings : TreeNode, device_settings : TreeNode, endpoint_settings : TreeNode
) -> List[Dict]:

    if service_settings  is None: return []
    if device_settings   is None: return []
    if endpoint_settings is None: return []

    json_settings          : Dict = service_settings.value
    json_device_settings   : Dict = device_settings.value
    json_endpoint_settings : Dict = endpoint_settings.value

    settings = (json_settings, json_endpoint_settings, json_device_settings)

    json_config_rules = []
    return json_config_rules
