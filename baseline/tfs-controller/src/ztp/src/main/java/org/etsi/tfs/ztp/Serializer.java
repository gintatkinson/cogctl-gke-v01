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

import acl.Acl;
import context.ContextOuterClass;
import context.ContextOuterClass.ConfigRule_ACL;
import context.ContextOuterClass.ConfigRule_Custom;
import context.ContextOuterClass.ContextId;
import context.ContextOuterClass.DeviceId;
import context.ContextOuterClass.DeviceOperationalStatusEnum;
import context.ContextOuterClass.Location.LocationCase;
import context.ContextOuterClass.Uuid;
import jakarta.inject.Singleton;
import java.util.stream.Collectors;
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
import org.etsi.tfs.ztp.context.model.EndPoint;
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
import ztp.Ztp;
import ztp.Ztp.ZtpDeviceState;

@Singleton
public class Serializer {

    public DeviceId serializeDeviceId(String expectedDeviceId) {
        final var builder = DeviceId.newBuilder();
        final var uuid = serializeUuid(expectedDeviceId);

        builder.setDeviceUuid(uuid);

        return builder.build();
    }

    public String deserialize(DeviceId deviceId) {
        return deviceId.getDeviceUuid().getUuid();
    }

    public Ztp.DeviceRoleId serialize(DeviceRoleId deviceRoleId) {
        final var builder = Ztp.DeviceRoleId.newBuilder();

        final var deviceRoleDevRoleId = deviceRoleId.getId();
        final var deviceRoleDeviceId = deviceRoleId.getDeviceId();

        final var deviceRoleDevRoleIdUuid = serializeUuid(deviceRoleDevRoleId);
        final var deviceRoleDeviceIdUuid = serializeUuid(deviceRoleDeviceId);

        final var deviceId = DeviceId.newBuilder().setDeviceUuid(deviceRoleDeviceIdUuid);

        builder.setDevRoleId(deviceRoleDevRoleIdUuid);
        builder.setDevId(deviceId);

        return builder.build();
    }

    public DeviceRoleId deserialize(Ztp.DeviceRoleId deviceRoleId) {
        final var devRoleId = deserialize(deviceRoleId.getDevRoleId());
        final var devId = deserialize(deviceRoleId.getDevId());

        return new DeviceRoleId(devRoleId, devId);
    }

    public Ztp.DeviceRoleType serialize(DeviceRoleType deviceRoleType) {
        switch (deviceRoleType) {
            case NONE:
                return Ztp.DeviceRoleType.NONE;
            case DEV_OPS:
                return Ztp.DeviceRoleType.DEV_OPS;
            case DEV_CONF:
                return Ztp.DeviceRoleType.DEV_CONF;
            case PIPELINE_CONF:
                return Ztp.DeviceRoleType.PIPELINE_CONF;
            default:
                return Ztp.DeviceRoleType.UNRECOGNIZED;
        }
    }

    public DeviceRoleType deserialize(Ztp.DeviceRoleType serializedDeviceRoleType) {
        switch (serializedDeviceRoleType) {
            case DEV_OPS:
                return DeviceRoleType.DEV_OPS;
            case DEV_CONF:
                return DeviceRoleType.DEV_CONF;
            case PIPELINE_CONF:
                return DeviceRoleType.PIPELINE_CONF;
            case NONE:
            case UNRECOGNIZED:
            default:
                return DeviceRoleType.NONE;
        }
    }

    public Ztp.ZtpDeviceState serialize(DeviceState deviceState) {
        switch (deviceState) {
            case CREATED:
                return ZtpDeviceState.ZTP_DEV_STATE_CREATED;
            case UPDATED:
                return ZtpDeviceState.ZTP_DEV_STATE_UPDATED;
            case DELETED:
                return ZtpDeviceState.ZTP_DEV_STATE_DELETED;
            case UNDEFINED:
                return ZtpDeviceState.ZTP_DEV_STATE_UNDEFINED;
            default:
                return ZtpDeviceState.UNRECOGNIZED;
        }
    }

    public DeviceState deserialize(Ztp.ZtpDeviceState serializedDeviceState) {
        switch (serializedDeviceState) {
            case ZTP_DEV_STATE_CREATED:
                return DeviceState.CREATED;
            case ZTP_DEV_STATE_UPDATED:
                return DeviceState.UPDATED;
            case ZTP_DEV_STATE_DELETED:
                return DeviceState.DELETED;
            case ZTP_DEV_STATE_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return DeviceState.UNDEFINED;
        }
    }

    public Ztp.DeviceRole serialize(DeviceRole deviceRole) {
        final var builder = Ztp.DeviceRole.newBuilder();
        final var serializedDeviceRoleId = serialize(deviceRole.getDeviceRoleId());
        final var serializedDeviceRoleType = serialize(deviceRole.getType());

        builder.setDevRoleId(serializedDeviceRoleId);
        builder.setDevRoleType(serializedDeviceRoleType);

        return builder.build();
    }

    public DeviceRole deserialize(Ztp.DeviceRole deviceRole) {
        final var deviceRoleId = deserialize(deviceRole.getDevRoleId());
        final var deviceRoleType = deserialize(deviceRole.getDevRoleType());

        return new DeviceRole(deviceRoleId, deviceRoleType);
    }

