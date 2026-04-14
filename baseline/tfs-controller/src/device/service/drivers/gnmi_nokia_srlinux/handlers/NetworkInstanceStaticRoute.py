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

import json, logging
from typing import Any, Dict, List, Tuple
from ._Handler import _Handler

LOGGER = logging.getLogger(__name__)

class NetworkInstanceStaticRouteHandler(_Handler):
    def get_resource_key(self) -> str: return '/network_instance/static_route'
    def get_path(self) -> str: return '/network-instances/network-instance/static_route'

    def compose(self, resource_key : str, resource_value : Dict, delete : bool = False) -> Tuple[str, str]:
        ni_name        = str(resource_value['name'                 ]) # test-svc
        prefix         = str(resource_value['prefix'               ]) # '172.0.1.0/24'

        identifier = 'STATIC'
        name = 'static'
        if delete:
            PATH_TMPL  = '/network-instances/network-instance[name={:s}]/protocols'
            PATH_TMPL += '/protocol[identifier={:s}][name={:s}]/static-routes/static[prefix={:s}]'
            str_path = PATH_TMPL.format(ni_name, identifier, name, prefix)
            str_data = json.dumps({})
            return str_path, str_data

        next_hop       = str(resource_value['next_hop'             ]) # '172.0.0.1'
        next_hop_index = int(resource_value.get('next_hop_index', 0)) # 0

        PATH_TMPL = '/network-instances/network-instance[name={:s}]/protocols/protocol[identifier={:s}][name={:s}]'
        str_path = PATH_TMPL.format(ni_name, identifier, name)
        str_data = json.dumps({
            'identifier': identifier, 'name': name,
            'config': {'identifier': identifier, 'name': name, 'enabled': True},
            'static_routes': {'static': [{
                'prefix': prefix,
                'config': {'prefix': prefix},
                'next_hops': {
                    'next-hop': [{
                        'index': next_hop_index,
                        'config': {'index': next_hop_index, 'next_hop': next_hop}
                    }]
                }
            }]}
        })
        return str_path, str_data

    def parse(self, json_data : Dict) -> List[Tuple[str, Dict[str, Any]]]:
        response = []
        return response
