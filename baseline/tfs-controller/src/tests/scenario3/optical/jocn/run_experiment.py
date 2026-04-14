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

import datetime
import pickle
import uuid
import logging
import multiprocessing
import signal
import os
import threading
import yaml

import requests
import redis
from kubernetes import client, config

from common.Constants import ServiceNameEnum
from common.Settings import get_service_host, get_setting, wait_for_environment_variables

LOGGER = None
SERVICE_LIST_KEY = get_setting(
    "OPTICALATTACKMANAGER_SERVICE_LIST_KEY", default="opt-sec:active-services"
)

# Configs can be set in Configuration class directly or using helper utility
namespace = get_setting("TFS_K8S_NAMESPACE", default="tfs")
config.load_kube_config()
v1 = client.CoreV1Api()

ret = v1.list_namespaced_endpoints(namespace=namespace, watch=False)
for item in ret.items:
    if "caching" in item.metadata.name:
        for subset in item.subsets:
            for port in subset.ports:
                if "redis" in port.name:  # endpoint is ready for being scraped
                    CACHING_HOST = subset.addresses[0].ip
                    CACHING_PORT = port.port

logging.getLogger("kubernetes").setLevel(logging.INFO) # avoid lengthy messages

# setting up graceful shutdown
terminate = threading.Event()


def signal_handler(signal, frame):  # pylint: disable=redefined-outer-name
    LOGGER.warning("Terminate signal received")
    terminate.set()


def manage_number_services(terminate, folder):

    # connecting with Redis
    redis_password = get_setting("REDIS_PASSWORD")
    
    cache = None
    try:
        cache = redis.Redis(host=CACHING_HOST, port=CACHING_PORT, password=redis_password)
    except Exception as e:
        LOGGER.exception(e)
    
    # clean the existing list that will be populated later on in this function
    cache.delete(SERVICE_LIST_KEY)

    # make sure we have the correct loop time
    cache.set("MONITORING_INTERVAL", 30)

    # define number of services
    # 6 values followed by two zeros
    number_services = [0, 10]

    loads = [120, 240, 480, 960, 1440, 1920, 1921]
    for load in loads:
        number_services.append(int(load/2))
        for _ in range(5):
            number_services.append(load)
        for _ in range(2):
            number_services.append(0)

    ticks = 1  # defines how much to wait
    set_to_60 = False
    cur_tick = 0
    LOGGER.info("Starting load!")
    while not terminate.wait(timeout=30):  # timeout=300
        if cur_tick % ticks == 0:
            LOGGER.debug("go load!")

            # calculate the difference between current and expected
            cur_services = cache.llen(SERVICE_LIST_KEY)
            diff_services = cur_services - number_services[cur_tick % len(number_services)]

            if not set_to_60 and number_services[cur_tick + 1 % len(number_services)] == 961:
                cache.set("MONITORING_INTERVAL", 60)
                LOGGER.info("Setting monitoring interval to 60")
                set_to_60 = True

            if diff_services < 0:  # current is lower than expected
                LOGGER.debug(f"inserting <{-diff_services}> services")
                for _ in range(-diff_services):
                    cache.lpush(
                        SERVICE_LIST_KEY,
                        pickle.dumps(
                            {
                                "context": str(uuid.uuid4()),
                                "service": str(uuid.uuid4()),
                                "kpi": str(uuid.uuid4()),
                            }
                        ),
                    )
            elif diff_services > 0:  # current is greater than expected
                # delete services
                LOGGER.debug(f"deleting <{diff_services}> services")
                cache.lpop(SERVICE_LIST_KEY, diff_services)

            assert number_services[cur_tick % len(number_services)] == cache.llen(SERVICE_LIST_KEY)

        else:
            LOGGER.debug("tick load!")
        cur_tick += 1
        if cur_tick > len(number_services) + 1:
            break

    # make sure we have the correct loop time
    cache.set("MONITORING_INTERVAL", 30)

    LOGGER.info("Finished load!")


if __name__ == "__main__":
    # logging.basicConfig(level="DEBUG")
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    LOGGER = logging.getLogger(__name__)

    wait_for_environment_variables(
        ["REDIS_PASSWORD"]
    )

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # start load handler
    manage_number_services(terminate=terminate)

    # Wait for Ctrl+C or termination signal
    while not terminate.wait(timeout=0.1):
        pass

    # exits
    LOGGER.info("Bye!")
