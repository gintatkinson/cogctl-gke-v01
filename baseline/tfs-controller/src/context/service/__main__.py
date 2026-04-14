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
from common.message_broker.Factory import get_messagebroker_backend
from common.message_broker.MessageBroker import MessageBroker
from .ContextService import ContextService
from .database.Engine import Engine
from .database.models._Base import rebuild_database

LOG_LEVEL = get_log_level()
logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
LOGGER = logging.getLogger(__name__)

#LOGGER.addHandler(logging.StreamHandler(stream=sys.stderr))
#LOGGER.setLevel(logging.WARNING)

terminate = threading.Event()

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name,unused-argument
    LOGGER.warning('Terminate signal received')
    terminate.set()

def main():
    LOGGER.info('Starting...')
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    # Get Database Engine instance and initialize database, if needed
    LOGGER.info('Getting SQLAlchemy DB Engine...')
    db_engine = Engine.get_engine()
    if db_engine is None:
        LOGGER.error('Unable to get SQLAlchemy DB Engine...')
        return -1

    try:
        Engine.create_database(db_engine)
    except: # pylint: disable=bare-except # pragma: no cover
        LOGGER.exception('Failed to check/create the database: {:s}'.format(str(db_engine.url)))

    rebuild_database(db_engine)

    # Get message broker instance
    messagebroker = MessageBroker(get_messagebroker_backend())

    # Starting context service
    grpc_service = ContextService(db_engine, messagebroker)
    grpc_service.start()

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
