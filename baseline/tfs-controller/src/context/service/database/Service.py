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
    ContextId, Empty, EventTypeEnum, Service, ServiceFilter, ServiceId, ServiceIdList,
    ServiceList, ServiceTypeEnum
)
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import InvalidArgumentException, NotFoundException
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Service import json_service_id
from context.service.database.ConfigRule import compose_config_rules_data, upsert_config_rules
from context.service.database.Constraint import compose_constraints_data, upsert_constraints
from .models.enums.ServiceStatus import grpc_to_enum__service_status
from .models.enums.ServiceType import grpc_to_enum__service_type
from .models.ServiceModel import ServiceModel, ServiceEndPointModel
from .uuids.Context import context_get_uuid
from .uuids.EndPoint import endpoint_get_uuid
from .uuids.Service import service_get_uuid
from .Events import notify_event_context, notify_event_service

LOGGER = logging.getLogger(__name__)

def service_list_ids(db_engine : Engine, request : ContextId) -> ServiceIdList:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[ServiceModel] = session.query(ServiceModel).filter_by(context_uuid=context_uuid).all()
        return [obj.dump_id() for obj in obj_list]
    service_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return ServiceIdList(service_ids=service_ids)

def service_list_objs(db_engine : Engine, request : ContextId) -> ServiceList:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[ServiceModel] = session.query(ServiceModel)\
            .options(selectinload(ServiceModel.service_endpoints))\
            .options(selectinload(ServiceModel.constraints))\
            .options(selectinload(ServiceModel.config_rules))\
            .filter_by(context_uuid=context_uuid).all()
        return [obj.dump() for obj in obj_list]
    services = run_transaction(sessionmaker(bind=db_engine), callback)
    return ServiceList(services=services)

