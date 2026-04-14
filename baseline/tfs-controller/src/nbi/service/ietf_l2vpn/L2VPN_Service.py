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
from common.proto.context_pb2 import SliceStatusEnum
from common.tools.context_queries.Slice import get_slice_by_uuid
from context.client.ContextClient import ContextClient
from slice.client.SliceClient import SliceClient
from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import (
    HTTP_GATEWAYTIMEOUT, HTTP_NOCONTENT, HTTP_OK, HTTP_SERVERERROR
)

LOGGER = logging.getLogger(__name__)

class L2VPN_Service(Resource):
    @HTTP_AUTH.login_required
    def get(self, vpn_id : str):
        LOGGER.debug('VPN_Id: {:s}'.format(str(vpn_id)))
        LOGGER.debug('Request: {:s}'.format(str(request)))

        try:
            context_client = ContextClient()

            target = get_slice_by_uuid(context_client, vpn_id, rw_copy=True)
            if target is None:
                raise Exception('VPN({:s}) not found in database'.format(str(vpn_id)))

            if target.slice_id.slice_uuid.uuid != vpn_id: # pylint: disable=no-member
                raise Exception('Slice retrieval failed. Wrong Slice Id was returned')

            slice_ready_status = SliceStatusEnum.SLICESTATUS_ACTIVE
            slice_status = target.slice_status.slice_status # pylint: disable=no-member
            response = jsonify({})
            response.status_code = HTTP_OK if slice_status == slice_ready_status else HTTP_GATEWAYTIMEOUT
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Something went wrong Retrieving VPN({:s})'.format(str(vpn_id)))
            response = jsonify({'error': str(e)})
            response.status_code = HTTP_SERVERERROR
        return response

    @HTTP_AUTH.login_required
    def delete(self, vpn_id : str):
        LOGGER.debug('VPN_Id: {:s}'.format(str(vpn_id)))
        LOGGER.debug('Request: {:s}'.format(str(request)))

        try:
            context_client = ContextClient()

            target = get_slice_by_uuid(context_client, vpn_id)
            if target is None:
                LOGGER.warning('VPN({:s}) not found in database. Nothing done.'.format(str(vpn_id)))
            else:
                if target.slice_id.slice_uuid.uuid != vpn_id: # pylint: disable=no-member
                    raise Exception('Slice retrieval failed. Wrong Slice Id was returned')
                slice_client = SliceClient()
                slice_client.DeleteSlice(target.slice_id)
            response = jsonify({})
            response.status_code = HTTP_NOCONTENT
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Something went wrong Deleting VPN({:s})'.format(str(vpn_id)))
            response = jsonify({'error': str(e)})
            response.status_code = HTTP_SERVERERROR
        return response
