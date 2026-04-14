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

public class SubsDescriptor {
    private final String subscriptionId;
    private final String kpiId;
    private final float samplingDurationS;
    private final float samplingIntervalS;
    private final double startTimestamp;
    private final double endTimestamp;

    public SubsDescriptor(
            String subscriptionId,
            String kpiId,
            float samplingDurationS,
            float samplingIntervalS,
            double startTimestamp,
            double endTimestamp) {
        this.subscriptionId = subscriptionId;
        this.kpiId = kpiId;
        this.samplingDurationS = samplingDurationS;
        this.samplingIntervalS = samplingIntervalS;
        this.startTimestamp = startTimestamp;
        this.endTimestamp = endTimestamp;
    }

    public String getSubscriptionId() {
        return subscriptionId;
    }

    public String getKpiId() {
        return kpiId;
    }

    public float getSamplingDurationS() {
        return samplingDurationS;
    }

    public float getSamplingIntervalS() {
        return samplingIntervalS;
    }

    public double getStartTimestamp() {
        return startTimestamp;
    }

    public double getEndTimestamp() {
        return endTimestamp;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{subscriptionId:\"%s\", kpiId:\"%s\", samplingDurationS:\"%f\", samplingIntervalS:\"%f\", startTimestamp:\"%f\", endTimestamp:\"%f\"}",
                getClass().getSimpleName(),
                subscriptionId,
                kpiId,
                samplingDurationS,
                samplingIntervalS,
                startTimestamp,
                endTimestamp);
    }
}
