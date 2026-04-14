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
from typing     import Any, Dict, List, Tuple
from .Namespace import NAMESPACES
from .Tools     import add_value_from_tag

LOGGER = logging.getLogger(__name__)

XPATH_INTERFACES    = "//oci:interfaces/oci:interface"
XPATH_SUBINTERFACES = ".//oci:subinterfaces/oci:subinterface"
XPATH_IPV4ADDRESSES = ".//ociip:ipv4/ociip:addresses/ociip:address"
XPATH_IPV6ADDRESSES = ".//ociip:ipv6/ociip:addresses/ociip:address"

def parse(xml_data : ET.Element) -> List[Tuple[str, Dict[str, Any]]]:
    response = []
    for xml_interface in xml_data.xpath(XPATH_INTERFACES, namespaces=NAMESPACES):
        #LOGGER.info('xml_interface = {:s}'.format(str(ET.tostring(xml_interface))))

        interface = {}

        #interface_type = xml_interface.find('oci:config/oci:type', namespaces=NAMESPACES)
        #add_value_from_tag(interface, 'type', interface_type)

        if xml_interface.find('oci:config/oci:type', namespaces=NAMESPACES) is not None:
            interface_type = xml_interface.find('oci:config/oci:type', namespaces=NAMESPACES)
        elif xml_interface.find('oci:state/oci:type', namespaces=NAMESPACES) is not None:
            interface_type = xml_interface.find('oci:state/oci:type', namespaces=NAMESPACES)
        else: continue

        interface_name = xml_interface.find('oci:name', namespaces=NAMESPACES)
        if interface_name is None or interface_name.text is None: continue
        add_value_from_tag(interface, 'name', interface_name)

        # Get the type of interface according to the vendor's type
        if 'ianaift:' in interface_type.text:
            interface_type.text = interface_type.text.replace('ianaift:', '')                       #ADVA
        elif 'idx'in interface_type.text:
            interface_type.text = interface_type.text.replace('idx:', '')                           #CISCO
        add_value_from_tag(interface, 'type', interface_type)

        interface_mtu = xml_interface.find('oci:config/oci:mtu', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'mtu', interface_mtu, cast=int)

        interface_description = xml_interface.find('oci:config/oci:description', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'description', interface_description)

        for xml_subinterface in xml_interface.xpath(XPATH_SUBINTERFACES, namespaces=NAMESPACES):
            #LOGGER.info('xml_subinterface = {:s}'.format(str(ET.tostring(xml_subinterface))))

            subinterface = {}

            add_value_from_tag(subinterface, 'name', interface_name)
            add_value_from_tag(subinterface, 'mtu', interface_mtu)
            add_value_from_tag(subinterface, 'type', interface_type)


            subinterface_index = xml_subinterface.find('oci:index', namespaces=NAMESPACES)
            if subinterface_index is None or subinterface_index.text is None: continue
            add_value_from_tag(subinterface, 'index', subinterface_index, cast=int)

            vlan_id = xml_subinterface.find('ocv:vlan/ocv:match/ocv:single-tagged/ocv:config/ocv:vlan-id', namespaces=NAMESPACES)
            add_value_from_tag(subinterface, 'vlan_id', vlan_id, cast=int)

            # TODO: implement support for multiple IP addresses per subinterface
            #ipv4_addresses = []
            for xml_ipv4_address in xml_subinterface.xpath(XPATH_IPV4ADDRESSES, namespaces=NAMESPACES):
                #LOGGER.info('xml_ipv4_address = {:s}'.format(str(ET.tostring(xml_ipv4_address))))

                #ipv4_address = {}

                #origin = xml_ipv4_address.find('ociip:state/ociip:origin', namespaces=NAMESPACES)
                #add_value_from_tag(ipv4_address, 'origin', origin)

                address = xml_ipv4_address.find('ociip:state/ociip:ip', namespaces=NAMESPACES)
                #add_value_from_tag(ipv4_address, 'ip', address)
                add_value_from_tag(subinterface, 'address_ip', address)

                prefix = xml_ipv4_address.find('ociip:state/ociip:prefix-length', namespaces=NAMESPACES)
                #add_value_from_tag(ipv4_address, 'prefix_length', prefix)
                add_value_from_tag(subinterface, 'address_prefix', prefix, cast=int)

                #if len(ipv4_address) == 0: continue
                #ipv4_addresses.append(ipv4_address)

            #add_value_from_collection(subinterface, 'ipv4_addresses', ipv4_addresses)

            for xml_ipv6_address in xml_subinterface.xpath(XPATH_IPV6ADDRESSES, namespaces=NAMESPACES):
                #LOGGER.info('xml_ipv6_address = {:s}'.format(str(ET.tostring(xml_ipv6_address))))

                address = xml_ipv6_address.find('ociip:state/ociip:ip', namespaces=NAMESPACES)
                add_value_from_tag(subinterface, 'address_ipv6', address)

                prefix = xml_ipv6_address.find('ociip:state/ociip:prefix-length', namespaces=NAMESPACES)
                add_value_from_tag(subinterface, 'address_prefix_v6', prefix, cast=int)

            if len(subinterface) == 0: continue
            resource_key = '/interface[{:s}]/subinterface[{:s}]'.format(interface['name'], str(subinterface['index']))
            response.append((resource_key, subinterface))

        if len(interface) == 0: continue
        response.append(('/interface[{:s}]'.format(interface['name']), interface))

    return response

def parse_counters(xml_data : ET.Element) -> List[Tuple[str, Dict[str, Any]]]:
    response = []
    for xml_interface in xml_data.xpath(XPATH_INTERFACES, namespaces=NAMESPACES):
        #LOGGER.info('[parse_counters] xml_interface = {:s}'.format(str(ET.tostring(xml_interface))))

        interface = {}

        interface_name = xml_interface.find('oci:name', namespaces=NAMESPACES)
        if interface_name is None or interface_name.text is None: continue
        add_value_from_tag(interface, 'name', interface_name)

        interface_in_pkts = xml_interface.find('oci:state/oci:counters/oci:in-pkts', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'in-pkts', interface_in_pkts, cast=int)

        interface_in_octets = xml_interface.find('oci:state/oci:counters/oci:in-octets', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'in-octets', interface_in_octets, cast=int)

        interface_in_errors = xml_interface.find('oci:state/oci:counters/oci:in-errors', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'in-errors', interface_in_errors, cast=int)

        interface_out_octets = xml_interface.find('oci:state/oci:counters/oci:out-octets', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'out-octets', interface_out_octets, cast=int)

        interface_out_pkts = xml_interface.find('oci:state/oci:counters/oci:out-pkts', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'out-pkts', interface_out_pkts, cast=int)

        interface_out_errors = xml_interface.find('oci:state/oci:counters/oci:out-errors', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'out-errors', interface_out_errors, cast=int)

        interface_out_discards = xml_interface.find('oci:state/oci:counters/oci:out-discards', namespaces=NAMESPACES)
        add_value_from_tag(interface, 'out-discards', interface_out_discards, cast=int)

        #LOGGER.info('[parse_counters] interface = {:s}'.format(str(interface)))

        if len(interface) == 0: continue
        response.append(('/interface[{:s}]'.format(interface['name']), interface))

    return response
