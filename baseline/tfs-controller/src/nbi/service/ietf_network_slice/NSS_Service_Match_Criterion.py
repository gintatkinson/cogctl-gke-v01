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

from flask.json import jsonify
from flask_restful import Resource

from context.client.ContextClient import ContextClient

from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import (
    HTTP_CREATED,
)
from .ietf_slice_handler import IETFSliceHandler

LOGGER = logging.getLogger(__name__)


class NSS_Service_Match_Criterion(Resource):
    # @HTTP_AUTH.login_required
    def get(self):
        response = jsonify({"message": "All went well!"})
        # TODO Return list of current network-slice-services
        return response

    # @HTTP_AUTH.login_required
    def delete(self, slice_id: str, sdp_id: str, match_criterion_id: str):
        context_client = ContextClient()
        slice_request = IETFSliceHandler.delete_match_criteria(
            slice_id, sdp_id, int(match_criterion_id), context_client
        )
        context_client = ContextClient()
        _ = context_client.SetSlice(slice_request)

        response = jsonify({})
        response.status_code = HTTP_CREATED
        return response
