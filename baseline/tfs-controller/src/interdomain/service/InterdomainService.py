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

from common.Constants import ServiceNameEnum
from common.Settings import get_service_port_grpc
from common.proto.interdomain_pb2_grpc import add_InterdomainServiceServicer_to_server
from common.tools.service.GenericGrpcService import GenericGrpcService
from .InterdomainServiceServicerImpl import InterdomainServiceServicerImpl
from .RemoteDomainClients import RemoteDomainClients

class InterdomainService(GenericGrpcService):
    def __init__(self, remote_domain_clients : RemoteDomainClients, cls_name: str = __name__) -> None:
        port = get_service_port_grpc(ServiceNameEnum.INTERDOMAIN)
        super().__init__(port, cls_name=cls_name)
        self.interdomain_servicer = InterdomainServiceServicerImpl(remote_domain_clients)

    def install_servicers(self):
        add_InterdomainServiceServicer_to_server(self.interdomain_servicer, self.server)
