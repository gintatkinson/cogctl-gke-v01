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

from typing import Dict
from flask.json import jsonify
from common.proto.context_pb2 import (
    ConnectionId, Context, ContextId, Device, DeviceId, Link, LinkId,
    ServiceId, Slice, SliceId, Topology, TopologyId, Service
)
from common.proto.policy_pb2 import PolicyRule, PolicyRuleId
from common.tools.grpc.Tools import grpc_message_to_json
from common.tools.object_factory.Connection import json_connection_id
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.Link import json_link_id
from common.tools.object_factory.PolicyRule import json_policyrule_id
from common.tools.object_factory.Service import json_service_id
from common.tools.object_factory.Slice import json_slice_id
from common.tools.object_factory.Topology import json_topology_id


def format_grpc_to_json(grpc_reply):
    return jsonify(grpc_message_to_json(grpc_reply))

def grpc_connection_id(connection_uuid):
    return ConnectionId(**json_connection_id(connection_uuid))

def grpc_context_id(context_uuid):
    return ContextId(**json_context_id(context_uuid))

def grpc_context(json_context : Dict):
    return Context(**json_context)

def grpc_device_id(device_uuid):
    return DeviceId(**json_device_id(device_uuid))

def grpc_device(json_device : Dict):
    return Device(**json_device)

def grpc_link_id(link_uuid):
    return LinkId(**json_link_id(link_uuid))

def grpc_link(json_link : Dict):
    return Link(**json_link)

def grpc_service_id(context_uuid, service_uuid):
    return ServiceId(**json_service_id(service_uuid, context_id=json_context_id(context_uuid)))

def grpc_service(json_service : Dict):
    return Service(**json_service)

def grpc_slice_id(context_uuid, slice_uuid):
    return SliceId(**json_slice_id(slice_uuid, context_id=json_context_id(context_uuid)))

def grpc_slice(json_slice : Dict):
    return Slice(**json_slice)

def grpc_topology_id(context_uuid, topology_uuid):
    return TopologyId(**json_topology_id(topology_uuid, context_id=json_context_id(context_uuid)))

def grpc_topology(json_topology : Dict):
    return Topology(**json_topology)

def grpc_policy_rule_id(policy_rule_uuid):
    return PolicyRuleId(**json_policyrule_id(policy_rule_uuid))

def grpc_policy_rule(json_policy_rule : Dict):
    return PolicyRule(**json_policy_rule)
