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
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import io.quarkus.test.junit.QuarkusTest;
import io.smallrye.mutiny.Uni;
import jakarta.inject.Inject;
import java.util.Collections;
import java.util.List;
import java.util.UUID;
import org.etsi.tfs.policy.context.ContextService;
import org.etsi.tfs.policy.context.model.ConfigActionEnum;
import org.etsi.tfs.policy.context.model.ConfigRule;
import org.etsi.tfs.policy.context.model.ConfigRuleCustom;
import org.etsi.tfs.policy.context.model.ConfigRuleTypeCustom;
import org.etsi.tfs.policy.context.model.Device;
import org.etsi.tfs.policy.context.model.DeviceConfig;
import org.etsi.tfs.policy.context.model.DeviceDriverEnum;
import org.etsi.tfs.policy.context.model.DeviceOperationalStatus;
import org.etsi.tfs.policy.context.model.EndPoint.EndPointBuilder;
import org.etsi.tfs.policy.context.model.EndPointId;
import org.etsi.tfs.policy.context.model.Location;
import org.etsi.tfs.policy.context.model.LocationTypeRegion;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.context.model.TopologyId;
import org.etsi.tfs.policy.kpi_sample_types.model.KpiSampleType;
import org.etsi.tfs.policy.monitoring.model.IntegerKpiValue;
import org.etsi.tfs.policy.monitoring.model.KpiValue;
import org.etsi.tfs.policy.policy.model.NumericalOperator;
import org.etsi.tfs.policy.policy.model.PolicyRuleAction;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionConfig;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleBasic;
import org.etsi.tfs.policy.policy.model.PolicyRuleCondition;
import org.etsi.tfs.policy.policy.model.PolicyRuleService;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.etsi.tfs.policy.policy.service.PolicyRuleConditionValidator;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

@QuarkusTest
class PolicyRuleServiceValidationTest {
    @Inject Serializer serializer;

    private ContextService contextService;
    private PolicyRuleConditionValidator policyRuleConditionValidator;

    @BeforeEach
    void setUp() {
        contextService = Mockito.mock(ContextService.class);
        policyRuleConditionValidator = new PolicyRuleConditionValidator(contextService);
    }

    @Test
    void testIsDeviceIdValidReturnsTrue() {
        String deviceId = "deviceId";
        Device device = createDevice(deviceId);

        when(contextService.getDevice(anyString())).thenReturn(Uni.createFrom().item(device));

        Boolean result = policyRuleConditionValidator.isDeviceIdValid(deviceId).await().indefinitely();

        assertThat(result).isEqualTo(true);
    }

    @Test
    void testIsDeviceIdValidReturnsFalse() {
        String deviceId = "deviceId";

        when(contextService.getDevice(anyString()))
                .thenReturn(Uni.createFrom().failure(new RuntimeException("Failure")));

        Boolean result = policyRuleConditionValidator.isDeviceIdValid(deviceId).await().indefinitely();

        assertThat(result).isEqualTo(false);
    }

