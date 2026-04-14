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

package org.etsi.tfs.policy;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import io.quarkus.test.junit.QuarkusTest;
import java.util.List;
import org.etsi.tfs.policy.context.model.EndPoint;
import org.etsi.tfs.policy.context.model.EndPointId;
import org.etsi.tfs.policy.context.model.Location;
import org.etsi.tfs.policy.context.model.LocationTypeRegion;
import org.etsi.tfs.policy.context.model.TopologyId;
import org.etsi.tfs.policy.kpi_sample_types.model.KpiSampleType;
import org.junit.jupiter.api.Test;

@QuarkusTest
class EndPointCreationTest {

    @Test
    void shouldCreateEndPointObjectGivenAllAvailableFields() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var expectedEndPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);
        final var expectedEndPointType = "expectedEndPointType";
        final var expectedKpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);

        final var expectedLocationType = new LocationTypeRegion("ATH");
        final var expectedEndPointLocation = new Location(expectedLocationType);

        final var expectedEndPoint =
                new EndPoint.EndPointBuilder(
                                expectedEndPointId, expectedEndPointType, expectedKpiSampleTypes)
                        .location(expectedEndPointLocation)
                        .build();

        assertThat(expectedEndPoint.getEndPointId()).isEqualTo(expectedEndPointId);
        assertThat(expectedEndPoint.getEndPointType()).isEqualTo(expectedEndPointType);
        assertThat(expectedEndPoint.getKpiSampleTypes()).isEqualTo(expectedKpiSampleTypes);
        assertThat(expectedEndPoint.getEndPointLocation()).isEqualTo(expectedEndPointLocation);
    }

    @Test
    void shouldCreateEndPointObjectGivenAllFieldsExceptFromLocation() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var expectedEndPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);
        final var expectedEndPointType = "expectedEndPointType";
        final var expectedKpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);

        final var expectedEndPoint =
                new EndPoint.EndPointBuilder(
                                expectedEndPointId, expectedEndPointType, expectedKpiSampleTypes)
                        .build();

        assertThat(expectedEndPoint.getEndPointId()).isEqualTo(expectedEndPointId);
        assertThat(expectedEndPoint.getEndPointType()).isEqualTo(expectedEndPointType);
        assertThat(expectedEndPoint.getKpiSampleTypes()).isEqualTo(expectedKpiSampleTypes);
    }

    @Test
    void shouldThrowIllegalStateExceptionDuringCreationOfEndPointObjectUponMissingEndPointId() {
        final var expectedEndPointType = "expectedEndPointType";
        final var expectedKpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);

        final var endPoint =
                new EndPoint.EndPointBuilder(null, expectedEndPointType, expectedKpiSampleTypes);

        assertThatExceptionOfType(IllegalStateException.class).isThrownBy(endPoint::build);
    }

    @Test
    void shouldThrowIllegalStateExceptionDuringCreationOfEndPointObjectUponMissingEndPointType() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var expectedEndPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);
        final var expectedKpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);

        final var endPoint =
                new EndPoint.EndPointBuilder(expectedEndPointId, null, expectedKpiSampleTypes);

        assertThatExceptionOfType(IllegalStateException.class).isThrownBy(endPoint::build);
    }

    @Test
    void shouldThrowIllegalStateExceptionDuringCreationOfEndPointObjectUponMissingKpiSampleTypes() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var expectedEndPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);
        final var expectedEndPointType = "expectedEndPointType";

        final var endPoint =
                new EndPoint.EndPointBuilder(expectedEndPointId, expectedEndPointType, null);

        assertThatExceptionOfType(IllegalStateException.class).isThrownBy(endPoint::build);
    }
}
