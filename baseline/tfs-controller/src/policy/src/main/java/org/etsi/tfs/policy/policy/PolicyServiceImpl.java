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

import static org.etsi.tfs.policy.common.ApplicationProperties.*;

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import java.util.function.Function;
import org.etsi.tfs.policy.context.ContextService;
import org.etsi.tfs.policy.exception.ExternalServiceFailureException;
import org.etsi.tfs.policy.policy.model.PolicyRule;
import org.etsi.tfs.policy.policy.model.PolicyRuleDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleService;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.etsi.tfs.policy.policy.service.PolicyRuleConditionValidator;
import org.jboss.logging.Logger;

@ApplicationScoped
public class PolicyServiceImpl implements PolicyService {

    private static final Logger LOGGER = Logger.getLogger(PolicyServiceImpl.class);

    private final ContextService contextService;
    private final PolicyRuleConditionValidator policyRuleConditionValidator;
    private final CommonPolicyServiceImpl commonPolicyServiceImpl;
    private final AddPolicyServiceImpl addPolicyServiceImpl;
    private final AddPolicyDeviceImpl addPolicyDeviceImpl;

    @Inject
    public PolicyServiceImpl(
            ContextService contextService,
            PolicyRuleConditionValidator policyRuleConditionValidator,
            CommonPolicyServiceImpl commonPolicyServiceImpl,
            AddPolicyServiceImpl addPolicyServiceImpl,
            AddPolicyDeviceImpl addPolicyDeviceImpl) {
        this.contextService = contextService;
        this.policyRuleConditionValidator = policyRuleConditionValidator;
        this.commonPolicyServiceImpl = commonPolicyServiceImpl;
        this.addPolicyServiceImpl = addPolicyServiceImpl;
        this.addPolicyDeviceImpl = addPolicyDeviceImpl;
    }

    @Override
    public Uni<PolicyRuleState> addPolicyService(PolicyRuleService policyRuleService) {
        LOGGER.infof("Received %s", policyRuleService);

        if (!policyRuleService.areArgumentsValid()) {
            LOGGER.error(policyRuleService.getExceptionMessage());
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleService.getExceptionMessage());

            return Uni.createFrom().item(policyRuleState);
        }

