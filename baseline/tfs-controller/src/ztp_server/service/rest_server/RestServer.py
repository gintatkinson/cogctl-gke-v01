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
from common.tools.rest_api.server.GenericRestServer import GenericRestServer

class RestServer(GenericRestServer):
    def __init__(self, cls_name: str = __name__) -> None:
        bind_port = get_service_port_http(ServiceNameEnum.ZTP_SERVER)
        base_url = get_service_baseurl_http(ServiceNameEnum.ZTP_SERVER)
        super().__init__(bind_port, base_url=base_url, cls_name=cls_name)
