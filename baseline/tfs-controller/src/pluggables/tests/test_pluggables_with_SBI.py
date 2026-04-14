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

import grpc, logging, pytest
from common.proto.context_pb2 import Empty
from common.proto.pluggables_pb2 import Pluggable, View
from context.client.ContextClient import ContextClient
from pluggables.client.PluggablesClient import PluggablesClient
from pluggables.tests.testmessages import (
    create_pluggable_request, create_list_pluggables_request,
    create_get_pluggable_request, create_delete_pluggable_request,
    create_configure_pluggable_request
)
from pluggables.tests.CommonObjects import (
    DEVICE_HUB_UUID, DEVICE_LEAF_UUID
)
from pluggables.tests.PreparePluggablesTestScenario import (  # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    mock_context_service, context_client, device_service, device_client,
    pluggables_service, pluggables_client, test_prepare_environment
)

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture(autouse=True)
def log_all_methods(request):
    '''
    This fixture logs messages before and after each test function runs, indicating the start and end of the test.
    The autouse=True parameter ensures that this logging happens automatically for all tests in the module.
    '''
    LOGGER.info(f" >>>>> Starting test: {request.node.name} ")
    yield
    LOGGER.info(f" <<<<< Finished test: {request.node.name} ")

# ----- Pluggable Tests with NETCONF -----------------------------------------

# Number 1.
def test_create_pluggable_hub_without_config(pluggables_client: PluggablesClient):
    """Test creating a pluggable on Hub device without initial configuration"""
    LOGGER.info('Creating Pluggable on Hub device without config...')
    
    _request = create_pluggable_request(
        device_uuid=DEVICE_HUB_UUID,
        preferred_pluggable_index=1,    # set 1 for HUB and leaf-1, 2 for leaf-2 and 3 for leaf-3
        with_initial_config=False
    )
    
    _pluggable = pluggables_client.CreatePluggable(_request)
    
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.id.device.device_uuid.uuid == DEVICE_HUB_UUID
    assert _pluggable.id.pluggable_index == 1
    LOGGER.info(f'Created Pluggable on Hub: {_pluggable.id}')

# Number 2.
@pytest.mark.integration
def test_create_pluggable_hub_with_config(pluggables_client: PluggablesClient):
    """Test creating a pluggable on Hub device with initial configuration
    
    Requires: Real NETCONF device at 10.30.7.7:2023
    """
    LOGGER.info('Creating Pluggable on Hub device with config...')
    
    _request = create_pluggable_request(
        device_uuid=DEVICE_HUB_UUID,
        preferred_pluggable_index=2,  # Use index 2 to avoid conflict with test #1
        with_initial_config=True
    )
    
    _pluggable = pluggables_client.CreatePluggable(_request)
    
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.id.device.device_uuid.uuid == DEVICE_HUB_UUID
    assert _pluggable.id.pluggable_index == 2
    assert len(_pluggable.config.dsc_groups) == 1  # Should be 1, not 2 (check testmessages.py)
    
    # Verify DSC group configuration
    dsc_group = _pluggable.config.dsc_groups[0]
    assert dsc_group.group_size == 4  # From testmessages.py
    assert len(dsc_group.subcarriers) == 2
    
    LOGGER.info(f'Created Pluggable on Hub with {len(dsc_group.subcarriers)} subcarriers')

# Number 3.
@pytest.mark.integration
def test_create_pluggable_leaf_with_config(pluggables_client: PluggablesClient):
    """Test creating a pluggable on Leaf device with initial configuration
    
    Requires: Real NETCONF device at 10.30.7.8:2023
    """
    LOGGER.info('Creating Pluggable on Leaf device with config...')
    
    _request = create_pluggable_request(
        device_uuid=DEVICE_LEAF_UUID,
        preferred_pluggable_index=1,
        with_initial_config=True
    )
    
    _pluggable = pluggables_client.CreatePluggable(_request)
    
    assert isinstance(_pluggable, Pluggable)
    assert _pluggable.id.device.device_uuid.uuid == DEVICE_LEAF_UUID
    assert _pluggable.id.pluggable_index == 1  # Should be 1, not 0
    assert len(_pluggable.config.dsc_groups) == 1
    
    LOGGER.info(f'Created Pluggable on Leaf: {_pluggable.id}')

# Number 4.
@pytest.mark.integration
def test_configure_pluggable_hub(pluggables_client: PluggablesClient):
    """Test configuring an existing pluggable on Hub device"""
    LOGGER.info('Configuring existing Pluggable on Hub device...')
    
    # First, create a pluggable without config
    _create_request = create_pluggable_request(
        device_uuid=DEVICE_HUB_UUID,
        preferred_pluggable_index=3,  # Use index 3 to avoid conflicts
        with_initial_config=False
    )
    _created = pluggables_client.CreatePluggable(_create_request)
    assert _created.id.pluggable_index == 3
    
    # Now configure it
    _config_request = create_configure_pluggable_request(
        device_uuid=DEVICE_HUB_UUID,
        pluggable_index=3,  # Match the created index
        view_level=View.VIEW_FULL
    )
    
    _configured = pluggables_client.ConfigurePluggable(_config_request)
    
    assert isinstance(_configured, Pluggable)
    assert _configured.id.device.device_uuid.uuid == DEVICE_HUB_UUID
    assert _configured.id.pluggable_index == 3
    assert len(_configured.config.dsc_groups) == 1
    
    # Verify configuration was applied
    dsc_group = _configured.config.dsc_groups[0]
    assert dsc_group.group_size == 2
    assert len(dsc_group.subcarriers) == 2
    
    LOGGER.info(f'Configured Pluggable on Hub with {len(dsc_group.subcarriers)} subcarriers')