    public Ztp.DeviceRoleConfig serialize(DeviceRoleConfig deviceRoleConfig) {
        final var builder = Ztp.DeviceRoleConfig.newBuilder();
        final var serializedDeviceRole = serialize(deviceRoleConfig.getDeviceRole());
        final var serializedDeviceConfig = serialize(deviceRoleConfig.getDeviceConfig());

        builder.setDevRole(serializedDeviceRole);
        builder.setDevConfig(serializedDeviceConfig);

        return builder.build();
    }

    public DeviceRoleConfig deserialize(Ztp.DeviceRoleConfig deviceRoleConfig) {
        final var deviceRole = deserialize(deviceRoleConfig.getDevRole());
        final var deviceConfig = deserialize(deviceRoleConfig.getDevConfig());

        return new DeviceRoleConfig(deviceRole, deviceConfig);
    }

    public ContextOuterClass.EventTypeEnum serialize(EventTypeEnum eventTypeEnum) {
        switch (eventTypeEnum) {
            case CREATE:
                return ContextOuterClass.EventTypeEnum.EVENTTYPE_CREATE;
            case REMOVE:
                return ContextOuterClass.EventTypeEnum.EVENTTYPE_REMOVE;
            case UPDATE:
                return ContextOuterClass.EventTypeEnum.EVENTTYPE_UPDATE;
            case UNDEFINED:
                return ContextOuterClass.EventTypeEnum.EVENTTYPE_UNDEFINED;
            default:
                return ContextOuterClass.EventTypeEnum.UNRECOGNIZED;
        }
    }

    public EventTypeEnum deserialize(ContextOuterClass.EventTypeEnum serializedEventType) {
        switch (serializedEventType) {
            case EVENTTYPE_CREATE:
                return EventTypeEnum.CREATE;
            case EVENTTYPE_REMOVE:
                return EventTypeEnum.REMOVE;
            case EVENTTYPE_UPDATE:
                return EventTypeEnum.UPDATE;
            case EVENTTYPE_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return EventTypeEnum.UNDEFINED;
        }
    }

    public ContextOuterClass.Timestamp serialize(double timestamp) {
        final var builder = ContextOuterClass.Timestamp.newBuilder();

        builder.setTimestamp(timestamp);

        return builder.build();
    }

    public double deserialize(ContextOuterClass.Timestamp serializedTimeStamp) {

        return serializedTimeStamp.getTimestamp();
    }

    public ContextOuterClass.Event serialize(Event event) {
        final var builder = ContextOuterClass.Event.newBuilder();

        final var eventType = serialize(event.getEventTypeEnum());
        final var timestamp = serialize(event.getTimestamp());
        builder.setEventType(eventType);
        builder.setTimestamp(timestamp);

        return builder.build();
    }

    public Event deserialize(ContextOuterClass.Event serializedEvent) {
        final var timestamp = deserialize(serializedEvent.getTimestamp());
        final var eventType = deserialize(serializedEvent.getEventType());

        return new Event(timestamp, eventType);
    }

    public ContextOuterClass.DeviceEvent serialize(DeviceEvent deviceEvent) {
        final var builder = ContextOuterClass.DeviceEvent.newBuilder();
        final var deviceIdUuid = serializeUuid(deviceEvent.getDeviceId());
        final var deviceId = DeviceId.newBuilder().setDeviceUuid(deviceIdUuid);

        builder.setDeviceId(deviceId);
        builder.setEvent(serialize(deviceEvent.getEvent()));
        builder.setDeviceConfig(serialize(deviceEvent.getDeviceConfig().orElse(null)));

        return builder.build();
    }

    public DeviceEvent deserialize(ContextOuterClass.DeviceEvent deviceEvent) {
        final var deviceId = deserialize(deviceEvent.getDeviceId());
        final var event = deserialize(deviceEvent.getEvent());
        final var deviceConfig = deserialize(deviceEvent.getDeviceConfig());

        return new DeviceEvent(deviceId, event, deviceConfig);
    }

    public ContextOuterClass.ConfigActionEnum serialize(ConfigActionEnum configAction) {
        switch (configAction) {
            case SET:
                return ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET;
            case DELETE:
                return ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE;
            case UNDEFINED:
            default:
                return ContextOuterClass.ConfigActionEnum.CONFIGACTION_UNDEFINED;
        }
    }

    public ConfigActionEnum deserialize(ContextOuterClass.ConfigActionEnum serializedConfigAction) {
        switch (serializedConfigAction) {
            case CONFIGACTION_SET:
                return ConfigActionEnum.SET;
            case CONFIGACTION_DELETE:
                return ConfigActionEnum.DELETE;
            case UNRECOGNIZED:
            case CONFIGACTION_UNDEFINED:
            default:
                return ConfigActionEnum.UNDEFINED;
        }
    }

    public ContextId serializeContextId(String expectedContextId) {
        final var builder = ContextId.newBuilder();
        final var uuid = serializeUuid(expectedContextId);

        builder.setContextUuid(uuid);

        return builder.build();
    }

