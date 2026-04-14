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
# request = {'ietf-l2vpn-svc:site-network-access': [{
#     'network-access-id': '3fd942ee-2dc3-41d1-aeec-65aa85d117b2',
#     'vpn-attachment': {'vpn-id': '954b1b53-4a8c-406d-9eff-750ec2c9a258',
#         'site-role': 'any-to-any-role'},
#     'connection': {'encapsulation-type': 'dot1q-vlan-tagged', 'tagged-interface': {
#         'dot1q-vlan-tagged': {'cvlan-id': 1234}}},
#     'bearer': {'bearer-reference': '1a'}
# }]}

from .Common import REGEX_UUID

SCHEMA_SITE_NETWORK_ACCESS = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'type': 'object',
    'required': ['ietf-l2vpn-svc:site-network-access'],
    'properties': {
        'ietf-l2vpn-svc:site-network-access': {
            'type': 'array',
            'minItems': 1,
            'maxItems': 1,  # by now we do not support multiple site-network-access in the same message
            'items': {
                'type': 'object',
                'required': ['network-access-id', 'vpn-attachment', 'connection', 'bearer'],
                'properties': {
                    'network-access-id': {'type': 'string', 'pattern': REGEX_UUID},
                    'vpn-attachment': {
                        'type': 'object',
                        'required': ['vpn-id', 'site-role'],
                        'properties': {
                            'vpn-id': {'type': 'string', 'pattern': REGEX_UUID},
                            'site-role': {'type': 'string', 'minLength': 1},
                        },
                    },
                    'connection': {
                        'type': 'object',
                        'required': ['encapsulation-type', 'tagged-interface'],
                        'properties': {
                            'encapsulation-type': {'enum': ['dot1q-vlan-tagged']},
                            'tagged-interface': {
                                'type': 'object',
                                'required': ['dot1q-vlan-tagged'],
                                'properties': {
                                    'dot1q-vlan-tagged': {
                                        'type': 'object',
                                        'required': ['cvlan-id'],
                                        'properties': {
                                            'cvlan-id': {'type': 'integer', 'minimum': 1, 'maximum': 4094},
                                        },
                                    },
                                },
                            },
                        },
                    },
                    'bearer': {
                        'type': 'object',
                        'required': ['bearer-reference'],
                        'properties': {
                            'bearer-reference': {'type': 'string', 'minLength': 1},
                        },
                    },
                },
            },
        },
    },
}
