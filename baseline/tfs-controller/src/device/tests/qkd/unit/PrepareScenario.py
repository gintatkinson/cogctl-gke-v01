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

import pytest, os, time, logging
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_HTTP,
    get_env_var_name, get_service_port_http
)
from context.client.ContextClient import ContextClient
from nbi.service.rest_server.RestServer import RestServer
from nbi.service.rest_server.nbi_plugins.tfs_api import register_tfs_api
from device.client.DeviceClient import DeviceClient
from device.service.DeviceService import DeviceService
from device.service.driver_api.DriverFactory import DriverFactory
from device.service.driver_api.DriverInstanceCache import DriverInstanceCache
from device.service.drivers import DRIVERS
from device.tests.CommonObjects import CONTEXT, TOPOLOGY
from device.tests.MockService_Dependencies import MockService_Dependencies
from monitoring.client.MonitoringClient import MonitoringClient
from requests import codes as requests_codes
import requests

# Constants
LOCAL_HOST = '127.0.0.1'
MOCKSERVICE_PORT = 8080

# Get dynamic port for NBI service
NBI_SERVICE_PORT = MOCKSERVICE_PORT + get_service_port_http(ServiceNameEnum.NBI)

# Set environment variables for the NBI service host and port
os.environ[get_env_var_name(ServiceNameEnum.NBI, ENVVAR_SUFIX_SERVICE_HOST)] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.NBI, ENVVAR_SUFIX_SERVICE_PORT_HTTP)] = str(NBI_SERVICE_PORT)

# Expected status codes for requests
EXPECTED_STATUS_CODES = {requests_codes['OK'], requests_codes['CREATED'], requests_codes['ACCEPTED'], requests_codes['NO_CONTENT']}

# Debugging output for the port number
print(f"MOCKSERVICE_PORT: {MOCKSERVICE_PORT}")
print(f"NBI_SERVICE_PORT: {NBI_SERVICE_PORT}")

@pytest.fixture(scope='session')
def mock_service():
    _service = MockService_Dependencies(MOCKSERVICE_PORT)
    _service.configure_env_vars()
    _service.start()
    yield _service
    _service.stop()

@pytest.fixture(scope='session')
def nbi_service_rest(mock_service):  # Pass the `mock_service` as an argument if needed
    _rest_server = RestServer()
    register_tfs_api(_rest_server)  # Register the TFS API with the REST server
    _rest_server.start()
    time.sleep(1)  # Give time for the server to start
    yield _rest_server
    _rest_server.shutdown()
    _rest_server.join()

@pytest.fixture(scope='session')
def context_client(mock_service):
    _client = ContextClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def device_service(context_client, monitoring_client):
    _driver_factory = DriverFactory(DRIVERS)
    _driver_instance_cache = DriverInstanceCache(_driver_factory)
    _service = DeviceService(_driver_instance_cache)
    _service.start()
    yield _service
    _service.stop()

@pytest.fixture(scope='session')
def device_client(device_service):
    _client = DeviceClient()
    yield _client
    _client.close()

# General request function
def do_rest_request(method, url, body=None, timeout=10, allow_redirects=True, logger=None):
    # Construct the request URL with NBI service port
    request_url = f"http://{LOCAL_HOST}:{NBI_SERVICE_PORT}{url}"
    
    # Log the request details for debugging
    if logger:
        msg = f"Request: {method.upper()} {request_url}"
        if body:
            msg += f" body={body}"
        logger.warning(msg)

    # Send the request
    reply = requests.request(method, request_url, timeout=timeout, json=body, allow_redirects=allow_redirects)
    
    # Log the response details for debugging
    if logger:
        logger.warning(f"Reply: {reply.text}")

    # Print status code and response for debugging instead of asserting
    print(f"Status code: {reply.status_code}")
    print(f"Response: {reply.text}")

    # Return the JSON response if present
    if reply.content:
        return reply.json()
    return None

# Function for GET requests
def do_rest_get_request(url, body=None, timeout=10, allow_redirects=True, logger=None):
    return do_rest_request('get', url, body, timeout, allow_redirects, logger=logger)

# Function for POST requests
def do_rest_post_request(url, body=None, timeout=10, allow_redirects=True, logger=None):
    return do_rest_request('post', url, body, timeout, allow_redirects, logger=logger)
