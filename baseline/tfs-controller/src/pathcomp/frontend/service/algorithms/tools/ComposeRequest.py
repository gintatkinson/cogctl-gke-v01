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

import logging
from typing import Dict
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import Constraint, Device, EndPointId, Link, Service, ServiceId, TopologyId
from common.tools.grpc.Tools import grpc_message_to_json_string
from .ConstantsMappings import (
    CapacityUnit, LinkForwardingDirection, LinkPortDirection, TerminationDirection, TerminationState)

LOGGER = logging.getLogger(__name__)

def compose_topology_id(topology_id : TopologyId) -> Dict: # pylint: disable=unused-argument
    # force context_uuid and topology_uuid to be always DEFAULT_CONTEXT_NAME and DEFAULT_TOPOLOGY_NAME for simplicity
    # for interdomain, contexts and topologies are managed in particular ways

    context_uuid = DEFAULT_CONTEXT_NAME
    #context_uuid = topology_id.context_id.context_uuid.uuid
    #if len(context_uuid) == 0: context_uuid = DEFAULT_CONTEXT_NAME

    topology_uuid = DEFAULT_TOPOLOGY_NAME
    #topology_uuid = topology_id.topology_uuid.uuid
    #if len(topology_uuid) == 0: topology_uuid = DEFAULT_TOPOLOGY_NAME

    return {'contextId': context_uuid, 'topology_uuid': topology_uuid}

def compose_service_id(service_id : ServiceId) -> Dict:
    # force context_uuid to be always DEFAULT_CONTEXT_NAME for simplicity
    # for interdomain, contexts are managed in particular ways

    #context_uuid = service_id.context_id.context_uuid.uuid
    #if len(context_uuid) == 0: context_uuid = DEFAULT_CONTEXT_NAME
    context_uuid = DEFAULT_CONTEXT_NAME

    service_uuid = service_id.service_uuid.uuid
    return {'contextId': context_uuid, 'service_uuid': service_uuid}

def compose_endpoint_id(endpoint_id : EndPointId) -> Dict:
    topology_id = compose_topology_id(endpoint_id.topology_id)
    device_uuid = endpoint_id.device_id.device_uuid.uuid
    endpoint_uuid = endpoint_id.endpoint_uuid.uuid
    return {'topology_id': topology_id, 'device_id': device_uuid, 'endpoint_uuid': endpoint_uuid}

def compose_capacity(value : str, unit : str) -> Dict:
    return {'total-size': {'value': value, 'unit': unit}}

def compose_endpoint(
    endpoint_id : Dict, endpoint_type : str, link_port_direction : int, termination_direction : int,
    termination_state : int, total_potential_capacity : Dict, available_capacity : Dict
) -> Dict:
    return {
        'endpoint_id': endpoint_id, 'endpoint_type': endpoint_type, 'link_port_direction': link_port_direction,
        'termination-direction': termination_direction, 'termination-state': termination_state,
        'total-potential-capacity': total_potential_capacity, 'available-capacity': available_capacity,
    }

def compose_cost_characteristics(cost_name : str, cost_value : str, cost_algorithm : str) -> Dict:
    return {'cost-name': cost_name, 'cost-value': cost_value, 'cost-algorithm': cost_algorithm}

def compose_latency_characteristics(fixed_latency_characteristic : str) -> Dict:
    return {'fixed-latency-characteristic': fixed_latency_characteristic}

def compose_constraint(constraint : Constraint) -> Dict:
    kind = constraint.WhichOneof('constraint')
    if kind == 'custom':
        constraint_type = constraint.custom.constraint_type
        if constraint_type in {'bandwidth[gbps]', 'latency[ms]', 'jitter[us]'}:
            constraint_value = constraint.custom.constraint_value
            return {'constraint_type': constraint_type, 'constraint_value': constraint_value}
    elif kind == 'sla_capacity':
        capacity_gbps = constraint.sla_capacity.capacity_gbps
        return {'constraint_type': 'bandwidth[gbps]', 'constraint_value': str(capacity_gbps)}
    elif kind == 'sla_latency':
        e2e_latency_ms = constraint.sla_latency.e2e_latency_ms
        return {'constraint_type': 'latency[ms]', 'constraint_value': str(e2e_latency_ms)}

    str_constraint = grpc_message_to_json_string(constraint)
    LOGGER.warning('Ignoring unsupported Constraint({:s})'.format(str_constraint))
    return None

