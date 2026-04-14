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

import pytest
from typing import List, Tuple
from device.service.drivers.qkd.QKDDriver2 import QKDDriver

MOCK_QKD_ADDRRESS = '127.0.0.1'
MOCK_PORT = 11111


@pytest.fixture
def qkd_driver():
    # Initialize the QKD driver
    return QKDDriver(address=MOCK_QKD_ADDRRESS, port=MOCK_PORT, username='user', password='pass')


def test_state_subscription(qkd_driver):
    """
    Test Case ID: SBI_Test_06 - Subscribe to state changes and validate the subscription process.
    """
    qkd_driver.Connect()

    try:
        # Step 1: Define the subscription
        subscriptions = [
            ('00000001-0000-0000-0000-000000000000', 60, 10)  # (node_id, frequency, timeout)
        ]
        
        # Step 2: Subscribe to state changes using the driver method
        subscription_results = qkd_driver.SubscribeState(subscriptions)
        
        # Step 3: Validate that the subscription was successful
        assert all(result is True for result in subscription_results), "Subscription to state changes failed."

        print("State subscription successful:", subscription_results)
    
    except Exception as e:
        pytest.fail(f"An unexpected error occurred during state subscription: {e}")
    
    finally:
        qkd_driver.Disconnect()
