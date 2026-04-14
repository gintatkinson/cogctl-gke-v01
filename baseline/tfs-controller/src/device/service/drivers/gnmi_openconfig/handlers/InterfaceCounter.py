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
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

#pylint: disable=abstract-method
class InterfaceCounterHandler(_Handler):
    def get_resource_key(self) -> str: return '/interface/counters'
    def get_path(self) -> str: return '/openconfig-interfaces:interfaces/interface/state/counters'

    def parse(
        self, json_data : Dict, yang_handler : YangHandler
    ) -> List[Tuple[str, Dict[str, Any]]]:
        LOGGER.debug('json_data = {:s}'.format(json.dumps(json_data)))

        yang_interfaces_path = self.get_path()
        json_data_valid = yang_handler.parse_to_dict(yang_interfaces_path, json_data, fmt='json')

        entries = []
        for interface in json_data_valid['interfaces']['interface']:
            LOGGER.debug('interface={:s}'.format(str(interface)))

            interface_name = interface['name']
            interface_counters = interface.get('state', {}).get('counters', {})
            _interface = {
                'name'              : interface_name,
                'in-broadcast-pkts' : interface_counters['in_broadcast_pkts' ],
                'in-discards'       : interface_counters['in_discards'       ],
                'in-errors'         : interface_counters['in_errors'         ],
                'in-fcs-errors'     : interface_counters['in_fcs_errors'     ],
                'in-multicast-pkts' : interface_counters['in_multicast_pkts' ],
                'in-octets'         : interface_counters['in_octets'         ],
                'in-pkts'           : interface_counters['in_pkts'           ],
                'in-unicast-pkts'   : interface_counters['in_unicast_pkts'   ],
                'out-broadcast-pkts': interface_counters['out_broadcast_pkts'],
                'out-discards'      : interface_counters['out_discards'      ],
                'out-errors'        : interface_counters['out_errors'        ],
                'out-multicast-pkts': interface_counters['out_multicast_pkts'],
                'out-octets'        : interface_counters['out_octets'        ],
                'out-pkts'          : interface_counters['out_pkts'          ],
                'out-unicast-pkts'  : interface_counters['out_unicast_pkts'  ],
            }
            LOGGER.debug('interface = {:s}'.format(str(interface)))

            entry_interface_key = '/interface[{:s}]'.format(interface_name)
            entries.append((entry_interface_key, _interface))

        return entries
