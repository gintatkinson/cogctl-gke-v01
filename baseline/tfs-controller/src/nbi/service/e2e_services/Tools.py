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
from decimal import ROUND_HALF_EVEN, Decimal
from flask.json import jsonify
from common.proto.context_pb2 import (
    ContextId, Empty, EndPointId, ServiceId, ServiceStatusEnum, ServiceTypeEnum,
    Service, Constraint, Constraint_SLA_Capacity, ConfigRule, ConfigRule_Custom,
    ConfigActionEnum
)
from common.tools.grpc.ConfigRules import update_config_rule_custom
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Service import json_service_id

LOGGER = logging.getLogger(__name__)

ENDPOINT_SETTINGS_KEY = '/device[{:s}]/endpoint[{:s}]/vlan[{:d}]/settings'
DEVICE_SETTINGS_KEY = '/device[{:s}]/settings'
RE_CONFIG_RULE_IF_SUBIF = re.compile(r'^\/interface\[([^\]]+)\]\/subinterface\[([^\]]+)\]$')
MEC_CONSIDERED_FIELDS = ['requestType', 'sessionFilter', 'fixedAllocation', 'allocationDirection', 'fixedBWPriority']
ALLOCATION_DIRECTION_DESCRIPTIONS = {
    '00' : 'Downlink (towards the UE)',
    '01' : 'Uplink (towards the application/session)',
    '10' : 'Symmetrical'}
VLAN_TAG = 0
PREFIX_LENGTH = 24
BGP_AS = 65000
POLICY_AZ = 'srv_{:d}_a'.format(VLAN_TAG)
POLICY_ZA = 'srv_{:d}_b'.format(VLAN_TAG)
BGP_NEIGHBOR_IP_A = '192.168.150.1'
BGP_NEIGHBOR_IP_Z = '192.168.150.2'
ROUTER_ID_A = '200.1.1.1'
ROUTER_ID_Z = '200.1.1.2'
ROUTE_DISTINGUISHER = '{:5d}:{:03d}'.format(BGP_AS, VLAN_TAG)

def service_2_bwInfo(service: Service) -> dict:
    response = {}
    # allocationDirection = '??' # String: 00 = Downlink (towards the UE); 01 = Uplink (towards the application/session); 10 = Symmetrical
    response['appInsId'] = service.service_id.service_uuid.uuid # String: Application instance identifier
    for constraint in service.service_constraints:
        if constraint.WhichOneof('constraint') == 'sla_capacity':
            # String: Size of requested fixed BW allocation in [bps]
            fixed_allocation = Decimal(constraint.sla_capacity.capacity_gbps * 1.e9)
            fixed_allocation = fixed_allocation.quantize(Decimal('0.1'), rounding=ROUND_HALF_EVEN)
            response['fixedAllocation'] = str(fixed_allocation)
            break

    for config_rule in service.service_config.config_rules:
        resource_value_json = json.loads(config_rule.custom.resource_value)
        if config_rule.custom.resource_key != '/request':
            continue
        for key in ['allocationDirection', 'fixedBWPriority', 'requestType', 'sourceIp', 'sourcePort', 'dstPort', 'protocol', 'sessionFilter']:
            if key not in resource_value_json: 
                continue

            if key == 'sessionFilter':
                response[key] = [resource_value_json[key]]
            elif key == 'requestType':
                response[key] = str(resource_value_json[key])
            else:
                response[key] = resource_value_json[key]

    unixtime = time.time()
    response['timeStamp'] = { # Time stamp to indicate when the corresponding information elements are sent
        "seconds": int(unixtime),
        "nanoseconds": int(unixtime%1*1e9)
    }

    return response

