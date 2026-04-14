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
from typing import Dict, List, Optional
from common.proto.policy_pb2 import PolicyRuleStateEnum

LOGGER = logging.getLogger(__name__)

def json_policyrule_id(policyrule_uuid : str) -> Dict:
    return {'uuid': {'uuid': policyrule_uuid}}

def json_policyrule(
    policyrule_uuid : str, policy_priority : int = 1, policy_kpi_id : str = '',
    policy_state : PolicyRuleStateEnum = PolicyRuleStateEnum.POLICY_UNDEFINED, policy_state_message : str = '',
    action_list : List[Dict] = [], service_id : Optional[Dict] = None, device_id_list : List[Dict] = []
) -> Dict:
    basic = {
        'policyRuleId': json_policyrule_id(policyrule_uuid),
        'policyRuleState': {
            'policyRuleState': policy_state,
            'policyRuleStateMessage': policy_state_message,
        },
        'priority': policy_priority,
        'kpiId': {'kpi_id': {'uuid': policy_kpi_id}},
        'actionList': action_list,
    }

    result = {}
    if service_id is not None:
        policyrule_type = 'service'
        result[policyrule_type] = {'policyRuleBasic': basic}
        result[policyrule_type]['serviceId'] = service_id
    else:
        policyrule_type = 'device'
        result[policyrule_type] = {'policyRuleBasic': basic}

    result[policyrule_type]['deviceList'] = device_id_list
    return result
