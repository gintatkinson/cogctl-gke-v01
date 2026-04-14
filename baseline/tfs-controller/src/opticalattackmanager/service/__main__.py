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

import asyncio
import logging
import math
import pickle
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Event, Manager, Process
from typing import Dict, List

import redis
from prometheus_client import Counter, Gauge, Histogram, start_http_server

from common.Constants import ServiceNameEnum
from common.proto.context_pb2 import (
    ContextIdList,
    Empty,
    EventTypeEnum,
    Service,
    ServiceIdList,
    ServiceTypeEnum,
)
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2 import KpiDescriptor
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST,
    ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name,
    get_log_level,
    get_metrics_port,
    get_service_host,
    get_service_port_grpc,
    get_setting,
    wait_for_environment_variables,
)
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from monitoring.client.MonitoringClient import MonitoringClient
from opticalattackmanager.Config import MONITORING_INTERVAL
from opticalattackmanager.utils.monitor import delegate_services

terminate = Event()
LOGGER = None

# SERVICE_LIST_MODE:
# 1 => use Redis
LIST_REDIS_MODE = 1
# 2 => use shared list
LIST_SHARED_MODE = 2
SERVICE_LIST_MODE = int(
    get_setting("OPTICALATTACKMANAGER_SERVICE_LIST_MODE", default=1)
)
SERVICE_LIST_KEY = get_setting(
    "OPTICALATTACKMANAGER_SERVICE_LIST_KEY", default="opt-sec-active-services"
)
MIN_NUMBER_WORKERS = int(
    get_setting("OPTICALATTACKMANAGERSERVICE_LOOP_MIN_WORKERS", default=2)
)
MAX_NUMBER_WORKERS = int(
    get_setting("OPTICALATTACKMANAGERSERVICE_LOOP_MAX_WORKERS", default=10)
)

# Create a metric to track time spent and requests made.
# TODO: adjust histogram buckets to more realistic values
LOOP_TIME = Histogram(
    "tfs_opticalattackmanager_loop_seconds",
    "Time taken by each security loop",
    buckets=(
        1.0, 2.5, 5.0, 7.5, 10.0, 12.5,
        15.0, 17.5, 20.0, 22.5, 25.0, 27.5,
        30.0, 32.5, 35.0, 37.5, 40.0,
        42.5, 45.0, 47.5,
        50.0, 52.5, 55.0, 57.5,
        60.0, 70.0, 80.0, 90.0, 100.0,
        float("inf"),
    ),
)

CURRENT_SERVICES = Gauge(
    "tfs_opticalattackmanager_active_services",
    "Active optical services currently in the network",
)

NUMBER_WORKERS = Gauge(
    "tfs_opticalattackmanager_number_workers",
    "Number of workers being used by the loop",
)

DESIRED_MONITORING_INTERVAL = Gauge(
    "tfs_opticalattackmanager_desired_monitoring_interval",
    "Desired loop monitoring interval",
)

DROP_COUNTER = Counter(
    "tfs_opticalattackmanager_dropped_assessments",
    "Dropped assessments due to detector timeout",
)

global service_list
global cache


def append_service(
    info: Dict[str, str], service_list: List = None, cache: redis.Redis = None
) -> None:
    if SERVICE_LIST_MODE == LIST_REDIS_MODE:
        cache.lpush(SERVICE_LIST_KEY, pickle.dumps(info))
    elif SERVICE_LIST_MODE == LIST_SHARED_MODE:
        service_list.append(info)


def delete_service(
    info: Dict[str, str], service_list: List = None, cache: redis.Redis = None
) -> None:
    # here we need to test if the service exists in the list because it has been
    # already deleted and there is not way of knowing if it is optical or not
    if SERVICE_LIST_MODE == LIST_REDIS_MODE:
        service_list = cache.lrange(SERVICE_LIST_KEY, 0, -1)
        for encoded in service_list:
            service = pickle.loads(encoded)
            if (
                service["service"] == info["service"]
                and service["context"] == info["context"]
            ):
                cache.lrem(SERVICE_LIST_KEY, 1, encoded)
                break
    elif SERVICE_LIST_MODE == LIST_SHARED_MODE:
        # find service and remove it from the list of currently monitored
        for service in service_list:
            if (
                service["service"] == info["service"]
                and service["context"] == info["context"]
            ):
                service_list.remove(service)
                break


