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
from flask import request
from flask.json import jsonify
from flask_restful import Resource
from common.tools.context_queries.Device import get_device
from context.client.ContextClient import ContextClient
from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import HTTP_OK, HTTP_SERVERERROR
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

class Hardware(Resource):
    @HTTP_AUTH.login_required
    def get(self, device_uuid : str):
        LOGGER.debug('Device UUID: {:s}'.format(str(device_uuid)))
        LOGGER.debug('Request: {:s}'.format(str(request)))

        try:
            context_client = ContextClient()
            device = get_device(
                context_client, device_uuid, rw_copy=False,
                include_endpoints=False, include_config_rules=False, include_components=True
            )
            if device is None:
                raise Exception('Device({:s}) not found in database'.format(str(device_uuid)))

            yang_handler = YangHandler()
            hardware_reply = yang_handler.compose(device)
            yang_handler.destroy()

            response = jsonify(hardware_reply)
            response.status_code = HTTP_OK
        except Exception as e: # pylint: disable=broad-except
            MSG = 'Something went wrong Retrieving Hardware of Device({:s})'
            LOGGER.exception(MSG.format(str(device_uuid)))
            response = jsonify({'error': str(e)})
            response.status_code = HTTP_SERVERERROR
        return response
