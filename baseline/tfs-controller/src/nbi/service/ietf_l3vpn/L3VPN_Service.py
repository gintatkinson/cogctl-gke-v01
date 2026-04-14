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
from common.proto.context_pb2 import ServiceStatusEnum
from common.tools.context_queries.Service import get_service_by_uuid
from context.client.ContextClient import ContextClient
from service.client.ServiceClient import ServiceClient
from typing import Dict, List
from werkzeug.exceptions import UnsupportedMediaType
from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import (
    HTTP_GATEWAYTIMEOUT, HTTP_NOCONTENT, HTTP_OK, HTTP_SERVERERROR, HTTP_CREATED
)
from .Handlers import  update_vpn
from .YangValidator import YangValidator

LOGGER = logging.getLogger(__name__)

class L3VPN_Service(Resource):
    # @HTTP_AUTH.login_required
    def get(self, vpn_id : str):
        LOGGER.debug('VPN_Id: {:s}'.format(str(vpn_id)))
        LOGGER.debug('Request: {:s}'.format(str(request)))

        try:
            context_client = ContextClient()

            target = get_service_by_uuid(context_client, vpn_id, rw_copy=True)
            if target is None:
                raise Exception('VPN({:s}) not found in database'.format(str(vpn_id)))

            service_ids = {target.service_id.service_uuid.uuid, target.name} # pylint: disable=no-member
            if vpn_id not in service_ids:
                raise Exception('Service retrieval failed. Wrong Service Id was returned')

            service_ready_status = ServiceStatusEnum.SERVICESTATUS_ACTIVE
            service_status = target.service_status.service_status # pylint: disable=no-member
            response = jsonify({'service-id': target.service_id.service_uuid.uuid})
            response.status_code = HTTP_OK if service_status == service_ready_status else HTTP_GATEWAYTIMEOUT
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Something went wrong Retrieving VPN({:s})'.format(str(vpn_id)))
            response = jsonify({'error': str(e)})
            response.status_code = HTTP_SERVERERROR
        return response

    # @HTTP_AUTH.login_required
    def delete(self, vpn_id : str):
        LOGGER.debug('VPN_Id: {:s}'.format(str(vpn_id)))
        LOGGER.debug('Request: {:s}'.format(str(request)))

        try:
            context_client = ContextClient()

            target = get_service_by_uuid(context_client, vpn_id)
            if target is None:
                LOGGER.warning('VPN({:s}) not found in database. Nothing done.'.format(str(vpn_id)))
            else:
                service_ids = {target.service_id.service_uuid.uuid, target.name} # pylint: disable=no-member
                if vpn_id not in service_ids:
                    raise Exception('Service retrieval failed. Wrong Service Id was returned')
                service_client = ServiceClient()
                service_client.DeleteService(target.service_id)
            response = jsonify({})
            response.status_code = HTTP_NOCONTENT
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Something went wrong Deleting VPN({:s})'.format(str(vpn_id)))
            response = jsonify({'error': str(e)})
            response.status_code = HTTP_SERVERERROR
        return response

    def put(self, vpn_id : str):
        #TODO: check vpn_id with request service_id in body
        if not request.is_json: raise UnsupportedMediaType('JSON payload is required')
        request_data: Dict = request.json
        LOGGER.debug('PUT Request: {:s}'.format(str(request_data)))

        errors = list()

        if 'ietf-l3vpn-svc:l3vpn-services' in request_data:
            for l3vpn_svc in request_data['ietf-l3vpn-svc:l3vpn-services']['l3vpn-svc']:
                l3vpn_svc.pop('service-id', None)
                l3vpn_svc_request_data = {'ietf-l3vpn-svc:l3vpn-svc': l3vpn_svc}
                errors.extend(self._update_l3vpn(l3vpn_svc_request_data))
        elif 'ietf-l3vpn-svc:l3vpn-svc' in request_data:
            errors.extend(self._update_l3vpn(request_data))
        else:
            errors.append('Unexpected request format: {:s}'.format(str(request_data)))

        response = jsonify(errors)
        response.status_code = HTTP_CREATED if len(errors) == 0 else HTTP_SERVERERROR
        return response

    def _update_l3vpn(self, request_data: Dict) -> List[Dict]:
        yang_validator = YangValidator('ietf-l3vpn-svc')
        request_data = yang_validator.parse_to_dict(request_data)
        yang_validator.destroy()

        errors = list()

        for site in request_data['l3vpn-svc']['sites']['site']:
            update_vpn(site, errors)

        return errors
