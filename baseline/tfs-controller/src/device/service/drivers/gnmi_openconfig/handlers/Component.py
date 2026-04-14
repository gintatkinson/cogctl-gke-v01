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

import json, logging, re # libyang
from typing import Any, Dict, List, Tuple
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from ._Handler import _Handler
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

PATH_IF_CTR = '/openconfig-interfaces:interfaces/interface[name={:s}]/state/counters/{:s}'

#pylint: disable=abstract-method
class ComponentHandler(_Handler):
    def get_resource_key(self) -> str: return '/endpoints/endpoint'
    def get_path(self) -> str: return '/openconfig-platform:components'

    def parse(
        self, json_data : Dict, yang_handler : YangHandler
    ) -> List[Tuple[str, Dict[str, Any]]]:
        LOGGER.debug('json_data = {:s}'.format(json.dumps(json_data)))

        yang_components_path = self.get_path()
        json_data_valid = yang_handler.parse_to_dict(yang_components_path, json_data, fmt='json')

        entries = []
        for component in json_data_valid['components']['component']:
            LOGGER.debug('component={:s}'.format(str(component)))

            component_name = component['name']
            #component_config = component.get('config', {})

            #yang_components : libyang.DContainer = yang_handler.get_data_path(yang_components_path)
            #yang_component_path = 'component[name="{:s}"]'.format(component_name)
            #yang_component : libyang.DContainer = yang_components.create_path(yang_component_path)
            #yang_component.merge_data_dict(component, strict=True, validate=False)

            component_state = component.get('state', {})
            component_type = component_state.get('type')
            if component_type is None: continue
            component_type = component_type.split(':')[-1]
            if component_type not in {'PORT'}: continue

            # TODO: improve mapping between interface name and component name
            # By now, computed by time for the sake of saving time for the Hackfest.
            interface_name = re.sub(r'\-[pP][oO][rR][tT]', '', component_name)

            endpoint = {'uuid': interface_name, 'type': '-'}
            endpoint['sample_types'] = {
                KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED     : PATH_IF_CTR.format(interface_name, 'in-octets' ),
                KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED  : PATH_IF_CTR.format(interface_name, 'out-octets'),
                KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED   : PATH_IF_CTR.format(interface_name, 'in-pkts'   ),
                KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED: PATH_IF_CTR.format(interface_name, 'out-pkts'  ),
            }

            entries.append(('/endpoints/endpoint[{:s}]'.format(endpoint['uuid']), endpoint))

        return entries
