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

import logging, networkx
from dataclasses import dataclass, field
from typing import Dict, List, Set
from common.proto.context_pb2 import ServiceTypeEnum
from common.tools.context_queries.Topology import get_topology_details
from common.tools.object_factory.Constraint import json_constraint_custom
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Service import json_service
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.DeviceTypes import DeviceTypeEnum
from context.client.ContextClient import ContextClient


LOGGER = logging.getLogger(__name__)


@dataclass
class GraphAndMapping:
    graph                   : networkx.Graph            = field(default_factory=networkx.Graph)
    device_to_type          : Dict[str, str]            = field(default_factory=dict)
    device_name_to_uuid     : Dict[str, str]            = field(default_factory=dict)
    endpoint_name_to_uuid   : Dict[Dict[str, str], str] = field(default_factory=dict)
    endpoint_to_device_uuid : Dict[str, str]            = field(default_factory=dict)


EXCLUDED_DEVICE_TYPES : Set[str] = {
    DeviceTypeEnum.EMULATED_IP_SDN_CONTROLLER.value,
    DeviceTypeEnum.EMULATED_MICROWAVE_RADIO_SYSTEM.value,
    DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM.value,
    DeviceTypeEnum.EMULATED_XR_CONSTELLATION.value,
    DeviceTypeEnum.IETF_SLICE.value,
    DeviceTypeEnum.IP_SDN_CONTROLLER.value,
    DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM.value,
    DeviceTypeEnum.NCE.value,
    DeviceTypeEnum.OPEN_LINE_SYSTEM.value,
    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER.value,
    DeviceTypeEnum.XR_CONSTELLATION.value,
}


def compose_graph_from_topology() -> GraphAndMapping:
    context_client = ContextClient()
    topology_details = get_topology_details(
        context_client, DEFAULT_TOPOLOGY_NAME,
        context_uuid=DEFAULT_CONTEXT_NAME, rw_copy=False
    )

    graph_and_mapping = GraphAndMapping()

    excluded_device_uuids : Set[str] = set()

    for device in topology_details.devices:
        device_uuid = device.device_id.device_uuid.uuid
        graph_and_mapping.device_name_to_uuid.setdefault(device.name, device_uuid)
        graph_and_mapping.device_name_to_uuid.setdefault(device_uuid, device_uuid)
        graph_and_mapping.device_to_type.setdefault(device_uuid, device.device_type)

        if device.device_type in EXCLUDED_DEVICE_TYPES:
            excluded_device_uuids.add(device_uuid)
            continue

        endpoint_uuids = list()
        for endpoint in device.device_endpoints:
            endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
            endpoint_uuids.append(endpoint_uuid)
            graph_and_mapping.graph.add_node(endpoint_uuid)

            graph_and_mapping.endpoint_name_to_uuid.setdefault((device_uuid, endpoint.name), endpoint_uuid)
            graph_and_mapping.endpoint_name_to_uuid.setdefault((device_uuid, endpoint_uuid), endpoint_uuid)
            graph_and_mapping.endpoint_to_device_uuid.setdefault(endpoint_uuid, device_uuid)

        for endpoint_uuid_i in endpoint_uuids:
            for endpoint_uuid_j in endpoint_uuids:
                if endpoint_uuid_i == endpoint_uuid_j: continue
                graph_and_mapping.graph.add_edge(endpoint_uuid_i, endpoint_uuid_j)

    for link in topology_details.links:
        endpoint_id_a = link.link_endpoint_ids[ 0]
        endpoint_id_z = link.link_endpoint_ids[-1]

        device_uuid_a = endpoint_id_a.device_id.device_uuid.uuid
        if device_uuid_a in excluded_device_uuids: continue

        device_uuid_z = endpoint_id_z.device_id.device_uuid.uuid
        if device_uuid_z in excluded_device_uuids: continue

        graph_and_mapping.graph.add_edge(
            endpoint_id_a.endpoint_uuid.uuid,
            endpoint_id_z.endpoint_uuid.uuid,
        )

    return graph_and_mapping

def compose_optical_service(vlink_request : Dict) -> Dict:
    graph_and_mapping = compose_graph_from_topology()

    vlink_endpoint_id_a = vlink_request['link_endpoint_ids'][ 0]
    vlink_endpoint_id_b = vlink_request['link_endpoint_ids'][-1]

    device_uuid_or_name_a   = vlink_endpoint_id_a['device_id']['device_uuid']['uuid']
    device_uuid_or_name_b   = vlink_endpoint_id_b['device_id']['device_uuid']['uuid']
    endpoint_uuid_or_name_a = vlink_endpoint_id_a['endpoint_uuid']['uuid']
    endpoint_uuid_or_name_b = vlink_endpoint_id_b['endpoint_uuid']['uuid']

    device_uuid_a = graph_and_mapping.device_name_to_uuid[device_uuid_or_name_a]
    device_uuid_b = graph_and_mapping.device_name_to_uuid[device_uuid_or_name_b]

    endpoint_uuid_a = graph_and_mapping.endpoint_name_to_uuid[(device_uuid_a, endpoint_uuid_or_name_a)]
    endpoint_uuid_b = graph_and_mapping.endpoint_name_to_uuid[(device_uuid_b, endpoint_uuid_or_name_b)]

    path_hops = networkx.shortest_path(
        graph_and_mapping.graph, endpoint_uuid_a, endpoint_uuid_b
    )

    LOGGER.info('[compose_optical_service] path_hops={:s}'.format(str(path_hops)))

    OPTICAL_TRANSPONDER_TYPE = {
        DeviceTypeEnum.EMULATED_OPTICAL_TRANSPONDER.value,
        DeviceTypeEnum.OPTICAL_TRANSPONDER.value,
    }

    optical_border_endpoint_ids : List[str] = list()
    for endpoint_uuid in path_hops:
        LOGGER.info('[compose_optical_service] endpoint_uuid={:s}'.format(str(endpoint_uuid)))
        device_uuid = graph_and_mapping.endpoint_to_device_uuid[endpoint_uuid]
        LOGGER.info('[compose_optical_service]   device_uuid={:s}'.format(str(device_uuid)))
        device_type = graph_and_mapping.device_to_type[device_uuid]
        LOGGER.info('[compose_optical_service]   device_type={:s}'.format(str(device_type)))
        if device_type not in OPTICAL_TRANSPONDER_TYPE: continue
        device_id = json_device_id(device_uuid)
        endpoint_id = json_endpoint_id(device_id, endpoint_uuid)
        LOGGER.info('[compose_optical_service]   endpoint_id={:s}'.format(str(endpoint_id)))
        optical_border_endpoint_ids.append(endpoint_id)

    LOGGER.info('[compose_optical_service] optical_border_endpoint_ids={:s}'.format(str(optical_border_endpoint_ids)))

    constraints = [
        json_constraint_custom('bandwidth[gbps]',  str(vlink_request['attributes']['total_capacity_gbps'])),
        json_constraint_custom('bidirectionality', '1'),
    ]

    vlink_service_uuid = vlink_request['link_id']['link_uuid']['uuid']

    if vlink_service_uuid == 'IP1/PORT-xe1==IP2/PORT-xe1':
        constraints.append(json_constraint_custom('optical-band-width[GHz]', '300'))

    vlink_optical_service = json_service(
        vlink_service_uuid,
        ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY,
        context_id=json_context_id(DEFAULT_CONTEXT_NAME),
        endpoint_ids=[
            optical_border_endpoint_ids[0], optical_border_endpoint_ids[-1]
        ],
        constraints=constraints,
    )
    return vlink_optical_service
