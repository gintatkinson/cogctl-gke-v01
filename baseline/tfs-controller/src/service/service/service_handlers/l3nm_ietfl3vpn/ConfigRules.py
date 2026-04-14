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

from typing import Dict, List, Tuple, TypedDict

from common.proto.context_pb2 import Link
from common.tools.object_factory.ConfigRule import (
    json_config_rule_delete,
    json_config_rule_set,
)
from context.client.ContextClient import ContextClient


class LANPrefixesDict(TypedDict):
    lan: str
    lan_tag: str


SITE_NETWORK_ACCESS_TYPE = "ietf-l3vpn-svc:multipoint"


def create_site_dict(
    site_id: str,
    site_location: str,
    device_uuid: str,
    endpoint_uuid: str,
    service_uuid: str,
    role: str,
    management_type: str,
    ce_address: str,
    pe_address: str,
    ce_pe_network_prefix: int,
    mtu: int,
    input_bw: int,
    output_bw: int,
    qos_profile_id: str,
    qos_profile_direction: str,
    qos_profile_latency: int,
    qos_profile_bw_guarantee: int,
    lan_prefixes: List[LANPrefixesDict],
) -> Dict:
    """
    Helper function that creates a dictionary representing a single 'site'
    entry (including management, locations, devices, routing-protocols, and
    site-network-accesses).
    """
    site_lan_prefixes = [
        {
            "lan": lp["lan"],
            "lan-tag": lp["lan_tag"],
            "next-hop": ce_address,
        }
        for lp in lan_prefixes
    ]

    return {
        "site-id": site_id,
        "management": {"type": management_type},
        "locations": {"location": [{"location-id": site_location}]},
        "devices": {
            "device": [
                {
                    "device-id": device_uuid,
                    "location": site_location,
                }
            ]
        },
        "routing-protocols": {
            "routing-protocol": [
                {
                    "type": "ietf-l3vpn-svc:static",
                    "static": {
                        "cascaded-lan-prefixes": {
                            "ipv4-lan-prefixes": site_lan_prefixes
                        }
                    },
                }
            ]
        },
        "site-network-accesses": {
            "site-network-access": [
                {
                    "site-network-access-id": endpoint_uuid,
                    "site-network-access-type": SITE_NETWORK_ACCESS_TYPE,
                    "device-reference": device_uuid,
                    "vpn-attachment": {
                        "vpn-id": service_uuid,
                        "site-role": role,
                    },
                    "ip-connection": {
                        "ipv4": {
                            "address-allocation-type": "ietf-l3vpn-svc:static-address",
                            "addresses": {
                                "provider-address": pe_address,
                                "customer-address": ce_address,
                                "prefix-length": ce_pe_network_prefix,
                            },
                        }
                    },
                    "service": {
                        "svc-mtu": mtu,
                        "svc-input-bandwidth": input_bw,
                        "svc-output-bandwidth": output_bw,
                        "qos": {
                            "qos-profile": {
                                "classes": {
                                    "class": [
                                        {
                                            "class-id": qos_profile_id,
                                            "direction": qos_profile_direction,
                                            "latency": {
                                                "latency-boundary": qos_profile_latency
                                            },
                                            "bandwidth": {
                                                "guaranteed-bw-percent": qos_profile_bw_guarantee
                                            },
                                        }
                                    ]
                                }
                            }
                        },
                    },
                }
            ]
        },
    }


