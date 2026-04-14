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

import pytest, requests, uuid
from requests.exceptions import HTTPError
from device.service.drivers.qkd.QKDDriver2 import QKDDriver
from device.service.drivers.qkd.Tools2 import RESOURCE_APPS

MOCK_QKD1_ADDRRESS = '127.0.0.1'
MOCK_PORT1 = 11111
MOCK_QKD3_ADDRRESS = '127.0.0.1'
MOCK_PORT3 = 33333

@pytest.fixture
def qkd_driver1():
    # Initialize the QKD driver for QKD1
    return QKDDriver(address=MOCK_QKD1_ADDRRESS, port=MOCK_PORT1, username='user', password='pass')

@pytest.fixture
def qkd_driver3():
    # Initialize the QKD driver for QKD3
    return QKDDriver(address=MOCK_QKD3_ADDRRESS, port=MOCK_PORT3, username='user', password='pass')

def create_qkd_app(driver, qkdn_id, backing_qkdl_id, client_app_id=None):
    """
    Helper function to create QKD applications on the given driver.
    """
    server_app_id = str(uuid.uuid4())  # Generate a unique server_app_id

    app_payload = {
        'app': {
            'server_app_id': server_app_id,
            'client_app_id': client_app_id if client_app_id else [],  # Add client_app_id if provided
            'app_status': 'ON',
            'local_qkdn_id': qkdn_id,
            'backing_qkdl_id': backing_qkdl_id
        }
    }
    
    try:
        # Log the payload being sent
        print(f"Sending payload to {driver.address}: {app_payload}")

        # Send POST request to create the application
        response = requests.post(f'http://{driver.address}/qkd_app/create_qkd_app', json=app_payload)
        
        # Check if the request was successful (HTTP 2xx)
        response.raise_for_status()
        
        # Validate the response
        assert response.status_code == 200, f"Failed to create QKD app for {driver.address}: {response.text}"
        
        response_data = response.json()
        assert response_data.get('status') == 'success', "Application creation failed."

        # Log the response from the server
        print(f"Server {driver.address} response: {response_data}")

        return server_app_id  # Return the created server_app_id

    except HTTPError as e:
        pytest.fail(f"HTTP error occurred while creating the QKD application on {driver.address}: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")

def test_create_qkd_application_bidirectional(qkd_driver1, qkd_driver3):
    """
    Create QKD applications on both qkd1 and qkd3, and validate the complete creation in both directions.
    """

    qkd_driver1.Connect()
    qkd_driver3.Connect()

    try:
        # Step 1: Create QKD application for qkd1, referencing qkd3 as the backing QKDL
        server_app_id_qkd1 = create_qkd_app(
            qkd_driver1,
            qkdn_id='00000001-0000-0000-0000-000000000000',
            backing_qkdl_id=['00000003-0002-0000-0000-000000000000']  # qkd3's QKDL
        )

        # Step 2: Create QKD application for qkd3, referencing qkd1 as the backing QKDL, and setting client_app_id to qkd1's app
        create_qkd_app(
            qkd_driver3,
            qkdn_id='00000003-0000-0000-0000-000000000000',
            backing_qkdl_id=['00000003-0002-0000-0000-000000000000'],  # qkd3's QKDL
            client_app_id=[server_app_id_qkd1]  # Set qkd1 as the client
        )

        # Step 3: Fetch applications from both qkd1 and qkd3 to validate that the applications exist
        apps_qkd1 = qkd_driver1.GetConfig([RESOURCE_APPS])
        apps_qkd3 = qkd_driver3.GetConfig([RESOURCE_APPS])

        print(f"QKD1 applications config: {apps_qkd1}")
        print(f"QKD3 applications config: {apps_qkd3}")

        # Debugging: Print the full structure of the apps to understand what is returned
        for app in apps_qkd1:
            print(f"QKD1 App: {app}")
       
        # Debugging: Print the full structure of the apps to understand what is returned
        for app in apps_qkd3:
            print(f"QKD3 App: {app}")

        # Step 4: Validate the applications are created using app_id instead of server_app_id
        assert any(app[1].get('app_id') == '00000001-0001-0000-0000-000000000000' for app in apps_qkd1), "QKD app not created on qkd1."
        assert any(app[1].get('app_id') == '00000003-0001-0000-0000-000000000000' for app in apps_qkd3), "QKD app not created on qkd3."

        print("QKD applications created successfully in both directions.")

    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
    finally:
        qkd_driver1.Disconnect()
        qkd_driver3.Disconnect()
