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


import logging
from flask.json import jsonify
from flask_restful import Resource, request
from common.proto.context_pb2 import Empty
from common.proto.osm_client_pb2 import CreateRequest, GetRequest, DeleteRequest
from common.tools.grpc.Tools import grpc_message_to_json
from osm_client.client.OsmClient import  OsmClient


LOGGER = logging.getLogger(__name__)


def format_grpc_to_json(grpc_reply):
    return jsonify(grpc_message_to_json(grpc_reply))


class _Resource(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.osm_client = OsmClient()


class NS_Services(_Resource):
    def get(self):
        grpc_response = self.osm_client.NsiList(Empty())
        return format_grpc_to_json(grpc_response)

    def post(self):
        json_requests = request.get_json()
        req = CreateRequest(
            nst_name = json_requests.get('nst_name', ''),
            nsi_name = json_requests.get('nsi_name', ''),
            account  = json_requests.get('account',  ''),
            ssh_key  = json_requests.get('ssh_key',  ''),
            config   = json_requests.get('config',   ''),
        )
        grpc_response = self.osm_client.NsiCreate(req)
        return format_grpc_to_json(grpc_response)


class NS_Service(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.osm_client = OsmClient()

    def get(self, ns_id : str):
        req = GetRequest(id=ns_id)
        resp = self.osm_client.NsiGet(req)
        return format_grpc_to_json(resp)

    def delete(self, ns_id : str):
        req = DeleteRequest(id=ns_id)
        resp = self.osm_client.NsiDelete(req)
        return format_grpc_to_json(resp)
