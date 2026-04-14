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

import json
import os
import pytest
import requests
from requests.exceptions import HTTPError
from device.service.drivers.qkd.QKDDriver2 import QKDDriver
from device.service.drivers.qkd.Tools2 import RESOURCE_CAPABILITES

# Helper function to print data in a formatted JSON style for debugging
def print_data(label, data):
    print(f"{label}: {json.dumps(data, indent=2)}")

# Environment variables for sensitive information
QKD1_ADDRESS = os.getenv("QKD1_ADDRESS")
MOCK_QKD_ADDRRESS = '127.0.0.1'
MOCK_PORT = 11111
PORT = os.getenv("QKD_PORT")
USERNAME = os.getenv("QKD_USERNAME")
PASSWORD = os.getenv("QKD_PASSWORD")


# Utility function to retrieve JWT token
def get_jwt_token(address, port, username, password):
    url = f"http://{address}:{port}/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = f"username={username}&password={password}"
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve JWT token: {e}")
        return None

# Real QKD Driver (Requires JWT token)
@pytest.fixture
def real_qkd_driver():
    token = get_jwt_token(QKD1_ADDRESS, PORT, USERNAME, PASSWORD)  # Replace with actual details
    if not token:
        pytest.fail("Failed to retrieve JWT token.")
    headers = {'Authorization': f'Bearer {token}'}
    return QKDDriver(address=QKD1_ADDRESS, port=PORT, headers=headers)

# Mock QKD Driver (No actual connection, mock capabilities)
@pytest.fixture
def mock_qkd_driver():
    # Initialize the mock QKD driver with mock settings
    token = "mock_token"
    headers = {"Authorization": f"Bearer {token}"}
    return QKDDriver(address=MOCK_QKD_ADDRRESS, port=MOCK_PORT, headers=headers)

# General function to retrieve and test capabilities
def retrieve_capabilities(qkd_driver, driver_name):
    try:
        qkd_driver.Connect()
        capabilities = qkd_driver.GetConfig([RESOURCE_CAPABILITES])
        assert isinstance(capabilities, list), "Expected a list of capabilities"
        assert len(capabilities) > 0, f"No capabilities found for {driver_name}"
        print_data(f"{driver_name} Capabilities", capabilities)
    except HTTPError as e:
        pytest.fail(f"HTTPError while fetching capabilities for {driver_name}: {e}")
    except AssertionError as e:
        pytest.fail(f"AssertionError: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")

# Test for Real QKD Capabilities
def test_real_qkd_capabilities(real_qkd_driver):
    retrieve_capabilities(real_qkd_driver, "Real QKD")

# Test for Mock QKD Capabilities
def test_mock_qkd_capabilities(mock_qkd_driver):
    retrieve_capabilities(mock_qkd_driver, "Mock QKD")
