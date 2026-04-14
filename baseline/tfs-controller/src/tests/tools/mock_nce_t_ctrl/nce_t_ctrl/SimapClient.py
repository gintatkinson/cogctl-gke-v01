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


from typing import Dict, List, Optional, Tuple
from common.tools.rest_conf.client.RestConfClient import RestConfClient


class TerminationPoint:
    ENDPOINT_NO_ID = '/ietf-network:networks/network={:s}/node={:s}'
    ENDPOINT_ID    = ENDPOINT_NO_ID + '/ietf-network-topology:termination-point={:s}'

    def __init__(self, restconf_client : RestConfClient, network_id : str, node_id : str, tp_id : str):
        self._restconf_client = restconf_client
        self._network_id = network_id
        self._node_id = node_id
        self._tp_id = tp_id

    def create(self, supporting_termination_point_ids : List[Tuple[str, str, str]] = []) -> None:
        endpoint = TerminationPoint.ENDPOINT_ID.format(self._network_id, self._node_id, self._tp_id)
        tp = {'tp-id': self._tp_id}
        stps = [
            {'network-ref': snet_id, 'node-ref': snode_id, 'tp-ref': stp_id}
            for snet_id,snode_id,stp_id in supporting_termination_point_ids
        ]
        if len(stps) > 0: tp['supporting-termination-point'] = stps
        node = {'node-id': self._node_id, 'ietf-network-topology:termination-point': [tp]}
        network = {'network-id': self._network_id, 'node': [node]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.post(endpoint, payload)

    def get(self) -> Dict:
        endpoint = TerminationPoint.ENDPOINT_ID.format(self._network_id, self._node_id, self._tp_id)
        node : Dict = self._restconf_client.get(endpoint)
        return node['ietf-network-topology:termination-point'][0]

    def update(self, supporting_termination_point_ids : List[Tuple[str, str, str]] = []) -> None:
        endpoint = TerminationPoint.ENDPOINT_ID.format(self._network_id, self._node_id, self._tp_id)
        tp = {'tp-id': self._tp_id}
        stps = [
            {'network-ref': snet_id, 'node-ref': snode_id, 'tp-ref': stp_id}
            for snet_id,snode_id,stp_id in supporting_termination_point_ids
        ]
        if len(stps) > 0: tp['supporting-termination-point'] = stps
        node = {'node-id': self._node_id, 'ietf-network-topology:termination-point': [tp]}
        network = {'network-id': self._network_id, 'node': [node]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.patch(endpoint, payload)

    def delete(self) -> None:
        endpoint = TerminationPoint.ENDPOINT_ID.format(self._network_id, self._node_id, self._tp_id)
        self._restconf_client.delete(endpoint)


class NodeTelemetry:
    ENDPOINT = '/ietf-network:networks/network={:s}/node={:s}/simap-telemetry:simap-telemetry'

    def __init__(self, restconf_client : RestConfClient, network_id : str, node_id : str):
        self._restconf_client = restconf_client
        self._network_id = network_id
        self._node_id = node_id

    def create(
        self, cpu_utilization : float, related_service_ids : List[str] = []
    ) -> None:
        endpoint = NodeTelemetry.ENDPOINT.format(self._network_id, self._node_id)
        telemetry = {
            'cpu-utilization': '{:.2f}'.format(cpu_utilization),
        }
        if len(related_service_ids) > 0: telemetry['related-service-ids'] = related_service_ids
        node = {'node-id': self._node_id, 'simap-telemetry:simap-telemetry': telemetry}
        network = {'network-id': self._network_id, 'node': [node]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.post(endpoint, payload)

    def get(self) -> Dict:
        endpoint = NodeTelemetry.ENDPOINT.format(self._network_id, self._node_id)
        telemetry : Dict = self._restconf_client.get(endpoint)
        return telemetry

    def update(
        self, cpu_utilization : float, related_service_ids : List[str] = []
    ) -> None:
        endpoint = NodeTelemetry.ENDPOINT.format(self._network_id, self._node_id)
        telemetry = {
            'cpu-utilization': '{:.2f}'.format(cpu_utilization),
        }
        if len(related_service_ids) > 0: telemetry['related-service-ids'] = related_service_ids
        node = {'node-id': self._node_id, 'simap-telemetry:simap-telemetry': telemetry}
        network = {'network-id': self._network_id, 'node': [node]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.patch(endpoint, payload)

    def delete(self) -> None:
        endpoint = NodeTelemetry.ENDPOINT.format(self._network_id, self._node_id)
        self._restconf_client.delete(endpoint)


class Node:
    ENDPOINT_NO_ID = '/ietf-network:networks/network={:s}'
    ENDPOINT_ID    = ENDPOINT_NO_ID + '/node={:s}'

    def __init__(self, restconf_client : RestConfClient, network_id : str, node_id : str):
        self._restconf_client = restconf_client
        self._network_id = network_id
        self._node_id = node_id
        self._tps : Dict[str, TerminationPoint] = dict()
        self._telemetry : Optional[NodeTelemetry] = None

    @property
    def telemetry(self) -> NodeTelemetry:
        if self._telemetry is None:
            self._telemetry = NodeTelemetry(self._restconf_client, self._network_id, self._node_id)
        return self._telemetry

    def termination_points(self) -> List[Dict]:
        tps : Dict = self._restconf_client.get(TerminationPoint.ENDPOINT_NO_ID)
        return tps['ietf-network-topology:termination-point'].get('termination-point', list())

    def termination_point(self, tp_id : str) -> TerminationPoint:
        _tp = self._tps.get(tp_id)
        if _tp is not None: return _tp
        _tp = TerminationPoint(self._restconf_client, self._network_id, self._node_id, tp_id)
        return self._tps.setdefault(tp_id, _tp)

    def create(
        self, termination_point_ids : List[str] = [],
        supporting_node_ids : List[Tuple[str, str]] = []
    ) -> None:
        endpoint = Node.ENDPOINT_ID.format(self._network_id, self._node_id)
        node = {'node-id': self._node_id}
        tps = [{'tp-id': tp_id} for tp_id in termination_point_ids]
        if len(tps) > 0: node['ietf-network-topology:termination-point'] = tps
        sns = [{'network-ref': snet_id, 'node-ref': snode_id} for snet_id,snode_id in supporting_node_ids]
        if len(sns) > 0: node['supporting-node'] = sns
        network = {'network-id': self._network_id, 'node': [node]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.post(endpoint, payload)

    def get(self) -> Dict:
        endpoint = Node.ENDPOINT_ID.format(self._network_id, self._node_id)
        node : Dict = self._restconf_client.get(endpoint)
        return node['ietf-network:node'][0]

    def update(
        self, termination_point_ids : List[str] = [],
        supporting_node_ids : List[Tuple[str, str]] = []
    ) -> None:
        endpoint = Node.ENDPOINT_ID.format(self._network_id, self._node_id)
        node = {'node-id': self._node_id}
        tps = [{'tp-id': tp_id} for tp_id in termination_point_ids]
        if len(tps) > 0: node['ietf-network-topology:termination-point'] = tps
        sns = [{'network-ref': snet_id, 'node-ref': snode_id} for snet_id,snode_id in supporting_node_ids]
        if len(sns) > 0: node['supporting-node'] = sns
        network = {'network-id': self._network_id, 'node': [node]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.patch(endpoint, payload)

    def delete(self) -> None:
        endpoint = Node.ENDPOINT_ID.format(self._network_id, self._node_id)
        self._restconf_client.delete(endpoint)


class LinkTelemetry:
    ENDPOINT = '/ietf-network:networks/network={:s}/ietf-network-topology:link={:s}/simap-telemetry:simap-telemetry'

    def __init__(self, restconf_client : RestConfClient, network_id : str, link_id : str):
        self._restconf_client = restconf_client
        self._network_id = network_id
        self._link_id = link_id

    def create(
        self, bandwidth_utilization : float, latency : float,
        related_service_ids : List[str] = []
    ) -> None:
        endpoint = LinkTelemetry.ENDPOINT.format(self._network_id, self._link_id)
        telemetry = {
            'bandwidth-utilization': '{:.2f}'.format(bandwidth_utilization),
            'latency'              : '{:.3f}'.format(latency),
        }
        if len(related_service_ids) > 0: telemetry['related-service-ids'] = related_service_ids
        link = {'link-id': self._link_id, 'simap-telemetry:simap-telemetry': telemetry}
        network = {'network-id': self._network_id, 'ietf-network-topology:link': [link]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.post(endpoint, payload)

    def get(self) -> Dict:
        endpoint = LinkTelemetry.ENDPOINT.format(self._network_id, self._link_id)
        telemetry : Dict = self._restconf_client.get(endpoint)
        return telemetry

    def update(
        self, bandwidth_utilization : float, latency : float,
        related_service_ids : List[str] = []
    ) -> None:
        endpoint = LinkTelemetry.ENDPOINT.format(self._network_id, self._link_id)
        telemetry = {
            'bandwidth-utilization': '{:.2f}'.format(bandwidth_utilization),
            'latency'              : '{:.3f}'.format(latency),
        }
        if len(related_service_ids) > 0: telemetry['related-service-ids'] = related_service_ids
        link = {'link-id': self._link_id, 'simap-telemetry:simap-telemetry': telemetry}
        network = {'network-id': self._network_id, 'ietf-network-topology:link': [link]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.patch(endpoint, payload)

    def delete(self) -> None:
        endpoint = LinkTelemetry.ENDPOINT.format(self._network_id, self._link_id)
        self._restconf_client.delete(endpoint)


class Link:
    ENDPOINT_NO_ID = '/ietf-network:networks/network={:s}'
    ENDPOINT_ID    = ENDPOINT_NO_ID + '/ietf-network-topology:link={:s}'

    def __init__(self, restconf_client : RestConfClient, network_id : str, link_id : str):
        self._restconf_client = restconf_client
        self._network_id = network_id
        self._link_id = link_id
        self._telemetry : Optional[LinkTelemetry] = None

    @property
    def telemetry(self) -> LinkTelemetry:
        if self._telemetry is None:
            self._telemetry = LinkTelemetry(self._restconf_client, self._network_id, self._link_id)
        return self._telemetry

    def create(
        self, src_node_id : str, src_tp_id : str, dst_node_id : str, dst_tp_id : str,
        supporting_link_ids : List[Tuple[str, str]] = []
    ) -> None:
        endpoint = Link.ENDPOINT_ID.format(self._network_id, self._link_id)
        link = {
            'link-id'    : self._link_id,
            'source'     : {'source-node': src_node_id, 'source-tp': src_tp_id},
            'destination': {'dest-node'  : dst_node_id, 'dest-tp'  : dst_tp_id},
        }
        sls = [{'network-ref': snet_id, 'link-ref': slink_id} for snet_id,slink_id in supporting_link_ids]
        if len(sls) > 0: link['supporting-link'] = sls
        network = {'network-id': self._network_id, 'ietf-network-topology:link': [link]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.post(endpoint, payload)

    def get(self) -> Dict:
        endpoint = Link.ENDPOINT_ID.format(self._network_id, self._link_id)
        link : Dict = self._restconf_client.get(endpoint)
        return link['ietf-network-topology:link'][0]

    def update(
        self, src_node_id : str, src_tp_id : str, dst_node_id : str, dst_tp_id : str,
        supporting_link_ids : List[Tuple[str, str]] = []
    ) -> None:
        endpoint = Link.ENDPOINT_ID.format(self._network_id, self._link_id)
        link = {
            'link-id'    : self._link_id,
            'source'     : {'source-node': src_node_id, 'source-tp': src_tp_id},
            'destination': {'dest-node'  : dst_node_id, 'dest-tp'  : dst_tp_id},
        }
        sls = [{'network-ref': snet_id, 'link-ref': slink_id} for snet_id,slink_id in supporting_link_ids]
        if len(sls) > 0: link['supporting-link'] = sls
        network = {'network-id': self._network_id, 'ietf-network-topology:link': [link]}
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.patch(endpoint, payload)

    def delete(self) -> None:
        endpoint = Link.ENDPOINT_ID.format(self._network_id, self._link_id)
        self._restconf_client.delete(endpoint)


class Network:
    ENDPOINT_NO_ID = '/ietf-network:networks'
    ENDPOINT_ID    = ENDPOINT_NO_ID + '/network={:s}'

    def __init__(self, restconf_client : RestConfClient, network_id : str):
        self._restconf_client = restconf_client
        self._network_id = network_id
        self._nodes : Dict[str, Node] = dict()
        self._links : Dict[str, Link] = dict()

    def nodes(self) -> List[Dict]:
        reply : Dict = self._restconf_client.get(Node.ENDPOINT_NO_ID.format(self._network_id))
        return reply['ietf-network:network'][0].get('node', list())

    def links(self) -> List[Dict]:
        reply : Dict = self._restconf_client.get(Link.ENDPOINT_NO_ID.format(self._network_id))
        return reply['ietf-network:network'][0].get('ietf-network-topology:link', list())

    def node(self, node_id : str) -> Node:
        _node = self._nodes.get(node_id)
        if _node is not None: return _node
        _node = Node(self._restconf_client, self._network_id, node_id)
        return self._nodes.setdefault(node_id, _node)

    def link(self, link_id : str) -> Link:
        _link = self._links.get(link_id)
        if _link is not None: return _link
        _link = Link(self._restconf_client, self._network_id, link_id)
        return self._links.setdefault(link_id, _link)

    def create(self, supporting_network_ids : List[str] = []) -> None:
        endpoint = Network.ENDPOINT_ID.format(self._network_id)
        network = {'network-id': self._network_id}
        sns = [{'network-ref': sn_id} for sn_id in supporting_network_ids]
        if len(sns) > 0: network['supporting-network'] = sns
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.post(endpoint, payload)

    def get(self) -> Dict:
        endpoint = Network.ENDPOINT_ID.format(self._network_id)
        networks : Dict = self._restconf_client.get(endpoint)
        return networks['ietf-network:network'][0]

    def update(self, supporting_network_ids : List[str] = []) -> None:
        endpoint = Network.ENDPOINT_ID.format(self._network_id)
        network = {'network-id': self._network_id}
        sns = [{'network-ref': sn_id} for sn_id in supporting_network_ids]
        if len(sns) > 0: network['supporting-network'] = sns
        payload  = {'ietf-network:networks': {'network': [network]}}
        self._restconf_client.patch(endpoint, payload)

    def delete(self) -> None:
        endpoint = Network.ENDPOINT_ID.format(self._network_id)
        self._restconf_client.delete(endpoint)


class SimapClient:
    def __init__(self, restconf_client : RestConfClient) -> None:
        self._restconf_client = restconf_client
        self._networks : Dict[str, Network] = dict()

    def networks(self) -> List[Dict]:
        reply : Dict = self._restconf_client.get(Network.ENDPOINT_NO_ID)
        return reply['ietf-network:networks'].get('network', list())

    def network(self, network_id : str) -> Network:
        _network = self._networks.get(network_id)
        if _network is not None: return _network
        _network = Network(self._restconf_client, network_id)
        return self._networks.setdefault(network_id, _network)
