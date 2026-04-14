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

XPATH_ACL_SET     = "//ocacl:acl/ocacl:acl-sets/ocacl:acl-set"
XPATH_A_ACL_ENTRY = ".//ocacl:acl-entries/ocacl:acl-entry"
XPATH_A_IPv4      = ".//ocacl:ipv4/ocacl:config"
XPATH_A_TRANSPORT = ".//ocacl:transport/ocacl:config"
XPATH_A_ACTIONS   = ".//ocacl:actions/ocacl:config"

XPATH_INTERFACE   = "//ocacl:acl/ocacl:interfaces/ocacl:interface"
XPATH_I_INGRESS   = ".//ocacl:ingress-acl-sets/ocacl:ingress-acl-set"
XPATH_I_EGRESS    = ".//ocacl:egress-acl-sets/ocacl:egress-acl-set"

def parse(xml_data : ET.Element) -> List[Tuple[str, Dict[str, Any]]]:
    #LOGGER.info('[ACL] xml_data = {:s}'.format(str(ET.tostring(xml_data))))

    response = []
    acl = {}
    name = {}

    for xml_acl in xml_data.xpath(XPATH_ACL_SET, namespaces=NAMESPACES):
        #LOGGER.info('xml_acl = {:s}'.format(str(ET.tostring(xml_acl))))

        acl_name = xml_acl.find('ocacl:name', namespaces=NAMESPACES)
        if acl_name is None or acl_name.text is None: continue
        add_value_from_tag(name, 'name', acl_name)

        acl_type = xml_acl.find('ocacl:type', namespaces=NAMESPACES)
        add_value_from_tag(acl, 'type', acl_type)

        for xml_acl_entries in xml_acl.xpath(XPATH_A_ACL_ENTRY, namespaces=NAMESPACES):

            acl_id = xml_acl_entries.find('ocacl:sequence-id', namespaces=NAMESPACES)
            add_value_from_tag(acl, 'sequence-id', acl_id)
            LOGGER.info('xml_acl_id = {:s}'.format(str(ET.tostring(acl_id))))

            for xml_ipv4 in xml_acl_entries.xpath(XPATH_A_IPv4, namespaces=NAMESPACES):

                ipv4_source = xml_ipv4.find('ocacl:source-address', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'source-address' , ipv4_source)

                ipv4_destination = xml_ipv4.find('ocacl:destination-address', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'destination-address' , ipv4_destination)

                ipv4_protocol = xml_ipv4.find('ocacl:protocol', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'protocol' , ipv4_protocol)

                ipv4_dscp = xml_ipv4.find('ocacl:dscp', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'dscp' , ipv4_dscp)

                ipv4_hop_limit = xml_ipv4.find('ocacl:hop-limit', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'hop-limit' , ipv4_hop_limit)

            for xml_transport in xml_acl_entries.xpath(XPATH_A_TRANSPORT, namespaces=NAMESPACES):

                transport_source = xml_transport.find('ocacl:source-port', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'source-port' ,transport_source)

                transport_destination = xml_transport.find('ocacl:destination-port', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'destination-port' ,transport_destination)

                transport_tcp_flags = xml_transport.find('ocacl:tcp-flags', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'tcp-flags' ,transport_tcp_flags)

            for xml_action in xml_acl_entries.xpath(XPATH_A_ACTIONS, namespaces=NAMESPACES):

                action = xml_action.find('ocacl:forwarding-action', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'forwarding-action' ,action)

                log_action = xml_action.find('ocacl:log-action', namespaces=NAMESPACES)
                add_value_from_tag(acl, 'log-action' ,log_action)

            resource_key =  '/acl/acl-set[{:s}][{:s}]/acl-entry[{:s}]'.format(
                name['name'], acl['type'], acl['sequence-id'])
            response.append((resource_key,acl))

    for xml_interface in xml_data.xpath(XPATH_INTERFACE, namespaces=NAMESPACES):

        interface = {}

        interface_id = xml_interface.find('ocacl:id', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'id' , interface_id)

        for xml_ingress in xml_interface.xpath(XPATH_I_INGRESS, namespaces=NAMESPACES):

            i_name = xml_ingress.find('ocacl:set-name-ingress', namespaces=NAMESPACES)
            add_value_from_tag(interface, 'ingress-set-name' , i_name)

            i_type = xml_ingress.find('ocacl:type-ingress', namespaces=NAMESPACES)
            add_value_from_tag(interface, 'ingress-type' , i_type)

            resource_key =  '/acl/interfaces/ingress[{:s}][{:s}]'.format(
                name['name'], acl['type'])
            response.append((resource_key,interface))

        for xml_egress in xml_interface.xpath(XPATH_I_EGRESS, namespaces=NAMESPACES):

            e_name = xml_egress.find('ocacl:set-name-egress', namespaces=NAMESPACES)
            add_value_from_tag(interface, 'egress-set-name' , e_name)

            e_type = xml_egress.find('ocacl:type-egress', namespaces=NAMESPACES)
            add_value_from_tag(interface, 'egress-type' , e_type)

            resource_key =  '/acl/interfaces/egress[{:s}][{:s}]'.format(
                name['name'], acl['type'])
            response.append((resource_key,interface))
    return response
