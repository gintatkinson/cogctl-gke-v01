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

import copy, deepdiff, logging, time
from typing import Callable, Dict, List, Tuple, Union
from device.service.driver_api._Driver import (
    RESOURCE_ENDPOINTS, RESOURCE_INTERFACES, RESOURCE_NETWORK_INSTANCES,
    RESOURCE_ROUTING_POLICIES, RESOURCE_SERVICES
)
from device.service.drivers.gnmi_openconfig.GnmiOpenConfigDriver import GnmiOpenConfigDriver
from device.tests.gnmi_openconfig.storage.Storage import Storage
from .result_config_adapters import adapt_endpoint, adapt_interface, adapt_network_instance

LOGGER = logging.getLogger(__name__)

def get_config(driver : GnmiOpenConfigDriver, resources_to_get : List[str]) -> List[Tuple[str, Dict]]:
    LOGGER.info('[get_config] resources_to_get = {:s}'.format(str(resources_to_get)))
    results_getconfig = driver.GetConfig(resources_to_get)
    LOGGER.info('[get_config] results_getconfig = {:s}'.format(str(results_getconfig)))
    return results_getconfig

def set_config(
    driver : GnmiOpenConfigDriver, resources_to_set : List[Tuple[str, Dict]]
) -> List[Tuple[str, Union[bool, Exception]]]:
    LOGGER.info('[set_config] resources_to_set = {:s}'.format(str(resources_to_set)))
    results_setconfig = driver.SetConfig(resources_to_set)
    LOGGER.info('[set_config] results_setconfig = {:s}'.format(str(results_setconfig)))
    return results_setconfig

def del_config(
    driver : GnmiOpenConfigDriver, resources_to_delete : List[Tuple[str, Dict]]
) -> List[Tuple[str, Union[bool, Exception]]]:
    LOGGER.info('resources_to_delete = {:s}'.format(str(resources_to_delete)))
    results_deleteconfig = driver.DeleteConfig(resources_to_delete)
    LOGGER.info('results_deleteconfig = {:s}'.format(str(results_deleteconfig)))
    return results_deleteconfig

def check_expected_config(
    driver : GnmiOpenConfigDriver, resources_to_get : List[str], expected_config : List[Dict],
    func_adapt_returned_config : Callable[[Tuple[str, Dict]], Tuple[str, Dict]] = lambda x: x,
    max_retries : int = 1, retry_delay : float = 0.5
) -> List[Dict]:
    LOGGER.info('expected_config = {:s}'.format(str(expected_config)))

    num_retry = 0
    return_data = None
    while num_retry < max_retries:
        results_getconfig = get_config(driver, resources_to_get)
        return_data = copy.deepcopy(results_getconfig)

        results_getconfig = [
            func_adapt_returned_config(resource_key, resource_value)
            for resource_key, resource_value in results_getconfig
        ]

        diff_data = deepdiff.DeepDiff(sorted(expected_config), sorted(results_getconfig))
        num_diffs = len(diff_data)
        if num_diffs == 0: break
        # let the device take some time to reconfigure
        time.sleep(retry_delay)
        num_retry += 1

    if num_diffs > 0: LOGGER.error('Differences[{:d}]:\n{:s}'.format(num_diffs, str(diff_data.pretty())))
    assert num_diffs == 0
    return return_data

def check_config_endpoints(
    driver : GnmiOpenConfigDriver, storage : Storage,
    max_retries : int = 1, retry_delay : float = 0.5
) -> List[Dict]:
    return check_expected_config(
        driver, [RESOURCE_ENDPOINTS], storage.endpoints.get_expected_config(),
        adapt_endpoint, max_retries=max_retries, retry_delay=retry_delay
    )

def check_config_interfaces(
    driver : GnmiOpenConfigDriver, storage : Storage,
    max_retries : int = 1, retry_delay : float = 0.5
) -> List[Dict]:
    return check_expected_config(
        driver, [RESOURCE_INTERFACES], storage.interfaces.get_expected_config(),
        adapt_interface, max_retries=max_retries, retry_delay=retry_delay
    )

def check_config_network_instances(
    driver : GnmiOpenConfigDriver, storage : Storage,
    max_retries : int = 1, retry_delay : float = 0.5
) -> List[Dict]:
    return check_expected_config(
        driver, [RESOURCE_NETWORK_INSTANCES], storage.network_instances.get_expected_config(),
        adapt_network_instance, max_retries=max_retries, retry_delay=retry_delay
    )
