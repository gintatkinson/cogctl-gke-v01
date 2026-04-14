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

# Enable eventlet for async networking
# NOTE: monkey_patch needs to be executed before importing any other module.
import eventlet
eventlet.monkey_patch()

#pylint: disable=wrong-import-position
import logging
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from tests.tools.mock_osm.MockOSM import MockOSM
from .OSM_Constants import SERVICE_CONNECTION_POINTS_1, SERVICE_CONNECTION_POINTS_2, SERVICE_TYPE
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    nbi_application, osm_wim, context_client
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = 'nbi/tests/data/topology-7router-emu-dummy.json'

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)

def test_prepare_environment(context_client : ContextClient) -> None: # pylint: disable=redefined-outer-name
    validate_empty_scenario(context_client)
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.topology_ids) == 1
    assert len(response.service_ids ) == 0
    assert len(response.slice_ids   ) == 0

def test_create_service(osm_wim : MockOSM): # pylint: disable=redefined-outer-name
    osm_wim.create_connectivity_service(SERVICE_TYPE, SERVICE_CONNECTION_POINTS_1)

def test_get_service_status(osm_wim : MockOSM): # pylint: disable=redefined-outer-name
    service_uuid = list(osm_wim.conn_info.keys())[0] # this test adds a single service
    osm_wim.get_connectivity_service_status(service_uuid)

def test_edit_service(osm_wim : MockOSM): # pylint: disable=redefined-outer-name
    service_uuid = list(osm_wim.conn_info.keys())[0] # this test adds a single service
    osm_wim.edit_connectivity_service(service_uuid, SERVICE_CONNECTION_POINTS_2)

def test_delete_service(osm_wim : MockOSM): # pylint: disable=redefined-outer-name
    service_uuid = list(osm_wim.conn_info.keys())[0] # this test adds a single service
    osm_wim.delete_connectivity_service(service_uuid)

def test_cleanup_environment(context_client : ContextClient) -> None: # pylint: disable=redefined-outer-name
    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.topology_ids) == 1
    assert len(response.service_ids ) == 0
    assert len(response.slice_ids   ) == 0

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    descriptor_loader.validate()
    descriptor_loader.unload()
    validate_empty_scenario(context_client)
