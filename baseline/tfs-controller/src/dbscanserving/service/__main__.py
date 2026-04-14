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

import logging
import signal
import sys
import threading

from common.Settings import get_log_level, get_metrics_port
from prometheus_client import start_http_server

from dbscanserving.service.DbscanService import DbscanService

terminate = threading.Event()
LOGGER = None


def signal_handler(signal, frame):  # pylint: disable=redefined-outer-name
    LOGGER.warning("Terminate signal received")
    terminate.set()


def main():
    global LOGGER  # pylint: disable=global-statement

    log_level = get_log_level()
    logging.basicConfig(level=log_level)
    LOGGER = logging.getLogger(__name__)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info("Starting...")

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    # Starting CentralizedCybersecurity service
    grpc_service = DbscanService()
    grpc_service.start()

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1):
        pass

    LOGGER.info("Terminating...")
    grpc_service.stop()

    LOGGER.info("Bye")
    return 0


if __name__ == "__main__":
    sys.exit(main())