    public String deserialize(ContextId contextId) {
        return contextId.getContextUuid().getUuid();
    }

    public ContextOuterClass.TopologyId serialize(TopologyId topologyId) {
        final var builder = ContextOuterClass.TopologyId.newBuilder();

        final var topologyIdContextId = topologyId.getContextId();
        final var topologyIdId = topologyId.getId();

        final var contextId = serializeContextId(topologyIdContextId);
        final var topologyIdIdUuid = serializeUuid(topologyIdId);

        builder.setContextId(contextId);
        builder.setTopologyUuid(topologyIdIdUuid);

        return builder.build();
    }

    public TopologyId deserialize(ContextOuterClass.TopologyId topologyId) {
        final var topologyIdContextId = deserialize(topologyId.getContextId());
        final var topologyIdId = deserialize(topologyId.getTopologyUuid());

        return new TopologyId(topologyIdContextId, topologyIdId);
    }

    public ContextOuterClass.EndPointId serialize(EndPointId endPointId) {
        final var builder = ContextOuterClass.EndPointId.newBuilder();

        final var endPointIdTopologyId = endPointId.getTopologyId();
        final var endPointIdDeviceId = endPointId.getDeviceId();
        final var endPointIdId = endPointId.getId();

        final var serializedTopologyId = serialize(endPointIdTopologyId);
        final var serializedDeviceId = serializeDeviceId(endPointIdDeviceId);
        final var serializedEndPointIdId = serializeUuid(endPointIdId);

        builder.setTopologyId(serializedTopologyId);
        builder.setDeviceId(serializedDeviceId);
        builder.setEndpointUuid(serializedEndPointIdId);

        return builder.build();
    }

    public EndPointId deserialize(ContextOuterClass.EndPointId serializedEndPointId) {
        final var serializedTopologyId = serializedEndPointId.getTopologyId();
        final var serializedDeviceId = serializedEndPointId.getDeviceId();
        final var serializedId = serializedEndPointId.getEndpointUuid();

        final var topologyId = deserialize(serializedTopologyId);
        final var deviceId = deserialize(serializedDeviceId);
        final var id = deserialize(serializedId);

        return new EndPointId(topologyId, deviceId, id);
    }

    public Acl.AclRuleTypeEnum serialize(AclRuleTypeEnum aclRuleTypeEnum) {
        switch (aclRuleTypeEnum) {
            case IPV4:
                return Acl.AclRuleTypeEnum.ACLRULETYPE_IPV4;
            case IPV6:
                return Acl.AclRuleTypeEnum.ACLRULETYPE_IPV6;
            case L2:
                return Acl.AclRuleTypeEnum.ACLRULETYPE_L2;
            case MPLS:
                return Acl.AclRuleTypeEnum.ACLRULETYPE_MPLS;
            case MIXED:
                return Acl.AclRuleTypeEnum.ACLRULETYPE_MIXED;
            case UNDEFINED:
                return Acl.AclRuleTypeEnum.ACLRULETYPE_UNDEFINED;
            default:
                return Acl.AclRuleTypeEnum.UNRECOGNIZED;
        }
    }

    public AclRuleTypeEnum deserialize(Acl.AclRuleTypeEnum serializedAclRuleTypeEnum) {
        switch (serializedAclRuleTypeEnum) {
            case ACLRULETYPE_IPV4:
                return AclRuleTypeEnum.IPV4;
            case ACLRULETYPE_IPV6:
                return AclRuleTypeEnum.IPV6;
            case ACLRULETYPE_L2:
                return AclRuleTypeEnum.L2;
            case ACLRULETYPE_MPLS:
                return AclRuleTypeEnum.MPLS;
            case ACLRULETYPE_MIXED:
                return AclRuleTypeEnum.MIXED;
            case UNRECOGNIZED:
            default:
                return AclRuleTypeEnum.UNDEFINED;
        }
    }

    public Acl.AclMatch serialize(AclMatch aclMatch) {
        final var builder = Acl.AclMatch.newBuilder();

        final var dscp = aclMatch.getDscp();
        final var protocol = aclMatch.getProtocol();
        final var srcAddress = aclMatch.getSrcAddress();
        final var dstAddress = aclMatch.getDstAddress();
        final var srcPort = aclMatch.getSrcPort();
        final var dstPort = aclMatch.getDstPort();
        final var startMplsLabel = aclMatch.getStartMplsLabel();
        final var endMplsLabel = aclMatch.getEndMplsLabel();

        builder.setDscp(dscp);
        builder.setProtocol(protocol);
        builder.setSrcAddress(srcAddress);
        builder.setDstAddress(dstAddress);
        builder.setSrcPort(srcPort);
        builder.setDstPort(dstPort);
        builder.setStartMplsLabel(startMplsLabel);
        builder.setEndMplsLabel(endMplsLabel);

        return builder.build();
    }

