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

# RFC 8299 - YANG Data Model for L3VPN Service Delivery
# Ref: https://datatracker.ietf.org/doc/rfc8299


from nbi.service.NbiApplication import NbiApplication
from .L3VPN_Services import L3VPN_Services
from .L3VPN_Service import L3VPN_Service
from .L3VPN_SiteNetworkAccesses import L3VPN_SiteNetworkAccesses

URL_PREFIX = '/restconf/data/ietf-l3vpn-svc:l3vpn-svc'

def register_ietf_l3vpn(nbi_app : NbiApplication):
    nbi_app.add_rest_api_resource(
        L3VPN_Services,
        URL_PREFIX + '/vpn-services',
    )
    nbi_app.add_rest_api_resource(
        L3VPN_Service,
        URL_PREFIX + '/vpn-services/vpn-service=<vpn_id>',
        URL_PREFIX + '/vpn-services/vpn-service=<vpn_id>/',
    )
    nbi_app.add_rest_api_resource(
        L3VPN_SiteNetworkAccesses,
        URL_PREFIX + '/sites/site=<site_id>/site-network-accesses',
        URL_PREFIX + '/sites/site=<site_id>/site-network-accesses/',
    )
