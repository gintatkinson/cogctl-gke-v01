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

import context.ContextOuterClass;
import context.ContextOuterClass.Uuid;
import io.quarkus.grpc.GrpcClient;
import io.quarkus.test.junit.QuarkusTest;
import jakarta.inject.Inject;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import monitoring.Monitoring.KpiId;
import org.etsi.tfs.policy.monitoring.model.FloatKpiValue;
import org.etsi.tfs.policy.monitoring.model.IntegerKpiValue;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionConfig;
import org.jboss.logging.Logger;
import org.junit.jupiter.api.Test;
import policy.Policy;
import policy.Policy.PolicyRuleBasic;
import policy.Policy.PolicyRuleStateEnum;
import policy.PolicyAction;
import policy.PolicyAction.PolicyRuleActionEnum;
import policy.PolicyCondition;
import policy.PolicyCondition.NumericalOperator;
import policy.PolicyCondition.PolicyRuleCondition;
import policy.PolicyService;

@QuarkusTest
class PolicyGrpcServiceTest {
    private static final Logger LOGGER = Logger.getLogger(PolicyGrpcServiceTest.class);

    @GrpcClient PolicyService client;
    private final Serializer serializer;

    @Inject
    PolicyGrpcServiceTest(Serializer serializer) {
        this.serializer = serializer;
    }

    private context.ContextOuterClass.ServiceId createContextServiceId() {
        final var contextIdUuid = serializer.serializeUuid("571eabc1-0f59-48da-b608-c45876c3fa8a");

        final var serviceIdUuid = serializer.serializeUuid("123456789");

        context.ContextOuterClass.ContextId contextId =
                context.ContextOuterClass.ContextId.newBuilder().setContextUuid(contextIdUuid).build();

        return context.ContextOuterClass.ServiceId.newBuilder()
                .setContextId(contextId)
                .setServiceUuid(serviceIdUuid)
                .build();
    }

    private PolicyRuleBasic createPolicyRuleBasic() {
        final var expectedPolicyRuleIdUuid =
                serializer.serializeUuid("571eabc1-0f59-48da-b608-c45876c3fa8a");

        final var expectedPolicyRuleId =
                Policy.PolicyRuleId.newBuilder().setUuid(expectedPolicyRuleIdUuid).build();

        final var expectedPolicyRuleState =
                Policy.PolicyRuleState.newBuilder()
                        .setPolicyRuleState(PolicyRuleStateEnum.POLICY_INSERTED)
                        .build();

        final var expectedFirstKpiValue = new IntegerKpiValue(22);
        final var expectedSecondKpiValue = new FloatKpiValue(69.1f);

        final var serializedExpectedFirstKpiValue = serializer.serialize(expectedFirstKpiValue);
        final var serializedExpectedSecondKpiValue = serializer.serialize(expectedSecondKpiValue);

        final var firstExpectedPolicyRuleCondition =
                PolicyRuleCondition.newBuilder()
                        .setKpiId(
                                KpiId.newBuilder()
                                        .setKpiId(
                                                Uuid.newBuilder().setUuid("79e49ba3-a7b4-4b4b-8aaa-28b05c6f888e").build()))
                        .setNumericalOperator(NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_EQUAL)
                        .setKpiValue(serializedExpectedFirstKpiValue)
                        .build();

        final var secondExpectedPolicyRuleCondition =
                PolicyCondition.PolicyRuleCondition.newBuilder()
                        .setKpiId(
                                KpiId.newBuilder()
                                        .setKpiId(
                                                Uuid.newBuilder().setUuid("eae900e5-2703-467d-82f2-97aae8b55c15").build()))
                        .setNumericalOperator(NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_GREATER_THAN)
                        .setKpiValue(serializedExpectedSecondKpiValue)
                        .build();

        final var expectedPolicyRuleConditions =
                List.of(firstExpectedPolicyRuleCondition, secondExpectedPolicyRuleCondition);

        PolicyRuleActionConfig policyRuleActionConfig_1 =
                new PolicyRuleActionConfig("paramater1", "parameter2");
        final var serializedPolicyRuleActionConfigList_1 =
                serializer.serialize(policyRuleActionConfig_1);

        PolicyRuleActionConfig policyRuleActionConfig_2 =
                new PolicyRuleActionConfig("paramater3", "parameter4");
        final var serializedPolicyRuleActionConfigList_2 =
                serializer.serialize(policyRuleActionConfig_2);

        final var firstExpectedPolicyRuleAction =
                PolicyAction.PolicyRuleAction.newBuilder()
                        .setAction(PolicyAction.PolicyRuleActionEnum.POLICYRULE_ACTION_ADD_SERVICE_CONFIGRULE)
                        .addActionConfig(serializedPolicyRuleActionConfigList_1)
                        .build();

        final var secondExpectedPolicyRuleAction =
                PolicyAction.PolicyRuleAction.newBuilder()
                        .setAction(PolicyRuleActionEnum.POLICYRULE_ACTION_ADD_SERVICE_CONSTRAINT)
                        .addActionConfig(serializedPolicyRuleActionConfigList_2)
                        .build();

        final var expectedPolicyRuleActions =
                List.of(firstExpectedPolicyRuleAction, secondExpectedPolicyRuleAction);

        return PolicyRuleBasic.newBuilder()
                .setPolicyRuleId(expectedPolicyRuleId)
                .setPolicyRuleState(expectedPolicyRuleState)
                .addAllActionList(expectedPolicyRuleActions)
                .build();
    }

