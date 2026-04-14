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
from requests.exceptions import HTTPError
from device.service.drivers.qkd.QKDDriver2 import QKDDriver
import requests
from device.service.drivers.qkd.Tools2 import (
    RESOURCE_INTERFACES, 
    RESOURCE_LINKS, 
    RESOURCE_ENDPOINTS, 
    RESOURCE_APPS, 
    RESOURCE_CAPABILITES, 
    RESOURCE_NODE
)

MOCK_QKD_ADDRRESS = '127.0.0.1'
MOCK_PORT = 11111

@pytest.fixture
def qkd_driver():
    # Initialize the QKD driver with the appropriate settings, ensure correct JWT headers are included
    token = "YOUR_JWT_TOKEN"  # Replace with your actual JWT token
    if not token:
        pytest.fail("JWT token is missing. Make sure to generate a valid JWT token.")
    headers = {"Authorization": f"Bearer {token}"}
    return QKDDriver(address=MOCK_QKD_ADDRRESS, port=MOCK_PORT, headers=headers)

# Utility function to print the retrieved data for debugging
def print_data(label, data):
    print(f"{label}: {json.dumps(data, indent=2)}")

# Test ID: SBI_Test_03 (Initial Config Retrieval)
def test_initial_config_retrieval(qkd_driver):
    qkd_driver.Connect()
    
    # Retrieve and validate the initial configuration
    config = qkd_driver.GetInitialConfig()
    
    # Since GetInitialConfig returns a list, adjust the assertions accordingly
    assert isinstance(config, list), "Expected a list for initial config"
    assert len(config) > 0, "Initial config should not be empty"
    
    # Output for debugging
    print_data("Initial Config", config)

# Test ID: INT_LQ_Test_05 (QKD Devices Retrieval)
def test_retrieve_devices(qkd_driver):
    qkd_driver.Connect()
    
    # Retrieve and validate device information
    devices = qkd_driver.GetConfig([RESOURCE_NODE])
    assert isinstance(devices, list), "Expected a list of devices"
    
    if not devices:
        pytest.skip("No devices found in the system. Skipping device test.")
    
    for device in devices:
        assert isinstance(device, tuple), "Each device entry must be a tuple"
        assert isinstance(device[1], dict), "Device data must be a dictionary"
        if isinstance(device[1], Exception):
            pytest.fail(f"Error retrieving devices: {device[1]}")
    
    # Output for debugging
    print_data("Devices", devices)

