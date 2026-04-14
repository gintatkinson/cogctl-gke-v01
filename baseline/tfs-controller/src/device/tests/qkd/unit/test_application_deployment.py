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
import json
import os
os.environ['DEVICE_EMULATED_ONLY'] = 'YES'
from device.service.drivers.qkd.QKDDriver2 import QKDDriver

MOCK_QKD_ADDRRESS = '10.0.2.10'
MOCK_PORT = 11111

@pytest.fixture
def qkd_driver():
    # Initialize the QKD driver with the appropriate settings
    return QKDDriver(address=MOCK_QKD_ADDRRESS, port=MOCK_PORT, username='user', password='pass')

def test_application_deployment(qkd_driver):
    qkd_driver.Connect()

    # Application registration data
    app_data = {
        'qkd_app': [
            {
                'app_id': '00000001-0001-0000-0000-000000000001',
                'client_app_id': [],
                'app_statistics': {'statistics': []},
                'app_qos': {},
                'backing_qkdl_id': []
            }
        ]
    }

    # Send a POST request to create the application
    response = qkd_driver.SetConfig([('/qkd_applications/qkd_app', json.dumps(app_data))])
    
    # Verify response
    assert response[0] is True, "Expected application registration to succeed"
