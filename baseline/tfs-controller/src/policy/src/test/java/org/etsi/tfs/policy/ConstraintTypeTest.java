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

import io.quarkus.test.junit.QuarkusTest;
import java.util.List;
import org.etsi.tfs.policy.context.model.ConstraintCustom;
import org.etsi.tfs.policy.context.model.ConstraintEndPointLocation;
import org.etsi.tfs.policy.context.model.ConstraintSchedule;
import org.etsi.tfs.policy.context.model.ConstraintSlaAvailability;
import org.etsi.tfs.policy.context.model.ConstraintSlaCapacity;
import org.etsi.tfs.policy.context.model.ConstraintSlaIsolationLevel;
import org.etsi.tfs.policy.context.model.ConstraintSlaLatency;
import org.etsi.tfs.policy.context.model.ConstraintTypeCustom;
import org.etsi.tfs.policy.context.model.ConstraintTypeEndPointLocation;
import org.etsi.tfs.policy.context.model.ConstraintTypeSchedule;
import org.etsi.tfs.policy.context.model.ConstraintTypeSlaAvailability;
import org.etsi.tfs.policy.context.model.ConstraintTypeSlaCapacity;
import org.etsi.tfs.policy.context.model.ConstraintTypeSlaIsolationLevel;
import org.etsi.tfs.policy.context.model.ConstraintTypeSlaLatency;
import org.etsi.tfs.policy.context.model.EndPointId;
import org.etsi.tfs.policy.context.model.IsolationLevelEnum;
import org.etsi.tfs.policy.context.model.Location;
import org.etsi.tfs.policy.context.model.LocationTypeRegion;
import org.etsi.tfs.policy.context.model.TopologyId;
import org.junit.jupiter.api.Test;

@QuarkusTest
class ConstraintTypeTest {

    @Test
    void shouldExtractConstraintCustomFromConstraintTypeCustom() {
        final var constraintType = "constraintType";
        final var constraintValue = "constraintValue";

        final var expectedConstraintCustom = new ConstraintCustom(constraintType, constraintValue);
        final var constraintTypeCustom = new ConstraintTypeCustom(expectedConstraintCustom);

        assertThat(constraintTypeCustom.getConstraintType()).isEqualTo(expectedConstraintCustom);
    }

    @Test
    void shouldExtractConstraintEndPointLocationFromConstraintTypeEndPointLocation() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";
        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var locationType = new LocationTypeRegion("ATH");
        final var location = new Location(locationType);

        final var expectedConstraintEndPointLocation =
                new ConstraintEndPointLocation(endPointId, location);
        final var constraintTypeEndPointLocation =
                new ConstraintTypeEndPointLocation(expectedConstraintEndPointLocation);

        assertThat(constraintTypeEndPointLocation.getConstraintType())
                .isEqualTo(expectedConstraintEndPointLocation);
    }

    @Test
    void shouldExtractConstraintScheduleFromConstraintTypeSchedule() {
        final var startTimestamp = 4.7f;
        final var durationDays = 97.4f;

        final var expectedConstraintSchedule = new ConstraintSchedule(startTimestamp, durationDays);
        final var constraintTypeSchedule = new ConstraintTypeSchedule(expectedConstraintSchedule);

        assertThat(constraintTypeSchedule.getConstraintType()).isEqualTo(expectedConstraintSchedule);
    }

    @Test
    void shouldExtractConstraintSlaAvailabilityFromConstraintTypeSlaAvailability() {
        final var numDisjointPaths = 88;
        final var allActive = false;

        final var expectedConstraintSlaAvailability =
                new ConstraintSlaAvailability(numDisjointPaths, allActive);
        final var constraintTypeSlaAvailability =
                new ConstraintTypeSlaAvailability(expectedConstraintSlaAvailability);

        assertThat(constraintTypeSlaAvailability.getConstraintType())
                .isEqualTo(expectedConstraintSlaAvailability);
    }

    @Test
    void shouldExtractConstraintSlaCapacityFromConstraintTypeSlaCapacity() {
        final var capacityGbps = 0.2f;

        final var expectedConstraintSlaCapacity = new ConstraintSlaCapacity(capacityGbps);
        final var constraintTypeSlaCapacity =
                new ConstraintTypeSlaCapacity(expectedConstraintSlaCapacity);

        assertThat(constraintTypeSlaCapacity.getConstraintType())
                .isEqualTo(expectedConstraintSlaCapacity);
    }

    @Test
    void shouldExtractConstraintSlaIsolationLevelFromConstraintTypeSlaIsolationLevel() {
        final var expectedConstraintSlaIsolationLevel =
                new ConstraintSlaIsolationLevel(
                        List.of(IsolationLevelEnum.PHYSICAL_ISOLATION, IsolationLevelEnum.LOGICAL_ISOLATION));
        final var constraintTypeSlaIsolationLevel =
                new ConstraintTypeSlaIsolationLevel(expectedConstraintSlaIsolationLevel);

        assertThat(constraintTypeSlaIsolationLevel.getConstraintType())
                .isEqualTo(expectedConstraintSlaIsolationLevel);
    }

    @Test
    void shouldExtractConstraintSlaLatencyFromConstraintTypeSlaLatency() {
        final var capacityGbps = 0.2f;

        final var expectedConstraintSlaLatency = new ConstraintSlaLatency(capacityGbps);
        final var constraintTypeSlaLatency = new ConstraintTypeSlaLatency(expectedConstraintSlaLatency);

        assertThat(constraintTypeSlaLatency.getConstraintType())
                .isEqualTo(expectedConstraintSlaLatency);
    }
}
