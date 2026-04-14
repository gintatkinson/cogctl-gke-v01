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
from typing import Optional
from prometheus_client.exposition import start_http_server
from common.Settings import get_log_level, get_metrics_port
from common.tools.kafka.Variables import KafkaTopic
from .TelemetryBackendService import TelemetryBackendService

from .collector_api.DriverFactory import DriverFactory
from .collector_api.DriverInstanceCache import DriverInstanceCache, preload_drivers
from .collectors import COLLECTORS

terminate = threading.Event()
LOGGER : Optional[logging.Logger] = None

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name
    if LOGGER:
       LOGGER.warning('Terminate signal received')
    terminate.set()

def main():
    global LOGGER # pylint: disable=global-statement

    log_level = get_log_level()
    logging.basicConfig(level=log_level, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
    LOGGER = logging.getLogger(__name__)

    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    KafkaTopic.create_all_topics()

    LOGGER.info('Starting...')

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    # Initialize Driver framework
    driver_factory = DriverFactory(COLLECTORS)
    driver_instance_cache = DriverInstanceCache(driver_factory)

    grpc_service = TelemetryBackendService(driver_instance_cache)
    grpc_service.start()

    # Preload drivers
    LOGGER.info('Preloading drivers...')
    preload_drivers(driver_instance_cache)

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
