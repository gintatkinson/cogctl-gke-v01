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
import org.etsi.tfs.policy.context.model.Empty;
import org.etsi.tfs.policy.monitoring.model.AlarmDescriptor;
import org.etsi.tfs.policy.monitoring.model.AlarmResponse;
import org.etsi.tfs.policy.monitoring.model.AlarmSubscription;
import org.etsi.tfs.policy.monitoring.model.KpiDescriptor;
import org.etsi.tfs.policy.monitoring.model.MonitorKpiRequest;
import org.etsi.tfs.policy.monitoring.model.SubsDescriptor;
import org.etsi.tfs.policy.monitoring.model.SubsResponse;

public interface MonitoringGateway {

    Uni<String> setKpi(KpiDescriptor kpiDescriptor);

    Uni<KpiDescriptor> getKpiDescriptor(String kpiId);

    Uni<Empty> monitorKpi(MonitorKpiRequest monitorKpiRequest);

    Multi<SubsResponse> setKpiSubscription(SubsDescriptor subsDescriptor);

    Uni<SubsDescriptor> getSubsDescriptor(String subscriptionId);

    Uni<String> setKpiAlarm(AlarmDescriptor alarmDescriptor);

    Uni<AlarmDescriptor> getAlarmDescriptor(String alarmId);

    Multi<AlarmResponse> getAlarmResponseStream(AlarmSubscription alarmSubscription);

    Uni<Empty> deleteAlarm(String deviceId);

    Uni<Empty> deleteKpi(String kpiId);
}
