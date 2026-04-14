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
from flask import jsonify, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from common.proto.simap_connector_pb2 import Subscription
from nbi.service._tools.Authentication import HTTP_AUTH
from simap_connector.client.SimapConnectorClient import SimapConnectorClient

LOGGER = logging.getLogger(__name__)


class EstablishSubscription(Resource):
    @HTTP_AUTH.login_required
    def post(self):
        if not request.is_json:
            raise UnsupportedMediaType('JSON payload is required')

        request_data = request.json
        LOGGER.debug('[post] Subscription request: {:s}'.format(str(request_data)))

        if 'ietf-subscribed-notifications:input' not in request_data:
            path = 'ietf-subscribed-notifications:input'
            MSG = 'Missing field({:s})'.format(str(path))
            raise BadRequest(MSG)
        input_data = request_data['ietf-subscribed-notifications:input']

        subscription = Subscription()

        if 'datastore' not in input_data:
            path = 'ietf-subscribed-notifications:input/datastore'
            MSG = 'Missing field({:s})'.format(str(path))
            raise BadRequest(MSG)
        subscription.datastore = input_data['datastore']

        if 'ietf-yang-push:datastore-xpath-filter' not in input_data:
            path = 'ietf-subscribed-notifications:input/ietf-yang-push:datastore-xpath-filter'
            MSG = 'Missing field({:s})'.format(str(path))
            raise BadRequest(MSG)
        subscription.xpath_filter = input_data['ietf-yang-push:datastore-xpath-filter']

        if 'ietf-yang-push:periodic' not in input_data:
            path = 'ietf-subscribed-notifications:input/ietf-yang-push:periodic'
            MSG = 'Missing field({:s})'.format(str(path))
            raise BadRequest(MSG)
        periodic = input_data['ietf-yang-push:periodic']

        if 'ietf-yang-push:period' not in periodic:
            path = 'ietf-subscribed-notifications:input/ietf-yang-push:periodic/ietf-yang-push:period'
            MSG = 'Missing field({:s})'.format(str(path))
            raise BadRequest(MSG)
        subscription.period = float(periodic['ietf-yang-push:period'])

        simap_connector_client = SimapConnectorClient()
        subscription_id = simap_connector_client.EstablishSubscription(subscription)
        subscription_id = subscription_id.subscription_id

        subscription_uri = url_for('sse.stream', subscription_id=subscription_id)
        sub_id = {'id': subscription_id, 'uri': subscription_uri}
        return jsonify(sub_id)
