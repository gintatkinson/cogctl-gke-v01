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
from common.proto.simap_connector_pb2 import SubscriptionId
from nbi.service._tools.Authentication import HTTP_AUTH
from simap_connector.client.SimapConnectorClient import SimapConnectorClient


LOGGER = logging.getLogger(__name__)


class DeleteSubscription(Resource):
    @HTTP_AUTH.login_required
    def post(self):
        if not request.is_json:
            raise UnsupportedMediaType('JSON payload is required')

        request_data = request.json
        LOGGER.debug('[post] Unsubscription request: {:s}'.format(str(request_data)))

        if 'ietf-subscribed-notifications:input' not in request_data:
            path = 'ietf-subscribed-notifications:input'
            MSG = 'Missing field({:s})'.format(str(path))
            raise BadRequest(MSG)
        input_data = request_data['ietf-subscribed-notifications:input']

        subscription_id = SubscriptionId()

        if 'id' not in input_data:
            path = 'ietf-subscribed-notifications:input/id'
            MSG = 'Missing field({:s})'.format(str(path))
            raise BadRequest(MSG)
        subscription_id.subscription_id = input_data['id']

        simap_connector_client = SimapConnectorClient()
        simap_connector_client.DeleteSubscription(subscription_id)

        return jsonify({})