    public AclMatch deserialize(Acl.AclMatch serializedAclMatch) {
        final var dscp = serializedAclMatch.getDscp();
        final var protocol = serializedAclMatch.getProtocol();
        final var srcAddress = serializedAclMatch.getSrcAddress();
        final var dstAddress = serializedAclMatch.getDstAddress();
        final var srcPort = serializedAclMatch.getSrcPort();
        final var dstPort = serializedAclMatch.getDstPort();
        final var startMplsLabel = serializedAclMatch.getStartMplsLabel();
        final var endMplsLabel = serializedAclMatch.getEndMplsLabel();

        return new AclMatch(
                dscp, protocol, srcAddress, dstAddress, srcPort, dstPort, startMplsLabel, endMplsLabel);
    }

    public Acl.AclForwardActionEnum serialize(AclForwardActionEnum aclForwardActionEnum) {
        switch (aclForwardActionEnum) {
            case DROP:
                return Acl.AclForwardActionEnum.ACLFORWARDINGACTION_DROP;
            case ACCEPT:
                return Acl.AclForwardActionEnum.ACLFORWARDINGACTION_ACCEPT;
            case REJECT:
                return Acl.AclForwardActionEnum.ACLFORWARDINGACTION_REJECT;
            case UNDEFINED:
                return Acl.AclForwardActionEnum.ACLFORWARDINGACTION_UNDEFINED;
            default:
                return Acl.AclForwardActionEnum.UNRECOGNIZED;
        }
    }

    public AclForwardActionEnum deserialize(Acl.AclForwardActionEnum serializedAclForwardActionEnum) {
        switch (serializedAclForwardActionEnum) {
            case ACLFORWARDINGACTION_DROP:
                return AclForwardActionEnum.DROP;
            case ACLFORWARDINGACTION_ACCEPT:
                return AclForwardActionEnum.ACCEPT;
            case ACLFORWARDINGACTION_REJECT:
                return AclForwardActionEnum.REJECT;
            case UNRECOGNIZED:
            default:
                return AclForwardActionEnum.UNDEFINED;
        }
    }

    public Acl.AclLogActionEnum serialize(AclLogActionEnum aclLogActionEnum) {
        switch (aclLogActionEnum) {
            case NO_LOG:
                return Acl.AclLogActionEnum.ACLLOGACTION_NOLOG;
            case SYSLOG:
                return Acl.AclLogActionEnum.ACLLOGACTION_SYSLOG;
            case UNDEFINED:
                return Acl.AclLogActionEnum.ACLLOGACTION_UNDEFINED;
            default:
                return Acl.AclLogActionEnum.UNRECOGNIZED;
        }
    }

    public AclLogActionEnum deserialize(Acl.AclLogActionEnum serializedAclLogActionEnum) {
        switch (serializedAclLogActionEnum) {
            case ACLLOGACTION_NOLOG:
                return AclLogActionEnum.NO_LOG;
            case ACLLOGACTION_SYSLOG:
                return AclLogActionEnum.SYSLOG;
            case UNRECOGNIZED:
            default:
                return AclLogActionEnum.UNDEFINED;
        }
    }

    public Acl.AclAction serialize(AclAction aclAction) {
        final var builder = Acl.AclAction.newBuilder();

        final var aclForwardActionEnum = aclAction.getAclForwardActionEnum();
        final var aclLogActionEnum = aclAction.getAclLogActionEnum();

        final var serializedAclForwardActionEnum = serialize(aclForwardActionEnum);
        final var serializedAclLogActionEnum = serialize(aclLogActionEnum);

        builder.setForwardAction(serializedAclForwardActionEnum);
        builder.setLogAction(serializedAclLogActionEnum);

        return builder.build();
    }

    public AclAction deserialize(Acl.AclAction serializedAclAction) {
        final var serializedAclForwardActionEnum = serializedAclAction.getForwardAction();
        final var serializedAclLogActionEnum = serializedAclAction.getLogAction();

        final var aclForwardActionEnum = deserialize(serializedAclForwardActionEnum);
        final var aclLogActionEnum = deserialize(serializedAclLogActionEnum);

        return new AclAction(aclForwardActionEnum, aclLogActionEnum);
    }

    public Acl.AclEntry serialize(AclEntry aclEntry) {
        final var builder = Acl.AclEntry.newBuilder();

        final var sequenceId = aclEntry.getSequenceId();
        final var description = aclEntry.getDescription();
        final var aclMatch = aclEntry.getMatch();
        final var aclAction = aclEntry.getAction();

        final var serializedAclMatch = serialize(aclMatch);
        final var serializedAclAction = serialize(aclAction);

        builder.setSequenceId(sequenceId);
        builder.setDescription(description);
        builder.setMatch(serializedAclMatch);
        builder.setAction(serializedAclAction);

        return builder.build();
    }

    public AclEntry deserialize(Acl.AclEntry serializedAclEntry) {
        final var sequenceId = serializedAclEntry.getSequenceId();
        final var description = serializedAclEntry.getDescription();
        final var serializedAclMatch = serializedAclEntry.getMatch();
        final var serializedAclAction = serializedAclEntry.getAction();

        final var aclMatch = deserialize(serializedAclMatch);
        final var aclAction = deserialize(serializedAclAction);

        return new AclEntry(sequenceId, description, aclMatch, aclAction);
    }

