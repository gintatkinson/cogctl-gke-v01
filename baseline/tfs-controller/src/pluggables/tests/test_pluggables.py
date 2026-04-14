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


import grpc
import os, pytest
import logging
from typing import Union

from common.proto.context_pb2 import  Empty
from common.Constants import ServiceNameEnum
from common.Settings import ( 
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, 
    get_env_var_name, get_service_port_grpc)
from common.tests.MockServicerImpl_Context import MockServicerImpl_Context
from common.proto.context_pb2_grpc import add_ContextServiceServicer_to_server
from common.proto.pluggables_pb2 import (
    PluggableId, Pluggable, ListPluggablesResponse, View
)
from common.tools.service.GenericGrpcService import GenericGrpcService
from pluggables.client.PluggablesClient import PluggablesClient
from pluggables.service.PluggablesService import PluggablesService
from pluggables.tests.testmessages import (
    create_pluggable_request, create_list_pluggables_request,
    create_get_pluggable_request, create_delete_pluggable_request,
    create_configure_pluggable_request,
)


###########################
# Tests Setup
###########################

LOCAL_HOST = '127.0.0.1'

DSCMPLUGGABLE_SERVICE_PORT = get_service_port_grpc(ServiceNameEnum.PLUGGABLES)  # type: ignore
os.environ[get_env_var_name(ServiceNameEnum.PLUGGABLES, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.PLUGGABLES, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(DSCMPLUGGABLE_SERVICE_PORT)

LOGGER = logging.getLogger(__name__)

class MockContextService(GenericGrpcService):
    # Mock Service implementing Context to simplify unitary tests of DSCM pluggables

    def __init__(self, bind_port: Union[str, int]) -> None:
        super().__init__(bind_port, LOCAL_HOST, enable_health_servicer=False, cls_name='MockService')

    # pylint: disable=attribute-defined-outside-init
    def install_servicers(self):
        self.context_servicer = MockServicerImpl_Context()
        add_ContextServiceServicer_to_server(self.context_servicer, self.server)

# This fixture will be requested by test cases and last during testing session
@pytest.fixture(scope='session')
def pluggables_service():
    LOGGER.info('Initializing PluggableService...')
    _service = PluggablesService()
    _service.start()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding PluggableService...')
    yield _service

    LOGGER.info('Terminating PluggableService...')
    _service.stop()

    LOGGER.info('Terminated PluggableService...')

@pytest.fixture(scope='function')
def pluggable_client(pluggables_service : PluggablesService):
    LOGGER.info('Creating PluggablesClient...')
    _client = PluggablesClient()

    LOGGER.info('Yielding PluggablesClient...')
    yield _client

    LOGGER.info('Closing PluggablesClient...')
    _client.close()

    LOGGER.info('Closed PluggablesClient...')

@pytest.fixture(autouse=True)
def log_all_methods(request):
    '''
    This fixture logs messages before and after each test function runs, indicating the start and end of the test.
    The autouse=True parameter ensures that this logging happens automatically for all tests in the module.
    '''
    LOGGER.info(f" >>>>> Starting test: {request.node.name} ")
    yield
    LOGGER.info(f" <<<<< Finished test: {request.node.name} ")

########################### 
# Test Cases
###########################

# CreatePluggable Test without configuration
def test_CreatePluggable(pluggable_client : PluggablesClient):
    LOGGER.info('Creating Pluggable for test...')
    _pluggable_request = create_pluggable_request(preferred_pluggable_index=-1)
    _pluggable         = pluggable_client.CreatePluggable(_pluggable_request)
    LOGGER.info('Created Pluggable for test: %s', _pluggable)
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.id.pluggable_index         == _pluggable_request.preferred_pluggable_index
    assert _pluggable.id.device.device_uuid.uuid == _pluggable_request.device.device_uuid.uuid


# CreatePluggable Test with configuration
def test_CreatePluggable_with_config(pluggable_client : PluggablesClient):
    LOGGER.info('Creating Pluggable with initial configuration for test...')
    _pluggable_request = create_pluggable_request(
                            device_uuid               = "9bbf1937-db9e-45bc-b2c6-3214a9d42157",
                            preferred_pluggable_index = -1,
                            with_initial_config       = True)
    _pluggable         = pluggable_client.CreatePluggable(_pluggable_request)
    LOGGER.info('Created Pluggable with initial configuration for test: %s', _pluggable)
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.id.pluggable_index         == _pluggable_request.preferred_pluggable_index
    assert _pluggable.id.device.device_uuid.uuid == _pluggable_request.device.device_uuid.uuid
    assert _pluggable.config is not None
    assert len(_pluggable.config.dsc_groups) == 1
    dsc_group = _pluggable.config.dsc_groups[0]
    assert dsc_group.group_size == 4
    assert len(dsc_group.subcarriers) == 2

# create pluggable request with pluggable key already exists error
def test_CreatePluggable_already_exists(pluggable_client : PluggablesClient):
    LOGGER.info('Creating Pluggable for test...')
    _pluggable_request = create_pluggable_request(preferred_pluggable_index=5)
    _pluggable         = pluggable_client.CreatePluggable(_pluggable_request)
    LOGGER.info('Created Pluggable for test: %s', _pluggable)
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.id.pluggable_index         == _pluggable_request.preferred_pluggable_index
    assert _pluggable.id.device.device_uuid.uuid == _pluggable_request.device.device_uuid.uuid
    # Try to create the same pluggable again, should raise ALREADY_EXISTS
    with pytest.raises(grpc.RpcError) as e:
        pluggable_client.CreatePluggable(_pluggable_request)
    assert e.value.code() == grpc.StatusCode.ALREADY_EXISTS

# ListPluggables Test
def test_ListPluggables(pluggable_client : PluggablesClient):
    LOGGER.info('Listing Pluggables for test...')
    _list_request = create_list_pluggables_request(
                        view_level = View.VIEW_CONFIG       # View.VIEW_STATE
    )
    _pluggables   = pluggable_client.ListPluggables(_list_request)
    LOGGER.info('Listed Pluggables for test: %s', _pluggables)
    assert isinstance(_pluggables, ListPluggablesResponse)
    if len(_pluggables.pluggables) != 0:
        assert len(_pluggables.pluggables) >= 1
        for p in _pluggables.pluggables:
            assert isinstance(p, Pluggable)
            assert isinstance(p.id, PluggableId)
    else:
        assert len(_pluggables.pluggables) == 0

# GetPluggable Test
def test_GetPluggable(pluggable_client : PluggablesClient):
    LOGGER.info('Starting GetPluggable test...')
    LOGGER.info('Getting Pluggable for test...')
    # First create a pluggable to get it later
    _pluggable_request = create_pluggable_request(preferred_pluggable_index=1)
    _created_pluggable = pluggable_client.CreatePluggable(_pluggable_request)
    LOGGER.info('Created Pluggable for GetPluggable test: %s', _created_pluggable)

    _get_request = create_get_pluggable_request(
                        device_uuid       = _created_pluggable.id.device.device_uuid.uuid,
                        pluggable_index   = _created_pluggable.id.pluggable_index,
                        view_level        = View.VIEW_FULL
    )
    _pluggable   = pluggable_client.GetPluggable(_get_request)
    LOGGER.info('Got Pluggable for test: %s', _pluggable)
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.id.pluggable_index         == _created_pluggable.id.pluggable_index
    assert _pluggable.id.device.device_uuid.uuid == _created_pluggable.id.device.device_uuid.uuid


# DeletePluggable Test
def test_DeletePluggable(pluggable_client : PluggablesClient):
    LOGGER.info('Starting DeletePluggable test...')
    LOGGER.info('Creating Pluggable to delete for test...')

    # First create a pluggable to delete it later
    _pluggable_request = create_pluggable_request(preferred_pluggable_index=2)
    _created_pluggable = pluggable_client.CreatePluggable(_pluggable_request)
    LOGGER.info('Created Pluggable to delete for test: %s', _created_pluggable)

    _delete_request = create_delete_pluggable_request(
                        device_uuid       = _created_pluggable.id.device.device_uuid.uuid,
                        pluggable_index   = _created_pluggable.id.pluggable_index
    )
    _response       = pluggable_client.DeletePluggable(_delete_request)
    LOGGER.info('Deleted Pluggable for test, response: %s', _response)
    assert isinstance(_response, Empty)

    # Try to get the deleted pluggable, should raise NOT_FOUND
    with pytest.raises(grpc.RpcError) as e:
        pluggable_client.GetPluggable(
            create_get_pluggable_request(
                device_uuid     = _created_pluggable.id.device.device_uuid.uuid,
                pluggable_index = _created_pluggable.id.pluggable_index
            )
        )
    assert e.value.code() == grpc.StatusCode.NOT_FOUND

# ConfigurePluggable Test
def test_ConfigurePluggable(pluggable_client : PluggablesClient):
    LOGGER.info('Starting ConfigurePluggable test...')
    LOGGER.info('Creating Pluggable to configure for test...')

    # First create a pluggable to configure it later
    _pluggable_request = create_pluggable_request(preferred_pluggable_index=3)
    _created_pluggable = pluggable_client.CreatePluggable(_pluggable_request)
    LOGGER.info('Created Pluggable to configure for test: %s', _created_pluggable)

    _configure_request = create_configure_pluggable_request(
                            device_uuid       = _created_pluggable.id.device.device_uuid.uuid,
                            pluggable_index   = _created_pluggable.id.pluggable_index,
    )
    _pluggable         = pluggable_client.ConfigurePluggable(_configure_request)
    LOGGER.info('Configured Pluggable for test: %s', _pluggable)
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.config is not None
    assert len(_pluggable.config.dsc_groups) == 1
    dsc_group = _pluggable.config.dsc_groups[0]
    assert dsc_group.group_size == 2
    assert len(dsc_group.subcarriers) == 2
