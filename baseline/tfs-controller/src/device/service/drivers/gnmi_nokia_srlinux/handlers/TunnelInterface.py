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

class TunnelInterfaceHandler(_Handler):
    def get_resource_key(self) -> str:
        return '/tunnel-interface'

    def get_path(self) -> str:
        return '/srl_nokia-tunnel-interfaces:tunnel-interface'
        #return '/tunnel-interface'

    def compose(self, resource_key: str, resource_value: Dict, delete: bool = False) -> Tuple[str, str]:
        name = str(resource_value['name'])

        if delete:
            PATH_TMPL = '/tunnel-interface[name={:s}]'
            str_path = PATH_TMPL.format(name)
            str_data = json.dumps({})
            return str_path, str_data
        
       
        str_path = '/tunnel-interface[name={:s}]'.format(name)
 

        if 'index' in resource_value:
            index = str(resource_value['index'])
            json_tunnel = {}
            subif_vxlaninterface = json_tunnel.setdefault('vxlan-interface', list())
            subif = {'index': index}

        if 'type_tunnel' in resource_value:
            type_tunnel = str(resource_value['type_tunnel'])
            subif['type'] = type_tunnel

        if 'vni_tunnel' in resource_value:
            vni_tunnel = int(resource_value['vni_tunnel'])
            subif['ingress'] = {}
            subif['ingress']['vni'] = vni_tunnel
            subif_vxlaninterface.append(subif)
        return str_path, json.dumps(json_tunnel)

    def parse(self, json_data: Dict) -> List[Tuple[str, Dict[str, Any]]]:
        response = []
        json_tunnel_list = json_data.get('srl_nokia-tunnel-interfaces:tunnel-interface', [])
        for json_tunnel in json_tunnel_list:
            tunnel_interface1 = {}
            name = json_tunnel.get('name', {})
            #tunnel_interface1['name']=str(name)
            json_vxlan_list = json_tunnel.get('vxlan-interface', [])
            lists = tunnel_interface1.setdefault('vxlan-interface', [])
            for json_vxlan1 in json_vxlan_list:
                tunnel_interface2 = {}
                index = json_vxlan1.get('index', {})
                type = json_vxlan1.get('type', {})
                ingress = json_vxlan1.get('ingress', {}).get('vni')

                tunnel_interface2['index'] = str(index)
                tunnel_interface2['type'] = str(type)
                tunnel_interface2['ingress'] = {}
                tunnel_interface2['ingress']['vni'] = int(ingress)

                lists.append(tunnel_interface2)

            # if len(tunnel_interface1 ) == 0:
            #     continue

            resource_key = '/tunnel-interface[{:s}]'.format(name)
            response.append((resource_key, tunnel_interface1 ))

        return response
