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

import org.etsi.tfs.policy.context.model.EndPointId;
import org.etsi.tfs.policy.context.model.ServiceId;
import org.etsi.tfs.policy.context.model.SliceId;
import org.etsi.tfs.policy.kpi_sample_types.model.KpiSampleType;

public class KpiDescriptor {

    private final String kpiDescription;
    private final KpiSampleType kpiSampleType;
    private final String deviceId;
    private final EndPointId endPointId;
    private final ServiceId serviceId;
    private final SliceId sliceId;

    public KpiDescriptor(
            String kpiDescription,
            KpiSampleType kpiSampleType,
            String deviceId,
            EndPointId endPointId,
            ServiceId serviceId,
            SliceId sliceId) {
        this.kpiDescription = kpiDescription;
        this.kpiSampleType = kpiSampleType;
        this.deviceId = deviceId;
        this.endPointId = endPointId;
        this.serviceId = serviceId;
        this.sliceId = sliceId;
    }

    public String getKpiDescription() {
        return kpiDescription;
    }

    public KpiSampleType getKpiSampleType() {
        return kpiSampleType;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public EndPointId getEndPointId() {
        return endPointId;
    }

    public ServiceId getServiceId() {
        return serviceId;
    }

    public SliceId getSliceId() {
        return sliceId;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{kpiDescription:\"%s\", kpiSampleType:\"%s\", deviceId:\"%s\", %s, %s, %s}",
                getClass().getSimpleName(),
                kpiDescription,
                kpiSampleType.toString(),
                deviceId,
                endPointId,
                serviceId,
                sliceId);
    }
}
