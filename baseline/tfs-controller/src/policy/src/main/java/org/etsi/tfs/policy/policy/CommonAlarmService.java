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

import io.smallrye.mutiny.Multi;
import io.smallrye.mutiny.Uni;
import io.smallrye.mutiny.subscription.Cancellable;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import java.util.ArrayList;
import java.util.List;
import org.etsi.tfs.policy.monitoring.MonitoringService;
import org.etsi.tfs.policy.monitoring.model.AlarmDescriptor;
import org.etsi.tfs.policy.monitoring.model.AlarmResponse;
import org.etsi.tfs.policy.monitoring.model.AlarmSubscription;
import org.etsi.tfs.policy.policy.model.PolicyRuleDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleService;
import org.jboss.logging.Logger;

@ApplicationScoped
public class CommonAlarmService {
    private static final Logger LOGGER = Logger.getLogger(CommonAlarmService.class);

    @Inject private CommonPolicyServiceImpl commonPolicyServiceImpl;
    @Inject private MonitoringService monitoringService;

    /**
     * Transform the alarmIds into promised alarms returned from the getAlarmResponseStream
     *
     * @param alarmIds the list of alarm ids
     * @param policyRuleService the policy rule service
     * @return
     */
    private List<Multi<AlarmResponse>> transformAlarmIds(
            List<Uni<String>> alarmIds, PolicyRuleService policyRuleService) {
        List<Multi<AlarmResponse>> alarmResponseStreamList = new ArrayList<>();
        for (Uni<String> alarmId : alarmIds) {
            Multi<AlarmResponse> alarmResponseStream =
                    alarmId.onItem().transformToMulti(id -> setPolicyMonitor(policyRuleService, id));

            alarmResponseStreamList.add(alarmResponseStream);
        }
        return alarmResponseStreamList;
    }

    private List<Multi<AlarmResponse>> transformAlarmIds(
            List<Uni<String>> alarmIds, PolicyRuleDevice policyRuleDevice) {
        // Transform the alarmIds into promised alarms returned from the
        // getAlarmResponseStream
        List<Multi<AlarmResponse>> alarmResponseStreamList = new ArrayList<>();
        for (Uni<String> alarmId : alarmIds) {
            alarmResponseStreamList.add(
                    alarmId.onItem().transformToMulti(id -> setPolicyMonitor(policyRuleDevice, id)));
        }
        return alarmResponseStreamList;
    }

    private Multi<AlarmResponse> setPolicyMonitor(PolicyRuleService policyRuleService, String id) {
        commonPolicyServiceImpl.getAlarmPolicyRuleServiceMap().put(id, policyRuleService);

        // TODO: Create infinite subscription
        var alarmSubscription = new AlarmSubscription(id, 259200, 5000);
        return monitoringService.getAlarmResponseStream(alarmSubscription);
    }

    private Multi<AlarmResponse> setPolicyMonitor(PolicyRuleDevice policyRuleDevice, String id) {
        commonPolicyServiceImpl.getAlarmPolicyRuleDeviceMap().put(id, policyRuleDevice);

        // TODO: Create infinite subscription
        var alarmSubscription = new AlarmSubscription(id, 259200, 5000);
        return monitoringService.getAlarmResponseStream(alarmSubscription);
    }

    /**
     * Create an alarmIds list that contains the promised ids returned from setKpiAlarm
     *
     * @param alarmDescriptorList the list of alarm descriptors
     * @return the list of alarm descriptors
     */
    public List<Uni<String>> createAlarmList(List<AlarmDescriptor> alarmDescriptorList) {
        List<Uni<String>> alarmIds = new ArrayList<Uni<String>>();
        for (AlarmDescriptor alarmDescriptor : alarmDescriptorList) {
            LOGGER.infof("alarmDescriptor:");
            LOGGER.infof(alarmDescriptor.toString());
            alarmIds.add(monitoringService.setKpiAlarm(alarmDescriptor));
        }
        return alarmIds;
    }

    private Cancellable monitorAlarmResponseForService(Multi<AlarmResponse> multi) {
        return multi
                .subscribe()
                .with(
                        alarmResponse -> {
                            LOGGER.infof("**************************Received Alarm!**************************");
                            LOGGER.infof("alarmResponse:");
                            LOGGER.info(alarmResponse);
                            LOGGER.info(alarmResponse.getAlarmId());
                            commonPolicyServiceImpl.applyActionService(alarmResponse.getAlarmId());
                        });
    }

    private Cancellable monitorAlarmResponseForDevice(Multi<AlarmResponse> multi) {
        return multi
                .subscribe()
                .with(
                        alarmResponse -> {
                            LOGGER.infof("**************************Received Alarm!**************************");
                            LOGGER.infof("alarmResponse:");
                            LOGGER.info(alarmResponse);
                            LOGGER.info(alarmResponse.getAlarmId());
                            commonPolicyServiceImpl.applyActionDevice(alarmResponse.getAlarmId());
                        });
    }
}
