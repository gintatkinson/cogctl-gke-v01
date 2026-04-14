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

import io.quarkus.grpc.GrpcClient;
import io.smallrye.mutiny.Multi;
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import monitoring.MutinyMonitoringServiceGrpc.MutinyMonitoringServiceStub;
import org.etsi.tfs.policy.Serializer;
import org.etsi.tfs.policy.context.model.Empty;
import org.etsi.tfs.policy.monitoring.model.AlarmDescriptor;
import org.etsi.tfs.policy.monitoring.model.AlarmResponse;
import org.etsi.tfs.policy.monitoring.model.AlarmSubscription;
import org.etsi.tfs.policy.monitoring.model.KpiDescriptor;
import org.etsi.tfs.policy.monitoring.model.MonitorKpiRequest;
import org.etsi.tfs.policy.monitoring.model.SubsDescriptor;
import org.etsi.tfs.policy.monitoring.model.SubsResponse;

@ApplicationScoped
public class MonitoringGatewayImpl implements MonitoringGateway {

    @GrpcClient("monitoring")
    MutinyMonitoringServiceStub streamingDelegateMonitoring;

    private final Serializer serializer;

    @Inject
    public MonitoringGatewayImpl(Serializer serializer) {
        this.serializer = serializer;
    }

    @Override
    public Uni<String> setKpi(KpiDescriptor kpiDescriptor) {
        final var serializedKpiDescriptor = serializer.serialize(kpiDescriptor);

        return streamingDelegateMonitoring
                .setKpi(serializedKpiDescriptor)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<KpiDescriptor> getKpiDescriptor(String kpiId) {
        final var serializedKpiId = serializer.serializeKpiId(kpiId);

        return streamingDelegateMonitoring
                .getKpiDescriptor(serializedKpiId)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<Empty> monitorKpi(MonitorKpiRequest monitorKpiRequest) {
        final var serializedKpiId = serializer.serialize(monitorKpiRequest);

        return streamingDelegateMonitoring
                .monitorKpi(serializedKpiId)
                .onItem()
                .transform(serializer::deserializeEmpty);
    }

    @Override
    public Multi<SubsResponse> setKpiSubscription(SubsDescriptor subsDescriptor) {
        final var serializedSubsDescriptor = serializer.serialize(subsDescriptor);

        return streamingDelegateMonitoring
                .setKpiSubscription(serializedSubsDescriptor)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<SubsDescriptor> getSubsDescriptor(String subscriptionId) {
        final var serializedSubscriptionId = serializer.serializeSubscriptionIdId(subscriptionId);

        return streamingDelegateMonitoring
                .getSubsDescriptor(serializedSubscriptionId)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<String> setKpiAlarm(AlarmDescriptor alarmDescriptor) {
        final var serializedAlarmDescriptor = serializer.serialize(alarmDescriptor);

        return streamingDelegateMonitoring
                .setKpiAlarm(serializedAlarmDescriptor)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<AlarmDescriptor> getAlarmDescriptor(String alarmId) {
        final var serializedAlarmId = serializer.serializeAlarmId(alarmId);

        return streamingDelegateMonitoring
                .getAlarmDescriptor(serializedAlarmId)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Multi<AlarmResponse> getAlarmResponseStream(AlarmSubscription alarmSubscription) {
        final var serializedAlarmSubscription = serializer.serialize(alarmSubscription);

        return streamingDelegateMonitoring
                .getAlarmResponseStream(serializedAlarmSubscription)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<Empty> deleteAlarm(String alarmId) {
        final var serializedAlarmId = serializer.serializeAlarmId(alarmId);

        return streamingDelegateMonitoring
                .deleteAlarm(serializedAlarmId)
                .onItem()
                .transform(serializer::deserializeEmpty);
    }

    @Override
    public Uni<Empty> deleteKpi(String kpiId) {
        final var serializedKpiId = serializer.serializeKpiId(kpiId);

        return streamingDelegateMonitoring
                .deleteKpi(serializedKpiId)
                .onItem()
                .transform(serializer::deserializeEmpty);
    }
}