def compose_device(grpc_device : Device) -> Dict:
    device_uuid = grpc_device.device_id.device_uuid.uuid
    device_type = grpc_device.device_type

    endpoints = []
    for device_endpoint in grpc_device.device_endpoints:
        endpoint_id = compose_endpoint_id(device_endpoint.endpoint_id)
        endpoint_type = device_endpoint.endpoint_type
        link_port_direction = LinkPortDirection.BIDIRECTIONAL.value
        termination_direction = TerminationDirection.BIDIRECTIONAL.value
        termination_state = TerminationState.TERMINATED_BIDIRECTIONAL.value
        total_potential_capacity = compose_capacity(100000, CapacityUnit.GBPS.value)
        available_capacity = compose_capacity(100000, CapacityUnit.GBPS.value)
        endpoint = compose_endpoint(
            endpoint_id, endpoint_type, link_port_direction, termination_direction,
            termination_state, total_potential_capacity, available_capacity)
        endpoints.append(endpoint)

    return {'device_Id': device_uuid, 'device_type': device_type, 'device_endpoints': endpoints}

def compose_link(grpc_link : Link) -> Dict:
    link_uuid = grpc_link.link_id.link_uuid.uuid

    endpoint_ids = [
        {'endpoint_id' : compose_endpoint_id(link_endpoint_id)}
        for link_endpoint_id in grpc_link.link_endpoint_ids
    ]

    total_capacity_gbps, used_capacity_gbps = None, None
    forwarding_direction = LinkForwardingDirection.UNIDIRECTIONAL.value
    if grpc_link.HasField('attributes'):
        attributes = grpc_link.attributes
        # In proto3, HasField() does not work for scalar fields, using ListFields() instead.
        attribute_names = set([field.name for field,_ in attributes.ListFields()])
        if 'total_capacity_gbps' in attribute_names:
            total_capacity_gbps = attributes.total_capacity_gbps
        if 'used_capacity_gbps' in attribute_names:
            used_capacity_gbps = attributes.used_capacity_gbps
        elif total_capacity_gbps is not None:
            used_capacity_gbps = total_capacity_gbps

        if 'is_bidirectional' in attribute_names:
            is_bidirectional = attributes.is_bidirectional
            if is_bidirectional:
                forwarding_direction = LinkForwardingDirection.BIDIRECTIONAL.value

    if total_capacity_gbps is None: total_capacity_gbps = 100000
    if used_capacity_gbps  is None: used_capacity_gbps = 0
    available_capacity_gbps = total_capacity_gbps - used_capacity_gbps

    total_potential_capacity = compose_capacity(total_capacity_gbps, CapacityUnit.GBPS.value)
    available_capacity = compose_capacity(available_capacity_gbps, CapacityUnit.GBPS.value)
    cost_characteristics = compose_cost_characteristics('linkcost', '1', '0')
    latency_characteristics = compose_latency_characteristics('1')

    return {
        'link_Id': link_uuid, 'link_endpoint_ids': endpoint_ids, 'forwarding_direction': forwarding_direction,
        'total-potential-capacity': total_potential_capacity, 'available-capacity': available_capacity,
        'cost-characteristics': cost_characteristics, 'latency-characteristics': latency_characteristics,
    }

def compose_service(grpc_service : Service) -> Dict:
    service_id = compose_service_id(grpc_service.service_id)
    service_type = grpc_service.service_type

    endpoint_ids = [
        compose_endpoint_id(service_endpoint_id)
        for service_endpoint_id in grpc_service.service_endpoint_ids
    ]

    constraints = list(filter(lambda constraint: constraint is not None, [
        compose_constraint(service_constraint)
        for service_constraint in grpc_service.service_constraints
    ]))

    constraint_types = {constraint['constraint_type'] for constraint in constraints}
    if 'bandwidth[gbps]' not in constraint_types:
        constraints.append({'constraint_type': 'bandwidth[gbps]', 'constraint_value': '20.0'})
    if 'latency[ms]' not in constraint_types:
        constraints.append({'constraint_type': 'latency[ms]', 'constraint_value': '20.0'})
    #if 'jitter[us]' not in constraint_types:
    #    constraints.append({'constraint_type': 'jitter[us]', 'constraint_value': '50.0'})

    return {
        'serviceId': service_id,
        'serviceType': service_type,
        'service_endpoints_ids': endpoint_ids,
        'service_constraints': constraints,
    }
