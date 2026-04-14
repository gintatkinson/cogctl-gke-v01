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

import logging, lxml.etree as ET
from typing import Any, Dict, List, Tuple
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from .Namespace import NAMESPACES
from .Tools import add_value_from_collection, add_value_from_tag

LOGGER = logging.getLogger(__name__)

XPATH_PORTS = "//ocp:components/ocp:component"
XPATH_IFACE_COUNTER = "//oci:interfaces/oci:interface[oci:name='{:s}']/state/counters/{:s}"

def parse(xml_data : ET.Element) -> List[Tuple[str, Dict[str, Any]]]:
    response = []
    for xml_component in xml_data.xpath(XPATH_PORTS, namespaces=NAMESPACES):
        #LOGGER.info('xml_component = {:s}'.format(str(ET.tostring(xml_component))))

        component_type = xml_component.find('ocp:state/ocp:type', namespaces=NAMESPACES)
        if component_type is None or component_type.text is None: continue
        component_type = component_type.text
        if component_type not in {'PORT', 'oc-platform-types:PORT', 'idx:PORT'}: continue

        LOGGER.info('PORT xml_component = {:s}'.format(str(ET.tostring(xml_component))))

        endpoint = {}

        component_name = xml_component.find('ocp:name', namespaces=NAMESPACES)
        if component_name is None or component_name.text is None: continue
        add_value_from_tag(endpoint, 'uuid', component_name)

        component_type = xml_component.find(
            'ocpp:port/ocpp:breakout-mode/ocpp:state/ocpp:channel-speed', namespaces=NAMESPACES)
        add_value_from_tag(endpoint, 'type', component_type)
        if 'type' not in endpoint: endpoint['type'] = '-'

        sample_types = {
            KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED     : XPATH_IFACE_COUNTER.format(endpoint['uuid'], 'in-octets' ),
            KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED  : XPATH_IFACE_COUNTER.format(endpoint['uuid'], 'out-octets'),
            KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED   : XPATH_IFACE_COUNTER.format(endpoint['uuid'], 'in-pkts'   ),
            KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED: XPATH_IFACE_COUNTER.format(endpoint['uuid'], 'out-pkts'  ),
        }
        add_value_from_collection(endpoint, 'sample_types', sample_types)

        if len(endpoint) == 0: continue
        response.append(('/endpoints/endpoint[{:s}]'.format(endpoint['uuid']), endpoint))
    return response
