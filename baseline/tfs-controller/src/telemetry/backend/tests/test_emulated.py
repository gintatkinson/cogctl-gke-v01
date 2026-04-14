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

import logging
import time
import pytest
from telemetry.backend.service.collectors.emulated.EmulatedCollector import EmulatedCollector
from telemetry.backend.tests.messages_emulated import (
    create_test_configuration,
    create_specific_config_keys,
    create_config_for_delete,
    create_test_subscriptions,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def setup_collector():
    """Sets up an EmulatedCollector instance for testing."""
    yield EmulatedCollector(address="127.0.0.1", port=8080)

@pytest.fixture
def connected_configured_collector(setup_collector):
    collector = setup_collector # EmulatedCollector(address="127.0.0.1", port=8080)
    collector.Connect()
    #collector.SetConfig(create_test_configuration())   # method not implemented
    yield collector
    collector.Disconnect()

def test_connect(setup_collector):
    logger.info(">>> test_connect <<<")
    collector = setup_collector
    assert collector.Connect() is True
    assert collector.connected is True

def test_disconnect(setup_collector):
    logger.info(">>> test_disconnect <<<")
    collector = setup_collector
    collector.Connect()
    assert collector.Disconnect() is True
    assert collector.connected is False

# def test_set_config(setup_collector):
#     logger.info(">>> test_set_config <<<")
#     collector = setup_collector
#     collector.Connect()

#     config = create_test_configuration()

#     results = collector.SetConfig(config)
#     assert all(result is True for result in results)

# def test_get_config(connected_configured_collector):
#     logger.info(">>> test_get_config <<<")
#     resource_keys = create_specific_config_keys() 
#     results = connected_configured_collector.GetConfig(resource_keys)

#     for key, value in results:
#         assert key in create_specific_config_keys()
#         assert value is not None

# def test_delete_config(connected_configured_collector):
#     logger.info(">>> test_delete_config <<<")
#     resource_keys = create_config_for_delete() 

#     results = connected_configured_collector.DeleteConfig(resource_keys)
#     assert all(result is True for result in results)

def test_subscribe_state(connected_configured_collector):
    logger.info(">>> test_subscribe_state <<<")
    subscriptions = create_test_subscriptions() 

    results = connected_configured_collector.SubscribeState(subscriptions)
    # logger.info(f"Subscribed result: {results}.")
    assert results ==  [False, True, True] # all(result is True for result in results)

def test_unsubscribe_state(connected_configured_collector):
    logger.info(">>> test_unsubscribe_state <<<")
    subscriptions = create_test_subscriptions()

    connected_configured_collector.SubscribeState(subscriptions)
    results = connected_configured_collector.UnsubscribeState(subscriptions)
    assert results ==  [False, True, True] # all(result is True for result in results)

def test_get_state(connected_configured_collector):
    logger.info(">>> test_get_state <<<")
    subscriptions = create_test_subscriptions()

    connected_configured_collector.SubscribeState(subscriptions)
    logger.info(f"Subscribed to state: {subscriptions}. waiting for 12 seconds ...")
    time.sleep(12)

    state_iterator = connected_configured_collector.GetState(blocking=False)
    states = list(state_iterator)

    assert len(states) > 0
