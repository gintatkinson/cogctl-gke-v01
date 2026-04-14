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

from typing import Dict, List, Tuple

from common.proto.context_pb2 import Link
from common.tools.object_factory.ConfigRule import (
    json_config_rule_delete,
    json_config_rule_set,
)
from context.client.ContextClient import ContextClient


def build_match_criterion(
    vlan: str,
    src_ip: str,
    src_port: str,
    dst_ip: str,
    dst_port: str,
    target_conn_group_id: str = "line1",
    index: int = 1,
) -> Dict:
    """
    Build the match-criterion structure used in the 'service-match-criteria'.
    """
    return {
        "index": index,
        "match-type": [
            {"type": "ietf-network-slice-service:vlan", "value": [vlan]},
            {
                "type": "ietf-network-slice-service:source-ip-prefix",
                "value": [src_ip],
            },
            {
                "type": "ietf-network-slice-service:source-tcp-port",
                "value": [src_port],
            },
            {
                "type": "ietf-network-slice-service:destination-ip-prefix",
                "value": [dst_ip],
            },
            {
                "type": "ietf-network-slice-service:destination-tcp-port",
                "value": [dst_port],
            },
        ],
        "target-connection-group-id": target_conn_group_id,
    }


def build_sdp(
    sdp_id: str,
    node_id: str,
    mgmt_ip: str,
    ac_node_id: str,
    ac_ep_id: str,
    match_criterion: Dict,
    attachment_id: str = "0",
    attachment_description: str = "dsc",
) -> Dict:
    """
    Build the sdp structure used in the 'slice_service' dictionary.
    """
    return {
        "id": sdp_id,
        "node-id": node_id,
        "sdp-ip-address": [mgmt_ip],
        "service-match-criteria": {"match-criterion": [match_criterion]},
        "attachment-circuits": {
            "attachment-circuit": [
                {
                    "id": attachment_id,
                    "description": attachment_description,
                    "ac-node-id": ac_node_id,
                    "ac-tp-id": ac_ep_id,
                }
            ]
        },
    }


def build_slo_policy_bound(
    one_way_delay: int, one_way_bandwidth: int, one_way_packet_loss: float
) -> List[Dict]:
    """
    Build the 'metric-bound' portion of the 'slo-policy' dictionary.
    """
    return [
        {
            "metric-type": "ietf-network-slice-service:one-way-delay-maximum",
            "metric-unit": "milliseconds",
            "bound": one_way_delay,
        },
        {
            "metric-type": "ietf-network-slice-service:one-way-bandwidth",
            "metric-unit": "Mbps",
            "bound": one_way_bandwidth,
        },
        {
            "metric-type": "ietf-network-slice-service:two-way-packet-loss",
            "metric-unit": "percentage",
            "percentile-value": one_way_packet_loss,
        },
    ]


def _get_device_endpoint_name(device_obj, endpoint_uuid: str) -> str:
    """
    Given a device object and an endpoint UUID, return the device endpoint name.
    Raises an exception if not found.
    """
    for d_ep in device_obj.device_endpoints:
        if d_ep.endpoint_id.endpoint_uuid.uuid == endpoint_uuid:
            return d_ep.name
    raise Exception("Endpoint not found")


