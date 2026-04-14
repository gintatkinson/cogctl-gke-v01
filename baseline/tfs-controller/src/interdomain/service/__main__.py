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
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name, get_log_level, get_metrics_port,
    wait_for_environment_variables)
from interdomain.Config import is_dlt_enabled, is_topology_abstractor_enabled
from .topology_abstractor.TopologyAbstractor import TopologyAbstractor
from .topology_abstractor.DltRecorder import DLTRecorder
from .InterdomainService import InterdomainService
from .RemoteDomainClients import RemoteDomainClients

terminate = threading.Event()
LOGGER : logging.Logger = None

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name
    LOGGER.warning('Terminate signal received')
    terminate.set()

def main():
    global LOGGER # pylint: disable=global-statement

    log_level = get_log_level()
    logging.basicConfig(level=log_level, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
    LOGGER = logging.getLogger(__name__)

    wait_for_environment_variables([
        get_env_var_name(ServiceNameEnum.CONTEXT,  ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.CONTEXT,  ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        get_env_var_name(ServiceNameEnum.PATHCOMP, ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.PATHCOMP, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        get_env_var_name(ServiceNameEnum.SLICE,    ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.SLICE,    ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    ])

    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info('Starting...')

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    # Define remote domain clients
    remote_domain_clients = RemoteDomainClients()
    remote_domain_clients.start()

    # Starting Interdomain service
    grpc_service = InterdomainService(remote_domain_clients)
    grpc_service.start()

    # Subscribe to Context Events
    topology_abstractor_enabled = is_topology_abstractor_enabled()
    if topology_abstractor_enabled:
        topology_abstractor = TopologyAbstractor()
        topology_abstractor.start()

    # Subscribe to Context Events
    dlt_enabled = is_dlt_enabled()
    if dlt_enabled:
        LOGGER.info('Starting DLT functionality...')
        dlt_recorder = DLTRecorder()
        dlt_recorder.start()

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    if topology_abstractor_enabled:
        topology_abstractor.stop()
    if dlt_enabled:
         dlt_recorder.stop()
    grpc_service.stop()
    remote_domain_clients.stop()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
