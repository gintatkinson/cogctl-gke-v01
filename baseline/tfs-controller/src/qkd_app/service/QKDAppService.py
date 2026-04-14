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

import logging
import sqlalchemy
from common.Constants import ServiceNameEnum
from common.Settings import get_service_port_grpc
from common.message_broker.MessageBroker import MessageBroker
from common.proto.qkd_app_pb2_grpc import add_AppServiceServicer_to_server
from common.tools.service.GenericGrpcService import GenericGrpcService
from qkd_app.service.QKDAppServiceServicerImpl import AppServiceServicerImpl

# Configure maximum number of workers for gRPC
GRPC_MAX_WORKERS = 200  # Adjusted for high concurrency
LOGGER = logging.getLogger(__name__)

class AppService(GenericGrpcService):
    """
    gRPC Service for handling QKD App-related operations. 
    This class initializes the gRPC server and installs the servicers.
    """
    def __init__(
        self, db_engine: sqlalchemy.engine.Engine, messagebroker: MessageBroker, cls_name: str = __name__
    ) -> None:
        """
        Initializes the AppService with the provided database engine and message broker.
        Sets up the gRPC server to handle app-related requests.

        Args:
            db_engine (sqlalchemy.engine.Engine): Database engine for handling app data.
            messagebroker (MessageBroker): Message broker for inter-service communication.
            cls_name (str): Class name for logging purposes (default is __name__).
        """
        # Get the port for the gRPC AppService
        port = get_service_port_grpc(ServiceNameEnum.QKD_APP)
        # Initialize the base class with port and max worker configuration
        super().__init__(port, max_workers=GRPC_MAX_WORKERS, cls_name=cls_name)
        # Initialize the AppServiceServicer with the database and message broker
        self.app_servicer = AppServiceServicerImpl(db_engine, messagebroker)

    def install_servicers(self):
        """
        Installs the AppService servicers to the gRPC server.
        This allows the server to handle requests for QKD app operations.
        """
        add_AppServiceServicer_to_server(self.app_servicer, self.server)
        LOGGER.debug("AppService servicer installed")