def service_get(db_engine : Engine, request : ServiceId) -> Service:
    _,service_uuid = service_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[ServiceModel] = session.query(ServiceModel)\
            .options(selectinload(ServiceModel.service_endpoints))\
            .options(selectinload(ServiceModel.constraints))\
            .options(selectinload(ServiceModel.config_rules))\
            .filter_by(service_uuid=service_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        context_uuid = context_get_uuid(request.context_id, allow_random=False)
        raw_service_uuid = '{:s}/{:s}'.format(request.context_id.context_uuid.uuid, request.service_uuid.uuid)
        raise NotFoundException('Service', raw_service_uuid, extra_details=[
            'context_uuid generated was: {:s}'.format(context_uuid),
            'service_uuid generated was: {:s}'.format(service_uuid),
        ])
    return Service(**obj)

def service_set(db_engine : Engine, messagebroker : MessageBroker, request : Service) -> ServiceId:
    raw_context_uuid = request.service_id.context_id.context_uuid.uuid
    raw_service_uuid = request.service_id.service_uuid.uuid
    raw_service_name = request.name
    service_name = raw_service_uuid if len(raw_service_name) == 0 else raw_service_name
    context_uuid,service_uuid = service_get_uuid(request.service_id, service_name=service_name, allow_random=True)

    service_type = grpc_to_enum__service_type(request.service_type)
    if service_type is None and request.service_type == ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY:
        service_type = "OPTICAL_CONNECTIVITY"
    if service_type is None and request.service_type == ServiceTypeEnum.SERVICETYPE_IP_LINK :
        service_type = "IP_LINK"
    if service_type is None and request.service_type == ServiceTypeEnum.SERVICETYPE_IPOWDM:
        service_type = "IPOWDM"
    if service_type is None and request.service_type == ServiceTypeEnum.SERVICETYPE_TAPI_LSP:
        service_type = "TAPI_LSP"

    service_status = grpc_to_enum__service_status(request.service_status.service_status)

    now = datetime.datetime.now(datetime.timezone.utc)

    service_endpoints_data : List[Dict] = list()
    for i,endpoint_id in enumerate(request.service_endpoint_ids):
        endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
        if len(endpoint_context_uuid) == 0:
            endpoint_context_uuid = context_get_uuid(request.service_id.context_id, allow_random=False)
        else:
            endpoint_context_uuid = context_get_uuid(endpoint_id.topology_id.context_id, allow_random=False)
        if endpoint_context_uuid != context_uuid:
            raise InvalidArgumentException(
                'request.service_endpoint_ids[{:d}].topology_id.context_id.context_uuid.uuid'.format(i),
                endpoint_context_uuid,
                ['should be == request.service_id.context_id.context_uuid.uuid({:s})'.format(raw_context_uuid)])

        _, _, endpoint_uuid = endpoint_get_uuid(endpoint_id, allow_random=False)
        service_endpoints_data.append({
            'service_uuid' : service_uuid,
            'endpoint_uuid': endpoint_uuid,
            'position'     : i,
        })

    constraints = compose_constraints_data(request.service_constraints, now, service_uuid=service_uuid)
    config_rules = compose_config_rules_data(request.service_config.config_rules, now, service_uuid=service_uuid)

    service_data = [{
        'context_uuid'  : context_uuid,
        'service_uuid'  : service_uuid,
        'service_name'  : service_name,
        'service_type'  : service_type,
        'service_status': service_status,
        'created_at'    : now,
        'updated_at'    : now,
    }]

    def callback(session : Session) -> bool:
        stmt = insert(ServiceModel).values(service_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[ServiceModel.service_uuid],
            set_=dict(
                service_name   = stmt.excluded.service_name,
                service_type   = stmt.excluded.service_type,
                service_status = stmt.excluded.service_status,
                updated_at     = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(ServiceModel.created_at, ServiceModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        updated = updated_at > created_at

        # TODO: check if endpoints are changed
        if len(service_endpoints_data) > 0:
            stmt = insert(ServiceEndPointModel).values(service_endpoints_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[ServiceEndPointModel.service_uuid, ServiceEndPointModel.endpoint_uuid]
            )
            session.execute(stmt)

        changed_constraints = upsert_constraints(session, constraints, service_uuid=service_uuid)
        changed_config_rules = upsert_config_rules(session, config_rules, service_uuid=service_uuid)

        return updated or changed_constraints or changed_config_rules

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    context_id = json_context_id(context_uuid)
    service_id = json_service_id(service_uuid, context_id=context_id)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_service(messagebroker, event_type, service_id)
    notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)
    return ServiceId(**service_id)

def service_unset(db_engine : Engine, messagebroker : MessageBroker, request : Service) -> ServiceId:
    raw_context_uuid = request.service_id.context_id.context_uuid.uuid
    raw_service_uuid = request.service_id.service_uuid.uuid
    raw_service_name = request.name
    service_name = raw_service_uuid if len(raw_service_name) == 0 else raw_service_name
    context_uuid,service_uuid = service_get_uuid(request.service_id, service_name=service_name, allow_random=False)

    service_endpoint_uuids : Set[str] = set()
    for i,endpoint_id in enumerate(request.service_endpoint_ids):
        endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
        if len(endpoint_context_uuid) == 0: endpoint_context_uuid = context_uuid
        if endpoint_context_uuid not in {raw_context_uuid, context_uuid}:
            raise InvalidArgumentException(
                'request.service_endpoint_ids[{:d}].topology_id.context_id.context_uuid.uuid'.format(i),
                endpoint_context_uuid,
                ['should be == request.service_id.context_id.context_uuid.uuid({:s})'.format(raw_context_uuid)])
        service_endpoint_uuids.add(endpoint_get_uuid(endpoint_id, allow_random=False)[2])

    now = datetime.datetime.now(datetime.timezone.utc)

    constraints = compose_constraints_data(request.service_constraints, now, service_uuid=service_uuid)
    config_rules = compose_config_rules_data(request.service_config.config_rules, now, service_uuid=service_uuid)

    def callback(session : Session) -> bool:
        num_deletes = 0
        if len(service_endpoint_uuids) > 0:
            num_deletes += session.query(ServiceEndPointModel)\
                .filter(and_(
                    ServiceEndPointModel.service_uuid == service_uuid,
                    ServiceEndPointModel.endpoint_uuid.in_(service_endpoint_uuids)
                )).delete()

        changed_constraints = upsert_constraints(session, constraints, is_delete=True, service_uuid=service_uuid)
        changed_config_rules = upsert_config_rules(session, config_rules, is_delete=True, service_uuid=service_uuid)

        return num_deletes > 0 or changed_constraints or changed_config_rules

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    service_id = json_service_id(service_uuid, json_context_id(context_uuid))
    if updated:
        notify_event_service(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, service_id)
    return ServiceId(**service_id)

def service_delete(db_engine : Engine, messagebroker : MessageBroker, request : ServiceId) -> Empty:
    context_uuid,service_uuid = service_get_uuid(request, allow_random=False)
    def callback(session : Session) -> bool:
        num_deleted = session.query(ServiceModel).filter_by(service_uuid=service_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    context_id = json_context_id(context_uuid)
    service_id = json_service_id(service_uuid, context_id=context_id)
    if deleted:
        notify_event_service(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, service_id)
        notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_UPDATE, context_id)
    return Empty()

def service_select(db_engine : Engine, request : ServiceFilter) -> ServiceList:
    service_uuids = [
        service_get_uuid(service_id, allow_random=False)[1]
        for service_id in request.service_ids.service_ids
    ]
    dump_params = dict(
        include_endpoint_ids=request.include_endpoint_ids,
        include_constraints =request.include_constraints,
        include_config_rules=request.include_config_rules,
    )
    def callback(session : Session) -> List[Dict]:
        query = session.query(ServiceModel)
        if request.include_endpoint_ids: query = query.options(selectinload(ServiceModel.service_endpoints))
        if request.include_constraints : query = query.options(selectinload(ServiceModel.constraints))
        if request.include_config_rules: query = query.options(selectinload(ServiceModel.config_rules))
        obj_list : List[ServiceModel] = query.filter(ServiceModel.service_uuid.in_(service_uuids)).all()
        return [obj.dump(**dump_params) for obj in obj_list]
    services = run_transaction(sessionmaker(bind=db_engine), callback)
    return ServiceList(services=services)
