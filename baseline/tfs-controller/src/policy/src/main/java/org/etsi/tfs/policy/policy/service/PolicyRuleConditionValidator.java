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

package org.etsi.tfs.policy.policy.service;

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import java.util.ArrayList;
import java.util.List;
import org.etsi.tfs.policy.context.ContextService;
import org.etsi.tfs.policy.context.model.Device;
import org.etsi.tfs.policy.context.model.EndPointId;
import org.etsi.tfs.policy.context.model.Service;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.policy.model.PolicyRuleService;
import org.jboss.logging.Logger;

@ApplicationScoped
public class PolicyRuleConditionValidator {

    private static final Logger LOGGER = Logger.getLogger(PolicyRuleConditionValidator.class);
    private static final String INVALID_MESSAGE = "%s is invalid.";
    private static final String VALID_MESSAGE = "%s is valid.";

    private final ContextService contextService;

    @Inject
    public PolicyRuleConditionValidator(ContextService contextService) {
        this.contextService = contextService;
    }

    public Uni<Boolean> isDeviceIdValid(String deviceId) {
        return contextService
                .getDevice(deviceId)
                .onFailure()
                .recoverWithItem((Device) null)
                .onItem()
                .transform(device -> checkIfDeviceIdExists(device, deviceId));
    }

    private boolean checkIfDeviceIdExists(Device device, String deviceId) {
        if (device == null) {
            return false;
        }

        final var deviceDeviceId = device.getDeviceId();
        return deviceDeviceId.equals(deviceId);
    }

    public Uni<Boolean> isServiceIdValid(ServiceId serviceId, List<String> deviceIds) {
        return contextService
                .getService(serviceId)
                .onFailure()
                .invoke(
                        throwable ->
                                LOGGER.error(
                                        "Failed to get service: " + serviceId + "Message " + throwable.getMessage(),
                                        throwable))
                //                .recoverWithItem((Service) null)
                .onItem()
                .transform(service -> checkIfServiceIsValid(service, serviceId, deviceIds));
    }

    private boolean checkIfServiceIsValid(
            Service service, ServiceId serviceId, List<String> deviceIds) {
        boolean checkIfServiceIdExists = checkIfServiceIdExists(service, serviceId);
        boolean checkIfServicesDeviceIdsExist = checkIfServicesDeviceIdsExist(service, deviceIds);
        return (checkIfServiceIdExists && checkIfServicesDeviceIdsExist);
    }

    private boolean checkIfServiceIdExists(Service service, ServiceId serviceId) {
        if (service == null) {
            return false;
        }

        final var serviceServiceIdServiceId = service.getServiceId();
        final var serviceServiceIdContextId = serviceServiceIdServiceId.getContextId();
        final var serviceServiceIdId = serviceServiceIdServiceId.getId();

        return serviceServiceIdContextId.equals(serviceId.getContextId())
                && serviceServiceIdId.equals(serviceId.getId());
    }

    private boolean checkIfServicesDeviceIdsExist(Service service, List<String> deviceIds) {
        if (deviceIds.isEmpty()) {
            return true;
        }

        List<String> serviceDeviceIds = new ArrayList<>();
        for (EndPointId serviceEndPointId : service.getServiceEndPointIds()) {
            serviceDeviceIds.add(serviceEndPointId.getDeviceId());
        }

        return deviceIds.containsAll(serviceDeviceIds);
    }

    public Uni<Boolean> isUpdatedPolicyRuleIdValid(String updatedPolicyRuleId) {
        return contextService
                .getPolicyRule(updatedPolicyRuleId)
                .onItem()
                .ifNotNull()
                .transform(
                        id -> {
                            return true;
                        })
                .onItem()
                .ifNull()
                .continueWith(false);
    }

    public Uni<Boolean> isPolicyRuleServiceValid(String updatedPolicyRuleId, ServiceId serviceId) {
        return contextService
                .getPolicyRule(updatedPolicyRuleId)
                .onItem()
                .ifNotNull()
                .transform(
                        policyRule -> {
                            var policyRuleService =
                                    (PolicyRuleService) policyRule.getPolicyRuleType().getPolicyRuleType();
                            if (policyRuleService.getServiceId().getId().equals(serviceId.getId())) {
                                return true;
                            }
                            return false;
                        })
                .onItem()
                .ifNull()
                .continueWith(false)
                .onFailure()
                .recoverWithItem(false);
    }
}
