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

import static org.etsi.tfs.policy.common.ApplicationProperties.ACTIVE_POLICYRULE_STATE;
import static org.etsi.tfs.policy.common.ApplicationProperties.ENFORCED_POLICYRULE_STATE;
import static org.etsi.tfs.policy.common.ApplicationProperties.INVALID_MESSAGE;

import io.smallrye.mutiny.subscription.Cancellable;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ConcurrentHashMap;
import org.etsi.tfs.policy.context.ContextService;
import org.etsi.tfs.policy.context.model.ConfigActionEnum;
import org.etsi.tfs.policy.context.model.ConfigRule;
import org.etsi.tfs.policy.context.model.ConfigRuleCustom;
import org.etsi.tfs.policy.context.model.ConfigRuleTypeCustom;
import org.etsi.tfs.policy.context.model.Constraint;
import org.etsi.tfs.policy.context.model.ConstraintCustom;
import org.etsi.tfs.policy.context.model.ConstraintTypeCustom;
import org.etsi.tfs.policy.context.model.ServiceConfig;
import org.etsi.tfs.policy.device.DeviceService;
import org.etsi.tfs.policy.monitoring.MonitoringService;
import org.etsi.tfs.policy.monitoring.model.AlarmDescriptor;
import org.etsi.tfs.policy.monitoring.model.KpiValueRange;
import org.etsi.tfs.policy.policy.model.PolicyRule;
import org.etsi.tfs.policy.policy.model.PolicyRuleAction;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionConfig;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleCondition;
import org.etsi.tfs.policy.policy.model.PolicyRuleDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleService;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleTypeDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleTypeService;
import org.etsi.tfs.policy.service.ServiceService;
import org.jboss.logging.Logger;

@ApplicationScoped
public class CommonPolicyServiceImpl {

    private static final Logger LOGGER = Logger.getLogger(CommonPolicyServiceImpl.class);

    @Inject private MonitoringService monitoringService;
    @Inject private ContextService contextService;
    @Inject private ServiceService serviceService;
    @Inject private DeviceService deviceService;

    private static final int POLICY_EVALUATION_TIMEOUT = 5;
    private static final int ACCEPTABLE_NUMBER_OF_ALARMS = 3;
    private static final int MONITORING_WINDOW_IN_SECONDS = 5;
    private static final int SAMPLING_RATE_PER_SECOND = 1;

    // TODO: Find a better way to disregard alarms while reconfiguring path
    // Temporary solution for not calling the same rpc more than it's needed
    public static int noAlarms = 0;
    private ConcurrentHashMap<String, PolicyRuleService> kpiPolicyRuleServiceMap =
            new ConcurrentHashMap<>();
    private ConcurrentHashMap<String, PolicyRuleService> alarmPolicyRuleServiceMap =
            new ConcurrentHashMap<>();
    private ConcurrentHashMap<String, PolicyRuleDevice> alarmPolicyRuleDeviceMap =
            new ConcurrentHashMap<>();
    private ConcurrentHashMap<String, Cancellable> subscriptionList = new ConcurrentHashMap<>();
    private HashMap<String, PolicyRuleAction> policyRuleActionMap = new HashMap<>();

    public ConcurrentHashMap<String, Cancellable> getSubscriptionList() {
        return subscriptionList;
    }

    public ConcurrentHashMap<String, PolicyRuleService> getKpiPolicyRuleServiceMap() {
        return kpiPolicyRuleServiceMap;
    }

    public ConcurrentHashMap<String, PolicyRuleService> getAlarmPolicyRuleServiceMap() {
        return alarmPolicyRuleServiceMap;
    }

    public ConcurrentHashMap<String, PolicyRuleDevice> getAlarmPolicyRuleDeviceMap() {
        return alarmPolicyRuleDeviceMap;
    }

    public HashMap<String, PolicyRuleAction> getPolicyRuleActionMap() {
        return policyRuleActionMap;
    }

    private static String gen() {
        Random r = new Random(System.currentTimeMillis());
        return String.valueOf((1 + r.nextInt(2)) * 10000 + r.nextInt(10000));
    }

    private static double getTimeStamp() {
        long now = Instant.now().getEpochSecond();
        return Long.valueOf(now).doubleValue();
    }

