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

from typing import Dict, List, Optional, Set, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME
from common.Settings import get_setting
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.proto.context_pb2 import IsolationLevelEnum, Slice, SliceId, SliceStatusEnum
from common.tools.context_queries.Context import create_context
from common.tools.context_queries.Slice import get_slice_by_uuid
from context.client.ContextClient import ContextClient
from slice.service.slice_grouper.MetricsExporter import MetricsExporter

SETTING_NAME_SLICE_GROUPING = 'SLICE_GROUPING'
TRUE_VALUES = {'Y', 'YES', 'TRUE', 'T', 'E', 'ENABLE', 'ENABLED'}

NO_ISOLATION = IsolationLevelEnum.NO_ISOLATION

def is_slice_grouping_enabled() -> bool:
    is_enabled = get_setting(SETTING_NAME_SLICE_GROUPING, default=None)
    if is_enabled is None: return False
    str_is_enabled = str(is_enabled).upper()
    return str_is_enabled in TRUE_VALUES

def create_slice_group(
    context_uuid : str, slice_name : str, capacity_gbps : float, availability : float
) -> Slice:
    slice_group_obj = Slice()
    slice_group_obj.slice_id.context_id.context_uuid.uuid = context_uuid            # pylint: disable=no-member
    slice_group_obj.slice_id.slice_uuid.uuid = slice_name                           # pylint: disable=no-member
    slice_group_obj.name = slice_name
    slice_group_obj.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_ACTIVE  # pylint: disable=no-member
    #del slice_group_obj.slice_endpoint_ids[:] # no endpoints initially
    #del slice_group_obj.slice_service_ids[:] # no sub-services
    #del slice_group_obj.slice_subslice_ids[:] # no sub-slices
    #del slice_group_obj.slice_config.config_rules[:] # no config rules
    slice_group_obj.slice_owner.owner_uuid.uuid = 'TeraFlowSDN'                     # pylint: disable=no-member
    slice_group_obj.slice_owner.owner_string = 'TeraFlowSDN'                        # pylint: disable=no-member

    constraint_sla_capacity = slice_group_obj.slice_constraints.add()               # pylint: disable=no-member
    constraint_sla_capacity.sla_capacity.capacity_gbps = capacity_gbps

    constraint_sla_availability = slice_group_obj.slice_constraints.add()           # pylint: disable=no-member
    constraint_sla_availability.sla_availability.num_disjoint_paths = 1
    constraint_sla_availability.sla_availability.all_active = True
    constraint_sla_availability.sla_availability.availability = availability

    constraint_sla_isolation = slice_group_obj.slice_constraints.add()              # pylint: disable=no-member
    constraint_sla_isolation.sla_isolation.isolation_level.append(NO_ISOLATION)

    return slice_group_obj

def create_slice_groups(
    slice_groups : List[Tuple[str, float, float]], context_uuid : str = DEFAULT_CONTEXT_NAME
) -> Dict[str, SliceId]:
    context_client = ContextClient()
    create_context(context_client, context_uuid)

    slice_group_ids : Dict[str, SliceId] = dict()
    for slice_group in slice_groups:
        slice_group_name = slice_group[0]
        slice_group_obj = get_slice_by_uuid(context_client, slice_group_name, DEFAULT_CONTEXT_NAME)
        if slice_group_obj is None:
            slice_group_obj = create_slice_group(
                DEFAULT_CONTEXT_NAME, slice_group_name, slice_group[2], slice_group[1])
            slice_group_id = context_client.SetSlice(slice_group_obj)
            slice_group_ids[slice_group_name] = slice_group_id
        else:
            slice_group_ids[slice_group_name] = slice_group_obj.slice_id

    return slice_group_ids

