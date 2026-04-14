# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, logging, re, time
from netaddr import IPAddress, IPNetwork
from typing import Dict, Tuple
from uuid import uuid4
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import (
    ContextId, Empty, EndPointId, QoSProfileId, Service, ServiceId,
    ServiceStatusEnum, ServiceTypeEnum, Uuid
)
from common.proto.qos_profile_pb2 import (
    QoSProfileValueUnitPair, QoSProfile,QoDConstraintsRequest
)
from common.tools.grpc.ConfigRules import update_config_rule_custom
from common.tools.grpc.Constraints import copy_constraints
from common.tools.grpc.Tools import grpc_message_to_json, grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Service import json_service_id
from context.client.ContextClient import ContextClient
from qos_profile.client.QoSProfileClient import QoSProfileClient


LOGGER = logging.getLogger(__name__)

ENDPOINT_SETTINGS_KEY = "/device[{:s}]/endpoint[{:s}]/vlan[{:d}]/settings"
DEVICE_SETTINGS_KEY = "/device[{:s}]/settings"
RE_CONFIG_RULE_IF_SUBIF = re.compile(r"^\/interface\[([^\]]+)\]\/subinterface\[([^\]]+)\]$")
MEC_FIELDS = [
    "device", "applicationServer", "qosProfile", "sessionId", "duration",
    "startedAt", "expiresAt", "qosStatus"
]

def grpc_context_id(context_uuid):
    return ContextId(**json_context_id(context_uuid))

def grpc_service_id(context_uuid, service_uuid):
    return ServiceId(**json_service_id(service_uuid, context_id=json_context_id(context_uuid)))

def grpc_message_to_qos_table_data(message : QoSProfile) -> dict:
    return {
        "qos_profile_id"          : message.qos_profile_id.qos_profile_id.uuid,
        "name"                    : message.name,
        "description"             : message.description,
        "status"                  : message.status,
        "targetMinUpstreamRate"   : grpc_message_to_json(message.targetMinUpstreamRate),
        "maxUpstreamRate"         : grpc_message_to_json(message.maxUpstreamRate),
        "maxUpstreamBurstRate"    : grpc_message_to_json(message.maxUpstreamBurstRate),
        "targetMinDownstreamRate" : grpc_message_to_json(message.targetMinDownstreamRate),
        "maxDownstreamRate"       : grpc_message_to_json(message.maxDownstreamRate),
        "maxDownstreamBurstRate"  : grpc_message_to_json(message.maxDownstreamBurstRate),
        "minDuration"             : grpc_message_to_json(message.minDuration),
        "maxDuration"             : grpc_message_to_json(message.maxDuration),
        "priority"                : message.priority,
        "packetDelayBudget"       : grpc_message_to_json(message.packetDelayBudget),
        "jitter"                  : grpc_message_to_json(message.jitter),
        "packetErrorLossRate"     : message.packetErrorLossRate,
    }

def create_value_unit(data) -> QoSProfileValueUnitPair:
    return QoSProfileValueUnitPair(value=data["value"], unit=data["unit"])

def create_qos_profile_from_json(qos_profile_data : dict) -> QoSProfile:
    qos_profile = QoSProfile()
    qos_profile.qos_profile_id.CopyFrom(QoSProfileId(qos_profile_id=Uuid(uuid=qos_profile_data["qos_profile_id"])))
    qos_profile.name = qos_profile_data["name"]
    qos_profile.description = qos_profile_data["description"]
    qos_profile.status = qos_profile_data["status"]
    qos_profile.targetMinUpstreamRate.CopyFrom(create_value_unit(qos_profile_data["targetMinUpstreamRate"]))
    qos_profile.maxUpstreamRate.CopyFrom(create_value_unit(qos_profile_data["maxUpstreamRate"]))
    qos_profile.maxUpstreamBurstRate.CopyFrom(create_value_unit(qos_profile_data["maxUpstreamBurstRate"]))
    qos_profile.targetMinDownstreamRate.CopyFrom(create_value_unit(qos_profile_data["targetMinDownstreamRate"]))
    qos_profile.maxDownstreamRate.CopyFrom(create_value_unit(qos_profile_data["maxDownstreamRate"]))
    qos_profile.maxDownstreamBurstRate.CopyFrom(create_value_unit(qos_profile_data["maxDownstreamBurstRate"]))
    qos_profile.minDuration.CopyFrom(create_value_unit(qos_profile_data["minDuration"]))
    qos_profile.maxDuration.CopyFrom(create_value_unit(qos_profile_data["maxDuration"]))
    qos_profile.priority = qos_profile_data["priority"]
    qos_profile.packetDelayBudget.CopyFrom(create_value_unit(qos_profile_data["packetDelayBudget"]))
    qos_profile.jitter.CopyFrom(create_value_unit(qos_profile_data["jitter"]))
    qos_profile.packetErrorLossRate = qos_profile_data["packetErrorLossRate"]
    return qos_profile