def signal_handler(signal, frame):  # pylint: disable=redefined-outer-name
    LOGGER.warning("Terminate signal received")
    terminate.set()


def create_kpi(client: MonitoringClient, service_id):
    # create kpi
    kpi_description: KpiDescriptor = KpiDescriptor()
    kpi_description.kpi_description = "Security status of service {}".format(service_id)
    kpi_description.service_id.service_uuid.uuid = service_id
    kpi_description.kpi_sample_type = KpiSampleType.KPISAMPLETYPE_UNKNOWN
    new_kpi = client.SetKpi(kpi_description)
    LOGGER.debug("Created KPI {}: ".format(grpc_message_to_json_string(new_kpi)))
    return new_kpi


def get_context_updates(terminate, service_list, cache):
    # to make sure we are thread safe...
    LOGGER.info("Connecting with context and monitoring components...")
    context_client: ContextClient = ContextClient()
    monitoring_client: MonitoringClient = MonitoringClient()

    events_collector: EventsCollector = EventsCollector(
        context_client,
        log_events_received=True,
        activate_connection_collector=False,
        activate_context_collector=False,
        activate_device_collector=False,
        activate_link_collector=False,
        activate_slice_collector=False,
        activate_topology_collector=False,
        activate_service_collector=True,
    )
    events_collector.start()

    LOGGER.info("Connected with components successfully... Waiting for events...")

    time.sleep(20)

    while not terminate.wait(timeout=5):
        event = events_collector.get_event(block=True, timeout=1)
        if event is None:
            LOGGER.debug("No event received")
            continue  # no event received
        LOGGER.debug("Event received: {}".format(grpc_message_to_json_string(event)))
        if event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE:
            service: Service = context_client.GetService(event.service_id)
            # only add if service is of type TAPI
            if (
                service.service_type
                == ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE
            ):
                LOGGER.info(
                    "Service created: {}".format(
                        grpc_message_to_json_string(event.service_id)
                    )
                )
                kpi_id = create_kpi(
                    monitoring_client, event.service_id.service_uuid.uuid
                )

                append_service(
                    {
                        "context": event.service_id.context_id.context_uuid.uuid,
                        "service": event.service_id.service_uuid.uuid,
                        "kpi": kpi_id.kpi_id.uuid,
                    },
                    service_list=service_list,
                    cache=cache,
                )

        elif event.event.event_type == EventTypeEnum.EVENTTYPE_REMOVE:
            # cannot fetch service details because it does not exist anymore
            LOGGER.info(
                "Service removed: {}".format(
                    grpc_message_to_json_string(event.service_id)
                )
            )
            delete_service(
                {
                    "service": event.service_id.service_uuid.uuid,
                    "context": event.service_id.context_id.context_uuid.uuid,
                },
                service_list=service_list,
                cache=cache,
            )

    events_collector.stop()


def get_number_workers(
    cur_value: int, cur_duration: float, desired_duration: float
) -> int:
    factor = cur_duration / desired_duration
    desired_number = cur_value * factor
    new_value = min(
        MAX_NUMBER_WORKERS, max(MIN_NUMBER_WORKERS, math.ceil(desired_number))
    )
    return new_value


