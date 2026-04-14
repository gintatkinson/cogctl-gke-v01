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
from .Resources import NS_Services, NS_Service


ENDPOINT_PREFIX = 'osm_api.'
URL_PREFIX = '/osm-api'

_RESOURCES = [
    ('api.NS_Services',   NS_Services, '/NS_Services'),
    ('api.NS_Service_id', NS_Service,  '/NS_Service/<string:ns_id>'),
]

RESOURCES = [
    (ENDPOINT_PREFIX + endpoint_name, resource_class, URL_PREFIX + resource_url)
    for endpoint_name, resource_class, resource_url in _RESOURCES
]


def register_osm_api(nbi_app : NbiApplication):
    nbi_app.add_rest_api_resources(RESOURCES)
