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

APPS = {}


class Apps(Resource):
    def get(self):
        return make_response(jsonify(APPS), 200)

    def post(self):
        json_request = request.get_json()
        name = json_request["application"][0]["name"]
        APPS[name] = json_request
        return make_response(jsonify({}), 201)


class App(Resource):
    def delete(self, app_name: str):
        app_flow = APPS.pop(app_name, None)
        data, status = ({}, 404) if app_flow is None else (app_flow, 204)
        return make_response(jsonify(data), status)
