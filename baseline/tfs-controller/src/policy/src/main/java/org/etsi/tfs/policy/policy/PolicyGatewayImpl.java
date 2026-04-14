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

package org.etsi.tfs.policy.policy;

import context.ContextOuterClass.ServiceId;
import io.quarkus.grpc.GrpcService;
import io.smallrye.mutiny.Uni;
import jakarta.inject.Inject;
import org.eclipse.microprofile.metrics.MetricUnits;
import org.eclipse.microprofile.metrics.annotation.Counted;
import org.eclipse.microprofile.metrics.annotation.Timed;
import org.etsi.tfs.policy.Serializer;
import policy.Policy;
import policy.Policy.PolicyRuleBasic;
import policy.Policy.PolicyRuleDevice;
import policy.Policy.PolicyRuleId;
import policy.Policy.PolicyRuleService;
import policy.Policy.PolicyRuleServiceList;
import policy.Policy.PolicyRuleState;

@GrpcService
public class PolicyGatewayImpl implements PolicyGateway {

    private final PolicyService policyService;
    private final Serializer serializer;

    @Inject
    public PolicyGatewayImpl(PolicyService policyService, Serializer serializer) {
        this.policyService = policyService;
        this.serializer = serializer;
    }

    @Override
    @Counted(name = "policy_policyAddService_counter")
    @Timed(name = "policy_policyAddService_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleState> policyAddService(PolicyRuleService request) {
        final var policyRuleService = serializer.deserialize(request);

        return policyService
                .addPolicyService(policyRuleService)
                .onItem()
                .transform(serializer::serialize);
    }

    @Override
    @Counted(name = "policy_policyUpdateService_counter")
    @Timed(name = "policy_policyUpdateService_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleState> policyUpdateService(PolicyRuleService request) {
        final var policyRuleService = serializer.deserialize(request);

        return policyService
                .updatePolicyService(policyRuleService)
                .onItem()
                .transform(serializer::serialize);
    }

    @Override
    @Counted(name = "policy_policyAddDevice_counter")
    @Timed(name = "policy_policyAddDevice_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleState> policyAddDevice(PolicyRuleDevice request) {
        final var policyRuleDevice = serializer.deserialize(request);

        return policyService
                .addPolicyDevice(policyRuleDevice)
                .onItem()
                .transform(serializer::serialize);
    }

    @Override
    @Counted(name = "policy_policyUpdateDevice_counter")
    @Timed(name = "policy_policyUpdateDevice_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleState> policyUpdateDevice(PolicyRuleDevice request) {
        final var policyRuleDevice = serializer.deserialize(request);

        return policyService
                .updatePolicyDevice(policyRuleDevice)
                .onItem()
                .transform(serializer::serialize);
    }

    @Override
    @Counted(name = "policy_policyDelete_counter")
    @Timed(name = "policy_policyDelete_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleState> policyDelete(PolicyRuleId request) {
        final var policyRuleId = serializer.deserialize(request);

        return policyService.deletePolicy(policyRuleId).onItem().transform(serializer::serialize);
    }

    @Override
    @Counted(name = "policy_getPolicyService_counter")
    @Timed(name = "policy_getPolicyService_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleService> getPolicyService(PolicyRuleId request) {
        final var policyRuleBasic = PolicyRuleBasic.newBuilder().setPolicyRuleId(request).build();

        return Uni.createFrom()
                .item(() -> PolicyRuleService.newBuilder().setPolicyRuleBasic(policyRuleBasic).build());
    }

    @Override
    @Counted(name = "policy_getPolicyDevice_counter")
    @Timed(name = "policy_getPolicyDevice_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleDevice> getPolicyDevice(PolicyRuleId request) {
        final var policyRuleBasic = PolicyRuleBasic.newBuilder().setPolicyRuleId(request).build();

        return Uni.createFrom()
                .item(() -> PolicyRuleDevice.newBuilder().setPolicyRuleBasic(policyRuleBasic).build());
    }

    @Override
    @Counted(name = "policy_getPolicyByServiceId_counter")
    @Timed(name = "policy_getPolicyByServiceId_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<PolicyRuleServiceList> getPolicyByServiceId(ServiceId request) {
        return Uni.createFrom().item(() -> Policy.PolicyRuleServiceList.newBuilder().build());
    }
}
