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
from common.Constants import ServiceNameEnum
from common.Settings import get_service_host, get_service_port_grpc
from common.proto.qkd_app_pb2 import App, AppId, AppList
from common.proto.qkd_app_pb2_grpc import AppServiceStub
from common.tools.client.RetryDecorator import retry, delay_exponential
from common.tools.grpc.Tools import grpc_message_to_json_string

LOGGER = logging.getLogger(__name__)

# Define retry mechanism
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)

class QKDAppClient:
    def __init__(self, host=None, port=None):
        self.host = host or get_service_host(ServiceNameEnum.QKD_APP)
        self.port = port or get_service_port_grpc(ServiceNameEnum.QKD_APP)
        self.endpoint = f'{self.host}:{self.port}'
        LOGGER.debug(f'Initializing gRPC client to {self.endpoint}...')
        self.channel = None
        self.stub = None
        self.connect()

    def connect(self):
        try:
            self.channel = grpc.insecure_channel(self.endpoint)
            self.stub = AppServiceStub(self.channel)
            LOGGER.debug(f'gRPC channel to {self.endpoint} established successfully')
        except Exception as e:
            LOGGER.error(f"Failed to establish gRPC connection: {e}")
            self.stub = None

    def close(self):
        if self.channel:
            self.channel.close()
            LOGGER.debug(f'gRPC channel to {self.endpoint} closed')
        self.channel = None
        self.stub = None

    def check_connection(self):
        if self.stub is None:
            LOGGER.error("gRPC connection is not established. Retrying...")
            self.connect()
            if self.stub is None:
                raise ConnectionError("gRPC connection could not be established.")

    @retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION)
    def RegisterApp(self, app_request: App) -> None:
        """Register a new QKD app."""
        self.check_connection()
        LOGGER.debug(f'RegisterApp request: {grpc_message_to_json_string(app_request)}')
        self.stub.RegisterApp(app_request)
        LOGGER.debug('App registered successfully')

    @retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION)
    def UpdateApp(self, app_request: App) -> None:
        """Update an existing QKD app."""
        self.check_connection()
        LOGGER.debug(f'UpdateApp request: {grpc_message_to_json_string(app_request)}')
        self.stub.UpdateApp(app_request)
        LOGGER.debug('App updated successfully')

    @retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION)
    def ListApps(self, context_id) -> AppList:
        """List all apps for a given context."""
        self.check_connection()
        LOGGER.debug(f'ListApps request for context_id: {grpc_message_to_json_string(context_id)}')
        response = self.stub.ListApps(context_id)
        LOGGER.debug(f'ListApps result: {grpc_message_to_json_string(response)}')
        return response

    @retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION)
    def GetApp(self, app_id: AppId) -> App:
        """Fetch details of a specific app by its ID."""
        self.check_connection()
        LOGGER.debug(f'GetApp request for app_id: {grpc_message_to_json_string(app_id)}')
        response = self.stub.GetApp(app_id)
        LOGGER.debug(f'GetApp result: {grpc_message_to_json_string(response)}')
        return response

    @retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION)
    def DeleteApp(self, app_id: AppId) -> None:
        """Delete an app by its ID."""
        self.check_connection()  # Ensures connection is established
        LOGGER.debug(f'DeleteApp request for app_id: {grpc_message_to_json_string(app_id)}')
        self.stub.DeleteApp(app_id)  # Calls the gRPC service
        LOGGER.debug('App deleted successfully')
