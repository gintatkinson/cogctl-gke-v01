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
import json, logging, pytest
from typing import Dict
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId
from common.tools.descriptor.Loader import (
    DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
)
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from nbi.service.NbiApplication import NbiApplication
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    nbi_application, context_client,
    do_rest_delete_request, do_rest_get_request, do_rest_post_request
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = 'nbi/tests/data/topology-dummy.json'
SVC1_DATA_FILE  = 'nbi/tests/data/ietf_l3vpn_req_svc1.json'
SVC2_DATA_FILE  = 'nbi/tests/data/ietf_l3vpn_req_svc2.json'

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)

@pytest.fixture(scope='session')
def storage() -> Dict:
    yield dict()

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

def test_create_svc1(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    with open(SVC1_DATA_FILE, 'r', encoding='UTF-8') as f:
        svc1_data = json.load(f)
    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services'
    do_rest_post_request(URL, body=svc1_data, logger=LOGGER, expected_status_codes={201})
    storage['svc1-uuid'] = svc1_data['ietf-l3vpn-svc:l3vpn-svc']['vpn-services']['vpn-service'][0]['vpn-id']

def test_create_svc2(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    with open(SVC2_DATA_FILE, 'r', encoding='UTF-8') as f:
        svc2_data = json.load(f)
    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services'
    do_rest_post_request(URL, body=svc2_data, logger=LOGGER, expected_status_codes={201})
    storage['svc2-uuid'] = svc2_data['ietf-l3vpn-svc:l3vpn-svc']['vpn-services']['vpn-service'][0]['vpn-id']

def test_get_state_svc1(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    assert 'svc1-uuid' in storage
    service_uuid = storage['svc1-uuid']
    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service={:s}/'.format(service_uuid)
    do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})

def test_get_state_svc2(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    assert 'svc2-uuid' in storage
    service_uuid = storage['svc2-uuid']
    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service={:s}/'.format(service_uuid)
    do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})

def test_delete_svc1(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    assert 'svc1-uuid' in storage
    service_uuid = storage['svc1-uuid']
    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service={:s}/'.format(service_uuid)
    do_rest_delete_request(URL, logger=LOGGER, expected_status_codes={204})

def test_delete_svc2(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    assert 'svc2-uuid' in storage
    service_uuid = storage['svc2-uuid']
    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service={:s}/'.format(service_uuid)
    do_rest_delete_request(URL, logger=LOGGER, expected_status_codes={204})

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
