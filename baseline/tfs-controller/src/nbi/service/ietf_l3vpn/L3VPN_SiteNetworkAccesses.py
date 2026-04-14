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
from flask.wrappers import Response
from flask_restful import Resource
from werkzeug.exceptions import UnsupportedMediaType
from nbi.service._tools.Authentication import HTTP_AUTH
from nbi.service._tools.HttpStatusCodes import HTTP_CREATED, HTTP_SERVERERROR
from .Handlers import process_site_network_access
from .YangValidator import YangValidator

LOGGER = logging.getLogger(__name__)

def process_site_network_accesses(site_id : str) -> Response:
    if not request.is_json: raise UnsupportedMediaType('JSON payload is required')
    request_data : Dict = request.json
    LOGGER.debug('Site_Id: {:s}'.format(str(site_id)))
    LOGGER.debug('Request: {:s}'.format(str(request_data)))

    yang_validator = YangValidator('ietf-l3vpn-svc')
    request_data = yang_validator.parse_to_dict(request_data)
    yang_validator.destroy()

    # TODO: retrieve site static routing from service
    site_static_routing = dict()

    errors = []
    for network_access in request_data['site-network-accesses']['site-network-access']:
        exc = process_site_network_access(site_id, network_access, site_static_routing, errors)
        if exc is not None: errors.append({'error': str(exc)})

    response = jsonify(errors)
    response.status_code = HTTP_CREATED if len(errors) == 0 else HTTP_SERVERERROR
    return response

class L3VPN_SiteNetworkAccesses(Resource):
    @HTTP_AUTH.login_required
    def post(self, site_id : str):
        return process_site_network_accesses(site_id)

    @HTTP_AUTH.login_required
    def put(self, site_id : str):
        return process_site_network_accesses(site_id)
