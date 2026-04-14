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
import json, logging, pytest, time, types
from device.service.drivers.morpheus.MorpheusApiDriver import MorpheusApiDriver

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


##### DRIVER FIXTURE ###################################################################################################

DRIVER_SETTING_ADDRESS  = '127.0.0.1'
DRIVER_SETTING_PORT     = 8090

@pytest.fixture(scope='session')
def driver() -> MorpheusApiDriver:
    _driver = MorpheusApiDriver(
        DRIVER_SETTING_ADDRESS, DRIVER_SETTING_PORT,
    )
    _driver.Connect()
    yield _driver
    time.sleep(1)
    _driver.Disconnect()


##### TEST METHODS #####################################################################################################

def print_data(label, data):
    print(f"{label}: {json.dumps(data, indent=2)}")

def test_initial_config_retrieval(driver: MorpheusApiDriver):
    config = driver.GetInitialConfig()

    assert isinstance(config, list), "Expected a list for initial config"
    assert len(config) > 0, "Initial config should not be empty"

    print_data("Initial Config", config)

def test_retrieve_config(driver: MorpheusApiDriver):
    config = driver.GetConfig(None)

    assert isinstance(config, list), "Expected a list for config"
    assert len(config) > 0, "Config should not be empty"

    print_data("Config", config)

def test_set_config(driver: MorpheusApiDriver):
    results = driver.SetConfig([('traffic_type', 'UDP')])

    assert len(results) == 1, "Expected only one result"
    assert results[0] is True, "Expected a succesfull result"

def test_retrieve_state(driver: MorpheusApiDriver):
    results = driver.SubscribeState([])

    assert all(isinstance(result, bool) and result for result in results), \
            f"Subscription error: {results}"

    state = driver.GetState(blocking=True)

    assert isinstance(state, types.GeneratorType), "Expected an iterator for state"
    i = 0
    for item in state:
        if i == 0:
            print_data("State Item", item)
            i += 1
        else:
            if item[1] == 'state': continue
            print_data("Other Item", item)
            i += 1
        if i > 3: break

    results = driver.UnsubscribeState([])

    assert all(isinstance(result, bool) and result for result in results), \
            f"Unsubscription error: {results}"
