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
from .Namespace import NAMESPACES
from .Tools import add_value_from_tag

LOGGER = logging.getLogger(__name__)

XPATH_PORTS = "//ocp:components/ocp:component"

"""
#Method Name: parse

#Parameters:

    - xml_data: [ET.Element] Represents the XML data to be parsed.

# Functionality:

    The parse function of the inventerio class has the functionality to parse
    an XML document represented by the xml_data parameter and extract specific
    information from the XML elements, namely the relevant characteristics of the
    components.

    To generate the template the following steps are performed:

    1) An empty list called response is created to store the results of the analysis.

    2) Iterate over the XML elements that match the pattern specified by the XPATH_PORTS
    expression. These elements represent components in the XML document.

    3) For each component element:
    A dictionary called inventory is initialized that will store the information extracted
    from the component.The values of the relevant XML elements are extracted and added to
    the dictionary.

#Return:
    List[Tuple[str, Dict[str, Any]]] The response list containing the tuples (path, dictionary)
    with the information extracted from the XML document components is returned.
"""

def parse(xml_data : ET.Element) -> List[Tuple[str, Dict[str, Any]]]:
    response = []
    parent_types = {}
    for xml_component in xml_data.xpath(XPATH_PORTS, namespaces=NAMESPACES):
        LOGGER.info('xml_component inventario = {:s}'.format(str(ET.tostring(xml_component))))
        inventory = {}
        inventory['parent-component-references'] = ''
        inventory['name'] = ''
        inventory['class'] = ''
        inventory['attributes'] = {}
        component_reference = []

        component_name = xml_component.find('ocp:name', namespaces=NAMESPACES)
        if component_name is None or component_name.text is None: continue
        add_value_from_tag(inventory, 'name', component_name)

        component_description = xml_component.find('ocp:state/ocp:description', namespaces=NAMESPACES)
        if not component_description is None:
            add_value_from_tag(inventory['attributes'], 'description', component_description)

        component_location = xml_component.find('ocp:state/ocp:location', namespaces=NAMESPACES)
        if not component_location is None:
            add_value_from_tag(inventory['attributes'], 'location', component_location)

        component_id = xml_component.find('ocp:state/ocp:id', namespaces=NAMESPACES)
        if not component_id is None:
            add_value_from_tag(inventory['attributes'], 'id', component_id)

        component_type = xml_component.find('ocp:state/ocp:type', namespaces=NAMESPACES)
        if component_type is not None:
            component_type.text = component_type.text.replace('oc-platform-types:','')
            add_value_from_tag(inventory, 'class', component_type)

        if inventory['class'] == 'CPU' or inventory['class'] == 'STORAGE': continue

        component_empty = xml_component.find('ocp:state/ocp:empty', namespaces=NAMESPACES)
        if not component_empty is None:
            add_value_from_tag(inventory['attributes'], 'empty', component_empty)

        component_parent = xml_component.find('ocp:state/ocp:parent', namespaces=NAMESPACES)
        if not component_parent is None:
            add_value_from_tag(inventory, 'parent-component-references', component_parent)

        component_HW = xml_component.find('ocp:state/ocp:hardware-version', namespaces=NAMESPACES)
        if not component_HW is None:
            add_value_from_tag(inventory['attributes'], 'hardware-rev', component_HW)

        component_firmware_version = xml_component.find('ocp:state/ocp:firmware-version', namespaces=NAMESPACES)
        if not component_firmware_version is None:
            add_value_from_tag(inventory['attributes'], 'firmware-rev', component_firmware_version)

        component_SW = xml_component.find('ocp:state/ocp:software-version', namespaces=NAMESPACES)
        if not component_SW is None:
            add_value_from_tag(inventory['attributes'], 'software-rev', component_SW)

        component_serial = xml_component.find('ocp:state/ocp:serial-no', namespaces=NAMESPACES)
        if not component_serial is None:
            add_value_from_tag(inventory['attributes'], 'serial-num', component_serial)

        component_mfg_name = xml_component.find('ocp:state/ocp:mfg-name', namespaces=NAMESPACES)
        if not component_mfg_name is None:
            add_value_from_tag(inventory['attributes'], 'mfg-name', component_mfg_name)

        component_removable = xml_component.find('ocp:state/ocp:removable', namespaces=NAMESPACES)
        if not component_removable is None:
            add_value_from_tag(inventory['attributes'], 'removable', component_removable)

        component_mfg_date = xml_component.find('ocp:state/ocp:mfg-date', namespaces=NAMESPACES)
        if not component_mfg_date is None:
            add_value_from_tag(inventory['attributes'], 'mfg-date', component_mfg_date)

        #Transceiver Information
        component_serial_t = xml_component.find('ocptr:transceiver/ocptr:state/ocptr:serial-no', namespaces=NAMESPACES)
        if not component_serial_t is None:
            add_value_from_tag(inventory['attributes'], 'serial-num', component_serial_t)

        component_present = xml_component.find('ocptr:transceiver/ocptr:state/ocptr:present', namespaces=NAMESPACES)
        if component_present is not None and 'NOT_PRESENT' in component_present.text: continue

        component_vendor = xml_component.find('ocptr:transceiver/ocptr:state/ocptr:vendor', namespaces=NAMESPACES)
        if not component_vendor is None:
            add_value_from_tag(inventory['attributes'], 'vendor', component_vendor)
        component_connector = xml_component.find('ocptr:transceiver/ocptr:state/ocptr:connector-type', namespaces=NAMESPACES)
        if not component_connector is None:
            component_connector.text = component_connector.text.replace('oc-opt-types:','')
            add_value_from_tag(inventory['attributes'], 'connector-type', component_connector)

        component_form = xml_component.find('ocptr:transceiver/ocptr:state/ocptr:form-factor', namespaces=NAMESPACES)
        if not component_form is None:
            component_form.text = component_form.text.replace('oc-opt-types:','')
            add_value_from_tag(inventory['attributes'], 'form-factor', component_form)

        if inventory['parent-component-references'] not in parent_types:
            parent_types[inventory['parent-component-references']] = len(parent_types) + 1

        component_reference.extend([parent_types[inventory['parent-component-references']]])

        response.append(('/inventory/{:s}'.format(inventory['name']), inventory))

        for tupla in response:
            if inventory['parent-component-references'] in tupla[0]:
                component_reference.extend([tupla[1]['class']])

        inventory['component-reference'] = component_reference

    return response
