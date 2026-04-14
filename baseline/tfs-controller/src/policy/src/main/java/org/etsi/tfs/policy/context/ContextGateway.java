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
import org.etsi.tfs.policy.context.model.Device;
import org.etsi.tfs.policy.context.model.Empty;
import org.etsi.tfs.policy.context.model.Service;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.policy.model.PolicyRule;

public interface ContextGateway {

    // Context related methods
    Uni<Service> getService(ServiceId serviceId);

    Uni<ServiceId> setService(Service service);

    Uni<Device> getDevice(String deviceId);

    // Context-policy related methods
    Uni<PolicyRule> getPolicyRule(String policyRuleId);

    Uni<String> setPolicyRule(PolicyRule policyRule);

    Uni<Empty> removePolicyRule(String policyRuleId);
}
