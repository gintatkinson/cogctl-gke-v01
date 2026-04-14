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
from common.tools.rest_conf.client.RestConfClient import RestConfClient
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name,
    get_log_level, get_metrics_port, wait_for_environment_variables
)
from simap_connector.Config import (
    SIMAP_SERVER_SCHEME, SIMAP_SERVER_ADDRESS, SIMAP_SERVER_PORT,
    SIMAP_SERVER_USERNAME, SIMAP_SERVER_PASSWORD,
)
from .database.Engine import Engine
from .database.models._Base import rebuild_database
from .simap_updater.SimapClient import SimapClient
from .simap_updater.SimapUpdater import SimapUpdater
from .telemetry.TelemetryPool import TelemetryPool
from .SimapConnectorService import SimapConnectorService


TERMINATE = threading.Event()

LOG_LEVEL = get_log_level()
logging.basicConfig(level=LOG_LEVEL, format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s')
logging.getLogger('RestConfClient').setLevel(logging.WARN)

LOGGER = logging.getLogger(__name__)


def signal_handler(signal, frame): # pylint: disable=redefined-outer-name
    LOGGER.warning('Terminate signal received')
    TERMINATE.set()


def main():
    wait_for_environment_variables([
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    ])

    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info('Starting...')

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

    restconf_client = RestConfClient(
        scheme=SIMAP_SERVER_SCHEME, address=SIMAP_SERVER_ADDRESS,
        port=SIMAP_SERVER_PORT, username=SIMAP_SERVER_USERNAME,
        password=SIMAP_SERVER_PASSWORD,
    )

    simap_client = SimapClient(restconf_client)
    telemetry_pool = TelemetryPool(simap_client, terminate=TERMINATE)

    grpc_service = SimapConnectorService(db_engine, restconf_client, telemetry_pool)
    grpc_service.start()

    simap_updater = SimapUpdater(simap_client, telemetry_pool, TERMINATE)
    simap_updater.start()

    LOGGER.info('Running...')
    # Wait for Ctrl+C or termination signal
    while not TERMINATE.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    simap_updater.stop()
    telemetry_pool.stop_all()
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0


if __name__ == '__main__':
    sys.exit(main())