def setup_config_rules(service_uuid: str, json_settings: Dict) -> List[Dict]:
    operation_type: str = json_settings["operation_type"]

    # Source parameters
    src_node_id: str = json_settings["src_node_id"]
    src_mgmt_ip_address: str = json_settings["src_mgmt_ip_address"]
    src_ac_node_id: str = json_settings["src_ac_node_id"]
    src_ac_ep_id: str = json_settings["src_ac_ep_id"]
    src_vlan: str = json_settings["src_vlan"]
    src_source_ip_prefix: str = json_settings["src_source_ip_prefix"]
    src_source_tcp_port: str = json_settings["src_source_tcp_port"]
    src_destination_ip_prefix: str = json_settings["src_destination_ip_prefix"]
    src_destination_tcp_port: str = json_settings["src_destination_tcp_port"]
    source_one_way_delay: int = int(json_settings["source_one_way_delay"])
    source_one_way_bandwidth: int = int(json_settings["source_one_way_bandwidth"])
    source_one_way_packet_loss: float = float(
        json_settings["source_one_way_packet_loss"]
    )

    # Destination parameters
    dst_node_id: str = json_settings["dst_node_id"]
    dst_mgmt_ip_address: str = json_settings["dst_mgmt_ip_address"]
    dst_ac_node_id: str = json_settings["dst_ac_node_id"]
    dst_ac_ep_id: str = json_settings["dst_ac_ep_id"]
    dst_vlan: str = json_settings["dst_vlan"]
    dst_source_ip_prefix: str = json_settings["dst_source_ip_prefix"]
    dst_source_tcp_port: str = json_settings["dst_source_tcp_port"]
    dst_destination_ip_prefix: str = json_settings["dst_destination_ip_prefix"]
    dst_destination_tcp_port: str = json_settings["dst_destination_tcp_port"]
    destination_one_way_delay: int = int(json_settings["destination_one_way_delay"])
    destination_one_way_bandwidth: int = int(
        json_settings["destination_one_way_bandwidth"]
    )
    destination_one_way_packet_loss: float = float(
        json_settings["destination_one_way_packet_loss"]
    )

    # Slice ID
    slice_id: str = json_settings["slice_id"]

    # build source & destination match criteria
    src_match_criterion = build_match_criterion(
        vlan=src_vlan,
        src_ip=src_source_ip_prefix,
        src_port=src_source_tcp_port,
        dst_ip=src_destination_ip_prefix,
        dst_port=src_destination_tcp_port,
    )
    dst_match_criterion = build_match_criterion(
        vlan=dst_vlan,
        src_ip=dst_source_ip_prefix,
        src_port=dst_source_tcp_port,
        dst_ip=dst_destination_ip_prefix,
        dst_port=dst_destination_tcp_port,
    )

    # Build SDPs
    sdp_src = build_sdp(
        sdp_id="1",
        node_id=src_node_id,
        mgmt_ip=src_mgmt_ip_address,
        ac_node_id=src_ac_node_id,
        ac_ep_id=src_ac_ep_id,
        match_criterion=src_match_criterion,
    )
    sdp_dst = build_sdp(
        sdp_id="2",
        node_id=dst_node_id,
        mgmt_ip=dst_mgmt_ip_address,
        ac_node_id=dst_ac_node_id,
        ac_ep_id=dst_ac_ep_id,
        match_criterion=dst_match_criterion,
    )

    sdps = [sdp_src, sdp_dst]

    # Build connection-groups
    connection_groups = [
        {
            "id": "line1",
            "connectivity-type": "point-to-point",
            "connectivity-construct": [
                {
                    "id": 1,
                    "p2p-sender-sdp": "1",
                    "p2p-receiver-sdp": "2",
                    "service-slo-sle-policy": {
                        "slo-policy": {
                            "metric-bound": build_slo_policy_bound(
                                one_way_delay=source_one_way_delay,
                                one_way_bandwidth=source_one_way_bandwidth,
                                one_way_packet_loss=source_one_way_packet_loss,
                            )
                        }
                    },
                },
                {
                    "id": 2,
                    "p2p-sender-sdp": "2",
                    "p2p-receiver-sdp": "1",
                    "service-slo-sle-policy": {
                        "slo-policy": {
                            "metric-bound": build_slo_policy_bound(
                                one_way_delay=destination_one_way_delay,
                                one_way_bandwidth=destination_one_way_bandwidth,
                                one_way_packet_loss=destination_one_way_packet_loss,
                            )
                        }
                    },
                },
            ],
        }
    ]

    slice_service = {
        "id": slice_id,
        "description": "dsc",
        "sdps": {"sdp": sdps},
        "connection-groups": {"connection-group": connection_groups},
    }
    slice_data_model = {"network-slice-services": {"slice-service": [slice_service]}}

    json_config_rules = [
        json_config_rule_set(
            "/service[{:s}]/IETFSlice".format(service_uuid),
            slice_data_model,
        ),
        json_config_rule_set(
            "/service[{:s}]/IETFSlice/operation".format(service_uuid),
            {"type": operation_type},
        ),
    ]
    return json_config_rules


def teardown_config_rules(service_uuid: str, json_settings: Dict) -> List[Dict]:
    json_config_rules = [
        json_config_rule_delete(
            "/service[{:s}]/IETFSlice".format(service_uuid),
            {},
        ),
        json_config_rule_delete(
            "/service[{:s}]/IETFSlice/operation".format(service_uuid),
            {},
        ),
    ]
    return json_config_rules


def get_link_ep_device_names(
    link: Link, context_client: ContextClient
) -> Tuple[str, str, str, str]:
    ep_ids = link.link_endpoint_ids
    ep_device_id_1 = ep_ids[0].device_id
    ep_uuid_1 = ep_ids[0].endpoint_uuid.uuid
    device_obj_1 = context_client.GetDevice(ep_device_id_1)
    ep_name_1 = _get_device_endpoint_name(device_obj_1, ep_uuid_1)
    device_obj_name_1 = device_obj_1.name

    ep_device_id_2 = ep_ids[1].device_id
    ep_uuid_2 = ep_ids[1].endpoint_uuid.uuid
    device_obj_2 = context_client.GetDevice(ep_device_id_2)
    ep_name_2 = _get_device_endpoint_name(device_obj_2, ep_uuid_2)
    device_obj_name_2 = device_obj_2.name

    return (
        device_obj_name_1,
        ep_name_1,
        device_obj_1,
        device_obj_name_2,
        ep_name_2,
        device_obj_2,
    )
