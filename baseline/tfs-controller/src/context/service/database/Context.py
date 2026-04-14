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
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import Dict, List, Optional
from common.proto.context_pb2 import Context, ContextId, ContextIdList, ContextList, Empty, EventTypeEnum
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.tools.object_factory.Context import json_context_id
from .models.ContextModel import ContextModel
from .uuids.Context import context_get_uuid
from .Events import notify_event_context

LOGGER = logging.getLogger(__name__)

def context_list_ids(db_engine : Engine) -> ContextIdList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[ContextModel] = session.query(ContextModel).all()
        return [obj.dump_id() for obj in obj_list]
    context_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return ContextIdList(context_ids=context_ids)

def context_list_objs(db_engine : Engine) -> ContextList:
    def callback(session : Session) -> List[Dict]:
        obj_list : List[ContextModel] = session.query(ContextModel)\
            .options(selectinload(ContextModel.topologies))\
            .options(selectinload(ContextModel.services))\
            .options(selectinload(ContextModel.slices))\
            .all()
        return [obj.dump() for obj in obj_list]
    contexts = run_transaction(sessionmaker(bind=db_engine), callback)
    return ContextList(contexts=contexts)

def context_get(db_engine : Engine, request : ContextId) -> Context:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[ContextModel] = session.query(ContextModel)\
            .options(selectinload(ContextModel.topologies))\
            .options(selectinload(ContextModel.services))\
            .options(selectinload(ContextModel.slices))\
            .filter_by(context_uuid=context_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        raw_context_uuid = request.context_uuid.uuid
        raise NotFoundException('Context', raw_context_uuid, extra_details=[
            'context_uuid generated was: {:s}'.format(context_uuid)
        ])
    return Context(**obj)

def context_set(db_engine : Engine, messagebroker : MessageBroker, request : Context) -> ContextId:
    context_name = request.name
    if len(context_name) == 0: context_name = request.context_id.context_uuid.uuid
    context_uuid = context_get_uuid(request.context_id, context_name=context_name, allow_random=True)

    # Ignore request.topology_ids, request.service_ids, and request.slice_ids. They are used
    # for retrieving topologies, services and slices added into the context. Explicit addition
    # into the context is done automatically qhen creating the topology, service or slice
    # specifying the associated context.

    if len(request.topology_ids) > 0:   # pragma: no cover
        LOGGER.warning('Items in field "topology_ids" ignored. This field is used for retrieval purposes only.')

    if len(request.service_ids) > 0:    # pragma: no cover
        LOGGER.warning('Items in field "service_ids" ignored. This field is used for retrieval purposes only.')

    if len(request.slice_ids) > 0:      # pragma: no cover
        LOGGER.warning('Items in field "slice_ids" ignored. This field is used for retrieval purposes only.')

    now = datetime.datetime.now(datetime.timezone.utc)

    context_data = [{
        'context_uuid': context_uuid,
        'context_name': context_name,
        'created_at'  : now,
        'updated_at'  : now,
    }]

    def callback(session : Session) -> bool:
        stmt = insert(ContextModel).values(context_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[ContextModel.context_uuid],
            set_=dict(
                context_name = stmt.excluded.context_name,
                updated_at   = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(ContextModel.created_at, ContextModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        return updated_at > created_at

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    context_id = json_context_id(context_uuid)
    notify_event_context(messagebroker, event_type, context_id)
    return ContextId(**context_id)

def context_delete(db_engine : Engine, messagebroker : MessageBroker, request : ContextId) -> Empty:
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> bool:
        num_deleted = session.query(ContextModel).filter_by(context_uuid=context_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    context_id = json_context_id(context_uuid)
    if deleted:
        notify_event_context(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, context_id)
    return Empty()
