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

import copy, json, libyang, logging, os
from typing import Dict, List, Optional

LOGGER = logging.getLogger(__name__)

YANG_DIR = os.path.join(os.path.dirname(__file__), 'yang')
YANG_MODULES = [
    'ietf-yang-types',
    'ietf-interfaces',
    'iana-if-type',
    'ietf-access-control-list',
]

class YangValidator:
    def __init__(self) -> None:
        self._yang_context = libyang.Context(YANG_DIR)
        for module_name in YANG_MODULES:
            LOGGER.info('Loading module: {:s}'.format(str(module_name)))
            yang_module = self._yang_context.load_module(module_name)
            yang_module.feature_enable_all()
            yang_module_prefix = yang_module.prefix()
            LOGGER.info('  Prefix: {:s}'.format(str(yang_module_prefix)))

    def parse_to_dict(self, message : Dict, interface_names : List[str]) -> Dict:
        interfaces = self._yang_context.create_data_path('/ietf-interfaces:interfaces')
        for if_index,interface_name in enumerate(interface_names):
            if_path = 'interface[name="{:s}"]'.format(str(interface_name))
            interface = interfaces.create_path(if_path)
            interface.create_path('if-index', if_index + 1)
            interface.create_path('type', 'iana-if-type:ethernetCsmacd')
            interface.create_path('admin-status', 'up')
            interface.create_path('oper-status', 'up')
            statistics = interface.create_path('statistics')
            statistics.create_path('discontinuity-time', '2024-07-11T10:00:00.000000Z')

        message = copy.deepcopy(message)
        message['ietf-interfaces:interfaces'] = interfaces.print_dict()['interfaces']

        dnode : Optional[libyang.DNode] = self._yang_context.parse_data_mem(
            json.dumps(message), 'json', validate_present=True, strict=True
        )
        if dnode is None: raise Exception('Unable to parse Message({:s})'.format(str(message)))
        message = dnode.print_dict()
        dnode.free()
        interfaces.free()
        return message

    def destroy(self) -> None:
        self._yang_context.destroy()
        self._yang_context = None

def main() -> None:
    import uuid # pylint: disable=import-outside-toplevel
    logging.basicConfig(level=logging.DEBUG)

    interface_names = {'200', '500', str(uuid.uuid4()), str(uuid.uuid4())}
    ACL_RULE = {"ietf-access-control-list:acls": {
        "acl": [{
            "name": "sample-ipv4-acl", "type": "ipv4-acl-type",
            "aces": {"ace": [{
                "name": "rule1",
                "matches": {
                    "ipv4": {
                        "source-ipv4-network": "128.32.10.6/24",
                        "destination-ipv4-network": "172.10.33.0/24",
                        "dscp": 18
                    },
                    "tcp": {
                        "source-port": {"operator": "eq", "port": 1444},
                        "destination-port": {"operator": "eq", "port": 1333},
                        "flags": "syn"
                    }
                },
                "actions": {"forwarding": "drop"}
            }]}
        }],
        "attachment-points": {"interface": [{
            "interface-id": "200",
            "ingress": {"acl-sets": {"acl-set": [{"name": "sample-ipv4-acl"}]}}
        }]
    }}}

    yang_validator = YangValidator()
    request_data = yang_validator.parse_to_dict(ACL_RULE, list(interface_names))
    yang_validator.destroy()

    LOGGER.info('request_data = {:s}'.format(str(request_data)))

if __name__ == '__main__':
    main()
