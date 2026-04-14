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

import copy, json, sys
from .Objects import CONTEXTS, DEVICES, LINKS, TOPOLOGIES

def main():
    with open('tests/ofc22/descriptors_emulated.json', 'w', encoding='UTF-8') as f:
        devices = []
        for device,connect_rules in DEVICES:
            device = copy.deepcopy(device)
            device['device_config']['config_rules'].extend(connect_rules)
            devices.append(device)

        f.write(json.dumps({
            'contexts': CONTEXTS,
            'topologies': TOPOLOGIES,
            'devices': devices,
            'links': LINKS
        }))
    return 0

if __name__ == '__main__':
    sys.exit(main())
