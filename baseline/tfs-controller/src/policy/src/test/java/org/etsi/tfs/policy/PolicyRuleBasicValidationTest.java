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
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import io.quarkus.test.junit.QuarkusTest;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import org.etsi.tfs.policy.monitoring.model.IntegerKpiValue;
import org.etsi.tfs.policy.monitoring.model.KpiValue;
import org.etsi.tfs.policy.policy.model.BooleanOperator;
import org.etsi.tfs.policy.policy.model.NumericalOperator;
import org.etsi.tfs.policy.policy.model.PolicyRuleAction;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionConfig;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleBasic;
import org.etsi.tfs.policy.policy.model.PolicyRuleCondition;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.junit.jupiter.api.Test;

// TODO: Revisit PolicyRuleBasicValidationTest cases after handling exceptions in PolicyRuleBasic
// constructor
@QuarkusTest
class PolicyRuleBasicValidationTestHelper {

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

    @Test
    void shouldThrowNullPointerExceptionGivenNullPolicyRuleId() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN,
                        new IntegerKpiValue(3));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE, "1");

        assertThatExceptionOfType(NullPointerException.class)
                .isThrownBy(() -> createPolicyRuleBasic(null, "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldThrowIllegalArgumentExceptionGivenEmptyPolicyRuleId() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                        new IntegerKpiValue(3));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_ENFORCED, "1");

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> createPolicyRuleBasic("", "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldThrowIllegalArgumentExceptionGivenWhiteSpacedPolicyRuleId() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_NOT_EQUAL,
                        new IntegerKpiValue(3));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_NO_ACTION,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_ENFORCED, "1");

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> createPolicyRuleBasic("  ", "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldThrowIllegalArgumentExceptionGivenNegativePriority() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL,
                        new IntegerKpiValue(3));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_SET_DEVICE_STATUS,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_INSERTED, "1");

        final var policyRuleId = UUID.randomUUID().toString();

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(
                        () -> createPolicyRuleBasic(policyRuleId, "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldThrowNullPointerExceptionGivenNullPolicyRuleConditions() {
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_ENFORCED, "1");

        final var policyRuleId = UUID.randomUUID().toString();

        assertThatExceptionOfType(NullPointerException.class)
                .isThrownBy(() -> createPolicyRuleBasic(null, "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldThrowIllegalArgumentExceptionGivenEmptyPolicyRuleConditions() {
        final var policyRuleConditions = Collections.<PolicyRuleCondition>emptyList();
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_REMOVED, "1");

        final var policyRuleId = UUID.randomUUID().toString();

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> createPolicyRuleBasic(null, "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldThrowIllegalArgumentExceptionGivenUndefinedBooleanOperator() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                        new IntegerKpiValue(3));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_VALIDATED, "1");

        final var policyRuleId = UUID.randomUUID().toString();

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> createPolicyRuleBasic(null, "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldThrowNullPointerExceptionGivenNullPolicyRuleActions() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                        new IntegerKpiValue(3));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_PROVISIONED, "1");

        final var policyRuleId = UUID.randomUUID().toString();

        assertThatExceptionOfType(NullPointerException.class)
                .isThrownBy(() -> createPolicyRuleBasic(null, "", policyRuleState, 3, null));
    }

    @Test
    void shouldThrowIllegalArgumentExceptionGivenEmptyPolicyPolicyRuleActions() {
        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                        new IntegerKpiValue(3));
        final var policyRuleActions = Collections.<PolicyRuleAction>emptyList();

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_FAILED, "1");

        final var policyRuleId = UUID.randomUUID().toString();

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> createPolicyRuleBasic(null, "", policyRuleState, 3, policyRuleActions));
    }

    @Test
    void shouldCreatePolicyRuleBasicObject() {
        final var expectedPolicyRuleId = "expectedPolicyRuleId";
        final var expectedPolicyRuleState =
                new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE, "1");
        final var expectedPriority = 3;

        final var firstKpiValue = new IntegerKpiValue(22);

        final var firstExpectedPolicyRuleCondition =
                new PolicyRuleCondition(
                        "firstExpectedPolicyRuleConditionVariable",
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                        firstKpiValue);

        final var expectedPolicyRuleConditions = List.of(firstExpectedPolicyRuleCondition);

        final var expectedBooleanOperator = BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_OR;

        final var firstExpectedPolicyRuleAction =
                new PolicyRuleAction(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_SET_DEVICE_STATUS,
                        List.of(new PolicyRuleActionConfig("parameter1", "parameter2")));

        final var expectedPolicyRuleActions = List.of(firstExpectedPolicyRuleAction);

        final var expectedPolicyRuleBasic =
                new PolicyRuleBasic(
                        expectedPolicyRuleId,
                        "kpiId",
                        expectedPolicyRuleState,
                        expectedPriority,
                        expectedPolicyRuleActions);

        final var policyRuleConditions =
                createPolicyRuleConditions(
                        "firstExpectedPolicyRuleConditionVariable",
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                        new IntegerKpiValue(22));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_SET_DEVICE_STATUS,
                        List.of(new PolicyRuleActionConfig("parameter1", "parameter2")));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE, "1");

        final var policyRuleBasic =
                createPolicyRuleBasic(null, "kpiId", policyRuleState, 3, policyRuleActions);

        assertThat(policyRuleBasic).usingRecursiveComparison().isEqualTo(expectedPolicyRuleBasic);
    }
}
