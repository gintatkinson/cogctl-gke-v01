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
from .Tools import add_value_from_collection, add_value_from_tag

LOGGER = logging.getLogger(__name__)

XPATH_NETWORK_INSTANCES = "//ocni:network-instances/ocni:network-instance"
XPATH_NI_PROTOCOLS      = ".//ocni:protocols/ocni:protocol"
XPATH_NI_TABLE_CONNECTS = ".//ocni:table-connections/ocni:table-connection"

XPATH_NI_INTERFACE      = ".//ocni:interfaces/ocni:interface"

XPATH_NI_IIP_AP         = ".//ocni:inter-instance-policies/ocni:apply-policy"
XPATH_NI_IIP_AP_IMPORT  = ".//ocni:config/ocni:import-policy"
XPATH_NI_IIP_AP_EXPORT  = ".//ocni:config/ocni:export-policy"

XPATH_NI_CPOINTS          = ".//ocni:connection-points/ocni:connection-point"
XPATH_NI_CPOINTS_ENDPOINT = ".//ocni:endpoints/ocni:endpoint/ocni:remote/ocni:config"

def parse(xml_data : ET.Element) -> List[Tuple[str, Dict[str, Any]]]:
    response = []
    for xml_network_instance in xml_data.xpath(XPATH_NETWORK_INSTANCES, namespaces=NAMESPACES):
        #LOGGER.info('xml_network_instance = {:s}'.format(str(ET.tostring(xml_network_instance))))

        network_instance = {}

        ni_name = xml_network_instance.find('ocni:name', namespaces=NAMESPACES)
        if ni_name is None or ni_name.text is None: continue
        add_value_from_tag(network_instance, 'name', ni_name)

        '''
        ni_type = xml_network_instance.find('ocni:config/ocni:type', namespaces=NAMESPACES)
        ni_type.text = ni_type.text.replace('oc-ni-types:','')
        add_value_from_tag(network_instance, 'type', ni_type)
        '''

        if xml_network_instance.find('ocni:config/ocni:type', namespaces=NAMESPACES) is not None:
            ni_type = xml_network_instance.find('ocni:config/ocni:type', namespaces=NAMESPACES)
        elif xml_network_instance.find('oci:state/oci:type', namespaces=NAMESPACES) is not None:
            ni_type = xml_network_instance.find('oci:state/oci:type', namespaces=NAMESPACES)
        else:
            continue
        if 'oc-ni-types:' in ni_type.text:
            ni_type.text = ni_type.text.replace('oc-ni-types:', '')                 #ADVA
        elif 'idx'in ni_type.text:
            ni_type.text = ni_type.text.replace('idx:', '')                         #CISCO
        add_value_from_tag(network_instance, 'type', ni_type)

        ni_router_id = xml_network_instance.find('ocni:config/ocni:router-id', namespaces=NAMESPACES)
        add_value_from_tag(network_instance, 'router_id', ni_router_id)

        ni_route_dist = xml_network_instance.find('ocni:config/ocni:route-distinguisher', namespaces=NAMESPACES)
        add_value_from_tag(network_instance, 'route_distinguisher', ni_route_dist)

        #ni_address_families = []
        #add_value_from_collection(network_instance, 'address_families', ni_address_families)

        if len(network_instance) == 0: continue
        response.append(('/network_instance[{:s}]'.format(network_instance['name']), network_instance))

        for xml_cpoints in xml_network_instance.xpath(XPATH_NI_PROTOCOLS, namespaces=NAMESPACES):
            cpoint = {}
            add_value_from_tag(cpoint, 'name', ni_name)

            connection_point = xml_cpoints.find('ocni:connection-point-id', namespaces=NAMESPACES)
            add_value_from_tag(cpoint, 'connection_point', connection_point)

            for xml_endpoint in xml_cpoints.xpath(XPATH_NI_CPOINTS_ENDPOINT, namespaces=NAMESPACES):
                remote_system = xml_endpoint.find('ocni:remote-system', namespaces=NAMESPACES)
                add_value_from_tag(cpoint, 'remote_system', remote_system)

                VC_ID = xml_endpoint.find('ocni:virtual-circuit-identifier', namespaces=NAMESPACES)
                add_value_from_tag(cpoint, 'VC_ID', VC_ID)

        for xml_protocol in xml_network_instance.xpath(XPATH_NI_PROTOCOLS, namespaces=NAMESPACES):
            #LOGGER.info('xml_protocol = {:s}'.format(str(ET.tostring(xml_protocol))))

            protocol = {}
            add_value_from_tag(protocol, 'name', ni_name)

            identifier = xml_protocol.find('ocni:identifier', namespaces=NAMESPACES)
            if identifier is None: identifier = xml_protocol.find('ocpt:identifier', namespaces=NAMESPACES)
            if identifier is None: identifier = xml_protocol.find('ocpt2:identifier', namespaces=NAMESPACES)
            if identifier is None or identifier.text is None: continue
            add_value_from_tag(protocol, 'identifier', identifier, cast=lambda s: s.replace('oc-pol-types:', ''))

            name = xml_protocol.find('ocni:name', namespaces=NAMESPACES)
            add_value_from_tag(protocol, 'protocol_name', name)

            if protocol['identifier'] == 'BGP':
                bgp_as = xml_protocol.find('ocni:bgp/ocni:global/ocni:config/ocni:as', namespaces=NAMESPACES)
                add_value_from_tag(protocol, 'as', bgp_as, cast=int)
                bgp_id = xml_protocol.find('ocni:bgp/ocni:global/ocni:config/ocni:router-id', namespaces=NAMESPACES)
                add_value_from_tag(protocol, 'router_id', bgp_id)

            resource_key = '/network_instance[{:s}]/protocols[{:s}]'.format(
                network_instance['name'], protocol['identifier'])
            response.append((resource_key, protocol))

        for xml_table_connection in xml_network_instance.xpath(XPATH_NI_TABLE_CONNECTS, namespaces=NAMESPACES):
            #LOGGER.info('xml_table_connection = {:s}'.format(str(ET.tostring(xml_table_connection))))

            table_connection = {}
            add_value_from_tag(table_connection, 'name', ni_name)

            src_protocol = xml_table_connection.find('ocni:src-protocol', namespaces=NAMESPACES)
            add_value_from_tag(table_connection, 'src_protocol', src_protocol,
                               cast=lambda s: s.replace('oc-pol-types:', ''))

            dst_protocol = xml_table_connection.find('ocni:dst-protocol', namespaces=NAMESPACES)
            add_value_from_tag(table_connection, 'dst_protocol', dst_protocol,
                               cast=lambda s: s.replace('oc-pol-types:', ''))

            address_family = xml_table_connection.find('ocni:address-family', namespaces=NAMESPACES)
            add_value_from_tag(table_connection, 'address_family', address_family,
                               cast=lambda s: s.replace('oc-types:', ''))

            default_import_policy = xml_table_connection.find('ocni:config/ocni:default-import-policy', namespaces=NAMESPACES)
            add_value_from_tag(table_connection, 'default_import_policy', default_import_policy)

            resource_key = '/network_instance[{:s}]/table_connections[{:s}][{:s}][{:s}]'.format(
                network_instance['name'], table_connection['src_protocol'], table_connection['dst_protocol'],
                table_connection['address_family'])
            response.append((resource_key, table_connection))

        for xml_interface in xml_network_instance.xpath(XPATH_NI_INTERFACE, namespaces=NAMESPACES):
            LOGGER.info('xml_interfaces = {:s}'.format(str(ET.tostring(xml_interface))))

            interface = {}
            name_iface = xml_interface.find('ocni:config/ocni:interface', namespaces=NAMESPACES)
            if name_iface is None or name_iface.text is None: continue
            add_value_from_tag(interface, 'name_iface', name_iface)

            name_subiface = xml_interface.find('ocni:config/ocni:subinterface', namespaces=NAMESPACES)
            add_value_from_tag(interface, 'name_subiface', name_subiface)

            resource_key = '/network_instance[{:s}]/interface[{:s}]'.format(
                network_instance['name'], interface['name_iface'])
            response.append((resource_key, interface))

        for xml_iip_ap in xml_network_instance.xpath(XPATH_NI_IIP_AP, namespaces=NAMESPACES):
            #LOGGER.info('xml_iip_ap = {:s}'.format(str(ET.tostring(xml_iip_ap))))

            for xml_import_policy in xml_iip_ap.xpath(XPATH_NI_IIP_AP_IMPORT, namespaces=NAMESPACES):
                #LOGGER.info('xml_import_policy = {:s}'.format(str(ET.tostring(xml_import_policy))))
                if xml_import_policy.text is None: continue
                iip_ap = {}
                add_value_from_tag(iip_ap, 'name', ni_name)
                add_value_from_tag(iip_ap, 'import_policy', xml_import_policy)
                resource_key = '/network_instance[{:s}]/inter_instance_policies[{:s}]'.format(
                    iip_ap['name'], iip_ap['import_policy'])
                response.append((resource_key, iip_ap))

            for xml_export_policy in xml_iip_ap.xpath(XPATH_NI_IIP_AP_EXPORT, namespaces=NAMESPACES):
                #LOGGER.info('xml_export_policy = {:s}'.format(str(ET.tostring(xml_export_policy))))
                if xml_export_policy.text is None: continue
                iip_ap = {}
                add_value_from_tag(iip_ap, 'name', ni_name)
                add_value_from_tag(iip_ap, 'export_policy', xml_export_policy)
                resource_key = '/network_instance[{:s}]/inter_instance_policies[{:s}]'.format(
                    iip_ap['name'], iip_ap['export_policy'])
                response.append((resource_key, iip_ap))




    return response
