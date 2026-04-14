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
import io.smallrye.mutiny.groups.UniJoin;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import java.util.List;
import org.etsi.tfs.policy.context.ContextService;
import org.etsi.tfs.policy.exception.ExternalServiceFailureException;
import org.etsi.tfs.policy.policy.model.PolicyRule;
import org.etsi.tfs.policy.policy.model.PolicyRuleBasic;
import org.etsi.tfs.policy.policy.model.PolicyRuleDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleTypeDevice;
import org.etsi.tfs.policy.policy.service.PolicyRuleConditionValidator;

@ApplicationScoped
public class AddPolicyDeviceImpl {

    @Inject private PolicyRuleConditionValidator policyRuleConditionValidator;

    @Inject private CommonPolicyServiceImpl commonPolicyServiceImpl;
    @Inject private CommonAlarmService commonAlarmService;

    @Inject private ContextService contextService;

    public Uni<List<Boolean>> returnInvalidDeviceIds(List<String> deviceIds) {
        UniJoin.Builder<Boolean> builder = Uni.join().builder();
        for (String deviceId : deviceIds) {
            final var validatedDeviceId = policyRuleConditionValidator.isDeviceIdValid(deviceId);
            builder.add(validatedDeviceId);
        }
        return builder.joinAll().andFailFast();
    }

    public Uni<PolicyRuleState> areDeviceOnContext(
            List<Boolean> areDevices,
            PolicyRuleDevice policyRuleDevice,
            PolicyRuleBasic policyRuleBasic) {
        if (areDevices.contains(false)) {
            var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED,
                            String.format(
                                    INVALID_MESSAGE, policyRuleDevice.getPolicyRuleBasic().getPolicyRuleId()));

            return Uni.createFrom().item(policyRuleState);
        }

        final var policyRuleTypeDevice = new PolicyRuleTypeDevice(policyRuleDevice);
        final var policyRule = new PolicyRule(policyRuleTypeDevice);

        return contextService
                .setPolicyRule(policyRule)
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transform(
                        policyId -> {
                            return VALIDATED_POLICYRULE_STATE;
                        });
    }
}
