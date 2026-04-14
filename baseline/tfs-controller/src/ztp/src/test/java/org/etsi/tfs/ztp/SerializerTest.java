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
import static org.assertj.core.api.Assertions.assertThatExceptionOfType;

import acl.Acl;
import context.ContextOuterClass;
import context.ContextOuterClass.DeviceId;
import context.ContextOuterClass.DeviceOperationalStatusEnum;
import context.ContextOuterClass.Uuid;
import io.quarkus.test.junit.QuarkusTest;
import jakarta.inject.Inject;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import kpi_sample_types.KpiSampleTypes;
import org.etsi.tfs.ztp.acl.AclAction;
import org.etsi.tfs.ztp.acl.AclEntry;
import org.etsi.tfs.ztp.acl.AclForwardActionEnum;
import org.etsi.tfs.ztp.acl.AclLogActionEnum;
import org.etsi.tfs.ztp.acl.AclMatch;
import org.etsi.tfs.ztp.acl.AclRuleSet;
import org.etsi.tfs.ztp.acl.AclRuleTypeEnum;
import org.etsi.tfs.ztp.context.model.ConfigActionEnum;
import org.etsi.tfs.ztp.context.model.ConfigRule;
import org.etsi.tfs.ztp.context.model.ConfigRuleAcl;
import org.etsi.tfs.ztp.context.model.ConfigRuleCustom;
import org.etsi.tfs.ztp.context.model.ConfigRuleTypeAcl;
import org.etsi.tfs.ztp.context.model.ConfigRuleTypeCustom;
import org.etsi.tfs.ztp.context.model.Device;
import org.etsi.tfs.ztp.context.model.DeviceConfig;
import org.etsi.tfs.ztp.context.model.DeviceDriverEnum;
import org.etsi.tfs.ztp.context.model.DeviceEvent;
import org.etsi.tfs.ztp.context.model.DeviceOperationalStatus;
import org.etsi.tfs.ztp.context.model.Empty;
import org.etsi.tfs.ztp.context.model.EndPoint.EndPointBuilder;
import org.etsi.tfs.ztp.context.model.EndPointId;
import org.etsi.tfs.ztp.context.model.Event;
import org.etsi.tfs.ztp.context.model.EventTypeEnum;
import org.etsi.tfs.ztp.context.model.GpsPosition;
import org.etsi.tfs.ztp.context.model.Location;
import org.etsi.tfs.ztp.context.model.LocationTypeGpsPosition;
import org.etsi.tfs.ztp.context.model.LocationTypeRegion;
import org.etsi.tfs.ztp.context.model.TopologyId;
import org.etsi.tfs.ztp.kpi_sample_types.model.KpiSampleType;
import org.etsi.tfs.ztp.model.DeviceRole;
import org.etsi.tfs.ztp.model.DeviceRoleConfig;
import org.etsi.tfs.ztp.model.DeviceRoleId;
import org.etsi.tfs.ztp.model.DeviceRoleType;
import org.etsi.tfs.ztp.model.DeviceState;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import ztp.Ztp;
import ztp.Ztp.ZtpDeviceState;

@QuarkusTest
class SerializerTest {

    @Inject Serializer serializer;

    private AclMatch createAclMatch(
            int dscp,
            int protocol,
            String srcAddress,
            String dstAddress,
            int srcPort,
            int dstPort,
            int startMplsLabel,
            int endMplsLabel) {
        return new AclMatch(
                dscp, protocol, srcAddress, dstAddress, srcPort, dstPort, startMplsLabel, endMplsLabel);
    }

    private AclAction createAclAction(
            AclForwardActionEnum forwardActionEnum, AclLogActionEnum logActionEnum) {

        return new AclAction(forwardActionEnum, logActionEnum);
    }

    private AclEntry createAclEntry(
            int sequenceId, String description, AclMatch aclMatch, AclAction aclAction) {

        return new AclEntry(sequenceId, description, aclMatch, aclAction);
    }

    @Test
    void shouldSerializeDeviceId() {
        final var expectedDeviceId = "expectedDeviceId";

        final var deviceIdUuid = serializer.serializeUuid(expectedDeviceId);
        final var deviceId =
                ContextOuterClass.DeviceId.newBuilder().setDeviceUuid(deviceIdUuid).build();

        final var serializedDeviceId = serializer.serializeDeviceId(expectedDeviceId);

        assertThat(serializedDeviceId).usingRecursiveComparison().isEqualTo(deviceId);
    }

    @Test
    void shouldDeserializeDeviceId() {
        final var expectedDeviceId = "expectedDeviceId";

        final var serializedDeviceIdUuid = serializer.serializeUuid("expectedDeviceId");
        final var serializedDeviceId =
                DeviceId.newBuilder().setDeviceUuid(serializedDeviceIdUuid).build();

        final var deviceId = serializer.deserialize(serializedDeviceId);

        assertThat(deviceId).isEqualTo(expectedDeviceId);
    }

    @Test
    void shouldSerializeDeviceRoleId() {
        final var expectedDevRoleId = "expectedDevRoleId";
        final var expectedDeviceId = "expectedDeviceId";

        final var deviceRoleId = new DeviceRoleId(expectedDevRoleId, expectedDeviceId);
        final var serializedDeviceRoleIdUuid = serializer.serializeUuid(expectedDevRoleId);
        final var serializedDeviceRoleDeviceIdUuid = serializer.serializeUuid(expectedDeviceId);
        final var serializedDeviceRoleDeviceId =
                ContextOuterClass.DeviceId.newBuilder()
                        .setDeviceUuid(serializedDeviceRoleDeviceIdUuid)
                        .build();

        final var expectedDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(serializedDeviceRoleIdUuid)
                        .setDevId(serializedDeviceRoleDeviceId)
                        .build();

        final var serializedDevRoleId = serializer.serialize(deviceRoleId);

        assertThat(serializedDevRoleId).usingRecursiveComparison().isEqualTo(expectedDeviceRoleId);
    }

    @Test
    void shouldDeserializeDeviceRoleId() {
        final var expectedDevRoleId = "expectedDevRoleId";
        final var expectedDeviceId = "expectedDeviceId";

        final var expectedDeviceRoleId = new DeviceRoleId(expectedDevRoleId, expectedDeviceId);

        final var serializedDeviceRoleId = serializer.serialize(expectedDeviceRoleId);
        final var deviceRoleId = serializer.deserialize(serializedDeviceRoleId);

        assertThat(deviceRoleId).usingRecursiveComparison().isEqualTo(expectedDeviceRoleId);
    }

    private static Stream<Arguments> provideDeviceRoleType() {
        return Stream.of(
                Arguments.of(DeviceRoleType.DEV_OPS, Ztp.DeviceRoleType.DEV_OPS),
                Arguments.of(DeviceRoleType.DEV_CONF, Ztp.DeviceRoleType.DEV_CONF),
                Arguments.of(DeviceRoleType.NONE, Ztp.DeviceRoleType.NONE),
                Arguments.of(DeviceRoleType.PIPELINE_CONF, Ztp.DeviceRoleType.PIPELINE_CONF));
    }

