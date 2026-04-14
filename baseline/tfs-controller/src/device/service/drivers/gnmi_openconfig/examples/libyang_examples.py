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
from typing import Dict

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

YANG_BASE_PATH = '/home/tfs/tfs-ctrl/src/device/service/drivers/gnmi_openconfig/git/openconfig/public'
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
]

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

    def destroy(self) -> None:
        self._yang_context.destroy()

def main():
    yang_handler = YangHandler()

    LOGGER.info('YangHandler Data (before):')
    for path, dnode in yang_handler.get_data_paths().items():
        LOGGER.info('|-> {:s}: {:s}'.format(str(path), json.dumps(dnode.print_dict())))

    if_name        = 'eth1'
    sif_index      = 0
    enabled        = True
    address_ip     = '172.16.0.1'
    address_ip2    = '192.168.0.1'
    address_prefix = 24
    mtu            = 1500

    yang_ifs : libyang.DContainer = yang_handler.get_data_path('/openconfig-interfaces:interfaces')
    yang_if_path = 'interface[name="{:s}"]'.format(if_name)
    yang_if : libyang.DContainer = yang_ifs.create_path(yang_if_path)
    yang_if.create_path('config/name',    if_name)
    yang_if.create_path('config/enabled', enabled)
    yang_if.create_path('config/mtu',     mtu    )

    yang_sifs : libyang.DContainer = yang_if.create_path('subinterfaces')
    yang_sif_path = 'subinterface[index="{:d}"]'.format(sif_index)
    yang_sif : libyang.DContainer = yang_sifs.create_path(yang_sif_path)
    yang_sif.create_path('config/index',   sif_index)
    yang_sif.create_path('config/enabled', enabled  )

    yang_ipv4 : libyang.DContainer = yang_sif.create_path('openconfig-if-ip:ipv4')
    yang_ipv4.create_path('config/enabled', enabled)

    yang_ipv4_addrs : libyang.DContainer = yang_ipv4.create_path('addresses')
    yang_ipv4_addr_path = 'address[ip="{:s}"]'.format(address_ip)
    yang_ipv4_addr : libyang.DContainer = yang_ipv4_addrs.create_path(yang_ipv4_addr_path)
    yang_ipv4_addr.create_path('config/ip',            address_ip    )
    yang_ipv4_addr.create_path('config/prefix-length', address_prefix)

    yang_ipv4_addr_path2 = 'address[ip="{:s}"]'.format(address_ip2)
    yang_ipv4_addr2 : libyang.DContainer = yang_ipv4_addrs.create_path(yang_ipv4_addr_path2)
    yang_ipv4_addr2.create_path('config/ip',            address_ip2   )
    yang_ipv4_addr2.create_path('config/prefix-length', address_prefix)

    str_data = yang_if.print_mem('json')
    json_data = json.loads(str_data)
    json_data = json_data['openconfig-interfaces:interface'][0]
    str_data = json.dumps(json_data, indent=4)
    LOGGER.info('Resulting Request (before unlink): {:s}'.format(str_data))

    yang_ipv4_addr2.unlink()

    root_node : libyang.DContainer = yang_handler.get_data_path('/openconfig-interfaces:interfaces')
    LOGGER.info('root_node={:s}'.format(str(root_node.print_mem('json'))))

    for s in root_node.siblings():
        LOGGER.info('sibling: {:s}'.format(str(s)))

    PATH_TMPL = '/openconfig-interfaces:interfaces/interface[name="{:s}"]/subinterfaces/subinterface[index="{:d}"]'
    yang_sif = root_node.find_path(PATH_TMPL.format(if_name, sif_index))
    if yang_sif is not None:
        LOGGER.info('yang_sif={:s}'.format(str(yang_sif.print_mem('json'))))
        yang_sif.unlink()
        yang_sif.free()

    str_data = yang_if.print_mem('json')
    json_data = json.loads(str_data)
    json_data = json_data['openconfig-interfaces:interface'][0]
    str_data = json.dumps(json_data, indent=4)
    LOGGER.info('Resulting Request (after unlink): {:s}'.format(str_data))

    yang_handler.destroy()

if __name__ == '__main__':
    main()
