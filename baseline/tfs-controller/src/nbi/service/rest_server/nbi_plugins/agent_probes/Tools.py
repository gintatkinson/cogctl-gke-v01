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

from flask.json import jsonify
from common.proto.context_pb2 import (
     DeviceDriverEnum, Device, DeviceId, DeviceOperationalStatusEnum
)
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.ConfigRule import json_config_rule
from common.tools.object_factory.EndPoint import json_endpoint
from common.tools.object_factory.Device import json_device_id, json_device

def format_grpc_to_json(grpc_reply):
    return jsonify(grpc_message_to_json(grpc_reply))

def grpc_device_id(device_uuid):
    return DeviceId(**json_device_id(device_uuid))

def grpc_device(
    device_uuid, device_type, status, endpoints=None, config_rules=None, drivers=None
):
    json_config_rules = [
        json_config_rule(
            config_rule['action'],
            config_rule['custom']['resource_key'],
            config_rule['custom']['resource_value']
        )
        for config_rule in config_rules
    ] if config_rules else []
    json_status = status if status else DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED
    json_drivers = drivers if drivers else DeviceDriverEnum.DEVICEDRIVER_UNDEFINED
    json_endpoints = [
        json_endpoint(
            endpoint['device_id']['device_uuid']['uuid'],
            endpoint['endpoint_uuid']['uuid'],
            endpoint['endpoint_type'],
            endpoint['topology_id'],
            endpoint['kpi_sample_types'],
            endpoint['location']['region']
        )
        for endpoint in endpoints
    ] if endpoints else []
    return Device(**json_device(
        device_uuid, device_type, json_status, None, json_endpoints, json_config_rules, json_drivers))
