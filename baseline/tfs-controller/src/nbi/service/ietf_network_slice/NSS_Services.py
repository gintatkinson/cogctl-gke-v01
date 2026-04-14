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
from slice.client.SliceClient import SliceClient

from nbi.service._tools.HttpStatusCodes import HTTP_CREATED, HTTP_OK
from .ietf_slice_handler import IETFSliceHandler

LOGGER = logging.getLogger(__name__)


class NSS_Services(Resource):
    # @HTTP_AUTH.login_required
    def get(self):
        context_client = ContextClient()
        ietf_slices = IETFSliceHandler.get_all_ietf_slices(context_client)
        response = jsonify(ietf_slices)
        response.status_code = HTTP_OK
        return response

    # @HTTP_AUTH.login_required
    def post(self):
        if not request.is_json:
            raise UnsupportedMediaType("JSON payload is required")
        request_data: Dict = request.json
        context_client = ContextClient()
        slice_request = IETFSliceHandler.create_slice_service(
            request_data, context_client
        )
        slice_client = SliceClient()
        slice_client.CreateSlice(slice_request)

        response = jsonify({})
        response.status_code = HTTP_CREATED
        return response
