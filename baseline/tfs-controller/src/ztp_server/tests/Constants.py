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


from common.Constants import ServiceNameEnum
from common.Settings import get_service_baseurl_http, get_service_port_http


USERNAME               = 'admin'
PASSWORD               = 'admin'
LOCAL_HOST             = '127.0.0.1'
MOCKSERVICE_PORT       = 10000
ZTP_SERVICE_PORT       = get_service_port_http(ServiceNameEnum.ZTP_SERVER) + MOCKSERVICE_PORT # avoid privileged ports
ZTP_SERVICE_PREFIX_URL = get_service_baseurl_http(ServiceNameEnum.ZTP_SERVER) or ''
ZTP_SERVICE_BASE_URL   = 'http://{:s}:{:s}@{:s}:{:d}{:s}'.format(
    USERNAME, PASSWORD, LOCAL_HOST, ZTP_SERVICE_PORT, ZTP_SERVICE_PREFIX_URL
)