    public void applyActionServiceBasedOnKpiId(String kpiId) {
        if (!kpiPolicyRuleServiceMap.containsKey(kpiId)) {
            LOGGER.info("No Policy for KpiId");
            return;
        }

        PolicyRuleService policyRuleService = kpiPolicyRuleServiceMap.get(kpiId);
        PolicyRuleAction policyRuleAction =
                policyRuleService.getPolicyRuleBasic().getPolicyRuleActions().get(0);

        setPolicyRuleServiceToContext(policyRuleService, ACTIVE_POLICYRULE_STATE);

        switch (policyRuleAction.getPolicyRuleActionEnum()) {
            case POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT:
                addServiceConstraint(policyRuleService, policyRuleAction);
            case POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE:
                addServiceConfigRule(policyRuleService, policyRuleAction);
            case POLICY_RULE_ACTION_RECALCULATE_PATH:
                callRecalculatePathRPC(policyRuleService, policyRuleAction);
            case POLICY_RULE_ACTION_CALL_SERVICE_RPC:
                callUpdateServiceRpc(policyRuleService, policyRuleAction);
            default:
                LOGGER.errorf(INVALID_MESSAGE, policyRuleAction.getPolicyRuleActionEnum());
        }
    }

    public void applyActionService(String alarmId) {
        PolicyRuleService policyRuleService = alarmPolicyRuleServiceMap.get(alarmId);
        PolicyRuleAction policyRuleAction =
                policyRuleService.getPolicyRuleBasic().getPolicyRuleActions().get(0);

        setPolicyRuleServiceToContext(policyRuleService, ACTIVE_POLICYRULE_STATE);

        switch (policyRuleAction.getPolicyRuleActionEnum()) {
            case POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT:
                addServiceConstraint(policyRuleService, policyRuleAction);
            case POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE:
                addServiceConfigRule(policyRuleService, policyRuleAction);
            case POLICY_RULE_ACTION_RECALCULATE_PATH:
                callRecalculatePathRPC(policyRuleService, policyRuleAction);
            default:
                LOGGER.errorf(INVALID_MESSAGE, policyRuleAction.getPolicyRuleActionEnum());
        }
    }

    private KpiValueRange convertPolicyRuleConditionToKpiValueRange(
            PolicyRuleCondition policyRuleCondition) {

        switch (policyRuleCondition.getNumericalOperator()) {
            case POLICY_RULE_CONDITION_NUMERICAL_EQUAL:
                return new KpiValueRange(
                        policyRuleCondition.getKpiValue(), policyRuleCondition.getKpiValue(), true, true, true);
            case POLICY_RULE_CONDITION_NUMERICAL_NOT_EQUAL:
                return new KpiValueRange(
                        policyRuleCondition.getKpiValue(),
                        policyRuleCondition.getKpiValue(),
                        true,
                        false,
                        false);

            case POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN:
                return new KpiValueRange(null, policyRuleCondition.getKpiValue(), true, false, false);

            case POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL:
                return new KpiValueRange(null, policyRuleCondition.getKpiValue(), true, true, false);

            case POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN:
                return new KpiValueRange(policyRuleCondition.getKpiValue(), null, true, false, false);

            case POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN_EQUAL:
                return new KpiValueRange(policyRuleCondition.getKpiValue(), null, true, false, true);
            default:
                return null;
        }
    }

    private KpiValueRange combineKpiValueRanges(
            String kpiId, KpiValueRange firstKpiValueRange, KpiValueRange secondKpiValueRange) {
        if (secondKpiValueRange.getInRange() == true) {
            LOGGER.errorf("KpiId: %s, has already range values", kpiId);
            return null;
        }

        if ((firstKpiValueRange.getKpiMinValue() != null)
                && (secondKpiValueRange.getKpiMinValue() != null)) {
            LOGGER.errorf("KpiId: %s, has already min value", kpiId);
            return null;
        }

        if ((firstKpiValueRange.getKpiMaxValue() != null)
                && (secondKpiValueRange.getKpiMinValue() != null)) {
            LOGGER.errorf("KpiId: %s, has already max value", kpiId);
            return null;
        }

        // Objects.nonNull(secondKpiValueRange);

        var kpiMinValue =
                firstKpiValueRange.getKpiMinValue() != null
                        ? firstKpiValueRange.getKpiMinValue()
                        : secondKpiValueRange.getKpiMinValue();
        var kpiMaxValue =
                firstKpiValueRange.getKpiMaxValue() != null
                        ? firstKpiValueRange.getKpiMaxValue()
                        : secondKpiValueRange.getKpiMaxValue();
        boolean includeMinValue =
                firstKpiValueRange.getIncludeMinValue() || secondKpiValueRange.getIncludeMinValue();
        boolean includeMaxValue =
                firstKpiValueRange.getIncludeMaxValue() || secondKpiValueRange.getIncludeMaxValue();

        return new KpiValueRange(kpiMinValue, kpiMaxValue, true, includeMinValue, includeMaxValue);
    }

    private AlarmDescriptor createAlarmDescriptorWithoutRange(
            PolicyRuleCondition policyRuleCondition) {

        final var kpiId = policyRuleCondition.getKpiId();
        final var kpiValueRange = convertPolicyRuleConditionToKpiValueRange(policyRuleCondition);

        return new AlarmDescriptor(
                "", "alarmDescription", "alarmName-" + gen(), kpiId, kpiValueRange, getTimeStamp());
    }

