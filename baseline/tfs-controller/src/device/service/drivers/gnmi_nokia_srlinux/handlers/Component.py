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
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from ._Handler import _Handler

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

#PATH_IF_CTR = "/interfaces/interface[name={:s}]/state/counters/{:s}"

class ComponentHandler(_Handler):
    def get_resource_key(self) -> str: return '/endpoints/endpoint'
    def get_path(self) -> str: return '/srl_nokia-interfaces:interface'

    def parse(self, json_data : Dict) -> List[Tuple[str, Dict[str, Any]]]:
        LOGGER.info('json_data = {:s}'.format(json.dumps(json_data)))
        json_interface_list : List[Dict] = json_data.get('srl_nokia-interfaces:interface', [])
        response = []
        for json_component in json_interface_list:
            #LOGGER.info('json_component = {:s}'.format(json.dumps(json_component)))
            endpoint = {}
            interface_name = json_component.get('name')
            if interface_name is None:
            #    LOGGER.info('DISCARDED json_interface = {:s}'.format(json.dumps(json_interface)))
                continue
            endpoint['uuid'] = interface_name
            endpoint['name'] = interface_name

            #endpoint_type1 = json_component.get('srl_nokia-platform-healthz:healthz', {})
            endpoint_type = json_component.get('ethernet', {})
            port_speed = endpoint_type.get('port-speed')
            if port_speed is not None: endpoint['type'] = port_speed

            #endpoint['sample_types'] = {
            #    KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED     : PATH_IF_CTR.format(interface_name, 'in-octets' ),
            #    KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED  : PATH_IF_CTR.format(interface_name, 'out-octets'),
            #    KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED   : PATH_IF_CTR.format(interface_name, 'in-pkts'   ),
            #    KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED: PATH_IF_CTR.format(interface_name, 'out-pkts'  ),
            #}

            if len(endpoint) == 0: continue
            response.append(('/endpoints/endpoint[{:s}]'.format(endpoint['uuid']) , endpoint))
        return response
