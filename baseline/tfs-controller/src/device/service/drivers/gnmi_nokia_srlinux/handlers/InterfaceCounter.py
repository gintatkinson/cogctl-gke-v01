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
from .Tools import dict_get_first

LOGGER = logging.getLogger(__name__)

class InterfaceCounterHandler(_Handler):
    def get_resource_key(self) -> str: return '/interface/counters'
    def get_path(self) -> str: return '/interfaces/interface/state/counters'

    def parse(self, json_data : Dict) -> List[Tuple[str, Dict[str, Any]]]:
        LOGGER.info('[parse] json_data = {:s}'.format(json.dumps(json_data)))
        json_interface_list : List[Dict] = json_data.get('interface', [])

        response = []
        for json_interface in json_interface_list:
            LOGGER.info('[parse] json_interface = {:s}'.format(json.dumps(json_interface)))

            interface = {}

            NAME_FIELDS = ('name', 'openconfig-interface:name', 'oci:name')
            interface_name = dict_get_first(json_interface, NAME_FIELDS)
            if interface_name is None: continue
            interface['name'] = interface_name

            STATE_FIELDS = ('state', 'openconfig-interface:state', 'oci:state')
            json_state = dict_get_first(json_interface, STATE_FIELDS, default={})

            COUNTERS_FIELDS = ('counters', 'openconfig-interface:counters', 'oci:counters')
            json_counters = dict_get_first(json_state, COUNTERS_FIELDS, default={})

            IN_PKTS_FIELDS = ('in-pkts', 'openconfig-interface:in-pkts', 'oci:in-pkts')
            interface_in_pkts = dict_get_first(json_counters, IN_PKTS_FIELDS)
            if interface_in_pkts is not None: interface['in-pkts'] = int(interface_in_pkts)

            IN_OCTETS_FIELDS = ('in-octets', 'openconfig-interface:in-octets', 'oci:in-octets')
            interface_in_octets = dict_get_first(json_counters, IN_OCTETS_FIELDS)
            if interface_in_octets is not None: interface['in-octets'] = int(interface_in_octets)

            IN_ERRORS_FIELDS = ('in-errors', 'openconfig-interface:in-errors', 'oci:in-errors')
            interface_in_errors = dict_get_first(json_counters, IN_ERRORS_FIELDS)
            if interface_in_errors is not None: interface['in-errors'] = int(interface_in_errors)

            OUT_OCTETS_FIELDS = ('out-octets', 'openconfig-interface:out-octets', 'oci:out-octets')
            interface_out_octets = dict_get_first(json_counters, OUT_OCTETS_FIELDS)
            if interface_out_octets is not None: interface['out-octets'] = int(interface_out_octets)

            OUT_PKTS_FIELDS = ('out-pkts', 'openconfig-interface:out-pkts', 'oci:out-pkts')
            interface_out_pkts = dict_get_first(json_counters, OUT_PKTS_FIELDS)
            if interface_out_pkts is not None: interface['out-pkts'] = int(interface_out_pkts)

            OUT_ERRORS_FIELDS = ('out-errors', 'openconfig-interface:out-errors', 'oci:out-errors')
            interface_out_errors = dict_get_first(json_counters, OUT_ERRORS_FIELDS)
            if interface_out_errors is not None: interface['out-errors'] = int(interface_out_errors)

            OUT_DISCARDS_FIELDS = ('out-discards', 'openconfig-interface:out-discards', 'oci:out-discards')
            interface_out_discards = dict_get_first(json_counters, OUT_DISCARDS_FIELDS)
            if interface_out_discards is not None: interface['out-discards'] = int(interface_out_discards)

            #LOGGER.info('[parse] interface = {:s}'.format(str(interface)))

            if len(interface) == 0: continue
            response.append(('/interface[{:s}]'.format(interface['name']), interface))

        return response
