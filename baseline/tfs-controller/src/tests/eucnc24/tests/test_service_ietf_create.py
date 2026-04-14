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

import json, logging, os
from typing import Dict
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, ServiceStatusEnum, ServiceTypeEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from .Fixtures import context_client        # pylint: disable=unused-import
from .Tools import do_rest_get_request, do_rest_post_request


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

REQUEST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'ietf-l3vpn-service.json')
ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))


# pylint: disable=redefined-outer-name, unused-argument
def test_service_ietf_creation(
    context_client : ContextClient,
):
    # Issue service creation request
    with open(REQUEST_FILE, 'r', encoding='UTF-8') as f:
        svc1_data = json.load(f)
    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services'
    do_rest_post_request(URL, body=svc1_data, logger=LOGGER, expected_status_codes={201})
    vpn_id = svc1_data['ietf-l3vpn-svc:l3vpn-svc']['vpn-services']['vpn-service'][0]['vpn-id']

    URL = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service={:s}/'.format(vpn_id)
    service_data = do_rest_get_request(URL, logger=LOGGER, expected_status_codes={200})
    service_uuid = service_data['service-id']

    # Verify service was created
    response = context_client.GetContext(ADMIN_CONTEXT_ID)
    assert len(response.service_ids) == 1
    assert len(response.slice_ids) == 0

    # Check there is 1 service
    response = context_client.ListServices(ADMIN_CONTEXT_ID)
    LOGGER.warning('Services[{:d}] = {:s}'.format(
        len(response.services), grpc_message_to_json_string(response)
    ))
    assert len(response.services) == 1

    for service in response.services:
        service_id = service.service_id
        assert service_id.service_uuid.uuid == service_uuid
        assert service.service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE
        assert service.service_type == ServiceTypeEnum.SERVICETYPE_L3NM

        response = context_client.ListConnections(service_id)
        LOGGER.warning('  ServiceId[{:s}] => Connections[{:d}] = {:s}'.format(
            grpc_message_to_json_string(service_id), len(response.connections),
            grpc_message_to_json_string(response)
        ))
        assert len(response.connections) == 1
