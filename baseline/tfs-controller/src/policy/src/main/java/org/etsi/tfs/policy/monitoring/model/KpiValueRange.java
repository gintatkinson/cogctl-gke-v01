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

public class KpiValueRange {

    private KpiValue<?> kpiMinValue;
    private KpiValue<?> kpiMaxValue;
    private boolean inRange;
    private boolean includeMinValue;
    private boolean includeMaxValue;

    public KpiValueRange(
            KpiValue<?> kpiMinValue,
            KpiValue<?> kpiMaxValue,
            boolean inRange,
            boolean includeMinValue,
            boolean includeMaxValue) {
        this.kpiMinValue = kpiMinValue;
        this.kpiMaxValue = kpiMaxValue;
        this.inRange = inRange;
        this.includeMinValue = includeMinValue;
        this.includeMaxValue = includeMaxValue;
    }

    public KpiValue<?> getKpiMinValue() {
        return kpiMinValue;
    }

    public KpiValue<?> getKpiMaxValue() {
        return kpiMaxValue;
    }

    public boolean getInRange() {
        return inRange;
    }

    public boolean getIncludeMinValue() {
        return includeMinValue;
    }

    public boolean getIncludeMaxValue() {
        return includeMaxValue;
    }

    public void setKpiMinValue(KpiValue<?> kpiMinValue) {
        this.kpiMinValue = kpiMinValue;
    }

    public void setKpiMaxValue(KpiValue<?> kpiMaxValue) {
        this.kpiMaxValue = kpiMaxValue;
    }

    public void setInRange(boolean inRange) {
        this.inRange = inRange;
    }

    public void setIncludeMinValue(boolean includeMinValue) {
        this.includeMinValue = includeMinValue;
    }

    public void setIncludeMaxValue(boolean includeMaxValue) {
        this.includeMaxValue = includeMaxValue;
    }

    @Override
    public String toString() {
        return String.format("%s:{%s, %s}", getClass().getSimpleName(), kpiMinValue, kpiMaxValue);
    }
}
