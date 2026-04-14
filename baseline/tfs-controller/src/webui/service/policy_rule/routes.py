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

import grpc
from flask import render_template, Blueprint
from common.proto.context_pb2 import Empty
from common.proto.policy_pb2 import PolicyRuleStateEnum
from context.client.ContextClient import ContextClient

policy_rule = Blueprint('policy_rule', __name__, url_prefix='/policy_rule')

context_client = ContextClient()

@policy_rule.get('/')
def home():
    context_client.connect()
    policy_rules = context_client.ListPolicyRules(Empty())
    policy_rules = policy_rules.policyRules
    context_client.close()
    return render_template('policy_rule/home.html', policy_rules=policy_rules, prse=PolicyRuleStateEnum)

#@policy_rule.get('<path:policy_rule_uuid>/detail')
#def detail(policy_rule_uuid: str):
#    try:
#        context_client.connect()
#
#        policy_rule_obj = get_policy_rule_by_uuid(context_client, policy_rule_uuid, rw_copy=False)
#        if policy_rule_obj is None:
#            flash('Context({:s})/PolicyRule({:s}) not found'.format(str(context_uuid), str(policy_rule_uuid)), 'danger')
#            policy_rule_obj = PolicyRule()
#
#        context_client.close()
#
#        return render_template(
#            'policy_rule/detail.html', policy_rule=policy_rule_obj, prse=PolicyRuleStateEnum)
#    except Exception as e:
#        flash('The system encountered an error and cannot show the details of this policy_rule.', 'warning')
#        current_app.logger.exception(e)
#        return redirect(url_for('policy_rule.home'))
