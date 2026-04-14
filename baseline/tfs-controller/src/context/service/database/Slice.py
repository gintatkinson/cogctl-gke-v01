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

import datetime, logging
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import Dict, List, Optional, Set
from common.proto.context_pb2 import (
    ContextId, Empty, EventTypeEnum, Slice, SliceFilter, SliceId, SliceIdList, SliceList)
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import InvalidArgumentException, NotFoundException
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Slice import json_slice_id
from context.service.database.ConfigRule import compose_config_rules_data, upsert_config_rules
from context.service.database.Constraint import compose_constraints_data, upsert_constraints
from .models.enums.SliceStatus import grpc_to_enum__slice_status
from .models.SliceModel import SliceModel, SliceEndPointModel, SliceServiceModel, SliceSubSliceModel
from .uuids.Context import context_get_uuid
from .uuids.EndPoint import endpoint_get_uuid
from .uuids.Service import service_get_uuid
from .uuids.Slice import slice_get_uuid
from .Events import notify_event_context, notify_event_slice

LOGGER = logging.getLogger(__name__)

def slice_list_ids(db_engine : Engine, request : ContextId) -> SliceIdList:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[SliceModel] = session.query(SliceModel).filter_by(context_uuid=context_uuid).all()
        return [obj.dump_id() for obj in obj_list]
    slice_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return SliceIdList(slice_ids=slice_ids)

def slice_list_objs(db_engine : Engine, request : ContextId) -> SliceList:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[SliceModel] = session.query(SliceModel)\
            .options(selectinload(SliceModel.slice_endpoints))\
            .options(selectinload(SliceModel.slice_services))\
            .options(selectinload(SliceModel.slice_subslices))\
            .options(selectinload(SliceModel.constraints))\
            .options(selectinload(SliceModel.config_rules))\
            .filter_by(context_uuid=context_uuid).all()
        return [obj.dump() for obj in obj_list]
    slices = run_transaction(sessionmaker(bind=db_engine), callback)
    return SliceList(slices=slices)

