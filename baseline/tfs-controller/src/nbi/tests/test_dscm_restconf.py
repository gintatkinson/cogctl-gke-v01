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

from typing import Union
import logging
import os, pytest
import requests
from .DSCM_MockWebServer import nbi_service_rest
from .messages.dscm_messages import get_hub_payload, get_leaf_payload
from common.Constants import ServiceNameEnum
from common.proto.context_pb2_grpc import add_ContextServiceServicer_to_server
from common.Settings import (
        ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, 
    get_env_var_name, get_service_port_grpc)
from common.tests.MockServicerImpl_Context import MockServicerImpl_Context
from common.tools.service.GenericGrpcService import GenericGrpcService
from pluggables.client.PluggablesClient import PluggablesClient
from pluggables.service.PluggablesService import PluggablesService


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

BASE_URL = "http://127.0.0.1:18080/restconf/data/"
HEADERS = { "Accept"      : "application/yang-data+json",
            "Content-Type": "application/yang-data+json" }

###########################
# Tests Setup
###########################

LOCAL_HOST = '127.0.0.1'

DSCMPLUGGABLE_SERVICE_PORT = get_service_port_grpc(ServiceNameEnum.DSCMPLUGGABLE)  
os.environ[get_env_var_name(ServiceNameEnum.DSCMPLUGGABLE, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.DSCMPLUGGABLE, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(DSCMPLUGGABLE_SERVICE_PORT)

class MockContextService(GenericGrpcService):
    def __init__(self, bind_port: Union[str, int]) -> None:
        super().__init__(bind_port, LOCAL_HOST, enable_health_servicer=False, cls_name='MockService')

    def install_servicers(self):
        self.context_servicer = MockServicerImpl_Context()
        add_ContextServiceServicer_to_server(self.context_servicer, self.server)


@pytest.fixture(scope='session')
def pluggables_service():
    LOGGER.info('Initializing DscmPluggableService...')
    _service = PluggablesService()
    _service.start()

    LOGGER.info('Yielding DscmPluggableService...')
    yield _service

    LOGGER.info('Terminating DscmPluggableService...')
    _service.stop()
    LOGGER.info('Terminated DscmPluggableService...')

@pytest.fixture(scope='function')
def dscm_pluggable_client(pluggables_service : PluggablesService):
    LOGGER.info('Creating PluggablesClient...')
    _client = PluggablesClient()

    LOGGER.info('Yielding PluggablesClient...')
    yield _client

    LOGGER.info('Closing PluggablesClient...')
    _client.close()
    LOGGER.info('Closed PluggablesClient...')

@pytest.fixture(autouse=True)
def log_each(request):
    LOGGER.info(f">>>>>> START {request.node.name} >>>>>>")
    yield
    LOGGER.info(f"<<<<<< END   {request.node.name} <<<<<<")

def test_post_hub_optical_channel_frequency(nbi_service_rest, dscm_pluggable_client: PluggablesClient):
    """Test PATCH to update optical channel frequency."""
    device = "device=T1.1/"
    encoded_path = f"{device}openconfig-platform:components/component=1/optical-channel/config"
    
    post_data = get_hub_payload()
    response = requests.post(f"{BASE_URL}{encoded_path}", 
                            json=post_data, 
                            headers=HEADERS)
    assert response.status_code == 201

def test_post_get_delete_leaf_optical_channel_frequency(nbi_service_rest, dscm_pluggable_client: PluggablesClient):
    """Test POST, GET, DELETE to manage optical channel frequency for leaf device."""
    device = "device=T1.2/"
    encoded_path = f"{device}openconfig-platform:components/component=1/optical-channel/config"
    
    # Step 1: POST to create a new device configuration
    post_data = get_leaf_payload()
    response = requests.post(f"{BASE_URL}{encoded_path}", 
                            json=post_data, 
                            headers=HEADERS)
    assert response.status_code == 201

    # Step 2: GET to retrieve the created device configuration
    response = requests.get(f"{BASE_URL}{encoded_path}", headers={"Accept": "application/yang-data+json"})
    assert response.status_code == 200
    get_data = response.json()
    assert get_data is not None

    # Step 3: DELETE to remove the created device configuration
    response = requests.delete(f"{BASE_URL}{encoded_path}", headers={"Accept": "application/yang-data+json"})
    assert response.status_code == 204

    # Step 4: GET again to verify the device configuration has been deleted
    response = requests.get(f"{BASE_URL}{encoded_path}", headers={"Accept": "application/yang-data+json"})
    assert response.status_code == 400  # Assuming 400 is returned for non-existing resource