    @ParameterizedTest
    @MethodSource("provideDeviceRoleType")
    void shouldSerializeDeviceRoleType(
            DeviceRoleType deviceRoleType, Ztp.DeviceRoleType expectedSerializedType) {
        final var serializedType = serializer.serialize(deviceRoleType);
        assertThat(serializedType.getNumber()).isEqualTo(expectedSerializedType.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideDeviceRoleType")
    void shouldDeserializeDeviceRoleType(
            DeviceRoleType expectedDeviceRoleType, Ztp.DeviceRoleType serializedDeviceRoleTypeType) {

        final var deviceRoleType = serializer.deserialize(serializedDeviceRoleTypeType);

        assertThat(deviceRoleType).isEqualTo(expectedDeviceRoleType);
    }

    @Test
    void shouldSerializeDeviceRole() {
        final var expectedDevRoleId = "expectedDevRoleId";
        final var expectedDeviceId = "expectedDeviceId";

        final var serializedDeviceRoleDevRoleIdUuid = serializer.serializeUuid(expectedDevRoleId);
        final var serializedDeviceRoleDeviceId = serializer.serializeDeviceId(expectedDeviceId);

        final var expectedDeviceRoleId =
                Ztp.DeviceRoleId.newBuilder()
                        .setDevRoleId(serializedDeviceRoleDevRoleIdUuid)
                        .setDevId(serializedDeviceRoleDeviceId)
                        .build();

        final var expectedDeviceRoleType = Ztp.DeviceRoleType.PIPELINE_CONF;

        final var expectedDeviceRole =
                Ztp.DeviceRole.newBuilder()
                        .setDevRoleId(expectedDeviceRoleId)
                        .setDevRoleType(expectedDeviceRoleType)
                        .build();

        final var deviceRoleId = new DeviceRoleId(expectedDevRoleId, expectedDeviceId);
        final var deviceRoleType = DeviceRoleType.PIPELINE_CONF;

        final var deviceRole = new DeviceRole(deviceRoleId, deviceRoleType);
        final var serializedDeviceRole = serializer.serialize(deviceRole);

        assertThat(serializedDeviceRole).usingRecursiveComparison().isEqualTo(expectedDeviceRole);
    }

    @Test
    void shouldDeserializeDeviceRole() {
        final var expectedDevRoleId = "expectedDevRoleId";
        final var expectedDeviceId = "expectedDeviceId";

        final var expectedDeviceRoleId = new DeviceRoleId(expectedDevRoleId, expectedDeviceId);
        final var expectedDeviceRoleType = DeviceRoleType.NONE;

        final var expectedDeviceRole = new DeviceRole(expectedDeviceRoleId, expectedDeviceRoleType);

        final var serializedDeviceRoleId = serializer.serialize(expectedDeviceRoleId);
        final var serializedDeviceRoleType = serializer.serialize(expectedDeviceRoleType);

        final var serializedDeviceRole =
                Ztp.DeviceRole.newBuilder()
                        .setDevRoleId(serializedDeviceRoleId)
                        .setDevRoleType(serializedDeviceRoleType)
                        .build();

        final var deviceRole = serializer.deserialize(serializedDeviceRole);

        assertThat(deviceRole).usingRecursiveComparison().isEqualTo(expectedDeviceRole);
    }

    @Test
    void shouldSerializeDeviceRoleConfig() {
        final var expectedDevRoleId = new DeviceRoleId("expectedDevRoleId", "expectedDeviceId");
        final var expectedDevRoleType = DeviceRoleType.DEV_OPS;

        final var deviceRole = new DeviceRole(expectedDevRoleId, expectedDevRoleType);
        final var serializedDeviceRole = serializer.serialize(deviceRole);

        final var configRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var configRuleTypeA = new ConfigRuleTypeCustom(configRuleCustomA);
        final var deviceConfig =
                new DeviceConfig(List.of(new ConfigRule(ConfigActionEnum.SET, configRuleTypeA)));
        final var serializedDeviceConfig = serializer.serialize(deviceConfig);

        final var expectedDeviceRoleConfig =
                Ztp.DeviceRoleConfig.newBuilder()
                        .setDevRole(serializedDeviceRole)
                        .setDevConfig(serializedDeviceConfig)
                        .build();

        final var deviceRoleConfig = new DeviceRoleConfig(deviceRole, deviceConfig);
        final var serializedDeviceRoleConfig = serializer.serialize(deviceRoleConfig);

        assertThat(serializedDeviceRoleConfig)
                .usingRecursiveComparison()
                .isEqualTo(expectedDeviceRoleConfig);
    }

    @Test
    void shouldDeserializeDeviceRoleConfig() {
        final var expectedDevRoleId = new DeviceRoleId("expectedDevRoleId", "expectedDeviceId");
        final var expectedDevRoleType = DeviceRoleType.DEV_OPS;

        final var deviceRole = new DeviceRole(expectedDevRoleId, expectedDevRoleType);
        final var serializedDeviceRole = serializer.serialize(deviceRole);

        final var configRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var configRuleTypeA = new ConfigRuleTypeCustom(configRuleCustomA);
        final var deviceConfig =
                new DeviceConfig(List.of(new ConfigRule(ConfigActionEnum.SET, configRuleTypeA)));
        final var serializedDeviceConfig = serializer.serialize(deviceConfig);

        final var expectedDeviceRoleConfig = new DeviceRoleConfig(deviceRole, deviceConfig);

        final var serializedDeviceRoleConfig =
                Ztp.DeviceRoleConfig.newBuilder()
                        .setDevRole(serializedDeviceRole)
                        .setDevConfig(serializedDeviceConfig)
                        .build();

        final var deviceRoleConfig = serializer.deserialize(serializedDeviceRoleConfig);

        assertThat(deviceRoleConfig).usingRecursiveComparison().isEqualTo(expectedDeviceRoleConfig);
    }

    private static Stream<Arguments> provideEventTypeEnum() {
        return Stream.of(
                Arguments.of(EventTypeEnum.CREATE, ContextOuterClass.EventTypeEnum.EVENTTYPE_CREATE),
                Arguments.of(EventTypeEnum.REMOVE, ContextOuterClass.EventTypeEnum.EVENTTYPE_REMOVE),
                Arguments.of(EventTypeEnum.UNDEFINED, ContextOuterClass.EventTypeEnum.EVENTTYPE_UNDEFINED),
                Arguments.of(EventTypeEnum.UPDATE, ContextOuterClass.EventTypeEnum.EVENTTYPE_UPDATE));
    }

    @ParameterizedTest
    @MethodSource("provideEventTypeEnum")
    void shouldSerializeEventType(
            EventTypeEnum eventType, ContextOuterClass.EventTypeEnum expectedSerializedType) {
        final var serializedType = serializer.serialize(eventType);
        assertThat(serializedType.getNumber()).isEqualTo(expectedSerializedType.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideEventTypeEnum")
    void shouldDeserializeEventType(
            EventTypeEnum expectedEventType, ContextOuterClass.EventTypeEnum serializedEventType) {
        final var eventType = serializer.deserialize(serializedEventType);
        assertThat(eventType).isEqualTo(expectedEventType);
    }

    private static Stream<Arguments> provideDeviceState() {
        return Stream.of(
                Arguments.of(DeviceState.CREATED, ZtpDeviceState.ZTP_DEV_STATE_CREATED),
                Arguments.of(DeviceState.UPDATED, ZtpDeviceState.ZTP_DEV_STATE_UPDATED),
                Arguments.of(DeviceState.DELETED, ZtpDeviceState.ZTP_DEV_STATE_DELETED),
                Arguments.of(DeviceState.UNDEFINED, ZtpDeviceState.ZTP_DEV_STATE_UNDEFINED));
    }

    @ParameterizedTest
    @MethodSource("provideDeviceState")
    void shouldSerializeDeviceState(
            DeviceState deviceState, ZtpDeviceState expectedSerializedDeviceState) {
        final var serializedDeviceState = serializer.serialize(deviceState);
        assertThat(serializedDeviceState.getNumber())
                .isEqualTo(expectedSerializedDeviceState.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideDeviceState")
    void shouldDeserializeDeviceState(
            DeviceState expectedDeviceState, ZtpDeviceState serializedDeviceState) {
        final var deviceState = serializer.deserialize(serializedDeviceState);
        assertThat(deviceState).isEqualTo(expectedDeviceState);
    }

    @Test
    void shouldSerializeEvent() {
        final var timestamp = ContextOuterClass.Timestamp.newBuilder().setTimestamp(1).build();

        final var expectedEvent =
                ContextOuterClass.Event.newBuilder()
                        .setTimestamp(timestamp)
                        .setEventType(ContextOuterClass.EventTypeEnum.EVENTTYPE_CREATE)
                        .build();

        final var event = new Event(1, EventTypeEnum.CREATE);
        final var serializedEvent = serializer.serialize(event);

        assertThat(serializedEvent).usingRecursiveComparison().isEqualTo(expectedEvent);
    }

    @Test
    void shouldDeserializeEvent() {
        final var expectedEvent = new Event(1, EventTypeEnum.CREATE);
        final var timestamp = ContextOuterClass.Timestamp.newBuilder().setTimestamp(1).build();

        final var serializedEvent =
                ContextOuterClass.Event.newBuilder()
                        .setTimestamp(timestamp)
                        .setEventType(ContextOuterClass.EventTypeEnum.EVENTTYPE_CREATE)
                        .build();
        final var event = serializer.deserialize(serializedEvent);

        assertThat(event).usingRecursiveComparison().isEqualTo(expectedEvent);
    }

    @Test
    void shouldSerializeDeviceEvent() {
        final var expectedUuid = Uuid.newBuilder().setUuid("deviceId");
        final var expectedDeviceId = DeviceId.newBuilder().setDeviceUuid(expectedUuid).build();
        final var expectedTimestamp = ContextOuterClass.Timestamp.newBuilder().setTimestamp(1).build();

        final var expectedEvent =
                ContextOuterClass.Event.newBuilder()
                        .setTimestamp(expectedTimestamp)
                        .setEventType(ContextOuterClass.EventTypeEnum.EVENTTYPE_CREATE)
                        .build();

        final var expectedConfigRuleCustomA =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyA")
                        .setResourceValue("resourceValueA")
                        .build();

        final var expectedConfigRuleCustomB =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyB")
                        .setResourceValue("resourceValueB")
                        .build();

        final var expectedConfigRuleA =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET)
                        .setCustom(expectedConfigRuleCustomA)
                        .build();
        final var expectedConfigRuleB =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE)
                        .setCustom(expectedConfigRuleCustomB)
                        .build();

        final var expectedDeviceConfig =
                ContextOuterClass.DeviceConfig.newBuilder()
                        .addAllConfigRules(List.of(expectedConfigRuleA, expectedConfigRuleB))
                        .build();

        final var expectedDeviceEvent =
                ContextOuterClass.DeviceEvent.newBuilder()
                        .setDeviceId(expectedDeviceId)
                        .setEvent(expectedEvent)
                        .setDeviceConfig(expectedDeviceConfig)
                        .build();

        final var creationEvent = new Event(1, EventTypeEnum.CREATE);
        final var configRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var configRuleCustomB = new ConfigRuleCustom("resourceKeyB", "resourceValueB");
        final var configRuleTypeA = new ConfigRuleTypeCustom(configRuleCustomA);
        final var configRuleTypeB = new ConfigRuleTypeCustom(configRuleCustomB);
        final var configRuleA = new ConfigRule(ConfigActionEnum.SET, configRuleTypeA);
        final var configRuleB = new ConfigRule(ConfigActionEnum.DELETE, configRuleTypeB);
        final var deviceConfig = new DeviceConfig(List.of(configRuleA, configRuleB));
        final var deviceEvent = new DeviceEvent("deviceId", creationEvent, deviceConfig);
        final var serializedDeviceEvent = serializer.serialize(deviceEvent);

        assertThat(serializedDeviceEvent).usingRecursiveComparison().isEqualTo(expectedDeviceEvent);
    }

    @Test
    void shouldDeserializeDeviceEvent() {
        final var dummyDeviceId = "deviceId";
        final var expectedEventType = EventTypeEnum.REMOVE;
        final var expectedTimestamp = ContextOuterClass.Timestamp.newBuilder().setTimestamp(1).build();

        final var creationEvent = new Event(1, expectedEventType);

        final var expectedConfigRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var expectedConfigRuleCustomB = new ConfigRuleCustom("resourceKeyB", "resourceValueB");

        final var expectedConfigRuleTypeA = new ConfigRuleTypeCustom(expectedConfigRuleCustomA);
        final var expectedConfigRuleTypeB = new ConfigRuleTypeCustom(expectedConfigRuleCustomB);

        final var expectedConfigRuleA = new ConfigRule(ConfigActionEnum.SET, expectedConfigRuleTypeA);
        final var expectedConfigRuleB =
                new ConfigRule(ConfigActionEnum.DELETE, expectedConfigRuleTypeB);

        final var expectedDeviceConfig =
                new DeviceConfig(List.of(expectedConfigRuleA, expectedConfigRuleB));

        final var expectedDeviceEvent =
                new DeviceEvent(dummyDeviceId, creationEvent, expectedDeviceConfig);

        final var deviceUuid = Uuid.newBuilder().setUuid("deviceId");
        final var deviceId = DeviceId.newBuilder().setDeviceUuid(deviceUuid).build();
        final var event =
                ContextOuterClass.Event.newBuilder()
                        .setTimestamp(expectedTimestamp)
                        .setEventType(ContextOuterClass.EventTypeEnum.EVENTTYPE_REMOVE)
                        .build();

        final var configRuleCustomA =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyA")
                        .setResourceValue("resourceValueA")
                        .build();
        final var configRuleCustomB =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyB")
                        .setResourceValue("resourceValueB")
                        .build();
        final var configRuleA =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET)
                        .setCustom(configRuleCustomA)
                        .build();
        final var configRuleB =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE)
                        .setCustom(configRuleCustomB)
                        .build();
        final var deviceConfig =
                ContextOuterClass.DeviceConfig.newBuilder()
                        .addAllConfigRules(List.of(configRuleA, configRuleB))
                        .build();

        final var serializedDeviceEvent =
                ContextOuterClass.DeviceEvent.newBuilder()
                        .setDeviceId(deviceId)
                        .setEvent(event)
                        .setDeviceConfig(deviceConfig)
                        .build();
        final var deviceEvent = serializer.deserialize(serializedDeviceEvent);

        assertThat(deviceEvent).usingRecursiveComparison().isEqualTo(expectedDeviceEvent);
    }

    private static Stream<Arguments> provideConfigActionEnum() {
        return Stream.of(
                Arguments.of(ConfigActionEnum.SET, ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET),
                Arguments.of(
                        ConfigActionEnum.DELETE, ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE),
                Arguments.of(
                        ConfigActionEnum.UNDEFINED, ContextOuterClass.ConfigActionEnum.CONFIGACTION_UNDEFINED));
    }

    @ParameterizedTest
    @MethodSource("provideConfigActionEnum")
    void shouldSerializeConfigActionEnum(
            ConfigActionEnum configAction, ContextOuterClass.ConfigActionEnum expectedConfigAction) {
        final var serializedConfigAction = serializer.serialize(configAction);
        assertThat(serializedConfigAction.getNumber()).isEqualTo(expectedConfigAction.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideConfigActionEnum")
    void shouldDeserializeConfigActionEnum(
            ConfigActionEnum expectedConfigAction,
            ContextOuterClass.ConfigActionEnum serializedConfigAction) {
        final var configAction = serializer.deserialize(serializedConfigAction);
        assertThat(configAction).isEqualTo(expectedConfigAction);
    }

    private static Stream<Arguments> provideAclRuleTypeEnum() {
        return Stream.of(
                Arguments.of(AclRuleTypeEnum.IPV4, Acl.AclRuleTypeEnum.ACLRULETYPE_IPV4),
                Arguments.of(AclRuleTypeEnum.IPV6, Acl.AclRuleTypeEnum.ACLRULETYPE_IPV6),
                Arguments.of(AclRuleTypeEnum.L2, Acl.AclRuleTypeEnum.ACLRULETYPE_L2),
                Arguments.of(AclRuleTypeEnum.MPLS, Acl.AclRuleTypeEnum.ACLRULETYPE_MPLS),
                Arguments.of(AclRuleTypeEnum.MIXED, Acl.AclRuleTypeEnum.ACLRULETYPE_MIXED),
                Arguments.of(AclRuleTypeEnum.UNDEFINED, Acl.AclRuleTypeEnum.ACLRULETYPE_UNDEFINED));
    }

    @ParameterizedTest
    @MethodSource("provideAclRuleTypeEnum")
    void shouldSerializeAclRuleTypeEnum(
            AclRuleTypeEnum aclRuleTypeEnum, Acl.AclRuleTypeEnum expectedAclRuleTypeEnum) {
        final var serializedAclRuleTypeEnum = serializer.serialize(aclRuleTypeEnum);
        assertThat(serializedAclRuleTypeEnum.getNumber())
                .isEqualTo(expectedAclRuleTypeEnum.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideAclRuleTypeEnum")
    void shouldDeserializeAclRuleTypeEnum(
            AclRuleTypeEnum expectedAclRuleTypeEnum, Acl.AclRuleTypeEnum serializedAclRuleTypeEnum) {
        final var aclRuleTypeEnum = serializer.deserialize(serializedAclRuleTypeEnum);
        assertThat(aclRuleTypeEnum).isEqualTo(expectedAclRuleTypeEnum);
    }

    private static Stream<Arguments> provideAclForwardActionEnum() {
        return Stream.of(
                Arguments.of(AclForwardActionEnum.DROP, Acl.AclForwardActionEnum.ACLFORWARDINGACTION_DROP),
                Arguments.of(
                        AclForwardActionEnum.ACCEPT, Acl.AclForwardActionEnum.ACLFORWARDINGACTION_ACCEPT),
                Arguments.of(
                        AclForwardActionEnum.REJECT, Acl.AclForwardActionEnum.ACLFORWARDINGACTION_REJECT),
                Arguments.of(
                        AclForwardActionEnum.UNDEFINED,
                        Acl.AclForwardActionEnum.ACLFORWARDINGACTION_UNDEFINED));
    }

    @ParameterizedTest
    @MethodSource("provideAclForwardActionEnum")
    void shouldSerializeAclForwardActionEnum(
            AclForwardActionEnum aclForwardActionEnum,
            Acl.AclForwardActionEnum expectedAclForwardActionEnum) {
        final var serializedAclForwardActionEnum = serializer.serialize(aclForwardActionEnum);
        assertThat(serializedAclForwardActionEnum.getNumber())
                .isEqualTo(expectedAclForwardActionEnum.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideAclForwardActionEnum")
    void shouldDeserializeAclForwardActionEnum(
            AclForwardActionEnum expectedAclForwardActionEnum,
            Acl.AclForwardActionEnum serializedAclForwardActionEnum) {
        final var aclForwardActionEnum = serializer.deserialize(serializedAclForwardActionEnum);
        assertThat(aclForwardActionEnum).isEqualTo(expectedAclForwardActionEnum);
    }

    private static Stream<Arguments> provideAclLogActionEnum() {
        return Stream.of(
                Arguments.of(AclLogActionEnum.NO_LOG, Acl.AclLogActionEnum.ACLLOGACTION_NOLOG),
                Arguments.of(AclLogActionEnum.SYSLOG, Acl.AclLogActionEnum.ACLLOGACTION_SYSLOG),
                Arguments.of(AclLogActionEnum.UNDEFINED, Acl.AclLogActionEnum.ACLLOGACTION_UNDEFINED));
    }

    @ParameterizedTest
    @MethodSource("provideAclLogActionEnum")
    void shouldSerializeAclLogActionEnum(
            AclLogActionEnum aclLogActionEnum, Acl.AclLogActionEnum expectedAclLogActionEnum) {
        final var serializedAclLogActionEnum = serializer.serialize(aclLogActionEnum);
        assertThat(serializedAclLogActionEnum.getNumber())
                .isEqualTo(expectedAclLogActionEnum.getNumber());
    }

    @Test
    void shouldSerializeAclAction() {
        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);

        final var expectedAclAction =
                Acl.AclAction.newBuilder()
                        .setForwardAction(Acl.AclForwardActionEnum.ACLFORWARDINGACTION_ACCEPT)
                        .setLogAction(Acl.AclLogActionEnum.ACLLOGACTION_SYSLOG)
                        .build();

        final var serializedAclAction = serializer.serialize(aclAction);

        assertThat(serializedAclAction).usingRecursiveComparison().isEqualTo(expectedAclAction);
    }

    @Test
    void shouldDeserializeAclAction() {
        final var expectedAclAction =
                createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);

        final var serializedAclAction = serializer.serialize(expectedAclAction);
        final var aclAction = serializer.deserialize(serializedAclAction);

        assertThat(aclAction).usingRecursiveComparison().isEqualTo(expectedAclAction);
    }

    @Test
    void shouldSerializeAclMatch() {
        final var aclMatch = createAclMatch(1, 1, "127.0.0.1", "127.0.0.2", 5601, 5602, 1, 2);

        final var expectedAclMatch =
                Acl.AclMatch.newBuilder()
                        .setDscp(1)
                        .setProtocol(1)
                        .setSrcAddress("127.0.0.1")
                        .setDstAddress("127.0.0.2")
                        .setSrcPort(5601)
                        .setDstPort(5602)
                        .setStartMplsLabel(1)
                        .setEndMplsLabel(2)
                        .build();

        final var serializedAclMatch = serializer.serialize(aclMatch);

        assertThat(serializedAclMatch).usingRecursiveComparison().isEqualTo(expectedAclMatch);
    }

    @Test
    void shouldDeserializeAclMatch() {
        final var expectedAclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);

        final var serializedAclMatch = serializer.serialize(expectedAclMatch);
        final var aclMatch = serializer.deserialize(serializedAclMatch);

        assertThat(aclMatch).usingRecursiveComparison().isEqualTo(expectedAclMatch);
    }

    @Test
    void shouldSerializeAclEntry() {
        final var sequenceId = 1;
        final var description = "aclEntryDescription";

        final var aclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);
        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
        final var aclEntry = createAclEntry(sequenceId, description, aclMatch, aclAction);

        final var serializedAclMatch = serializer.serialize(aclMatch);
        final var serializedAclAction = serializer.serialize(aclAction);

        final var expectedAclEntry =
                Acl.AclEntry.newBuilder()
                        .setSequenceId(sequenceId)
                        .setDescription(description)
                        .setMatch(serializedAclMatch)
                        .setAction(serializedAclAction)
                        .build();

        final var serializedAclEntry = serializer.serialize(aclEntry);

        assertThat(serializedAclEntry).usingRecursiveComparison().isEqualTo(expectedAclEntry);
    }

    @Test
    void shouldDeserializeAclEntry() {
        final var sequenceId = 1;
        final var description = "aclEntryDescription";

        final var aclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);
        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
        final var expectedAclEntry = createAclEntry(sequenceId, description, aclMatch, aclAction);

        final var serializedAclEntry = serializer.serialize(expectedAclEntry);
        final var aclEntry = serializer.deserialize(serializedAclEntry);

        assertThat(aclEntry).usingRecursiveComparison().isEqualTo(expectedAclEntry);
    }

    @Test
    void shouldSerializeAclRuleSet() {
        final var sequenceId = 1;
        final var aclEntryDescription = "aclEntryDescription";

        final var aclRuleSetName = "aclRuleSetName";
        final var aclRuleSetDescription = "aclRuleSetDescription";
        final var aclRuleSetUserId = "aclRuleSetUserId";

        final var aclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);
        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
        final var aclEntry = createAclEntry(sequenceId, aclEntryDescription, aclMatch, aclAction);
        final var aclRuleSet =
                new AclRuleSet(
                        aclRuleSetName,
                        AclRuleTypeEnum.MIXED,
                        aclRuleSetDescription,
                        aclRuleSetUserId,
                        List.of(aclEntry));

        final var serializedAclEntry = serializer.serialize(aclEntry);
        final var serializedAclEntries = List.of(serializedAclEntry);

        final var expectedAclRuleSet =
                Acl.AclRuleSet.newBuilder()
                        .setName(aclRuleSetName)
                        .setType(Acl.AclRuleTypeEnum.ACLRULETYPE_MIXED)
                        .setDescription(aclRuleSetDescription)
                        .setUserId(aclRuleSetUserId)
                        .addAllEntries(serializedAclEntries)
                        .build();

        final var serializedAclRuleset = serializer.serialize(aclRuleSet);

        assertThat(serializedAclRuleset).usingRecursiveComparison().isEqualTo(expectedAclRuleSet);
    }

    @Test
    void shouldDeserializeAclRuleSet() {
        final var sequenceId = 1;
        final var aclEntryDescription = "aclEntryDescription";

        final var aclRuleSetName = "aclRuleSetName";
        final var aclRuleSetDescription = "aclRuleSetDescription";
        final var aclRuleSetUserId = "aclRuleSetUserId";

        final var aclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);
        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
        final var aclEntry = createAclEntry(sequenceId, aclEntryDescription, aclMatch, aclAction);
        final var expectedAclRuleSet =
                new AclRuleSet(
                        aclRuleSetName,
                        AclRuleTypeEnum.MIXED,
                        aclRuleSetDescription,
                        aclRuleSetUserId,
                        List.of(aclEntry));

        final var serializedAclRuleSet = serializer.serialize(expectedAclRuleSet);
        final var aclRuleSet = serializer.deserialize(serializedAclRuleSet);

        assertThat(aclRuleSet).usingRecursiveComparison().isEqualTo(expectedAclRuleSet);
    }

    @ParameterizedTest
    @MethodSource("provideAclLogActionEnum")
    void shouldDeserializeAclLogActionEnum(
            AclLogActionEnum expectedAclLogActionEnum, Acl.AclLogActionEnum serializedAclLogActionEnum) {
        final var aclLogActionEnum = serializer.deserialize(serializedAclLogActionEnum);
        assertThat(aclLogActionEnum).isEqualTo(expectedAclLogActionEnum);
    }

    @Test
    void shouldSerializeTopologyId() {
        final var expectedContextId = "expectedContextId";
        final var expectedId = "expectedId";
        final var topologyId = new TopologyId(expectedContextId, expectedId);

        final var serializedContextId = serializer.serializeContextId(expectedContextId);
        final var serializedIdUuid = serializer.serializeUuid(expectedId);

        final var expectedTopologyId =
                ContextOuterClass.TopologyId.newBuilder()
                        .setContextId(serializedContextId)
                        .setTopologyUuid(serializedIdUuid)
                        .build();

        final var serializedTopologyId = serializer.serialize(topologyId);

        assertThat(serializedTopologyId).usingRecursiveComparison().isEqualTo(expectedTopologyId);
    }

    @Test
    void shouldDeserializeTopologyId() {
        final var expectedContextId = "expectedContextId";
        final var expectedId = "expectedId";

        final var expectedTopologyId = new TopologyId(expectedContextId, expectedId);

        final var serializedTopologyId = serializer.serialize(expectedTopologyId);
        final var topologyId = serializer.deserialize(serializedTopologyId);

        assertThat(topologyId).usingRecursiveComparison().isEqualTo(expectedTopologyId);
    }

    @Test
    void shouldSerializeEndPointId() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var serializedTopologyId = serializer.serialize(expectedTopologyId);
        final var serializedDeviceId = serializer.serializeDeviceId(expectedDeviceId);
        final var serializedEndPointUuid = serializer.serializeUuid(expectedId);

        final var expectedEndPointId =
                ContextOuterClass.EndPointId.newBuilder()
                        .setTopologyId(serializedTopologyId)
                        .setDeviceId(serializedDeviceId)
                        .setEndpointUuid(serializedEndPointUuid)
                        .build();

        final var serializedEndPointId = serializer.serialize(endPointId);

        assertThat(serializedEndPointId).usingRecursiveComparison().isEqualTo(expectedEndPointId);
    }

