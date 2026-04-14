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
from typing import Dict

from flask import request
from flask.json import jsonify
from flask_restful import Resource
from werkzeug.exceptions import UnsupportedMediaType

from context.client.ContextClient import ContextClient

from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import HTTP_CREATED
from .ietf_slice_handler import IETFSliceHandler

LOGGER = logging.getLogger(__name__)


class NSS_Service_Connection_Groups(Resource):
    # @HTTP_AUTH.login_required
    def get(self):
        response = jsonify({"message": "All went well!"})
        # TODO Return list of current network-slice-services
        return response

    # @HTTP_AUTH.login_required
    def post(self, slice_id: str):
        if not request.is_json:
            raise UnsupportedMediaType("JSON payload is required")
        request_data: Dict = request.json

        context_client = ContextClient()
        slice_request = IETFSliceHandler.create_connection_group(
            request_data, slice_id, context_client
        )
        _ = context_client.SetSlice(slice_request)

        response = jsonify({})
        response.status_code = HTTP_CREATED
        return response
