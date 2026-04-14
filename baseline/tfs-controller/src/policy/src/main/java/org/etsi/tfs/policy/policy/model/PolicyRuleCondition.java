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

import org.etsi.tfs.policy.monitoring.model.KpiValue;

public class PolicyRuleCondition {

    private final String kpiId;
    private final NumericalOperator numericalOperator;
    private final KpiValue<?> kpiValue;

    public PolicyRuleCondition(
            String kpiId, NumericalOperator numericalOperator, KpiValue<?> kpiValue) {
        checkNotNull(kpiId, "Kpi ID must not be null.");
        checkArgument(!kpiId.isBlank(), "Kpi ID must not be empty.");
        this.kpiId = kpiId;
        checkArgument(
                numericalOperator != NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_UNDEFINED,
                "Numerical operator cannot be undefined");
        this.numericalOperator = numericalOperator;
        checkNotNull(kpiValue, "Kpi value must not be null.");
        checkArgument(
                isKpiValueValid(kpiValue),
                "Kpi value must be: String, Float, Boolean or Integer but it was [%s].",
                kpiValue.getValue().getClass().getName());
        this.kpiValue = kpiValue;
    }

    public String getKpiId() {
        return kpiId;
    }

    public NumericalOperator getNumericalOperator() {
        return numericalOperator;
    }

    public KpiValue<?> getKpiValue() {
        return kpiValue;
    }

    private boolean isKpiValueValid(KpiValue<?> kpiValue) {
        final var kpiValueType = kpiValue.getValue();

        if (kpiValueType instanceof String) {
            return true;
        }

        if (kpiValueType instanceof Boolean) {
            return true;
        }

        if (kpiValueType instanceof Integer) {
            return true;
        }

        return kpiValueType instanceof Float;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{kpiId:\"%s\", numericalOperator:\"%s\", %s}",
                getClass().getSimpleName(), kpiId, numericalOperator.toString(), kpiValue);
    }
}
