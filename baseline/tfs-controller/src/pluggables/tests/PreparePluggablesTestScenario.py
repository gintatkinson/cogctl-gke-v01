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

import logging, os, pytest
from typing import Union
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC,
    get_env_var_name, get_service_port_grpc
)
from common.proto.context_pb2 import DeviceId, Topology, Context
from common.tools.service.GenericGrpcService import GenericGrpcService
from common.tests.MockServicerImpl_Context import MockServicerImpl_Context
from common.proto.context_pb2_grpc import add_ContextServiceServicer_to_server
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from device.service.DeviceService import DeviceService
from device.service.driver_api.DriverFactory import DriverFactory
from device.service.driver_api.DriverInstanceCache import DriverInstanceCache
from device.service.drivers import DRIVERS
from pluggables.client.PluggablesClient import PluggablesClient
from pluggables.service.PluggablesService import PluggablesService
from pluggables.tests.CommonObjects import (
    DEVICE_HUB, DEVICE_HUB_ID, DEVICE_HUB_UUID, DEVICE_HUB_CONNECT_RULES,
    DEVICE_LEAF, DEVICE_LEAF_ID, DEVICE_LEAF_UUID, DEVICE_LEAF_CONNECT_RULES,
    CONTEXT_ID, CONTEXT, TOPOLOGY_ID, TOPOLOGY,
    get_device_hub_with_connect_rules, get_device_leaf_with_connect_rules
)


LOGGER = logging.getLogger(__name__)

LOCAL_HOST = '127.0.0.1'
MOCKSERVICE_PORT = 10000

# Configure service endpoints
CONTEXT_SERVICE_PORT = MOCKSERVICE_PORT + get_service_port_grpc(ServiceNameEnum.CONTEXT)
DEVICE_SERVICE_PORT = MOCKSERVICE_PORT + get_service_port_grpc(ServiceNameEnum.DEVICE)
PLUGGABLE_SERVICE_PORT = get_service_port_grpc(ServiceNameEnum.PLUGGABLES)

os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST)]         = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC)]    = str(CONTEXT_SERVICE_PORT)
os.environ[get_env_var_name(ServiceNameEnum.DEVICE, ENVVAR_SUFIX_SERVICE_HOST)]          = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.DEVICE, ENVVAR_SUFIX_SERVICE_PORT_GRPC)]     = str(DEVICE_SERVICE_PORT)
os.environ[get_env_var_name(ServiceNameEnum.PLUGGABLES, ENVVAR_SUFIX_SERVICE_HOST)]      = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.PLUGGABLES, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(PLUGGABLE_SERVICE_PORT)


class MockContextService(GenericGrpcService):
    """Mock Context Service for testing"""

    def __init__(self, bind_port: Union[str, int]) -> None:
        super().__init__(bind_port, LOCAL_HOST, enable_health_servicer=False, cls_name='MockContextService')

    def install_servicers(self):
        self.context_servicer = MockServicerImpl_Context()
        add_ContextServiceServicer_to_server(self.context_servicer, self.server)

@pytest.fixture(scope='session')
def mock_context_service():
    """Start mock Context service for the test session"""
    LOGGER.info('Initializing MockContextService...')
    _service = MockContextService(CONTEXT_SERVICE_PORT)
    _service.start()
    yield _service
    LOGGER.info('Terminating MockContextService...')
    _service.stop()


@pytest.fixture(scope='session')
def context_client(mock_context_service):  # pylint: disable=redefined-outer-name
    """Create Context client for the test session"""
    LOGGER.info('Creating ContextClient...')
    _client = ContextClient()
    yield _client
    LOGGER.info('Closing ContextClient...')
    _client.close()

@pytest.fixture(scope='session')
def device_service(context_client : ContextClient):  # pylint: disable=redefined-outer-name
    """Start Device service for the test session"""
    LOGGER.info('Initializing DeviceService...')
    _driver_factory = DriverFactory(DRIVERS)
    _driver_instance_cache = DriverInstanceCache(_driver_factory)
    _service = DeviceService(_driver_instance_cache)
    _service.start()
    yield _service
    LOGGER.info('Terminating DeviceService...')
    _service.stop()

@pytest.fixture(scope='session')
def device_client(device_service: DeviceService):  # pylint: disable=redefined-outer-name
    """Create Device client for the test session"""
    LOGGER.info('Creating DeviceClient...')
    _client = DeviceClient()
    yield _client
    LOGGER.info('Closing DeviceClient...')
    _client.close()


@pytest.fixture(scope='session')
def pluggables_service(context_client: ContextClient):
    """Start Pluggables service for the test session"""
    LOGGER.info('Initializing PluggablesService...')
    _service = PluggablesService()
    _service.start()
    yield _service
    LOGGER.info('Terminating PluggablesService...')
    _service.stop()


@pytest.fixture(scope='session')
def pluggables_client(pluggables_service: PluggablesService,
                      context_client: ContextClient,
                      device_client: DeviceClient
                      ):
    """Create Pluggables client for the test session"""
    LOGGER.info('Creating PluggablesClient...')
    _client = PluggablesClient()
    yield _client
    LOGGER.info('Closing PluggablesClient...')
    _client.close()


def test_prepare_environment(
    context_client: ContextClient,      # pylint: disable=redefined-outer-name
    device_client: DeviceClient,        # pylint: disable=redefined-outer-name
    pluggables_client: PluggablesClient, 
    device_service: DeviceService ):  # pylint: disable=redefined-outer-name
    """Prepare test environment by adding devices to Context"""

    LOGGER.info('Preparing test environment...')


    context_client.SetContext(Context(**CONTEXT))
    context_client.SetTopology(Topology(**TOPOLOGY))
    LOGGER.info('Created admin Context and Topology')

    # Add Hub device with connect rules
    hub_device = get_device_hub_with_connect_rules()
    context_client.SetDevice(hub_device)
    LOGGER.info(f'Added Hub device: {DEVICE_HUB_UUID}')

    # Add Leaf device with connect rules
    leaf_device = get_device_leaf_with_connect_rules()
    context_client.SetDevice(leaf_device)
    LOGGER.info(f'Added Leaf device: {DEVICE_LEAF_UUID}')

    # Verify devices were added
    hub_device_retrieved = context_client.GetDevice(DeviceId(**DEVICE_HUB_ID))
    assert hub_device_retrieved is not None
    assert hub_device_retrieved.device_id.device_uuid.uuid == DEVICE_HUB_UUID
    LOGGER.info(f'Verified Hub device: {hub_device_retrieved.name}')

    leaf_device_retrieved = context_client.GetDevice(DeviceId(**DEVICE_LEAF_ID))
    assert leaf_device_retrieved is not None
    assert leaf_device_retrieved.device_id.device_uuid.uuid == DEVICE_LEAF_UUID
    LOGGER.info(f'Verified Leaf device: {leaf_device_retrieved.name}')
