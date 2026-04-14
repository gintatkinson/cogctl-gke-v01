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

import datetime
import logging
from typing import Dict, List, Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from common.method_wrappers.ServiceExceptions import NotFoundException
from common.message_broker.MessageBroker import MessageBroker
from common.proto.context_pb2 import ContextId, Empty
from common.proto.qkd_app_pb2 import AppList, App, AppId
from common.tools.object_factory.QKDApp import json_app_id
from common.tools.object_factory.Context import json_context_id

from .models.QKDAppModel import AppModel
from .uuids.QKDApp import app_get_uuid
from context.service.database.uuids.Context import context_get_uuid
from .models.enums.QKDAppStatus import grpc_to_enum__qkd_app_status
from .models.enums.QKDAppTypes import grpc_to_enum__qkd_app_types

LOGGER = logging.getLogger(__name__)


def app_list_objs(db_engine : Engine, request : ContextId) -> AppList:
    """
    Fetches a list of all QKD applications from the database. Optionally filters by context UUID.

    :param db_engine: SQLAlchemy Engine for DB connection
    :param request: Context Id containing the UUID of the context to filter by
    :return: AppList containing all apps
    """
    context_uuid = context_get_uuid(request, allow_random=False)
    def callback(session : Session) -> List[Dict]:
        query = session.query(AppModel)
        query = query.filter_by(context_uuid=context_uuid)
        obj_list : List[AppModel] = query.all()
        return [obj.dump() for obj in obj_list]
    apps = run_transaction(sessionmaker(bind=db_engine), callback)
    return AppList(apps=apps)


def app_get(db_engine : Engine, request : AppId) -> App:
    """
    Fetches a specific app by its UUID.

    :param db_engine: SQLAlchemy Engine for DB connection
    :param request: AppId protobuf containing app ID and context ID
    :return: App protobuf object
    :raises NotFoundException: If the app is not found in the database
    """
    context_uuid,app_uuid = app_get_uuid(request, allow_random=False)

    def callback(session : Session) -> Optional[Dict]:
        query = session.query(AppModel)
        query = query.filter_by(app_uuid=app_uuid)
        obj : Optional[AppModel] = query.one_or_none()
        return None if obj is None else obj.dump()

    obj = run_transaction(sessionmaker(bind=db_engine), callback)

    if obj is None:
        raw_app_uuid = '{:s}/{:s}'.format(request.context_id.context_uuid.uuid, request.app_uuid.uuid)
        raise NotFoundException('App', raw_app_uuid, extra_details=[
            'context_uuid generated was: {:s}'.format(context_uuid),
            'app_uuid generated was: {:s}'.format(app_uuid),
        ])

    return App(**obj)


def app_set(db_engine : Engine, messagebroker : MessageBroker, request : App) -> AppId:
    """
    Creates or updates an app in the database. If the app already exists, updates the app.
    Otherwise, inserts a new entry.

    :param db_engine: SQLAlchemy Engine for DB connection
    :param messagebroker: MessageBroker instance for notifications
    :param request: App protobuf object containing app data
    :return: AppId protobuf object representing the newly created or updated app
    """
    context_uuid,app_uuid = app_get_uuid(request.app_id, allow_random=True)

    # Prepare app data for insertion/update
    app_data = {
        'context_uuid': context_uuid,
        'app_uuid': app_uuid,
        'app_status': grpc_to_enum__qkd_app_status(request.app_status),
        'app_type': grpc_to_enum__qkd_app_types(request.app_type),
        'server_app_id': request.server_app_id,
        'client_app_id': request.client_app_id,
        'backing_qkdl_uuid': [qkdl.qkdl_uuid.uuid for qkdl in request.backing_qkdl_id],
        'local_device_uuid': request.local_device_id.device_uuid.uuid,
        'remote_device_uuid': request.remote_device_id.device_uuid.uuid if request.remote_device_id.device_uuid.uuid else None,
        'created_at': datetime.datetime.utcnow(),
        'updated_at': datetime.datetime.utcnow(),
    }

    def callback(session: Session) -> bool:
        # Create the insert statement
        stmt = insert(AppModel).values(app_data)

        # Apply the conflict resolution
        stmt = stmt.on_conflict_do_update(
            index_elements=[AppModel.app_uuid],
            set_=dict(
                app_status=stmt.excluded.app_status,
                app_type=stmt.excluded.app_type,
                server_app_id=stmt.excluded.server_app_id,
                client_app_id=stmt.excluded.client_app_id,
                backing_qkdl_uuid=stmt.excluded.backing_qkdl_uuid,
                local_device_uuid=stmt.excluded.local_device_uuid,
                remote_device_uuid=stmt.excluded.remote_device_uuid,
                updated_at=stmt.excluded.updated_at
            )
        )
        session.execute(stmt)
        return True

    run_transaction(sessionmaker(bind=db_engine), callback)
    app_id = json_app_id(app_uuid, context_id=json_context_id(context_uuid))

    return AppId(**app_id)


def app_get_by_server(db_engine: Engine, server_app_id: str) -> App:
    """
    Fetches an app by its server_app_id.
    """
    def callback(session: Session) -> Optional[Dict]:
        obj = session.query(AppModel).filter_by(server_app_id=server_app_id).one_or_none()
        return obj.dump() if obj else None

    obj = run_transaction(sessionmaker(bind=db_engine), callback)

    if not obj:
        raise NotFoundException('App', server_app_id)

    return App(**obj)


def app_delete(db_engine : Engine, request : AppId) -> Empty:
    """
    Deletes an app by its UUID from the database.

    :param db_engine: SQLAlchemy Engine for DB connection
    :param app_id: The UUID of the app to be deleted
    """

    _,app_uuid = app_get_uuid(request, allow_random=False)

    def callback(session : Session) -> bool:
        query = session.query(AppModel)
        query = query.filter_by(app_uuid=app_uuid)
        num_deleted = query.delete()
        return num_deleted > 0

    run_transaction(sessionmaker(bind=db_engine), callback)
    return Empty()
