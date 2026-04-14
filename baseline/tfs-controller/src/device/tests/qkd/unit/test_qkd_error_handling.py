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

import pytest, requests
from requests.exceptions import ConnectionError, HTTPError, Timeout
from device.service.drivers.qkd.QKDDriver2 import QKDDriver

MOCK_QKD_ADDRRESS = '127.0.0.1'
MOCK_PORT = 11111

@pytest.fixture
def qkd_driver():
    # Initialize the QKD driver for testing
    return QKDDriver(address=MOCK_QKD_ADDRRESS, port=MOCK_PORT, username='user', password='pass')

def test_invalid_operations_on_network_links(qkd_driver):
    """
    Test Case ID: SBI_Test_09 - Perform invalid operations and validate error handling.
    Objective: Perform invalid operations on network links and ensure proper error handling and logging.
    """
    qkd_driver.Connect()

    # Step 1: Perform invalid operation with an incorrect resource key
    invalid_payload = {
        "invalid_resource_key": {
            "invalid_field": "invalid_value"
        }
    }

    try:
        # Attempt to perform an invalid operation (simulate wrong resource key)
        response = requests.post(f'http://{qkd_driver.address}:{qkd_driver.port}/invalid_resource', json=invalid_payload)
        response.raise_for_status()

    except HTTPError as e:
        # Step 2: Validate proper error handling and user-friendly messages
        print(f"Handled HTTPError: {e}")
        assert e.response.status_code in [400, 404], "Expected 400 Bad Request or 404 Not Found for invalid operation."
        if e.response.status_code == 404:
            assert "Not Found" in e.response.text, "Expected user-friendly 'Not Found' message."
        elif e.response.status_code == 400:
            assert "Invalid resource key" in e.response.text, "Expected user-friendly 'Bad Request' message."

    except Exception as e:
        # Log unexpected exceptions
        pytest.fail(f"Unexpected error occurred: {e}")

    finally:
        qkd_driver.Disconnect()

def test_network_failure_simulation(qkd_driver):
    """
    Test Case ID: SBI_Test_10 - Simulate network failures and validate resilience and recovery.
    Objective: Simulate network failures (e.g., QKD node downtime) and validate system's resilience.
    """
    qkd_driver.Connect()

    try:
        # Step 1: Simulate network failure (disconnect QKD node, or use unreachable address/port)
        qkd_driver_with_failure = QKDDriver(address='127.0.0.1', port=12345, username='user', password='pass')  # Valid but incorrect port

        # Try to connect and retrieve state, expecting a failure
        response = qkd_driver_with_failure.GetState()

        # Step 2: Validate resilience and recovery mechanisms
        # Check if the response is empty, indicating a failure to retrieve state
        if not response:
            print("Network failure simulated successfully and handled.")
        else:
            pytest.fail("Expected network failure but received a valid response.")
    
    except HTTPError as e:
        # Log HTTP errors as part of error handling
        print(f"Handled network failure error: {e}")
    
    except Exception as e:
        # Step 3: Log unexpected exceptions
        print(f"Network failure encountered: {e}")
    
    finally:
        # Step 4: Ensure driver disconnects properly
        qkd_driver.Disconnect()
