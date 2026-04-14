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

package org.etsi.tfs.policy.device;

import io.smallrye.mutiny.Uni;
import org.etsi.tfs.policy.context.model.Device;
import org.etsi.tfs.policy.context.model.DeviceConfig;
import org.etsi.tfs.policy.context.model.Empty;

public interface DeviceGateway {
    Uni<DeviceConfig> getInitialConfiguration(String deviceId);

    Uni<String> configureDevice(Device device);

    Uni<Empty> deleteDevice(String deviceId);
}
