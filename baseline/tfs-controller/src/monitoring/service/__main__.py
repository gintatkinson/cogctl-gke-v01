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

import logging, signal, sys, threading, time
from prometheus_client import start_http_server
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name, get_log_level, get_metrics_port,
    wait_for_environment_variables)
from common.proto import monitoring_pb2
from .EventTools import EventsDeviceCollector
from .MonitoringService import MonitoringService
from .NameMapping import NameMapping

terminate = threading.Event()
LOGGER = None

def signal_handler(signal, frame): # pylint: disable=redefined-outer-name
    LOGGER.warning('Terminate signal received')
    terminate.set()

def start_monitoring(name_mapping : NameMapping):
    LOGGER.info('Start Monitoring...',)

    events_collector = EventsDeviceCollector(name_mapping)
    events_collector.start()

    # TODO: redesign this method to be more clear and clean

    # Iterate while terminate is not set
    while not terminate.is_set():
        list_new_kpi_ids = events_collector.listen_events()

        # Monitor Kpis
        if bool(list_new_kpi_ids):
            for kpi_id in list_new_kpi_ids:
                # Create Monitor Kpi Requests
                monitor_kpi_request = monitoring_pb2.MonitorKpiRequest()
                monitor_kpi_request.kpi_id.CopyFrom(kpi_id)
                monitor_kpi_request.monitoring_window_s = 86400
                monitor_kpi_request.sampling_rate_s = 10
                events_collector._monitoring_client.MonitorKpi(monitor_kpi_request)
        
        time.sleep(0.5) # let other tasks run; do not overload CPU
    else:
        # Terminate is set, looping terminates
        LOGGER.warning("Stopping execution...")

    events_collector.start()

def main():
    global LOGGER # pylint: disable=global-statement

    log_level = get_log_level()
    logging.basicConfig(level=log_level)
    LOGGER = logging.getLogger(__name__)

    wait_for_environment_variables([
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.DEVICE,  ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    ])

    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info('Starting...')

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    name_mapping = NameMapping()

    # Starting monitoring service
    grpc_service = MonitoringService(name_mapping)
    grpc_service.start()

    start_monitoring(name_mapping)

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=1.0): pass

    LOGGER.info('Terminating...')
    grpc_service.stop()

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
