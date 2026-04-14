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
import requests
import time
import socket
from unittest.mock import patch
from device.service.drivers.qkd.QKDDriver2 import QKDDriver

MOCK_QKD_ADDRESS = '127.0.0.1'  # Use localhost to connect to the mock node in the Docker container
MOCK_PORT = 11111

@pytest.fixture(scope="module")
def wait_for_mock_node():
    """
    Fixture to wait for the mock QKD node to be ready before running tests.
    """
    timeout = 30  # seconds
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((MOCK_QKD_ADDRESS, MOCK_PORT), timeout=1):
                break  # Success
        except (socket.timeout, socket.error):
            if time.time() - start_time > timeout:
                raise RuntimeError("Timed out waiting for mock QKD node to be ready.")
            time.sleep(1)

@pytest.fixture
def qkd_driver(wait_for_mock_node):
    return QKDDriver(address=MOCK_QKD_ADDRESS, port=MOCK_PORT, username='user', password='pass')

# Deliverable Test ID: SBI_Test_01
def test_qkd_driver_connection(qkd_driver):
    assert qkd_driver.Connect() is True

# Deliverable Test ID: SBI_Test_01
def test_qkd_driver_invalid_connection():
    qkd_driver = QKDDriver(address=MOCK_QKD_ADDRESS, port=12345, username='user', password='pass')  # Use invalid port directly
    assert qkd_driver.Connect() is False

# Deliverable Test ID: SBI_Test_10
@patch('device.service.drivers.qkd.QKDDriver2.requests.get')
def test_qkd_driver_timeout_connection(mock_get, qkd_driver):
    mock_get.side_effect = requests.exceptions.Timeout
    qkd_driver.timeout = 0.001  # Simulate very short timeout
    assert qkd_driver.Connect() is False