        final var policyRuleBasic = policyRuleService.getPolicyRuleBasic();
        if (!policyRuleBasic.areArgumentsValid()) {
            LOGGER.error(policyRuleService.getExceptionMessage());
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleBasic.getExceptionMessage());
            return Uni.createFrom().item(policyRuleState);
        }

        final var serviceId = policyRuleService.getServiceId();
        final var deviceIds = policyRuleService.getDeviceIds();
        final var isServiceValid = policyRuleConditionValidator.isServiceIdValid(serviceId, deviceIds);

        return isServiceValid
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transform(
                        isService ->
                                addPolicyServiceImpl.constructPolicyStateBasedOnCriteria(
                                        isService, serviceId, policyRuleService))
                .flatMap(Function.identity());
    }

    @Override
    public Uni<PolicyRuleState> addPolicyDevice(PolicyRuleDevice policyRuleDevice) {
        LOGGER.infof("Received %s", policyRuleDevice);

        if (!policyRuleDevice.areArgumentsValid()) {
            LOGGER.error(policyRuleDevice.getExceptionMessage());
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleDevice.getExceptionMessage());

            return Uni.createFrom().item(policyRuleState);
        }

        final var policyRuleBasic = policyRuleDevice.getPolicyRuleBasic();
        if (!policyRuleBasic.areArgumentsValid()) {
            LOGGER.error(policyRuleDevice.getExceptionMessage());
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleBasic.getExceptionMessage());
            return Uni.createFrom().item(policyRuleState);
        }

        final var deviceIds = policyRuleDevice.getDeviceIds();
        final var areDevicesValid = addPolicyDeviceImpl.returnInvalidDeviceIds(deviceIds);

        return areDevicesValid
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transform(
                        areDevices ->
                                addPolicyDeviceImpl.areDeviceOnContext(
                                        areDevices, policyRuleDevice, policyRuleBasic))
                .flatMap(Function.identity());
    }

    @Override
    public Uni<PolicyRuleState> updatePolicyService(PolicyRuleService policyRuleService) {
        LOGGER.infof("Received %s", policyRuleService);

        if (!policyRuleService.areArgumentsValid()) {
            LOGGER.error(policyRuleService.getExceptionMessage());
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleService.getExceptionMessage());

            return Uni.createFrom().item(policyRuleState);
        }

        final var policyRuleBasic = policyRuleService.getPolicyRuleBasic();
        if (!policyRuleBasic.areArgumentsValid()) {
            LOGGER.error(policyRuleService.getExceptionMessage());
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleBasic.getExceptionMessage());
            return Uni.createFrom().item(policyRuleState);
        }

        final var serviceId = policyRuleService.getServiceId();
        final var policyRuleId = policyRuleBasic.getPolicyRuleId();
        final var isPolicyRuleServiceValid =
                policyRuleConditionValidator.isPolicyRuleServiceValid(policyRuleId, serviceId);

        return isPolicyRuleServiceValid
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transform(
                        isPolicyRuleService -> {
                            if (!isPolicyRuleService) {
                                return new PolicyRuleState(
                                        PolicyRuleStateEnum.POLICY_FAILED, String.format(INVALID_MESSAGE, serviceId));
                            }

                            return VALIDATED_POLICYRULE_STATE;
                        });
    }

    @Override
    public Uni<PolicyRuleState> updatePolicyDevice(PolicyRuleDevice policyRuleDevice) {
        LOGGER.infof("Received %s", policyRuleDevice);

        if (!policyRuleDevice.areArgumentsValid()) {
            LOGGER.error(policyRuleDevice.getExceptionMessage());
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleDevice.getExceptionMessage());

            return Uni.createFrom().item(policyRuleState);
        }

        final var policyRuleBasic = policyRuleDevice.getPolicyRuleBasic();
        if (!policyRuleBasic.areArgumentsValid()) {
            final var policyRuleState =
                    new PolicyRuleState(
                            PolicyRuleStateEnum.POLICY_FAILED, policyRuleBasic.getExceptionMessage());
            return Uni.createFrom().item(policyRuleState);
        }

        final var policyRuleId = policyRuleBasic.getPolicyRuleId();
        final var isPolicyRuleValid =
                policyRuleConditionValidator.isUpdatedPolicyRuleIdValid(policyRuleId);

        return isPolicyRuleValid
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .onItem()
                .transform(
                        isPolicyRuleService -> {
                            if (!isPolicyRuleService) {
                                return new PolicyRuleState(
                                        PolicyRuleStateEnum.POLICY_FAILED,
                                        String.format(INVALID_MESSAGE, policyRuleId));
                            }

                            return VALIDATED_POLICYRULE_STATE;
                        });
    }

    @Override
    public Uni<PolicyRuleState> deletePolicy(String policyRuleId) {
        LOGGER.infof("Received %s", policyRuleId);

        final var getPolicyRule = contextService.getPolicyRule(policyRuleId);

        return getPolicyRule.onItem().transform(policyRule -> removePolicyFromContext(policyRule));
    }

    private PolicyRuleState removePolicyFromContext(PolicyRule policyRule) {
        var policyRuleBasic = policyRule.getPolicyRuleType().getPolicyRuleBasic();
        String policyId = policyRuleBasic.getPolicyRuleId();

        policyRule
                .getPolicyRuleType()
                .getPolicyRuleBasic()
                .setPolicyRuleState(REMOVED_POLICYRULE_STATE);

        contextService
                .setPolicyRule(policyRule)
                .onFailure()
                .transform(failure -> new ExternalServiceFailureException(failure.getMessage()))
                .subscribe()
                .with(
                        tmp ->
                                LOGGER.infof(
                                        "DeletePolicy with id: " + VALID_MESSAGE, policyRuleBasic.getPolicyRuleId()));

        contextService.removePolicyRule(policyId).subscribe().with(x -> {});

        // TODO: When the Map doesn't contains the policyId we should throw an exception?
        if (commonPolicyServiceImpl.getSubscriptionList().contains(policyId))
            commonPolicyServiceImpl.getSubscriptionList().get(policyId).cancel();

        return policyRuleBasic.getPolicyRuleState();
    }
}
