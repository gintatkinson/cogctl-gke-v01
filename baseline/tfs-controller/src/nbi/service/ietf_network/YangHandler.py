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

import json
import libyang, logging, os
from typing import Any
from common.proto.context_pb2 import TopologyDetails, Device, Link
from .NameMapping import NameMappings
from context.client.ContextClient import ContextClient
from common.tools.object_factory.Device import json_device_id
from common.proto.context_pb2 import DeviceId

LOGGER = logging.getLogger(__name__)

YANG_DIR = os.path.join(os.path.dirname(__file__), 'yang')
YANG_MODULES = ['ietf-network', 'ietf-network-topology', 'ietf-l3-unicast-topology']

class YangHandler:
    def __init__(self) -> None:
        self._yang_context = libyang.Context(YANG_DIR)
        for yang_module_name in YANG_MODULES:
            LOGGER.info('Loading module: {:s}'.format(str(yang_module_name)))
            self._yang_context.load_module(yang_module_name).feature_enable_all()

    def compose_network(self, te_topology_name: str, topology_details: TopologyDetails) -> dict:
        networks = self._yang_context.create_data_path('/ietf-network:networks')
        network = networks.create_path(f'network[network-id="{te_topology_name}"]')
        network.create_path('network-id', te_topology_name)

        network_types = network.create_path('network-types')
        network_types.create_path('ietf-l3-unicast-topology:l3-unicast-topology')

        name_mappings = NameMappings()

        for device in topology_details.devices:
            self.compose_node(device, name_mappings, network)

        for link in topology_details.links:
            self.compose_link(link, name_mappings, network)

        return json.loads(networks.print_mem('json'))

    def compose_node(self, dev: Device, name_mappings: NameMappings, network: Any) -> None:
        device_name = dev.name
        name_mappings.store_device_name(dev)

        node = network.create_path(f'node[node-id="{device_name}"]')
        node.create_path('node-id', device_name)
        node_attributes = node.create_path('ietf-l3-unicast-topology:l3-node-attributes')
        node_attributes.create_path('name', device_name)

        context_client = ContextClient()
        device = context_client.GetDevice(DeviceId(**json_device_id(device_name)))

        for endpoint in device.device_endpoints:
            name_mappings.store_endpoint_name(dev, endpoint)

        self._process_device_config(device, node)

    def _process_device_config(self, device: Device, node: Any) -> None:
        for config in device.device_config.config_rules:
            if config.WhichOneof('config_rule') != 'custom' or '/interface[' not in config.custom.resource_key:
                continue

            for endpoint in device.device_endpoints:
                endpoint_name = endpoint.name
                if f'/interface[{endpoint_name}]' in config.custom.resource_key or f'/interface[{endpoint_name}.' in config.custom.resource_key:
                    interface_name = config.custom.resource_key.split('interface[')[1].split(']')[0]
                    self._create_termination_point(node, interface_name, endpoint_name, config.custom.resource_value)

    def _create_termination_point(self, node: Any, interface_name: str, endpoint_name: str, resource_value: str) -> None:
        ip_addresses = self._extract_ip_addresses(json.loads(resource_value))
        if ip_addresses:
            tp = node.create_path(f'ietf-network-topology:termination-point[tp-id="{interface_name}"]')
            tp.create_path('tp-id', interface_name)
            tp_attributes = tp.create_path('ietf-l3-unicast-topology:l3-termination-point-attributes')

            for ip in ip_addresses:
                tp_attributes.create_path('ip-address', ip)
            tp_attributes.create_path('interface-name', endpoint_name)

    @staticmethod
    def _extract_ip_addresses(resource_value: dict) -> list:
        ip_addresses = []
        if 'address_ip' in resource_value:
            ip_addresses.append(resource_value['address_ip'])
        if 'address_ipv6' in resource_value:
            ip_addresses.append(resource_value['address_ipv6'])
        return ip_addresses

    def compose_link(self, link_specs: Link, name_mappings: NameMappings, network: Any) -> None:
        link_name = link_specs.name
        links = network.create_path(f'ietf-network-topology:link[link-id="{link_name}"]')
        links.create_path('link-id', link_name)

        self._create_link_endpoint(links, 'source', link_specs.link_endpoint_ids[0], name_mappings)
        self._create_link_endpoint(links, 'destination', link_specs.link_endpoint_ids[-1], name_mappings)

    def _create_link_endpoint(self, links: Any, endpoint_type: str, endpoint_id: Any, name_mappings: NameMappings) -> None:
        endpoint = links.create_path(endpoint_type)
        if endpoint_type == 'destination': endpoint_type = 'dest'
        endpoint.create_path(f'{endpoint_type}-node', name_mappings.get_device_name(endpoint_id.device_id))
        endpoint.create_path(f'{endpoint_type}-tp', name_mappings.get_endpoint_name(endpoint_id))

    def destroy(self) -> None:
        self._yang_context.destroy()
