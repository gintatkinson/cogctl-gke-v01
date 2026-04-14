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
import java.util.stream.Stream;
import org.etsi.tfs.policy.monitoring.model.BooleanKpiValue;
import org.etsi.tfs.policy.monitoring.model.FloatKpiValue;
import org.etsi.tfs.policy.monitoring.model.IntegerKpiValue;
import org.etsi.tfs.policy.monitoring.model.KpiValue;
import org.etsi.tfs.policy.monitoring.model.StringKpiValue;
import org.etsi.tfs.policy.policy.model.NumericalOperator;
import org.etsi.tfs.policy.policy.model.PolicyRuleCondition;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.mockito.Mockito;

@QuarkusTest
class PolicyRuleConditionValidationTest {

    private PolicyRuleCondition createPolicyRuleCondition(
            String kpiId, NumericalOperator numericalOperator, KpiValue<?> kpiValue) {

        return new PolicyRuleCondition(kpiId, numericalOperator, kpiValue);
    }

    private static Stream<Arguments> provideKpiValues() {
        return Stream.of(
                Arguments.of(new StringKpiValue("stringKpiValue")),
                Arguments.of(new BooleanKpiValue(true)),
                Arguments.of(new IntegerKpiValue(44)),
                Arguments.of(new FloatKpiValue(12.3f)));
    }

    @ParameterizedTest
    @MethodSource("provideKpiValues")
    void shouldThrowNullPointerExceptionGivenNullKpiId(KpiValue<?> kpiValue) {
        assertThatExceptionOfType(NullPointerException.class)
                .isThrownBy(
                        () ->
                                createPolicyRuleCondition(
                                        null,
                                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                                        kpiValue));
    }

    @ParameterizedTest
    @MethodSource("provideKpiValues")
    void shouldThrowIllegalArgumentExceptionGivenEmptyKpiId(KpiValue<?> kpiValue) {
        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(
                        () ->
                                createPolicyRuleCondition(
                                        "", NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_NOT_EQUAL, kpiValue));
    }

    @ParameterizedTest
    @MethodSource("provideKpiValues")
    void shouldThrowIllegalArgumentExceptionGivenWhiteSpacedKpiId(KpiValue<?> kpiValue) {
        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(
                        () ->
                                createPolicyRuleCondition(
                                        " ", NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_NOT_EQUAL, kpiValue));
    }

    @ParameterizedTest
    @MethodSource("provideKpiValues")
    void shouldThrowIllegalArgumentExceptionGivenUndefinedNumericalOperator(KpiValue<?> kpiValue) {
        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(
                        () ->
                                createPolicyRuleCondition(
                                        "kpiId",
                                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_UNDEFINED,
                                        kpiValue));
    }

    @Test
    void shouldThrowNullPointerExceptionGivenNullKpiValue() {
        assertThatExceptionOfType(NullPointerException.class)
                .isThrownBy(
                        () ->
                                createPolicyRuleCondition(
                                        "kpiId", NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN, null));
    }

    @Test
    void shouldThrowIllegalArgumentExceptionIfIsKpiValueIsOfInvalidType() {
        final var kpiValue = Mockito.mock(KpiValue.class);
        Mockito.when(kpiValue.getValue()).thenReturn(1_2L);

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(
                        () ->
                                createPolicyRuleCondition(
                                        "kpiId",
                                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                                        kpiValue));
    }

    @ParameterizedTest
    @MethodSource("provideKpiValues")
    void shouldCreatePolicyRuleConditionObject(KpiValue<?> kpiValue) {
        final var expectedKpiId = "expectedKpiId";
        final var expectedNumericalOperator =
                NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN;

        final var expectedPolicyRuleCondition =
                new PolicyRuleCondition(expectedKpiId, expectedNumericalOperator, kpiValue);

        final var policyRuleCondition =
                createPolicyRuleCondition(
                        "expectedKpiId", NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN, kpiValue);

        assertThat(policyRuleCondition)
                .usingRecursiveComparison()
                .isEqualTo(expectedPolicyRuleCondition);
    }
}