def bwInfo_2_service(client, bw_info: dict) -> Service:
    # add description to allocationDirection code
    if 'sessionFilter' in bw_info:
        bw_info['sessionFilter'] = bw_info['sessionFilter'][0] # Discard other items in sessionFilter field

    service = Service()
    
    service_config_rules = service.service_config.config_rules


    request_cr_key = '/request'
    request_cr_value = {k:bw_info[k] for k in MEC_CONSIDERED_FIELDS}

    config_rule = ConfigRule()
    config_rule.action = ConfigActionEnum.CONFIGACTION_SET
    config_rule_custom = ConfigRule_Custom()
    config_rule_custom.resource_key  = request_cr_key
    config_rule_custom.resource_value = json.dumps(request_cr_value)
    config_rule.custom.CopyFrom(config_rule_custom)
    service_config_rules.append(config_rule)

    if 'sessionFilter' in bw_info:
        a_ip = bw_info['sessionFilter']['sourceIp']
        z_ip = bw_info['sessionFilter']['dstAddress']

        devices = client.ListDevices(Empty()).devices
        ip_interface_name_dict = {}
        for device in devices:
            device_endpoint_uuids = {ep.name:ep.endpoint_id.endpoint_uuid.uuid for ep in device.device_endpoints}
            skip_device = True
            for cr in device.device_config.config_rules:
                if cr.WhichOneof('config_rule') != 'custom':
                    continue
                match_subif = RE_CONFIG_RULE_IF_SUBIF.match(cr.custom.resource_key)
                if not match_subif:
                    continue
                address_ip = json.loads(cr.custom.resource_value).get('address_ip')
                short_port_name = match_subif.groups(0)[0]
                ip_interface_name_dict[address_ip] = short_port_name
                if address_ip not in [a_ip, z_ip]:
                    continue
                port_name = 'PORT-' + short_port_name # `PORT-` added as prefix
                ep_id = EndPointId()
                ep_id.endpoint_uuid.uuid = device_endpoint_uuids[port_name]
                ep_id.device_id.device_uuid.uuid = device.device_id.device_uuid.uuid
                service.service_endpoint_ids.append(ep_id)
                # add interface config rules
                endpoint_settings_key = ENDPOINT_SETTINGS_KEY.format(device.name, port_name, VLAN_TAG)
                if address_ip in a_ip:
                    router_id = ROUTER_ID_A
                    policy_az = POLICY_AZ
                    policy_za = POLICY_ZA
                    neighbor_bgp_interface_address_ip = BGP_NEIGHBOR_IP_Z
                    self_bgp_interface_address_ip = BGP_NEIGHBOR_IP_A
                else:
                    router_id = ROUTER_ID_Z
                    policy_az = POLICY_ZA
                    policy_za = POLICY_AZ
                    neighbor_bgp_interface_address_ip= BGP_NEIGHBOR_IP_A
                    self_bgp_interface_address_ip = BGP_NEIGHBOR_IP_Z
                endpoint_field_updates = {
                    'address_ip': (address_ip, True),
                    'address_prefix'     : (PREFIX_LENGTH, True),
                    'sub_interface_index': (0, True),
                        }
                LOGGER.debug(f'BEFORE UPDATE -> device.device_config.config_rules: {service_config_rules}')
                update_config_rule_custom(service_config_rules, endpoint_settings_key, endpoint_field_updates)
                LOGGER.debug(f'AFTER UPDATE -> device.device_config.config_rules: {service_config_rules}')
                skip_device = False
            if skip_device:
                continue
            device_field_updates = {
                         'bgp_as':(BGP_AS, True),
                         'route_distinguisher': (ROUTE_DISTINGUISHER, True),
                         'router_id': (router_id, True),
                         'policy_AZ': (policy_az, True),
                         'policy_ZA': (policy_za, True),
                         'neighbor_bgp_interface_address_ip': (neighbor_bgp_interface_address_ip, True),
                         'self_bgp_interface_name': (ip_interface_name_dict[self_bgp_interface_address_ip], True),
                         'self_bgp_interface_address_ip': (self_bgp_interface_address_ip, True),
                         'bgp_interface_address_prefix': (PREFIX_LENGTH, True)
                        }
            device_settings_key = DEVICE_SETTINGS_KEY.format(device.name)
            LOGGER.debug(f'BEFORE UPDATE -> device.device_config.config_rules: {service_config_rules}')
            update_config_rule_custom(service_config_rules, device_settings_key, device_field_updates)
            LOGGER.debug(f'AFTER UPDATE -> device.device_config.config_rules: {service_config_rules}')
    
    settings_cr_key = '/settings'
    settings_cr_value = {}
    update_config_rule_custom(service_config_rules, settings_cr_key, settings_cr_value)

    service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED
    service.service_type = ServiceTypeEnum.SERVICETYPE_L3NM

    if 'appInsId' in bw_info:
        service.service_id.service_uuid.uuid = bw_info['appInsId']
        service.service_id.context_id.context_uuid.uuid = 'admin'
        service.name = bw_info['appInsId']

    if 'fixedAllocation' in bw_info:
        capacity = Constraint_SLA_Capacity()
        capacity.capacity_gbps = float(bw_info['fixedAllocation']) / 1.e9
        constraint = Constraint()
        constraint.sla_capacity.CopyFrom(capacity)
        service.service_constraints.append(constraint)

    return service


def format_grpc_to_json(grpc_reply):
    return jsonify(grpc_message_to_json(grpc_reply))

def grpc_context_id(context_uuid):
    return ContextId(**json_context_id(context_uuid))

def grpc_service_id(context_uuid, service_uuid):
    return ServiceId(**json_service_id(service_uuid, context_id=json_context_id(context_uuid)))
