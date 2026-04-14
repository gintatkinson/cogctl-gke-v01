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

package org.etsi.tfs.policy.policy.service;

import jakarta.inject.Singleton;
import java.util.List;
import java.util.stream.Collectors;
import org.etsi.tfs.policy.monitoring.model.KpiValue;
import org.etsi.tfs.policy.policy.model.NumericalOperator;
import org.etsi.tfs.policy.policy.model.PolicyRuleCondition;

@Singleton
public class PolicyRuleConditionFieldsGetter {

    public List<String> getKpiIds(List<PolicyRuleCondition> policyRuleConditions) {
        return policyRuleConditions.stream()
                .map(PolicyRuleCondition::getKpiId)
                .collect(Collectors.toList());
    }

    public List<KpiValue> getKpiValues(List<PolicyRuleCondition> policyRuleConditions) {
        return policyRuleConditions.stream()
                .map(PolicyRuleCondition::getKpiValue)
                .collect(Collectors.toList());
    }

    public List<NumericalOperator> getNumericalOperators(
            List<PolicyRuleCondition> policyRuleConditions) {
        return policyRuleConditions.stream()
                .map(PolicyRuleCondition::getNumericalOperator)
                .collect(Collectors.toList());
    }
}
