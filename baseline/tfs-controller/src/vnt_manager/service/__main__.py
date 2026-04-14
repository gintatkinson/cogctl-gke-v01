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
from common.tools.kafka.Variables import KafkaTopic
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name, get_log_level, get_metrics_port,
    wait_for_environment_variables
)
from .VNTManagerService import VNTManagerService

LOG_LEVEL = get_log_level()
logging.basicConfig(level=LOG_LEVEL, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
LOGGER = logging.getLogger(__name__)

terminate = threading.Event()

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name,unused-argument
    LOGGER.warning("Terminate signal received")
    terminate.set()

def main():
    LOGGER.info("Starting...")

    wait_for_environment_variables([
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    ])

    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    KafkaTopic.create_all_topics()

    # Starting VNTManager service
    grpc_service = VNTManagerService()
    grpc_service.start()

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1): pass

    LOGGER.info("Terminating...")
    grpc_service.stop()

    LOGGER.info("Bye")
    return 0

if __name__ == "__main__":
    sys.exit(main())