    // @Test
    // void shouldAddPolicyService() throws ExecutionException, InterruptedException, TimeoutException
    // {
    //    CompletableFuture<String> message = new CompletableFuture<>();

    //    final var policyRuleBasic = createPolicyRuleBasic();

    //    final var expectedPolicyRuleState = policyRuleBasic.getPolicyRuleState();

    //    final var serviceId = createContextServiceId();

    //    final var expectedDeviceIdUuid1 =
    //            serializer.serializeUuid("20db867c-772d-4872-9179-244ecafb3257");

    //    final var expectedDeviceId1 =
    //
    // ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(expectedDeviceIdUuid1).build();

    //    final var deviceIds = List.of(expectedDeviceId1);
    //    final var policyRuleService =
    //            Policy.PolicyRuleService.newBuilder()
    //                    .setPolicyRuleBasic(policyRuleBasic)
    //                    .setServiceId(serviceId)
    //                    .addAllDeviceList(deviceIds)
    //                    .build();

    //    client
    //            .policyAddService(policyRuleService)
    //            .subscribe()
    //            .with(policyRuleState ->
    // message.complete(policyRuleState.getPolicyRuleState().toString()));

    //    assertThat(message.get(5, TimeUnit.SECONDS))
    //            .isEqualTo(expectedPolicyRuleState.getPolicyRuleState().toString());
    // }

    // @Test
    // void shouldAddPolicyDevice() throws ExecutionException, InterruptedException, TimeoutException
    // {
    //    CompletableFuture<String> message = new CompletableFuture<>();

    //    final var expectedDeviceIdUuid1 =
    //            serializer.serializeUuid("20db867c-772d-4872-9179-244ecafb3257");
    //    final var expectedDeviceIdUuid2 =
    //            serializer.serializeUuid("095974ac-d757-412d-b317-bcf355220aa9");

    //    final var expectedDeviceId1 =
    //
    // ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(expectedDeviceIdUuid1).build();
    //    final var expectedDeviceId2 =
    //
    // ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(expectedDeviceIdUuid2).build();

    //    final var policyRuleBasic = createPolicyRuleBasic();
    //    final var deviceIds = List.of(expectedDeviceId1, expectedDeviceId2);

    //    final var expectedPolicyRuleState = policyRuleBasic.getPolicyRuleState();

    //    final var policyRuleDevice =
    //            Policy.PolicyRuleDevice.newBuilder()
    //                    .setPolicyRuleBasic(policyRuleBasic)
    //                    .addAllDeviceList(deviceIds)
    //                    .build();

    //    client
    //            .policyAddDevice(policyRuleDevice)
    //            .subscribe()
    //            .with(policyRuleState ->
    // message.complete(policyRuleState.getPolicyRuleState().toString()));

    //    assertThat(message.get(5, TimeUnit.SECONDS))
    //            .isEqualTo(expectedPolicyRuleState.getPolicyRuleState().toString());
    // }

    @Test
    void shouldUpdatePolicyServiceReturnFailedState()
            throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();

        final var expectedPolicyRuleState =
                Policy.PolicyRuleState.newBuilder()
                        .setPolicyRuleState(PolicyRuleStateEnum.POLICY_FAILED)
                        .build();

        final var policyRuleBasic =
                PolicyRuleBasic.newBuilder().setPolicyRuleState(expectedPolicyRuleState).build();
        final var policyRuleService =
                Policy.PolicyRuleService.newBuilder().setPolicyRuleBasic(policyRuleBasic).build();

        client
                .policyUpdateService(policyRuleService)
                .subscribe()
                .with(policyRuleState -> message.complete(policyRuleState.getPolicyRuleState().toString()));

