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
import grpc
from typing import Optional, Tuple, Union
from uuid import UUID, uuid5
from common.Constants import DEFAULT_CONTEXT_NAME
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from common.proto.context_pb2 import ContextId, Slice, SliceFilter, SliceId
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from common.proto.context_pb2 import ContextId, Slice, SliceFilter, SliceId
from context.client.ContextClient import ContextClient


NAMESPACE_TFS = UUID("200e3a1f-2223-534f-a100-758e29c37f40")

LOGGER = logging.getLogger(__name__)

def get_slice_by_id(
    context_client : ContextClient, slice_id : SliceId, rw_copy : bool = False, include_endpoint_ids : bool = True,
    include_constraints : bool = True, include_service_ids : bool = True, include_subslice_ids : bool = True,
    include_config_rules : bool = True
) -> Optional[Slice]:
    slice_filter = SliceFilter()
    slice_id = slice_filter.slice_ids.slice_ids.append(slice_id) # pylint: disable=no-member
    slice_filter.include_endpoint_ids = include_endpoint_ids
    slice_filter.include_constraints = include_constraints
    slice_filter.include_service_ids = include_service_ids
    slice_filter.include_subslice_ids = include_subslice_ids
    slice_filter.include_config_rules = include_config_rules

    try:
        ro_slices = context_client.SelectSlice(slice_filter)
        if len(ro_slices.slices) == 0: return None
        assert len(ro_slices.slices) == 1
        ro_slice = ro_slices.slices[0]
        if not rw_copy: return ro_slice
        rw_slice = Slice()
        rw_slice.CopyFrom(ro_slice)
        return rw_slice
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.NOT_FOUND: raise # pylint: disable=no-member
        #LOGGER.exception('Unable to get slice({:s} / {:s})'.format(str(context_uuid), str(slice_uuid)))
        return None

def get_slice_by_uuid(
    context_client : ContextClient, slice_uuid : str, context_uuid : str = DEFAULT_CONTEXT_NAME,
    rw_copy : bool = False, include_endpoint_ids : bool = True, include_constraints : bool = True,
    include_service_ids : bool = True, include_subslice_ids : bool = True, include_config_rules : bool = True
) -> Optional[Slice]:
    slice_id = SliceId()
    slice_id.context_id.context_uuid.uuid = context_uuid    # pylint: disable=no-member
    slice_id.slice_uuid.uuid = slice_uuid                   # pylint: disable=no-member
    return get_slice_by_id(
        context_client, slice_id, rw_copy=rw_copy, include_endpoint_ids=include_endpoint_ids,
        include_constraints=include_constraints, include_service_ids=include_service_ids,
        include_subslice_ids=include_subslice_ids, include_config_rules=include_config_rules)


def get_uuid_from_string(
    str_uuid_or_name: Union[str, UUID], prefix_for_name: Optional[str] = None
) -> str:
    # if UUID given, assume it is already a valid UUID
    if isinstance(str_uuid_or_name, UUID):
        return str_uuid_or_name
    if not isinstance(str_uuid_or_name, str):
        MSG = "Parameter({:s}) cannot be used to produce a UUID"
        raise Exception(MSG.format(str(repr(str_uuid_or_name))))
    try:
        # try to parse as UUID
        return str(UUID(str_uuid_or_name))
    except:  # pylint: disable=bare-except
        # produce a UUID within TFS namespace from parameter
        if prefix_for_name is not None:
            str_uuid_or_name = "{:s}/{:s}".format(prefix_for_name, str_uuid_or_name)
        return str(uuid5(NAMESPACE_TFS, str_uuid_or_name))


def context_get_uuid(
    context_id: ContextId,
    context_name: str = "",
    allow_random: bool = False,
    allow_default: bool = False,
) -> str:
    context_uuid = context_id.context_uuid.uuid

    if len(context_uuid) > 0:
        return get_uuid_from_string(context_uuid)
    if len(context_name) > 0:
        return get_uuid_from_string(context_name)
    if allow_default:
        return get_uuid_from_string(DEFAULT_CONTEXT_NAME)

    raise InvalidArgumentsException(
        [
            ("context_id.context_uuid.uuid", context_uuid),
            ("name", context_name),
        ],
        extra_details=["At least one is required to produce a Context UUID"],
    )


def slice_get_uuid(slice_id: SliceId) -> Tuple[str, str]:
    context_uuid = context_get_uuid(slice_id.context_id, allow_random=False)
    raw_slice_uuid = slice_id.slice_uuid.uuid

    if len(raw_slice_uuid) > 0:
        return context_uuid, get_uuid_from_string(
            raw_slice_uuid, prefix_for_name=context_uuid
        )

    raise InvalidArgumentsException(
        [
            ("slice_id.slice_uuid.uuid", raw_slice_uuid),
        ],
        extra_details=["At least one is required to produce a Slice UUID"],
    )

def get_slice_by_defualt_id(
    context_client : ContextClient, default_slice_id : SliceId, context_uuid : str = DEFAULT_CONTEXT_NAME,
    rw_copy : bool = False, include_endpoint_ids : bool = True, include_constraints : bool = True,
    include_service_ids : bool = True, include_subslice_ids : bool = True, include_config_rules : bool = True
) -> Optional[Slice]:
    context_uuid, slice_uuid = slice_get_uuid(default_slice_id)
    LOGGER.debug(f'P60: {context_uuid} {slice_uuid}')
    slice_id = SliceId()
    slice_id.context_id.context_uuid.uuid = context_uuid    # pylint: disable=no-member
    slice_id.slice_uuid.uuid = slice_uuid                   # pylint: disable=no-member
    return get_slice_by_id(
        context_client, slice_id, rw_copy=rw_copy, include_endpoint_ids=include_endpoint_ids,
        include_constraints=include_constraints, include_service_ids=include_service_ids,
        include_subslice_ids=include_subslice_ids, include_config_rules=include_config_rules)


def get_slice_by_defualt_name(
    context_client : ContextClient, slice_name : str, context_uuid : str = DEFAULT_CONTEXT_NAME,
    rw_copy : bool = False, include_endpoint_ids : bool = True, include_constraints : bool = True,
    include_service_ids : bool = True, include_subslice_ids : bool = True, include_config_rules : bool = True
) -> Optional[Slice]:
    default_slice_id = SliceId()
    default_slice_id.context_id.context_uuid.uuid = context_uuid    # pylint: disable=no-member
    default_slice_id.slice_uuid.uuid = slice_name                   # pylint: disable=no-member
    context_uuid, slice_uuid = slice_get_uuid(default_slice_id)
    slice_id = SliceId()
    slice_id.context_id.context_uuid.uuid = context_uuid    # pylint: disable=no-member
    slice_id.slice_uuid.uuid = slice_uuid                   # pylint: disable=no-member
    return get_slice_by_id(
        context_client, slice_id, rw_copy=rw_copy, include_endpoint_ids=include_endpoint_ids,
        include_constraints=include_constraints, include_service_ids=include_service_ids,
        include_subslice_ids=include_subslice_ids, include_config_rules=include_config_rules)
