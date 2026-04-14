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

import logging, pytest
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, Service
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from service.client.ServiceClient import ServiceClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = 'src/service/tests/descriptors_recompute_conns.json'
ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))

@pytest.fixture(scope='session')
def context_client():
    _client = ContextClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def device_client():
    _client = DeviceClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def service_client():
    _client = ServiceClient()
    yield _client
    _client.close()


def test_service_recompute_connection(
    context_client : ContextClient, # pylint: disable=redefined-outer-name
    device_client  : DeviceClient,  # pylint: disable=redefined-outer-name
    service_client : ServiceClient, # pylint: disable=redefined-outer-name
) -> None:
    
    # ===== Setup scenario =============================================================================================
    validate_empty_scenario(context_client)

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(
        descriptors_file=DESCRIPTOR_FILE, context_client=context_client, device_client=device_client,
        service_client=service_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()


    # ===== Recompute Connection =======================================================================================
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.info('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
    assert len(response.services) == 1
    service = response.services[0]
    service_id = service.service_id

    response = context_client.ListConnections(service_id)
    LOGGER.info('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
        grpc_message_to_json_string(service_id), len(response.connections), grpc_message_to_json_string(response)))
    assert len(response.connections) == 1 # 1 connection per service
    str_old_connections = grpc_message_to_json_string(response)

    # Change path first time
    request = Service()
    request.CopyFrom(service)
    del request.service_endpoint_ids[:]         # pylint: disable=no-member
    del request.service_constraints[:]          # pylint: disable=no-member
    del request.service_config.config_rules[:]  # pylint: disable=no-member
    service_client.RecomputeConnections(request)

    response = context_client.ListConnections(service_id)
    LOGGER.info('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
        grpc_message_to_json_string(service_id), len(response.connections), grpc_message_to_json_string(response)))
    assert len(response.connections) == 1 # 1 connection per service
    str_new_connections = grpc_message_to_json_string(response)

    assert str_old_connections != str_new_connections

    str_old_connections = str_new_connections

    # Change path second time
    request = Service()
    request.CopyFrom(service)
    del request.service_endpoint_ids[:]         # pylint: disable=no-member
    del request.service_constraints[:]          # pylint: disable=no-member
    del request.service_config.config_rules[:]  # pylint: disable=no-member
    service_client.RecomputeConnections(request)

    response = context_client.ListConnections(service_id)
    LOGGER.info('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
        grpc_message_to_json_string(service_id), len(response.connections), grpc_message_to_json_string(response)))
    assert len(response.connections) == 1 # 1 connection per service
    str_new_connections = grpc_message_to_json_string(response)

    assert str_old_connections != str_new_connections


    # ===== Cleanup scenario ===========================================================================================
    # Validate and unload the base scenario
    descriptor_loader.validate()
    descriptor_loader.unload()
    validate_empty_scenario(context_client)
