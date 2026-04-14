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

import logging, pytest, time
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, Empty
from common.proto.context_pb2 import ConfigActionEnum, Device, DeviceId
from common.tools.descriptor.Loader import DescriptorLoader, check_descriptor_load_results, validate_empty_scenario
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from interdomain.service.topology_abstractor.TopologyAbstractor import TopologyAbstractor

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

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
def topology_abstractor():
    _topology_abstractor = TopologyAbstractor()
    _topology_abstractor.start()
    yield _topology_abstractor
    _topology_abstractor.stop()
    _topology_abstractor.join()

def test_pre_cleanup_scenario(
    context_client : ContextClient,             # pylint: disable=redefined-outer-name
    device_client : DeviceClient,               # pylint: disable=redefined-outer-name
) -> None:
    for link_id in context_client.ListLinkIds(Empty()).link_ids: context_client.RemoveLink(link_id)
    for device_id in context_client.ListDeviceIds(Empty()).device_ids: device_client.DeleteDevice(device_id)

    contexts = context_client.ListContexts(Empty())
    for context in contexts.contexts:
        assert len(context.slice_ids) == 0, 'Found Slices: {:s}'.format(grpc_message_to_json_string(context))
        assert len(context.service_ids) == 0, 'Found Services: {:s}'.format(grpc_message_to_json_string(context))
        for topology_id in context.topology_ids: context_client.RemoveTopology(topology_id)
        context_client.RemoveContext(context.context_id)

DESCRIPTOR_FILE = 'oeccpsc22/descriptors/domain1.json'
#DESCRIPTOR_FILE = 'oeccpsc22/descriptors/domain2.json'

def test_interdomain_topology_abstractor(
    context_client : ContextClient,             # pylint: disable=redefined-outer-name
    device_client : DeviceClient,               # pylint: disable=redefined-outer-name
    topology_abstractor : TopologyAbstractor,   # pylint: disable=redefined-outer-name
) -> None:
    #validate_empty_scenario(context_client)

    time.sleep(3)

    descriptor_loader = DescriptorLoader(
        descriptors_file=DESCRIPTOR_FILE, context_client=context_client, device_client=device_client)
    results = descriptor_loader.process()
    check_descriptor_load_results(results, descriptor_loader)
    #descriptor_loader.validate()

    time.sleep(3)

    LOGGER.warning('real_to_abstract_device_uuid={:s}'.format(str(topology_abstractor.real_to_abstract_device_uuid)))
    LOGGER.warning('real_to_abstract_link_uuid={:s}'.format(str(topology_abstractor.real_to_abstract_link_uuid)))

    LOGGER.warning('abstract_device_to_topology_id={:s}'.format(str(topology_abstractor.abstract_device_to_topology_id)))
    LOGGER.warning('abstract_link_to_topology_id={:s}'.format(str(topology_abstractor.abstract_link_to_topology_id)))

    LOGGER.warning('abstract_devices={:s}'.format(str({
        k:v.to_json()
        for k,v in topology_abstractor.abstract_devices.items()
    })))
    LOGGER.warning('abstract_links={:s}'.format(str({
        k:v.to_json()
        for k,v in topology_abstractor.abstract_links.items()
    })))

    raise Exception()


#def test_post_cleanup_scenario(
#    context_client : ContextClient,             # pylint: disable=redefined-outer-name
#    device_client : DeviceClient,               # pylint: disable=redefined-outer-name
#) -> None:
#    test_pre_cleanup_scenario(context_client, device_client)