    // TODO: To be refactored or deprecated
    //    private void evaluateAction(
    //            PolicyRule policyRule,
    //            List<AlarmDescriptor> alarmDescriptorList,
    //            Multi<AlarmResponse> multi) {
    //
    //        Long count =
    //                multi
    //                        .collect()
    //                        .with(Collectors.counting())
    //                        .await()
    //                        .atMost(Duration.ofMinutes(POLICY_EVALUATION_TIMEOUT));
    //
    //        if (count > ACCEPTABLE_NUMBER_OF_ALARMS) {
    //            for (AlarmDescriptor alarmDescriptor : alarmDescriptorList) {
    //                monitoringService
    //                        .deleteAlarm(alarmDescriptor.getAlarmId())
    //                        .subscribe()
    //                        .with(
    //                                emptyMessage ->
    //                                        LOGGER.infof(
    //                                                "Alarm [%s] has been deleted as ineffective.\n",
    //                                                alarmDescriptor.getAlarmId()));
    //            }
    //            setPolicyRuleToContext(policyRule, INEFFECTIVE_POLICYRULE_STATE);
    //        } else {
    //            setPolicyRuleToContext(policyRule, EFFECTIVE_POLICYRULE_STATE);
    //        }
    //    }

    public void applyActionDevice(String alarmId) {
        PolicyRuleDevice policyRuleDevice = alarmPolicyRuleDeviceMap.get(alarmId);

        if (policyRuleActionMap.get(alarmId).getPolicyRuleActionEnum()
                == PolicyRuleActionEnum.POLICY_RULE_ACTION_SET_DEVICE_STATUS) {
            // In case additional PolicyRuleAction for Devices will be added
        }

        setPolicyRuleDeviceToContext(policyRuleDevice, ACTIVE_POLICYRULE_STATE);

        List<String> deviceIds = policyRuleDevice.getDeviceIds();
        List<PolicyRuleActionConfig> actionConfigs =
                policyRuleActionMap.get(alarmId).getPolicyRuleActionConfigs();

        if (deviceIds.size() != actionConfigs.size()) {
            String message =
                    String.format(
                            "The number of action parameters in PolicyRuleDevice with ID: %s, is not aligned with the number of devices.",
                            policyRuleDevice.getPolicyRuleBasic().getPolicyRuleId());
            setPolicyRuleDeviceToContext(
                    policyRuleDevice, new PolicyRuleState(PolicyRuleStateEnum.POLICY_FAILED, message));
            return;
        }

        for (var i = 0; i < deviceIds.size(); i++) {
            activateDevice(deviceIds.get(i), actionConfigs.get(i));
        }

        setPolicyRuleDeviceToContext(policyRuleDevice, ENFORCED_POLICYRULE_STATE);
    }

    private void activateDevice(String deviceId, PolicyRuleActionConfig actionConfig) {

        Boolean toBeEnabled;
        if (actionConfig.getActionKey() == "ENABLED") {
            toBeEnabled = true;
        } else if (actionConfig.getActionKey() == "DISABLED") {
            toBeEnabled = false;
        } else {
            LOGGER.errorf(INVALID_MESSAGE, actionConfig.getActionKey());
            return;
        }

        final var deserializedDeviceUni = contextService.getDevice(deviceId);

        deserializedDeviceUni
                .subscribe()
                .with(
                        device -> {
                            if (toBeEnabled && device.isDisabled()) {
                                device.enableDevice();
                            } else if (!toBeEnabled && device.isEnabled()) {
                                device.disableDevice();
                            } else {
                                LOGGER.errorf(INVALID_MESSAGE, "Device is already in the desired state");
                                return;
                            }

                            deviceService.configureDevice(device);
                        });
    }

    private void addServiceConfigRule(
            PolicyRuleService policyRuleService, PolicyRuleAction policyRuleAction) {

        ConfigActionEnum configActionEnum = ConfigActionEnum.SET;
        List<PolicyRuleActionConfig> actionConfigs = policyRuleAction.getPolicyRuleActionConfigs();
        List<ConfigRule> newConfigRules = new ArrayList<>();

        for (PolicyRuleActionConfig actionConfig : actionConfigs) {
            ConfigRuleCustom configRuleCustom =
                    new ConfigRuleCustom(actionConfig.getActionKey(), actionConfig.getActionValue());
            ConfigRuleTypeCustom configRuleType = new ConfigRuleTypeCustom(configRuleCustom);
            ConfigRule configRule = new ConfigRule(configActionEnum, configRuleType);
            newConfigRules.add(configRule);
        }

        var deserializedServiceUni = contextService.getService(policyRuleService.getServiceId());
        deserializedServiceUni
                .subscribe()
                .with(
                        deserializedService -> {
                            List<ConfigRule> configRules =
                                    deserializedService.getServiceConfig().getConfigRules();
                            configRules.addAll(newConfigRules);
                            deserializedService.setServiceConfig(new ServiceConfig(configRules));
                        });
    }

