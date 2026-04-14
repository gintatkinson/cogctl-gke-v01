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
import static org.etsi.tfs.policy.common.ApplicationProperties.INVALID_MESSAGE;
import static org.etsi.tfs.policy.common.ApplicationProperties.VALIDATED_POLICYRULE_STATE;

import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.junit.mockito.InjectMock;
import io.smallrye.mutiny.Uni;
import jakarta.inject.Inject;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import org.etsi.tfs.policy.context.ContextService;
import org.etsi.tfs.policy.context.model.Service;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.context.model.ServiceTypeEnum;
import org.etsi.tfs.policy.monitoring.MonitoringService;
import org.etsi.tfs.policy.monitoring.model.IntegerKpiValue;
import org.etsi.tfs.policy.monitoring.model.KpiValue;
import org.etsi.tfs.policy.policy.PolicyServiceImpl;
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
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

@QuarkusTest
class PolicyUpdateServiceTest {

    @Inject PolicyServiceImpl policyService;

    @InjectMock PolicyRuleConditionValidator policyRuleConditionValidator;

    @InjectMock ContextService contextService;

    @InjectMock MonitoringService monitoringService;

    static PolicyRuleBasic policyRuleBasic;
    static PolicyRuleService policyRuleService;

    @BeforeAll
    static void init() {

        String policyId = "policyRuleId";
        KpiValue kpiValue = new IntegerKpiValue(100);

        PolicyRuleCondition policyRuleCondition =
                new PolicyRuleCondition(
                        "kpiId", NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN, kpiValue);

        PolicyRuleActionConfig policyRuleActionConfig = new PolicyRuleActionConfig("key", "value");

        PolicyRuleAction policyRuleAction =
                new PolicyRuleAction(
                        PolicyRuleActionEnum.POLICY_RULE_ACTION_NO_ACTION,
                        Arrays.asList(policyRuleActionConfig));

        policyRuleBasic =
                new PolicyRuleBasic(
                        policyId,
                        "kpiId",
                        new PolicyRuleState(PolicyRuleStateEnum.POLICY_INSERTED, "Failed due to some errors"),
                        1,
                        Arrays.asList(policyRuleAction));

        ServiceId serviceId = new ServiceId("contextId", "serviceId");

        Service service = new Service(serviceId, ServiceTypeEnum.UNKNOWN, null, null, null, null, 0.0);

        List<String> deviceIds = Arrays.asList("device1", "device2");

        policyRuleService = new PolicyRuleService(policyRuleBasic, serviceId, deviceIds);
    }

    @Test
    void contextOrServiceIdMustNotBeEmpty()
            throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<PolicyRuleState> message = new CompletableFuture<>();

        ServiceId serviceId = new ServiceId("", "");
        List<String> deviceIds = Arrays.asList("device1", "device2");

        PolicyRuleService policyRuleService =
                new PolicyRuleService(policyRuleBasic, serviceId, deviceIds);

        PolicyRuleState expectedResult =
                new PolicyRuleState(
                        PolicyRuleStateEnum.POLICY_FAILED, "Context Id of Service Id must not be empty.");

        policyService
                .updatePolicyService(policyRuleService)
                .subscribe()
                .with(
                        item -> {
                            message.complete(item);
                        });

        assertThat(message.get(5, TimeUnit.SECONDS).getPolicyRuleStateMessage())
                .isEqualTo(expectedResult.getPolicyRuleStateMessage().toString());
    }

    @Test
    void serviceIdMustNotBeEmpty() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<PolicyRuleState> message = new CompletableFuture<>();

        ServiceId serviceId = new ServiceId("sdf", "");
        List<String> deviceIds = Arrays.asList("device1", "device2");

        PolicyRuleService policyRuleService =
                new PolicyRuleService(policyRuleBasic, serviceId, deviceIds);

        PolicyRuleState expectedResult =
                new PolicyRuleState(PolicyRuleStateEnum.POLICY_FAILED, "Service Id must not be empty.");

        policyService
                .updatePolicyService(policyRuleService)
                .subscribe()
                .with(item -> message.complete(item));

        assertThat(message.get(5, TimeUnit.SECONDS).getPolicyRuleStateMessage())
                .isEqualTo(expectedResult.getPolicyRuleStateMessage().toString());
    }

    @Test
    void checkMessageIfServiceIsNotValid()
            throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<PolicyRuleState> message = new CompletableFuture<>();

        ServiceId serviceId = new ServiceId("contextId", "serviceId");

        PolicyRuleService policyRuleService =
                new PolicyRuleService(policyRuleBasic, serviceId, new ArrayList<>());

        PolicyRuleState expectedResult =
                new PolicyRuleState(
                        PolicyRuleStateEnum.POLICY_FAILED, String.format(INVALID_MESSAGE, serviceId));

        Mockito.when(
                        policyRuleConditionValidator.isPolicyRuleServiceValid(
                                Mockito.anyString(), Mockito.any(ServiceId.class)))
                .thenReturn(Uni.createFrom().item(Boolean.FALSE));

        policyService
                .updatePolicyService(policyRuleService)
                .subscribe()
                .with(
                        item -> {
                            message.complete(item);
                        });

        assertThat(message.get(5, TimeUnit.SECONDS).getPolicyRuleStateMessage())
                .isEqualTo(expectedResult.getPolicyRuleStateMessage().toString());
    }

    @Test
    void successUpdatePolicyService()
            throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<PolicyRuleState> message = new CompletableFuture<>();

        ServiceId serviceId = new ServiceId("contextId", "serviceId");

        PolicyRuleService policyRuleService =
                new PolicyRuleService(policyRuleBasic, serviceId, new ArrayList<>());

        PolicyRuleState expectedResult =
                new PolicyRuleState(
                        PolicyRuleStateEnum.POLICY_VALIDATED,
                        VALIDATED_POLICYRULE_STATE.getPolicyRuleStateMessage());

        Mockito.when(
                        policyRuleConditionValidator.isPolicyRuleServiceValid(
                                Mockito.anyString(), Mockito.any(ServiceId.class)))
                .thenReturn(Uni.createFrom().item(Boolean.TRUE));

        policyService
                .updatePolicyService(policyRuleService)
                .subscribe()
                .with(
                        item -> {
                            message.complete(item);
                        });

        assertThat(message.get(5, TimeUnit.SECONDS).getPolicyRuleStateMessage())
                .isEqualTo(expectedResult.getPolicyRuleStateMessage().toString());
    }
}