async def monitor_services(terminate, service_list=None, cache=None):

    host = get_service_host(ServiceNameEnum.OPTICALATTACKDETECTOR)
    port = get_service_port_grpc(ServiceNameEnum.OPTICALATTACKDETECTOR)

    cur_number_workers = MIN_NUMBER_WORKERS
    desired_monitoring_interval = 30  # defaults to 30 seconds
    DESIRED_MONITORING_INTERVAL.set(desired_monitoring_interval)

    event_loop = asyncio.get_running_loop()

    LOGGER.info("Starting execution of the async loop")

    while not terminate.is_set():
        # we account the entire set of procedures as the loop time
        start_time = time.time()

        # obtain desired monitoring interval
        temp = cache.get("MONITORING_INTERVAL")
        if temp is not None:
            new_desired_monitoring_interval = int(temp)
        else:
            # if not set in Redis, fallback to the environment variable
            new_desired_monitoring_interval = int(
                get_setting("MONITORING_INTERVAL", default=MONITORING_INTERVAL)
            )
            cache.set("MONITORING_INTERVAL", new_desired_monitoring_interval)

        # only reports when changes happen
        if desired_monitoring_interval != new_desired_monitoring_interval:
            LOGGER.info(
                "Changing monitoring interval from {} [sec.] to {} [sec.]".format(
                    desired_monitoring_interval, new_desired_monitoring_interval
                )
            )
            desired_monitoring_interval = new_desired_monitoring_interval
            DESIRED_MONITORING_INTERVAL.set(desired_monitoring_interval)

        pool_executor = ProcessPoolExecutor(max_workers=cur_number_workers)
        NUMBER_WORKERS.set(cur_number_workers)

        current_list = []
        if SERVICE_LIST_MODE == LIST_REDIS_MODE:
            LOGGER.debug(f"Services at the Redis DB: {cache.llen(SERVICE_LIST_KEY)}")
            current_list.extend(
                [
                    pickle.loads(service)
                    for service in cache.lrange(SERVICE_LIST_KEY, 0, -1)
                ]
            )
        elif SERVICE_LIST_MODE == LIST_SHARED_MODE:
            current_list.extend(service_list)

        CURRENT_SERVICES.set(len(current_list))

        if len(current_list) == 0:
            LOGGER.info(
                f"No services to monitor... {desired_monitoring_interval} [sec.] / {cur_number_workers} workers"
            )

            duration = time.time() - start_time

            # calculate new number of workers
            cur_number_workers = get_number_workers(
                cur_number_workers, duration, desired_monitoring_interval
            )

            LOOP_TIME.observe(0)  # ignore internal procedure time
            time.sleep(desired_monitoring_interval - duration)
            continue

        LOGGER.info(
            "Starting new monitoring cycle for {} sec. with {} for {} "
            "services with {} workers...".format(
                desired_monitoring_interval,
                "REDIS" if SERVICE_LIST_MODE == 1 else "local",
                len(current_list),
                cur_number_workers,
            )
        )

        # start pool implementation
        if len(current_list) == 0:  # guard clause to re-check if services still there
            LOGGER.info(
                f"No services to monitor... "
                f"{desired_monitoring_interval} / {cur_number_workers}"
            )

            duration = time.time() - start_time

            # calculate new number of workers
            cur_number_workers = get_number_workers(
                cur_number_workers, duration, desired_monitoring_interval
            )

            LOOP_TIME.observe(0)
            time.sleep(desired_monitoring_interval - duration)
            continue

        # process to get (close to) equal slices:
        # https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
        k, m = divmod(len(current_list), cur_number_workers)
        if k == 0:  # happens when a single process is working
            k = m
            m = 0
        # dividing async work across multiple processes:
        # https://stackoverflow.com/questions/69729488/how-to-run-multiple-asyncio-loops-inside-syncrhonous-sub-processes-inside-a-main
        # https://stackoverflow.com/questions/65557258/typeerror-cant-pickle-coroutine-objects-when-i-am-using-asyncio-loop-run-in-ex
        # https://stackoverflow.com/questions/69741177/run-multiple-async-loops-in-separate-processes-within-a-main-async-app
        tasks = [
            event_loop.run_in_executor(
                pool_executor,
                delegate_services,
                current_list,
                i * k + min(i, m),  # first index
                (i + 1) * k + min(i + 1, m),  # last index
                host,
                port,
                desired_monitoring_interval * 0.9,
            )
            for i in range(cur_number_workers)
        ]
        # await for all tasks to finish
        await asyncio.gather(*tasks)

        end_time = time.time()

        duration = end_time - start_time
        LOOP_TIME.observe(duration)
        LOGGER.info(
            "Monitoring loop with {} services took {:.3f} seconds ({:.2f}%)... "
            "Waiting for {:.2f} seconds...".format(
                len(current_list),
                duration,
                (duration / desired_monitoring_interval) * 100,
                desired_monitoring_interval - duration,
            )
        )

        # calculate new number of workers
        cur_number_workers = get_number_workers(
            cur_number_workers, duration, desired_monitoring_interval * 0.9
        )
        LOGGER.info(f"New number of workers: {cur_number_workers}")

        if duration / desired_monitoring_interval > 0.9:
            LOGGER.warning(
                "Monitoring loop is taking {} % of the desired time "
                "({} seconds)".format(
                    (duration / desired_monitoring_interval) * 100,
                    desired_monitoring_interval,
                )
            )
        if desired_monitoring_interval - duration > 0:
            time.sleep(desired_monitoring_interval - duration)