    public Acl.AclRuleSet serialize(AclRuleSet aclRuleSet) {
        final var builder = Acl.AclRuleSet.newBuilder();

        final var name = aclRuleSet.getName();
        final var type = aclRuleSet.getType();
        final var description = aclRuleSet.getDescription();
        final var userId = aclRuleSet.getUserId();
        final var entries = aclRuleSet.getEntries();

        final var serializedType = serialize(type);
        final var serializedEntries =
                entries.stream().map(this::serialize).collect(Collectors.toList());

        builder.setName(name);
        builder.setType(serializedType);
        builder.setDescription(description);
        builder.setUserId(userId);
        builder.addAllEntries(serializedEntries);

        return builder.build();
    }

    public AclRuleSet deserialize(Acl.AclRuleSet serializedAclRuleSet) {
        final var serializedName = serializedAclRuleSet.getName();
        final var serializedType = serializedAclRuleSet.getType();
        final var serializedDescription = serializedAclRuleSet.getDescription();
        final var serializedUserId = serializedAclRuleSet.getUserId();
        final var serializedEntries = serializedAclRuleSet.getEntriesList();

        final var type = deserialize(serializedType);
        final var entries =
                serializedEntries.stream().map(this::deserialize).collect(Collectors.toList());

        return new AclRuleSet(serializedName, type, serializedDescription, serializedUserId, entries);
    }

    public ConfigRule_ACL serialize(ConfigRuleAcl configRuleAcl) {
        final var builder = ContextOuterClass.ConfigRule_ACL.newBuilder();

        final var endPointId = configRuleAcl.getEndPointId();
        final var aclRuleSet = configRuleAcl.getRuleSet();

        final var serializedEndPointId = serialize(endPointId);
        final var serializedAclRuleSet = serialize(aclRuleSet);

        builder.setEndpointId(serializedEndPointId);
        builder.setRuleSet(serializedAclRuleSet);

        return builder.build();
    }

    public ConfigRuleAcl deserialize(ConfigRule_ACL serializedConfigRuleAcl) {
        final var serializedEndPointId = serializedConfigRuleAcl.getEndpointId();
        final var serializedAclRuleSet = serializedConfigRuleAcl.getRuleSet();

        final var endPointId = deserialize(serializedEndPointId);
        final var aclRuleSet = deserialize(serializedAclRuleSet);

        return new ConfigRuleAcl(endPointId, aclRuleSet);
    }

    public ConfigRule_Custom serialize(ConfigRuleCustom configRuleCustom) {
        final var builder = ConfigRule_Custom.newBuilder();

        final var resourceKey = configRuleCustom.getResourceKey();
        final var resourceValue = configRuleCustom.getResourceValue();

        builder.setResourceKey(resourceKey);
        builder.setResourceValue(resourceValue);

        return builder.build();
    }

    public ConfigRuleCustom deserialize(ConfigRule_Custom serializedConfigRuleCustom) {
        final var serializedResourceKey = serializedConfigRuleCustom.getResourceKey();
        final var serializedResourceValue = serializedConfigRuleCustom.getResourceValue();

        return new ConfigRuleCustom(serializedResourceKey, serializedResourceValue);
    }

    public ContextOuterClass.ConfigRule serialize(ConfigRule configRule) {
        final var builder = ContextOuterClass.ConfigRule.newBuilder();

        final var configActionEnum = configRule.getConfigActionEnum();
        final var configRuleType = configRule.getConfigRuleType();
        final var configRuleTypeSpecificType = configRuleType.getConfigRuleType();

        if (configRuleTypeSpecificType instanceof ConfigRuleAcl) {
            final var endPointId = ((ConfigRuleAcl) configRuleTypeSpecificType).getEndPointId();
            final var aclRuleSet = ((ConfigRuleAcl) configRuleTypeSpecificType).getRuleSet();

            final var serializedEndPointId = serialize(endPointId);
            final var serializedAclRuleSet = serialize(aclRuleSet);

            final var serializedConfigRuleAcl =
                    ConfigRule_ACL.newBuilder()
                            .setEndpointId(serializedEndPointId)
                            .setRuleSet(serializedAclRuleSet)
                            .build();

            builder.setAcl(serializedConfigRuleAcl);
        }

        if (configRuleTypeSpecificType instanceof ConfigRuleCustom) {
            final var configRuleCustomResourceKey =
                    ((ConfigRuleCustom) configRuleTypeSpecificType).getResourceKey();
            final var configRuleCustomResourceValue =
                    ((ConfigRuleCustom) configRuleTypeSpecificType).getResourceValue();

            final var serializedConfigRuleCustom =
                    ConfigRule_Custom.newBuilder()
                            .setResourceKey(configRuleCustomResourceKey)
                            .setResourceValue(configRuleCustomResourceValue)
                            .build();

            builder.setCustom(serializedConfigRuleCustom);
        }

        final var serializedConfigActionEnum = serialize(configActionEnum);

        builder.setAction(serializedConfigActionEnum);

        return builder.build();
    }

