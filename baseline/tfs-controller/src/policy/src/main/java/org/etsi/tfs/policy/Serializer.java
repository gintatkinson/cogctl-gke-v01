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
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import kpi_sample_types.KpiSampleTypes;
import monitoring.Monitoring;
import monitoring.Monitoring.AlarmID;
import monitoring.Monitoring.KpiId;
import monitoring.Monitoring.SubscriptionID;
import org.etsi.tfs.policy.acl.AclAction;
import org.etsi.tfs.policy.acl.AclEntry;
import org.etsi.tfs.policy.acl.AclForwardActionEnum;
import org.etsi.tfs.policy.acl.AclLogActionEnum;
import org.etsi.tfs.policy.acl.AclMatch;
import org.etsi.tfs.policy.acl.AclRuleSet;
import org.etsi.tfs.policy.acl.AclRuleTypeEnum;
import org.etsi.tfs.policy.context.model.*;
import org.etsi.tfs.policy.kpi_sample_types.model.KpiSampleType;
import org.etsi.tfs.policy.monitoring.model.AlarmDescriptor;
import org.etsi.tfs.policy.monitoring.model.AlarmResponse;
import org.etsi.tfs.policy.monitoring.model.AlarmSubscription;
import org.etsi.tfs.policy.monitoring.model.BooleanKpiValue;
import org.etsi.tfs.policy.monitoring.model.FloatKpiValue;
import org.etsi.tfs.policy.monitoring.model.IntegerKpiValue;
import org.etsi.tfs.policy.monitoring.model.Kpi;
import org.etsi.tfs.policy.monitoring.model.KpiDescriptor;
import org.etsi.tfs.policy.monitoring.model.KpiValue;
import org.etsi.tfs.policy.monitoring.model.KpiValueRange;
import org.etsi.tfs.policy.monitoring.model.LongKpiValue;
import org.etsi.tfs.policy.monitoring.model.MonitorKpiRequest;
import org.etsi.tfs.policy.monitoring.model.StringKpiValue;
import org.etsi.tfs.policy.monitoring.model.SubsDescriptor;
import org.etsi.tfs.policy.monitoring.model.SubsResponse;
import org.etsi.tfs.policy.policy.model.*;
import org.etsi.tfs.policy.policy.model.BooleanOperator;
import org.etsi.tfs.policy.policy.model.NumericalOperator;
import org.etsi.tfs.policy.policy.model.PolicyRule;
import org.etsi.tfs.policy.policy.model.PolicyRuleAction;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionConfig;
import org.etsi.tfs.policy.policy.model.PolicyRuleActionEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleBasic;
import org.etsi.tfs.policy.policy.model.PolicyRuleCondition;
import org.etsi.tfs.policy.policy.model.PolicyRuleDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleService;
import org.etsi.tfs.policy.policy.model.PolicyRuleState;
import org.etsi.tfs.policy.policy.model.PolicyRuleStateEnum;
import org.etsi.tfs.policy.policy.model.PolicyRuleTypeDevice;
import org.etsi.tfs.policy.policy.model.PolicyRuleTypeService;
import policy.Policy;
import policy.Policy.PolicyRuleId;
import policy.PolicyAction;
import policy.PolicyCondition;

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

    public ContextId serializeContextId(String expectedContextId) {
        final var builder = ContextId.newBuilder();
        final var uuid = serializeUuid(expectedContextId);

        builder.setContextUuid(uuid);

        return builder.build();
    }

    public String deserialize(ContextId contextId) {
        return contextId.getContextUuid().getUuid();
    }

    public PolicyRuleId serializePolicyRuleId(String expectedPolicyRuleId) {
        final var builder = PolicyRuleId.newBuilder();
        final var uuid = serializeUuid(expectedPolicyRuleId);

        builder.setUuid(uuid);

        return builder.build();
    }

    public String deserialize(PolicyRuleId policyRuleId) {
        return policyRuleId.getUuid().getUuid();
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

    public ContextOuterClass.ConfigActionEnum serialize(ConfigActionEnum configActionEnum) {
        switch (configActionEnum) {
            case SET:
                return ContextOuterClass.ConfigActionEnum.CONFIGACTION_SET;
            case DELETE:
                return ContextOuterClass.ConfigActionEnum.CONFIGACTION_DELETE;
            case UNDEFINED:
                return ContextOuterClass.ConfigActionEnum.CONFIGACTION_UNDEFINED;
            default:
                return ContextOuterClass.ConfigActionEnum.UNRECOGNIZED;
        }
    }

    public ConfigActionEnum deserialize(
            ContextOuterClass.ConfigActionEnum serializedConfigActionEnum) {
        switch (serializedConfigActionEnum) {
            case CONFIGACTION_SET:
                return ConfigActionEnum.SET;
            case CONFIGACTION_DELETE:
                return ConfigActionEnum.DELETE;
            case CONFIGACTION_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return ConfigActionEnum.UNDEFINED;
        }
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

    public ContextOuterClass.IsolationLevelEnum serialize(IsolationLevelEnum isolationLevelEnum) {
        switch (isolationLevelEnum) {
            case NO_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.NO_ISOLATION;
            case PHYSICAL_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.PHYSICAL_ISOLATION;
            case LOGICAL_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.LOGICAL_ISOLATION;
            case PROCESS_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.PROCESS_ISOLATION;
            case PHYSICAL_MEMORY_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.PHYSICAL_MEMORY_ISOLATION;
            case PHYSICAL_NETWORK_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.PHYSICAL_NETWORK_ISOLATION;
            case VIRTUAL_RESOURCE_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.VIRTUAL_RESOURCE_ISOLATION;
            case NETWORK_FUNCTIONS_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.NETWORK_FUNCTIONS_ISOLATION;
            case SERVICE_ISOLATION:
                return ContextOuterClass.IsolationLevelEnum.SERVICE_ISOLATION;
            default:
                return ContextOuterClass.IsolationLevelEnum.UNRECOGNIZED;
        }
    }

    public IsolationLevelEnum deserialize(
            ContextOuterClass.IsolationLevelEnum serializedIsolationLevelEnum) {
        switch (serializedIsolationLevelEnum) {
            case PHYSICAL_ISOLATION:
                return IsolationLevelEnum.PHYSICAL_ISOLATION;
            case LOGICAL_ISOLATION:
                return IsolationLevelEnum.LOGICAL_ISOLATION;
            case PROCESS_ISOLATION:
                return IsolationLevelEnum.PROCESS_ISOLATION;
            case PHYSICAL_MEMORY_ISOLATION:
                return IsolationLevelEnum.PHYSICAL_MEMORY_ISOLATION;
            case PHYSICAL_NETWORK_ISOLATION:
                return IsolationLevelEnum.PHYSICAL_NETWORK_ISOLATION;
            case VIRTUAL_RESOURCE_ISOLATION:
                return IsolationLevelEnum.VIRTUAL_RESOURCE_ISOLATION;
            case NETWORK_FUNCTIONS_ISOLATION:
                return IsolationLevelEnum.NETWORK_FUNCTIONS_ISOLATION;
            case SERVICE_ISOLATION:
                return IsolationLevelEnum.SERVICE_ISOLATION;
            case UNRECOGNIZED:
            default:
                return IsolationLevelEnum.NO_ISOLATION;
        }
    }

    public ContextOuterClass.Constraint_Custom serialize(ConstraintCustom constraintCustom) {
        final var builder = ContextOuterClass.Constraint_Custom.newBuilder();

        final var constraintType = constraintCustom.getConstraintType();
        final var constraintValue = constraintCustom.getConstraintValue();

        builder.setConstraintType(constraintType);
        builder.setConstraintValue(constraintValue);

        return builder.build();
    }

    public ConstraintCustom deserialize(
            ContextOuterClass.Constraint_Custom serializedConstraintCustom) {
        final var constraintType = serializedConstraintCustom.getConstraintType();
        final var constraintValue = serializedConstraintCustom.getConstraintValue();

        return new ConstraintCustom(constraintType, constraintValue);
    }

    public ContextOuterClass.Constraint_Schedule serialize(ConstraintSchedule constraintSchedule) {
        final var builder = ContextOuterClass.Constraint_Schedule.newBuilder();

        final var startTimestamp = constraintSchedule.getStartTimestamp();
        final var durationDays = constraintSchedule.getDurationDays();

        builder.setStartTimestamp(startTimestamp);
        builder.setDurationDays(durationDays);

        return builder.build();
    }

    public ConstraintSchedule deserialize(
            ContextOuterClass.Constraint_Schedule serializedConstraintSchedule) {
        final var startTimestamp = serializedConstraintSchedule.getStartTimestamp();
        final var durationDays = serializedConstraintSchedule.getDurationDays();

        return new ConstraintSchedule(startTimestamp, durationDays);
    }

    public ContextOuterClass.Constraint_EndPointLocation serialize(
            ConstraintEndPointLocation constraintEndPointLocation) {
        final var builder = ContextOuterClass.Constraint_EndPointLocation.newBuilder();

        final var endPointId = constraintEndPointLocation.getEndPointId();
        final var location = constraintEndPointLocation.getLocation();

        final var serializedEndPointId = serialize(endPointId);
        final var serializedLocation = serialize(location);

        builder.setEndpointId(serializedEndPointId);
        builder.setLocation(serializedLocation);

        return builder.build();
    }

    public ConstraintEndPointLocation deserialize(
            ContextOuterClass.Constraint_EndPointLocation serializedConstraintEndPointLocation) {
        final var serializedEndPointId = serializedConstraintEndPointLocation.getEndpointId();
        final var serializedLocation = serializedConstraintEndPointLocation.getLocation();

        final var endPointId = deserialize(serializedEndPointId);
        final var location = deserialize(serializedLocation);

        return new ConstraintEndPointLocation(endPointId, location);
    }

    public ContextOuterClass.Constraint_SLA_Availability serialize(
            ConstraintSlaAvailability constraintSlaAvailability) {
        final var builder = ContextOuterClass.Constraint_SLA_Availability.newBuilder();

        final var numDisjointPaths = constraintSlaAvailability.getNumDisjointPaths();
        final var isAllActive = constraintSlaAvailability.isAllActive();

        builder.setNumDisjointPaths(numDisjointPaths);
        builder.setAllActive(isAllActive);

        return builder.build();
    }

    public ConstraintSlaAvailability deserialize(
            ContextOuterClass.Constraint_SLA_Availability serializedConstraintSlaAvailability) {
        final var numDisjointPaths = serializedConstraintSlaAvailability.getNumDisjointPaths();
        final var isAllActive = serializedConstraintSlaAvailability.getAllActive();

        return new ConstraintSlaAvailability(numDisjointPaths, isAllActive);
    }

    public ContextOuterClass.Constraint_SLA_Capacity serialize(
            ConstraintSlaCapacity constraintSlaCapacity) {
        final var builder = ContextOuterClass.Constraint_SLA_Capacity.newBuilder();

        final var capacityGbps = constraintSlaCapacity.getCapacityGbps();

        builder.setCapacityGbps(capacityGbps);

        return builder.build();
    }

    public ConstraintSlaCapacity deserialize(
            ContextOuterClass.Constraint_SLA_Capacity serializedConstraintSlaCapacity) {
        final var capacityGbps = serializedConstraintSlaCapacity.getCapacityGbps();

        return new ConstraintSlaCapacity(capacityGbps);
    }

    public ContextOuterClass.Constraint_SLA_Isolation_level serialize(
            ConstraintSlaIsolationLevel constraintSlaIsolationLevel) {
        final var builder = ContextOuterClass.Constraint_SLA_Isolation_level.newBuilder();

        final var isolationLevelEnums = constraintSlaIsolationLevel.getIsolationLevelEnums();

        final var serializedIsolationLevelEnums =
                isolationLevelEnums.stream().map(this::serialize).collect(Collectors.toList());

        builder.addAllIsolationLevel(serializedIsolationLevelEnums);

        return builder.build();
    }

    public ConstraintSlaIsolationLevel deserialize(
            ContextOuterClass.Constraint_SLA_Isolation_level serializedConstraintIsolationLevel) {
        final var serializedIsolationLevelEnums =
                serializedConstraintIsolationLevel.getIsolationLevelList();

        final var isolationLevelEnums =
                serializedIsolationLevelEnums.stream().map(this::deserialize).collect(Collectors.toList());

        return new ConstraintSlaIsolationLevel(isolationLevelEnums);
    }

    public ContextOuterClass.Constraint_SLA_Latency serialize(
            ConstraintSlaLatency constraintSlaLatency) {
        final var builder = ContextOuterClass.Constraint_SLA_Latency.newBuilder();

        final var e2eLatencyMs = constraintSlaLatency.getE2eLatencyMs();

        builder.setE2ELatencyMs(e2eLatencyMs);

        return builder.build();
    }

    public ConstraintSlaLatency deserialize(
            ContextOuterClass.Constraint_SLA_Latency serializedConstraintSlaLatency) {
        final var e2ELatencyMs = serializedConstraintSlaLatency.getE2ELatencyMs();

        return new ConstraintSlaLatency(e2ELatencyMs);
    }

    public ContextOuterClass.Constraint serialize(Constraint constraint) {
        final var builder = ContextOuterClass.Constraint.newBuilder();

        final var constraintType = constraint.getConstraintType();
        final var constraintTypeSpecificType = constraintType.getConstraintType();

        if (constraintTypeSpecificType instanceof ConstraintCustom) {
            final var constraintCustomType =
                    ((ConstraintCustom) constraintTypeSpecificType).getConstraintType();
            final var constraintCustomValue =
                    ((ConstraintCustom) constraintTypeSpecificType).getConstraintValue();

            final var serializedConstraintCustom =
                    ContextOuterClass.Constraint_Custom.newBuilder()
                            .setConstraintType(constraintCustomType)
                            .setConstraintValue(constraintCustomValue)
                            .build();

            builder.setCustom(serializedConstraintCustom);
        }

        if (constraintTypeSpecificType instanceof ConstraintSchedule) {
            final var startTimestamp =
                    ((ConstraintSchedule) constraintTypeSpecificType).getStartTimestamp();
            final var durationDays = ((ConstraintSchedule) constraintTypeSpecificType).getDurationDays();

            final var serializedConstraintSchedule =
                    ContextOuterClass.Constraint_Schedule.newBuilder()
                            .setStartTimestamp(startTimestamp)
                            .setDurationDays(durationDays)
                            .build();

            builder.setSchedule(serializedConstraintSchedule);
        }

        if (constraintTypeSpecificType instanceof ConstraintEndPointLocation) {
            final var endPointId =
                    ((ConstraintEndPointLocation) constraintTypeSpecificType).getEndPointId();
            final var location = ((ConstraintEndPointLocation) constraintTypeSpecificType).getLocation();

            final var serializedEndPointId = serialize(endPointId);
            final var serializedLocation = serialize(location);

            final var serializedConstraintEndPointLocation =
                    ContextOuterClass.Constraint_EndPointLocation.newBuilder()
                            .setEndpointId(serializedEndPointId)
                            .setLocation(serializedLocation)
                            .build();

            builder.setEndpointLocation(serializedConstraintEndPointLocation);
        }

        if (constraintTypeSpecificType instanceof ConstraintSlaAvailability) {
            final var numDisJointPaths =
                    ((ConstraintSlaAvailability) constraintTypeSpecificType).getNumDisjointPaths();
            final var isAllActive =
                    ((ConstraintSlaAvailability) constraintTypeSpecificType).isAllActive();

            final var serializedConstraintSlaAvailability =
                    ContextOuterClass.Constraint_SLA_Availability.newBuilder()
                            .setNumDisjointPaths(numDisJointPaths)
                            .setAllActive(isAllActive)
                            .build();

            builder.setSlaAvailability(serializedConstraintSlaAvailability);
        }

        if (constraintTypeSpecificType instanceof ConstraintSlaCapacity) {
            final var capacityGbps =
                    ((ConstraintSlaCapacity) constraintTypeSpecificType).getCapacityGbps();

            final var serializedConstraintSlaCapacity =
                    ContextOuterClass.Constraint_SLA_Capacity.newBuilder()
                            .setCapacityGbps(capacityGbps)
                            .build();

            builder.setSlaCapacity(serializedConstraintSlaCapacity);
        }

        if (constraintTypeSpecificType instanceof ConstraintSlaIsolationLevel) {
            final var isolationLevelEnums =
                    ((ConstraintSlaIsolationLevel) constraintTypeSpecificType).getIsolationLevelEnums();

            final var serializedIsolationLevelEnums =
                    isolationLevelEnums.stream().map(this::serialize).collect(Collectors.toList());
            final var serializedConstraintSlaIsolationLevel =
                    ContextOuterClass.Constraint_SLA_Isolation_level.newBuilder()
                            .addAllIsolationLevel(serializedIsolationLevelEnums)
                            .build();

            builder.setSlaIsolation(serializedConstraintSlaIsolationLevel);
        }

        if (constraintTypeSpecificType instanceof ConstraintSlaLatency) {
            final var e2eLatencyMs =
                    ((ConstraintSlaLatency) constraintTypeSpecificType).getE2eLatencyMs();

            final var serializedConstraintSlaLatency =
                    ContextOuterClass.Constraint_SLA_Latency.newBuilder()
                            .setE2ELatencyMs(e2eLatencyMs)
                            .build();

            builder.setSlaLatency(serializedConstraintSlaLatency);
        }

        if (constraintTypeSpecificType instanceof ConstraintExclusions) {
            final var isPermanent = ((ConstraintExclusions) constraintTypeSpecificType).isPermanent();
            final var deviceIds = ((ConstraintExclusions) constraintTypeSpecificType).getDeviceIds();

            final var serializedDeviceIds =
                    deviceIds.stream().map(this::serializeDeviceId).collect(Collectors.toList());

            final var serializedConstraintExclusions =
                    ContextOuterClass.Constraint_Exclusions.newBuilder()
                            .setIsPermanent(isPermanent)
                            .addAllDeviceIds(serializedDeviceIds)
                            .build();

            builder.setExclusions(serializedConstraintExclusions);
        }

        return builder.build();
    }

    public Constraint deserialize(ContextOuterClass.Constraint serializedConstraint) {
        final var typeOfConstraint = serializedConstraint.getConstraintCase();

        switch (typeOfConstraint) {
            case CUSTOM:
                final var serializedConstraintCustom = serializedConstraint.getCustom();
                final var constraintType = serializedConstraintCustom.getConstraintType();
                final var constraintValue = serializedConstraintCustom.getConstraintValue();

                final var constraintCustom = new ConstraintCustom(constraintType, constraintValue);
                final var constraintTypeCustom = new ConstraintTypeCustom(constraintCustom);

                return new Constraint(constraintTypeCustom);
            case SCHEDULE:
                final var serializedConstraintSchedule = serializedConstraint.getSchedule();
                final var startTimestamp = serializedConstraintSchedule.getStartTimestamp();
                final var durationDays = serializedConstraintSchedule.getDurationDays();

                final var constraintSchedule = new ConstraintSchedule(startTimestamp, durationDays);
                final var constraintTypeSchedule = new ConstraintTypeSchedule(constraintSchedule);

                return new Constraint(constraintTypeSchedule);
            case ENDPOINT_LOCATION:
                final var serializedConstrainEndPointLocation = serializedConstraint.getEndpointLocation();
                final var serializedEndPointId = serializedConstrainEndPointLocation.getEndpointId();
                final var serializedLocation = serializedConstrainEndPointLocation.getLocation();

                final var endPointId = deserialize(serializedEndPointId);
                final var location = deserialize(serializedLocation);
                final var constraintEndPointLocation = new ConstraintEndPointLocation(endPointId, location);
                final var constraintTypeEndPointLocation =
                        new ConstraintTypeEndPointLocation(constraintEndPointLocation);

                return new Constraint(constraintTypeEndPointLocation);
            case SLA_CAPACITY:
                final var serializedConstrainSlaCapacity = serializedConstraint.getSlaCapacity();
                final var capacityGbps = serializedConstrainSlaCapacity.getCapacityGbps();

                final var constraintSlaCapacity = new ConstraintSlaCapacity(capacityGbps);
                final var constraintTypeSlaCapacity = new ConstraintTypeSlaCapacity(constraintSlaCapacity);

                return new Constraint(constraintTypeSlaCapacity);
            case SLA_LATENCY:
                final var serializedConstrainSlaLatency = serializedConstraint.getSlaLatency();
                final var e2ELatencyMs = serializedConstrainSlaLatency.getE2ELatencyMs();

                final var constraintSlaLatency = new ConstraintSlaLatency(e2ELatencyMs);
                final var constraintTypeSlaLatency = new ConstraintTypeSlaLatency(constraintSlaLatency);

                return new Constraint(constraintTypeSlaLatency);
            case SLA_AVAILABILITY:
                final var serializedConstrainSlaAvailability = serializedConstraint.getSlaAvailability();
                final var numDisjointPaths = serializedConstrainSlaAvailability.getNumDisjointPaths();
                final var isAllActive = serializedConstrainSlaAvailability.getAllActive();

                final var constraintSlaAvailability =
                        new ConstraintSlaAvailability(numDisjointPaths, isAllActive);
                final var constraintTypeSlaAvailability =
                        new ConstraintTypeSlaAvailability(constraintSlaAvailability);

                return new Constraint(constraintTypeSlaAvailability);
            case SLA_ISOLATION:
                final var serializedConstrainSlaIsolation = serializedConstraint.getSlaIsolation();
                final var serializedIsolationLevelEnums =
                        serializedConstrainSlaIsolation.getIsolationLevelList();

                final var isolationLevelEnums =
                        serializedIsolationLevelEnums.stream()
                                .map(this::deserialize)
                                .collect(Collectors.toList());
                final var constraintSlaIsolation = new ConstraintSlaIsolationLevel(isolationLevelEnums);
                final var constraintTypeSlaIsolation =
                        new ConstraintTypeSlaIsolationLevel(constraintSlaIsolation);

                return new Constraint(constraintTypeSlaIsolation);
            case EXCLUSIONS:
                final var exclusions = serializedConstraint.getExclusions();

                final var isPermanent = exclusions.getIsPermanent();
                final var serializedDevices = exclusions.getDeviceIdsList();

                final var deviceIds =
                        serializedDevices.stream().map(this::deserialize).collect(Collectors.toList());

                final var constraintExclusions =
                        new org.etsi.tfs.policy.context.model.ConstraintExclusions(
                                isPermanent, deviceIds, new ArrayList<>(), new ArrayList<>());
                final var constraintTypeExclusions =
                        new org.etsi.tfs.policy.context.model.ConstraintTypeExclusions(constraintExclusions);
                return new Constraint(constraintTypeExclusions);

            default:
            case CONSTRAINT_NOT_SET:
                throw new IllegalStateException("Constraint value not set");
        }
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

    public ContextOuterClass.ServiceId serialize(ServiceId serviceId) {
        final var builder = ContextOuterClass.ServiceId.newBuilder();

        final var contextId = serviceId.getContextId();
        final var id = serviceId.getId();

        final var serializedContextId = serializeContextId(contextId);
        final var serializedId = serializeUuid(id);

        builder.setContextId(serializedContextId);
        builder.setServiceUuid(serializedId);

        return builder.build();
    }

    public ServiceId deserialize(ContextOuterClass.ServiceId serializedServiceId) {
        final var serializedContextId = serializedServiceId.getContextId();
        final var serializedId = serializedServiceId.getServiceUuid();

        final var contextId = deserialize(serializedContextId);
        final var id = deserialize(serializedId);

        return new ServiceId(contextId, id);
    }

    public ContextOuterClass.SliceId serialize(SliceId sliceId) {
        final var builder = ContextOuterClass.SliceId.newBuilder();

        final var contextId = sliceId.getContextId();
        final var id = sliceId.getId();

        final var serializedContextId = serializeContextId(contextId);
        final var serializedId = serializeUuid(id);

        builder.setContextId(serializedContextId);
        builder.setSliceUuid(serializedId);

        return builder.build();
    }

    public SliceId deserialize(ContextOuterClass.SliceId serializedSliceId) {
        final var serializedContextId = serializedSliceId.getContextId();
        final var serializedId = serializedSliceId.getSliceUuid();

        final var contextId = deserialize(serializedContextId);
        final var id = deserialize(serializedId);

        return new SliceId(contextId, id);
    }

    public ContextOuterClass.ServiceStatusEnum serialize(ServiceStatusEnum serviceStatusEnum) {
        switch (serviceStatusEnum) {
            case ACTIVE:
                return ContextOuterClass.ServiceStatusEnum.SERVICESTATUS_ACTIVE;
            case PLANNED:
                return ContextOuterClass.ServiceStatusEnum.SERVICESTATUS_PLANNED;
            case PENDING_REMOVAL:
                return ContextOuterClass.ServiceStatusEnum.SERVICESTATUS_PENDING_REMOVAL;
            case SLA_VIOLATED:
                return ContextOuterClass.ServiceStatusEnum.SERVICESTATUS_SLA_VIOLATED;
            case UNDEFINED:
                return ContextOuterClass.ServiceStatusEnum.SERVICESTATUS_UNDEFINED;
            case UPDATING:
                return ContextOuterClass.ServiceStatusEnum.SERVICESTATUS_UPDATING;
            default:
                return ContextOuterClass.ServiceStatusEnum.UNRECOGNIZED;
        }
    }

    public ServiceStatusEnum deserialize(
            ContextOuterClass.ServiceStatusEnum serializedServiceStatusEnum) {
        switch (serializedServiceStatusEnum) {
            case SERVICESTATUS_ACTIVE:
                return ServiceStatusEnum.ACTIVE;
            case SERVICESTATUS_PLANNED:
                return ServiceStatusEnum.PLANNED;
            case SERVICESTATUS_PENDING_REMOVAL:
                return ServiceStatusEnum.PENDING_REMOVAL;
            case SERVICESTATUS_SLA_VIOLATED:
                return ServiceStatusEnum.SLA_VIOLATED;
            case SERVICESTATUS_UPDATING:
                return ServiceStatusEnum.UPDATING;
            case SERVICESTATUS_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return ServiceStatusEnum.UNDEFINED;
        }
    }

    public ContextOuterClass.ServiceTypeEnum serialize(ServiceTypeEnum serviceTypeEnum) {
        switch (serviceTypeEnum) {
            case L3NM:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_L3NM;
            case L2NM:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_L2NM;
            case TAPI_CONNECTIVITY_SERVICE:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE;
            case TE:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_TE;
            case E2E:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_E2E;
            case OPTICAL_CONNECTIVITY:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY;
            case QKD:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_QKD;
            case L1NM:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_L1NM;
            case INT:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_INT;
            case ACL:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_ACL;
            case IP_LINK:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_IP_LINK;
            case IPOWDM:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_IPOWDM;
            case TAPI_LSP:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_TAPI_LSP;
            case UNKNOWN:
                return ContextOuterClass.ServiceTypeEnum.SERVICETYPE_UNKNOWN;
            default:
                return ContextOuterClass.ServiceTypeEnum.UNRECOGNIZED;
        }
    }

    public ServiceTypeEnum deserialize(ContextOuterClass.ServiceTypeEnum serializedServiceTypeEnum) {
        switch (serializedServiceTypeEnum) {
            case SERVICETYPE_L3NM:
                return ServiceTypeEnum.L3NM;
            case SERVICETYPE_L2NM:
                return ServiceTypeEnum.L2NM;
            case SERVICETYPE_TAPI_CONNECTIVITY_SERVICE:
                return ServiceTypeEnum.TAPI_CONNECTIVITY_SERVICE;
            case SERVICETYPE_TE:
                return ServiceTypeEnum.TE;
            case SERVICETYPE_E2E:
                return ServiceTypeEnum.E2E;
            case SERVICETYPE_OPTICAL_CONNECTIVITY:
                return ServiceTypeEnum.OPTICAL_CONNECTIVITY;
            case SERVICETYPE_QKD:
                return ServiceTypeEnum.QKD;
            case SERVICETYPE_L1NM:
                return ServiceTypeEnum.L1NM;
            case SERVICETYPE_INT:
                return ServiceTypeEnum.INT;
            case SERVICETYPE_ACL:
                return ServiceTypeEnum.ACL;
            case SERVICETYPE_IP_LINK:
                return ServiceTypeEnum.IP_LINK;
            case SERVICETYPE_IPOWDM:
                return ServiceTypeEnum.IPOWDM;
            case SERVICETYPE_TAPI_LSP:
                return ServiceTypeEnum.TAPI_LSP;
            case SERVICETYPE_UNKNOWN:
            case UNRECOGNIZED:
            default:
                return ServiceTypeEnum.UNKNOWN;
        }
    }

    public ContextOuterClass.ServiceStatus serialize(ServiceStatus serviceStatus) {
        final var builder = ContextOuterClass.ServiceStatus.newBuilder();

        final var serviceStatusEnum = serviceStatus.getServiceStatus();
        final var serializedServiceStatusEnum = serialize(serviceStatusEnum);

        builder.setServiceStatus(serializedServiceStatusEnum);

        return builder.build();
    }

    public ServiceStatus deserialize(ContextOuterClass.ServiceStatus serializedServiceStatus) {
        final var serializedServiceStatusEnum = serializedServiceStatus.getServiceStatus();
        final var serviceStatusEnum = deserialize(serializedServiceStatusEnum);

        return new ServiceStatus(serviceStatusEnum);
    }

    public ContextOuterClass.ServiceConfig serialize(ServiceConfig serviceConfig) {
        final var builder = ContextOuterClass.ServiceConfig.newBuilder();

        final var serializedConfigRules =
                serviceConfig.getConfigRules().stream().map(this::serialize).collect(Collectors.toList());

        builder.addAllConfigRules(serializedConfigRules);

        return builder.build();
    }

    public ServiceConfig deserialize(ContextOuterClass.ServiceConfig serviceConfig) {
        final var configRules =
                serviceConfig.getConfigRulesList().stream()
                        .map(this::deserialize)
                        .collect(Collectors.toList());

        return new ServiceConfig(configRules);
    }

    public ContextOuterClass.Service serialize(Service service) {
        final var builder = ContextOuterClass.Service.newBuilder();

        final var serviceId = service.getServiceId();
        final var serviceType = service.getServiceType();
        final var serviceEndPointIds = service.getServiceEndPointIds();
        final var serviceConstraints = service.getServiceConstraints();
        final var serviceStatus = service.getServiceStatus();
        final var serviceConfig = service.getServiceConfig();
        final var serviceTimestamp = service.getTimestamp();

        final var serializedServiceId = serialize(serviceId);
        final var serializedServiceType = serialize(serviceType);
        final var serializedServiceEndPointIds =
                serviceEndPointIds.stream().map(this::serialize).collect(Collectors.toList());
        final var serializedServiceConstraints =
                serviceConstraints.stream().map(this::serialize).collect(Collectors.toList());
        final var serializedServiceStatus = serialize(serviceStatus);
        final var serializedServiceConfig = serialize(serviceConfig);
        final var serializedTimestamp = serialize(serviceTimestamp);

        builder.setServiceId(serializedServiceId);
        builder.setServiceType(serializedServiceType);
        builder.addAllServiceEndpointIds(serializedServiceEndPointIds);
        builder.addAllServiceConstraints(serializedServiceConstraints);
        builder.setServiceStatus(serializedServiceStatus);
        builder.setServiceConfig(serializedServiceConfig);
        builder.setTimestamp(serializedTimestamp);

        return builder.build();
    }

    public Service deserialize(ContextOuterClass.Service serializedService) {

        final var serializedServiceId = serializedService.getServiceId();
        final var serializedServiceType = serializedService.getServiceType();
        final var serializedServiceEndPointIds = serializedService.getServiceEndpointIdsList();
        final var serializedServiceConstraints = serializedService.getServiceConstraintsList();
        final var serializedServiceStatus = serializedService.getServiceStatus();
        final var serializedServiceConfig = serializedService.getServiceConfig();
        final var serializedTimestamp = serializedService.getTimestamp();

        final var serviceId = deserialize(serializedServiceId);
        final var serviceType = deserialize(serializedServiceType);
        final var serviceEndPointIds =
                serializedServiceEndPointIds.stream().map(this::deserialize).collect(Collectors.toList());
        final var serviceConstraints =
                serializedServiceConstraints.stream().map(this::deserialize).collect(Collectors.toList());
        final var serviceStatus = deserialize(serializedServiceStatus);
        final var serviceConfig = deserialize(serializedServiceConfig);
        final var timestamp = deserialize(serializedTimestamp);

        return new Service(
                serviceId,
                serviceType,
                serviceEndPointIds,
                serviceConstraints,
                serviceStatus,
                serviceConfig,
                timestamp);
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

    public Policy.PolicyRuleStateEnum serialize(PolicyRuleStateEnum policyRuleStateEnum) {
        switch (policyRuleStateEnum) {
            case POLICY_FAILED:
                return Policy.PolicyRuleStateEnum.POLICY_FAILED;
            case POLICY_INSERTED:
                return Policy.PolicyRuleStateEnum.POLICY_INSERTED;
            case POLICY_VALIDATED:
                return Policy.PolicyRuleStateEnum.POLICY_VALIDATED;
            case POLICY_PROVISIONED:
                return Policy.PolicyRuleStateEnum.POLICY_PROVISIONED;
            case POLICY_ACTIVE:
                return Policy.PolicyRuleStateEnum.POLICY_ACTIVE;
            case POLICY_ENFORCED:
                return Policy.PolicyRuleStateEnum.POLICY_ENFORCED;
            case POLICY_INEFFECTIVE:
                return Policy.PolicyRuleStateEnum.POLICY_INEFFECTIVE;
            case POLICY_EFFECTIVE:
                return Policy.PolicyRuleStateEnum.POLICY_EFFECTIVE;
            case POLICY_UPDATED:
                return Policy.PolicyRuleStateEnum.POLICY_UPDATED;
            case POLICY_REMOVED:
                return Policy.PolicyRuleStateEnum.POLICY_REMOVED;
            case POLICY_UNDEFINED:
                return Policy.PolicyRuleStateEnum.POLICY_UNDEFINED;
            default:
                return Policy.PolicyRuleStateEnum.UNRECOGNIZED;
        }
    }

    public PolicyRuleStateEnum deserialize(Policy.PolicyRuleStateEnum serializedPolicyRuleStateEnum) {
        switch (serializedPolicyRuleStateEnum) {
            case POLICY_INSERTED:
                return PolicyRuleStateEnum.POLICY_INSERTED;
            case POLICY_VALIDATED:
                return PolicyRuleStateEnum.POLICY_VALIDATED;
            case POLICY_PROVISIONED:
                return PolicyRuleStateEnum.POLICY_PROVISIONED;
            case POLICY_ACTIVE:
                return PolicyRuleStateEnum.POLICY_ACTIVE;
            case POLICY_ENFORCED:
                return PolicyRuleStateEnum.POLICY_ENFORCED;
            case POLICY_INEFFECTIVE:
                return PolicyRuleStateEnum.POLICY_INEFFECTIVE;
            case POLICY_EFFECTIVE:
                return PolicyRuleStateEnum.POLICY_EFFECTIVE;
            case POLICY_UPDATED:
                return PolicyRuleStateEnum.POLICY_UPDATED;
            case POLICY_REMOVED:
                return PolicyRuleStateEnum.POLICY_REMOVED;
            case POLICY_FAILED:
                return PolicyRuleStateEnum.POLICY_FAILED;
            case POLICY_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return PolicyRuleStateEnum.POLICY_UNDEFINED;
        }
    }

    public Policy.PolicyRuleState serialize(PolicyRuleState policyRuleState) {
        final var builder = Policy.PolicyRuleState.newBuilder();

        final var ruleState = policyRuleState.getRuleState();
        final var policyRuleStateMessage = policyRuleState.getPolicyRuleStateMessage();

        final var serializedRuleState = serialize(ruleState);

        builder.setPolicyRuleState(serializedRuleState);
        builder.setPolicyRuleStateMessage(policyRuleStateMessage);

        return builder.build();
    }

    public PolicyRuleState deserialize(Policy.PolicyRuleState serializedPolicyRuleState) {
        final var serializedRuleState = serializedPolicyRuleState.getPolicyRuleState();
        final var serializedRuleStateMessage = serializedPolicyRuleState.getPolicyRuleStateMessage();

        final var ruleState = deserialize(serializedRuleState);

        return new PolicyRuleState(ruleState, serializedRuleStateMessage);
    }

    public PolicyCondition.NumericalOperator serialize(NumericalOperator numericalOperator) {
        switch (numericalOperator) {
            case POLICY_RULE_CONDITION_NUMERICAL_EQUAL:
                return PolicyCondition.NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_EQUAL;
            case POLICY_RULE_CONDITION_NUMERICAL_NOT_EQUAL:
                return PolicyCondition.NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_NOT_EQUAL;
            case POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN:
                return PolicyCondition.NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_LESS_THAN;
            case POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN_EQUAL:
                return PolicyCondition.NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_LESS_THAN_EQUAL;
            case POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN:
                return PolicyCondition.NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_GREATER_THAN;
            case POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL:
                return PolicyCondition.NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL;
            case POLICY_RULE_CONDITION_NUMERICAL_UNDEFINED:
                return PolicyCondition.NumericalOperator.POLICYRULE_CONDITION_NUMERICAL_UNDEFINED;
            default:
                return PolicyCondition.NumericalOperator.UNRECOGNIZED;
        }
    }

    public NumericalOperator deserialize(
            PolicyCondition.NumericalOperator serializedNumericalOperator) {
        switch (serializedNumericalOperator) {
            case POLICYRULE_CONDITION_NUMERICAL_EQUAL:
                return NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_EQUAL;
            case POLICYRULE_CONDITION_NUMERICAL_NOT_EQUAL:
                return NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_NOT_EQUAL;
            case POLICYRULE_CONDITION_NUMERICAL_LESS_THAN:
                return NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN;
            case POLICYRULE_CONDITION_NUMERICAL_LESS_THAN_EQUAL:
                return NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_LESS_THAN_EQUAL;
            case POLICYRULE_CONDITION_NUMERICAL_GREATER_THAN:
                return NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN;
            case POLICYRULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL:
                return NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_GREATER_THAN_EQUAL;
            case POLICYRULE_CONDITION_NUMERICAL_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return NumericalOperator.POLICY_RULE_CONDITION_NUMERICAL_UNDEFINED;
        }
    }

    public Monitoring.KpiValue serializeStringKpiValue(KpiValue<String> kpiValue) {
        final var builder = Monitoring.KpiValue.newBuilder();

        return builder.setStringVal(kpiValue.getValue()).build();
    }

    public String deserializeStringKpiValue(Monitoring.KpiValue serializedKpiValue) {

        return serializedKpiValue.getStringVal();
    }

    public Monitoring.KpiValue serializeBooleanKpiValue(KpiValue<Boolean> kpiValue) {
        final var builder = Monitoring.KpiValue.newBuilder();

        return builder.setBoolVal(kpiValue.getValue()).build();
    }

    public boolean deserializeBooleanKpiValue(Monitoring.KpiValue serializedKpiValue) {

        return serializedKpiValue.getBoolVal();
    }

    public Monitoring.KpiValue serializeFloatKpiValue(KpiValue<Float> kpiValue) {
        final var builder = Monitoring.KpiValue.newBuilder();

        return builder.setFloatVal(kpiValue.getValue()).build();
    }

    public float deserializeFloatKpiValue(Monitoring.KpiValue serializedKpiValue) {

        return serializedKpiValue.getFloatVal();
    }

    public Monitoring.KpiValue serializeIntegerKpiValue(KpiValue<Integer> kpiValue) {
        final var builder = Monitoring.KpiValue.newBuilder();

        return builder.setInt32Val(kpiValue.getValue()).build();
    }

    public Monitoring.KpiValue serializeLongKpiValue(KpiValue<Long> kpiValue) {
        final var builder = Monitoring.KpiValue.newBuilder();

        return builder.setInt64Val(kpiValue.getValue()).build();
    }

    public int deserializeIntegerKpiValue(Monitoring.KpiValue serializedKpiValue) {

        return serializedKpiValue.getInt32Val();
    }

    public Monitoring.KpiValue serialize(KpiValue<?> kpiValue) {
        final var builder = Monitoring.KpiValue.newBuilder();

        if (kpiValue.getValue() instanceof Integer) {
            final var serializedIntegerKpiValue = serializeIntegerKpiValue((KpiValue<Integer>) kpiValue);
            builder.setInt32Val(serializedIntegerKpiValue.getInt32Val());
        }
        if (kpiValue.getValue() instanceof Long) {
            final var serializedIntegerKpiValue = serializeLongKpiValue((KpiValue<Long>) kpiValue);
            builder.setInt64Val(serializedIntegerKpiValue.getInt64Val());
        }
        if (kpiValue.getValue() instanceof Float) {
            final var serializedFloatKpiValue = serializeFloatKpiValue((KpiValue<Float>) kpiValue);
            builder.setFloatVal(serializedFloatKpiValue.getFloatVal());
        }
        if (kpiValue.getValue() instanceof String) {
            final var serializedStringKpiValue = serializeStringKpiValue((KpiValue<String>) kpiValue);
            builder.setStringVal(serializedStringKpiValue.getStringVal());
        }
        if (kpiValue.getValue() instanceof Boolean) {
            final var serializedBooleanKpiValue = serializeBooleanKpiValue((KpiValue<Boolean>) kpiValue);
            builder.setBoolVal(serializedBooleanKpiValue.getBoolVal());
        }

        return builder.build();
    }

    public KpiValue deserialize(Monitoring.KpiValue serializedKpiValue) {

        final var typeOfKpiValue = serializedKpiValue.getValueCase();

        switch (typeOfKpiValue) {
            case INT32VAL:
                final var intValue = deserializeIntegerKpiValue(serializedKpiValue);
                return new IntegerKpiValue(intValue);
            case UINT32VAL:
                final var uintValue = deserializeIntegerKpiValue(serializedKpiValue);
                return new IntegerKpiValue(uintValue);
            case INT64VAL:
                final var longValue = deserializeIntegerKpiValue(serializedKpiValue);
                return new LongKpiValue(longValue);
            case UINT64VAL:
                final var ulongValue = deserializeIntegerKpiValue(serializedKpiValue);
                return new LongKpiValue(ulongValue);
            case BOOLVAL:
                final var booleanValue = deserializeBooleanKpiValue(serializedKpiValue);
                return new BooleanKpiValue(booleanValue);
            case FLOATVAL:
                final var floatValue = deserializeFloatKpiValue(serializedKpiValue);
                return new FloatKpiValue(floatValue);
            case STRINGVAL:
                final var stringValue = deserializeStringKpiValue(serializedKpiValue);
                return new StringKpiValue(stringValue);
            default:
            case VALUE_NOT_SET:
                throw new IllegalStateException("Kpi value not set");
        }
    }

    public Monitoring.KpiValueRange serialize(KpiValueRange kpiValueRange) {
        final var builder = Monitoring.KpiValueRange.newBuilder();

        final var kpiValueMin = kpiValueRange.getKpiMinValue();
        final var kpiValueMax = kpiValueRange.getKpiMaxValue();

        Monitoring.KpiValue serializedKpiValueMin;
        Monitoring.KpiValue serializedKpiValueMax;

        if (kpiValueMin == null && kpiValueMax == null) {
            throw new IllegalStateException("KPI value max and min cannot be both null");
        } else if (kpiValueMax == null) {
            serializedKpiValueMin = serialize(kpiValueMin);
            serializedKpiValueMax = serialize(new StringKpiValue("NaN"));
        } else if (kpiValueMin == null) {
            serializedKpiValueMin = serialize(new StringKpiValue("NaN"));
            serializedKpiValueMax = serialize(kpiValueMax);
        } else {
            serializedKpiValueMin = serialize(kpiValueMin);
            serializedKpiValueMax = serialize(kpiValueMax);
        }

        builder.setKpiMinValue(serializedKpiValueMin);
        builder.setKpiMaxValue(serializedKpiValueMax);

        return builder.build();
    }

    public KpiValueRange deserialize(Monitoring.KpiValueRange serializedKpiValueRange) {
        final var serializedMinKpiValue = serializedKpiValueRange.getKpiMinValue();
        final var serializedMaxKpiValue = serializedKpiValueRange.getKpiMaxValue();
        final var serializedInRange = serializedKpiValueRange.getInRange();
        final var serializedMaxValue = serializedKpiValueRange.getIncludeMaxValue();
        final var serializedMinValue = serializedKpiValueRange.getIncludeMinValue();

        final var minKpiValue = deserialize(serializedMinKpiValue);
        final var maxKpiValue = deserialize(serializedMaxKpiValue);

        return new KpiValueRange(
                minKpiValue, maxKpiValue, serializedInRange, serializedMaxValue, serializedMinValue);
    }

    public AlarmID serializeAlarmId(String alarmId) {
        final var builder = Monitoring.AlarmID.newBuilder();

        final var serializedAlarmIdUuid = serializeUuid(alarmId);
        builder.setAlarmId(serializedAlarmIdUuid);

        return builder.build();
    }

    public String deserialize(AlarmID serializedAlarmId) {
        final var serializedAlarmIdUuid = serializedAlarmId.getAlarmId();

        return deserialize(serializedAlarmIdUuid);
    }

    public Monitoring.AlarmDescriptor serialize(AlarmDescriptor alarmDescriptor) {
        final var builder = Monitoring.AlarmDescriptor.newBuilder();

        final var alarmId = alarmDescriptor.getAlarmId();
        final var alarmDescription = alarmDescriptor.getAlarmDescription();
        final var name = alarmDescriptor.getName();
        final var kpiId = alarmDescriptor.getKpiId();
        final var kpiValueRange = alarmDescriptor.getKpiValueRange();
        final var timestamp = alarmDescriptor.getTimestamp();

        final var serializedAlarmId = serializeAlarmId(alarmId);
        final var serializedKpiId = serializeKpiId(kpiId);
        final var serializedKpiValueRange = serialize(kpiValueRange);
        final var serializedTimestamp = serialize(timestamp);

        builder.setAlarmId(serializedAlarmId);
        builder.setAlarmDescription(alarmDescription);
        builder.setName(name);
        builder.setKpiId(serializedKpiId);
        builder.setKpiValueRange(serializedKpiValueRange);
        builder.setTimestamp(serializedTimestamp);

        return builder.build();
    }

    public AlarmDescriptor deserialize(Monitoring.AlarmDescriptor serializedAlarmDescriptor) {

        final var serializedAlarmId = serializedAlarmDescriptor.getAlarmId();
        final var alarmDescription = serializedAlarmDescriptor.getAlarmDescription();
        final var name = serializedAlarmDescriptor.getName();
        final var serializedKpiId = serializedAlarmDescriptor.getKpiId();
        final var serializedKpiValueRange = serializedAlarmDescriptor.getKpiValueRange();
        final var serializeTimestamp = serializedAlarmDescriptor.getTimestamp();

        final var alarmId = deserialize(serializedAlarmId);
        final var kpiId = deserialize(serializedKpiId);
        final var kpiValueRange = deserialize(serializedKpiValueRange);
        final var timestamp = deserialize(serializeTimestamp);

        return new AlarmDescriptor(alarmId, alarmDescription, name, kpiId, kpiValueRange, timestamp);
    }

    public Monitoring.AlarmResponse serialize(AlarmResponse alarmResponse) {
        final var builder = Monitoring.AlarmResponse.newBuilder();

        final var alarmId = alarmResponse.getAlarmId();
        final var kpiList = alarmResponse.getKpiList();

        final var serializedAlarmIdUuid = serializeUuid(alarmId);
        final var serializedAlarmId =
                Monitoring.AlarmID.newBuilder().setAlarmId(serializedAlarmIdUuid).build();
        final var serializedKpis = kpiList.stream().map(this::serialize).collect(Collectors.toList());
        final var serializedKpisList = Monitoring.KpiList.newBuilder().addAllKpi(serializedKpis);

        builder.setAlarmId(serializedAlarmId);
        builder.setKpiList(serializedKpisList);

        return builder.build();
    }

    public Monitoring.SubsResponse serialize(SubsResponse subsResponse) {
        final var builder = Monitoring.SubsResponse.newBuilder();

        final var subscriptionId = subsResponse.getSubscriptionId();
        final var kpiList = subsResponse.getKpiList();

        final var serializedSubscriptionIdUuid = serializeSubscriptionIdId(subscriptionId);
        final var serializedKpis = kpiList.stream().map(this::serialize).collect(Collectors.toList());
        final var serializedKpisList = Monitoring.KpiList.newBuilder().addAllKpi(serializedKpis);

        builder.setSubsId(serializedSubscriptionIdUuid);
        builder.setKpiList(serializedKpisList);

        return builder.build();
    }

    public AlarmResponse deserialize(Monitoring.AlarmResponse serializedAlarmResponse) {
        final var serializedAlarmId = serializedAlarmResponse.getAlarmId().getAlarmId();
        final var serializedKpiList = serializedAlarmResponse.getKpiList();
        final var listSerializedKpis = serializedKpiList.getKpiList();

        final var alarmId = deserialize(serializedAlarmId);
        final var kpisList =
                listSerializedKpis.stream().map(this::deserialize).collect(Collectors.toList());

        return new AlarmResponse(alarmId, kpisList);
    }

    public Monitoring.MonitorKpiRequest serialize(MonitorKpiRequest monitorKpiRequest) {
        final var builder = Monitoring.MonitorKpiRequest.newBuilder();

        final var kpiId = monitorKpiRequest.getKpiId();
        final var monitoringWindow = monitorKpiRequest.getMonitoringWindow();
        final var samplingRate = monitorKpiRequest.getSamplingRate();

        final var serializedKpiId = serializeKpiId(kpiId);

        builder.setKpiId(serializedKpiId);
        builder.setMonitoringWindowS(monitoringWindow);
        builder.setSamplingRateS(samplingRate);

        return builder.build();
    }

    public MonitorKpiRequest deserialize(Monitoring.MonitorKpiRequest serializedMonitorKpiRequest) {

        final var serializedKpiId = serializedMonitorKpiRequest.getKpiId();
        final var kpiId = deserialize(serializedKpiId);
        final var monitoringWindow = serializedMonitorKpiRequest.getMonitoringWindowS();
        final var samplingRate = serializedMonitorKpiRequest.getSamplingRateS();

        return new MonitorKpiRequest(kpiId, monitoringWindow, samplingRate);
    }

    public SubsResponse deserialize(Monitoring.SubsResponse serializedSubsResponse) {
        final var serializedSubsId = serializedSubsResponse.getSubsId();
        final var serializedKpiList = serializedSubsResponse.getKpiList();
        final var listSerializedKpis = serializedKpiList.getKpiList();

        final var subsId = deserialize(serializedSubsId);
        final var kpiList =
                listSerializedKpis.stream().map(this::deserialize).collect(Collectors.toList());

        return new SubsResponse(subsId, kpiList);
    }

    public Monitoring.SubsDescriptor serialize(SubsDescriptor subDescriptor) {
        final var builder = Monitoring.SubsDescriptor.newBuilder();

        final var subscriptionId = subDescriptor.getSubscriptionId();
        final var kpiId = subDescriptor.getKpiId();
        final var samplingDurationS = subDescriptor.getSamplingDurationS();
        final var samplingIntervalS = subDescriptor.getSamplingIntervalS();
        final var startTimestamp = subDescriptor.getStartTimestamp();
        final var endTimestamp = subDescriptor.getEndTimestamp();

        final var serializedSubscriptionIdUuid = serializeSubscriptionIdId(subscriptionId);
        final var serializedKpiIdUuid = serializeUuid(kpiId);
        final var serializedKpiId = Monitoring.KpiId.newBuilder().setKpiId(serializedKpiIdUuid).build();
        final var serializedStartTimestamp = serialize(startTimestamp);
        final var serializedEndTimestamp = serialize(endTimestamp);

        builder.setSubsId(serializedSubscriptionIdUuid);
        builder.setKpiId(serializedKpiId);
        builder.setSamplingDurationS(samplingDurationS);
        builder.setSamplingIntervalS(samplingIntervalS);
        builder.setStartTimestamp(serializedStartTimestamp);
        builder.setEndTimestamp(serializedEndTimestamp);

        return builder.build();
    }

    public SubsDescriptor deserialize(Monitoring.SubsDescriptor serializedSubDescriptor) {
        final var serializedSubscriptionId = serializedSubDescriptor.getSubsId();
        final var serializedKpiId = serializedSubDescriptor.getKpiId();
        final var samplingDurationS = serializedSubDescriptor.getSamplingDurationS();
        final var samplingIntervalS = serializedSubDescriptor.getSamplingIntervalS();
        final var serializedStartTimestamp = serializedSubDescriptor.getStartTimestamp();
        final var serializedEndTimestamp = serializedSubDescriptor.getEndTimestamp();

        final var subscriptionId = deserialize(serializedSubscriptionId);
        final var kpiId = deserialize(serializedKpiId);
        final var startTimestamp = deserialize(serializedStartTimestamp);
        final var endTimestamp = deserialize(serializedEndTimestamp);

        return new SubsDescriptor(
                subscriptionId, kpiId, samplingDurationS, samplingIntervalS, startTimestamp, endTimestamp);
    }

    public SubscriptionID serializeSubscriptionIdId(String subscriptionId) {
        final var builder = Monitoring.SubscriptionID.newBuilder();

        final var serializedSubscriptionIdUuid = serializeUuid(subscriptionId);
        builder.setSubsId(serializedSubscriptionIdUuid);

        return builder.build();
    }

    public String deserialize(SubscriptionID serializedSubscriptionId) {
        final var serializedSubscriptionIdUuid = serializedSubscriptionId.getSubsId();

        return deserialize(serializedSubscriptionIdUuid);
    }

    public PolicyCondition.PolicyRuleCondition serialize(PolicyRuleCondition policyRuleCondition) {
        final var builder = PolicyCondition.PolicyRuleCondition.newBuilder();

        final var policyRuleConditionKpiId = policyRuleCondition.getKpiId();
        final var numericalOperator = policyRuleCondition.getNumericalOperator();
        final var policyRuleConditionKpiValue = policyRuleCondition.getKpiValue();

        final var serializedKpiIdUuid = serializeUuid(policyRuleConditionKpiId);
        final var serializedKpiId = KpiId.newBuilder().setKpiId(serializedKpiIdUuid).build();
        final var serializedNumericalOperator = serialize(numericalOperator);
        final var serializedPolicyRuleConditionKpiValue = serialize(policyRuleConditionKpiValue);

        builder.setKpiId(serializedKpiId);
        builder.setNumericalOperator(serializedNumericalOperator);
        builder.setKpiValue(serializedPolicyRuleConditionKpiValue);

        return builder.build();
    }

    public PolicyRuleCondition deserialize(
            PolicyCondition.PolicyRuleCondition serializedPolicyRuleCondition) {

        final var serializedPolicyRuleConditionKpiId =
                serializedPolicyRuleCondition.getKpiId().getKpiId();
        final var serializedNumericalOperator = serializedPolicyRuleCondition.getNumericalOperator();
        final var serializedPolicyRuleConditionKpiValue = serializedPolicyRuleCondition.getKpiValue();

        final var policyRuleConditionKpiId = deserialize(serializedPolicyRuleConditionKpiId);
        final var numericalOperator = deserialize(serializedNumericalOperator);
        final var policyRuleConditionKpiValue = deserialize(serializedPolicyRuleConditionKpiValue);

        return new PolicyRuleCondition(
                policyRuleConditionKpiId, numericalOperator, policyRuleConditionKpiValue);
    }

    public PolicyAction.PolicyRuleActionEnum serialize(PolicyRuleActionEnum policyRuleActionEnum) {
        switch (policyRuleActionEnum) {
            case POLICY_RULE_ACTION_SET_DEVICE_STATUS:
                return PolicyAction.PolicyRuleActionEnum.POLICYRULE_ACTION_SET_DEVICE_STATUS;
            case POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE:
                return PolicyAction.PolicyRuleActionEnum.POLICYRULE_ACTION_ADD_SERVICE_CONFIGRULE;
            case POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT:
                return PolicyAction.PolicyRuleActionEnum.POLICYRULE_ACTION_ADD_SERVICE_CONSTRAINT;
            case POLICY_RULE_ACTION_NO_ACTION:
                return PolicyAction.PolicyRuleActionEnum.POLICYRULE_ACTION_NO_ACTION;
            case POLICY_RULE_ACTION_CALL_SERVICE_RPC:
                return PolicyAction.PolicyRuleActionEnum.POLICY_RULE_ACTION_CALL_SERVICE_RPC;
            case POLICY_RULE_ACTION_RECALCULATE_PATH:
                return PolicyAction.PolicyRuleActionEnum.POLICY_RULE_ACTION_RECALCULATE_PATH;
            default:
                return PolicyAction.PolicyRuleActionEnum.UNRECOGNIZED;
        }
    }

    public PolicyRuleActionEnum deserialize(
            PolicyAction.PolicyRuleActionEnum serializePolicyRuleActionEnum) {
        switch (serializePolicyRuleActionEnum) {
            case POLICYRULE_ACTION_SET_DEVICE_STATUS:
                return PolicyRuleActionEnum.POLICY_RULE_ACTION_SET_DEVICE_STATUS;
            case POLICYRULE_ACTION_ADD_SERVICE_CONFIGRULE:
                return PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONFIGRULE;
            case POLICYRULE_ACTION_ADD_SERVICE_CONSTRAINT:
                return PolicyRuleActionEnum.POLICY_RULE_ACTION_ADD_SERVICE_CONSTRAINT;
            case POLICY_RULE_ACTION_CALL_SERVICE_RPC:
                return PolicyRuleActionEnum.POLICY_RULE_ACTION_CALL_SERVICE_RPC;
            case POLICY_RULE_ACTION_RECALCULATE_PATH:
                return PolicyRuleActionEnum.POLICY_RULE_ACTION_RECALCULATE_PATH;
            case POLICYRULE_ACTION_NO_ACTION:
            case UNRECOGNIZED:
            default:
                return PolicyRuleActionEnum.POLICY_RULE_ACTION_NO_ACTION;
        }
    }

    public PolicyAction.PolicyRuleActionConfig serialize(
            PolicyRuleActionConfig policyRuleActionConfig) {
        final var builder = PolicyAction.PolicyRuleActionConfig.newBuilder();

        final var actionKey = policyRuleActionConfig.getActionKey();
        final var actionValue = policyRuleActionConfig.getActionValue();

        builder.setActionKey(actionKey);
        builder.setActionValue(actionValue);

        return builder.build();
    }

    public PolicyRuleActionConfig deserialize(
            PolicyAction.PolicyRuleActionConfig serializedPolicyRuleActionConfig) {
        final var serializedActionKey = serializedPolicyRuleActionConfig.getActionKey();
        final var serializedActionValue = serializedPolicyRuleActionConfig.getActionValue();

        return new PolicyRuleActionConfig(serializedActionKey, serializedActionValue);
    }

    public PolicyAction.PolicyRuleAction serialize(PolicyRuleAction policyRuleAction) {
        final var builder = PolicyAction.PolicyRuleAction.newBuilder();

        final var policyRuleActionEnum = policyRuleAction.getPolicyRuleActionEnum();
        final var policyRuleActionConfigList = policyRuleAction.getPolicyRuleActionConfigs();

        final var serializedPolicyRuleActionEnum = serialize(policyRuleActionEnum);
        final var serializedPolicyRuleActionConfigList =
                policyRuleActionConfigList.stream().map(this::serialize).collect(Collectors.toList());

        builder.setAction(serializedPolicyRuleActionEnum);
        builder.addAllActionConfig(serializedPolicyRuleActionConfigList);

        return builder.build();
    }

    public PolicyRuleAction deserialize(PolicyAction.PolicyRuleAction serializedPolicyRuleAction) {
        final var serializedPolicyRuleActionEnum = serializedPolicyRuleAction.getAction();
        final var serializedPolicyRuleActionActionConfigs =
                serializedPolicyRuleAction.getActionConfigList();

        final var policyRuleActionEnum = deserialize(serializedPolicyRuleActionEnum);
        final var policyRuleActionActionConfigs =
                serializedPolicyRuleActionActionConfigs.stream()
                        .map(this::deserialize)
                        .collect(Collectors.toList());

        return new PolicyRuleAction(policyRuleActionEnum, policyRuleActionActionConfigs);
    }

    public PolicyCondition.BooleanOperator serialize(BooleanOperator booleanOperator) {
        switch (booleanOperator) {
            case POLICYRULE_CONDITION_BOOLEAN_AND:
                return PolicyCondition.BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_AND;
            case POLICYRULE_CONDITION_BOOLEAN_OR:
                return PolicyCondition.BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_OR;
            case POLICYRULE_CONDITION_BOOLEAN_UNDEFINED:
                return PolicyCondition.BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_UNDEFINED;
            default:
                return PolicyCondition.BooleanOperator.UNRECOGNIZED;
        }
    }

    public BooleanOperator deserialize(PolicyCondition.BooleanOperator serializedBooleanOperator) {
        switch (serializedBooleanOperator) {
            case POLICYRULE_CONDITION_BOOLEAN_OR:
                return BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_OR;
            case POLICYRULE_CONDITION_BOOLEAN_AND:
                return BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_AND;
            case POLICYRULE_CONDITION_BOOLEAN_UNDEFINED:
            case UNRECOGNIZED:
            default:
                return BooleanOperator.POLICYRULE_CONDITION_BOOLEAN_UNDEFINED;
        }
    }

    public Policy.PolicyRuleBasic serialize(PolicyRuleBasic policyRuleBasic) {
        final var builder = Policy.PolicyRuleBasic.newBuilder();

        final var policyRuleId = policyRuleBasic.getPolicyRuleId();
        final var policyRuleState = policyRuleBasic.getPolicyRuleState();
        final var priority = policyRuleBasic.getPriority();
        final var kpiId = policyRuleBasic.getKpiId();
        final var policyRuleActions = policyRuleBasic.getPolicyRuleActions();

        final var serializedPolicyRuleId = serializePolicyRuleId(policyRuleId);
        final var serializedPolicyRuleState = serialize(policyRuleState);
        final var serializedPolicyRuleActions =
                policyRuleActions.stream().map(this::serialize).collect(Collectors.toList());

        builder.setPolicyRuleId(serializedPolicyRuleId);
        builder.setPolicyRuleState(serializedPolicyRuleState);
        builder.setPriority(priority);
        builder.setKpiId(KpiId.newBuilder().setKpiId(Uuid.newBuilder().setUuid("kpiId").build()));
        builder.addAllActionList(serializedPolicyRuleActions);

        return builder.build();
    }

    public PolicyRuleBasic deserialize(Policy.PolicyRuleBasic serializedPolicyRuleBasic) {
        final var serializedPolicyRuleId = serializedPolicyRuleBasic.getPolicyRuleId();
        final var serializedPolicyRuleState = serializedPolicyRuleBasic.getPolicyRuleState();
        final var priority = serializedPolicyRuleBasic.getPriority();
        final var serializedPolicyRuleActions = serializedPolicyRuleBasic.getActionListList();
        final var serializedKpiId = serializedPolicyRuleBasic.getKpiId();

        final var policyRuleId = deserialize(serializedPolicyRuleId);
        final var kpiId = deserialize(serializedKpiId);
        final var policyRuleState = deserialize(serializedPolicyRuleState);
        final var policyRuleActions =
                serializedPolicyRuleActions.stream().map(this::deserialize).collect(Collectors.toList());

        return new PolicyRuleBasic(policyRuleId, kpiId, policyRuleState, priority, policyRuleActions);
    }

    public Policy.PolicyRuleService serialize(PolicyRuleService policyRuleService) {
        final var builder = Policy.PolicyRuleService.newBuilder();

        final var policyRuleBasic = policyRuleService.getPolicyRuleBasic();
        final var policyRuleServiceId = policyRuleService.getServiceId();
        final var policyRuleDeviceIds = policyRuleService.getDeviceIds();

        final var serializedPolicyRuleBasic = serialize(policyRuleBasic);
        final var serializedPolicyRuleServiceId = serialize(policyRuleServiceId);
        final var serializedPolicyRuleDeviceIds =
                policyRuleDeviceIds.stream().map(this::serializeDeviceId).collect(Collectors.toList());

        builder.setPolicyRuleBasic(serializedPolicyRuleBasic);
        builder.setServiceId(serializedPolicyRuleServiceId);
        builder.addAllDeviceList(serializedPolicyRuleDeviceIds);

        return builder.build();
    }

    public Policy.PolicyRule serialize(PolicyRule policyRule) {
        final var builder = Policy.PolicyRule.newBuilder();

        final var policyRuleType = policyRule.getPolicyRuleType();
        final var policyRuleTypeSpecificType = policyRuleType.getPolicyRuleType();

        if (policyRuleTypeSpecificType instanceof PolicyRuleService) {
            final var policyRuleService = serialize((PolicyRuleService) policyRuleTypeSpecificType);
            builder.setService(policyRuleService).build();
        }

        if (policyRuleTypeSpecificType instanceof PolicyRuleDevice) {
            final var policyRuleDevice = serialize((PolicyRuleDevice) policyRuleTypeSpecificType);
            builder.setDevice(policyRuleDevice).build();
        }

        return builder.build();
    }

    public PolicyRuleService deserialize(Policy.PolicyRuleService serializedPolicyRuleService) {
        final var serializedPolicyRuleBasic = serializedPolicyRuleService.getPolicyRuleBasic();
        final var serializedPolicyRuleServiceId = serializedPolicyRuleService.getServiceId();
        final var serializedPolicyRuleDeviceIds = serializedPolicyRuleService.getDeviceListList();

        final var policyRuleBasic = deserialize(serializedPolicyRuleBasic);
        final var policyRuleServiceId = deserialize(serializedPolicyRuleServiceId);
        final var policyRuleDeviceIds =
                serializedPolicyRuleDeviceIds.stream().map(this::deserialize).collect(Collectors.toList());

        return new PolicyRuleService(policyRuleBasic, policyRuleServiceId, policyRuleDeviceIds);
    }

    public PolicyRule deserialize(Policy.PolicyRule serializedPolicyRule) {

        final var typeOfPolicyRule = serializedPolicyRule.getPolicyRuleCase();

        switch (typeOfPolicyRule) {
            case SERVICE:
                final var serializedPolicyRuleService = serializedPolicyRule.getService();
                final var policyRuleService = deserialize(serializedPolicyRuleService);
                final var policyRuleTypeService = new PolicyRuleTypeService(policyRuleService);

                return new PolicyRule(policyRuleTypeService);
            case DEVICE:
                final var serializedPolicyRuleDevice = serializedPolicyRule.getDevice();
                final var policyRuleDevice = deserialize(serializedPolicyRuleDevice);
                final var policyRuleTypeDevice = new PolicyRuleTypeDevice(policyRuleDevice);

                return new PolicyRule(policyRuleTypeDevice);
            default:
            case POLICYRULE_NOT_SET:
                throw new IllegalStateException("Policy Rule not set");
        }
    }

    public Policy.PolicyRuleDevice serialize(PolicyRuleDevice policyRuleDevice) {
        final var builder = Policy.PolicyRuleDevice.newBuilder();

        final var policyRuleBasic = policyRuleDevice.getPolicyRuleBasic();
        final var policyRuleDeviceIds = policyRuleDevice.getDeviceIds();

        final var serializedPolicyRuleBasic = serialize(policyRuleBasic);
        final var serializedPolicyRuleDeviceIds =
                policyRuleDeviceIds.stream().map(this::serializeDeviceId).collect(Collectors.toList());

        builder.setPolicyRuleBasic(serializedPolicyRuleBasic);
        builder.addAllDeviceList(serializedPolicyRuleDeviceIds);

        return builder.build();
    }

    public PolicyRuleDevice deserialize(Policy.PolicyRuleDevice serializedPolicyRuleDevice) {
        final var serializedPolicyRuleBasic = serializedPolicyRuleDevice.getPolicyRuleBasic();
        final var serializedPolicyRuleDeviceIds = serializedPolicyRuleDevice.getDeviceListList();

        final var policyRuleBasic = deserialize(serializedPolicyRuleBasic);
        final var policyRuleDeviceIds =
                serializedPolicyRuleDeviceIds.stream().map(this::deserialize).collect(Collectors.toList());

        return new PolicyRuleDevice(policyRuleBasic, policyRuleDeviceIds);
    }

    public KpiId serializeKpiId(String kpiId) {
        final var builder = Monitoring.KpiId.newBuilder();

        final var serializedKpiIdUuid = serializeUuid(kpiId);
        builder.setKpiId(serializedKpiIdUuid);

        return builder.build();
    }

    public String deserialize(KpiId serializedKpiId) {
        final var serializedKpiIdUuid = serializedKpiId.getKpiId();

        return deserialize(serializedKpiIdUuid);
    }

    public Monitoring.Kpi serialize(Kpi kpi) {
        final var builder = Monitoring.Kpi.newBuilder();

        final var kpiId = kpi.getKpiId();
        final var timestamp = kpi.getTimestamp();
        final var kpiValue = kpi.getKpiValue();

        final var serializedKpiId = serializeKpiId(kpiId);
        final var serializedTimestamp = serialize(timestamp);
        final var serializedKpiValue = serialize(kpiValue);

        builder.setKpiId(serializedKpiId);
        builder.setTimestamp(serializedTimestamp);
        builder.setKpiValue(serializedKpiValue);

        return builder.build();
    }

    public Kpi deserialize(Monitoring.Kpi serializedKpi) {

        final var serializedKpiId = serializedKpi.getKpiId();
        final var serializedTimestamp = serializedKpi.getTimestamp();
        final var serializedKpiValue = serializedKpi.getKpiValue();

        final var kpiId = deserialize(serializedKpiId);
        final var timestamp = deserialize(serializedTimestamp);
        final var kpiValue = deserialize(serializedKpiValue);

        return new Kpi(kpiId, timestamp, kpiValue);
    }

    public List<Monitoring.Kpi> serialize(List<Kpi> kpis) {
        List<Monitoring.Kpi> serializedKpis = new ArrayList<>();

        for (Kpi kpi : kpis) {
            final var serializedKpi = serialize(kpi);

            serializedKpis.add(serializedKpi);
        }
        return serializedKpis;
    }

    public List<Kpi> deserialize(List<Monitoring.Kpi> serializedKpis) {
        List<Kpi> kpis = new ArrayList<>();

        for (Monitoring.Kpi serializedKpi : serializedKpis) {
            final var kpi = deserialize(serializedKpi);

            kpis.add(kpi);
        }
        return kpis;
    }

    public Monitoring.KpiDescriptor serialize(KpiDescriptor kpiDescriptor) {
        final var builder = Monitoring.KpiDescriptor.newBuilder();

        final var kpiDescriptorDescription = kpiDescriptor.getKpiDescription();
        final var kpiDescriptorKpiSampleType = kpiDescriptor.getKpiSampleType();
        final var kpiDescriptorDeviceId = kpiDescriptor.getDeviceId();
        final var kpiDescriptorEndPointId = kpiDescriptor.getEndPointId();
        final var kpiDescriptorServiceId = kpiDescriptor.getServiceId();
        final var kpiDescriptorSliceId = kpiDescriptor.getSliceId();

        final var serializedKpiDescriptorKpiSampleType = serialize(kpiDescriptorKpiSampleType);
        final var serializedKpiDescriptorDeviceId = serializeDeviceId(kpiDescriptorDeviceId);
        final var serializedKpiDescriptorEndPointId = serialize(kpiDescriptorEndPointId);
        final var serializedKpiDescriptorServiceId = serialize(kpiDescriptorServiceId);
        final var serializedKpiDescriptorSliceId = serialize(kpiDescriptorSliceId);

        builder.setKpiDescription(kpiDescriptorDescription);
        builder.setKpiSampleType(serializedKpiDescriptorKpiSampleType);
        builder.setDeviceId(serializedKpiDescriptorDeviceId);
        builder.setEndpointId(serializedKpiDescriptorEndPointId);
        builder.setServiceId(serializedKpiDescriptorServiceId);
        builder.setSliceId(serializedKpiDescriptorSliceId);

        return builder.build();
    }

    public KpiDescriptor deserialize(Monitoring.KpiDescriptor serializedKpiDescriptor) {

        final var serializedKpiDescriptorDescription = serializedKpiDescriptor.getKpiDescription();
        final var serializedKpiDescriptorKpiSampleType = serializedKpiDescriptor.getKpiSampleType();
        final var serializedKpiDescriptorDeviceId = serializedKpiDescriptor.getDeviceId();
        final var serializedKpiDescriptorEndPointId = serializedKpiDescriptor.getEndpointId();
        final var serializedKpiDescriptorServiceId = serializedKpiDescriptor.getServiceId();
        final var serializedKpiDescriptorSLiceId = serializedKpiDescriptor.getSliceId();

        final var kpiSampleType = deserialize(serializedKpiDescriptorKpiSampleType);
        final var deviceId = deserialize(serializedKpiDescriptorDeviceId);
        final var endPointId = deserialize(serializedKpiDescriptorEndPointId);
        final var serviceId = deserialize(serializedKpiDescriptorServiceId);
        final var sliceId = deserialize(serializedKpiDescriptorSLiceId);

        return new KpiDescriptor(
                serializedKpiDescriptorDescription,
                kpiSampleType,
                deviceId,
                endPointId,
                serviceId,
                sliceId);
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

    public Monitoring.AlarmSubscription serialize(AlarmSubscription alarmSubscription) {
        final var builder = Monitoring.AlarmSubscription.newBuilder();

        final var alarmId = alarmSubscription.getAlarmId();
        final var subscriptionTimeoutS = alarmSubscription.getSubscriptionTimeoutS();
        final var subscriptionFrequencyMs = alarmSubscription.getSubscriptionFrequencyMs();

        final var serializedAlarmId = serializeAlarmId(alarmId);

        builder.setAlarmId(serializedAlarmId);
        builder.setSubscriptionTimeoutS(subscriptionTimeoutS);
        builder.setSubscriptionFrequencyMs(subscriptionFrequencyMs);

        return builder.build();
    }

    public AlarmSubscription deserialize(Monitoring.AlarmSubscription serializedAlarmSubscription) {

        final var serializedAlarmId = serializedAlarmSubscription.getAlarmId();
        final var subscriptionTimeoutS = serializedAlarmSubscription.getSubscriptionTimeoutS();
        final var subscriptionFrequencyMs = serializedAlarmSubscription.getSubscriptionFrequencyMs();

        final var alarmId = deserialize(serializedAlarmId);

        return new AlarmSubscription(alarmId, subscriptionTimeoutS, subscriptionFrequencyMs);
    }

    public ContextOuterClass.Device serialize(Device device) {
        final var builder = ContextOuterClass.Device.newBuilder();

        final var deviceIdUuid = serializeUuid(device.getDeviceId());
        final var deviceId = DeviceId.newBuilder().setDeviceUuid(deviceIdUuid);
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
        builder.setDeviceType(deviceType);
        builder.setDeviceConfig(serializedDeviceConfig);
        builder.setDeviceOperationalStatus(serializedDeviceOperationalStatus);
        builder.addAllDeviceDrivers(serializedDeviceDrivers);
        builder.addAllDeviceEndpoints(serializedDeviceEndPoints);

        return builder.build();
    }

    public Device deserialize(ContextOuterClass.Device device) {

        final var serializedDeviceId = device.getDeviceId();
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
