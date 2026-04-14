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

import copy, logging, pytest
from common.Settings import get_setting
from context.client.ContextClient import ContextClient
from context.proto.context_pb2 import Context, ContextId, Device, Empty, Link, Topology
from device.client.DeviceClient import DeviceClient
from .Objects_Domain_1 import D1_CONTEXT_ID, D1_CONTEXTS, D1_DEVICES, D1_LINKS, D1_TOPOLOGIES
from .Objects_Domain_2 import D2_CONTEXT_ID, D2_CONTEXTS, D2_DEVICES, D2_LINKS, D2_TOPOLOGIES

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture(scope='session')
def d1_context_client():
    _client = ContextClient(
        get_setting('D1_CONTEXTSERVICE_SERVICE_HOST'), get_setting('D1_CONTEXTSERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def d1_device_client():
    _client = DeviceClient(
        get_setting('D1_DEVICESERVICE_SERVICE_HOST'), get_setting('D1_DEVICESERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def d2_context_client():
    _client = ContextClient(
        get_setting('D2_CONTEXTSERVICE_SERVICE_HOST'), get_setting('D2_CONTEXTSERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def d2_device_client():
    _client = DeviceClient(
        get_setting('D2_DEVICESERVICE_SERVICE_HOST'), get_setting('D2_DEVICESERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()


def test_scenario_empty(
    d1_context_client : ContextClient,  # pylint: disable=redefined-outer-name
    d2_context_client : ContextClient): # pylint: disable=redefined-outer-name

    def per_domain(context_client):
        response = context_client.ListContexts(Empty())
        assert len(response.contexts) == 0

        response = context_client.ListDevices(Empty())
        assert len(response.devices) == 0

        response = context_client.ListLinks(Empty())
        assert len(response.links) == 0

    # ----- List entities - Ensure database is empty -------------------------------------------------------------------
    per_domain(d1_context_client)
    per_domain(d2_context_client)


def test_prepare_scenario(
    d1_context_client : ContextClient,  # pylint: disable=redefined-outer-name
    d2_context_client : ContextClient): # pylint: disable=redefined-outer-name

    def per_domain(contexts, topologies, context_client):
        for context in contexts:
            context_uuid = context['context_id']['context_uuid']['uuid']
            LOGGER.info('Adding Context {:s}'.format(context_uuid))
            response = context_client.SetContext(Context(**context))
            assert response.context_uuid.uuid == context_uuid

        for topology in topologies:
            context_uuid = topology['topology_id']['context_id']['context_uuid']['uuid']
            topology_uuid = topology['topology_id']['topology_uuid']['uuid']
            LOGGER.info('Adding Topology {:s}/{:s}'.format(context_uuid, topology_uuid))
            response = context_client.SetTopology(Topology(**topology))
            assert response.context_id.context_uuid.uuid == context_uuid
            assert response.topology_uuid.uuid == topology_uuid

    # ----- Create Contexts and Topologies -----------------------------------------------------------------------------
    per_domain(D1_CONTEXTS, D1_TOPOLOGIES, d1_context_client)
    per_domain(D2_CONTEXTS, D2_TOPOLOGIES, d2_context_client)


def test_scenario_ready(
    d1_context_client : ContextClient,  # pylint: disable=redefined-outer-name
    d2_context_client : ContextClient): # pylint: disable=redefined-outer-name

    def per_domain(contexts, topologies, context_id, context_client):
        response = context_client.ListContexts(Empty())
        assert len(response.contexts) == len(contexts)

        response = context_client.ListTopologies(ContextId(**context_id))
        assert len(response.topologies) == len(topologies)

        response = context_client.ListDevices(Empty())
        assert len(response.devices) == 0

        response = context_client.ListLinks(Empty())
        assert len(response.links) == 0

        response = context_client.ListSlices(ContextId(**context_id))
        assert len(response.slices) == 0

        response = context_client.ListServices(ContextId(**context_id))
        assert len(response.services) == 0

    # ----- List entities - Ensure scenario is ready -------------------------------------------------------------------
    per_domain(D1_CONTEXTS, D1_TOPOLOGIES, D1_CONTEXT_ID, d1_context_client)
    per_domain(D2_CONTEXTS, D2_TOPOLOGIES, D2_CONTEXT_ID, d2_context_client)


def test_devices_bootstraping(
    d1_device_client : DeviceClient,    # pylint: disable=redefined-outer-name
    d2_device_client : DeviceClient):   # pylint: disable=redefined-outer-name

    def per_domain(devices, device_client):
        for device, connect_rules in devices:
            device_uuid = device['device_id']['device_uuid']['uuid']
            LOGGER.info('Adding Device {:s}'.format(device_uuid))
            device_with_connect_rules = copy.deepcopy(device)
            device_with_connect_rules['device_config']['config_rules'].extend(connect_rules)
            response = device_client.AddDevice(Device(**device_with_connect_rules))
            assert response.device_uuid.uuid == device_uuid

    # ----- Create Devices and Validate Collected Events ---------------------------------------------------------------
    per_domain(D1_DEVICES, d1_device_client)
    per_domain(D2_DEVICES, d2_device_client)


def test_devices_bootstrapped(
    d1_context_client : ContextClient,  # pylint: disable=redefined-outer-name
    d2_context_client : ContextClient): # pylint: disable=redefined-outer-name

    def per_domain(contexts, topologies, devices, context_id, context_client):
        response = context_client.ListContexts(Empty())
        assert len(response.contexts) == len(contexts)

        response = context_client.ListTopologies(ContextId(**context_id))
        assert len(response.topologies) == len(topologies)

        response = context_client.ListDevices(Empty())
        assert len(response.devices) == len(devices)

        response = context_client.ListLinks(Empty())
        assert len(response.links) == 0

        response = context_client.ListSlices(ContextId(**context_id))
        assert len(response.slices) == 0

        response = context_client.ListServices(ContextId(**context_id))
        assert len(response.services) == 0

    # ----- List entities - Ensure bevices are created -----------------------------------------------------------------
    per_domain(D1_CONTEXTS, D1_TOPOLOGIES, D1_DEVICES, D1_CONTEXT_ID, d1_context_client)
    per_domain(D2_CONTEXTS, D2_TOPOLOGIES, D2_DEVICES, D2_CONTEXT_ID, d2_context_client)


def test_links_creation(
    d1_context_client : ContextClient,  # pylint: disable=redefined-outer-name
    d2_context_client : ContextClient): # pylint: disable=redefined-outer-name

    def per_domain(links, context_client):
        for link in links:
            link_uuid = link['link_id']['link_uuid']['uuid']
            LOGGER.info('Adding Link {:s}'.format(link_uuid))
            response = context_client.SetLink(Link(**link))
            assert response.link_uuid.uuid == link_uuid

    # ----- Create Links and Validate Collected Events -----------------------------------------------------------------
    per_domain(D1_LINKS, d1_context_client)
    per_domain(D2_LINKS, d2_context_client)


def test_links_created(
    d1_context_client : ContextClient,  # pylint: disable=redefined-outer-name
    d2_context_client : ContextClient): # pylint: disable=redefined-outer-name

    def per_domain(contexts, topologies, devices, links, context_id, context_client):
        response = context_client.ListContexts(Empty())
        assert len(response.contexts) == len(contexts)

        response = context_client.ListTopologies(ContextId(**context_id))
        assert len(response.topologies) == len(topologies)

        response = context_client.ListDevices(Empty())
        assert len(response.devices) == len(devices)

        response = context_client.ListLinks(Empty())
        assert len(response.links) == len(links)

        response = context_client.ListSlices(ContextId(**context_id))
        assert len(response.slices) == 0

        response = context_client.ListServices(ContextId(**context_id))
        assert len(response.services) == 0

    # ----- List entities - Ensure links are created -------------------------------------------------------------------
    per_domain(D1_CONTEXTS, D1_TOPOLOGIES, D1_DEVICES, D1_LINKS, D1_CONTEXT_ID, d1_context_client)
    per_domain(D2_CONTEXTS, D2_TOPOLOGIES, D2_DEVICES, D2_LINKS, D2_CONTEXT_ID, d2_context_client)
