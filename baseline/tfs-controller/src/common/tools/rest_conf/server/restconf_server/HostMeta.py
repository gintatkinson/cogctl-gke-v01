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


import xml.etree.ElementTree as ET
from flask import abort, jsonify, make_response, request
from flask_restful import Resource
from .HttpStatusCodesEnum import HttpStatusCodesEnum

XRD_NS = 'http://docs.oasis-open.org/ns/xri/xrd-1.0'
ET.register_namespace('', XRD_NS)

class HostMeta(Resource):
    def __init__(self, restconf_prefix : str) -> None:
        super().__init__()
        self._restconf_prefix = restconf_prefix

    def get(self):
        best = request.accept_mimetypes.best_match([
            'application/xrd+xml', 'application/json'
        ], default='application/xrd+xml')

        if best == 'application/xrd+xml':
            xrd = ET.Element('{{{:s}}}XRD'.format(str(XRD_NS)))
            ET.SubElement(xrd, '{{{:s}}}Link'.format(str(XRD_NS)), attrib={
                'rel': 'restconf', 'href': self._restconf_prefix
            })
            xml_string = ET.tostring(xrd, encoding='utf-8', xml_declaration=True).decode()
            response = make_response(str(xml_string))
            response.status_code = 200
            response.content_type = best
            return response
        elif best == 'application/json':
            response = jsonify({'links': [{'rel': 'restconf', 'href': self._restconf_prefix}]})
            response.status_code = 200
            response.content_type = best
            return response
        else:
            abort(HttpStatusCodesEnum.CLI_ERR_NOT_ACCEPTABLE)
