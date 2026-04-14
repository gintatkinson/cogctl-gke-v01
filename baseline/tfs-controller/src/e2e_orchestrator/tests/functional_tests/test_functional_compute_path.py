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

import logging, random
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, Empty, ServiceTypeEnum, Service
from common.proto.e2eorchestrator_pb2 import E2EOrchestratorRequest
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.descriptor.Loader import DescriptorLoader
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from service.client.ServiceClient import ServiceClient
from .Fixtures import context_client, device_client, e2eorchestrator_client # pylint: disable=unused-import
from e2e_orchestrator.client.E2EOrchestratorClient import E2EOrchestratorClient
from .Objects import SERVICES
import copy

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

DESCRIPTOR_FILE = 'src/e2e_orchestrator/tests/descriptors_emulated.json'
ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))


def test_orchestration(context_client : ContextClient, e2eorchestrator_client : E2EOrchestratorClient): # pylint: disable=redefined-outer-name
    # Load descriptors and validate the base scenario
    descriptor_loader = DescriptorLoader(descriptors_file=DESCRIPTOR_FILE, context_client=context_client)
    descriptor_loader.validate()

    # Verify the scenario has no services/slices
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 0
    assert len(response.slice_ids) == 0



    # ----- Compute E2E path ---------------------------------------------------------------
    for service, endpoints in SERVICES:
        service_uuid = service['service_id']['service_uuid']['uuid']
        print('Creating Service {:s}'.format(service_uuid))
        service_p4 = copy.deepcopy(service)
        service_p4['service_endpoint_ids'].extend(endpoints)

        request = E2EOrchestratorRequest()
        request.service.MergeFrom(Service(**service_p4))
        reply = e2eorchestrator_client.Compute(request)
        LOGGER.info(reply)
        assert len(reply.connections) == 6

