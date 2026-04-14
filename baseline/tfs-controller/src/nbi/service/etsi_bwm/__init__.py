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

from nbi.service.NbiApplication import NbiApplication
from .Resources import BwInfo, BwInfoId

URL_PREFIX = '/restconf/bwm/v1'

def register_etsi_bwm_api(nbi_app : NbiApplication):
    nbi_app.add_rest_api_resource(
        BwInfo,
        URL_PREFIX + '/bw_allocations',
        endpoint='etsi_bwm.bw_info'
    )
    nbi_app.add_rest_api_resource(
        BwInfoId,
        URL_PREFIX + '/bw_allocations/<path:allocationId>',
        endpoint='etsi_bwm.bw_info_id'
    )