def main():
    global LOGGER  # pylint: disable=global-statement

    log_level = get_log_level()
    logging.basicConfig(level=log_level)
    LOGGER = logging.getLogger(__name__)

    logging.getLogger("hpack").setLevel(logging.CRITICAL)

    wait_for_environment_variables(
        [
            get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST),
            get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
            get_env_var_name(ServiceNameEnum.MONITORING, ENVVAR_SUFIX_SERVICE_HOST),
            get_env_var_name(
                ServiceNameEnum.MONITORING, ENVVAR_SUFIX_SERVICE_PORT_GRPC
            ),
            get_env_var_name(
                ServiceNameEnum.OPTICALATTACKDETECTOR, ENVVAR_SUFIX_SERVICE_HOST
            ),
            get_env_var_name(
                ServiceNameEnum.OPTICALATTACKDETECTOR, ENVVAR_SUFIX_SERVICE_PORT_GRPC
            ),
        ]
    )

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    LOGGER.info("Starting...")

    # Start metrics server
    metrics_port = get_metrics_port()
    start_http_server(metrics_port)

    if SERVICE_LIST_MODE not in [1, 2]:
        LOGGER.critical(
            "Service mode has wrong configuration. Value: {}.".format(SERVICE_LIST_MODE)
        )

    redis_host = get_service_host(ServiceNameEnum.CACHING)
    if redis_host is not None:
        redis_port = int(get_setting("CACHINGSERVICE_SERVICE_PORT_REDIS", default=6379))
        redis_password = get_setting("REDIS_PASSWORD")
        LOGGER.debug(f"Redis password: {redis_password}")

    service_list = None
    cache = None
    if SERVICE_LIST_MODE == LIST_REDIS_MODE:
        cache = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
        cache.ping()
        LOGGER.info(f"Connecting to Redis: host={redis_host}, port={redis_port}, password={redis_password}")

        # clean the existing list that will be populated later on in this function
        cache.delete(SERVICE_LIST_KEY)
    elif SERVICE_LIST_MODE == LIST_SHARED_MODE:
        # creating a thread-safe list to be shared among threads
        service_list = Manager().list()

    LOGGER.info("Connecting with context component...")
    context_client: ContextClient = ContextClient()
    monitoring_client: MonitoringClient = MonitoringClient()
    LOGGER.info("Connected successfully...")

    if get_setting("TESTING", default=False):
        # if testing, create dummy services
        kpi_id = create_kpi(monitoring_client, "1213")
        append_service(
            {"context": "admin", "service": "1213", "kpi": kpi_id.kpi_id.uuid},
            service_list=service_list,
            cache=cache,
        )
        kpi_id = create_kpi(monitoring_client, "1456")
        append_service(
            {"context": "admin", "service": "1456", "kpi": kpi_id.kpi_id.uuid},
            service_list=service_list,
            cache=cache,
        )

    context_ids: ContextIdList = context_client.ListContextIds(Empty())

    # populate with initial services
    for context_id in context_ids.context_ids:
        context_services: ServiceIdList = context_client.ListServiceIds(context_id)
        for service_id in context_services.service_ids:
            service: Service = context_client.GetService(service_id)
            if (
                service.service_type
                == ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE
            ):
                # in case of a service restart, monitoring component will not duplicate KPIs
                # but rather return the existing KPI if that's the case
                kpi_id = create_kpi(monitoring_client, service_id.service_uuid.uuid)
                append_service(
                    {
                        "context": context_id.context_uuid.uuid,
                        "service": service_id.service_uuid.uuid,
                        "kpi": kpi_id.kpi_id.uuid,
                    },
                    service_list=service_list,
                    cache=cache,
                )

    context_client.close()
    monitoring_client.close()

    # starting background process to monitor service addition/removal
    process_context = Process(
        target=get_context_updates, args=(terminate, service_list, cache)
    )
    process_context.start()

    time.sleep(5)  # wait for the context updates to startup

    # runs the async loop in the background
    loop = asyncio.get_event_loop()
    loop.run_until_complete(monitor_services(terminate, service_list, cache))
    # asyncio.create_task(monitor_services(service_list))

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=10):
        pass

    LOGGER.info("Terminating...")
    process_context.kill()
    # process_security_loop.kill()

    LOGGER.info("Bye")
    return 0


if __name__ == "__main__":
    sys.exit(main())
