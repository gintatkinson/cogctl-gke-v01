# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grpc
import logging
import sqlalchemy
import uuid
from common.message_broker.MessageBroker import MessageBroker
from common.proto.context_pb2 import Empty, ContextId
from common.proto.qkd_app_pb2 import App, AppId, AppList, QKDAppTypesEnum, QoS
from common.method_wrappers.ServiceExceptions import InvalidArgumentException, NotFoundException
from common.proto.qkd_app_pb2_grpc import AppServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from .database.QKDApp import app_set, app_list_objs, app_get, app_get_by_server, app_delete

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('QkdApp', 'RPC')

class AppServiceServicerImpl(AppServiceServicer):
    def __init__(self, db_engine: sqlalchemy.engine.Engine, messagebroker: MessageBroker):
        LOGGER.debug('Initializing AppServiceServicer...')
        self.db_engine = db_engine
        self.messagebroker = messagebroker
        LOGGER.debug('AppServiceServicer initialized')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RegisterApp(self, request: App, context: grpc.ServicerContext) -> Empty:
        """
        Registers an app in the system, handling both internal and external applications
        with ETSI GS QKD 015 compliance.
        """
        LOGGER.debug(f"Received RegisterApp request: {grpc_message_to_json_string(request)}")

        try:
            # Validate QoS parameters as per ETSI 015 requirements
            self._validate_qos(request.qos)

            # Check if an app with the same server_app_id and local_device_id already exists
            existing_app = self._check_existing_app(request.server_app_id, request.local_device_id.device_uuid.uuid)

            if existing_app:
                if request.app_type == QKDAppTypesEnum.QKDAPPTYPES_CLIENT:
                    LOGGER.debug(f"Handling external app registration for server_app_id: {request.server_app_id}")
                    # Handle second-party registration for external apps
                    if not existing_app.remote_device_id.device_uuid.uuid:
                        existing_app.remote_device_id.device_uuid.uuid = request.local_device_id.device_uuid.uuid
                        app_set(self.db_engine, self.messagebroker, existing_app)
                        LOGGER.debug(f"Updated external app with server_app_id: {request.server_app_id}, remote_device_id: {request.local_device_id.device_uuid.uuid}")
                    else:
                        context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                        context.set_details(f"App with server_app_id {request.server_app_id} already has both parties registered.")
                        return Empty()
                else:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    context.set_details(f"App with server_app_id {request.server_app_id} already exists.")
                    return Empty()
            else:
                # Assign application IDs as required
                self._validate_and_assign_app_ids(request)

                # Register the app
                if request.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL:
                    LOGGER.debug(f"Registering internal app with app_uuid: {request.app_id.app_uuid.uuid}")
                    app_set(self.db_engine, self.messagebroker, request)
                else:
                    self._register_external_app(request)

            LOGGER.debug(f"RegisterApp completed successfully for app: {request.server_app_id}")
            return Empty()

        except InvalidArgumentException as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            raise e
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("An internal error occurred during app registration.")
            raise e

    def _validate_qos(self, qos: QoS) -> None:
        """
        Validates the QoS parameters for the application, ensuring ETSI 015 compliance.
        """
        if qos.max_bandwidth and qos.min_bandwidth and qos.max_bandwidth < qos.min_bandwidth:
            raise InvalidArgumentException("QoS max_bandwidth cannot be less than min_bandwidth.")

        if qos.ttl and qos.ttl <= 0:
            raise InvalidArgumentException("QoS TTL must be a positive value.")

        LOGGER.debug(f"QoS validated: {qos}")

    def _check_existing_app(self, server_app_id: str, local_device_id: str):
        try:
            return app_get_by_server(self.db_engine, server_app_id)
        except NotFoundException:
            return None

    def _validate_and_assign_app_ids(self, request: App) -> None:
        """
        Validates and assigns app IDs (app_uuid, server_app_id, client_app_id) if not provided.
        """
        if not request.app_id.app_uuid.uuid:
            request.app_id.app_uuid.uuid = str(uuid.uuid4())
            LOGGER.debug(f"Assigned new app_uuid: {request.app_id.app_uuid.uuid}")

        if not request.server_app_id:
            request.server_app_id = str(uuid.uuid4())
            LOGGER.debug(f"Assigned new server_app_id: {request.server_app_id}")

        del request.client_app_id[:]  # Clear the repeated field for clients

    def _register_external_app(self, request: App) -> None:
        try:
            existing_app = app_get_by_server(self.db_engine, request.server_app_id)

            if not existing_app.remote_device_id.device_uuid.uuid:
                existing_app.remote_device_id.device_uuid.uuid = request.local_device_id.device_uuid.uuid
                app_set(self.db_engine, self.messagebroker, existing_app)
            else:
                LOGGER.debug(f"App with server_app_id: {request.server_app_id} already has both parties registered.")
        except NotFoundException:
            app_set(self.db_engine, self.messagebroker, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListApps(self, request : ContextId, context : grpc.ServicerContext) -> AppList:
        """
        Lists all apps in the system, including their statistics and QoS attributes.
        """
        return app_list_objs(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetApp(self, request : AppId, context : grpc.ServicerContext) -> App:
        """
        Fetches details of a specific app based on its AppId, including QoS and performance stats.
        """
        return app_get(self.db_engine, request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteApp(self, request : AppId, context : grpc.ServicerContext) -> Empty:
        """
        Deletes an app from the system by its AppId, following ETSI compliance.
        """
        return app_delete(self.db_engine, request)
