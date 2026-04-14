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

from flask import abort, jsonify, make_response, request
from flask_restful import Resource
from .SimapUpdater import SimapUpdater

ETHT_SERVICES = {}

class EthServices(Resource):
    def __init__(self, simap_updater : SimapUpdater):
        super().__init__()
        self._simap_updater = simap_updater

    def get(self):
        etht_services = [etht_service for etht_service in ETHT_SERVICES.values()]
        data = {'ietf-eth-tran-service:etht-svc': {'etht-svc-instances': etht_services}}
        return make_response(jsonify(data), 200)

    def post(self):
        json_request = request.get_json()
        if not json_request: abort(400)
        if not isinstance(json_request, dict): abort(400)
        if 'ietf-eth-tran-service:etht-svc' not in json_request: abort(400)
        json_request = json_request['ietf-eth-tran-service:etht-svc']
        if 'etht-svc-instances' not in json_request: abort(400)
        etht_services = json_request['etht-svc-instances']
        if not isinstance(etht_services, list): abort(400)
        if len(etht_services) != 1: abort(400)
        etht_service = etht_services[0]
        etht_service_name = etht_service['etht-svc-name']
        ETHT_SERVICES[etht_service_name] = etht_service
        self._simap_updater.create_simap_trans_otn(etht_service)
        return make_response(jsonify({}), 201)

class EthService(Resource):
    def __init__(self, simap_updater : SimapUpdater):
        super().__init__()
        self._simap_updater = simap_updater

    def get(self, etht_service_name : str):
        etht_service = ETHT_SERVICES.get(etht_service_name, None)
        data,status = ({}, 404) if etht_service is None else (etht_service, 200)
        return make_response(jsonify(data), status)

    def post(self, etht_service_name : str):
        json_request = request.get_json()
        if not json_request: abort(400)
        if not isinstance(json_request, dict): abort(400)
        if 'ietf-eth-tran-service:etht-svc' not in json_request: abort(400)
        json_request = json_request['ietf-eth-tran-service:etht-svc']
        if 'etht-svc-instances' not in json_request: abort(400)
        etht_services = json_request['etht-svc-instances']
        if not isinstance(etht_services, list): abort(400)
        if len(etht_services) != 1: abort(400)
        etht_service = etht_services[0]
        assert etht_service_name == etht_service['etht-svc-name']
        ETHT_SERVICES[etht_service_name] = etht_service
        self._simap_updater.create_simap_trans_otn(etht_service)
        return make_response(jsonify({}), 201)

    def delete(self, etht_service_name : str):
        etht_service = ETHT_SERVICES.pop(etht_service_name, None)
        data,status = ({}, 404) if etht_service is None else (etht_service, 204)
        self._simap_updater.delete_simap_trans_otn(etht_service_name)
        return make_response(jsonify(data), status)
