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

package org.etsi.tfs.ztp.device;

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.ztp.context.model.Device;
import org.etsi.tfs.ztp.context.model.DeviceConfig;
import org.etsi.tfs.ztp.context.model.Empty;

@ApplicationScoped
public class DeviceServiceImpl implements DeviceService {

    private final DeviceGateway deviceGateway;

    @Inject
    public DeviceServiceImpl(DeviceGateway deviceGateway) {
        this.deviceGateway = deviceGateway;
    }

    @Override
    public Uni<DeviceConfig> getInitialConfiguration(String deviceId) {

        return deviceGateway.getInitialConfiguration(deviceId);
    }

    @Override
    public Uni<String> configureDevice(Device device) {

        return deviceGateway.configureDevice(device);
    }

    @Override
    public Uni<Empty> deleteDevice(String deviceId) {
        return deviceGateway.deleteDevice(deviceId);
    }
}
