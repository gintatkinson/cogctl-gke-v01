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

# Example request:
# request = {'ietf-l2vpn-svc:vpn-service': [{
#   'vpn-id': 'c6270231-f1de-4687-b2ed-7b58f9105775',
#   'vpn-svc-type': 'vpws',
#   'svc-topo': 'any-to-any',
#   'customer-name': 'osm'
# }]}

from .Common import REGEX_UUID

SCHEMA_VPN_SERVICE = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'type': 'object',
    'required': ['ietf-l2vpn-svc:vpn-service'],
    'properties': {
        'ietf-l2vpn-svc:vpn-service': {
            'type': 'array',
            'minItems': 1,
            'maxItems': 1,  # by now we do not support multiple vpn-service in the same message
            'items': {
                'type': 'object',
                'required': ['vpn-id', 'vpn-svc-type', 'svc-topo', 'customer-name'],
                'properties': {
                    'vpn-id': {'type': 'string', 'pattern': REGEX_UUID},
                    'vpn-svc-type': {'enum': ['vpws', 'vpls']},
                    'svc-topo': {'enum': ['any-to-any']},
                    'customer-name': {'const': 'osm'},
                },
            }
        }
    },
}
