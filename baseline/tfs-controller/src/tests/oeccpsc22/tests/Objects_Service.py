# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Objects_Domain_1 import D1_DEVICE_D1R1_UUID, D1_ENDPOINT_IDS
from .Objects_Domain_2 import D2_DEVICE_D2R4_UUID, D2_ENDPOINT_IDS
from .Tools import compose_bearer, compose_service_endpoint_id

# ----- WIM Service Settings -------------------------------------------------------------------------------------------
WIM_SEP_D1R1_ID          = compose_service_endpoint_id(D1_ENDPOINT_IDS[D1_DEVICE_D1R1_UUID]['3/1'])
WIM_SEP_D1R1_ROUTER_ID   = '10.10.10.1'
WIM_SEP_D1R1_ROUTER_DIST = '65000:111'
WIM_SEP_D1R1_SITE_ID     = '1'
WIM_SEP_D1R1_BEARER      = compose_bearer(D1_ENDPOINT_IDS[D1_DEVICE_D1R1_UUID]['3/1'])
WIM_SRV_D1R1_VLAN_ID     = 400

WIM_SEP_D2R4_ID          = compose_service_endpoint_id(D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['3/3'])
WIM_SEP_D2R4_ROUTER_ID   = '20.20.20.1'
WIM_SEP_D2R4_ROUTER_DIST = '65000:222'
WIM_SEP_D2R4_SITE_ID     = '2'
WIM_SEP_D2R4_BEARER      = compose_bearer(D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['3/3'])
WIM_SRV_D2R4_VLAN_ID     = 500

WIM_USERNAME = 'admin'
WIM_PASSWORD = 'admin'

WIM_MAPPING  = [
    {'device-id': D1_DEVICE_D1R1_UUID, 'service_endpoint_id': WIM_SEP_D1R1_ID,
     'service_mapping_info': {'bearer': {'bearer-reference': WIM_SEP_D1R1_BEARER}, 'site-id': WIM_SEP_D1R1_SITE_ID}},
    {'device-id': D2_DEVICE_D2R4_UUID, 'service_endpoint_id': WIM_SEP_D2R4_ID,
     'service_mapping_info': {'bearer': {'bearer-reference': WIM_SEP_D2R4_BEARER}, 'site-id': WIM_SEP_D2R4_SITE_ID}},
]
WIM_SERVICE_TYPE = 'ELAN'
WIM_SERVICE_CONNECTION_POINTS = [
    {'service_endpoint_id': WIM_SEP_D1R1_ID,
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': WIM_SRV_D1R1_VLAN_ID}},
    {'service_endpoint_id': WIM_SEP_D2R4_ID,
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': WIM_SRV_D2R4_VLAN_ID}},
]
