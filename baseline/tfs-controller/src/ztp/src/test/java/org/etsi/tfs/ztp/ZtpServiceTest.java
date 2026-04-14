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

import static org.assertj.core.api.Assertions.assertThat;

import context.ContextOuterClass;
import io.quarkus.grpc.GrpcClient;
import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.junit.mockito.InjectMock;
import io.smallrye.mutiny.Uni;
import jakarta.inject.Inject;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import org.etsi.tfs.ztp.context.ContextGateway;
import org.etsi.tfs.ztp.context.model.ConfigActionEnum;
import org.etsi.tfs.ztp.context.model.ConfigRule;
import org.etsi.tfs.ztp.context.model.ConfigRuleCustom;
import org.etsi.tfs.ztp.context.model.ConfigRuleTypeCustom;
import org.etsi.tfs.ztp.context.model.Device;
import org.etsi.tfs.ztp.context.model.DeviceConfig;
import org.etsi.tfs.ztp.context.model.DeviceDriverEnum;
import org.etsi.tfs.ztp.context.model.DeviceOperationalStatus;
import org.etsi.tfs.ztp.context.model.EndPoint.EndPointBuilder;
import org.etsi.tfs.ztp.context.model.EndPointId;
import org.etsi.tfs.ztp.context.model.Location;
import org.etsi.tfs.ztp.context.model.LocationTypeRegion;
import org.etsi.tfs.ztp.context.model.TopologyId;
import org.etsi.tfs.ztp.device.DeviceGateway;
import org.etsi.tfs.ztp.kpi_sample_types.model.KpiSampleType;
import org.etsi.tfs.ztp.model.DeviceRole;
import org.etsi.tfs.ztp.model.DeviceRoleConfig;
import org.etsi.tfs.ztp.model.DeviceRoleId;
import org.etsi.tfs.ztp.model.DeviceRoleType;
import org.jboss.logging.Logger;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import ztp.Ztp;
import ztp.ZtpService;

@QuarkusTest
class ZtpServiceTest {
    private static final Logger LOGGER = Logger.getLogger(ZtpServiceTest.class);

    @GrpcClient ZtpService client;
    private final Serializer serializer;

    @InjectMock DeviceGateway deviceGateway;
    @InjectMock ContextGateway contextGateway;

    @Inject
    ZtpServiceTest(Serializer serializer) {
        this.serializer = serializer;
    }

    @Test
    void shouldAddDeviceRole() throws ExecutionException, InterruptedException, TimeoutException {
        final var message = new CompletableFuture<>();
        final var DEVICE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389b";
        final var DEVICE_ROLE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389a";
        final var DEVICE_NAME = "deviceNameA";
        final var DEVICE_TYPE = "ztp";

        final var deviceDrivers = List.of(DeviceDriverEnum.IETF_NETWORK_TOPOLOGY, DeviceDriverEnum.P4);

        final var topologyIdA = new TopologyId("contextIdA", "idA");
        final var deviceIdA = "deviceIdA";
        final var idA = "idA";
        final var endPointIdA = new EndPointId(topologyIdA, deviceIdA, idA);

        final var endPointTypeA = "endPointTypeA";
        final var kpiSampleTypesA =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionA = new LocationTypeRegion("ATH");
        final var locationA = new Location(locationTypeRegionA);
        final var endPointA =
                new EndPointBuilder(endPointIdA, endPointTypeA, kpiSampleTypesA)
                        .location(locationA)
                        .build();

        final var topologyIdB = new TopologyId("contextIdB", "idB");
        final var deviceIdB = "deviceIdB";
        final var idB = "idB";
        final var endPointIdB = new EndPointId(topologyIdB, deviceIdB, idB);
        final var endPointTypeB = "endPointTypeB";
        final var kpiSampleTypesB =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionB = new LocationTypeRegion("ATH");
        final var locationB = new Location(locationTypeRegionB);
        final var endPointB =
                new EndPointBuilder(endPointIdB, endPointTypeB, kpiSampleTypesB)
                        .location(locationB)
                        .build();

        final var endPoints = List.of(endPointA, endPointB);

        final var emptyDeviceConfig = new DeviceConfig(List.of());
        final var disabledDevice =
                new Device(
                        DEVICE_ID,
                        DEVICE_NAME,
                        DEVICE_TYPE,
                        emptyDeviceConfig,
                        DeviceOperationalStatus.DISABLED,
                        deviceDrivers,
                        endPoints);
        Mockito.when(contextGateway.getDevice(Mockito.any()))
                .thenReturn(Uni.createFrom().item(disabledDevice));

        final var configRuleCustom = new ConfigRuleCustom("resourceKey", "resourceValue");
        final var configRuleType = new ConfigRuleTypeCustom(configRuleCustom);
        final var configRule = new ConfigRule(ConfigActionEnum.SET, configRuleType);
        final var initialDeviceConfig = new DeviceConfig(List.of(configRule));
        Mockito.when(deviceGateway.getInitialConfiguration(Mockito.any()))
                .thenReturn(Uni.createFrom().item(initialDeviceConfig));

        Mockito.when(deviceGateway.configureDevice(Mockito.any()))
                .thenReturn(Uni.createFrom().item(DEVICE_ID));

        final var deviceRoleId = new DeviceRoleId(DEVICE_ROLE_ID, DEVICE_ID);
        final var deviceRoleType = DeviceRoleType.DEV_OPS;
        final var deviceRole = new DeviceRole(deviceRoleId, deviceRoleType);
        final var serializedDeviceRole = serializer.serialize(deviceRole);

        client
                .ztpAdd(serializedDeviceRole)
                .subscribe()
                .with(
                        deviceRoleState -> {
                            LOGGER.infof("Received %s", deviceRoleState);
                            final var devRoleId = deviceRoleState.getDevRoleId();

                            final var deviceRoleIdUuid = serializer.deserialize(devRoleId);

                            assertThat(deviceRoleIdUuid.getId()).isEqualTo(DEVICE_ROLE_ID);

                            final var deviceId = serializer.deserialize(devRoleId.getDevId());
                            assertThat(deviceId).isEqualTo(DEVICE_ID);

                            final var devRoleUuid = serializer.deserialize(devRoleId.getDevRoleId());
                            message.complete(devRoleUuid);
                        });
        assertThat(message.get(5, TimeUnit.SECONDS)).isEqualTo(DEVICE_ROLE_ID);
    }

