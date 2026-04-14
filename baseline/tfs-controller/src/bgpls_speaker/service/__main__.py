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
from prometheus_client import start_http_server
from common.Settings import get_log_level, get_metrics_port
from .tools.DiscoveredDBManager import DiscoveredDBManager
from .BgplsService import BgplsService
from .tools.GrpcServer import GrpcServer

terminate = threading.Event()
LOGGER : logging.Logger = None
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def signal_handler(signal, frame): 
    LOGGER.warning('Terminate signal received') 
    LOGGER.warning(signal)
    terminate.set()

def main():
    global LOGGER 
    
    log_level = get_log_level()
    logging.basicConfig(level=log_level, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
    LOGGER = logging.getLogger(__name__)
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info('Starting...')

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)
    # One common database for all bgpls_speakers connection
    DB=DiscoveredDBManager()
    
    speaker_server = GrpcServer(DB)
    speaker_server.Connect()

    grpc_service = BgplsService(DB,speaker_server)
    grpc_service.start()

    # Wait for termination signal
    while not terminate.wait(timeout=0.1): pass
    LOGGER.info('Terminating...')
    speaker_server.terminateGrpcServer()
    grpc_service.stop()
    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