def ip_withoutsubnet(ip_withsubnet, target_ip_address):
    network = IPNetwork(ip_withsubnet)
    return IPAddress(target_ip_address) in network

def map_ip_addresses_to_endpoint_ids(
    context_client : ContextClient, a_ip : str, z_ip : str
) -> Tuple[EndPointId, EndPointId]:
    a_ep_id = None
    z_ep_id = None

    devices = context_client.ListDevices(Empty()).devices
    for device in devices:
        endpoint_mappings = dict()
        for endpoint in device.device_endpoints:
            endpoint_id   = endpoint.endpoint_id
            endpoint_uuid = endpoint_id.endpoint_uuid.uuid
            endpoint_name = endpoint.name
            endpoint_mappings[endpoint_uuid] = endpoint_id
            endpoint_mappings[endpoint_name] = endpoint_id

        for config_rule in device.device_config.config_rules:
            if config_rule.WhichOneof("config_rule") != "custom": continue
            match_subif = RE_CONFIG_RULE_IF_SUBIF.match(config_rule.custom.resource_key)
            if not match_subif: continue

            short_port_name = match_subif.groups()[0]
            endpoint_id = endpoint_mappings[short_port_name]

            address_ip = json.loads(config_rule.custom.resource_value).get("address_ip")
            if ip_withoutsubnet(a_ip, address_ip): a_ep_id = endpoint_id
            if ip_withoutsubnet(z_ip, address_ip): z_ep_id = endpoint_id

    return a_ep_id, z_ep_id

def QOD_2_service(
    context_client : ContextClient, qos_profile_client : QoSProfileClient,
    qod_info : Dict
) -> Service:
    
    if "session_id" not in qod_info:
        session_id = str(uuid4())
        qod_info["session_id"] = session_id

    service = Service()
    service.service_id.service_uuid.uuid = session_id
    service.service_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
    service.name = session_id
    service.service_type = ServiceTypeEnum.SERVICETYPE_L3NM
    service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED

    if 'device' in qod_info and 'applicationServer' in qod_info:
        a_ip = qod_info['device'].get('ipv4Address')
        z_ip = qod_info['applicationServer'].get('ipv4Address')
        if a_ip and z_ip:
            a_ep_id, z_ep_id = map_ip_addresses_to_endpoint_ids(context_client, a_ip, z_ip)
            if a_ep_id is not None: service.service_endpoint_ids.append(a_ep_id)
            if z_ep_id is not None: service.service_endpoint_ids.append(z_ep_id)

    service_config_rules = service.service_config.config_rules
    update_config_rule_custom(service_config_rules, '/settings', {})
    update_config_rule_custom(service_config_rules, '/request', {
        k : (qod_info[k], True) for k in MEC_FIELDS if k in qod_info
    })

    qos_profile_id = qod_info.get('qos_profile_id')
    qos_profile_id = QoSProfileId(qos_profile_id=Uuid(uuid=qos_profile_id))
    current_time = time.time()
    duration_days = qod_info.get('duration')
    request = QoDConstraintsRequest(
        qos_profile_id=qos_profile_id, start_timestamp=current_time, duration=duration_days
    )
    qos_profile_constraints = qos_profile_client.GetConstraintsFromQoSProfile(request)
    LOGGER.warning('qos_profile_constraints = {:s}'.format(grpc_message_to_json_string(qos_profile_constraints)))
    copy_constraints(qos_profile_constraints.constraints, service.service_constraints)
    LOGGER.warning('service.service_constraints = {:s}'.format(grpc_message_to_json_string(service.service_constraints)))

    return service

def service_2_qod(service : Service) -> Dict:
    response = {}
    for config_rule in service.service_config.config_rules:
        if config_rule.WhichOneof("config_rule") != "custom": continue
        if config_rule.custom.resource_key != '/request': continue
        resource_value_json = json.loads(config_rule.custom.resource_value)

        if 'device' in resource_value_json and 'ipv4Address' in resource_value_json['device']:
            response['device'] = {'ipv4Address': resource_value_json['device']['ipv4Address']}

        if 'applicationServer' in resource_value_json and 'ipv4Address' in resource_value_json['applicationServer']:
            response['applicationServer'] = {'ipv4Address': resource_value_json['applicationServer']['ipv4Address']}

    if service.service_id:
        response['session_id'] = service.service_id.service_uuid.uuid

    for constraint in service.service_constraints:
        if constraint.WhichOneof('constraint') == 'schedule':
            response['duration' ] = float(constraint.schedule.duration_days)
            response['startedAt'] = int(constraint.schedule.start_timestamp)
            response['expiresAt'] = response['startedAt'] + response['duration']

        if constraint.WhichOneof('constraint') == 'qos_profile':
            response['qos_profile_id'] = constraint.qos_profile.qos_profile_id.qos_profile_id.uuid

    return response
