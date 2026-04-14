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

package org.etsi.tfs.policy;

import static org.assertj.core.api.Assertions.assertThat;

import io.quarkus.test.junit.QuarkusTest;
import java.util.List;
import java.util.UUID;
import org.etsi.tfs.policy.monitoring.model.IntegerKpiValue;
import org.etsi.tfs.policy.monitoring.model.KpiValue;
import org.etsi.tfs.policy.policy.model.NumericalOperator;
import org.etsi.tfs.policy.policy.model.PolicyRuleAction;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionConfig;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleBasic;
import org.etsi.tfs.policy.policy.model.PolicyRuleCondition;
import org.etsi.tfs.policy.policy.model.PolicyRuleDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.junit.jupiter.api.Test;

@QuarkusTest
class PolicyRuleDeviceValidationTest {

    private PolicyRuleBasic createPolicyRuleBasic(
            String policyRuleId,
            String kpiId,
            PolicyRuleState policyRuleState,
            int priority,
            List<PolicyRuleAction> policyRuleActions) {

        return new PolicyRuleBasic(policyRuleId, kpiId, policyRuleState, priority, policyRuleActions);
    }

    private List<PolicyRuleCondition> createPolicyRuleConditions(
            String kpiId, NumericalOperator numericalOperator, KpiValue<?> kpiValue) {
        final var policyRuleCondition = new PolicyRuleCondition(kpiId, numericalOperator, kpiValue);

        return List.of(policyRuleCondition);
    }

    private List<PolicyRuleAction> createPolicyRuleActions(
            PolicyRuleActionEnum policyRuleActionEnum, List<PolicyRuleActionConfig> parameters) {
        final var policyRuleAction = new PolicyRuleAction(policyRuleActionEnum, parameters);

        return List.of(policyRuleAction);
    }

    private PolicyRuleDevice createPolicyRuleDevice(
            PolicyRuleBasic policyRuleBasic, List<String> deviceIds) {

        return new PolicyRuleDevice(policyRuleBasic, deviceIds);
    }

    private List<String> createDeviceIds() {
        return List.of("deviceId1", "deviceId2");
    }

    //     @Test
    //     void shouldThrowNullPointerExceptionGivenNullPolicyRuleBasic() {
    //         final var deviceIds = createDeviceIds();

    //         assertThatExceptionOfType(NullPointerException.class)
    //                 .isThrownBy(() -> createPolicyRuleDevice(null, deviceIds));
    //     }

    //     @Test
    //     void shouldThrowNullPointerExceptionGivenNullDeviceIds() {
    //         final var policyRuleConditions =
    //                 createPolicyRuleConditions(
    //                         UUID.randomUUID().toString(),
    //                         NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN,
    //                         new IntegerKpiValue(3));
    //         final var policyRuleActions =
    //                 createPolicyRuleActions(
    //                         PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT,
    //                         List.of(UUID.randomUUID().toString(), UUID.randomUUID().toString()));

    //         final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE,
    // "1");

    //         final var policyRuleBasic =
    //                 createPolicyRuleBasic(
    //                         "policyRuleId",
    //                         3,
    //                         policyRuleState,
    //                         BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_OR,
    //                         policyRuleConditions,
    //                         policyRuleActions);

    //         assertThatExceptionOfType(NullPointerException.class)
    //                 .isThrownBy(() -> createPolicyRuleDevice(policyRuleBasic, null));
    //     }

    //     @Test
    //     void shouldThrowIllegalArgumentExceptionGivenEmptyDeviceIds() {
    //         final var policyRuleConditions =
    //                 createPolicyRuleConditions(
    //                         UUID.randomUUID().toString(),
    //                         NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL,
    //                         new IntegerKpiValue(3));
    //         final var policyRuleActions =
    //                 createPolicyRuleActions(
    //                         PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE,
    //                         List.of(UUID.randomUUID().toString(), UUID.randomUUID().toString()));

    //         final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE,
    // "1");

    //         final var policyRuleBasic =
    //                 createPolicyRuleBasic(
    //                         "policyRuleId1",
    //                         213,
    //                         policyRuleState,
    //                         BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_AND,
    //                         policyRuleConditions,
    //                         policyRuleActions);

    //         final var deviceIds = Collections.<String>emptyList();

    //         assertThatExceptionOfType(IllegalArgumentException.class)
    //                 .isThrownBy(() -> createPolicyRuleDevice(policyRuleBasic, deviceIds));
    //     }

    @Test
    void shouldCreatePolicyRuleDeviceObject() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_NOT_EQUAL,
                        new IntegerKpiValue(3));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_SET_DEVICE_STATUS,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE, "1");

        final var policyRuleBasic =
                createPolicyRuleBasic("policyRuleId", "", policyRuleState, 3, policyRuleActions);

        final var deviceIds = createDeviceIds();

        final var expectedPolicyRuleDevice = new PolicyRuleDevice(policyRuleBasic, deviceIds);

        final var policyRuleDevice = createPolicyRuleDevice(policyRuleBasic, deviceIds);

        assertThat(policyRuleDevice).usingRecursiveComparison().isEqualTo(expectedPolicyRuleDevice);
    }
}
