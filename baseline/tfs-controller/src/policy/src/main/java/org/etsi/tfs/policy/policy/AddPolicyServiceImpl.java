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

import static org.etsi.tfs.policy.common.ApplicationProperties.INVALID_MESSAGE;
import static org.etsi.tfs.policy.common.ApplicationProperties.VALIDATED_POLICYRULE_STATE;

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.policy.context.ContextService;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.exception.ExternalServiceFailureException;
import org.etsi.tfs.policy.policy.model.PolicyRule;
import org.etsi.tfs.policy.policy.model.PolicyRuleService;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleTypeService;
import org.jboss.logging.Logger;

@ApplicationScoped
public class AddPolicyServiceImpl {

    @Inject private CommonPolicyServiceImpl commonPolicyService;
    @Inject private ContextService contextService;

    private static final Logger LOGGER = Logger.getLogger(AddPolicyServiceImpl.class);

    public Uni<PolicyRuleState> constructPolicyStateBasedOnCriteria(
            Boolean isService, ServiceId serviceId, PolicyRuleService policyRuleService) {

        if (!isService) {
            var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, String.format(INVALID_MESSAGE, serviceId));

            return Uni.createFrom().item(policyRuleState);
        }
        final var policyRuleTypeService = new PolicyRuleTypeService(policyRuleService);
        final var policyRule = new PolicyRule(policyRuleTypeService);

        final String kpiId = policyRuleService.getPolicyRuleBasic().getKpiId();
        commonPolicyService.getKpiPolicyRuleServiceMap().put(kpiId, policyRuleService);

        return setPolicyRuleOnContextAndReturnState(policyRule);
    }

    private Uni<PolicyRuleState> setPolicyRuleOnContextAndReturnState(PolicyRule policyRule) {
        return contextService
                .setPolicyRule(policyRule)
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transform(policyId -> VALIDATED_POLICYRULE_STATE);
    }
}
