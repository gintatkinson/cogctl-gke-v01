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

class NetworkInstanceInterfaceHandler(_Handler):
    def get_resource_key(self) -> str: return '/network-instance/interface'
    def get_path(self) -> str: return '/network-instance/interface'

    def compose(self, resource_key : str, resource_value : Dict, delete : bool = False) -> Tuple[str, str]:
        ni_name = str(resource_value['name'     ])    # default
        name = str(resource_value['name'  ])    # ethernet-1/49.0


        if delete:
            PATH_TMPL = '/network-instances/network-instance[name={:s}]/interface[if_name={:s}]'
            str_path = PATH_TMPL.format(ni_name,name)
            str_data = json.dumps({})
            return str_path, str_data

        str_path = 'network-instance[name={:s}]/interface'.format(ni_name, name)
        str_data = json.dumps({})

    def parse(self, json_data : Dict) -> List[Tuple[str, Dict[str, Any]]]:
        response = []
        return response
