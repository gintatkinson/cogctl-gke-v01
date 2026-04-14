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
from prometheus_client import start_http_server
from common.Settings import get_log_level, get_metrics_port
from qkd_app.service.QKDAppService import AppService
from qkd_app.service.database.Engine import Engine
from qkd_app.service.database.models._Base import rebuild_database

# Set up logging
LOG_LEVEL = get_log_level()
logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
LOGGER = logging.getLogger(__name__)

#LOGGER.addHandler(logging.StreamHandler(stream=sys.stderr))
#LOGGER.setLevel(logging.WARNING)

# Event for terminating the service gracefully
terminate = threading.Event()

def signal_handler(signum, frame):
    """
    Handle termination signals like SIGINT and SIGTERM to ensure graceful shutdown.
    """
    LOGGER.warning('Termination signal received')
    terminate.set()

def main():
    LOGGER.info('Starting...')
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start Prometheus metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)
    LOGGER.info(f'Metrics server started on port {metrics_port}')

    # Initialize the SQLAlchemy database engine
    LOGGER.info('Getting SQLAlchemy DB Engine...')
    db_engine = Engine.get_engine()
    if db_engine is None:
        LOGGER.error('Unable to get SQLAlchemy DB Engine. Exiting...')
        return -1

    # Try creating the database or log any issues
    try:
        Engine.create_database(db_engine)
    except Exception as e:  # More specific exception handling
        LOGGER.exception(f'Failed to check/create the database: {db_engine.url}. Error: {str(e)}')
        return -1

    # Rebuild the database schema if necessary
    rebuild_database(db_engine)

    # Initialize the message broker (if needed)
    messagebroker = None  # Disabled until further notice, can be re-enabled when necessary
    # messagebroker = MessageBroker(get_messagebroker_backend())

    # Start the gRPC App Service
    grpc_service = AppService(db_engine, messagebroker)
    grpc_service.start()

    LOGGER.info('Services started. Waiting for termination signal...')

    # Wait for Ctrl+C or termination signal
    # Keep the process running until a termination signal is received
    while not terminate.wait(timeout=1.0):
        pass

    # Shutdown services gracefully on termination
    LOGGER.info('Terminating services...')
    grpc_service.stop()

    LOGGER.info('Shutdown complete. Exiting...')
    return 0

if __name__ == '__main__':
    sys.exit(main())