    public ConfigRule deserialize(ContextOuterClass.ConfigRule serializedConfigRule) {
        final var serializedConfigActionEnum = serializedConfigRule.getAction();
        final var typeOfConfigRule = serializedConfigRule.getConfigRuleCase();

        final var configActionEnum = deserialize(serializedConfigActionEnum);

        switch (typeOfConfigRule) {
            case ACL:
                final var serializedConfigRuleAcl = serializedConfigRule.getAcl();

                final var configRuleAcl = deserialize(serializedConfigRuleAcl);
                final var configRuleTypeAcl = new ConfigRuleTypeAcl(configRuleAcl);

                return new ConfigRule(configActionEnum, configRuleTypeAcl);
            case CUSTOM:
                final var serializedConfigRuleCustom = serializedConfigRule.getCustom();

                final var configRuleCustom = deserialize(serializedConfigRuleCustom);
                final var configRuleTypeCustom = new ConfigRuleTypeCustom(configRuleCustom);

                return new ConfigRule(configActionEnum, configRuleTypeCustom);
            default:
            case CONFIGRULE_NOT_SET:
                throw new IllegalStateException("Config Rule not set");
        }
    }

    public ContextOuterClass.DeviceConfig serialize(DeviceConfig deviceConfig) {
        final var builder = ContextOuterClass.DeviceConfig.newBuilder();

        final var serializedConfigRules =
                deviceConfig.getConfigRules().stream().map(this::serialize).collect(Collectors.toList());
        builder.addAllConfigRules(serializedConfigRules);

        return builder.build();
    }

    public DeviceConfig deserialize(ContextOuterClass.DeviceConfig deviceConfig) {
        final var configRules =
                deviceConfig.getConfigRulesList().stream()
                        .map(this::deserialize)
                        .collect(Collectors.toList());

        return new DeviceConfig(configRules);
    }

    public ContextOuterClass.DeviceOperationalStatusEnum serialize(DeviceOperationalStatus opStatus) {
        switch (opStatus) {
            case ENABLED:
                return DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED;
            case DISABLED:
                return DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED;
            case UNDEFINED:
            default:
                return DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED;
        }
    }

    public DeviceOperationalStatus deserialize(
            ContextOuterClass.DeviceOperationalStatusEnum opStatus) {
        switch (opStatus) {
            case DEVICEOPERATIONALSTATUS_ENABLED:
                return DeviceOperationalStatus.ENABLED;
            case DEVICEOPERATIONALSTATUS_DISABLED:
                return DeviceOperationalStatus.DISABLED;
            case DEVICEOPERATIONALSTATUS_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return DeviceOperationalStatus.UNDEFINED;
        }
    }

    public KpiSampleTypes.KpiSampleType serialize(KpiSampleType kpiSampleType) {
        switch (kpiSampleType) {
            case PACKETS_TRANSMITTED:
                return KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED;
            case PACKETS_RECEIVED:
                return KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED;
            case BYTES_TRANSMITTED:
                return KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED;
            case BYTES_RECEIVED:
                return KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED;
            case LINK_TOTAL_CAPACITY_GBPS:
                return KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_LINK_TOTAL_CAPACITY_GBPS;
            case LINK_USED_CAPACITY_GBPS:
                return KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS;
            case UNKNOWN:
                return KpiSampleTypes.KpiSampleType.KPISAMPLETYPE_UNKNOWN;
            default:
                return KpiSampleTypes.KpiSampleType.UNRECOGNIZED;
        }
    }

    public KpiSampleType deserialize(KpiSampleTypes.KpiSampleType serializedKpiSampleType) {
        switch (serializedKpiSampleType) {
            case KPISAMPLETYPE_PACKETS_TRANSMITTED:
                return KpiSampleType.PACKETS_TRANSMITTED;
            case KPISAMPLETYPE_PACKETS_RECEIVED:
                return KpiSampleType.PACKETS_RECEIVED;
            case KPISAMPLETYPE_BYTES_TRANSMITTED:
                return KpiSampleType.BYTES_TRANSMITTED;
            case KPISAMPLETYPE_BYTES_RECEIVED:
                return KpiSampleType.BYTES_RECEIVED;
            case KPISAMPLETYPE_LINK_TOTAL_CAPACITY_GBPS:
                return KpiSampleType.LINK_TOTAL_CAPACITY_GBPS;
            case KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS:
                return KpiSampleType.LINK_USED_CAPACITY_GBPS;
            case KPISAMPLETYPE_UNKNOWN:
            default:
                return KpiSampleType.UNKNOWN;
        }
    }

    public ContextOuterClass.Location serialize(Location location) {
        final var builder = ContextOuterClass.Location.newBuilder();

        final var locationType = location.getLocationType();
        final var locationTypeSpecificType = locationType.getLocationType();

        if (locationTypeSpecificType instanceof GpsPosition) {
            final var latitude = ((GpsPosition) locationTypeSpecificType).getLatitude();
            final var longitude = ((GpsPosition) locationTypeSpecificType).getLongitude();

            final var serializedGpsPosition =
                    ContextOuterClass.GPS_Position.newBuilder()
                            .setLatitude(latitude)
                            .setLongitude(longitude)
                            .build();

            builder.setGpsPosition(serializedGpsPosition);
        }

        if (locationTypeSpecificType instanceof String) {
            final var region = ((String) locationTypeSpecificType);

            builder.setRegion(region);
        }

        return builder.build();
    }