    @Test
    void shouldDeserializeEndPointId() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var expectedEndPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var serializedEndPointId = serializer.serialize(expectedEndPointId);
        final var endPointId = serializer.deserialize(serializedEndPointId);

        assertThat(endPointId).usingRecursiveComparison().isEqualTo(expectedEndPointId);
    }

    @Test
    void shouldSerializeConfigRuleAcl() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var sequenceId = 1;
        final var aclEntryDescription = "aclEntryDescription";

        final var aclRuleSetName = "aclRuleSetName";
        final var aclRuleSetDescription = "aclRuleSetDescription";
        final var aclRuleSetUserId = "aclRuleSetUserId";

        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var aclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);
        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
        final var aclEntry = createAclEntry(sequenceId, aclEntryDescription, aclMatch, aclAction);
        final var aclRuleSet =
                new AclRuleSet(
                        aclRuleSetName,
                        AclRuleTypeEnum.MIXED,
                        aclRuleSetDescription,
                        aclRuleSetUserId,
                        List.of(aclEntry));

        final var configRuleAcl = new ConfigRuleAcl(endPointId, aclRuleSet);

        final var serializedEndPointId = serializer.serialize(endPointId);
        final var serializedAclRuleSet = serializer.serialize(aclRuleSet);

        final var expectedConfigRuleAcl =
                ContextOuterClass.ConfigRule_ACL.newBuilder()
                        .setEndpointId(serializedEndPointId)
                        .setRuleSet(serializedAclRuleSet)
                        .build();

        final var serializedConfigRuleAcl = serializer.serialize(configRuleAcl);

        assertThat(serializedConfigRuleAcl).usingRecursiveComparison().isEqualTo(expectedConfigRuleAcl);
    }

    @Test
    void shouldDeserializeConfigRuleAcl() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";

        final var sequenceId = 1;
        final var aclEntryDescription = "aclEntryDescription";

        final var aclRuleSetName = "aclRuleSetName";
        final var aclRuleSetDescription = "aclRuleSetDescription";
        final var aclRuleSetUserId = "aclRuleSetUserId";

        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var aclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);
        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
        final var aclEntry = createAclEntry(sequenceId, aclEntryDescription, aclMatch, aclAction);
        final var aclRuleSet =
                new AclRuleSet(
                        aclRuleSetName,
                        AclRuleTypeEnum.MIXED,
                        aclRuleSetDescription,
                        aclRuleSetUserId,
                        List.of(aclEntry));

        final var expectedConfigRuleAcl = new ConfigRuleAcl(endPointId, aclRuleSet);

        final var serializedConfigRuleAcl = serializer.serialize(expectedConfigRuleAcl);
        final var configRuleAcl = serializer.deserialize(serializedConfigRuleAcl);

        assertThat(configRuleAcl).usingRecursiveComparison().isEqualTo(expectedConfigRuleAcl);
    }

    @Test
    void shouldSerializeConfigRuleCustom() {
        final var resourceKey = "resourceKey";
        final var resourceValue = "resourceValue";

        final var configRuleCustom = new ConfigRuleCustom(resourceKey, resourceValue);

        final var expectedConfigRuleCustom =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey(resourceKey)
                        .setResourceValue(resourceValue)
                        .build();

        final var serializedConfigRuleCustom = serializer.serialize(configRuleCustom);

        assertThat(serializedConfigRuleCustom)
                .usingRecursiveComparison()
                .isEqualTo(expectedConfigRuleCustom);
    }

    @Test
    void shouldDeserializeConfigRuleCustom() {
        final var resourceKey = "resourceKey";
        final var resourceValue = "resourceValue";

        final var expectedConfigRuleCustom = new ConfigRuleCustom(resourceKey, resourceValue);

        final var serializedConfigRuleCustom = serializer.serialize(expectedConfigRuleCustom);
        final var configRuleCustom = serializer.deserialize(serializedConfigRuleCustom);

        assertThat(configRuleCustom).usingRecursiveComparison().isEqualTo(expectedConfigRuleCustom);
    }

    @Test
    void shouldSerializeConfigRule() {
        final var contextIdUuid = "contextId";
        final var topologyIdUuid = "topologyUuid";
        final var deviceIdUuid = "deviceIdUuid";
        final var endpointIdUuid = "endpointIdUuid";

        final var expectedSerializedContextId = serializer.serializeContextId(contextIdUuid);
        final var expectedSerializedTopologyIdUuid = serializer.serializeUuid(topologyIdUuid);
        final var expectedSerializedDeviceId = serializer.serializeDeviceId(deviceIdUuid);
        final var expectedSerializedEndPointIdUuid = serializer.serializeUuid(endpointIdUuid);

        final var expectedSerializedTopologyId =
                ContextOuterClass.TopologyId.newBuilder()
                        .setContextId(expectedSerializedContextId)
                        .setTopologyUuid(expectedSerializedTopologyIdUuid)
                        .build();

        final var topologyId = new TopologyId(contextIdUuid, topologyIdUuid);

        final var expectedSerializedEndPointId =
                ContextOuterClass.EndPointId.newBuilder()
                        .setTopologyId(expectedSerializedTopologyId)
                        .setDeviceId(expectedSerializedDeviceId)
                        .setEndpointUuid(expectedSerializedEndPointIdUuid)
                        .build();

        final var endPointId = new EndPointId(topologyId, deviceIdUuid, endpointIdUuid);

        final var expectedSerializedAclMatch =
                Acl.AclMatch.newBuilder()
                        .setDscp(1)
                        .setProtocol(1)
                        .setSrcAddress("127.0.0.1")
                        .setDstAddress("127.0.0.2")
                        .setSrcPort(5601)
                        .setDstPort(5602)
                        .setStartMplsLabel(1)
                        .setEndMplsLabel(2)
                        .build();

        final var aclMatch = createAclMatch(1, 1, "127.0.0.1", "127.0.0.2", 5601, 5602, 1, 2);

        final var expectedSerializedAclAction =
                Acl.AclAction.newBuilder()
                        .setForwardAction(Acl.AclForwardActionEnum.ACLFORWARDINGACTION_ACCEPT)
                        .setLogAction(Acl.AclLogActionEnum.ACLLOGACTION_SYSLOG)
                        .build();

        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);

        final var expectedSerializedAclEntry =
                Acl.AclEntry.newBuilder()
                        .setSequenceId(1)
                        .setDescription("aclEntryDescription")
                        .setMatch(expectedSerializedAclMatch)
                        .setAction(expectedSerializedAclAction)
                        .build();

        final var aclEntry = createAclEntry(1, "aclEntryDescription", aclMatch, aclAction);

        final var expectedSerializedAclRuleSet =
                Acl.AclRuleSet.newBuilder()
                        .setName("aclRuleName")
                        .setType(Acl.AclRuleTypeEnum.ACLRULETYPE_IPV4)
                        .setDescription("AclRuleDescription")
                        .setUserId("userId")
                        .addEntries(expectedSerializedAclEntry)
                        .build();

        final var aclRuleSet =
                new AclRuleSet(
                        "aclRuleName",
                        org.etsi.tfs.ztp.acl.AclRuleTypeEnum.IPV4,
                        "AclRuleDescription",
                        "userId",
                        List.of(aclEntry));

        final var expectedSerializedConfigRuleAcl =
                ContextOuterClass.ConfigRule_ACL.newBuilder()
                        .setEndpointId(expectedSerializedEndPointId)
                        .setRuleSet(expectedSerializedAclRuleSet)
                        .build();

        final var configRuleAcl = new ConfigRuleAcl(endPointId, aclRuleSet);

        final var expectedConfigRule =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET)
                        .setAcl(expectedSerializedConfigRuleAcl)
                        .build();

        final var configRuleTypeAcl = new ConfigRuleTypeAcl(configRuleAcl);
        final var configRule = new ConfigRule(ConfigActionEnum.SET, configRuleTypeAcl);
        final var serializedConfigRule = serializer.serialize(configRule);

        assertThat(serializedConfigRule).isEqualTo(expectedConfigRule);
    }

    @Test
    void shouldDeserializeConfigRule() {
        final var contextIdUuid = "contextId";
        final var topologyIdUuid = "topologyUuid";
        final var deviceIdUuid = "deviceIdUuid";
        final var endpointIdUuid = "endpointIdUuid";

        final var serializedContextId = serializer.serializeContextId(contextIdUuid);
        final var serializedTopologyIdUuid = serializer.serializeUuid(topologyIdUuid);
        final var serializedDeviceId = serializer.serializeDeviceId(deviceIdUuid);
        final var serializedEndPointIdUuid = serializer.serializeUuid(endpointIdUuid);

        final var topologyId = new TopologyId(contextIdUuid, topologyIdUuid);
        final var serializedTopologyId =
                ContextOuterClass.TopologyId.newBuilder()
                        .setContextId(serializedContextId)
                        .setTopologyUuid(serializedTopologyIdUuid)
                        .build();

        final var endPointId = new EndPointId(topologyId, deviceIdUuid, endpointIdUuid);
        final var serializedEndPointId =
                ContextOuterClass.EndPointId.newBuilder()
                        .setTopologyId(serializedTopologyId)
                        .setDeviceId(serializedDeviceId)
                        .setEndpointUuid(serializedEndPointIdUuid)
                        .build();

        final var aclMatch = createAclMatch(1, 2, "127.0.0.1", "127.0.0.2", 5601, 5602, 5, 10);
        final var serializedAclMatch =
                Acl.AclMatch.newBuilder()
                        .setDscp(1)
                        .setProtocol(2)
                        .setSrcAddress("127.0.0.1")
                        .setDstAddress("127.0.0.2")
                        .setSrcPort(5601)
                        .setDstPort(5602)
                        .setStartMplsLabel(5)
                        .setEndMplsLabel(10)
                        .build();

        final var aclAction = createAclAction(AclForwardActionEnum.ACCEPT, AclLogActionEnum.SYSLOG);
        final var serializedAclAction =
                Acl.AclAction.newBuilder()
                        .setForwardAction(Acl.AclForwardActionEnum.ACLFORWARDINGACTION_ACCEPT)
                        .setLogAction(Acl.AclLogActionEnum.ACLLOGACTION_SYSLOG)
                        .build();

        final var aclEntry = createAclEntry(1, "aclEntryDescription", aclMatch, aclAction);

        final var serializedAclEntry =
                Acl.AclEntry.newBuilder()
                        .setSequenceId(1)
                        .setDescription("aclEntryDescription")
                        .setMatch(serializedAclMatch)
                        .setAction(serializedAclAction)
                        .build();

        final var aclRuleSet =
                new AclRuleSet(
                        "aclRuleName",
                        org.etsi.tfs.ztp.acl.AclRuleTypeEnum.IPV4,
                        "AclRuleDescription",
                        "userId",
                        List.of(aclEntry));

        final var serializedAclRuleSet =
                Acl.AclRuleSet.newBuilder()
                        .setName("aclRuleName")
                        .setType(Acl.AclRuleTypeEnum.ACLRULETYPE_IPV4)
                        .setDescription("AclRuleDescription")
                        .setUserId("userId")
                        .addEntries(serializedAclEntry)
                        .build();

        final var configRuleAcl = new ConfigRuleAcl(endPointId, aclRuleSet);
        final var configRuleTypeAcl = new ConfigRuleTypeAcl(configRuleAcl);

        final var expectedConfigRule = new ConfigRule(ConfigActionEnum.DELETE, configRuleTypeAcl);

        final var serializedConfigRuleAcl =
                ContextOuterClass.ConfigRule_ACL.newBuilder()
                        .setEndpointId(serializedEndPointId)
                        .setRuleSet(serializedAclRuleSet)
                        .build();

        final var serializedConfigRule =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE)
                        .setAcl(serializedConfigRuleAcl)
                        .build();

        final var configRule = serializer.deserialize(serializedConfigRule);

        assertThat(configRule).usingRecursiveComparison().isEqualTo(expectedConfigRule);
    }

    @Test
    void shouldThrowIllegalStateExceptionDuringDeserializationOfNonSpecifiedConfigRule() {
        final var serializedConfigRule =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET)
                        .build();

        assertThatExceptionOfType(IllegalStateException.class)
                .isThrownBy(() -> serializer.deserialize(serializedConfigRule));
    }

    private static Stream<Arguments> provideKpiSampleType() {
        return Stream.of(
                Arguments.of(
                        KpiSampleType.PACKETS_TRANSMITTED,
                        KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED),
                Arguments.of(
                        KpiSampleType.PACKETS_RECEIVED,
                        KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED),
                Arguments.of(
                        KpiSampleType.BYTES_TRANSMITTED,
                        KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED),
                Arguments.of(
                        KpiSampleType.BYTES_RECEIVED,
                        KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED),
                Arguments.of(
                        KpiSampleType.LINK_TOTAL_CAPACITY_GBPS,
                        KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_LINK_TOTAL_CAPACITY_GBPS),
                Arguments.of(
                        KpiSampleType.LINK_USED_CAPACITY_GBPS,
                        KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS),
                Arguments.of(KpiSampleType.UNKNOWN, KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_UNKNOWN));
    }

    @ParameterizedTest
    @MethodSource("provideKpiSampleType")
    void shouldSerializeKpiSampleType(
            KpiSampleType kpiSampleType, KpiSampleTypes.KpiSampleType expectedSerializedType) {
        final var serializedKpiSampleType = serializer.serialize(kpiSampleType);

        assertThat(serializedKpiSampleType.getNumber()).isEqualTo(expectedSerializedType.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideKpiSampleType")
    void shouldDeserializeKpiSampleType(
            KpiSampleType expectedKpiSampleType, KpiSampleTypes.KpiSampleType serializedKpiSampleType) {
        final var kpiSampleType = serializer.deserialize(serializedKpiSampleType);

        assertThat(kpiSampleType).isEqualTo(expectedKpiSampleType);
    }

    private static Stream<Arguments> provideDeviceDriverEnum() {
        return Stream.of(
                Arguments.of(
                        DeviceDriverEnum.OPENCONFIG,
                        ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG),
                Arguments.of(
                        DeviceDriverEnum.TRANSPORT_API,
                        ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API),
                Arguments.of(DeviceDriverEnum.P4, ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_P4),
                Arguments.of(
                        DeviceDriverEnum.IETF_NETWORK_TOPOLOGY,
                        ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY),
                Arguments.of(
                        DeviceDriverEnum.ONF_TR_532,
                        ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_ONF_TR_532),
                Arguments.of(DeviceDriverEnum.XR, ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_XR),
                Arguments.of(
                        DeviceDriverEnum.IETF_L2VPN,
                        ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_L2VPN),
                Arguments.of(
                        DeviceDriverEnum.GNMI_OPENCONFIG,
                        ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_GNMI_OPENCONFIG),
                Arguments.of(
                        DeviceDriverEnum.OPTICAL_TFS,
                        ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_OPTICAL_TFS),
                Arguments.of(
                        DeviceDriverEnum.IETF_ACTN, ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_ACTN),
                Arguments.of(
                        DeviceDriverEnum.UNDEFINED, ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_UNDEFINED));
    }

    @ParameterizedTest
    @MethodSource("provideDeviceDriverEnum")
    void shouldSerializeDeviceDriverEnum(
            DeviceDriverEnum deviceDriverEnum,
            ContextOuterClass.DeviceDriverEnum expectedDeviceDriverEnum) {
        final var serializedDeviceDriverEnum = serializer.serialize(deviceDriverEnum);

        assertThat(serializedDeviceDriverEnum.getNumber())
                .isEqualTo(expectedDeviceDriverEnum.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideDeviceDriverEnum")
    void shouldDeserializeDeviceDriverEnum(
            DeviceDriverEnum expectedDeviceDriverEnum,
            ContextOuterClass.DeviceDriverEnum serializedDeviceDriverEnum) {
        final var deviceDriverEnum = serializer.deserialize(serializedDeviceDriverEnum);

        assertThat(deviceDriverEnum).isEqualTo(expectedDeviceDriverEnum);
    }

    @Test
    void shouldSerializeDeviceConfig() {
        final var expectedConfigRuleCustomA =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyA")
                        .setResourceValue("resourceValueA")
                        .build();

        final var configRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");

        final var expectedConfigRuleCustomB =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyB")
                        .setResourceValue("resourceValueB")
                        .build();

        final var configRuleCustomB = new ConfigRuleCustom("resourceKeyB", "resourceValueB");

        final var expectedConfigRuleA =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET)
                        .setCustom(expectedConfigRuleCustomA)
                        .build();
        final var expectedConfigRuleB =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE)
                        .setCustom(expectedConfigRuleCustomB)
                        .build();

        final var expectedDeviceConfig =
                ContextOuterClass.DeviceConfig.newBuilder()
                        .addAllConfigRules(List.of(expectedConfigRuleA, expectedConfigRuleB))
                        .build();

        final var configRuleTypeA = new ConfigRuleTypeCustom(configRuleCustomA);
        final var configRuleTypeB = new ConfigRuleTypeCustom(configRuleCustomB);

        final var configRuleA = new ConfigRule(ConfigActionEnum.SET, configRuleTypeA);
        final var configRuleB = new ConfigRule(ConfigActionEnum.DELETE, configRuleTypeB);

        final var deviceConfig = new DeviceConfig(List.of(configRuleA, configRuleB));
        final var serializedDeviceConfig = serializer.serialize(deviceConfig);

        assertThat(serializedDeviceConfig).isEqualTo(expectedDeviceConfig);
    }

    @Test
    void shouldDeserializeDeviceConfig() {
        final var expectedConfigRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var expectedConfigRuleCustomB = new ConfigRuleCustom("resourceKeyB", "resourceValueB");

        final var expectedConfigRuleTypeA = new ConfigRuleTypeCustom(expectedConfigRuleCustomA);
        final var expectedConfigRuleTypeB = new ConfigRuleTypeCustom(expectedConfigRuleCustomB);

        final var expectedConfigRuleA = new ConfigRule(ConfigActionEnum.SET, expectedConfigRuleTypeA);
        final var expectedConfigRuleB =
                new ConfigRule(ConfigActionEnum.DELETE, expectedConfigRuleTypeB);

        final var expectedDeviceConfig =
                new DeviceConfig(List.of(expectedConfigRuleA, expectedConfigRuleB));

        final var configRuleCustomA =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyA")
                        .setResourceValue("resourceValueA")
                        .build();

        final var configRuleCustomB =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyB")
                        .setResourceValue("resourceValueB")
                        .build();

        final var configRuleA =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET)
                        .setCustom(configRuleCustomA)
                        .build();
        final var configRuleB =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE)
                        .setCustom(configRuleCustomB)
                        .build();
        final var serializedDeviceConfig =
                ContextOuterClass.DeviceConfig.newBuilder()
                        .addAllConfigRules(List.of(configRuleA, configRuleB))
                        .build();
        final var deviceConfig = serializer.deserialize(serializedDeviceConfig);

        assertThat(deviceConfig).usingRecursiveComparison().isEqualTo(expectedDeviceConfig);
    }

    private static Stream<Arguments> provideOperationalStatusEnum() {
        return Stream.of(
                Arguments.of(
                        DeviceOperationalStatus.ENABLED,
                        DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED),
                Arguments.of(
                        DeviceOperationalStatus.DISABLED,
                        DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED),
                Arguments.of(
                        DeviceOperationalStatus.UNDEFINED,
                        DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED));
    }

    @ParameterizedTest
    @MethodSource("provideOperationalStatusEnum")
    void shouldSerializeOperationalStatusEnum(
            DeviceOperationalStatus opStatus,
            ContextOuterClass.DeviceOperationalStatusEnum expectedOpStatus) {
        final var serializedOpStatus = serializer.serialize(opStatus);
        assertThat(serializedOpStatus.getNumber()).isEqualTo(expectedOpStatus.getNumber());
    }

    @ParameterizedTest
    @MethodSource("provideOperationalStatusEnum")
    void shouldDeserializeOperationalStatusEnum(
            DeviceOperationalStatus expectedOpStatus,
            ContextOuterClass.DeviceOperationalStatusEnum serializedOpStatus) {
        final var operationalStatus = serializer.deserialize(serializedOpStatus);
        assertThat(operationalStatus).isEqualTo(expectedOpStatus);
    }

    @Test
    void shouldSerializeLocationOfTypeRegion() {
        final var region = "Tokyo";

        final var locationTypeRegion = new LocationTypeRegion(region);
        final var location = new Location(locationTypeRegion);

        final var expectedLocation = ContextOuterClass.Location.newBuilder().setRegion(region).build();

        final var serializedLocation = serializer.serialize(location);

        assertThat(serializedLocation).isEqualTo(expectedLocation);
    }

    @Test
    void shouldDeserializeLocationOfTypeRegion() {
        final var region = "Tokyo";

        final var locationTypeRegion = new LocationTypeRegion(region);
        final var expectedLocation = new Location(locationTypeRegion);

        final var serializedLocation =
                ContextOuterClass.Location.newBuilder().setRegion(region).build();

        final var location = serializer.deserialize(serializedLocation);

        assertThat(location).usingRecursiveComparison().isEqualTo(expectedLocation);
    }

    @Test
    void shouldSerializeLocationOfTypeGpsPosition() {
        final var latitude = 33.3f;
        final var longitude = 86.4f;

        final var gpsPosition = new GpsPosition(latitude, longitude);
        final var locationTypeGpsPosition = new LocationTypeGpsPosition(gpsPosition);
        final var location = new Location(locationTypeGpsPosition);

        final var serializedGpsPosition =
                ContextOuterClass.GPS_Position.newBuilder()
                        .setLatitude(latitude)
                        .setLongitude(longitude)
                        .build();

        final var expectedLocation =
                ContextOuterClass.Location.newBuilder().setGpsPosition(serializedGpsPosition).build();

        final var serializedLocation = serializer.serialize(location);

        assertThat(serializedLocation).isEqualTo(expectedLocation);
    }

    @Test
    void shouldDeserializeLocationOfTypeGpsPosition() {
        final var latitude = 33.3f;
        final var longitude = 86.4f;

        final var gpsPosition = new GpsPosition(latitude, longitude);
        final var locationTypeGpsPosition = new LocationTypeGpsPosition(gpsPosition);
        final var expectedLocation = new Location(locationTypeGpsPosition);

        final var serializedGpsPosition =
                ContextOuterClass.GPS_Position.newBuilder()
                        .setLatitude(latitude)
                        .setLongitude(longitude)
                        .build();

        final var serializedLocation =
                ContextOuterClass.Location.newBuilder().setGpsPosition(serializedGpsPosition).build();

        final var location = serializer.deserialize(serializedLocation);

        assertThat(location).usingRecursiveComparison().isEqualTo(expectedLocation);
    }

    @Test
    void shouldThrowIllegalStateExceptionDuringDeserializationOfNonSpecifiedLocation() {
        final var serializedLocation = ContextOuterClass.Location.newBuilder().build();

        assertThatExceptionOfType(IllegalStateException.class)
                .isThrownBy(() -> serializer.deserialize(serializedLocation));
    }

    @Test
    void shouldSerializeEndPointWithAllAvailableFields() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";
        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var endPointType = "endPointType";
        final var kpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegion = new LocationTypeRegion("ATH");
        final var location = new Location(locationTypeRegion);

        final var endPoint =
                new EndPointBuilder(endPointId, endPointType, kpiSampleTypes).location(location).build();

        final var serializedEndPointId = serializer.serialize(endPointId);
        final var serializedKpiSampleTypes =
                kpiSampleTypes.stream().map(serializer::serialize).collect(Collectors.toList());
        final var serializedEndPointLocation = serializer.serialize(location);

        final var expectedEndPoint =
                ContextOuterClass.EndPoint.newBuilder()
                        .setEndpointId(serializedEndPointId)
                        .setEndpointType(endPointType)
                        .addAllKpiSampleTypes(serializedKpiSampleTypes)
                        .setEndpointLocation(serializedEndPointLocation)
                        .build();

        final var serializedEndPoint = serializer.serialize(endPoint);

        assertThat(serializedEndPoint).isEqualTo(expectedEndPoint);
    }

    @Test
    void shouldDeserializeEndPointWithAllAvailableFields() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";
        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var endPointType = "endPointType";
        final var kpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegion = new LocationTypeRegion("ATH");
        final var location = new Location(locationTypeRegion);

        final var expectedEndPoint =
                new EndPointBuilder(endPointId, endPointType, kpiSampleTypes).location(location).build();

        final var serializedEndPointId = serializer.serialize(endPointId);
        final var serializedKpiSampleTypes =
                kpiSampleTypes.stream().map(serializer::serialize).collect(Collectors.toList());
        final var serializedEndPointLocation = serializer.serialize(location);

        final var serializedEndPoint =
                ContextOuterClass.EndPoint.newBuilder()
                        .setEndpointId(serializedEndPointId)
                        .setEndpointType(endPointType)
                        .addAllKpiSampleTypes(serializedKpiSampleTypes)
                        .setEndpointLocation(serializedEndPointLocation)
                        .build();

        final var endPoint = serializer.deserialize(serializedEndPoint);

        assertThat(endPoint).usingRecursiveComparison().isEqualTo(expectedEndPoint);
    }

    @Test
    void shouldSerializeEndPointWithAllAvailableFieldsMissingLocation() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";
        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var endPointType = "endPointType";
        final var kpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);

        final var endPoint = new EndPointBuilder(endPointId, endPointType, kpiSampleTypes).build();

        final var serializedEndPointId = serializer.serialize(endPointId);
        final var serializedKpiSampleTypes =
                kpiSampleTypes.stream().map(serializer::serialize).collect(Collectors.toList());

        final var expectedEndPoint =
                ContextOuterClass.EndPoint.newBuilder()
                        .setEndpointId(serializedEndPointId)
                        .setEndpointType(endPointType)
                        .addAllKpiSampleTypes(serializedKpiSampleTypes)
                        .build();

        final var serializedEndPoint = serializer.serialize(endPoint);

        assertThat(serializedEndPoint).isEqualTo(expectedEndPoint);
    }

    @Test
    void shouldDeserializeEndPointWithAllAvailableFieldsMissingLocation() {
        final var expectedTopologyId = new TopologyId("contextId", "id");
        final var expectedDeviceId = "expectedDeviceId";
        final var expectedId = "expectedId";
        final var endPointId = new EndPointId(expectedTopologyId, expectedDeviceId, expectedId);

        final var endPointType = "endPointType";
        final var kpiSampleTypes =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);

        final var expectedEndPoint =
                new EndPointBuilder(endPointId, endPointType, kpiSampleTypes).build();

        final var serializedEndPointId = serializer.serialize(endPointId);
        final var serializedKpiSampleTypes =
                kpiSampleTypes.stream().map(serializer::serialize).collect(Collectors.toList());

        final var serializedEndPoint =
                ContextOuterClass.EndPoint.newBuilder()
                        .setEndpointId(serializedEndPointId)
                        .setEndpointType(endPointType)
                        .addAllKpiSampleTypes(serializedKpiSampleTypes)
                        .build();

        final var endPoint = serializer.deserialize(serializedEndPoint);

        assertThat(endPoint).usingRecursiveComparison().isEqualTo(expectedEndPoint);
    }

    @Test
    void shouldSerializeDevice() {
        final var expectedConfigRuleCustomA =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyA")
                        .setResourceValue("resourceValueA")
                        .build();
        final var configRuleCustomA = new ConfigRuleCustom("resourceKeyA", "resourceValueA");

        final var expectedConfigRule =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET)
                        .setCustom(expectedConfigRuleCustomA)
                        .build();

        final var configRuleTypeA = new ConfigRuleTypeCustom(configRuleCustomA);
        final var deviceConfig =
                new DeviceConfig(List.of(new ConfigRule(ConfigActionEnum.SET, configRuleTypeA)));

        final var deviceDrivers = List.of(DeviceDriverEnum.IETF_NETWORK_TOPOLOGY, DeviceDriverEnum.P4);

        final var expectedTopologyIdA = new TopologyId("contextIdA", "idA");
        final var expectedDeviceIdA = "expectedDeviceIdA";
        final var expectedIdA = "expectedIdA";
        final var endPointIdA = new EndPointId(expectedTopologyIdA, expectedDeviceIdA, expectedIdA);

        final var endPointTypeA = "endPointTypeA";
        final var kpiSampleTypesA =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionA = new LocationTypeRegion("ATH");
        final var locationA = new Location(locationTypeRegionA);
        final var endPointA =
                new EndPointBuilder(endPointIdA, endPointTypeA, kpiSampleTypesA)
                        .location(locationA)
                        .build();

        final var expectedTopologyIdB = new TopologyId("contextIdB", "idB");
        final var expectedDeviceIdB = "expectedDeviceIdB";
        final var expectedIdB = "expectedIdB";
        final var endPointIdB = new EndPointId(expectedTopologyIdB, expectedDeviceIdB, expectedIdB);

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

        final var expectedDeviceConfig =
                ContextOuterClass.DeviceConfig.newBuilder().addConfigRules(expectedConfigRule).build();

        final var serializedDeviceId = serializer.serializeDeviceId("deviceId");
        final var serializedDrivers =
                deviceDrivers.stream()
                        .map(deviceDriverEnum -> serializer.serialize(deviceDriverEnum))
                        .collect(Collectors.toList());

        final var serializedEndPoints =
                endPoints.stream()
                        .map(endPoint -> serializer.serialize(endPoint))
                        .collect(Collectors.toList());

        final var deviceBuilder = ContextOuterClass.Device.newBuilder();

        deviceBuilder.setDeviceId(serializedDeviceId);
        deviceBuilder.setName("deviceName");
        deviceBuilder.setDeviceType("deviceType");
        deviceBuilder.setDeviceConfig(expectedDeviceConfig);
        deviceBuilder.setDeviceOperationalStatus(serializer.serialize(DeviceOperationalStatus.ENABLED));
        deviceBuilder.addAllDeviceDrivers(serializedDrivers);
        deviceBuilder.addAllDeviceEndpoints(serializedEndPoints);

        final var expectedDevice = deviceBuilder.build();

        final var device =
                new Device(
                        "deviceId",
                        "deviceName",
                        "deviceType",
                        deviceConfig,
                        DeviceOperationalStatus.ENABLED,
                        deviceDrivers,
                        endPoints);
        final var serializedDevice = serializer.serialize(device);

        assertThat(serializedDevice).isEqualTo(expectedDevice);
    }

    @Test
    void shouldDeserializeDevice() {
        final var configRuleCustom = new ConfigRuleCustom("resourceKeyA", "resourceValueA");
        final var expectedConfigRuleCustom =
                ContextOuterClass.ConfigRule_Custom.newBuilder()
                        .setResourceKey("resourceKeyA")
                        .setResourceValue("resourceValueA")
                        .build();
        final var configRuleType = new ConfigRuleTypeCustom(configRuleCustom);

        final var expectedConfig =
                new DeviceConfig(List.of(new ConfigRule(ConfigActionEnum.DELETE, configRuleType)));

        final var deviceDrivers = List.of(DeviceDriverEnum.IETF_NETWORK_TOPOLOGY, DeviceDriverEnum.P4);

        final var expectedTopologyIdA = new TopologyId("contextIdA", "idA");
        final var expectedDeviceIdA = "expectedDeviceIdA";
        final var expectedIdA = "expectedIdA";
        final var endPointIdA = new EndPointId(expectedTopologyIdA, expectedDeviceIdA, expectedIdA);

        final var endPointTypeA = "endPointTypeA";
        final var kpiSampleTypesA =
                List.of(KpiSampleType.BYTES_RECEIVED, KpiSampleType.BYTES_TRANSMITTED);
        final var locationTypeRegionA = new LocationTypeRegion("ATH");
        final var locationA = new Location(locationTypeRegionA);
        final var endPointA =
                new EndPointBuilder(endPointIdA, endPointTypeA, kpiSampleTypesA)
                        .location(locationA)
                        .build();

        final var expectedTopologyIdB = new TopologyId("contextIdB", "idB");
        final var expectedDeviceIdB = "expectedDeviceIdB";
        final var expectedIdB = "expectedIdB";
        final var endPointIdB = new EndPointId(expectedTopologyIdB, expectedDeviceIdB, expectedIdB);

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

        final var expectedDevice =
                new Device(
                        "deviceId",
                        "deviceName",
                        "deviceType",
                        expectedConfig,
                        DeviceOperationalStatus.ENABLED,
                        deviceDrivers,
                        endPoints);

        final var configRule =
                ContextOuterClass.ConfigRule.newBuilder()
                        .setAction(ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE)
                        .setCustom(expectedConfigRuleCustom)
                        .build();
        final var deviceConfig =
                ContextOuterClass.DeviceConfig.newBuilder().addConfigRules(configRule).build();

        final var serializedDeviceId = serializer.serializeDeviceId("deviceId");
        final var serializedDeviceOperationalStatus =
                serializer.serialize(DeviceOperationalStatus.ENABLED);

        final var serializedDrivers =
                deviceDrivers.stream()
                        .map(deviceDriverEnum -> serializer.serialize(deviceDriverEnum))
                        .collect(Collectors.toList());

        final var serializedEndPoints =
                endPoints.stream()
                        .map(endPoint -> serializer.serialize(endPoint))
                        .collect(Collectors.toList());

        final var deviceBuilder = ContextOuterClass.Device.newBuilder();
        deviceBuilder.setDeviceId(serializedDeviceId);
        deviceBuilder.setName("deviceName");
        deviceBuilder.setDeviceType("deviceType");
        deviceBuilder.setDeviceConfig(deviceConfig);
        deviceBuilder.setDeviceOperationalStatus(serializedDeviceOperationalStatus);
        deviceBuilder.addAllDeviceDrivers(serializedDrivers);
        deviceBuilder.addAllDeviceEndpoints(serializedEndPoints);

        final var serializedDevice = deviceBuilder.build();
        final var device = serializer.deserialize(serializedDevice);

        assertThat(device).usingRecursiveComparison().isEqualTo(expectedDevice);
    }

    @Test
    void shouldSerializeEmpty() {
        final var empty = new Empty();
        final var expectedEmpty = ContextOuterClass.Empty.newBuilder().build();

        final var serializeEmpty = serializer.serializeEmpty(empty);

        assertThat(serializeEmpty).isEqualTo(expectedEmpty);
    }

    @Test
    void shouldDeserializeEmpty() {
        final var expectedEmpty = new Empty();

        final var serializedEmpty = serializer.serializeEmpty(expectedEmpty);

        final var empty = serializer.deserializeEmpty(serializedEmpty);

        assertThat(empty).usingRecursiveComparison().isEqualTo(expectedEmpty);
    }

    @Test
    void shouldSerializeUuid() {
        final var expectedUuid = "uuid";

        final var serializeUuid = serializer.serializeUuid("uuid");

        assertThat(serializeUuid.getUuid()).isEqualTo(expectedUuid);
    }

    @Test
    void shouldDeserializeUuid() {
        final var expectedUuid = "uuid";

        final var uuid = serializer.deserialize(Uuid.newBuilder().setUuid("uuid").build());

        assertThat(uuid).isEqualTo(expectedUuid);
    }
}
