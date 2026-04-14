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
from .Resources import ProfileList, ProfileDetail, QodInfo, QodInfoID

URL_PREFIX = '/camara/qod/v0'

def register_camara_qod(nbi_app : NbiApplication):
    nbi_app.add_rest_api_resource(
        QodInfo,
        URL_PREFIX + '/sessions',
        endpoint='camara.qod.session_list'
    )
    nbi_app.add_rest_api_resource(
        QodInfoID,
        URL_PREFIX + '/sessions/<string:session_id>',
        endpoint='camara.qod.session_detail'
    )
    nbi_app.add_rest_api_resource(
        ProfileList,
        URL_PREFIX + '/profiles',
        endpoint='camara.qod.profile_list'
    )
    nbi_app.add_rest_api_resource(
        ProfileDetail,
        URL_PREFIX + '/profiles/<string:qos_profile_id>',
        endpoint='camara.qod.profile_detail'
    )
