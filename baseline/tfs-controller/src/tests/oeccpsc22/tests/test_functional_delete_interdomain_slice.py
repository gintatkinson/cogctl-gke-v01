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
from common.DeviceTypes import DeviceTypeEnum
from common.Settings import get_setting
from common.tools.grpc.Tools import grpc_message_to_json_string
from nbi.tests.mock_osm.MockOSM import MockOSM
from context.client.ContextClient import ContextClient
from context.proto.context_pb2 import ContextId, Empty
from .Objects_Domain_1 import D1_CONTEXT_ID, D1_CONTEXTS, D1_DEVICES, D1_LINKS, D1_TOPOLOGIES
from .Objects_Domain_2 import D2_CONTEXT_ID, D2_CONTEXTS, D2_DEVICES, D2_LINKS, D2_TOPOLOGIES
from .Objects_Service import WIM_MAPPING, WIM_PASSWORD, WIM_USERNAME

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DEVTYPE_EMU_PR  = DeviceTypeEnum.EMULATED_PACKET_ROUTER.value
DEVTYPE_EMU_OLS = DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM.value


@pytest.fixture(scope='session')
def d1_context_client():
    _client = ContextClient(
        get_setting('D1_CONTEXTSERVICE_SERVICE_HOST'), get_setting('D1_CONTEXTSERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()


@pytest.fixture(scope='session')
def d2_context_client():
    _client = ContextClient(
        get_setting('D2_CONTEXTSERVICE_SERVICE_HOST'), get_setting('D2_CONTEXTSERVICE_SERVICE_PORT_GRPC'))
    yield _client
    _client.close()


@pytest.fixture(scope='session')
def d1_osm_wim():
    wim_url = 'http://{:s}:{:s}'.format(
        get_setting('D1_NBISERVICE_SERVICE_HOST'), str(get_setting('D1_NBISERVICE_SERVICE_PORT_HTTP')))
    return MockOSM(wim_url, WIM_MAPPING, WIM_USERNAME, WIM_PASSWORD)


def test_interdomain_slice_created(
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

        # TODO: implement validation of number of slices according to the domain they belong
        #response = context_client.ListSlices(ContextId(**context_id))
        #LOGGER.info('Slices[{:d}] = {:s}'.format(len(response.slices), grpc_message_to_json_string(response)))
        #assert len(response.slices) == (2 if D1 else 1)
        # TODO: implement validation that slices are correct

        response = context_client.ListServices(ContextId(**context_id))
        LOGGER.info('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
        assert len(response.services) == 1 # L3NM
        # TODO: improve validation of services created
        for service in response.services:
            service_id = service.service_id
            response = context_client.ListConnections(service_id)
            LOGGER.info('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
                grpc_message_to_json_string(service_id), len(response.connections),
                grpc_message_to_json_string(response)))
            assert len(response.connections) == 1 # one connection per service

    # ----- List entities - Ensure Inter-domain slice is created -------------------------------------------------------
    per_domain(D1_CONTEXTS, D1_TOPOLOGIES, D1_DEVICES, D1_LINKS, D1_CONTEXT_ID, d1_context_client)
    per_domain(D2_CONTEXTS, D2_TOPOLOGIES, D2_DEVICES, D2_LINKS, D2_CONTEXT_ID, d2_context_client)


def test_interdomain_slice_removal(
    d1_context_client : ContextClient,  # pylint: disable=redefined-outer-name
    d1_osm_wim : MockOSM):              # pylint: disable=redefined-outer-name

    # ----- Remove Inter-domain Slice ----------------------------------------------------------------------------------
    # TODO: implement retrieval of inter-domain slice to be deleted
    #response = d1_context_client.ListSliceIds(ContextId(**D1_CONTEXT_ID))
    #LOGGER.info('SliceIds[{:d}] = {:s}'.format(len(response.slice_ids), grpc_message_to_json_string(response)))
    #assert len(response.service_ids) == 2 # L3NM + TAPI
    #service_uuids = set()
    #for service_id in response.service_ids:
    #    service_uuid = service_id.service_uuid.uuid
    #    if service_uuid.endswith(':optical'): continue
    #    service_uuids.add(service_uuid)
    #    osm_wim.conn_info[service_uuid] = {}

    # TODO: implement removal of service
    #assert len(service_uuids) == 1  # assume a single service has been created
    #service_uuid = set(service_uuids).pop()
    #osm_wim.delete_connectivity_service(service_uuid)
    pass


def test_interdomain_slice_removed(
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

    # ----- List entities - Ensure services removed --------------------------------------------------------------------
    per_domain(D1_CONTEXTS, D1_TOPOLOGIES, D1_DEVICES, D1_LINKS, D1_CONTEXT_ID, d1_context_client)
    per_domain(D2_CONTEXTS, D2_TOPOLOGIES, D2_DEVICES, D2_LINKS, D2_CONTEXT_ID, d2_context_client)