def slice_get(db_engine : Engine, request : SliceId) -> Slice:
    _,slice_uuid = slice_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[SliceModel] = session.query(SliceModel)\
            .options(selectinload(SliceModel.slice_endpoints))\
            .options(selectinload(SliceModel.slice_services))\
            .options(selectinload(SliceModel.slice_subslices))\
            .options(selectinload(SliceModel.constraints))\
            .options(selectinload(SliceModel.config_rules))\
            .filter_by(slice_uuid=slice_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        context_uuid = context_get_uuid(request.context_id, allow_random=False)
        raw_slice_uuid = '{:s}/{:s}'.format(request.context_id.context_uuid.uuid, request.slice_uuid.uuid)
        raise NotFoundException('Slice', raw_slice_uuid, extra_details=[
            'context_uuid generated was: {:s}'.format(context_uuid),
            'slice_uuid generated was: {:s}'.format(slice_uuid),
        ])
    return Slice(**obj)

def slice_set(db_engine : Engine, messagebroker : MessageBroker, request : Slice) -> SliceId:
    raw_context_uuid = request.slice_id.context_id.context_uuid.uuid
    raw_slice_uuid = request.slice_id.slice_uuid.uuid
    raw_slice_name = request.name
    slice_name = raw_slice_uuid if len(raw_slice_name) == 0 else raw_slice_name
    context_uuid,slice_uuid = slice_get_uuid(request.slice_id, slice_name=slice_name, allow_random=True)

    slice_status = grpc_to_enum__slice_status(request.slice_status.slice_status)

    now = datetime.datetime.now(datetime.timezone.utc)

    slice_endpoints_data : List[Dict] = list()
    for i,endpoint_id in enumerate(request.slice_endpoint_ids):
        endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
        if len(endpoint_context_uuid) == 0:
            endpoint_context_uuid = context_get_uuid(request.slice_id.context_id, allow_random=False)
        else:
            endpoint_context_uuid = context_get_uuid(endpoint_id.topology_id.context_id, allow_random=False)
        if endpoint_context_uuid != context_uuid:
            raise InvalidArgumentException(
                'request.slice_endpoint_ids[{:d}].topology_id.context_id.context_uuid.uuid'.format(i),
                endpoint_context_uuid,
                ['should be == request.slice_id.context_id.context_uuid.uuid({:s})'.format(raw_context_uuid)])

        _, _, endpoint_uuid = endpoint_get_uuid(endpoint_id, allow_random=False)
        slice_endpoints_data.append({
            'slice_uuid'   : slice_uuid,
            'endpoint_uuid': endpoint_uuid,
            'position'     : i,
        })

    slice_services_data : List[Dict] = list()
    for i,service_id in enumerate(request.slice_service_ids):
        _, service_uuid = service_get_uuid(service_id, allow_random=False)
        slice_services_data.append({
            'slice_uuid'  : slice_uuid,
            'service_uuid': service_uuid,
        })

    slice_subslices_data : List[Dict] = list()
    for i,subslice_id in enumerate(request.slice_subslice_ids):
        _, subslice_uuid = slice_get_uuid(subslice_id, allow_random=False)
        slice_subslices_data.append({
            'slice_uuid'   : slice_uuid,
            'subslice_uuid': subslice_uuid,
        })

    constraints = compose_constraints_data(request.slice_constraints, now, slice_uuid=slice_uuid)
    config_rules = compose_config_rules_data(request.slice_config.config_rules, now, slice_uuid=slice_uuid)

    slice_data = [{
        'context_uuid'      : context_uuid,
        'slice_uuid'        : slice_uuid,
        'slice_name'        : slice_name,
        'slice_status'      : slice_status,
        'slice_owner_uuid'  : request.slice_owner.owner_uuid.uuid,
        'slice_owner_string': request.slice_owner.owner_string,
        'created_at'        : now,
        'updated_at'        : now,
    }]

    def callback(session : Session) -> bool:
        stmt = insert(SliceModel).values(slice_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[SliceModel.slice_uuid],
            set_=dict(
                slice_name         = stmt.excluded.slice_name,
                slice_status       = stmt.excluded.slice_status,
                updated_at         = stmt.excluded.updated_at,
                slice_owner_uuid   = stmt.excluded.slice_owner_uuid,
                slice_owner_string = stmt.excluded.slice_owner_string,
            )
        )
        stmt = stmt.returning(SliceModel.created_at, SliceModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        updated = updated_at > created_at

        # TODO: check if endpoints are changed
        if len(slice_endpoints_data) > 0:
            stmt = insert(SliceEndPointModel).values(slice_endpoints_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[SliceEndPointModel.slice_uuid, SliceEndPointModel.endpoint_uuid]
            )
            session.execute(stmt)

        # TODO: check if services are changed
        if len(slice_services_data) > 0:
            stmt = insert(SliceServiceModel).values(slice_services_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[SliceServiceModel.slice_uuid, SliceServiceModel.service_uuid]
            )
            session.execute(stmt)

        # TODO: check if subslices are changed
        if len(slice_subslices_data) > 0:
            stmt = insert(SliceSubSliceModel).values(slice_subslices_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[SliceSubSliceModel.slice_uuid, SliceSubSliceModel.subslice_uuid]
            )
            session.execute(stmt)

        changed_constraints = upsert_constraints(session, constraints, slice_uuid=slice_uuid)
        changed_config_rules = upsert_config_rules(session, config_rules, slice_uuid=slice_uuid)

        return updated or changed_constraints or changed_config_rules

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    context_id = json_context_id(context_uuid)
    slice_id = json_slice_id(slice_uuid, context_id=context_id)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_slice(messagebroker, event_type, slice_id)
    notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)
    return SliceId(**slice_id)

def slice_unset(db_engine : Engine, messagebroker : MessageBroker, request : Slice) -> SliceId:
    raw_context_uuid = request.slice_id.context_id.context_uuid.uuid
    raw_slice_uuid = request.slice_id.slice_uuid.uuid
    raw_slice_name = request.name
    slice_name = raw_slice_uuid if len(raw_slice_name) == 0 else raw_slice_name
    context_uuid,slice_uuid = slice_get_uuid(request.slice_id, slice_name=slice_name, allow_random=False)

    slice_endpoint_uuids : Set[str] = set()
    for i,endpoint_id in enumerate(request.slice_endpoint_ids):
        endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
        if len(endpoint_context_uuid) == 0: endpoint_context_uuid = context_uuid
        if endpoint_context_uuid not in {raw_context_uuid, context_uuid}:
            raise InvalidArgumentException(
                'request.slice_endpoint_ids[{:d}].topology_id.context_id.context_uuid.uuid'.format(i),
                endpoint_context_uuid,
                ['should be == request.slice_id.context_id.context_uuid.uuid({:s})'.format(raw_context_uuid)])
        slice_endpoint_uuids.add(endpoint_get_uuid(endpoint_id, allow_random=False)[2])

    slice_service_uuids : Set[str] = {
        service_get_uuid(service_id, allow_random=False)[1]
        for service_id in request.slice_service_ids
    }

    slice_subslice_uuids : Set[str] = {
        slice_get_uuid(subslice_id, allow_random=False)[1]
        for subslice_id in request.slice_subslice_ids
    }

    now = datetime.datetime.now(datetime.timezone.utc)

    constraints = compose_constraints_data(request.slice_constraints, now, slice_uuid=slice_uuid)
    config_rules = compose_config_rules_data(request.slice_config.config_rules, now, slice_uuid=slice_uuid)

    def callback(session : Session) -> bool:
        num_deletes = 0
        if len(slice_service_uuids) > 0:
            num_deletes += session.query(SliceServiceModel)\
                .filter(and_(
                    SliceServiceModel.slice_uuid == slice_uuid,
                    SliceServiceModel.service_uuid.in_(slice_service_uuids)
                )).delete()
        if len(slice_subslice_uuids) > 0:
            num_deletes += session.query(SliceSubSliceModel)\
                .filter(and_(
                    SliceSubSliceModel.slice_uuid == slice_uuid,
                    SliceSubSliceModel.subslice_uuid.in_(slice_subslice_uuids)
                )).delete()
        if len(slice_endpoint_uuids) > 0:
            num_deletes += session.query(SliceEndPointModel)\
                .filter(and_(
                    SliceEndPointModel.slice_uuid == slice_uuid,
                    SliceEndPointModel.endpoint_uuid.in_(slice_endpoint_uuids)
                )).delete()

        changed_constraints = upsert_constraints(session, constraints, is_delete=True, slice_uuid=slice_uuid)
        changed_config_rules = upsert_config_rules(session, config_rules, is_delete=True, slice_uuid=slice_uuid)

        return num_deletes > 0 or changed_constraints or changed_config_rules

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    slice_id = json_slice_id(slice_uuid, json_context_id(context_uuid))
    if updated:
        notify_event_slice(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, slice_id)
    return SliceId(**slice_id)

def slice_delete(db_engine : Engine, messagebroker : MessageBroker, request : SliceId) -> Empty:
    context_uuid,slice_uuid = slice_get_uuid(request, allow_random=False)
    def callback(session : Session) -> bool:
        num_deleted = session.query(SliceModel).filter_by(slice_uuid=slice_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    context_id = json_context_id(context_uuid)
    slice_id = json_slice_id(slice_uuid, context_id=context_id)
    if deleted:
        notify_event_slice(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, slice_id)
        notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)
    return Empty()

def slice_select(db_engine : Engine, request : SliceFilter) -> SliceList:
    slice_uuids = [
        slice_get_uuid(slice_id, allow_random=False)[1]
        for slice_id in request.slice_ids.slice_ids
    ]
    dump_params = dict(
        include_endpoint_ids=request.include_endpoint_ids,
        include_constraints =request.include_constraints,
        include_service_ids =request.include_service_ids,
        include_subslice_ids=request.include_subslice_ids,
        include_config_rules=request.include_config_rules,
    )
    def callback(session : Session) -> List[Dict]:
        query = session.query(SliceModel)
        if request.include_endpoint_ids: query = query.options(selectinload(SliceModel.slice_endpoints))
        if request.include_service_ids : query = query.options(selectinload(SliceModel.slice_services))
        if request.include_subslice_ids: query = query.options(selectinload(SliceModel.slice_subslices))
        if request.include_constraints : query = query.options(selectinload(SliceModel.constraints))
        if request.include_config_rules: query = query.options(selectinload(SliceModel.config_rules))
        obj_list : List[SliceModel] = query.filter(SliceModel.slice_uuid.in_(slice_uuids)).all()
        return [obj.dump(**dump_params) for obj in obj_list]
    slices = run_transaction(sessionmaker(bind=db_engine), callback)
    return SliceList(slices=slices)
