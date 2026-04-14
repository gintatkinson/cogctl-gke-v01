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

import pickle
import uuid
import logging
import signal
import threading

import redis
from kubernetes import client, config

from common.Settings import get_setting, wait_for_environment_variables

# Configs can be set in Configuration class directly or using helper utility
namespace = get_setting("TFS_K8S_NAMESPACE", default="tfs")
config.load_kube_config()
v1 = client.CoreV1Api()

ret = v1.list_namespaced_endpoints(namespace=namespace, watch=False)
for item in ret.items:
    if "caching" in item.metadata.name:
        for subset in item.subsets:
            for port in subset.ports:
                print(item.metadata.name, port)
                if "redis" in port.name:  # endpoint is ready for being scraped
                    CACHING_HOST = subset.addresses[0].ip
                    CACHING_PORT = port.port

LOGGER = None
SERVICE_LIST_KEY = get_setting(
    "OPTICALATTACKMANAGER_SERVICE_LIST_KEY", default="opt-sec-active-services"
)

# setting up graceful shutdown
terminate = threading.Event()


def signal_handler(signal, frame):  # pylint: disable=redefined-outer-name
    LOGGER.warning("Terminate signal received")
    terminate.set()


def manage_number_services(terminate):

    # connecting with Redis
    redis_password = get_setting("REDIS_PASSWORD")
    
    cache = None
    try:
        LOGGER.info(f"Connecting to Redis: host={CACHING_HOST}, port={CACHING_PORT}, password={redis_password}")
        cache = redis.Redis(host=CACHING_HOST, port=CACHING_PORT, password=redis_password)
        cache.ping()
        LOGGER.info("Connected to Redis")
    except Exception as e:
        LOGGER.exception(e)
    
    # clean the existing list that will be populated later on in this function
    cache.delete(SERVICE_LIST_KEY)

    # make sure we have the correct loop time
    cache.set("MONITORING_INTERVAL", 30)

    # define number of services
    next_kpi_id = 0

    print("Starting load!")
    while not terminate.wait(timeout=1):  # timeout=300
        print("\n\no <number> -> sets the number services currently monitored")
        print("p <seconds> -> sets the loop period")
        print("m <1=SL / 2=UL> -> sets the ML model used")
        print("q -> exit")
        from_user = input("Command: ")
        if from_user.strip() == "q":
            return
        try:
            parts = from_user.split(" ")
            assert len(parts) == 2, "Wrong number of values!"
            number = int(parts[1])
            if parts[0].strip() == "o":
                print(f"New number of services: {number}")

                cur_services = cache.llen(SERVICE_LIST_KEY)
                diff_services = cur_services - number

                if diff_services < 0:  # current is lower than expected
                    LOGGER.debug(f"\tinserting <{-diff_services}> services")
                    for _ in range(-diff_services):
                        next_kpi_id += 1
                        cache.lpush(
                            SERVICE_LIST_KEY,
                            pickle.dumps(
                                {
                                    "context": str(uuid.uuid4()),
                                    "service": str(uuid.uuid4()),
                                    # "kpi": str(uuid.uuid4()),
                                    "kpi": str(next_kpi_id),
                                }
                            ),
                        )
                    LOGGER.debug(f"Services at the Redis DB: {cache.llen(SERVICE_LIST_KEY)}")
                    
                elif diff_services > 0:  # current is greater than expected
                    # delete services
                    LOGGER.debug(f"\tdeleting <{diff_services}> services")
                    cache.lpop(SERVICE_LIST_KEY, diff_services)

            elif parts[0].strip() == "p":
                print(f"setting new period: {number} seconds")
                cache.set("MONITORING_INTERVAL", number)
            elif parts[0] == "m":
                if "1" == parts[1].strip():
                    print(f"setting new ML model: {parts[1]}")
                    cache.set("ATTACK_DETECTION_MODE", "SL")
                elif "2" == parts[1].strip():
                    print(f"setting new ML model: {parts[1]}")
                    cache.set("ATTACK_DETECTION_MODE", "UL")
                else:
                    print(f"your input is not valid: `{from_user}`")
            else:
                print(f"Wrong command: {from_user}")
        except:
            print(f"Your input is not a number: `{from_user}`")
            continue

    # make sure we have the correct loop time
    cache.set("MONITORING_INTERVAL", 30)

    print("Finished load!")


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

    manage_number_services(terminate)

    # exits
    LOGGER.info("Bye!")
