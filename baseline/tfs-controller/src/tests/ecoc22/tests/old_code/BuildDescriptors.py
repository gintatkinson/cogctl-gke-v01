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

# Execution:
# $ cd src
# $ python -m tests.ecoc22.tests.BuildDescriptors dc-csgw-tn
# $ python -m tests.ecoc22.tests.BuildDescriptors dc-csgw-tn-ols
# $ python -m tests.ecoc22.tests.BuildDescriptors bignet

import copy, json, os, sys
from enum import Enum
from typing import Dict, Tuple

class Scenario(Enum):
    BIGNET         = 'bignet'
    DC_CSGW_TN     = 'dc-csgw-tn'
    DC_CSGW_TN_OLS = 'dc-csgw-tn-ols'

scenario = None if len(sys.argv) < 2 else sys.argv[1].lower()

if scenario == Scenario.BIGNET.value:
    from .Objects_BigNet import CONTEXTS, DEVICES, LINKS, TOPOLOGIES
    FILENAME = 'tests/ecoc22/descriptors_emulated-BigNet.json'
elif scenario == Scenario.DC_CSGW_TN.value:
    os.environ['ADD_CONNECT_RULES_TO_DEVICES'] = 'TRUE'
    from .Objects_DC_CSGW_TN import CONTEXTS, DEVICES, LINKS, TOPOLOGIES
    FILENAME = 'tests/ecoc22/descriptors_emulated-DC_CSGW_TN.json'
elif scenario == Scenario.DC_CSGW_TN_OLS.value:
    os.environ['ADD_CONNECT_RULES_TO_DEVICES'] = 'TRUE'
    from .Objects_DC_CSGW_TN_OLS import CONTEXTS, DEVICES, LINKS, TOPOLOGIES
    FILENAME = 'tests/ecoc22/descriptors_emulated-DC_CSGW_TN_OLS.json'
else:
    scenarios = str([s.value for s in Scenario])
    raise Exception('Unsupported Scenario({:s}), choices are: {:s}'.format(scenario, scenarios))

def main():
    with open(FILENAME, 'w', encoding='UTF-8') as f:
        devices = []
        for item in DEVICES:
            if isinstance(item, Dict):
                device = item
            elif isinstance(item, Tuple) and len(item) == 2:
                device,connect_rules = item
            else:
                raise Exception('Wrongly formatted item: {:s}'.format(str(item)))
            device = copy.deepcopy(device)
            if len(item) == 2:
                device['device_config']['config_rules'].extend(connect_rules)
            devices.append(device)

        f.write(json.dumps({
            'contexts': CONTEXTS,
            'topologies': TOPOLOGIES,
            'devices': devices,
            'links': LINKS
        }, sort_keys=True, indent=4))
    return 0

if __name__ == '__main__':
    sys.exit(main())
