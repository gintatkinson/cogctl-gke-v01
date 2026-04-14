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

import java.util.List;
import java.util.stream.Collectors;

public class PolicyRuleAction {

    private final PolicyRuleActionEnum policyRuleActionEnum;
    private final List<PolicyRuleActionConfig> policyRuleActionConfigs;

    public PolicyRuleAction(
            PolicyRuleActionEnum policyRuleActionEnum,
            List<PolicyRuleActionConfig> policyRuleActionConfigs) {

        this.policyRuleActionEnum = policyRuleActionEnum;
        this.policyRuleActionConfigs = policyRuleActionConfigs;
    }

    public PolicyRuleActionEnum getPolicyRuleActionEnum() {
        return policyRuleActionEnum;
    }

    public List<PolicyRuleActionConfig> getPolicyRuleActionConfigs() {
        return policyRuleActionConfigs;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{policyRuleActionEnum:\"%s\", [%s]}",
                getClass().getSimpleName(),
                policyRuleActionEnum.toString(),
                toString(policyRuleActionConfigs));
    }

    private <T> String toString(List<T> list) {
        return list.stream().map(T::toString).collect(Collectors.joining(", "));
    }
}
