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
from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from common.proto.simap_connector_pb2 import Affectation
from simap_connector.client.SimapConnectorClient import SimapConnectorClient


LOGGER = logging.getLogger(__name__)


class AffectSampleSynthesizer(Resource):
    # @HTTP_AUTH.login_required
    def post(self):
        if not request.is_json:
            raise UnsupportedMediaType('JSON payload is required')

        request_data = request.json
        LOGGER.debug('[post] Affectation request: {:s}'.format(str(request_data)))

        if 'network_id' not in request_data:
            raise BadRequest('Missing field(network_id)')
        network_id = str(request_data['network_id'])

        if 'link_id' not in request_data:
            raise BadRequest('Missing field(link_id)')
        link_id = str(request_data['link_id'])

        if 'bandwidth_factor' not in request_data:
            raise BadRequest('Missing field(bandwidth_factor)')
        bandwidth_factor = float(request_data['bandwidth_factor'])

        if 'latency_factor' not in request_data:
            raise BadRequest('Missing field(latency_factor)')
        latency_factor = float(request_data['latency_factor'])

        affectation = Affectation()
        affectation.network_id       = network_id
        affectation.link_id          = link_id
        affectation.bandwidth_factor = bandwidth_factor
        affectation.latency_factor   = latency_factor

        simap_connector_client = SimapConnectorClient()
        simap_connector_client.AffectSampleSynthesizer(affectation)
        return jsonify({})
