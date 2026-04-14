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
import org.etsi.tfs.policy.context.model.GpsPosition;
import org.etsi.tfs.policy.context.model.LocationTypeGpsPosition;
import org.etsi.tfs.policy.context.model.LocationTypeRegion;
import org.junit.jupiter.api.Test;

@QuarkusTest
class LocationTypeTest {

    @Test
    void shouldExtractRegionFromLocationTypeRegion() {
        final var expectedRegion = "ATH";

        final var locationTypeRegion = new LocationTypeRegion(expectedRegion);

        assertThat(locationTypeRegion.getLocationType()).isEqualTo(expectedRegion);
    }

    @Test
    void shouldExtractLocationGpsPositionFromLocationTypeGpsPosition() {
        final var latitude = 3.99f;
        final var longitude = 77.32f;

        final var expectedLocationGpsPosition = new GpsPosition(latitude, longitude);
        final var locationTypeGpsPosition = new LocationTypeGpsPosition(expectedLocationGpsPosition);

        assertThat(locationTypeGpsPosition.getLocationType()).isEqualTo(expectedLocationGpsPosition);
    }
}