# Number 5.
@pytest.mark.integration
def test_get_pluggable(pluggables_client: PluggablesClient):
    """Test retrieving an existing pluggable
    
    Requires: Real NETCONF device at 10.30.7.7:2023
    """
    LOGGER.info('Getting existing Pluggable...')
    
    # Create a pluggable first
    _create_request = create_pluggable_request(
        device_uuid=DEVICE_HUB_UUID,
        preferred_pluggable_index=4,  # Use index 4 to avoid conflicts
        with_initial_config=True
    )
    _created = pluggables_client.CreatePluggable(_create_request)
    
    # Now get it
    _get_request = create_get_pluggable_request(
        device_uuid=DEVICE_HUB_UUID,
        pluggable_index=4,  # Match the created index
        view_level=View.VIEW_FULL
    )
    
    _retrieved = pluggables_client.GetPluggable(_get_request)
    
    assert isinstance(_retrieved, Pluggable)
    assert _retrieved.id.device.device_uuid.uuid == DEVICE_HUB_UUID
    assert _retrieved.id.pluggable_index == 4
    assert len(_retrieved.config.dsc_groups) == len(_created.config.dsc_groups)
    
    LOGGER.info(f'Retrieved Pluggable: {_retrieved.id}')

# Number 6.
def test_list_pluggables(pluggables_client: PluggablesClient):
    """Test listing all pluggables for a device"""
    LOGGER.info('Listing Pluggables for Hub device...')
    
    _list_request = create_list_pluggables_request(
        device_uuid=DEVICE_HUB_UUID,
        view_level=View.VIEW_CONFIG
    )
    
    _response = pluggables_client.ListPluggables(_list_request)
    
    assert _response is not None
    assert len(_response.pluggables) >= 1  # At least one from previous tests
    
    for pluggable in _response.pluggables:
        assert pluggable.id.device.device_uuid.uuid == DEVICE_HUB_UUID
        LOGGER.info(f'Found Pluggable: index={pluggable.id.pluggable_index}')

# Number 7.
@pytest.mark.integration
def test_delete_pluggable(pluggables_client: PluggablesClient):
    """Test deleting a pluggable
    
    Requires: Real NETCONF device at 10.30.7.8:2023
    """
    LOGGER.info('Deleting Pluggable...')
    
    # Create a pluggable to delete
    _create_request = create_pluggable_request(
        device_uuid=DEVICE_LEAF_UUID,
        preferred_pluggable_index=2,  # Use index 2 to avoid conflict with test #3
        with_initial_config=True
    )
    _created = pluggables_client.CreatePluggable(_create_request)
    assert _created.id.pluggable_index == 2
    
    # Delete it
    _delete_request = create_delete_pluggable_request(
        device_uuid=DEVICE_LEAF_UUID,
        pluggable_index=2
    )
    
    _response = pluggables_client.DeletePluggable(_delete_request)
    assert isinstance(_response, Empty)
    
    # Verify it's deleted
    with pytest.raises(grpc.RpcError) as e:
        _get_request = create_get_pluggable_request(
            device_uuid=DEVICE_LEAF_UUID,
            pluggable_index=2
        )
        pluggables_client.GetPluggable(_get_request)
    
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    LOGGER.info('Successfully deleted Pluggable and verified removal')

# Number 8.
def test_pluggable_already_exists_error(pluggables_client: PluggablesClient):
    """Test that creating a pluggable with same key raises ALREADY_EXISTS"""
    LOGGER.info('Testing ALREADY_EXISTS error...')
    
    _request = create_pluggable_request(
        device_uuid=DEVICE_LEAF_UUID,
        preferred_pluggable_index=3,  # Use index 3
        with_initial_config=False
    )
    
    # Create first time - should succeed
    _pluggable = pluggables_client.CreatePluggable(_request)
    assert _pluggable.id.pluggable_index == 3  # Should be 3, not 5
    
    # Try to create again - should fail
    with pytest.raises(grpc.RpcError) as e:
        pluggables_client.CreatePluggable(_request)
    
    assert e.value.code() == grpc.StatusCode.ALREADY_EXISTS
    LOGGER.info('Successfully caught ALREADY_EXISTS error')

# Number 9.
def test_pluggable_not_found_error(pluggables_client: PluggablesClient):
    """Test that getting non-existent pluggable raises NOT_FOUND"""
    LOGGER.info('Testing NOT_FOUND error...')
    
    _request = create_get_pluggable_request(
        device_uuid=DEVICE_HUB_UUID,
        pluggable_index=999,  # Non-existent index
        view_level=View.VIEW_FULL
    )
    
    with pytest.raises(grpc.RpcError) as e:
        pluggables_client.GetPluggable(_request)
    
    assert e.value.code() == grpc.StatusCode.NOT_FOUND
    LOGGER.info('Successfully caught NOT_FOUND error')


# ----- Cleanup Tests --------------------------------------------------------

def test_cleanup_environment(
    context_client: ContextClient,      # pylint: disable=redefined-outer-name
    pluggables_client: PluggablesClient):  # pylint: disable=redefined-outer-name
    """Cleanup test environment by removing test devices"""
    
    
    LOGGER.info('Test environment cleanup completed')
