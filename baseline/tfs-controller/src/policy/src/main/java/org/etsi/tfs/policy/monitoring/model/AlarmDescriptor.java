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

package org.etsi.tfs.policy.monitoring.model;

public class AlarmDescriptor {
    private final String alarmId;
    private final String alarmDescription;
    private final String name;
    private final String kpiId;
    private final KpiValueRange kpiValueRange;
    private final double timestamp;

    public AlarmDescriptor(
            String alarmId,
            String alarmDescription,
            String name,
            String kpiId,
            KpiValueRange kpiValueRange,
            double timestamp) {
        this.alarmId = alarmId;
        this.alarmDescription = alarmDescription;
        this.name = name;
        this.kpiId = kpiId;
        this.kpiValueRange = kpiValueRange;
        this.timestamp = timestamp;
    }

    public String getAlarmId() {
        return alarmId;
    }

    public String getAlarmDescription() {
        return alarmDescription;
    }

    public String getName() {
        return name;
    }

    public String getKpiId() {
        return kpiId;
    }

    public KpiValueRange getKpiValueRange() {
        return kpiValueRange;
    }

    public double getTimestamp() {
        return timestamp;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{alarmId:\"%s\", alarmDescription:\"%s\", name:\"%s\", [%s], [%s], timestamp:\"%f\"}",
                getClass().getSimpleName(),
                alarmId,
                alarmDescription,
                name,
                kpiId,
                kpiValueRange,
                timestamp);
    }
}
