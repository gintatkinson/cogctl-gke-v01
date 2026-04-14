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

# RFC 8466 - L2VPN Service Model (L2SM)
# Ref: https://datatracker.ietf.org/doc/html/rfc8466


import json
from typing import Any, Dict, List, Optional, Tuple
from common.proto.context_pb2 import Constraint, ConstraintActionEnum, EndPointId, QoSProfileId
from common.tools.grpc.Tools import grpc_message_to_json_string

def update_constraint_custom_scalar(
    constraints, constraint_type : str, value : Any, raise_if_differs : bool = False,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:

    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'custom': continue
        if constraint.custom.constraint_type != constraint_type: continue
        json_constraint_value = json.loads(constraint.custom.constraint_value)
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member
        constraint.custom.constraint_type = constraint_type
        json_constraint_value = None

    constraint.action = new_action

    if (json_constraint_value is None) or not raise_if_differs:
        # missing or raise_if_differs=False, add/update it
        json_constraint_value = value
    elif json_constraint_value != value:
        # exists, differs, and raise_if_differs=True
        msg = 'Specified value({:s}) differs existing value({:s})'
        raise Exception(msg.format(str(value), str(json_constraint_value)))

    constraint.custom.constraint_value = json.dumps(json_constraint_value, sort_keys=True)
    return constraint

def update_constraint_custom_dict(
    constraints, constraint_type : str, fields : Dict[str, Tuple[Any, bool]],
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    # fields: Dict[field_name : str, Tuple[field_value : Any, raise_if_differs : bool]]

    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'custom': continue
        if constraint.custom.constraint_type != constraint_type: continue
        json_constraint_value = json.loads(constraint.custom.constraint_value)
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member
        constraint.custom.constraint_type = constraint_type
        json_constraint_value = {}

    constraint.action = new_action

    for field_name,(field_value, raise_if_differs) in fields.items():
        if (field_name not in json_constraint_value) or not raise_if_differs:
            # missing or raise_if_differs=False, add/update it
            json_constraint_value[field_name] = field_value
        elif json_constraint_value[field_name] != field_value:
            # exists, differs, and raise_if_differs=True
            msg = 'Specified {:s}({:s}) differs existing value({:s})'
            raise Exception(msg.format(str(field_name), str(field_value), str(json_constraint_value[field_name])))

    constraint.custom.constraint_value = json.dumps(json_constraint_value, sort_keys=True)
    return constraint

def update_constraint_schedule(
    constraints, start_timestamp : float, duration_days : float,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'schedule': continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member

    constraint.action = new_action

    constraint.schedule.start_timestamp = start_timestamp
    constraint.schedule.duration_days   = duration_days
    return constraint

def update_constraint_endpoint_location(
    constraints, endpoint_id : EndPointId,
    region : Optional[str] = None, gps_position : Optional[Tuple[float, float]] = None,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    # gps_position: (latitude, longitude)
    if region is not None and gps_position is not None:
        raise Exception('Only one of region/gps_position can be provided')

    endpoint_uuid = endpoint_id.endpoint_uuid.uuid
    device_uuid = endpoint_id.device_id.device_uuid.uuid
    topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
    context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid

    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'endpoint_location': continue
        _endpoint_id = constraint.endpoint_location.endpoint_id
        if _endpoint_id.endpoint_uuid.uuid != endpoint_uuid: continue
        if _endpoint_id.device_id.device_uuid.uuid != device_uuid: continue
        if _endpoint_id.topology_id.topology_uuid.uuid != topology_uuid: continue
        if _endpoint_id.topology_id.context_id.context_uuid.uuid != context_uuid: continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member
        _endpoint_id = constraint.endpoint_location.endpoint_id
        _endpoint_id.endpoint_uuid.uuid = endpoint_uuid
        _endpoint_id.device_id.device_uuid.uuid = device_uuid
        _endpoint_id.topology_id.topology_uuid.uuid = topology_uuid
        _endpoint_id.topology_id.context_id.context_uuid.uuid = context_uuid

    constraint.action = new_action

    location = constraint.endpoint_location.location
    if region is not None:
        location.region = region
    elif gps_position is not None:
        location.gps_position.latitude = gps_position[0]
        location.gps_position.longitude = gps_position[1]
    return constraint

def update_constraint_endpoint_priority(
    constraints, endpoint_id : EndPointId, priority : int,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    endpoint_uuid = endpoint_id.endpoint_uuid.uuid
    device_uuid = endpoint_id.device_id.device_uuid.uuid
    topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
    context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid

    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'endpoint_priority': continue
        _endpoint_id = constraint.endpoint_priority.endpoint_id
        if _endpoint_id.endpoint_uuid.uuid != endpoint_uuid: continue
        if _endpoint_id.device_id.device_uuid.uuid != device_uuid: continue
        if _endpoint_id.topology_id.topology_uuid.uuid != topology_uuid: continue
        if _endpoint_id.topology_id.context_id.context_uuid.uuid != context_uuid: continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member
        _endpoint_id = constraint.endpoint_priority.endpoint_id
        _endpoint_id.endpoint_uuid.uuid = endpoint_uuid
        _endpoint_id.device_id.device_uuid.uuid = device_uuid
        _endpoint_id.topology_id.topology_uuid.uuid = topology_uuid
        _endpoint_id.topology_id.context_id.context_uuid.uuid = context_uuid

    constraint.action = new_action

    constraint.endpoint_priority.priority = priority
    return constraint

def update_constraint_sla_capacity(
    constraints, capacity_gbps : float,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'sla_capacity': continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member

    constraint.action = new_action

    constraint.sla_capacity.capacity_gbps = capacity_gbps
    return constraint

def update_constraint_sla_latency(
    constraints, e2e_latency_ms : float,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'sla_latency': continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member

    constraint.action = new_action

    constraint.sla_latency.e2e_latency_ms = e2e_latency_ms
    return constraint

def update_constraint_sla_availability(
    constraints, num_disjoint_paths : int, all_active : bool, availability : float,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'sla_availability': continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member

    constraint.action = new_action

    constraint.sla_availability.num_disjoint_paths = num_disjoint_paths
    constraint.sla_availability.all_active = all_active
    constraint.sla_availability.availability = availability
    return constraint

def update_constraint_sla_isolation(
    constraints, isolation_levels : List[int],
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'sla_isolation': continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member

    constraint.action = new_action

    for isolation_level in isolation_levels:
        if isolation_level in constraint.sla_isolation.isolation_level: continue
        constraint.sla_isolation.isolation_level.append(isolation_level)
    return constraint

def update_constraint_qos_profile(
    constraints, qos_profile_id : QoSProfileId, qos_profile_name : str,
    new_action : ConstraintActionEnum = ConstraintActionEnum.CONSTRAINTACTION_SET
) -> Constraint:
    for constraint in constraints:
        if constraint.WhichOneof('constraint') != 'qos_profile': continue
        break   # found, end loop
    else:
        # not found, add it
        constraint = constraints.add()      # pylint: disable=no-member

    constraint.action = new_action

    constraint.qos_profile.qos_profile_id.qos_profile_id.uuid = qos_profile_id.qos_profile_id.uuid
    constraint.qos_profile.qos_profile_name = qos_profile_name
    return constraint

def copy_constraints(source_constraints, target_constraints):
    for source_constraint in source_constraints:
        constraint_kind = source_constraint.WhichOneof('constraint')
        if constraint_kind == 'custom':
            custom = source_constraint.custom
            constraint_type = custom.constraint_type
            try:
                constraint_value = json.loads(custom.constraint_value)
            except: # pylint: disable=bare-except
                constraint_value = custom.constraint_value
            if isinstance(constraint_value, dict):
                raise_if_differs = True
                fields = {name:(value, raise_if_differs) for name,value in constraint_value.items()}
                update_constraint_custom_dict(target_constraints, constraint_type, fields)
            else:
                raise_if_differs = True
                update_constraint_custom_scalar(
                    target_constraints, constraint_type, constraint_value, raise_if_differs=raise_if_differs)

        elif constraint_kind == 'schedule':
            start_timestamp = source_constraint.schedule.start_timestamp
            duration_days   = source_constraint.schedule.duration_days
            update_constraint_schedule(target_constraints, start_timestamp, duration_days)

        elif constraint_kind == 'endpoint_location':
            endpoint_id = source_constraint.endpoint_location.endpoint_id
            location = source_constraint.endpoint_location.location
            location_kind = location.WhichOneof('location')
            if location_kind == 'region':
                region = location.region
                update_constraint_endpoint_location(target_constraints, endpoint_id, region=region)
            elif location_kind == 'gps_position':
                gps_position = location.gps_position
                gps_position = (gps_position.latitude, gps_position.longitude)
                update_constraint_endpoint_location(target_constraints, endpoint_id, gps_position=gps_position)
            else:
                str_constraint = grpc_message_to_json_string(source_constraint)
                raise NotImplementedError('Constraint({:s}): Location({:s})'.format(str_constraint, constraint_kind))

        elif constraint_kind == 'endpoint_priority':
            endpoint_id = source_constraint.endpoint_priority.endpoint_id
            priority = source_constraint.endpoint_priority.priority
            update_constraint_endpoint_priority(target_constraints, endpoint_id, priority)

        elif constraint_kind == 'sla_capacity':
            sla_capacity = source_constraint.sla_capacity
            capacity_gbps = sla_capacity.capacity_gbps
            update_constraint_sla_capacity(target_constraints, capacity_gbps)

        elif constraint_kind == 'sla_latency':
            sla_latency = source_constraint.sla_latency
            e2e_latency_ms = sla_latency.e2e_latency_ms
            update_constraint_sla_latency(target_constraints, e2e_latency_ms)

        elif constraint_kind == 'sla_availability':
            sla_availability = source_constraint.sla_availability
            num_disjoint_paths = sla_availability.num_disjoint_paths
            all_active = sla_availability.all_active
            availability = sla_availability.availability
            update_constraint_sla_availability(target_constraints, num_disjoint_paths, all_active, availability)

        elif constraint_kind == 'sla_isolation':
            sla_isolation = source_constraint.sla_isolation
            isolation_levels = sla_isolation.isolation_level
            update_constraint_sla_isolation(target_constraints, isolation_levels)

        elif constraint_kind == 'qos_profile':
            qos_profile_id   = source_constraint.qos_profile.qos_profile_id
            qos_profile_name = source_constraint.qos_profile.qos_profile_name
            update_constraint_qos_profile(target_constraints, qos_profile_id, qos_profile_name)

        else:
            raise NotImplementedError('Constraint({:s})'.format(grpc_message_to_json_string(source_constraint)))
