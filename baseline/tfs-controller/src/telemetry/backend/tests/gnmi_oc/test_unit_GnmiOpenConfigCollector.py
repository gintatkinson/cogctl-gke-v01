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
from telemetry.backend.service.collectors.gnmi_oc.GnmiOpenConfigCollector import GNMIOpenConfigCollector
from .messages import creat_basic_sub_request_parameters

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)8s [%(name)s - %(funcName)s()]: %(message)s",
)
logger = logging.getLogger(__name__)


@pytest.fixture
def sub_parameters():
    """Fixture to provide subscription parameters."""
    return creat_basic_sub_request_parameters()


@pytest.fixture
def collector(sub_parameters):
    """Fixture to create and connect GNMI collector."""
    collector = GNMIOpenConfigCollector(
        username = sub_parameters['username'],
        password = sub_parameters['password'],
        insecure = sub_parameters['insecure'],
        address  = sub_parameters['target'][0],
        port     = sub_parameters['target'][1],
    )
    collector.Connect()
    yield collector
    collector.Disconnect()


@pytest.fixture
def subscription_data(sub_parameters):
    """Fixture to provide subscription data."""
    # It should return a list of tuples with subscription parameters.
    return [
        (
            "x123",
            {
                "kpi"      : sub_parameters['kpi'],
                "endpoint" : sub_parameters['endpoint'],
                "resource" : sub_parameters['resource'],
            },
            float(10.0),
            float(5.0),
        ),
    ]

# --------------------------------------------------------------
# -------------------- ACTUAL TEST CASES -----------------------
# --------------------------------------------------------------
# Necessary to have a containerLab running with gNMI OpenConfig devices.
    # - See messages.py for more details on the parameters. 

def test_collector_connection(collector):
    """Test collector connection."""
    logger.info("----- Testing GNMI OpenConfig Collector Connection -----")
    assert collector.connected is True
    logger.debug("Collector connected: %s", collector.connected)


def test_subscription_state(collector, subscription_data):
    """Test state subscription."""
    logger.info("----- Testing State Subscription -----")
    response = collector.SubscribeState(subscription_data)
    logger.info("Subscription started: %s", subscription_data)
    assert all(response) and isinstance(response, list)


def test_get_state_updates(collector, subscription_data):
    """Test getting state updates."""
    logger.info("----- Testing State Updates -----")
    collector.SubscribeState(subscription_data)
    
    logger.info("Requesting state updates for 5 seconds ...")
    updates_received = []
    for samples in collector.GetState(duration=5.0, blocking=True):
        logger.info("Received state update: %s", samples)
        updates_received.append(samples)
    
    assert len(updates_received) > 0


def test_unsubscribe_state(collector, subscription_data):
    """Test unsubscribing from state."""
    logger.info("----- Testing Unsubscribe -----")
    collector.SubscribeState(subscription_data)
    
    time.sleep(2)  # Wait briefly for subscription to be active
    
    response = collector.UnsubscribeState("x123")
    logger.info("Unsubscribed from state: %s", subscription_data)
    assert response is True

def test_full_workflow(collector, subscription_data):
    """Test complete workflow: subscribe, get updates, unsubscribe."""
    logger.info("----- Testing Full Workflow -----")
    
    # Subscribe
    response1 = collector.SubscribeState(subscription_data)
    logger.info("Subscription started: %s", subscription_data)
    assert all(response1) and isinstance(response1, list)
    
    # Get updates
    logger.info("Requesting state updates for 5 seconds ...")
    updates_received = []
    for samples in collector.GetState(duration=5.0, blocking=True):
        logger.info("Received state update: %s", samples)
        updates_received.append(samples)
    assert len(updates_received) > 0
    # Wait for additional updates
    logger.info("Waiting for updates for 5 seconds...")
    time.sleep(5)
    
    # Unsubscribe
    response2 = collector.UnsubscribeState("x123")
    logger.info("Unsubscribed from state: %s", subscription_data)
    assert response2 is True
    
    logger.info("----- Workflow test completed -----")
