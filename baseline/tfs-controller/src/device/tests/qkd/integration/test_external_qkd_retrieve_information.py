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
import json
import os
from device.service.drivers.qkd.QKDDriver2 import QKDDriver
from device.service.drivers.qkd.Tools2 import (
    RESOURCE_INTERFACES, 
    RESOURCE_LINKS, 
    RESOURCE_CAPABILITES, 
    RESOURCE_NODE,
    RESOURCE_APPS
)

# Test ID: INT_LQ_Test_01 (QKD Node Authentication)
# Function to retrieve JWT token
def get_jwt_token(node_address, port, username, password):
    """ Retrieve JWT token from a node's login endpoint if it's secured. """
    login_url = f"http://{node_address}:{port}/login"
    payload = {'username': username, 'password': password}
    try:
        print(f"Attempting to retrieve JWT token from {login_url}...")
        response = requests.post(login_url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload)
        response.raise_for_status()
        print(f"Successfully retrieved JWT token from {login_url}")
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve JWT token from {login_url}: {e}")
        return None


# Environment variables for sensitive information
QKD1_ADDRESS = os.getenv("QKD1_ADDRESS")
QKD2_ADDRESS = os.getenv("QKD2_ADDRESS")
PORT = os.getenv("QKD_PORT")
USERNAME = os.getenv("QKD_USERNAME")
PASSWORD = os.getenv("QKD_PASSWORD")

# Pytest fixture to initialize QKDDriver with token for Node 1
@pytest.fixture
def driver_qkd1():
    token = get_jwt_token(QKD1_ADDRESS, PORT, USERNAME, PASSWORD)
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    return QKDDriver(address=QKD1_ADDRESS, port=PORT, headers=headers)

# Pytest fixture to initialize QKDDriver with token for Node 2
@pytest.fixture
def driver_qkd2():
    token = get_jwt_token(QKD2_ADDRESS, PORT, USERNAME, PASSWORD)
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    return QKDDriver(address=QKD2_ADDRESS, port=PORT, headers=headers)

# Utility function to save data to a JSON file, filtering out non-serializable objects
def save_json_file(filename, data):
    serializable_data = filter_serializable(data)
    with open(filename, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    print(f"Saved data to {filename}")

# Function to filter out non-serializable objects like HTTPError
def filter_serializable(data):
    if isinstance(data, list):
        return [filter_serializable(item) for item in data if not isinstance(item, requests.exceptions.RequestException)]
    elif isinstance(data, dict):
        return {key: filter_serializable(value) for key, value in data.items() if not isinstance(value, requests.exceptions.RequestException)}
    return data

# Utility function to print the retrieved data for debugging, handling errors
def print_data(label, data):
    try:
        print(f"{label}: {json.dumps(data, indent=2)}")
    except TypeError as e:
        print(f"Error printing {label}: {e}, Data: {data}")

# General function to retrieve and handle HTTP errors
def retrieve_data(driver_qkd, resource, resource_name):
    try:
        data = driver_qkd.GetConfig([resource])
        assert isinstance(data, list), f"Expected a list for {resource_name}"
        assert len(data) > 0, f"No {resource_name} found in the system"
        return data
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError while fetching {resource_name}: {e}")
        return None
    except AssertionError as e:
        print(f"AssertionError: {e}")
        return None

# Test ID: INT_LQ_Test_02 (QKD Node Capabilities)
def retrieve_capabilities(driver_qkd, node_name):
    capabilities = retrieve_data(driver_qkd, RESOURCE_CAPABILITES, "capabilities")
    if capabilities:
        print_data(f"{node_name} Capabilities", capabilities)
    return capabilities

# Test ID: INT_LQ_Test_03 (QKD Interfaces)
def retrieve_interfaces(driver_qkd, node_name):
    interfaces = retrieve_data(driver_qkd, RESOURCE_INTERFACES, "interfaces")
    if interfaces:
        print_data(f"{node_name} Interfaces", interfaces)
    return interfaces

# Test ID: INT_LQ_Test_04 (QKD Links)
def retrieve_links(driver_qkd, node_name):
    links = retrieve_data(driver_qkd, RESOURCE_LINKS, "links")
    if links:
        print_data(f"{node_name} Links", links)
    return links

# Test ID: INT_LQ_Test_05 (QKD Link Metrics)
def retrieve_link_metrics(driver_qkd, node_name):
    links = retrieve_links(driver_qkd, node_name)
    if links:
        for link in links:
            if 'performance_metrics' in link[1]:
                print_data(f"{node_name} Link Metrics", link[1]['performance_metrics'])
            else:
                print(f"No metrics found for link {link[0]}")
    return links

# Test ID: INT_LQ_Test_06 (QKD Applications)
def retrieve_applications(driver_qkd, node_name):
    applications = retrieve_data(driver_qkd, RESOURCE_APPS, "applications")
    if applications:
        print_data(f"{node_name} Applications", applications)
    return applications

# Test ID: INT_LQ_Test_07 (System Health Check)
def retrieve_node_data(driver_qkd, node_name):
    node_data = retrieve_data(driver_qkd, RESOURCE_NODE, "node data")
    if node_data:
        print_data(f"{node_name} Node Data", node_data)
    return node_data

# Main test to retrieve and save data from QKD1 and QKD2 to files
def test_retrieve_and_save_data(driver_qkd1, driver_qkd2):
    # Retrieve data for QKD1
    qkd1_interfaces = retrieve_interfaces(driver_qkd1, "QKD1")
    qkd1_links = retrieve_links(driver_qkd1, "QKD1")
    qkd1_capabilities = retrieve_capabilities(driver_qkd1, "QKD1")
    qkd1_node_data = retrieve_node_data(driver_qkd1, "QKD1")
    qkd1_apps = retrieve_applications(driver_qkd1, "QKD1")

    qkd1_data = {
        "interfaces": qkd1_interfaces,
        "links": qkd1_links,
        "capabilities": qkd1_capabilities,
        "apps": qkd1_apps,
        "node_data": qkd1_node_data
    }

    # Save QKD1 data to file
    save_json_file('qkd1_data.json', qkd1_data)

    # Retrieve data for QKD2
    qkd2_interfaces = retrieve_interfaces(driver_qkd2, "QKD2")
    qkd2_links = retrieve_links(driver_qkd2, "QKD2")
    qkd2_capabilities = retrieve_capabilities(driver_qkd2, "QKD2")
    qkd2_node_data = retrieve_node_data(driver_qkd2, "QKD2")
    qkd2_apps = retrieve_applications(driver_qkd2, "QKD2")

    qkd2_data = {
        "interfaces": qkd2_interfaces,
        "links": qkd2_links,
        "capabilities": qkd2_capabilities,
        "apps": qkd2_apps,
        "node_data": qkd2_node_data
    }

    # Save QKD2 data to file
    save_json_file('qkd2_data.json', qkd2_data)
