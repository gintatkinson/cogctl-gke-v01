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
import deepdiff, json, logging, pytest
from typing import Dict
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import ContextId, TopologyId
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from nbi.service.NbiApplication import NbiApplication
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    nbi_application, context_client,
    do_rest_delete_request, do_rest_get_request, do_rest_patch_request, do_rest_post_request, do_rest_put_request
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE  = 'nbi/tests/data/topology-dummy.json'

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)
ADMIN_TOPOLOGY_ID = TopologyId(**json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=JSON_ADMIN_CONTEXT_ID))
BASE_URL = '/restconf/bwm/v1'

@pytest.fixture(scope='session')
def storage() -> Dict:
    yield dict()

#def compare_dicts(dict1, dict2):
#    # Function to recursively sort dictionaries
#    def recursively_sort(d):
#        if isinstance(d, dict):
#            return {k: recursively_sort(v) for k, v in sorted(d.items())}
#        if isinstance(d, list):
#            return [recursively_sort(item) for item in d]
#        return d
#
#    # Sort dictionaries to ignore the order of fields
#    sorted_dict1 = recursively_sort(dict1)
#    sorted_dict2 = recursively_sort(dict2)
#
#    if sorted_dict1 != sorted_dict2:
#        LOGGER.error(sorted_dict1)
#        LOGGER.error(sorted_dict2)
#
#    return sorted_dict1 != sorted_dict2

def check_timestamps(bwm_service):
    assert 'timeStamp' in bwm_service
    assert 'seconds' in bwm_service['timeStamp']
    assert 'nanoseconds' in bwm_service['timeStamp']

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

def test_get_allocations_empty(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    URL = BASE_URL + '/bw_allocations'
    retrieved_data = do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})
    LOGGER.debug('retrieved_data={:s}'.format(json.dumps(retrieved_data, sort_keys=True)))
    assert len(retrieved_data) == 0

def test_allocation(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name
) -> None:
    URL = BASE_URL + '/bw_allocations'
    data = {
        "appInsId"            : "service_uuid_01",
        "allocationDirection" : "00",
        "fixedAllocation"     : "123000.0",
        "fixedBWPriority"     : "SEE_DESCRIPTION",
        "requestType"         : 0,
        "sessionFilter"       : [{
            "sourceIp"   : "192.168.1.2",
            "sourcePort" : ["a"],
            "protocol"   : "string",
            "dstAddress" : "192.168.3.2",
            "dstPort"    : ["b"],
        }]
    }
    retrieved_data = do_rest_post_request(URL, body=data, logger=LOGGER, expected_status_codes={200})
    LOGGER.debug('retrieved_data={:s}'.format(json.dumps(retrieved_data, sort_keys=True)))
    storage['service_uuid_01'] = 'service_uuid_01'


def test_get_allocations(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name
) -> None:
    assert 'service_uuid_01' in storage
    URL = BASE_URL + '/bw_allocations'
    retrieved_data = do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})
    LOGGER.debug('retrieved_data={:s}'.format(json.dumps(retrieved_data, sort_keys=True)))
    assert len(retrieved_data) == 1
    good_result = [
        {
            "appInsId"            : "service_uuid_01",
            "fixedAllocation"     : "123000.0",
            "allocationDirection" : "00",
            "fixedBWPriority"     : "SEE_DESCRIPTION",
            "requestType"         : "0",
            "sessionFilter"       : [{
                "sourceIp"   : "192.168.1.2",
                "sourcePort" : ["a"],
                "protocol"   : "string",
                "dstAddress" : "192.168.3.2",
                "dstPort"    : ["b"],
            }],
        }
    ]
    check_timestamps(retrieved_data[0])
    del retrieved_data[0]['timeStamp']
    diff_data = deepdiff.DeepDiff(good_result, retrieved_data)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0


def test_get_allocation(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name
) -> None:
    assert 'service_uuid_01' in storage
    URL = BASE_URL + '/bw_allocations/service_uuid_01'
    retrieved_data = do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})
    LOGGER.debug('retrieved_data={:s}'.format(json.dumps(retrieved_data, sort_keys=True)))
    good_result = {
        "appInsId"           : "service_uuid_01",
        "fixedAllocation"    : "123000.0",
        "allocationDirection": "00",
        "fixedBWPriority"    : "SEE_DESCRIPTION",
        "requestType"        : "0",
        "sessionFilter"      : [{
            "sourceIp"   : "192.168.1.2",
            "sourcePort" : ["a"],
            "protocol"   : "string",
            "dstAddress" : "192.168.3.2",
            "dstPort"    : ["b"],
        }]
    }
    check_timestamps(retrieved_data)
    del retrieved_data['timeStamp']
    diff_data = deepdiff.DeepDiff(good_result, retrieved_data)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0


def test_put_allocation(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name
) -> None:
    assert 'service_uuid_01' in storage
    URL = BASE_URL + '/bw_allocations/service_uuid_01'
    changed_allocation = {
        "appInsId"           : "service_uuid_01",
        "fixedAllocation"    : "200.0",
        "allocationDirection": "00",
        "fixedBWPriority"    : "NOPRIORITY",
        "requestType"        : "0",
        "sessionFilter"      : [{
            "sourceIp"   : "192.168.1.2",
            "sourcePort" : ["a"],
            "protocol"   : "string",
            "dstAddress" : "192.168.3.2",
            "dstPort"    : ["b"],
        }]
    }
    retrieved_data = do_rest_put_request(URL, body=json.dumps(changed_allocation), logger=LOGGER, expected_status_codes={200})
    check_timestamps(retrieved_data)
    del retrieved_data['timeStamp']
    diff_data = deepdiff.DeepDiff(changed_allocation, retrieved_data)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0


def test_patch_allocation(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name
) -> None:
    assert 'service_uuid_01' in storage
    URL = BASE_URL + '/bw_allocations/service_uuid_01'
    difference = {
        "fixedBWPriority":"FULLPRIORITY",
    }
    changed_allocation = {
        "appInsId"           : "service_uuid_01",
        "fixedAllocation"    : "200.0",
        "allocationDirection": "00",
        "fixedBWPriority"    : "FULLPRIORITY",
        "requestType"        : "0",
        "sessionFilter"      : [{
            "sourceIp"   : "192.168.1.2",
            "sourcePort" : ["a"],
            "protocol"   : "string",
            "dstAddress" : "192.168.3.2",
            "dstPort"    : ["b"],
        }]
    }
    retrieved_data = do_rest_patch_request(URL, body=difference, logger=LOGGER, expected_status_codes={200})
    check_timestamps(retrieved_data)
    del retrieved_data['timeStamp']
    diff_data = deepdiff.DeepDiff(changed_allocation, retrieved_data)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0


def test_delete_allocation(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name
) -> None:
    assert 'service_uuid_01' in storage
    URL = BASE_URL + '/bw_allocations/service_uuid_01'
    do_rest_delete_request(URL, logger=LOGGER, expected_status_codes={200})


def test_get_allocations_empty_final(
    nbi_application : NbiApplication,   # pylint: disable=redefined-outer-name, unused-argument
    storage : Dict                      # pylint: disable=redefined-outer-name, unused-argument
) -> None:
    URL = BASE_URL + '/bw_allocations'
    retrieved_data = do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})
    LOGGER.debug('retrieved_data={:s}'.format(json.dumps(retrieved_data, sort_keys=True)))
    assert len(retrieved_data) == 0


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
