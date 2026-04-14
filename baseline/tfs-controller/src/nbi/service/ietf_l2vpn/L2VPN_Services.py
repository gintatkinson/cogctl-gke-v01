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
from typing import Dict, List
from flask import request
from flask.json import jsonify
from flask_restful import Resource
from werkzeug.exceptions import UnsupportedMediaType
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import SliceStatusEnum, Slice
from slice.client.SliceClient import SliceClient
from nbi.service._tools.HttpStatusCodes import HTTP_CREATED, HTTP_SERVERERROR
from nbi.service._tools.Validator import validate_message
from nbi.service._tools.Authentication import HTTP_AUTH
from .schemas.vpn_service import SCHEMA_VPN_SERVICE

LOGGER = logging.getLogger(__name__)

class L2VPN_Services(Resource):
    @HTTP_AUTH.login_required
    def get(self):
        return {}

    @HTTP_AUTH.login_required
    def post(self):
        if not request.is_json: raise UnsupportedMediaType('JSON payload is required')
        request_data : Dict = request.json
        LOGGER.debug('Request: {:s}'.format(str(request_data)))
        validate_message(SCHEMA_VPN_SERVICE, request_data)

        vpn_services : List[Dict] = request_data['ietf-l2vpn-svc:vpn-service']
        for vpn_service in vpn_services:
            try:
                # pylint: disable=no-member
                slice_request = Slice()
                slice_request.slice_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
                slice_request.slice_id.slice_uuid.uuid = vpn_service['vpn-id']
                slice_request.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_PLANNED

                slice_client = SliceClient()
                slice_client.CreateSlice(slice_request)

                response = jsonify({})
                response.status_code = HTTP_CREATED
            except Exception as e: # pylint: disable=broad-except
                LOGGER.exception('Something went wrong Creating Service {:s}'.format(str(request)))
                response = jsonify({'error': str(e)})
                response.status_code = HTTP_SERVERERROR
        return response
