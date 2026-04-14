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

import copy, grpc, pytest
from common.proto.context_pb2 import Empty
from common.proto.policy_pb2 import PolicyRuleId, PolicyRule
from context.client.ContextClient import ContextClient
from context.service.database.uuids.PolicuRule import policyrule_get_uuid
from .Objects import POLICYRULE, POLICYRULE_ID, POLICYRULE_NAME

@pytest.mark.depends(on=['context/tests/test_connection.py::test_connection'])
def test_policy(context_client : ContextClient):

    # ----- Get when the object does not exist -------------------------------------------------------------------------
    policyrule_id = PolicyRuleId(**POLICYRULE_ID)
    policyrule_uuid = policyrule_get_uuid(policyrule_id, allow_random=False)

    with pytest.raises(grpc.RpcError) as e:
        context_client.GetPolicyRule(policyrule_id)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    MSG = 'PolicyRule({:s}) not found; policyrule_uuid generated was: {:s}'
    assert e.value.details() == MSG.format(POLICYRULE_NAME, policyrule_uuid)

    # ----- List when the object does not exist ------------------------------------------------------------------------
    response = context_client.ListPolicyRuleIds(Empty())
    assert len(response.policyRuleIdList) == 0

    response = context_client.ListPolicyRules(Empty())
    assert len(response.policyRules) == 0

    # ----- Create the object ------------------------------------------------------------------------------------------
    response = context_client.SetPolicyRule(PolicyRule(**POLICYRULE))
    assert response.uuid.uuid == policyrule_uuid

    # ----- Get when the object exists ---------------------------------------------------------------------------------
    response = context_client.GetPolicyRule(PolicyRuleId(**POLICYRULE_ID))
    assert response.device.policyRuleBasic.policyRuleId.uuid.uuid == policyrule_uuid
    assert response.device.policyRuleBasic.priority == 1
    assert response.device.policyRuleBasic.kpiId.kpi_id.uuid == 'my-kpi-id'

    # ----- List when the object exists --------------------------------------------------------------------------------
    response = context_client.ListPolicyRuleIds(Empty())
    assert len(response.policyRuleIdList) == 1
    assert response.policyRuleIdList[0].uuid.uuid == policyrule_uuid

    response = context_client.ListPolicyRules(Empty())
    assert len(response.policyRules) == 1
    assert response.policyRules[0].device.policyRuleBasic.policyRuleId.uuid.uuid == policyrule_uuid
    assert response.policyRules[0].device.policyRuleBasic.priority == 1
    assert response.policyRules[0].device.policyRuleBasic.kpiId.kpi_id.uuid == 'my-kpi-id'

    # ----- Update the object ------------------------------------------------------------------------------------------
    new_policy_priority = 100
    new_policy_kpi_id = 'new-kpi-id'
    POLICYRULE_UPDATED = copy.deepcopy(POLICYRULE)
    POLICYRULE_UPDATED['device']['policyRuleBasic']['priority'] = new_policy_priority
    POLICYRULE_UPDATED['device']['policyRuleBasic']['kpiId']['kpi_id']['uuid'] = new_policy_kpi_id
    response = context_client.SetPolicyRule(PolicyRule(**POLICYRULE_UPDATED))
    assert response.uuid.uuid == policyrule_uuid

    # ----- Get when the object is modified ----------------------------------------------------------------------------
    response = context_client.GetPolicyRule(PolicyRuleId(**POLICYRULE_ID))
    assert response.device.policyRuleBasic.policyRuleId.uuid.uuid == policyrule_uuid

    # ----- List when the object is modified ---------------------------------------------------------------------------
    response = context_client.ListPolicyRuleIds(Empty())
    assert len(response.policyRuleIdList) == 1
    assert response.policyRuleIdList[0].uuid.uuid == policyrule_uuid

    response = context_client.ListPolicyRules(Empty())
    assert len(response.policyRules) == 1
    assert response.policyRules[0].device.policyRuleBasic.policyRuleId.uuid.uuid == policyrule_uuid
    assert response.policyRules[0].device.policyRuleBasic.priority == new_policy_priority
    assert response.policyRules[0].device.policyRuleBasic.kpiId.kpi_id.uuid == new_policy_kpi_id

    # ----- Remove the object ------------------------------------------------------------------------------------------
    context_client.RemovePolicyRule(PolicyRuleId(**POLICYRULE_ID))

    # ----- List after deleting the object -----------------------------------------------------------------------------
    response = context_client.ListPolicyRuleIds(Empty())
    assert len(response.policyRuleIdList) == 0

    response = context_client.ListPolicyRules(Empty())
    assert len(response.policyRules) == 0
