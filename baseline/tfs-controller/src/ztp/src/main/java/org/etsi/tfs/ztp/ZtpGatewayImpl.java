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

package org.etsi.tfs.ztp;

import context.ContextOuterClass;
import io.quarkus.grpc.GrpcService;
import io.smallrye.mutiny.Uni;
import jakarta.inject.Inject;
import org.eclipse.microprofile.metrics.MetricUnits;
import org.eclipse.microprofile.metrics.annotation.Counted;
import org.eclipse.microprofile.metrics.annotation.Timed;
import org.etsi.tfs.ztp.context.model.Device;
import org.etsi.tfs.ztp.model.DeviceRoleId;
import org.etsi.tfs.ztp.model.DeviceState;
import ztp.Ztp;
import ztp.Ztp.DeviceRoleConfig;
import ztp.Ztp.DeviceRoleState;

@GrpcService
public class ZtpGatewayImpl implements ZtpGateway {

    private final ZtpService ztpService;
    private final Serializer serializer;

    @Inject
    public ZtpGatewayImpl(ZtpService ztpService, Serializer serializer) {
        this.ztpService = ztpService;
        this.serializer = serializer;
    }

    @Override
    @Counted(name = "ztp_ztpGetDeviceRole_counter")
    @Timed(name = "ztp_ztpGetDeviceRole_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<Ztp.DeviceRole> ztpGetDeviceRole(Ztp.DeviceRoleId request) {
        return Uni.createFrom().item(() -> Ztp.DeviceRole.newBuilder().setDevRoleId(request).build());
    }

    @Override
    @Counted(name = "ztp_ztpGetDeviceRolesByDeviceId_counter")
    @Timed(name = "ztp_ztpGetDeviceRolesByDeviceId_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<Ztp.DeviceRoleList> ztpGetDeviceRolesByDeviceId(ContextOuterClass.DeviceId request) {
        return Uni.createFrom().item(() -> Ztp.DeviceRoleList.newBuilder().build());
    }

    @Override
    @Counted(name = "ztp_ztpAdd_counter")
    @Timed(name = "ztp_ztpAdd_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<Ztp.DeviceRoleState> ztpAdd(Ztp.DeviceRole request) {
        final var devRoleId = request.getDevRoleId().getDevRoleId().getUuid();
        final var deviceId = serializer.deserialize(request.getDevRoleId().getDevId());

        return ztpService
                .addDevice(deviceId)
                .onItem()
                .transform(device -> transformToDeviceRoleState(device, devRoleId, DeviceState.CREATED));
    }

    @Override
    @Counted(name = "ztp_ztpUpdate_counter")
    @Timed(name = "ztp_ztpUpdate_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<DeviceRoleState> ztpUpdate(DeviceRoleConfig request) {
        final var devRoleId = request.getDevRole().getDevRoleId().getDevRoleId().getUuid();
        final var deviceId = serializer.deserialize(request.getDevRole().getDevRoleId().getDevId());
        final var deviceConfig = serializer.deserialize(request.getDevConfig());

        return ztpService
                .updateDevice(deviceId, deviceConfig)
                .onItem()
                .transform(device -> transformToDeviceRoleState(device, devRoleId, DeviceState.UPDATED));
    }

    @Override
    @Counted(name = "ztp_ztpDelete_counter")
    @Timed(name = "ztp_ztpDelete_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<Ztp.DeviceRoleState> ztpDelete(Ztp.DeviceRole request) {
        final var devRoleId = request.getDevRoleId().getDevRoleId().getUuid();
        return ztpService
                .deleteDevice(devRoleId)
                .onItem()
                .transform(device -> transformToDeviceRoleState(device, devRoleId, DeviceState.DELETED));
    }

    @Override
    @Counted(name = "ztp_ztpDeleteAll_counter")
    @Timed(name = "ztp_ztpDeleteAll_histogram", unit = MetricUnits.MILLISECONDS)
    public Uni<Ztp.DeviceDeletionResult> ztpDeleteAll(ContextOuterClass.Empty empty) {
        return Uni.createFrom().item(() -> Ztp.DeviceDeletionResult.newBuilder().build());
    }

    private Ztp.DeviceRoleState transformToDeviceRoleState(
            Device device, String devRoleId, DeviceState deviceState) {
        final var deviceRoleId = new DeviceRoleId(devRoleId, device.getDeviceId());
        final var serializeDeviceRoleId = serializer.serialize(deviceRoleId);
        final var serializedDeviceState = serializer.serialize(deviceState);

        return Ztp.DeviceRoleState.newBuilder()
                .setDevRoleId(serializeDeviceRoleId)
                .setDevRoleState(serializedDeviceState)
                .build();
    }
}
