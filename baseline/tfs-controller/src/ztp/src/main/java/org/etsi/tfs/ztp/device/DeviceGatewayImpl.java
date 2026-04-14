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

import device.DeviceService;
import io.quarkus.grpc.GrpcClient;
import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import org.etsi.tfs.ztp.Serializer;
import org.etsi.tfs.ztp.context.model.Device;
import org.etsi.tfs.ztp.context.model.DeviceConfig;
import org.etsi.tfs.ztp.context.model.Empty;

@ApplicationScoped
public class DeviceGatewayImpl implements DeviceGateway {

    @GrpcClient("device")
    DeviceService deviceDelegate;

    private final Serializer serializer;

    @Inject
    public DeviceGatewayImpl(Serializer serializer) {
        this.serializer = serializer;
    }

    @Override
    public Uni<DeviceConfig> getInitialConfiguration(String deviceId) {
        final var serializedDeviceId = serializer.serializeDeviceId(deviceId);

        return deviceDelegate
                .getInitialConfig(serializedDeviceId)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<String> configureDevice(Device device) {
        final var serializedDevice = serializer.serialize(device);

        return deviceDelegate
                .configureDevice(serializedDevice)
                .onItem()
                .transform(serializer::deserialize);
    }

    @Override
    public Uni<Empty> deleteDevice(String deviceId) {
        final var serializedDeviceId = serializer.serializeDeviceId(deviceId);

        return deviceDelegate
                .deleteDevice(serializedDeviceId)
                .onItem()
                .transform(serializer::deserializeEmpty);
    }
}