    @Test
    void shouldUpdateDeviceRole() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();

        final var DEVICE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389b";
        final var DEVICE_ROLE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389a";
        final var DEVICE_NAME = "deviceNameA";
        final var DEVICE_TYPE = "ztp";

        final var deviceDrivers = List.of(DeviceDriverEnum.IETF_NETWORK_TOPOLOGY, DeviceDriverEnum.P4);

        final var topologyIdA = new TopologyId("contextIdA", "idA");
        final var deviceIdA = "deviceIdA";
        final var idA = "idA";
        final var endPointIdA = new EndPointId(topologyIdA, deviceIdA, idA);

        final var endPointTypeA = "endPointTypeA";
        final var kpiSampleTypesA =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionA = new LocationTypeRegion("ATH");
        final var locationA = new Location(locationTypeRegionA);
        final var endPointA =
                new EndPointBuilder(endPointIdA, endPointTypeA, kpiSampleTypesA)
                        .location(locationA)
                        .build();

        final var topologyIdB = new TopologyId("contextIdB", "idB");
        final var deviceIdB = "deviceIdB";
        final var idB = "idB";
        final var endPointIdB = new EndPointId(topologyIdB, deviceIdB, idB);
        final var endPointTypeB = "endPointTypeB";
        final var kpiSampleTypesB =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionB = new LocationTypeRegion("ATH");
        final var locationB = new Location(locationTypeRegionB);
        final var endPointB =
                new EndPointBuilder(endPointIdB, endPointTypeB, kpiSampleTypesB)
                        .location(locationB)
                        .build();

        final var endPoints = List.of(endPointA, endPointB);

        final var emptyDeviceConfig = new DeviceConfig(List.of());
        final var device =
                new Device(
                        DEVICE_ID,
                        DEVICE_NAME,
                        DEVICE_TYPE,
                        emptyDeviceConfig,
                        DeviceOperationalStatus.ENABLED,
                        deviceDrivers,
                        endPoints);
        Mockito.when(contextGateway.getDevice(Mockito.any())).thenReturn(Uni.createFrom().item(device));

        final var deviceRoleId = new DeviceRoleId(DEVICE_ROLE_ID, DEVICE_ID);
        final var deviceRole = new DeviceRole(deviceRoleId, DeviceRoleType.DEV_OPS);

        final var configRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var configRuleTypeA = new ConfigRuleTypeCustom(configRuleCustomA);
        final var deviceConfig =
                new DeviceConfig(List.of(new ConfigRule(ConfigActionEnum.SET, configRuleTypeA)));

        final var deviceRoleConfig = new DeviceRoleConfig(deviceRole, deviceConfig);
        final var serializedDeviceRoleConfig = serializer.serialize(deviceRoleConfig);

