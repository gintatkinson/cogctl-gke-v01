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

package org.etsi.tfs.policy.context.model;

import java.util.List;
import org.etsi.tfs.policy.common.Util;
import org.etsi.tfs.policy.kpi_sample_types.model.KpiSampleType;

public class EndPoint {
    private final EndPointId endPointId;
    private final String endPointType;
    private final List<KpiSampleType> kpiSampleTypes;
    private final Location endPointLocation;

    EndPoint(EndPointBuilder builder) {
        this.endPointId = builder.endPointId;
        this.endPointType = builder.endPointType;
        this.kpiSampleTypes = builder.kpiSampleTypes;
        this.endPointLocation = builder.endPointLocation;
    }

    public EndPointId getEndPointId() {
        return endPointId;
    }

    public String getEndPointType() {
        return endPointType;
    }

    public List<KpiSampleType> getKpiSampleTypes() {
        return kpiSampleTypes;
    }

    public Location getEndPointLocation() {
        return endPointLocation;
    }

    @Override
    public String toString() {
        return String.format(
                "%s:{%s, endPointType:\"%s\", [%s], %s}",
                getClass().getSimpleName(),
                endPointId,
                endPointType,
                Util.toString(kpiSampleTypes),
                endPointLocation);
    }

    public static class EndPointBuilder {
        private final EndPointId endPointId;
        private final String endPointType;
        private final List<KpiSampleType> kpiSampleTypes;
        private Location endPointLocation;

        public EndPointBuilder(
                EndPointId endPointId, String endPointType, List<KpiSampleType> kpiSampleTypes) {
            this.endPointId = endPointId;
            this.endPointType = endPointType;
            this.kpiSampleTypes = kpiSampleTypes;
        }

        public EndPointBuilder location(Location endPointLocation) {
            this.endPointLocation = endPointLocation;
            return this;
        }

        public EndPoint build() {
            EndPoint endPoint = new EndPoint(this);
            validateEndPointObject(endPoint);
            return endPoint;
        }

        private void validateEndPointObject(EndPoint endPoint) {
            final var validatedEndPointId = endPoint.getEndPointId();
            final var validatedEndPointType = endPoint.getEndPointType();
            final var validatedKpiSampleTypes = endPoint.getKpiSampleTypes();

            if (validatedEndPointId == null) {
                throw new IllegalStateException("EndPoint ID cannot be null");
            }

            if (validatedEndPointType == null) {
                throw new IllegalStateException("EndPoint type cannot be null");
            }

            if (validatedKpiSampleTypes == null) {
                throw new IllegalStateException("Kpi sample types cannot be null");
            }
        }
    }
}
