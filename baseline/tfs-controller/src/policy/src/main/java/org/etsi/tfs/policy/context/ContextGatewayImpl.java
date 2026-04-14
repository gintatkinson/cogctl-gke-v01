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

package org.etsi.tfs.policy.context;

import context.MutinyContextServiceGrpc.MutinyContextServiceStub;
import context_policy.MutinyContextPolicyServiceGrpc.MutinyContextPolicyServiceStub;
import io.quarkus.grpc.GrpcClient;
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.policy.Serializer;
import org.etsi.tfs.policy.context.model.Device;
import org.etsi.tfs.policy.context.model.Empty;
import org.etsi.tfs.policy.context.model.Service;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.policy.model.PolicyRule;

@ApplicationScoped
public class ContextGatewayImpl implements ContextGateway {

    @GrpcClient("context")
    MutinyContextServiceStub streamingDelegateContext;

    // TODO remove client when RPCs declared in context_policy.proto are moved in context.proto
    //  and use streamingDelegateContext for all methods
    @GrpcClient("context_policy")
    MutinyContextPolicyServiceStub streamingDelegateContextPolicy;

    private final Serializer serializer;

    @Inject
    public ContextGatewayImpl(Serializer serializer) {
        this.serializer = serializer;
    }

    @Override
    public Uni<Service> getService(ServiceId serviceId) {

        final var serializedServiceId = serializer.serialize(serviceId);

        return streamingDelegateContext
                .getService(serializedServiceId)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<ServiceId> setService(Service service) {
        final var serializedService = serializer.serialize(service);

        return streamingDelegateContext
                .setService(serializedService)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<Device> getDevice(String deviceId) {
        final var serializedDeviceId = serializer.serializeDeviceId(deviceId);

        return streamingDelegateContext
                .getDevice(serializedDeviceId)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<PolicyRule> getPolicyRule(String policyRuleId) {
        final var serializedPolicyRuleId = serializer.serializePolicyRuleId(policyRuleId);

        return streamingDelegateContextPolicy
                .getPolicyRule(serializedPolicyRuleId)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<String> setPolicyRule(PolicyRule policyRule) {
        // return Uni.createFrom().item("571eabc1-0f59-48da-b608-c45876c3fa8a");
        final var serializedPolicyRuleBasic = serializer.serialize(policyRule);

        return streamingDelegateContextPolicy
                .setPolicyRule(serializedPolicyRuleBasic)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<Empty> removePolicyRule(String policyRuleId) {
        final var serializedPolicyRuleId = serializer.serializePolicyRuleId(policyRuleId);

        return streamingDelegateContextPolicy
                .removePolicyRule(serializedPolicyRuleId)
                .onItem()
                .transform(serializer::deserializeEmpty);
    }
}