def setup_config_rules(
    service_uuid: str, json_settings: Dict, operation_type: str
) -> List[Dict]:
    # --- Extract common or required fields for the source site ---
    src_device_uuid: str = json_settings["src_device_name"]
    src_endpoint_uuid: str = json_settings["src_endpoint_name"]
    src_site_location: str = json_settings["src_site_location"]
    src_ipv4_lan_prefixes: list[LANPrefixesDict] = json_settings.get(
        "src_ipv4_lan_prefixes"
    )
    src_site_id: str = json_settings.get("src_site_id", f"site_{src_site_location}")
    src_management_type: str = json_settings.get(
        "src_management_type", "ietf-l3vpn-svc:provider-managed"
    )
    if src_management_type != "ietf-l3vpn-svc:provider-managed":
        raise Exception("management type %s not supported", src_management_type)

    src_role: str = "ietf-l3vpn-svc:hub-role"
    src_ce_address: str = json_settings["src_ce_address"]
    src_pe_address: str = json_settings["src_pe_address"]
    src_ce_pe_network_prefix: int = json_settings["src_ce_pe_network_prefix"]
    src_mtu: int = json_settings["src_mtu"]
    src_input_bw: int = json_settings["src_input_bw"]
    src_output_bw: int = json_settings["src_output_bw"]
    src_qos_profile_id = "qos-realtime"
    src_qos_profile_direction = "ietf-l3vpn-svc:both"
    src_qos_profile_latency: int = json_settings["src_qos_profile_latency"]
    src_qos_profile_bw_guarantee: int = json_settings.get(
        "src_qos_profile_bw_guarantee", 100
    )

    # --- Extract common or required fields for the destination site ---
    dst_device_uuid = json_settings["dst_device_name"]
    dst_endpoint_uuid = json_settings["dst_endpoint_name"]
    dst_site_location: str = json_settings["dst_site_location"]
    dst_ipv4_lan_prefixes: list[LANPrefixesDict] = json_settings[
        "dst_ipv4_lan_prefixes"
    ]
    dst_site_id: str = json_settings.get("dst_site_id", f"site_{dst_site_location}")
    dst_management_type: str = json_settings.get(
        "dst_management_type", "ietf-l3vpn-svc:provider-managed"
    )
    if dst_management_type != "ietf-l3vpn-svc:provider-managed":
        raise Exception("management type %s not supported", dst_management_type)

    dst_role: str = "ietf-l3vpn-svc:spoke-role"
    dst_ce_address: str = json_settings["dst_ce_address"]
    dst_pe_address: str = json_settings["dst_pe_address"]
    dst_ce_pe_network_prefix: int = json_settings["dst_ce_pe_network_prefix"]
    dst_mtu: int = json_settings["dst_mtu"]
    dst_input_bw: int = json_settings["dst_input_bw"]
    dst_output_bw: int = json_settings["dst_output_bw"]
    dst_qos_profile_id = "qos-realtime"
    dst_qos_profile_direction = "ietf-l3vpn-svc:both"
    dst_qos_profile_latency: int = json_settings["dst_qos_profile_latency"]
    dst_qos_profile_bw_guarantee: int = json_settings.get(
        "dst_qos_profile_bw_guarantee", 100
    )

    # --- Build site dictionaries using the helper function ---
    src_site_dict = create_site_dict(
        site_id=src_site_id,
        site_location=src_site_location,
        device_uuid=src_device_uuid,
        endpoint_uuid=src_endpoint_uuid,
        service_uuid=service_uuid,
        role=src_role,
        management_type=src_management_type,
        ce_address=src_ce_address,
        pe_address=src_pe_address,
        ce_pe_network_prefix=src_ce_pe_network_prefix,
        mtu=src_mtu,
        input_bw=src_input_bw,
        output_bw=src_output_bw,
        qos_profile_id=src_qos_profile_id,
        qos_profile_direction=src_qos_profile_direction,
        qos_profile_latency=src_qos_profile_latency,
        qos_profile_bw_guarantee=src_qos_profile_bw_guarantee,
        lan_prefixes=src_ipv4_lan_prefixes,
    )

    dst_site_dict = create_site_dict(
        site_id=dst_site_id,
        site_location=dst_site_location,
        device_uuid=dst_device_uuid,
        endpoint_uuid=dst_endpoint_uuid,
        service_uuid=service_uuid,
        role=dst_role,
        management_type=dst_management_type,
        ce_address=dst_ce_address,
        pe_address=dst_pe_address,
        ce_pe_network_prefix=dst_ce_pe_network_prefix,
        mtu=dst_mtu,
        input_bw=dst_input_bw,
        output_bw=dst_output_bw,
        qos_profile_id=dst_qos_profile_id,
        qos_profile_direction=dst_qos_profile_direction,
        qos_profile_latency=dst_qos_profile_latency,
        qos_profile_bw_guarantee=dst_qos_profile_bw_guarantee,
        lan_prefixes=dst_ipv4_lan_prefixes,
    )

    # --- Combine both sites into one structure ---
    sites = {
        "site": [
            src_site_dict,
            dst_site_dict,
        ]
    }

    l3_vpn_data_model = {
        "ietf-l3vpn-svc:l3vpn-svc": {
            "vpn-services": {"vpn-service": [{"vpn-id": service_uuid}]},
            "sites": sites,
        }
    }

    json_config_rules = [
        json_config_rule_set(
            "/service[{:s}]/IETFL3VPN".format(service_uuid),
            l3_vpn_data_model,
        ),
        #json_config_rule_set(
        #    "/service[{:s}]/IETFL3VPN/operation".format(service_uuid),
        #    {"type": operation_type},
        #),
    ]

    return json_config_rules


def teardown_config_rules(service_uuid: str) -> List[Dict]:
    json_config_rules = [
        json_config_rule_delete(
            "/service[{:s}]/IETFL3VPN".format(service_uuid),
            {"id": service_uuid},
        ),
        #json_config_rule_delete(
        #    "/service[{:s}]/IETFL3VPN/operation".format(service_uuid),
        #    {},
        #),
    ]
    return json_config_rules


def get_link_ep_device_names(
    link: Link, context_client: ContextClient
) -> Tuple[str, str, str, str]:
    ep_ids = link.link_endpoint_ids
    ep_device_id_1 = ep_ids[0].device_id
    ep_uuid_1 = ep_ids[0].endpoint_uuid.uuid
    device_obj_1 = context_client.GetDevice(ep_device_id_1)
    for d_ep in device_obj_1.device_endpoints:
        if d_ep.endpoint_id.endpoint_uuid.uuid == ep_uuid_1:
            ep_name_1 = d_ep.name
            break
    else:
        raise Exception("endpoint not found")
    device_obj_name_1 = device_obj_1.name
    ep_device_id_2 = ep_ids[1].device_id
    ep_uuid_2 = ep_ids[1].endpoint_uuid.uuid
    device_obj_2 = context_client.GetDevice(ep_device_id_2)
    for d_ep in device_obj_2.device_endpoints:
        if d_ep.endpoint_id.endpoint_uuid.uuid == ep_uuid_2:
            ep_name_2 = d_ep.name
            break
    else:
        raise Exception("endpoint not found")
    device_obj_name_2 = device_obj_2.name
    return (
        device_obj_name_1,
        ep_name_1,
        device_obj_1,
        device_obj_name_2,
        ep_name_2,
        device_obj_2,
    )