    Device createDevice(String deviceId) {

        final var configRuleCustom = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var configRuleType = new ConfigRuleTypeCustom(configRuleCustom);
        final var deviceConfig =
                new DeviceConfig(List.of(new ConfigRule(ConfigActionEnum.SET, configRuleType)));

        final var deviceDrivers = List.of(DeviceDriverEnum.IETF_NETWORK_TOPOLOGY, DeviceDriverEnum.P4);

        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";
        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var endPointType = "endPointType";
        final var kpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegion = new LocationTypeRegion("ATH");
        final var location = new Location(locationTypeRegion);
        final var endPoint =
                new EndPointBuilder(endPointId, endPointType, kpiSampleTypes).location(location).build();

        final var endPoints = List.of(endPoint);

        return new Device(
                deviceId,
                "deviceType",
                deviceConfig,
                DeviceOperationalStatus.ENABLED,
                deviceDrivers,
                endPoints);
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

    private PolicyRuleBasic createPolicyRuleBasic(
            String policyRuleId,
            String kpiId,
            PolicyRuleState policyRuleState,
            int priority,
            List<PolicyRuleAction> policyRuleActions) {

        return new PolicyRuleBasic(policyRuleId, kpiId, policyRuleState, priority, policyRuleActions);
    }

    private ServiceId createServiceId(String contextId, String id) {
        return new ServiceId(contextId, id);
    }

    private List<String> createDeviceIds() {
        return List.of("deviceIdA", "deviceIdB");
    }

    private PolicyRuleService createPolicyRuleService(
            PolicyRuleBasic policyRuleBasic, ServiceId serviceId, List<String> deviceIds) {

        return new PolicyRuleService(policyRuleBasic, serviceId, deviceIds);
    }

    //     @Test
    //     void shouldThrowNullPointerExceptionGivenNullPolicyRuleBasic() {
    //         final var serviceId = createServiceId("CONTEXT_ID", "id");
    //         final var deviceIds = createDeviceIds();

    //         assertThatExceptionOfType(NullPointerException.class)
    //                 .isThrownBy(() -> createPolicyRuleService(null, serviceId, deviceIds));
    //     }

    //     @Test
    //     void shouldThrowNullPointerExceptionGivenNullServiceId() {
    //         final var policyRuleConditions =
    //                 createPolicyRuleConditions(
    //                         UUID.randomUUID().toString(),
    //                         NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL,
    //                         new IntegerKpiValue(3));
    //         final var policyRuleActions =
    //                 createPolicyRuleActions(
    //                         PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT,
    //                         List.of(UUID.randomUUID().toString(), UUID.randomUUID().toString()));

    //         final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE,
    // "1");

    //         final var deviceIds = createDeviceIds();

    //         final var policyRuleBasic =
    //                 createPolicyRuleBasic(
    //                         "policyRuleId1",
    //                         3,
    //                         policyRuleState,
    //                         BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_OR,
    //                         policyRuleConditions,
    //                         policyRuleActions);

    //         assertThatExceptionOfType(NullPointerException.class)
    //                 .isThrownBy(() -> createPolicyRuleService(policyRuleBasic, null, deviceIds));
    //     }

    //     @Test
    //     void shouldThrowNullPointerExceptionGivenNullDeviceIds() {
    //         final var serviceId = createServiceId("contextId", "ID");

    //         final var policyRuleConditions =
    //                 createPolicyRuleConditions(
    //                         UUID.randomUUID().toString(),
    //                         NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN,
    //                         new IntegerKpiValue(3));
    //         final var policyRuleActions =
    //                 createPolicyRuleActions(
    //                         PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE,
    //                         List.of(UUID.randomUUID().toString(), UUID.randomUUID().toString()));

    //         final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE,
    // "1");

    //         final var policyRuleBasic =
    //                 createPolicyRuleBasic(
    //                         "policyRuleId2",
    //                         2,
    //                         policyRuleState,
    //                         BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_AND,
    //                         policyRuleConditions,
    //                         policyRuleActions);

    //         assertThatExceptionOfType(NullPointerException.class)
    //                 .isThrownBy(() -> createPolicyRuleService(policyRuleBasic, serviceId, null));
    //     }

    @Test
    void shouldCreatePolicyRuleServiceObjectGivenEmptyDeviceIds() {
        final var serviceId = createServiceId("contextId", "id");
        final var deviceIds = Collections.<String>emptyList();

        final var policyRuleConditions =
                createPolicyRuleConditions(
                        UUID.randomUUID().toString(),
                        NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN,
                        new IntegerKpiValue(3));
        final var policyRuleActions =
                createPolicyRuleActions(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_SET_DEVICE_STATUS,
                        List.of(
                                new PolicyRuleActionConfig(
                                        UUID.randomUUID().toString(), UUID.randomUUID().toString())));

        final var policyRuleState = new PolicyRuleState(PolicyRuleStateEnum.POLICY_EFFECTIVE, "1");

        final var policyRuleBasic =
                createPolicyRuleBasic("policyRuleId", "kpiId", policyRuleState, 0, policyRuleActions);

        final var expectedPolicyRuleService =
                new PolicyRuleService(policyRuleBasic, serviceId, deviceIds);

        final var policyRuleService = createPolicyRuleService(policyRuleBasic, serviceId, deviceIds);

        assertThat(policyRuleService).usingRecursiveComparison().isEqualTo(expectedPolicyRuleService);
    }

    @Test
    void shouldCreatePolicyRuleServiceObject() {
        final var serviceId = createServiceId("contextId", "id");
        final var deviceIds = List.of("deviceIdA", "deviceIdB");

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

        final var policyRuleBasic =
                createPolicyRuleBasic("policyRuleId", "kpiId", policyRuleState, 0, policyRuleActions);

        final var expectedPolicyRuleService =
                new PolicyRuleService(policyRuleBasic, serviceId, deviceIds);

        final var policyRuleService = createPolicyRuleService(policyRuleBasic, serviceId, deviceIds);

        assertThat(policyRuleService).usingRecursiveComparison().isEqualTo(expectedPolicyRuleService);
    }
}
