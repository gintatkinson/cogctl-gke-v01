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

import os
os.environ['DEVICE_EMULATED_ONLY'] = 'YES'


# pylint: disable=wrong-import-position
import json, logging, pytest, time
from typing import Dict, List, Tuple, Union
from device.service.driver_api._Driver import RESOURCE_ACL, RESOURCE_ENDPOINTS
from device.service.drivers.restconf_openconfig.RestConfOpenConfigDriver import RestConfOpenConfigDriver


DATA_FILE_PATH = 'device/tests/restconf_openconfig/data/'

##### LOGGERS ##########################################################################################################

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


##### DRIVER FIXTURE ###################################################################################################

DRIVER_ADDRESS  = '10.0.2.25'
DRIVER_PORT     = 8888
DRIVER_SETTINGS = dict(
    scheme='http', username='admin', password='admin',
    timeout=30, verify_certs=False, allow_redirects=True,
)

@pytest.fixture(scope='session')
def driver() -> RestConfOpenConfigDriver:
    _driver = RestConfOpenConfigDriver(
        DRIVER_ADDRESS, DRIVER_PORT, **DRIVER_SETTINGS
    )
    _driver.Connect()
    yield _driver
    time.sleep(1)
    _driver.Disconnect()


##### HELPER METHODS ###################################################################################################

def get_config(
    driver : RestConfOpenConfigDriver, resources_to_get : List[str]
) -> List[Tuple[str, Dict]]:
    LOGGER.info('[get_config] resources_to_get = {:s}'.format(str(resources_to_get)))
    results_getconfig = driver.GetConfig(resources_to_get)
    LOGGER.info('[get_config] results_getconfig = {:s}'.format(str(results_getconfig)))
    return results_getconfig

def set_config(
    driver : RestConfOpenConfigDriver, resources_to_set : List[Tuple[str, Dict]]
) -> List[Tuple[str, Union[bool, Exception]]]:
    LOGGER.info('[set_config] resources_to_set = {:s}'.format(str(resources_to_set)))
    results_setconfig = driver.SetConfig(resources_to_set)
    LOGGER.info('[set_config] results_setconfig = {:s}'.format(str(results_setconfig)))
    return results_setconfig

def del_config(
    driver : RestConfOpenConfigDriver, resources_to_delete : List[Tuple[str, Dict]]
) -> List[Tuple[str, Union[bool, Exception]]]:
    LOGGER.info('[del_config] resources_to_delete = {:s}'.format(str(resources_to_delete)))
    results_deleteconfig = driver.DeleteConfig(resources_to_delete)
    LOGGER.info('[del_config] results_deleteconfig = {:s}'.format(str(results_deleteconfig)))
    return results_deleteconfig

def create_acl_from_file(file_name : str) -> Tuple[str, Dict]:
    with open(DATA_FILE_PATH + file_name, 'r', encoding='UTF-8') as f:
        acl_data = json.load(f)
        device_uuid   = acl_data['endpoint_id']['device_id']['device_uuid']['uuid']
        endpoint_uuid = acl_data['endpoint_id']['endpoint_uuid']['uuid']
        aclset_name   = acl_data['rule_set']['name']
        key_or_path = '/device[{:s}]/endpoint[{:s}]/acl_ruleset[{:s}]'.format(
            device_uuid, endpoint_uuid, aclset_name
        )
        return key_or_path, acl_data


##### TEST METHODS #####################################################################################################

def test_get_endpoints(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    results_getconfig = get_config(driver, [RESOURCE_ENDPOINTS])
    assert len(results_getconfig) > 0
    endpoint_names = {res_val['uuid'] for _, res_val in results_getconfig}
    assert len(endpoint_names) == 1
    assert 'enp0s3' in endpoint_names


def test_get_acls(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    get_config(driver, [RESOURCE_ACL])


def test_set_acl_reject_30435_from_all(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    resources_to_set = [create_acl_from_file('reject_30435_from_all.json')]
    set_config(driver, resources_to_set)


def test_set_acl_accept_30435_from_10_0_2_2(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    resources_to_set = [create_acl_from_file('accept_30435_from_10_0_2_2.json')]
    set_config(driver, resources_to_set)


def test_set_acl_accept_30435_from_10_0_2_10(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    resources_to_set = [create_acl_from_file('accept_30435_from_10_0_2_10.json')]
    set_config(driver, resources_to_set)


def test_del_acl_accept_30435_from_10_0_2_10(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    resources_to_delete = [create_acl_from_file('accept_30435_from_10_0_2_10.json')]
    del_config(driver, resources_to_delete)


def test_del_acl_accept_30435_from_10_0_2_2(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    resources_to_delete = [create_acl_from_file('accept_30435_from_10_0_2_2.json')]
    del_config(driver, resources_to_delete)


def test_del_acl_reject_30435_from_all(
    driver : RestConfOpenConfigDriver,  # pylint: disable=redefined-outer-name
) -> None:
    resources_to_delete = [create_acl_from_file('reject_30435_from_all.json')]
    del_config(driver, resources_to_delete)