def get_slice_grouping_parameters(slice_obj : Slice) -> Optional[Tuple[float, float]]:
    isolation_levels : Set[int] = set()
    availability : Optional[float] = None
    capacity_gbps : Optional[float] = None

    for constraint in slice_obj.slice_constraints:
        kind = constraint.WhichOneof('constraint')
        if kind == 'sla_isolation':
            isolation_levels.update(constraint.sla_isolation.isolation_level)
        elif kind == 'sla_capacity':
            capacity_gbps = constraint.sla_capacity.capacity_gbps
        elif kind == 'sla_availability':
            availability = constraint.sla_availability.availability
        else:
            continue

    no_isolation_level = len(isolation_levels) == 0
    single_isolation_level = len(isolation_levels) == 1
    has_no_isolation_level = NO_ISOLATION in isolation_levels
    can_be_grouped = no_isolation_level or (single_isolation_level and has_no_isolation_level)
    if not can_be_grouped: return None
    if availability is None: return None
    if capacity_gbps is None: return None
    return availability, capacity_gbps

def add_slice_to_group(slice_obj : Slice, selected_group : Tuple[str, float, float]) -> bool:
    group_name, availability, capacity_gbps = selected_group
    slice_uuid = slice_obj.slice_id.slice_uuid.uuid

    context_client = ContextClient()
    slice_group_obj = get_slice_by_uuid(context_client, group_name, DEFAULT_CONTEXT_NAME, rw_copy=True)
    if slice_group_obj is None:
        raise NotFoundException('Slice', group_name, extra_details='while adding to group')

    del slice_group_obj.slice_endpoint_ids[:]
    for endpoint_id in slice_obj.slice_endpoint_ids:
        slice_group_obj.slice_endpoint_ids.add().CopyFrom(endpoint_id)

    del slice_group_obj.slice_constraints[:]
    del slice_group_obj.slice_service_ids[:]

    del slice_group_obj.slice_subslice_ids[:]
    slice_group_obj.slice_subslice_ids.add().CopyFrom(slice_obj.slice_id)

    del slice_group_obj.slice_config.config_rules[:]
    for config_rule in slice_obj.slice_config.config_rules:
        group_config_rule = slice_group_obj.slice_config.config_rules.add()
        group_config_rule.CopyFrom(config_rule)
        if config_rule.WhichOneof('config_rule') != 'custom': continue
        TEMPLATE = '/subslice[{:s}]{:s}'
        slice_resource_key = config_rule.custom.resource_key
        group_resource_key = TEMPLATE.format(slice_uuid, slice_resource_key)
        group_config_rule.custom.resource_key = group_resource_key

    context_client.SetSlice(slice_group_obj)

    metrics_exporter = MetricsExporter()
    metrics_exporter.export_point(
        slice_uuid, group_name, availability, capacity_gbps, is_center=False)

    return True

def remove_slice_from_group(slice_obj : Slice, selected_group : Tuple[str, float, float]) -> bool:
    group_name, _, _ = selected_group
    slice_uuid = slice_obj.slice_id.slice_uuid.uuid

    context_client = ContextClient()
    slice_group_obj = get_slice_by_uuid(context_client, group_name, DEFAULT_CONTEXT_NAME, rw_copy=True)
    if slice_group_obj is None:
        raise NotFoundException('Slice', group_name, extra_details='while removing from group')

    if slice_obj.slice_id in slice_group_obj.slice_subslice_ids:
        tmp_slice_group_obj = Slice()
        tmp_slice_group_obj.slice_id.CopyFrom(slice_group_obj.slice_id)             # pylint: disable=no-member

        tmp_slice_group_obj.slice_subslice_ids.add().CopyFrom(slice_obj.slice_id)   # pylint: disable=no-member

        for endpoint_id in slice_obj.slice_endpoint_ids:
            tmp_slice_group_obj.slice_endpoint_ids.add().CopyFrom(endpoint_id)      # pylint: disable=no-member

        for config_rule in slice_obj.slice_config.config_rules:
            group_config_rule = tmp_slice_group_obj.slice_config.config_rules.add() # pylint: disable=no-member
            group_config_rule.CopyFrom(config_rule)
            if group_config_rule.WhichOneof('config_rule') != 'custom': continue
            TEMPLATE = '/subslice[{:s}]{:s}'
            slice_resource_key = group_config_rule.custom.resource_key
            group_resource_key = TEMPLATE.format(slice_uuid, slice_resource_key)
            group_config_rule.custom.resource_key = group_resource_key

        context_client.UnsetSlice(tmp_slice_group_obj)

    metrics_exporter = MetricsExporter()
    metrics_exporter.delete_point(slice_uuid)
    return True
