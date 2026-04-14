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

import json, libyang, logging, os
from typing import Dict, Optional

YANG_BASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'git', 'openconfig', 'public')
YANG_SEARCH_PATHS = ':'.join([
    os.path.join(YANG_BASE_PATH, 'release'),
    os.path.join(YANG_BASE_PATH, 'third_party'),
])

YANG_MODULES = [
    'iana-if-type',
    'openconfig-bgp-types',
    'openconfig-vlan-types',

    'openconfig-interfaces',
    'openconfig-if-8021x',
    'openconfig-if-aggregate',
    'openconfig-if-ethernet-ext',
    'openconfig-if-ethernet',
    'openconfig-if-ip-ext',
    'openconfig-if-ip',
    'openconfig-if-poe',
    'openconfig-if-sdn-ext',
    'openconfig-if-tunnel',

    'openconfig-vlan',

    'openconfig-types',
    'openconfig-policy-types',
    'openconfig-mpls-types',
    'openconfig-network-instance-types',
    'openconfig-network-instance',
    'openconfig-acl',

    'openconfig-platform',
    'openconfig-platform-controller-card',
    'openconfig-platform-cpu',
    'openconfig-platform-ext',
    'openconfig-platform-fabric',
    'openconfig-platform-fan',
    'openconfig-platform-integrated-circuit',
    'openconfig-platform-linecard',
    'openconfig-platform-pipeline-counters',
    'openconfig-platform-port',
    'openconfig-platform-psu',
    'openconfig-platform-software',
    'openconfig-platform-transceiver',
    'openconfig-platform-types',
    'openconfig-platform-healthz',
]

LOGGER = logging.getLogger(__name__)

class YangHandler:
    def __init__(self) -> None:
        self._yang_context = libyang.Context(YANG_SEARCH_PATHS)
        self._loaded_modules = set()
        for yang_module_name in YANG_MODULES:
            LOGGER.info('Loading module: {:s}'.format(str(yang_module_name)))
            self._yang_context.load_module(yang_module_name).feature_enable_all()
            self._loaded_modules.add(yang_module_name)
        self._data_path_instances = dict()

    def get_data_paths(self) -> Dict[str, libyang.DNode]:
        return self._data_path_instances

    def get_data_path(self, path : str) -> libyang.DNode:
        data_path_instance = self._data_path_instances.get(path)
        if data_path_instance is None:
            data_path_instance = self._yang_context.create_data_path(path)
            self._data_path_instances[path] = data_path_instance
        return data_path_instance

    def parse_to_dict(
        self, request_path : str, json_data : Dict, fmt : str = 'json', strict : bool = True
    ) -> Dict:
        if fmt != 'json': raise Exception('Unsupported format: {:s}'.format(str(fmt)))
        LOGGER.debug('request_path = {:s}'.format(str(request_path)))
        LOGGER.debug('json_data = {:s}'.format(str(json_data)))
        LOGGER.debug('format = {:s}'.format(str(fmt)))

        parent_path_parts = list(filter(lambda s: len(s) > 0, request_path.split('/')))
        for parent_path_part in reversed(parent_path_parts):
            json_data = {parent_path_part: json_data}
        str_data = json.dumps(json_data)

        dnode : Optional[libyang.DNode] = self._yang_context.parse_data_mem(
            str_data, fmt, strict=strict, parse_only=True, #validate_present=True, #validate=True,
        )
        if dnode is None: raise Exception('Unable to parse Data({:s})'.format(str(json_data)))

        parsed = dnode.print_dict()
        LOGGER.debug('parsed = {:s}'.format(json.dumps(parsed)))
        dnode.free()
        return parsed

    def destroy(self) -> None:
        self._yang_context.destroy()