        client
                .ztpUpdate(serializedDeviceRoleConfig)
                .subscribe()
                .with(
                        deviceRoleState -> {
                            LOGGER.infof("Received response %s", deviceRoleState);
                            message.complete(deviceRoleState.getDevRoleId().toString());
                        });
        assertThat(message.get(5, TimeUnit.SECONDS)).contains(DEVICE_ID);
    }

    @Test
    void shouldGetDeviceRole() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();
        final var DEVICE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389b";
        final var DEVICE_ROLE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389a";

        final var deviceRoleId = new DeviceRoleId(DEVICE_ROLE_ID, DEVICE_ID);
        final var serializeDeviceRoleId = serializer.serialize(deviceRoleId);

        client
                .ztpGetDeviceRole(serializeDeviceRoleId)
                .subscribe()
                .with(
                        deviceRole -> {
                            LOGGER.infof("Received response %s", deviceRole);
                            assertThat(deviceRole.getDevRoleId().getDevId().getDeviceUuid().getUuid())
                                    .isEqualTo(DEVICE_ID);
                            message.complete(deviceRole.getDevRoleId().toString());
                        });
        assertThat(message.get(5, TimeUnit.SECONDS)).contains(DEVICE_ROLE_ID);
    }

    @Test
    void shouldGetAllDeviceRolesByDeviceId()
            throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();

        final var deviceId = serializer.serializeDeviceId("0f14d0ab-9605-7862-a9e4-5ed26688389b");

        client
                .ztpGetDeviceRolesByDeviceId(deviceId)
                .subscribe()
                .with(
                        deviceRoleList -> {
                            LOGGER.infof("Received response %s", deviceRoleList);
                            message.complete(deviceRoleList.toString());
                        });
        assertThat(message.get(5, TimeUnit.SECONDS)).isEmpty();
    }

    @Test
    void shouldDeleteDeviceRole() throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();
        final var UUID_VALUE = "0f14d0ab-9605-7862-a9e4-5ed26688389b";

        final var uuid = serializer.serializeUuid(UUID_VALUE);
        final var deviceRoleId = Ztp.DeviceRoleId.newBuilder().setDevRoleId(uuid).build();
        final var deviceRole = Ztp.DeviceRole.newBuilder().setDevRoleId(deviceRoleId).build();
        final var DEVICE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389b";
        final var DEVICE_ROLE_ID = "0f14d0ab-9608-7862-a9e4-5ed26688389a";
        final var DEVICE_NAME = "deviceNameA";
        final var DEVICE_TYPE = "ztp";

        final var deviceDrivers = List.of(DeviceDriverEnum.IETF_NETWORK_TOPOLOGY, DeviceDriverEnum.P4);

        final var topologyIdA = new TopologyId("contextIdA", "idA");
        final var deviceIdA = "deviceIdA";
        final var idA = "idA";
        final var endPointIdA = new EndPointId(topologyIdA, deviceIdA, idA);

        final var endPointTypeA = "endPointTypeA";
        final var kpiSampleTypesA =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionA = new LocationTypeRegion("ATH");
        final var locationA = new Location(locationTypeRegionA);
        final var endPointA =
                new EndPointBuilder(endPointIdA, endPointTypeA, kpiSampleTypesA)
                        .location(locationA)
                        .build();

        final var topologyIdB = new TopologyId("contextIdB", "idB");
        final var deviceIdB = "deviceIdB";
        final var idB = "idB";
        final var endPointIdB = new EndPointId(topologyIdB, deviceIdB, idB);
        final var endPointTypeB = "endPointTypeB";
        final var kpiSampleTypesB =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionB = new LocationTypeRegion("ATH");
        final var locationB = new Location(locationTypeRegionB);
        final var endPointB =
                new EndPointBuilder(endPointIdB, endPointTypeB, kpiSampleTypesB)
                        .location(locationB)
                        .build();

        final var endPoints = List.of(endPointA, endPointB);

        final var emptyDeviceConfig = new DeviceConfig(List.of());
        final var device =
                new Device(
                        DEVICE_ID,
                        DEVICE_NAME,
                        DEVICE_TYPE,
                        emptyDeviceConfig,
                        DeviceOperationalStatus.ENABLED,
                        deviceDrivers,
                        endPoints);
        Mockito.when(contextGateway.getDevice(Mockito.any())).thenReturn(Uni.createFrom().item(device));

        client
                .ztpDelete(deviceRole)
                .subscribe()
                .with(
                        deviceRoleState -> {
                            LOGGER.infof("Received response %s", deviceRoleState);
                            message.complete(deviceRoleState.getDevRoleId().toString());
                        });
        assertThat(message.get(5, TimeUnit.SECONDS)).contains(UUID_VALUE);
    }

    @Test
    void shouldDeleteAllDevicesRolesByDeviceId()
            throws ExecutionException, InterruptedException, TimeoutException {
        CompletableFuture<String> message = new CompletableFuture<>();
        final var empty = ContextOuterClass.Empty.newBuilder().build();

        client
                .ztpDeleteAll(empty)
                .subscribe()
                .with(
                        deletionResult -> {
                            LOGGER.infof("Received response %s", deletionResult);
                            message.complete(deletionResult.toString());
                        });
        assertThat(message.get(5, TimeUnit.SECONDS)).isEmpty();
    }
}
