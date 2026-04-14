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
from .AnalyticsFrontendService import AnalyticsFrontendService
from analytics.database.AnalyzerModel import Analyzer as Model
from common.tools.database.GenericDatabase import Database
from common.tools.kafka.Variables import KafkaTopic


terminate = threading.Event()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER    = None

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name
    LOGGER.warning('Terminate signal received')
    terminate.set()

def main():
    global LOGGER # pylint: disable=global-statement

    log_level = get_log_level()
    logging.basicConfig(level=log_level, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
    LOGGER = logging.getLogger(__name__)

    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info('Starting...')

    # To create DB 
    kpiDBobj = Database(Model)
    kpiDBobj.create_database()
    kpiDBobj.create_tables()

    KafkaTopic.create_all_topics()

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    grpc_service = AnalyticsFrontendService()
    grpc_service.start()

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
