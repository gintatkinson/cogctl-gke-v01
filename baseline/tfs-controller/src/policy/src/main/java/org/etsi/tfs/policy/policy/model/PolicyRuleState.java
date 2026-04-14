/*
 * Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.etsi.tfs.policy.policy.model;

public class PolicyRuleState {

    private PolicyRuleStateEnum policyRuleStateEnum;
    private String policyRuleStateMessage;

    public PolicyRuleState(PolicyRuleStateEnum policyRuleStateEnum, String policyRuleStateMessage) {
        this.policyRuleStateEnum = policyRuleStateEnum;
        this.policyRuleStateMessage = policyRuleStateMessage;
    }

    public void setRuleState(PolicyRuleStateEnum policyRuleStateEnum) {
        this.policyRuleStateEnum = policyRuleStateEnum;
    }

    public PolicyRuleStateEnum getRuleState() {
        return policyRuleStateEnum;
    }

    public void setPolicyRuleStateMessage(String policyRuleStateMessage) {
        this.policyRuleStateMessage = policyRuleStateMessage;
    }

    public String getPolicyRuleStateMessage() {
        return this.policyRuleStateMessage;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{ruleState:\"%s\"}", getClass().getSimpleName(), policyRuleStateEnum.toString());
    }
}
