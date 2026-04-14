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
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name,
    get_log_level, get_metrics_port, wait_for_environment_variables
)
from .subscriptions.ControllerDiscoverer import ControllerDiscoverer
from .subscriptions.Subscriptions import Subscriptions
from .subscriptions.dispatchers.Dispatchers import Dispatchers
from .subscriptions.dispatchers.recommendation.Dispatcher import RecommendationDispatcher
from .E2EOrchestratorService import E2EOrchestratorService

TERMINATE = threading.Event()

LOG_LEVEL = get_log_level()
logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
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

    # Starting service
    grpc_service = E2EOrchestratorService()
    grpc_service.start()


    dispatchers   = Dispatchers(TERMINATE)
    dispatchers.add_dispatcher(RecommendationDispatcher)
    subscriptions = Subscriptions(dispatchers, TERMINATE)
    discoverer    = ControllerDiscoverer(subscriptions, TERMINATE)
    discoverer.start()

    LOGGER.info('Running...')
    # Wait for Ctrl+C or termination signal
    while not TERMINATE.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    discoverer.stop()
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0


if __name__ == '__main__':
    sys.exit(main())
