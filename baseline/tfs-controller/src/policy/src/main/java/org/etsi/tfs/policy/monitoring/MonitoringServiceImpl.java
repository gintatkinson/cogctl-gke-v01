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

package org.etsi.tfs.policy.monitoring;

import io.smallrye.mutiny.Multi;
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.policy.context.model.Empty;
import org.etsi.tfs.policy.monitoring.model.AlarmDescriptor;
import org.etsi.tfs.policy.monitoring.model.AlarmResponse;
import org.etsi.tfs.policy.monitoring.model.AlarmSubscription;
import org.etsi.tfs.policy.monitoring.model.KpiDescriptor;
import org.etsi.tfs.policy.monitoring.model.MonitorKpiRequest;
import org.etsi.tfs.policy.monitoring.model.SubsDescriptor;
import org.etsi.tfs.policy.monitoring.model.SubsResponse;

@ApplicationScoped
public class MonitoringServiceImpl implements MonitoringService {

    private final MonitoringGateway monitoringGateway;

    @Inject
    public MonitoringServiceImpl(MonitoringGateway monitoringGateway) {
        this.monitoringGateway = monitoringGateway;
    }

    @Override
    public Uni<String> setKpi(KpiDescriptor kpiDescriptor) {
        return monitoringGateway.setKpi(kpiDescriptor);
    }

    @Override
    public Uni<KpiDescriptor> getKpiDescriptor(String kpiId) {
        return monitoringGateway.getKpiDescriptor(kpiId);
    }

    @Override
    public Uni<Empty> monitorKpi(MonitorKpiRequest monitorKpiRequest) {
        return monitoringGateway.monitorKpi(monitorKpiRequest);
    }

    @Override
    public Multi<SubsResponse> setKpiSubscription(SubsDescriptor subsDescriptor) {
        return monitoringGateway.setKpiSubscription(subsDescriptor);
    }

    @Override
    public Uni<SubsDescriptor> getSubsDescriptor(String subscriptionId) {
        return monitoringGateway.getSubsDescriptor(subscriptionId);
    }

    @Override
    public Uni<String> setKpiAlarm(AlarmDescriptor alarmDescriptor) {
        return monitoringGateway.setKpiAlarm(alarmDescriptor);
    }

    @Override
    public Uni<AlarmDescriptor> getAlarmDescriptor(String alarmId) {
        return monitoringGateway.getAlarmDescriptor(alarmId);
    }

    @Override
    public Multi<AlarmResponse> getAlarmResponseStream(AlarmSubscription alarmSubscription) {
        return monitoringGateway.getAlarmResponseStream(alarmSubscription);
    }

    @Override
    public Uni<Empty> deleteAlarm(String alarmId) {
        return monitoringGateway.deleteAlarm(alarmId);
    }

    @Override
    public Uni<Empty> deleteKpi(String kpiId) {
        return monitoringGateway.deleteKpi(kpiId);
    }
}
