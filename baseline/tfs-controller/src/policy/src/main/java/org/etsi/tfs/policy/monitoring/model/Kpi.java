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

public class Kpi {

    private final String kpiId;
    private final double timestamp;
    private final KpiValue<?> kpiValue;

    public Kpi(String kpiId, double timestamp, KpiValue<?> kpiValue) {
        this.kpiId = kpiId;
        this.timestamp = timestamp;
        this.kpiValue = kpiValue;
    }

    public String getKpiId() {
        return kpiId;
    }

    public double getTimestamp() {
        return timestamp;
    }

    public KpiValue getKpiValue() {
        return kpiValue;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{kpiId:\"%s\", timeStamp:\"%f\", %s}",
                getClass().getSimpleName(), kpiId, timestamp, kpiValue);
    }
}