    public Location deserialize(ContextOuterClass.Location serializedLocation) {
        final var typeOfLocation = serializedLocation.getLocationCase();

        switch (typeOfLocation) {
            case REGION:
                final var region = serializedLocation.getRegion();
                final var locationTypeRegion = new LocationTypeRegion(region);

                return new Location(locationTypeRegion);
            case GPS_POSITION:
                final var serializedGpsPosition = serializedLocation.getGpsPosition();
                final var latitude = serializedGpsPosition.getLatitude();
                final var longitude = serializedGpsPosition.getLongitude();

                final var gpsPosition = new GpsPosition(latitude, longitude);
                final var locationTypeGpsPosition = new LocationTypeGpsPosition(gpsPosition);

                return new Location(locationTypeGpsPosition);
            default:
            case LOCATION_NOT_SET:
                throw new IllegalStateException("Location value not set");
        }
    }

    public ContextOuterClass.DeviceDriverEnum serialize(DeviceDriverEnum deviceDriverEnum) {
        switch (deviceDriverEnum) {
            case OPENCONFIG:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_OPENCONFIG;
            case TRANSPORT_API:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_TRANSPORT_API;
            case P4:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_P4;
            case IETF_NETWORK_TOPOLOGY:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_NETWORK_TOPOLOGY;
            case ONF_TR_532:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_ONF_TR_532;
            case XR:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_XR;
            case IETF_L2VPN:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_L2VPN;
            case GNMI_OPENCONFIG:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_GNMI_OPENCONFIG;
            case OPTICAL_TFS:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_OPTICAL_TFS;
            case IETF_ACTN:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_ACTN;
            case OC:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_OC;
            case QKD:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_QKD;
            case IETF_L3VPN:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_L3VPN;
            case IETF_SLICE:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_IETF_SLICE;
            case NCE:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_NCE;
            case SMARTNIC:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_SMARTNIC;
            case MORPHEUS:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_MORPHEUS;
            case RYU:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_RYU;
            case GNMI_NOKIA_SRLINUX:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_GNMI_NOKIA_SRLINUX;
            case OPENROADM:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_OPENROADM;
            case RESTCONF_OPENCONFIG:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_RESTCONF_OPENCONFIG;
            case UNDEFINED:
            default:
                return ContextOuterClass.DeviceDriverEnum.DEVICEDRIVER_UNDEFINED;
        }
    }

    public DeviceDriverEnum deserialize(
            ContextOuterClass.DeviceDriverEnum serializedDeviceDriverEnum) {
        switch (serializedDeviceDriverEnum) {
            case DEVICEDRIVER_OPENCONFIG:
                return DeviceDriverEnum.OPENCONFIG;
            case DEVICEDRIVER_TRANSPORT_API:
                return DeviceDriverEnum.TRANSPORT_API;
            case DEVICEDRIVER_P4:
                return DeviceDriverEnum.P4;
            case DEVICEDRIVER_IETF_NETWORK_TOPOLOGY:
                return DeviceDriverEnum.IETF_NETWORK_TOPOLOGY;
            case DEVICEDRIVER_ONF_TR_532:
                return DeviceDriverEnum.ONF_TR_532;
            case DEVICEDRIVER_XR:
                return DeviceDriverEnum.XR;
            case DEVICEDRIVER_IETF_L2VPN:
                return DeviceDriverEnum.IETF_L2VPN;
            case DEVICEDRIVER_GNMI_OPENCONFIG:
                return DeviceDriverEnum.GNMI_OPENCONFIG;
            case DEVICEDRIVER_OPTICAL_TFS:
                return DeviceDriverEnum.OPTICAL_TFS;
            case DEVICEDRIVER_IETF_ACTN:
                return DeviceDriverEnum.IETF_ACTN;
            case DEVICEDRIVER_OC:
                return DeviceDriverEnum.OC;
            case DEVICEDRIVER_QKD:
                return DeviceDriverEnum.QKD;
            case DEVICEDRIVER_IETF_L3VPN:
                return DeviceDriverEnum.IETF_L3VPN;
            case DEVICEDRIVER_IETF_SLICE:
                return DeviceDriverEnum.IETF_SLICE;
            case DEVICEDRIVER_NCE:
                return DeviceDriverEnum.NCE;
            case DEVICEDRIVER_SMARTNIC:
                return DeviceDriverEnum.SMARTNIC;
            case DEVICEDRIVER_MORPHEUS:
                return DeviceDriverEnum.MORPHEUS;
            case DEVICEDRIVER_RYU:
                return DeviceDriverEnum.RYU;
            case DEVICEDRIVER_GNMI_NOKIA_SRLINUX:
                return DeviceDriverEnum.GNMI_NOKIA_SRLINUX;
            case DEVICEDRIVER_OPENROADM:
                return DeviceDriverEnum.OPENROADM;
            case DEVICEDRIVER_RESTCONF_OPENCONFIG:
                return DeviceDriverEnum.RESTCONF_OPENCONFIG;
            case DEVICEDRIVER_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return DeviceDriverEnum.UNDEFINED;
        }
    }

