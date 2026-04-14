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
from .Resources import E2EInfoDelete

URL_PREFIX = '/restconf/E2E/v1'

def register_etsi_api(nbi_app : NbiApplication):

    nbi_app.add_rest_api_resource(
        E2EInfoDelete,
        URL_PREFIX + '/service/<string:allocationId>',
        endpoint='etsi_E2E.e2e_info_delete'
    )
