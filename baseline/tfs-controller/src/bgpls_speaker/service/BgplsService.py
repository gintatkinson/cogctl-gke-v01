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

from bgpls_speaker.service.tools.DiscoveredDBManager import DiscoveredDBManager
from bgpls_speaker.service.tools.GrpcServer import GrpcServer
from common.Constants import ServiceNameEnum
from common.Settings import get_service_port_grpc
from common.proto.bgpls_pb2_grpc import add_BgplsServiceServicer_to_server
from common.tools.service.GenericGrpcService import GenericGrpcService
from .BgplsServiceServicerImpl import BgplsServiceServicerImpl

class BgplsService(GenericGrpcService):
    def __init__(self, discoveredDB : DiscoveredDBManager,
                 speakerServer : GrpcServer,cls_name: str = __name__) -> None:
        port = get_service_port_grpc(ServiceNameEnum.BGPLS) # El enum en common.constants
        super().__init__(port, cls_name=cls_name)
        self.bgpls_servicer = BgplsServiceServicerImpl(discoveredDB,speakerServer)

    def install_servicers(self):
        add_BgplsServiceServicer_to_server(self.bgpls_servicer, self.server)
