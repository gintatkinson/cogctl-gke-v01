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
import deepdiff, json, logging, operator, os
from typing import Dict
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId
from common.tools.descriptor.Loader import (
    DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
)
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from nbi.service.NbiApplication import NbiApplication

# Explicitly state NBI to use PyangBind Renderer for this test
os.environ['IETF_NETWORK_RENDERER'] = 'PYANGBIND'

from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    nbi_application, context_client,
    do_rest_get_request
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE  = 'nbi/tests/data/topology-dummy.json'
TARGET_DATA_FILE = 'nbi/tests/data/test-ietf-network.json'

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

def sort_data(data : Dict) -> None:
    if 'ietf-network:networks' not in data: return
    if 'network' not in data['ietf-network:networks']: return
    data['ietf-network:networks']['network'] = sorted(
        data['ietf-network:networks']['network'],
        key=operator.itemgetter('network-id')
    )
    for network in data['ietf-network:networks']['network']:
        if 'node' in network:
            network['node'] = sorted(
                network['node'],
                key=operator.itemgetter('node-id')
            )

            for node in network['node']:
                if 'ietf-network-topology:termination-point' in node:
                    node['ietf-network-topology:termination-point'] = sorted(
                        node['ietf-network-topology:termination-point'],
                        key=operator.itemgetter('tp-id')
                    )

        if 'ietf-network-topology:link' in network:
            network['ietf-network-topology:link'] = sorted(
                network['ietf-network-topology:link'],
                key=operator.itemgetter('link-id')
            )

def test_rest_get_networks(
    nbi_application : NbiApplication    # pylint: disable=redefined-outer-name
) -> None:
    with open(TARGET_DATA_FILE, 'r', encoding='UTF-8') as f:
        target_data = json.load(f)
    URL = '/restconf/data/ietf-network:networks'
    retrieved_data = do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})
    sort_data(retrieved_data)
    sort_data(target_data)
    diff_data = deepdiff.DeepDiff(target_data, retrieved_data)
    LOGGER.error('Differences:\n{:s}'.format(str(diff_data.pretty())))
    assert len(diff_data) == 0

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
