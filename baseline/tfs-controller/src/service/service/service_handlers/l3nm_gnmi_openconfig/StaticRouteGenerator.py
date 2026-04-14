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

import json, logging, netaddr, sys
from typing import List, Optional, Tuple
from .ConfigRuleComposer import ConfigRuleComposer

LOGGER = logging.getLogger(__name__)

# Used to infer routing networks for adjacent ports when there is no hint in device/endpoint settings
ROOT_NEIGHBOR_ROUTING_NETWORK = netaddr.IPNetwork('10.254.254.0/16')
NEIGHBOR_ROUTING_NETWORKS_PREFIX_LEN = 30
NEIGHBOR_ROUTING_NETWORKS = set(ROOT_NEIGHBOR_ROUTING_NETWORK.subnet(NEIGHBOR_ROUTING_NETWORKS_PREFIX_LEN))

def _generate_neighbor_addresses() -> Tuple[netaddr.IPAddress, netaddr.IPAddress, int]:
    ip_network = NEIGHBOR_ROUTING_NETWORKS.pop()
    ip_addresses = list(ip_network.iter_hosts())
    ip_addresses.append(NEIGHBOR_ROUTING_NETWORKS_PREFIX_LEN)
    return ip_addresses

def _compute_gateway(ip_network : netaddr.IPNetwork, gateway_host=1) -> netaddr.IPAddress:
    return netaddr.IPAddress(ip_network.cidr.first + gateway_host)

def _compose_ipv4_network(ipv4_network, ipv4_prefix_len) -> netaddr.IPNetwork:
    return netaddr.IPNetwork('{:s}/{:d}'.format(str(ipv4_network), int(ipv4_prefix_len)))