    public ContextOuterClass.EndPoint serialize(EndPoint endPoint) {
        final var builder = ContextOuterClass.EndPoint.newBuilder();

        final var endPointId = endPoint.getEndPointId();
        final var endPointType = endPoint.getEndPointType();
        final var kpiSampleTypes = endPoint.getKpiSampleTypes();
        final var endPointLocation = endPoint.getEndPointLocation();

        final var serializedEndPointId = serialize(endPointId);
        final var serializedKpiSampleTypes =
                kpiSampleTypes.stream().map(this::serialize).collect(Collectors.toList());
        if (endPointLocation != null) {
            final var serializedEndPointLocation = serialize(endPointLocation);
            builder.setEndpointLocation(serializedEndPointLocation);
        }

        builder.setEndpointId(serializedEndPointId);
        builder.setEndpointType(endPointType);
        builder.addAllKpiSampleTypes(serializedKpiSampleTypes);

        return builder.build();
    }

    public EndPoint deserialize(ContextOuterClass.EndPoint serializedEndPoint) {
        final var serializedEndPointId = serializedEndPoint.getEndpointId();
        final var endPointType = serializedEndPoint.getEndpointType();
        final var serializedKpiSampleTypes = serializedEndPoint.getKpiSampleTypesList();
        final var serializedEndPointLocation = serializedEndPoint.getEndpointLocation();

        final var endPointId = deserialize(serializedEndPointId);
        final var kpiSampleTypes =
                serializedKpiSampleTypes.stream().map(this::deserialize).collect(Collectors.toList());

        if (serializedEndPointLocation.getLocationCase() != LocationCase.LOCATION_NOT_SET) {
            final var endPointLocation = deserialize(serializedEndPointLocation);
            return new EndPoint.EndPointBuilder(endPointId, endPointType, kpiSampleTypes)
                    .location(endPointLocation)
                    .build();
        }

        return new EndPoint.EndPointBuilder(endPointId, endPointType, kpiSampleTypes).build();
    }

    public ContextOuterClass.Device serialize(Device device) {
        final var builder = ContextOuterClass.Device.newBuilder();

        final var deviceIdUuid = serializeUuid(device.getDeviceId());
        final var deviceId = DeviceId.newBuilder().setDeviceUuid(deviceIdUuid);
        final var deviceName = device.getDeviceName();
        final var deviceType = device.getDeviceType();
        final var deviceConfig = device.getDeviceConfig();
        final var deviceOperationalStatus = device.getDeviceOperationalStatus();
        final var deviceDrivers = device.getDeviceDrivers();
        final var deviceEndPoints = device.getEndPoints();

        final var serializedDeviceConfig = serialize(deviceConfig);
        final var serializedDeviceOperationalStatus = serialize(deviceOperationalStatus);
        final var serializedDeviceDrivers =
                deviceDrivers.stream().map(this::serialize).collect(Collectors.toList());
        final var serializedDeviceEndPoints =
                deviceEndPoints.stream().map(this::serialize).collect(Collectors.toList());

        builder.setDeviceId(deviceId);
        builder.setName(deviceName);
        builder.setDeviceType(deviceType);
        builder.setDeviceConfig(serializedDeviceConfig);
        builder.setDeviceOperationalStatus(serializedDeviceOperationalStatus);
        builder.addAllDeviceDrivers(serializedDeviceDrivers);
        builder.addAllDeviceEndpoints(serializedDeviceEndPoints);

        return builder.build();
    }

    public Device deserialize(ContextOuterClass.Device device) {

        final var serializedDeviceId = device.getDeviceId();
        final var deviceName = device.getName();
        final var deviceType = device.getDeviceType();
        final var serializedDeviceConfig = device.getDeviceConfig();
        final var serializedDeviceOperationalStatus = device.getDeviceOperationalStatus();
        final var serializedDeviceDrivers = device.getDeviceDriversList();
        final var serializedDeviceEndPoints = device.getDeviceEndpointsList();

        final var deviceId = deserialize(serializedDeviceId);
        final var deviceConfig = deserialize(serializedDeviceConfig);
        final var deviceOperationalStatus = deserialize(serializedDeviceOperationalStatus);
        final var deviceDrivers =
                serializedDeviceDrivers.stream().map(this::deserialize).collect(Collectors.toList());
        final var deviceEndPoints =
                serializedDeviceEndPoints.stream().map(this::deserialize).collect(Collectors.toList());

        return new Device(
                deviceId,
                deviceName,
                deviceType,
                deviceConfig,
                deviceOperationalStatus,
                deviceDrivers,
                deviceEndPoints);
    }

    public ContextOuterClass.Empty serializeEmpty(Empty empty) {

        final var builder = ContextOuterClass.Empty.newBuilder();

        return builder.build();
    }

    public Empty deserializeEmpty(ContextOuterClass.Empty serializedEmpty) {
        return new Empty();
    }

    public Uuid serializeUuid(String uuid) {
        return Uuid.newBuilder().setUuid(uuid).build();
    }

    public String deserialize(Uuid uuid) {
        return uuid.getUuid();
    }
}
