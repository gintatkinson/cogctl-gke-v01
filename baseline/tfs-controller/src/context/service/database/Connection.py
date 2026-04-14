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

import datetime, logging, re
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from typing import Dict, List, Optional, Tuple
from common.proto.context_pb2 import (
    Connection, ConnectionId, ConnectionIdList, ConnectionList, Empty, EventTypeEnum, ServiceId)
from common.message_broker.MessageBroker import MessageBroker
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Connection import json_connection_id
from .models.ConnectionModel import ConnectionEndPointModel, ConnectionModel, ConnectionSubServiceModel
from .uuids.Connection import connection_get_uuid
from .uuids.EndPoint import endpoint_get_uuid
from .uuids.Service import service_get_uuid
from .Events import notify_event_connection

LOGGER = logging.getLogger(__name__)

def connection_list_ids(db_engine : Engine, request : ServiceId) -> ConnectionIdList:
    _,service_uuid = service_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[ConnectionModel] = session.query(ConnectionModel).filter_by(service_uuid=service_uuid).all()
        return [obj.dump_id() for obj in obj_list]
    connection_ids = run_transaction(sessionmaker(bind=db_engine), callback)
    return ConnectionIdList(connection_ids=connection_ids)

def connection_list_objs(db_engine : Engine, request : ServiceId) -> ConnectionList:
    _,service_uuid = service_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        obj_list : List[ConnectionModel] = session.query(ConnectionModel)\
            .options(selectinload(ConnectionModel.connection_service))\
            .options(selectinload(ConnectionModel.connection_endpoints))\
            .options(selectinload(ConnectionModel.connection_subservices))\
            .filter_by(service_uuid=service_uuid).all()
        return [obj.dump() for obj in obj_list]
    connections = run_transaction(sessionmaker(bind=db_engine), callback)
    return ConnectionList(connections=connections)

def connection_get(db_engine : Engine, request : ConnectionId) -> Connection:
    connection_uuid = connection_get_uuid(request, allow_random=False)
    def callback(session : Session) -> Optional[Dict]:
        obj : Optional[ConnectionModel] = session.query(ConnectionModel)\
            .options(selectinload(ConnectionModel.connection_service))\
            .options(selectinload(ConnectionModel.connection_endpoints))\
            .options(selectinload(ConnectionModel.connection_subservices))\
            .filter_by(connection_uuid=connection_uuid).one_or_none()
        return None if obj is None else obj.dump()
    obj = run_transaction(sessionmaker(bind=db_engine), callback)
    if obj is None:
        raise NotFoundException('Connection', request.connection_uuid.uuid, extra_details=[
            'connection_uuid generated was: {:s}'.format(connection_uuid),
        ])
    return Connection(**obj)

def connection_set(db_engine : Engine, messagebroker : MessageBroker, request : Connection) -> ConnectionId:
    connection_uuid = connection_get_uuid(request.connection_id, allow_random=True)
    _,service_uuid = service_get_uuid(request.service_id, allow_random=False)
    settings = grpc_message_to_json_string(request.settings),

    now = datetime.datetime.now(datetime.timezone.utc)

    connection_data = [{
        'connection_uuid': connection_uuid,
        'service_uuid'   : service_uuid,
        'settings'       : settings,
        'created_at'     : now,
        'updated_at'     : now,
    }]

    connection_endpoints_data : List[Dict] = list()
    for position,endpoint_id in enumerate(request.path_hops_endpoint_ids):
        _, _, endpoint_uuid = endpoint_get_uuid(endpoint_id, allow_random=False)
        connection_endpoints_data.append({
            'connection_uuid': connection_uuid,
            'endpoint_uuid'  : endpoint_uuid,
            'position'       : position,
        })

    connection_subservices_data : List[Dict] = list()
    for service_id in request.sub_service_ids:
        _, service_uuid = service_get_uuid(service_id, allow_random=False)
        connection_subservices_data.append({
            'connection_uuid': connection_uuid,
            'subservice_uuid': service_uuid,
        })

    def callback(session : Session) -> bool:
        stmt = insert(ConnectionModel).values(connection_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[ConnectionModel.connection_uuid],
            set_=dict(
                settings   = stmt.excluded.settings,
                updated_at = stmt.excluded.updated_at,
            )
        )
        stmt = stmt.returning(ConnectionModel.created_at, ConnectionModel.updated_at)
        created_at,updated_at = session.execute(stmt).fetchone()
        updated = updated_at > created_at

        # TODO: manage update connection endpoints
        if len(connection_endpoints_data) > 0:
            stmt = insert(ConnectionEndPointModel).values(connection_endpoints_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[ConnectionEndPointModel.connection_uuid, ConnectionEndPointModel.endpoint_uuid]
            )
            try:
                session.execute(stmt)
            except IntegrityError as e:
                str_args = ''.join(e.args).replace('\n', ' ')
                pattern_fkv = \
                    r'\(psycopg2.errors.ForeignKeyViolation\) '\
                    r'insert on table \"([^\"]+)\" violates foreign key constraint '\
                    r'.+DETAIL\:  Key \([^\)]+\)\=\([\'\"]*([^\)\'\"]+)[\'\"]*\) is not present in table \"([^\"]+)\"'
                m_fkv = re.match(pattern_fkv, str_args)
                if m_fkv is not None:
                    insert_table, primary_key, origin_table = m_fkv.groups()
                    raise NotFoundException(origin_table, primary_key, extra_details=[
                        'while inserting in table "{:s}"'.format(insert_table)
                    ]) from e
                else:
                    raise

        # TODO: manage update connection subservices
        if len(connection_subservices_data) > 0:
            stmt = insert(ConnectionSubServiceModel).values(connection_subservices_data)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=[ConnectionSubServiceModel.connection_uuid, ConnectionSubServiceModel.subservice_uuid]
            )
            session.execute(stmt)

        return updated

    updated = run_transaction(sessionmaker(bind=db_engine), callback)
    connection_id = json_connection_id(connection_uuid)
    event_type = EventTypeEnum.EVENTTYPE_UPDATE if updated else EventTypeEnum.EVENTTYPE_CREATE
    notify_event_connection(messagebroker, event_type, connection_id)
    return ConnectionId(**connection_id)

def connection_delete(db_engine : Engine, messagebroker : MessageBroker, request : ConnectionId) -> Tuple[Dict, bool]:
    connection_uuid = connection_get_uuid(request, allow_random=False)
    def callback(session : Session) -> bool:
        num_deleted = session.query(ConnectionModel).filter_by(connection_uuid=connection_uuid).delete()
        return num_deleted > 0
    deleted = run_transaction(sessionmaker(bind=db_engine), callback)
    connection_id = json_connection_id(connection_uuid)
    if deleted:
        notify_event_connection(messagebroker, EventTypeEnum.EVENTTYPE_REMOVE, connection_id)
    return Empty()
