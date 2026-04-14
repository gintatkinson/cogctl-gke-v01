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

import json, libyang, logging
from typing import Any, Dict, List, Tuple
from ._Handler import _Handler
from .Tools import get_int, get_str
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

IS_CEOS = True

class NetworkInstanceInterfaceHandler(_Handler):
    def get_resource_key(self) -> str: return '/network_instance/interface'
    def get_path(self) -> str: return '/openconfig-network-instance:network-instances/network-instance/interfaces'

    def compose(
        self, resource_key : str, resource_value : Dict, yang_handler : YangHandler, delete : bool = False
    ) -> Tuple[str, str]:
        ni_name   = get_str(resource_value, 'name'           ) # test-svc
        ni_if_id  = get_str(resource_value, 'id'             ) # ethernet-1/1.0
        if_name   = get_str(resource_value, 'interface'      ) # ethernet-1/1
        sif_index = get_int(resource_value, 'subinterface', 0) # 0

        if IS_CEOS: ni_if_id = if_name

        PATH_TMPL = '/network-instances/network-instance[name={:s}]/interfaces/interface[id={:s}]'
        str_path = PATH_TMPL.format(ni_name, ni_if_id)

        if delete:
            str_data = json.dumps({})
            return str_path, str_data

        #str_data = json.dumps({
        #    'id': if_id,
        #    'config': {'id': if_id, 'interface': if_name, 'subinterface': sif_index},
        #})

        yang_nis : libyang.DContainer = yang_handler.get_data_path('/openconfig-network-instance:network-instances')
        yang_ni : libyang.DContainer = yang_nis.create_path('network-instance[name="{:s}"]'.format(ni_name))
        yang_ni_ifs : libyang.DContainer = yang_ni.create_path('interfaces')
        yang_ni_if_path = 'interface[id="{:s}"]'.format(ni_if_id)
        yang_ni_if : libyang.DContainer = yang_ni_ifs.create_path(yang_ni_if_path)
        yang_ni_if.create_path('config/id',           ni_if_id)
        yang_ni_if.create_path('config/interface',    if_name)
        yang_ni_if.create_path('config/subinterface', sif_index)

        str_data = yang_ni_if.print_mem('json')
        json_data = json.loads(str_data)
        json_data = json_data['openconfig-network-instance:interface'][0]
        str_data = json.dumps(json_data)
        return str_path, str_data

    def parse(
        self, json_data : Dict, yang_handler : YangHandler
    ) -> List[Tuple[str, Dict[str, Any]]]:
        LOGGER.debug('[parse] json_data = {:s}'.format(str(json_data)))
        response = []
        return response
