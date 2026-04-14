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

import grpc, pytest
from osm_client.client.OsmClient import OsmClient
from common.proto.osm_client_pb2 import CreateRequest, CreateResponse, NsiListResponse
from common.proto.context_pb2 import Empty


from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    osm_client_service, osm_client
)

def test_OsmClient(
    osm_client : OsmClient,
):  # pylint: disable=redefined-outer-name

    nbi_list_request = Empty()

    osm_list_reply = osm_client.NsiList(nbi_list_request)
    assert len(osm_list_reply.id) == 0

    nbi_create_request = CreateRequest()
    nbi_create_request.nst_name = "nst1"
    nbi_create_request.nsi_name = "nsi1"
    nbi_create_request.account = "account1"

    osm_create_reply = osm_client.NsiCreate(nbi_create_request)
    assert osm_create_reply.succeded == True

    osm_list_reply2 = osm_client.NsiList(nbi_list_request)
    assert len(osm_list_reply2.id) == 1