class StaticRouteGenerator:
    def __init__(self, config_rule_composer : ConfigRuleComposer) -> None:
        self._config_rule_composer = config_rule_composer

    def compose(self, connection_hop_list : List[Tuple[str, str, Optional[str]]]) -> None:
        link_endpoints = self._compute_link_endpoints(connection_hop_list)
        LOGGER.debug('link_endpoints = {:s}'.format(str(link_endpoints)))

        self._compute_link_addresses(link_endpoints)
        LOGGER.debug('config_rule_composer = {:s}'.format(json.dumps(self._config_rule_composer.dump())))

        self._discover_connected_networks(connection_hop_list)
        LOGGER.debug('config_rule_composer = {:s}'.format(json.dumps(self._config_rule_composer.dump())))

        # Compute and propagate static routes forward (service_endpoint_a => service_endpoint_b)
        self._compute_static_routes(link_endpoints)

        # Compute and propagate static routes backward (service_endpoint_b => service_endpoint_a)
        reversed_endpoints = list(reversed(connection_hop_list))
        reversed_link_endpoints = self._compute_link_endpoints(reversed_endpoints)
        LOGGER.debug('reversed_link_endpoints = {:s}'.format(str(reversed_link_endpoints)))
        self._compute_static_routes(reversed_link_endpoints)

        LOGGER.debug('config_rule_composer = {:s}'.format(json.dumps(self._config_rule_composer.dump())))

    def _compute_link_endpoints(
        self, connection_hop_list : List[Tuple[str, str, Optional[str]]]
    ) -> List[Tuple[Tuple[str, str, Optional[str]], Tuple[str, str, Optional[str]]]]:
        # In some cases connection_hop_list might contain repeated endpoints, remove them here.
        added_connection_hops = set()
        filtered_connection_hop_list = list()
        for connection_hop in connection_hop_list:
            if connection_hop in added_connection_hops: continue
            filtered_connection_hop_list.append(connection_hop)
            added_connection_hops.add(connection_hop)
        connection_hop_list = filtered_connection_hop_list

        # In some cases connection_hop_list first and last items might be internal endpoints of
        # devices instead of link endpoints. Filter those endpoints not reaching a new device.
        if len(connection_hop_list) > 2 and connection_hop_list[0][0] == connection_hop_list[1][0]:
            # same device on first 2 endpoints
            connection_hop_list = connection_hop_list[1:]
        if len(connection_hop_list) > 2 and connection_hop_list[-1][0] == connection_hop_list[-2][0]:
            # same device on last 2 endpoints
            connection_hop_list = connection_hop_list[:-1]

        num_connection_hops = len(connection_hop_list)
        if num_connection_hops % 2 != 0: raise Exception('Number of connection hops must be even')
        if num_connection_hops < 4: raise Exception('Number of connection hops must be >= 4')

        it_connection_hops = iter(connection_hop_list)
        return list(zip(it_connection_hops, it_connection_hops))

    def _compute_link_addresses(
        self, link_endpoints_list : List[Tuple[Tuple[str, str, Optional[str]], Tuple[str, str, Optional[str]]]]
    ) -> None:
        for link_endpoints in link_endpoints_list:
            device_endpoint_a, device_endpoint_b = link_endpoints

            device_uuid_a, endpoint_uuid_a = device_endpoint_a[0:2]
            endpoint_a = self._config_rule_composer.get_device(device_uuid_a).get_endpoint(endpoint_uuid_a)

            device_uuid_b, endpoint_uuid_b = device_endpoint_b[0:2]
            endpoint_b = self._config_rule_composer.get_device(device_uuid_b).get_endpoint(endpoint_uuid_b)

            if endpoint_a.ipv4_address is None and endpoint_b.ipv4_address is None:
                ip_endpoint_a, ip_endpoint_b, prefix_len = _generate_neighbor_addresses()
                endpoint_a.ipv4_address    = str(ip_endpoint_a)
                endpoint_a.ipv4_prefix_len = prefix_len
                endpoint_b.ipv4_address    = str(ip_endpoint_b)
                endpoint_b.ipv4_prefix_len = prefix_len
            elif endpoint_a.ipv4_address is not None and endpoint_b.ipv4_address is None:
                prefix_len = endpoint_a.ipv4_prefix_len
                ip_network_a = _compose_ipv4_network(endpoint_a.ipv4_address, prefix_len)
                if prefix_len > 30:
                    MSG = 'Unsupported prefix_len for {:s}: {:s}'
                    raise Exception(MSG.format(str(endpoint_a), str(prefix_len)))
                ip_endpoint_b = _compute_gateway(ip_network_a, gateway_host=1)
                if ip_endpoint_b == ip_network_a.ip:
                    ip_endpoint_b = _compute_gateway(ip_network_a, gateway_host=2)
                endpoint_b.ipv4_address    = str(ip_endpoint_b)
                endpoint_b.ipv4_prefix_len = prefix_len
            elif endpoint_a.ipv4_address is None and endpoint_b.ipv4_address is not None:
                prefix_len = endpoint_b.ipv4_prefix_len
                ip_network_b = _compose_ipv4_network(endpoint_b.ipv4_address, prefix_len)
                if prefix_len > 30:
                    MSG = 'Unsupported prefix_len for {:s}: {:s}'
                    raise Exception(MSG.format(str(endpoint_b), str(prefix_len)))
                ip_endpoint_a = _compute_gateway(ip_network_b, gateway_host=1)
                if ip_endpoint_a == ip_network_b.ip:
                    ip_endpoint_a = _compute_gateway(ip_network_b, gateway_host=2)
                endpoint_a.ipv4_address    = str(ip_endpoint_a)
                endpoint_a.ipv4_prefix_len = prefix_len
            elif endpoint_a.ipv4_address is not None and endpoint_b.ipv4_address is not None:
                ip_network_a = _compose_ipv4_network(endpoint_a.ipv4_address, endpoint_a.ipv4_prefix_len)
                ip_network_b = _compose_ipv4_network(endpoint_b.ipv4_address, endpoint_b.ipv4_prefix_len)
                if ip_network_a.cidr != ip_network_b.cidr:
                    MSG = 'Incompatible CIDRs: endpoint_a({:s})=>{:s} endpoint_b({:s})=>{:s}'
                    raise Exception(MSG.format(str(endpoint_a), str(ip_network_a), str(endpoint_b), str(ip_network_b)))
                if ip_network_a.ip == ip_network_b.ip:
                    MSG = 'Duplicated IP: endpoint_a({:s})=>{:s} endpoint_b({:s})=>{:s}'
                    raise Exception(MSG.format(str(endpoint_a), str(ip_network_a), str(endpoint_b), str(ip_network_b)))

    def _discover_connected_networks(self, connection_hop_list : List[Tuple[str, str, Optional[str]]]) -> None:
        for connection_hop in connection_hop_list:
            device_uuid, endpoint_uuid = connection_hop[0:2]
            device = self._config_rule_composer.get_device(device_uuid)
            endpoint = device.get_endpoint(endpoint_uuid)

            if endpoint.ipv4_address is None: continue
            ip_network = _compose_ipv4_network(endpoint.ipv4_address, endpoint.ipv4_prefix_len)

            if '0.0.0.0/' in str(ip_network.cidr): continue
            device.connected.add(str(ip_network.cidr))

    def _compute_static_routes(
        self, link_endpoints_list : List[Tuple[Tuple[str, str, Optional[str]], Tuple[str, str, Optional[str]]]]
    ) -> None:
        for link_endpoints in link_endpoints_list:
            device_endpoint_a, device_endpoint_b = link_endpoints

            device_uuid_a, endpoint_uuid_a = device_endpoint_a[0:2]
            device_a   = self._config_rule_composer.get_device(device_uuid_a)
            endpoint_a = device_a.get_endpoint(endpoint_uuid_a)

            device_uuid_b, endpoint_uuid_b = device_endpoint_b[0:2]
            device_b   = self._config_rule_composer.get_device(device_uuid_b)
            endpoint_b = device_b.get_endpoint(endpoint_uuid_b)

            # Compute static routes from networks connected in device_a
            for ip_network_a in device_a.connected:
                if ip_network_a in device_b.connected: continue
                if ip_network_a in device_b.static_routes: continue
                if ip_network_a in ROOT_NEIGHBOR_ROUTING_NETWORK: continue
                endpoint_a_ip_network = _compose_ipv4_network(endpoint_a.ipv4_address, endpoint_a.ipv4_prefix_len)
                next_hop = str(endpoint_a_ip_network.ip)
                metric = 1
                device_b.static_routes.setdefault(ip_network_a, dict())[metric] = next_hop

            # Compute static routes from networks connected in device_b
            for ip_network_b in device_b.connected:
                if ip_network_b in device_a.connected: continue
                if ip_network_b in device_a.static_routes: continue
                if ip_network_b in ROOT_NEIGHBOR_ROUTING_NETWORK: continue
                endpoint_b_ip_network = _compose_ipv4_network(endpoint_b.ipv4_address, endpoint_b.ipv4_prefix_len)
                next_hop = str(endpoint_b_ip_network.ip)
                metric = 1
                device_a.static_routes.setdefault(ip_network_b, dict())[metric] = next_hop

            # Propagate static routes from networks connected in device_a
            for ip_network_a, metric_next_hop in device_a.static_routes.items():
                if ip_network_a in device_b.connected: continue
                if ip_network_a in ROOT_NEIGHBOR_ROUTING_NETWORK: continue
                endpoint_a_ip_network = _compose_ipv4_network(endpoint_a.ipv4_address, endpoint_a.ipv4_prefix_len)
                if ip_network_a in device_b.static_routes:
                    current_metric = min(device_b.static_routes[ip_network_a].keys())
                else:
                    current_metric = int(sys.float_info.max)
                for metric, next_hop in metric_next_hop.items():
                    new_metric = metric + 1
                    if new_metric >= current_metric: continue
                    next_hop_a = str(endpoint_a_ip_network.ip)
                    device_b.static_routes.setdefault(ip_network_a, dict())[metric] = next_hop_a

            # Propagate static routes from networks connected in device_b
            for ip_network_b in device_b.static_routes.keys():
                if ip_network_b in device_a.connected: continue
                if ip_network_b in ROOT_NEIGHBOR_ROUTING_NETWORK: continue
                endpoint_b_ip_network = _compose_ipv4_network(endpoint_b.ipv4_address, endpoint_b.ipv4_prefix_len)
                if ip_network_b in device_a.static_routes:
                    current_metric = min(device_a.static_routes[ip_network_b].keys())
                else:
                    current_metric = int(sys.float_info.max)
                for metric, next_hop in metric_next_hop.items():
                    new_metric = metric + 1
                    if new_metric >= current_metric: continue
                    next_hop_b = str(endpoint_b_ip_network.ip)
                    device_a.static_routes.setdefault(ip_network_b, dict())[metric] = next_hop_b
