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

import logging, os
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, ServiceTypeEnum
from common.tools.descriptor.Loader import DescriptorLoader
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from tests.Fixtures import context_client                                       # pylint: disable=unused-import
from tests.tools.mock_osm.MockOSM import MockOSM
from .Fixtures import osm_wim                                                   # pylint: disable=unused-import

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'descriptors_emulated.json')
ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))

def test_service_removal(context_client : ContextClient, osm_wim : MockOSM): # pylint: disable=redefined-outer-name
    # Ensure slices and services are created
    response = context_client.ListSlices(ADMIN_CONTEXT_ID)
    LOGGER.info('Slices[{:d}] = {:s}'.format(len(response.slices), grpc_message_to_json_string(response)))
    assert len(response.slices) == 1 # OSM slice

    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.info('Services[{:d}] = {:s}'.format(len(response.services), grpc_message_to_json_string(response)))
    assert len(response.services) == 3 # 1xL2NM + 2xTAPI

    service_uuids = set()
    for service in response.services:
        service_id = service.service_id
        response = context_client.ListConnections(service_id)
        LOGGER.info('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
            grpc_message_to_json_string(service_id), len(response.connections), grpc_message_to_json_string(response)))

        if service.service_type == ServiceTypeEnum.SERVICETYPE_L2NM:
            assert len(response.connections) == 2 # 2 connections per service (primary + backup)
            service_uuid = service_id.service_uuid.uuid
            service_uuids.add(service_uuid)
            osm_wim.conn_info[service_uuid] = {}
        elif service.service_type == ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE:
            assert len(response.connections) == 1 # 1 connection per service
        else:
            str_service = grpc_message_to_json_string(service)
            raise Exception('Unexpected ServiceType: {:s}'.format(str_service))

    # Identify service to delete
    assert len(service_uuids) == 1  # assume a single L2NM service has been created
    service_uuid = set(service_uuids).pop()

    # Delete Connectivity Service
    osm_wim.delete_connectivity_service(service_uuid)

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0

    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    descriptor_loader.validate()
