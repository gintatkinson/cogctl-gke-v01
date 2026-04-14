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

# REST-API resource implementing minimal support for "IETF YANG Data Model for Traffic Engineering Tunnels,
# Label Switched Paths and Interfaces".
# Ref: https://www.ietf.org/archive/id/draft-ietf-teas-yang-te-34.html


from flask import abort, jsonify, make_response, request
from flask_restful import Resource

OSU_TUNNELS = {}

class OsuTunnels(Resource):
    def get(self):
        osu_tunnels = [osu_tunnel for osu_tunnel in OSU_TUNNELS.values()]
        data = {'ietf-te:tunnel': osu_tunnels}
        return make_response(jsonify(data), 200)

    def post(self):
        json_request = request.get_json()
        if not json_request: abort(400)
        if not isinstance(json_request, dict): abort(400)
        if 'ietf-te:tunnel' not in json_request: abort(400)
        osu_tunnels = json_request['ietf-te:tunnel']
        if not isinstance(osu_tunnels, list): abort(400)
        if len(osu_tunnels) != 1: abort(400)
        osu_tunnel = osu_tunnels[0]
        osu_tunnel_name = osu_tunnel['name']
        OSU_TUNNELS[osu_tunnel_name] = osu_tunnel
        return make_response(jsonify({}), 201)

class OsuTunnel(Resource):
    def get(self, osu_tunnel_name : str):
        osu_tunnel = OSU_TUNNELS.get(osu_tunnel_name, None)
        data,status = ({}, 404) if osu_tunnel is None else (osu_tunnel, 200)
        return make_response(jsonify(data), status)

    def delete(self, osu_tunnel_name : str):
        osu_tunnel = OSU_TUNNELS.pop(osu_tunnel_name, None)
        data,status = ({}, 404) if osu_tunnel is None else (osu_tunnel, 204)
        return make_response(jsonify(data), status)
