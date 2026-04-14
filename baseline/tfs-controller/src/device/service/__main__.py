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
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name, get_log_level, get_metrics_port,
    wait_for_environment_variables
)
from .DeviceService import DeviceService
from .driver_api.DriverFactory import DriverFactory
from .driver_api.DriverInstanceCache import DriverInstanceCache, preload_drivers
from .drivers import DRIVERS

terminate = threading.Event()
LOGGER : logging.Logger = None

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name
    LOGGER.warning('Terminate signal received')
    terminate.set()

def main():
    global LOGGER # pylint: disable=global-statement

    log_level = get_log_level()
    logging.basicConfig(level=log_level, format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s")
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
    logging.getLogger('apscheduler.scheduler').setLevel(logging.WARNING)
    logging.getLogger('monitoring-client').setLevel(logging.WARNING)
    LOGGER = logging.getLogger(__name__)

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

    # Initialize Driver framework
    driver_factory = DriverFactory(DRIVERS)
    driver_instance_cache = DriverInstanceCache(driver_factory)

    # Starting device service
    grpc_service = DeviceService(driver_instance_cache)
    grpc_service.start()

    # Initialize drivers with existing devices in context
    LOGGER.info('Pre-loading drivers...')
    preload_drivers(driver_instance_cache)

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    grpc_service.stop()
    driver_instance_cache.terminate()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
