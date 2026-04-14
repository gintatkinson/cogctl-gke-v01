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

# IETF draft-ietf-teas-ietf-network-slice-nbi-yang-02 - IETF Network Slice Service YANG Model
# Ref: https://datatracker.ietf.org/doc/draft-ietf-teas-ietf-network-slice-nbi-yang/

from nbi.service.NbiApplication import NbiApplication
from .NSS_Service import NSS_Service
from .NSS_Service_Match_Criteria import NSS_Service_Match_Criteria
from .NSS_Service_Match_Criterion import NSS_Service_Match_Criterion
from .NSS_Services import NSS_Services
from .NSS_Services_Connection_Group import NSS_Service_Connection_Group
from .NSS_Services_Connection_Groups import NSS_Service_Connection_Groups
from .NSS_Services_SDP import NSS_Service_SDP
from .NSS_Services_SDPs import NSS_Service_SDPs

URL_PREFIX = '/restconf/data/ietf-network-slice-service:network-slice-services'

def register_ietf_nss(nbi_app: NbiApplication):
    nbi_app.add_rest_api_resource(
        NSS_Services,
        URL_PREFIX + '/'
    )
    nbi_app.add_rest_api_resource(
        NSS_Service,
        URL_PREFIX + '/slice-service=<string:slice_id>',
    )
    nbi_app.add_rest_api_resource(
        NSS_Service_SDPs,
        URL_PREFIX + '/slice-service=<string:slice_id>/sdps',
    )
    nbi_app.add_rest_api_resource(
        NSS_Service_SDP,
        URL_PREFIX + '/slice-service=<string:slice_id>/sdps/sdp=<string:sdp_id>',
    )
    nbi_app.add_rest_api_resource(
        NSS_Service_Connection_Groups,
        URL_PREFIX + '/slice-service=<string:slice_id>/connection-groups',
    )
    nbi_app.add_rest_api_resource(
        NSS_Service_Connection_Group,
        URL_PREFIX + '/slice-service=<string:slice_id>/connection-groups/connection-group=<string:connection_group_id>',
    )
    nbi_app.add_rest_api_resource(
        NSS_Service_Match_Criteria,
        URL_PREFIX + '/slice-service=<string:slice_id>/sdps/sdp=<string:sdp_id>/service-match-criteria',
    )
    nbi_app.add_rest_api_resource(
        NSS_Service_Match_Criterion,
        URL_PREFIX + '/slice-service=<string:slice_id>/sdps/sdp=<string:sdp_id>/service-match-criteria/match-criterion=<string:match_criterion_id>',
    )
