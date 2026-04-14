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

import logging, signal, sys, threading
from common.Constants import ServiceNameEnum
from common.Settings import get_log_level, get_service_port_grpc
from common.proto.dlt_gateway_pb2_grpc import add_DltGatewayServiceServicer_to_server
from common.tests.MockServicerImpl_DltGateway import MockServicerImpl_DltGateway
from common.tools.service.GenericGrpcService import GenericGrpcService

terminate = threading.Event()

logging.basicConfig(level=get_log_level())
LOGGER = logging.getLogger(__name__)

class MockDltGatewayService(GenericGrpcService):
    def __init__(self, cls_name: str = 'MockDltGatewayService') -> None:
        port = get_service_port_grpc(ServiceNameEnum.DLT_GATEWAY)
        super().__init__(port, cls_name=cls_name)
        self.dltgateway_servicer = MockServicerImpl_DltGateway()

    # pylint: disable=attribute-defined-outside-init
    def install_servicers(self):
        add_DltGatewayServiceServicer_to_server(self.dltgateway_servicer, self.server)

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name
    LOGGER.warning('Terminate signal received')
    terminate.set()

def main():
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info('Starting...')

    # Starting Mock DLT gateway service
    grpc_service = MockDltGatewayService()
    grpc_service.start()

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
