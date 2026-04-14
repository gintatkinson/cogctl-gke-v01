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

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import context.ContextOuterClass;
import io.quarkus.test.junit.QuarkusTest;
import io.quarkus.test.junit.mockito.InjectMock;
import io.smallrye.mutiny.Uni;
import jakarta.inject.Inject;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.assertj.core.api.Assertions;
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
import org.jboss.logging.Logger;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import ztp.Ztp;

@QuarkusTest
class ZtpFunctionalServiceTest {
    private static final Logger LOGGER = Logger.getLogger(ZtpFunctionalServiceTest.class);

    @Inject ZtpService ztpService;

    @InjectMock DeviceGateway deviceGateway;
    @InjectMock ContextGateway contextGateway;

    @Test
    void shouldConfigureDevice() {
        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("0f14d0ab-9608-7862-a9e4-5ed26688389b").toString())
                        .build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("9f14d0ab-9608-7862-a9e4-5ed26688389c").toString())
                        .build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevRoleId().toString();
        String deviceName = "deviceName";
        String deviceType = "cisco";

        final var configRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var configRuleTypeA = new ConfigRuleTypeCustom(configRuleCustomA);
        ConfigRule configRule1 = new ConfigRule(ConfigActionEnum.UNDEFINED, configRuleTypeA);

        final var configRuleCustomB = new ConfigRuleCustom("resourceKeyB", "resourceValueB");
        final var configRuleTypeB = new ConfigRuleTypeCustom(configRuleCustomB);
        ConfigRule configRule2 = new ConfigRule(ConfigActionEnum.SET, configRuleTypeB);

        List<ConfigRule> configRuleList = new ArrayList<>();
        configRuleList.add(configRule1);
        configRuleList.add(configRule2);

        DeviceConfig expectedDeviceConfig = new DeviceConfig(configRuleList);
        Uni<DeviceConfig> expectedDeviceConfigUni = Uni.createFrom().item(expectedDeviceConfig);
        Uni<String> expectedDeviceId = Uni.createFrom().item(deviceId);

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

        Device device =
                new Device(
                        deviceId,
                        deviceName,
                        deviceType,
                        DeviceOperationalStatus.DISABLED,
                        deviceDrivers,
                        endPoints);
        Uni<Device> deviceUni = Uni.createFrom().item(device);

        Mockito.when(contextGateway.getDevice(Mockito.any())).thenReturn(deviceUni);
        Mockito.when(deviceGateway.getInitialConfiguration(Mockito.any()))
                .thenReturn(expectedDeviceConfigUni);
        Mockito.when(deviceGateway.configureDevice(Mockito.any())).thenReturn(expectedDeviceId);

        final var currentDevice = ztpService.addDevice(deviceId);

        Assertions.assertThat(currentDevice).isNotNull();
        currentDevice
                .subscribe()
                .with(
                        deviceConfig -> {
                            LOGGER.infof("Received response %s", deviceConfig);

                            assertThat(deviceConfig).hasToString(device.getDeviceOperationalStatus().toString());

                            assertThat(deviceConfig.getDeviceConfig().toString()).isNotNull();

                            final var rulesList = deviceConfig.getDeviceConfig().getConfigRules();

                            for (int i = 0; i < rulesList.size(); i++) {

                                if (rulesList.get(i).getConfigRuleType().getConfigRuleType()
                                        instanceof ConfigRuleCustom) {
                                    assertThat(
                                                    ((ConfigRuleCustom)
                                                                    rulesList.get(i).getConfigRuleType().getConfigRuleType())
                                                            .getResourceKey())
                                            .isEqualTo(String.valueOf(i + 1));
                                    assertThat(
                                                    ((ConfigRuleCustom)
                                                                    rulesList.get(i).getConfigRuleType().getConfigRuleType())
                                                            .getResourceValue())
                                            .isEqualTo(String.valueOf(i + 1));
                                }
                            }
                            assertThat(deviceConfig.getDeviceType()).isEqualTo("cisco");
                            assertThat(deviceConfig.getDeviceId()).isEqualTo(deviceId);
                        });
    }

    @Test
    void shouldNotConfigureDevice() {

        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("2f14d0ab-9608-7862-a9e4-5ed26688389f").toString())
                        .build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("3f14d0ab-9608-7862-a9e4-5ed26688389d").toString())
                        .build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevId().toString();
        String deviceName = "deviceName";
        String deviceType = "ztp";

        List<ConfigRule> configRuleList = new ArrayList<>();

        final var configRuleCustom = new ConfigRuleCustom("resourceKey", "resourceValue");
        final var configRuleType = new ConfigRuleTypeCustom(configRuleCustom);

        ConfigRule expectedConfigRule = new ConfigRule(ConfigActionEnum.UNDEFINED, configRuleType);
        configRuleList.add(expectedConfigRule);

        DeviceConfig expectedDeviceConfig = new DeviceConfig(configRuleList);

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

        Device device =
                new Device(
                        deviceId,
                        deviceName,
                        deviceType,
                        expectedDeviceConfig,
                        DeviceOperationalStatus.ENABLED,
                        deviceDrivers,
                        endPoints);

        Uni<Device> deviceUni = Uni.createFrom().item(device);

        Mockito.when(contextGateway.getDevice(Mockito.any())).thenReturn(deviceUni);

        final var currentDevice = ztpService.addDevice(deviceId);

        Assertions.assertThat(currentDevice).isNotNull();

        currentDevice
                .subscribe()
                .with(
                        deviceConfig -> {
                            LOGGER.infof("Received response %s", deviceConfig);

                            assertThat(deviceConfig).hasToString(device.getDeviceOperationalStatus().toString());

                            assertThat(deviceConfig.getDeviceConfig().toString()).isNotNull();

                            final var rulesList = deviceConfig.getDeviceConfig().getConfigRules();

                            for (ConfigRule configRule : rulesList) {
                                if (configRule.getConfigRuleType().getConfigRuleType()
                                        instanceof ConfigRuleCustom) {

                                    if (expectedConfigRule.getConfigRuleType().getConfigRuleType()
                                            instanceof ConfigRuleCustom) {
                                        assertThat(
                                                        ((ConfigRuleCustom) configRule.getConfigRuleType().getConfigRuleType())
                                                                .getResourceKey())
                                                .isEqualTo(
                                                        ((ConfigRuleCustom)
                                                                        expectedConfigRule.getConfigRuleType().getConfigRuleType())
                                                                .getResourceKey());
                                        assertThat(
                                                        ((ConfigRuleCustom) configRule.getConfigRuleType().getConfigRuleType())
                                                                .getResourceValue())
                                                .isEqualTo(
                                                        ((ConfigRuleCustom)
                                                                        expectedConfigRule.getConfigRuleType().getConfigRuleType())
                                                                .getResourceValue());
                                    }
                                }
                            }
                            assertThat(deviceConfig.getDeviceType()).isEqualTo("ztp");
                            assertThat(deviceConfig.getDeviceId()).isEqualTo(deviceId);
                        });
    }

    @Test
    void shouldDeleteDevice() {
        final var uuidForDeviceRoleId =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("0f14d0ab-9608-7862-a9e4-5ed26688389b").toString())
                        .build();

        final var uuidForDeviceId =
                ContextOuterClass.Uuid.newBuilder()
                        .setUuid(UUID.fromString("9f14d0ab-9608-7862-a9e4-5ed26688389c").toString())
                        .build();

        final var outDeviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(uuidForDeviceId).build();

        final var outDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(uuidForDeviceRoleId)
                        .setDevId(outDeviceId)
                        .build();

        String deviceId = outDeviceRoleId.getDevRoleId().toString();
        String deviceName = "deviceName";
        String deviceType = "cisco";

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

        Device device =
                new Device(
                        deviceId,
                        deviceName,
                        deviceType,
                        DeviceOperationalStatus.DISABLED,
                        deviceDrivers,
                        endPoints);
        Uni<Device> deviceUni = Uni.createFrom().item(device);

        Mockito.when(contextGateway.getDevice(Mockito.any())).thenReturn(deviceUni);

        final var deletedDevice = ztpService.deleteDevice(deviceId);

        Assertions.assertThat(deletedDevice).isNotNull();

        deletedDevice
                .subscribe()
                .with(
                        removedDevice -> {
                            assertThat(removedDevice).isEqualTo(deletedDevice);
                        });
    }
}
