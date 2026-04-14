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

import grpc, logging
from typing import Dict, List, Set, Tuple
from common.Checkers import chk_options, chk_string
from common.database.api.Database import Database
from common.database.api.context.Constants import DEFAULT_CONTEXT_ID, DEFAULT_TOPOLOGY_ID
from common.database.api.context.service.Service import Service
from slice.old_code.SliceStatus import SliceStatus, slicestatus_enum_values, to_slicestatus_enum
from common.database.api.context.topology.device.Endpoint import Endpoint
from common.exceptions.ServiceException import ServiceException
from common.proto.slice_pb2 import TransportSlice
from common.tools.service.ConstraintsChecker import check_constraints
from common.tools.service.EndpointIdCheckers import check_endpoint_id
from common.tools.service.DeviceCheckers import check_device_endpoint_exists
from common.tools.service.EnumCheckers import check_enum
from common.tools.service.ServiceCheckers import check_service_exists
from common.tools.service.SliceCheckers import check_slice_exists #, check_slice_not_exists

# For each method name, define acceptable slice statuses. Empty set means accept all.
ACCEPTED_SLICE_STATUSES : Dict[str, Set[SliceStatus]] = {
    'CreateUpdateSlice': set([SliceStatus.PLANNED, SliceStatus.INIT, SliceStatus.ACTIVE]),
    'DeleteSlice': set([SliceStatus.PLANNED, SliceStatus.DEINIT]),
}

def _check_slice_exists(method_name : str, database : Database, context_id : str, slice_id : str):
    if method_name in ['CreateUpdateSlice']:
        # Do nothing; creation implies checking slice does not exist. However, if it exists, we can perform an update.
        #check_slice_not_exists(database, context_id, slice_id)
        pass
    elif method_name in ['DeleteSlice']:
        check_slice_exists(database, context_id, slice_id)
    else:                                       # pragma: no cover (test requires malforming the code)
        msg = 'Unexpected condition [_check_slice_exists(method_name={}, slice_id={})]'
        msg = msg.format(str(method_name), str(slice_id))
        raise ServiceException(grpc.StatusCode.UNIMPLEMENTED, msg)

def _check_slice_endpoints(
    logger : logging.Logger, database : Database, context_id : str, slice_id : str, slice_endpoints
    ) -> List[Tuple[Endpoint, str]]:

    add_topology_devices_endpoints : Dict[str, Dict[str, Set[str]]] = {}
    db_endpoints__port_types : List[Tuple[Endpoint, str]] = []
    for endpoint_number,slice_endpoint in enumerate(slice_endpoints):
        parent_name = 'SliceEndpoint(#{}) of Context({})/Slice({})'
        parent_name = parent_name.format(endpoint_number, context_id, slice_id)

        ep_topology_id, ep_device_id, ep_port_id = check_endpoint_id(
            logger, endpoint_number, parent_name, slice_endpoint.port_id.port_id, add_topology_devices_endpoints,
            acceptable_context_ids=set([context_id]), prevent_same_device_multiple_times=False)

        try:
            ep_port_type = chk_string('endpoint[#{}].port_type'.format(endpoint_number),
                                      slice_endpoint.port_id.port_type,
                                      allow_empty=False)
        except Exception as e:
            logger.exception('Invalid arguments:')
            raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        db_endpoint = check_device_endpoint_exists(
            database, parent_name, context_id, ep_topology_id, ep_device_id, ep_port_id)
        db_endpoints__port_types.append((db_endpoint, ep_port_type))
    return db_endpoints__port_types

def _check_services(
    logger : logging.Logger, database : Database, parent_name : str, context_id : str, slice_service_ids
    ) -> List[Service]:

    add_context_services : Dict[str, Set[str]] = {}
    db_services : List[Service] = []
    for service_number,service_id in enumerate(slice_service_ids):
        # ----- Parse attributes ---------------------------------------------------------------------------------------
        try:
            service_context_id = chk_string ('services[#{}].contextId.contextUuid.uuid'.format(service_number),
                                             service_id.contextId.contextUuid.uuid,
                                             allow_empty=True)
            service_id         = chk_string ('services[#{}].cs_id.uuid'.format(service_number),
                                             service_id.cs_id.uuid,
                                             allow_empty=False)
        except Exception as e:
            logger.exception('Invalid arguments:')
            raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        if len(service_context_id) == 0: service_context_id = context_id

        add_services = add_context_services.setdefault(context_id, dict())
        if service_id in add_services:
            msg = 'Duplicated Context({})/Service({}) in {}.'
            msg = msg.format(service_context_id, service_id, parent_name)
            raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, msg)

        db_service = check_service_exists(database, service_context_id, service_id)
        db_services.append(db_service)
        add_services.add(service_id)
    return db_services

