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

import logging, sqlalchemy
from common.Constants import ServiceNameEnum
from common.Settings import get_service_port_grpc
from common.message_broker.MessageBroker import MessageBroker
from common.proto.context_pb2 import DESCRIPTOR as CONTEXT_DESCRIPTOR
from common.proto.context_pb2_grpc import add_ContextServiceServicer_to_server
from common.proto.context_policy_pb2 import DESCRIPTOR as CONTEXT_POLICY_DESCRIPTOR
from common.proto.context_policy_pb2_grpc import add_ContextPolicyServiceServicer_to_server
from common.tools.service.GenericGrpcService import GenericGrpcService
from .ContextServiceServicerImpl import ContextServiceServicerImpl

# Custom gRPC settings
GRPC_MAX_WORKERS = 200 # multiple clients might keep connections alive for Get*Events() RPC methods
LOGGER = logging.getLogger(__name__)

class ContextService(GenericGrpcService):
    def __init__(
        self, db_engine : sqlalchemy.engine.Engine, messagebroker : MessageBroker, cls_name: str = __name__
    ) -> None:
        port = get_service_port_grpc(ServiceNameEnum.CONTEXT)
        super().__init__(port, max_workers=GRPC_MAX_WORKERS, cls_name=cls_name)
        self.context_servicer = ContextServiceServicerImpl(db_engine, messagebroker)

    def install_servicers(self):
        add_ContextServiceServicer_to_server(self.context_servicer, self.server)
        add_ContextPolicyServiceServicer_to_server(self.context_servicer, self.server)

        self.add_reflection_service_name(CONTEXT_DESCRIPTOR, 'ContextService')
        self.add_reflection_service_name(CONTEXT_POLICY_DESCRIPTOR, 'ContextPolicyService')
