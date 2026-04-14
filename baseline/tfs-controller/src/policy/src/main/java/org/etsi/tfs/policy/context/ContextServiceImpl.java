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

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.policy.context.model.Device;
import org.etsi.tfs.policy.context.model.Empty;
import org.etsi.tfs.policy.context.model.Service;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.policy.model.PolicyRule;

@ApplicationScoped
public class ContextServiceImpl implements ContextService {

    private final ContextGateway contextGateway;

    @Inject
    public ContextServiceImpl(ContextGateway contextGateway) {
        this.contextGateway = contextGateway;
    }

    @Override
    public Uni<Service> getService(ServiceId serviceId) {
        return contextGateway.getService(serviceId);
    }

    @Override
    public Uni<ServiceId> setService(Service service) {
        return contextGateway.setService(service);
    }

    @Override
    public Uni<Device> getDevice(String deviceId) {
        return contextGateway.getDevice(deviceId);
    }

    @Override
    public Uni<PolicyRule> getPolicyRule(String policyRuleId) {
        return contextGateway.getPolicyRule(policyRuleId);
    }

    @Override
    public Uni<String> setPolicyRule(PolicyRule policyRule) {
        return contextGateway.setPolicyRule(policyRule);
    }

    @Override
    public Uni<Empty> removePolicyRule(String policyRuleId) {
        return contextGateway.removePolicyRule(policyRuleId);
    }
}