# Test ID: INT_LQ_Test_04 (QKD Links Retrieval)
def test_retrieve_links(qkd_driver):
    qkd_driver.Connect()

    try:
        # Fetch the links using the correct resource key
        links = qkd_driver.GetConfig([RESOURCE_LINKS])
        assert isinstance(links, list), "Expected a list of tuples (resource key, data)."

        if len(links) == 0:
            pytest.skip("No links found in the system, skipping link validation.")

        for link in links:
            assert isinstance(link, tuple), "Each link entry must be a tuple"
            resource_key, link_data = link  # Unpack the tuple

            # Handle HTTPError or exception in the response
            if isinstance(link_data, requests.exceptions.HTTPError):
                pytest.fail(f"Failed to retrieve links due to HTTP error: {link_data}")
            
            if isinstance(link_data, dict):
                # For real QKD data (links as dictionaries)
                assert 'qkdl_id' in link_data, "Missing 'qkdl_id' in link data"
                assert 'qkdl_local' in link_data, "Missing 'qkdl_local' in link data"
                assert 'qkdl_remote' in link_data, "Missing 'qkdl_remote' in link data"
                assert 'qkdl_type' in link_data, "Missing 'qkdl_type' in link data"

                # Check 'virt_prev_hop' only for virtual links (VIRT)
                if link_data['qkdl_type'] == 'etsi-qkd-node-types:VIRT':
                    virt_prev_hop = link_data.get('virt_prev_hop')
                    assert virt_prev_hop is None or re.match(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', str(virt_prev_hop)), \
                        f"Invalid 'virt_prev_hop': {virt_prev_hop}"

                # Print out the link details for debugging
                print(f"Link ID: {link_data['qkdl_id']}")
                print(f"Link Type: {link_data['qkdl_type']}")
                print(f"Local QKD: {json.dumps(link_data['qkdl_local'], indent=2)}")
                print(f"Remote QKD: {json.dumps(link_data['qkdl_remote'], indent=2)}")

            elif isinstance(link_data, list):
                # For mocked QKD data (links as lists of dictionaries)
                for mock_link in link_data:
                    assert 'uuid' in mock_link, "Missing 'uuid' in mocked link data"
                    assert 'src_qkdn_id' in mock_link, "Missing 'src_qkdn_id' in mocked link data"
                    assert 'dst_qkdn_id' in mock_link, "Missing 'dst_qkdn_id' in mocked link data"

                    # Print out the mocked link details for debugging
                    print(f"Mock Link ID: {mock_link['uuid']}")
                    print(f"Source QKD ID: {mock_link['src_qkdn_id']}")
                    print(f"Destination QKD ID: {mock_link['dst_qkdn_id']}")

            else:
                pytest.fail(f"Unexpected link data format: {type(link_data)}")

    except HTTPError as e:
        pytest.fail(f"HTTP error occurred while retrieving links: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")

# Test for QKD Services
def test_retrieve_services(qkd_driver):
    qkd_driver.Connect()
    services = qkd_driver.GetConfig([RESOURCE_ENDPOINTS])
    assert isinstance(services, list), "Expected a list of services"
    
    if not services:
        pytest.skip("No services found in the system. Skipping service test.")
    
    for service in services:
        assert isinstance(service, tuple), "Each service entry must be a tuple"
        assert isinstance(service[1], dict), "Service data must be a dictionary"
        if isinstance(service[1], Exception):
            pytest.fail(f"Error retrieving services: {service[1]}")
    
    print("Services:", json.dumps(services, indent=2))

# Test ID: INT_LQ_Test_07 (QKD Applications Retrieval)
def test_retrieve_applications(qkd_driver):
    qkd_driver.Connect()
    
    # Retrieve and validate applications information
    applications = qkd_driver.GetConfig([RESOURCE_APPS])  # Adjust to fetch applications using the correct key
    assert isinstance(applications, list), "Expected a list of applications"
    
    if not applications:
        pytest.skip("No applications found in the system. Skipping applications test.")
    
    for app in applications:
        assert isinstance(app, tuple), "Each application entry must be a tuple"
        assert isinstance(app[1], dict), "Application data must be a dictionary"
        if isinstance(app[1], Exception):
            pytest.fail(f"Error retrieving applications: {app[1]}")
    
    # Output for debugging
    print_data("Applications", applications)

# Test ID: INT_LQ_Test_03 (QKD Interfaces Retrieval)
def test_retrieve_interfaces(qkd_driver):
    qkd_driver.Connect()
    
    # Retrieve and validate interface information
    interfaces = qkd_driver.GetConfig([RESOURCE_INTERFACES])
    
    assert isinstance(interfaces, list), "Expected a list of interfaces"
    assert len(interfaces) > 0, "No interfaces found in the system"
    
    for interface in interfaces:
        assert isinstance(interface, tuple), "Each interface entry must be a tuple"
        assert isinstance(interface[1], dict), "Interface data must be a dictionary"
        if isinstance(interface[1], Exception):
            pytest.fail(f"Error retrieving interfaces: {interface[1]}")
    
    # Output for debugging
    print_data("Interfaces", interfaces)

# Test ID: INT_LQ_Test_02 (QKD Capabilities Retrieval)
def test_retrieve_capabilities(qkd_driver):
    qkd_driver.Connect()
    
    # Retrieve and validate capabilities information
    capabilities = qkd_driver.GetConfig([RESOURCE_CAPABILITES])
    
    assert isinstance(capabilities, list), "Expected a list of capabilities"
    assert len(capabilities) > 0, "No capabilities found in the system"
    
    for capability in capabilities:
        assert isinstance(capability, tuple), "Each capability entry must be a tuple"
        assert isinstance(capability[1], dict), "Capability data must be a dictionary"
        if isinstance(capability[1], Exception):
            pytest.fail(f"Error retrieving capabilities: {capability[1]}")
    
    # Output for debugging
    print_data("Capabilities", capabilities)

# Test ID: INT_LQ_Test_03 (QKD Endpoints Retrieval)
def test_retrieve_endpoints(qkd_driver):
    qkd_driver.Connect()
    
    # Retrieve and validate endpoint information
    endpoints = qkd_driver.GetConfig([RESOURCE_ENDPOINTS])
    
    assert isinstance(endpoints, list), "Expected a list of endpoints"
    assert len(endpoints) > 0, "No endpoints found in the system"
    
    for endpoint in endpoints:
        assert isinstance(endpoint, tuple), "Each endpoint entry must be a tuple"
        assert isinstance(endpoint[1], dict), "Endpoint data must be a dictionary"
        if isinstance(endpoint[1], Exception):
            pytest.fail(f"Error retrieving endpoints: {endpoint[1]}")
    
    # Output for debugging
    print_data("Endpoints", endpoints)
