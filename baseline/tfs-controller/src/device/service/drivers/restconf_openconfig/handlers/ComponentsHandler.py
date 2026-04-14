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

import logging
from typing import Dict, List, Tuple
from common.tools.rest_conf.client.RestConfClient import RestConfClient


LOGGER = logging.getLogger(__name__)


class ComponentsHandler:
    def __init__(self, rest_conf_client : RestConfClient) -> None:
        self._rest_conf_client = rest_conf_client
        self._subpath_root = '/openconfig-platform:components'

    def get(self) -> List[Tuple[str, Dict]]:
        reply = self._rest_conf_client.get(self._subpath_root)

        if 'openconfig-platform:components' not in reply:
            raise Exception('Malformed reply. "openconfig-platform:components" missing')
        components = reply['openconfig-platform:components']

        if 'component' not in components:
            raise Exception('Malformed reply. "openconfig-platform:components/component" missing')
        component_lst = components['component']

        if len(component_lst) == 0:
            MSG = '[get] No components are reported'
            LOGGER.debug(MSG)
            return list()
        
        entries : List[Tuple[str, Dict]] = list()
        for component in component_lst:
            if 'state' not in component:
                MSG = 'Malformed component. "state" missing: {:s}'
                raise Exception(MSG.format(str(component)))
            comp_state = component['state']

            if 'type' not in comp_state:
                MSG = 'Malformed component. "state/type" missing: {:s}'
                raise Exception(MSG.format(str(component)))
            comp_type : str = comp_state['type']
            comp_type = comp_type.split(':')[-1]
            if comp_type  != 'PORT': continue

            if 'name' not in component:
                MSG = 'Malformed component. "name" missing: {:s}'
                raise Exception(MSG.format(str(component)))
            comp_name = component['name']

            if comp_name.startswith('cali'): continue # calico port
            if comp_name.startswith('vxlan'): continue # vxlan.calico port
            if comp_name.startswith('docker'): continue # docker port
            if comp_name in {'lo', 'loop', 'loopback'}: continue # loopback port

            endpoint = {'uuid': comp_name, 'type': '-'}
            entries.append(('/endpoints/endpoint[{:s}]'.format(endpoint['uuid']), endpoint))

        return entries