def _check_subslices(
    logger : logging.Logger, database : Database, parent_name : str, context_id : str, slice_subslice_ids
    ) -> List[Slice]:

    add_context_subslices : Dict[str, Set[str]] = {}
    db_subslices : List[Slice] = []
    for subslice_number,subslice_id in enumerate(slice_subslice_ids):
        # ----- Parse attributes ---------------------------------------------------------------------------------------
        try:
            subslice_context_id = chk_string ('subSlicesId[#{}].contextId.contextUuid.uuid'.format(subslice_number),
                                             subslice_id.contextId.contextUuid.uuid,
                                             allow_empty=True)
            subslice_id         = chk_string ('subSlicesId[#{}].slice_id.uuid'.format(subslice_number),
                                             subslice_id.slice_id.uuid,
                                             allow_empty=False)
        except Exception as e:
            logger.exception('Invalid arguments:')
            raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

        if len(subslice_context_id) == 0: subslice_context_id = context_id

        add_subslices = add_context_subslices.setdefault(context_id, dict())
        if subslice_id in add_subslices:
            msg = 'Duplicated Context({})/Slice({}) in {}.'
            msg = msg.format(subslice_context_id, subslice_id, parent_name)
            raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, msg)

        db_subslice = check_slice_exists(database, subslice_context_id, subslice_id)
        db_subslices.append(db_subslice)
        add_subslices.add(subslice_id)
    return db_subslices

def check_slice_status(method_name : str, value : str) -> SliceStatus:
    return check_enum(
        'SliceStatus', method_name, value, to_slicestatus_enum, ACCEPTED_SLICE_STATUSES)

def check_slice_request(
    method_name : str, request : TransportSlice, database : Database, logger : logging.Logger
    ): # -> Tuple[str, str, str, OperationalStatus, List[Tuple[Endpoint, str]]]:

    # ----- Parse attributes -------------------------------------------------------------------------------------------
    try:
        context_id        = chk_string ('slice.slice_id.contextId.contextUuid.uuid',
                                        request.slice_id.contextId.contextUuid.uuid,
                                        allow_empty=True)
        slice_id          = chk_string ('slice.slice_id.slice_id.uuid',
                                        request.slice_id.slice_id.uuid,
                                        allow_empty=False)
        status_context_id = chk_string ('slice.status.slice_id.contextId.contextUuid.uuid',
                                        request.status.slice_id.contextId.contextUuid.uuid,
                                        allow_empty=True)
        status_slice_id   = chk_string ('slice.status.slice_id.slice_id.uuid',
                                        request.status.slice_id.slice_id.uuid,
                                        allow_empty=True)
        slice_status      = chk_options('slice.status.status',
                                        request.status.status,
                                        slicestatus_enum_values())
    except Exception as e:
        logger.exception('Invalid arguments:')
        raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    if len(context_id) == 0: context_id = DEFAULT_CONTEXT_ID

    if (len(status_context_id) > 0) and (status_context_id != context_id):
        msg = ' '.join([
            'slice.status.slice_id.contextId.contextUuid.uuid({})',
            'is not empty and is different than',
            'slice.slice_id.contextId.contextUuid.uuid({}).',
            'Optionally, leave field empty to use slice.slice_id.contextId.contextUuid.uuid({}), if set,',
            'or, otherwise, the default Context({})'
        ])
        msg = msg.format(
            status_context_id, context_id, context_id, DEFAULT_CONTEXT_ID)
        raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, msg)
        
    if (len(status_slice_id) > 0) and (status_slice_id != slice_id):
        msg = ' '.join([
            'slice.status.slice_id.slice_id.uuid({})',
            'is not empty and is different than',
            'slice.slice_id.slice_id.uuid({}).',
            'Optionally, leave field empty to use slice.slice_id.slice_id.uuid({}).',
        ])
        msg = msg.format(
            status_slice_id, slice_id, slice_id)
        raise ServiceException(grpc.StatusCode.INVALID_ARGUMENT, msg)

    slice_status = check_slice_status(method_name, slice_status)

    # ----- Check if slice exists in database --------------------------------------------------------------------------
    _check_slice_exists(method_name, database, context_id, slice_id)

    # ----- Parse endpoints and check if they exist in the database as device endpoints --------------------------------
    db_endpoints__port_types = _check_slice_endpoints(logger, database, context_id, slice_id, request.endpoints)

    # ----- Parse constraints ------------------------------------------------------------------------------------------
    parent_name = 'Context({})/Slice({})'.format(context_id, slice_id)
    constraint_tuples : List[Tuple[str, str]] = check_constraints(logger, parent_name, request.constraints)

    # ----- Parse Service Ids ------------------------------------------------------------------------------------------
    db_services = _check_services(logger, database, parent_name, context_id, request.services)

    # ----- Parse SubSlice Ids -----------------------------------------------------------------------------------------
    db_subslices = _check_subslices(logger, database, parent_name, context_id, request.subSlicesId)

    return context_id, slice_id, slice_status, db_endpoints__port_types, constraint_tuples, db_services, db_subslices
