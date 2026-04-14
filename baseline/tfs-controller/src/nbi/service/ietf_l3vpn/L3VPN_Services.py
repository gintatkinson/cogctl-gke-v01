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
from nbi.service._tools.HttpStatusCodes import HTTP_CREATED, HTTP_SERVERERROR
from nbi.service._tools.Authentication import HTTP_AUTH
from .Handlers import process_site, process_vpn_service
from .YangValidator import YangValidator

LOGGER = logging.getLogger(__name__)

class L3VPN_Services(Resource):
    # @HTTP_AUTH.login_required
    def get(self):
        return {}

    # @HTTP_AUTH.login_required
    def post(self):
        if not request.is_json: raise UnsupportedMediaType('JSON payload is required')
        request_data : Dict = request.json
        LOGGER.debug('Request: {:s}'.format(str(request_data)))

        errors = list()
        if 'ietf-l3vpn-svc:l3vpn-services' in request_data:
            # processing multiple L3VPN service requests formatted as:
            #{
            #  "ietf-l3vpn-svc:l3vpn-services": {
            #    "l3vpn-svc": [
            #      {
            #        "service-id": "vpn1",
            #        "vpn-services": {
            #          "vpn-service": [
            for l3vpn_svc in request_data['ietf-l3vpn-svc:l3vpn-services']['l3vpn-svc']:
                l3vpn_svc.pop('service-id', None)
                l3vpn_svc_request_data = {'ietf-l3vpn-svc:l3vpn-svc': l3vpn_svc}
                errors.extend(self._process_l3vpn(l3vpn_svc_request_data))
        elif 'ietf-l3vpn-svc:l3vpn-svc' in request_data:
            # processing single (standard) L3VPN service request formatted as:
            #{
            #  "ietf-l3vpn-svc:l3vpn-svc": {
            #    "vpn-services": {
            #      "vpn-service": [
            errors.extend(self._process_l3vpn(request_data))
        else:
            errors.append('unexpected request: {:s}'.format(str(request_data)))

        response = jsonify(errors)
        response.status_code = HTTP_CREATED if len(errors) == 0 else HTTP_SERVERERROR
        return response

    def _process_l3vpn(self, request_data : Dict) -> List[Dict]:
        yang_validator = YangValidator('ietf-l3vpn-svc')
        request_data = yang_validator.parse_to_dict(request_data)
        yang_validator.destroy()

        errors = list()

        for vpn_service in request_data['l3vpn-svc']['vpn-services']['vpn-service']:
            process_vpn_service(vpn_service, errors)

        for site in request_data['l3vpn-svc']['sites']['site']:
            process_site(site, errors)

        return errors
