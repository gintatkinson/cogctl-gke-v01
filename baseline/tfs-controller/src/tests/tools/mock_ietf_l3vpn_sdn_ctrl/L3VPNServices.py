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

# REST-API resource implementing minimal support for "IETF YANG Data Model for Transport Network Client Signals".
# Ref: https://www.ietf.org/archive/id/draft-ietf-ccamp-client-signal-yang-10.html

from flask import jsonify, make_response, request
from flask_restful import Resource

VPN_SERVICES = {}


class L3VPNServices(Resource):
    def get(self):
        return make_response(jsonify(VPN_SERVICES), 200)

    def post(self):
        json_request = request.get_json()
        name = json_request["ietf-l3vpn-svc:l3vpn-svc"]["vpn-services"]["vpn-service"][0]["vpn-id"]
        VPN_SERVICES[name] = json_request
        return make_response(jsonify({}), 201)


class L3VPNService(Resource):
    def put(self, vpn_id: str):
        json_request = request.get_json()
        VPN_SERVICES[vpn_id] = json_request
        return make_response(jsonify({}), 200)

    def delete(self, vpn_id: str):
        slice = VPN_SERVICES.pop(vpn_id, None)
        data, status = ({}, 404) if slice is None else (slice, 204)
        return make_response(jsonify(data), status)
