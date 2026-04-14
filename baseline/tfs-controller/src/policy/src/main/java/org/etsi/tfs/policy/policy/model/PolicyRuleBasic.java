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

import static com.google.common.base.Preconditions.checkArgument;
import static com.google.common.base.Preconditions.checkNotNull;

import java.util.ArrayList;
import java.util.List;
import org.etsi.tfs.policy.common.Util;

public class PolicyRuleBasic {

    private String kpiId;
    private String policyRuleId;
    private PolicyRuleState policyRuleState;
    private int priority;
    private List<PolicyRuleAction> policyRuleActions;
    private Boolean isValid;
    private String exceptionMessage;

    public PolicyRuleBasic(
            String policyRuleId,
            String kpiId,
            PolicyRuleState policyRuleState,
            int priority,
            List<PolicyRuleAction> policyRuleActions) {

        try {
            checkArgument(!policyRuleId.isBlank(), "Policy rule ID must not be empty.");
            this.policyRuleId = policyRuleId;
            this.policyRuleState = policyRuleState;
            this.priority = priority;
            checkArgument(priority >= 0, "Priority value must be greater or equal than zero.");
            checkNotNull(kpiId, "Kpi ID must not be null.");
            checkArgument(!kpiId.isBlank(), "Kpi ID must not be empty.");
            this.kpiId = kpiId;
            checkArgument(!policyRuleActions.isEmpty(), "Policy Rule actions cannot be empty.");
            this.policyRuleActions = policyRuleActions;
            this.isValid = true;

        } catch (Exception e) {
            this.policyRuleId = "";
            this.priority = 0;
            this.policyRuleActions = new ArrayList<PolicyRuleAction>();
            this.isValid = false;
            this.exceptionMessage = e.getMessage();
        }
    }

    public boolean areArgumentsValid() {
        return isValid;
    }

    public String getExceptionMessage() {
        return exceptionMessage;
    }

    public List<PolicyRuleAction> getPolicyRuleActions() {
        return policyRuleActions;
    }

    public String getKpiId() {
        return kpiId;
    }

    public void setKpiId(String kpiId) {
        this.kpiId = kpiId;
    }

    public String getPolicyRuleId() {
        return policyRuleId;
    }

    public void setPolicyRuleId(String policyRuleId) {
        this.policyRuleId = policyRuleId;
    }

    public PolicyRuleState getPolicyRuleState() {
        return policyRuleState;
    }

    public void setPolicyRuleState(PolicyRuleState policyRuleState) {
        this.policyRuleState = policyRuleState;
    }

    public int getPriority() {
        return priority;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{policyRuleId:\"%s\", %s, priority:%d, [%s]}",
                getClass().getSimpleName(),
                policyRuleId,
                policyRuleState,
                priority,
                Util.toString(policyRuleActions));
    }
}