    private void addServiceConstraint(
            PolicyRuleService policyRuleService, PolicyRuleAction policyRuleAction) {

        List<PolicyRuleActionConfig> actionConfigs = policyRuleAction.getPolicyRuleActionConfigs();
        List<Constraint> constraintList = new ArrayList<>();

        for (PolicyRuleActionConfig actionConfig : actionConfigs) {
            var constraintCustom =
                    new ConstraintCustom(actionConfig.getActionKey(), actionConfig.getActionValue());
            var constraintTypeCustom = new ConstraintTypeCustom(constraintCustom);
            constraintList.add(new Constraint(constraintTypeCustom));
        }

        final var deserializedServiceUni = contextService.getService(policyRuleService.getServiceId());

        deserializedServiceUni
                .subscribe()
                .with(
                        deserializedService -> {
                            deserializedService.appendServiceConstraints(constraintList);
                            serviceService.updateService(deserializedService);
                            setPolicyRuleServiceToContext(policyRuleService, ENFORCED_POLICYRULE_STATE);
                        });
    }

    private void callUpdateServiceRpc(
            PolicyRuleService policyRuleService, PolicyRuleAction policyRuleAction) {

        final var deserializedServiceUni = contextService.getService(policyRuleService.getServiceId());

        deserializedServiceUni
                .subscribe()
                .with(
                        deserializedService -> {
                            serviceService
                                    .updateService(deserializedService)
                                    .subscribe()
                                    .with(
                                            x -> {
                                                LOGGER.info(deserializedService);
                                                setPolicyRuleServiceToContext(policyRuleService, ENFORCED_POLICYRULE_STATE);
                                            });
                        });
    }

    private void callRecalculatePathRPC(
            PolicyRuleService policyRuleService, PolicyRuleAction policyRuleAction) {

        final var deserializedServiceUni = contextService.getService(policyRuleService.getServiceId());

        deserializedServiceUni
                .subscribe()
                .with(
                        deserializedService -> {
                            serviceService
                                    .recomputeConnections(deserializedService)
                                    .subscribe()
                                    .with(
                                            x -> {
                                                LOGGER.info("called recomputeConnections with:");
                                                LOGGER.info(deserializedService);
                                                setPolicyRuleServiceToContext(policyRuleService, ENFORCED_POLICYRULE_STATE);
                                            });
                        });
    }

    private void setPolicyRuleToContext(PolicyRule policyRule, PolicyRuleState policyRuleState) {
        final var policyRuleType = policyRule.getPolicyRuleType();
        final var policyRuleTypeSpecificType = policyRuleType.getPolicyRuleType();

        if (policyRuleTypeSpecificType instanceof PolicyRuleService) {
            setPolicyRuleServiceToContext(
                    (PolicyRuleService) policyRuleTypeSpecificType, policyRuleState);
        }
        if (policyRuleTypeSpecificType instanceof PolicyRuleDevice) {
            setPolicyRuleDeviceToContext((PolicyRuleDevice) policyRuleTypeSpecificType, policyRuleState);
        }
    }

    public void setPolicyRuleServiceToContext(
            PolicyRuleService policyRuleService, PolicyRuleState policyRuleState) {
        LOGGER.infof("Setting Policy Rule state to [%s]", policyRuleState.toString());

        final var policyRuleBasic = policyRuleService.getPolicyRuleBasic();
        policyRuleService.setPolicyRuleBasic(policyRuleBasic);

        final var policyRuleTypeService = new PolicyRuleTypeService(policyRuleService);
        final var policyRule = new PolicyRule(policyRuleTypeService);
        contextService.setPolicyRule(policyRule).subscribe().with(x -> {});
    }

    public void setPolicyRuleDeviceToContext(
            PolicyRuleDevice policyRuleDevice, PolicyRuleState policyRuleState) {
        LOGGER.infof("Setting Policy Rule state to [%s]", policyRuleState.toString());

        final var policyRuleBasic = policyRuleDevice.getPolicyRuleBasic();
        policyRuleDevice.setPolicyRuleBasic(policyRuleBasic);

        final var policyRuleTypeService = new PolicyRuleTypeDevice(policyRuleDevice);
        final var policyRule = new PolicyRule(policyRuleTypeService);
        contextService.setPolicyRule(policyRule).subscribe().with(x -> {});
    }
}