        assertThat(message.get(5, TimeUnit.SECONDS))
                .isEqualTo(expectedPolicyRuleState.getPolicyRuleState().toString());
    }

    @Test
    void shouldUpdatePolicyDeviceReturnFailedState()
            throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();

        final var expectedDeviceIdUuid =
                serializer.serializeUuid("20db867c-772d-4872-9179-244ecafb3257");

        final var expectedDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(expectedDeviceIdUuid).build();

        final var expectedPolicyRuleState =
                Policy.PolicyRuleState.newBuilder()
                        .setPolicyRuleState(PolicyRuleStateEnum.POLICY_FAILED)
                        .build();

        final var policyRuleBasic =
                PolicyRuleBasic.newBuilder().setPolicyRuleState(expectedPolicyRuleState).build();
        final var deviceIds = List.of(expectedDeviceId);
        final var policyRuleDevice =
                Policy.PolicyRuleDevice.newBuilder()
                        .setPolicyRuleBasic(policyRuleBasic)
                        .addAllDeviceList(deviceIds)
                        .build();

        client
                .policyUpdateDevice(policyRuleDevice)
                .subscribe()
                .with(policyRuleState -> message.complete(policyRuleState.getPolicyRuleState().toString()));

        assertThat(message.get(5, TimeUnit.SECONDS))
                .isEqualTo(expectedPolicyRuleState.getPolicyRuleState().toString());
    }

    // TODO: Disable shouldDeletePolicy test until mock context service
    //     @Test
    //     void shouldDeletePolicy() throws ExecutionException, InterruptedException, TimeoutException
    // {
    //         CompletableFuture<String> message = new CompletableFuture<>();

    //         final var uuid =
    //                 ContextOuterClass.Uuid.newBuilder()
    //
    // .setUuid(UUID.fromString("0f14d0ab-9608-7862-a9e4-5ed26688389b").toString())
    //                         .build();
    //         final var policyRuleId = Policy.PolicyRuleId.newBuilder().setUuid(uuid).build();

    //         final var expectedPolicyRuleState =
    //                 Policy.PolicyRuleState.newBuilder()
    //                         .setPolicyRuleState(PolicyRuleStateEnum.POLICY_REMOVED)
    //                         .build();

    //         client
    //                 .policyDelete(policyRuleId)
    //                 .subscribe()
    //                 .with(policyRuleState ->
    // message.complete(policyRuleState.getPolicyRuleState().toString()));

    //         assertThat(message.get(5, TimeUnit.SECONDS))
    //                 .isEqualTo(expectedPolicyRuleState.getPolicyRuleState().toString());
    //     }

    @Test
    void shouldGetPolicyService() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();

        final var uuid =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("0f14d0ab-9608-7862-a9e4-5ed26688389b").toString())
                        .build();
        final var policyRuleId = Policy.PolicyRuleId.newBuilder().setUuid(uuid).build();

        client
                .getPolicyService(policyRuleId)
                .subscribe()
                .with(
                        policyRuleService -> {
                            LOGGER.infof(
                                    "Getting policy with ID: %s",
                                    policyRuleService.getPolicyRuleBasic().getPolicyRuleId().getUuid());
                            message.complete(
                                    policyRuleService.getPolicyRuleBasic().getPolicyRuleId().getUuid().getUuid());
                        });

        assertThat(message.get(5, TimeUnit.SECONDS)).isEqualTo(policyRuleId.getUuid().getUuid());
    }

    @Test
    void shouldGetPolicyDevice() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();

        final var uuid =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("0f14d0ab-9608-7862-a9e4-5ed26688389b").toString())
                        .build();
        final var policyRuleId = Policy.PolicyRuleId.newBuilder().setUuid(uuid).build();

        client
                .getPolicyDevice(policyRuleId)
                .subscribe()
                .with(
                        policyRuleService -> {
                            LOGGER.infof(
                                    "Getting policy with ID: %s",
                                    policyRuleService.getPolicyRuleBasic().getPolicyRuleId().getUuid());
                            message.complete(
                                    policyRuleService.getPolicyRuleBasic().getPolicyRuleId().getUuid().getUuid());
                        });

        assertThat(message.get(5, TimeUnit.SECONDS)).isEqualTo(policyRuleId.getUuid().getUuid());
    }

    @Test
    void shouldGetPolicyByServiceId()
            throws ExecutionException, InterruptedException, TimeoutException {

        CompletableFuture<String> message = new CompletableFuture<>();

        final var uuid =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("0f14d0ab-9608-7862-a9e4-5ed26688389b").toString())
                        .build();
        final var serviceId = ContextOuterClass.ServiceId.newBuilder().setServiceUuid(uuid).build();

        client
                .getPolicyByServiceId(serviceId)
                .subscribe()
                .with(
                        policyRuleList -> {
                            LOGGER.infof("Getting policyRuleList with ID: %s", policyRuleList);
                            message.complete(policyRuleList.toString());
                        });

        assertThat(message.get(5, TimeUnit.SECONDS)).isEmpty();
    }
}
