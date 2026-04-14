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
import logging
import re
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

from deepdiff import DeepDiff
from dataclasses import dataclass

from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, DeviceId, Empty, Service, ServiceConfig
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from context.client.ContextClient import ContextClient
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.service_handler_api.Tools import (
    get_device_endpoint_uuids,
)
from service.service.task_scheduler.TaskExecutor import TaskExecutor

from .ConfigRules import (
    get_link_ep_device_names,
    setup_config_rules,
    teardown_config_rules,
)

RUNNING_RESOURCE_KEY = "running_ietf_slice"
CANDIDATE_RESOURCE_KEY = "candidate_ietf_slice"

SDP_DIFF_RE = re.compile(
    r"^root\[\'network-slice-services\'\]\[\'slice-service\'\]\[0\]\[\'sdps\'\]\[\'sdp\'\]\[(\d)\]$"
)
CONNECTION_GROUP_DIFF_RE = re.compile(
    r"^root\[\'network-slice-services\'\]\[\'slice-service\'\]\[0\]\[\'connection-groups\'\]\[\'connection-group\'\]\[(\d)\]$"
)
MATCH_CRITERION_DIFF_RE = re.compile(
    r"^root\[\'network-slice-services\'\]\[\'slice-service\'\]\[0\]\[\'sdps\'\]\[\'sdp\'\]\[(\d)\]\[\'service-match-criteria\'\]\[\'match-criterion\'\]\[(\d)\]$"
)

RE_GET_ENDPOINT_FROM_INTERFACE = re.compile(r"^\/interface\[([^\]]+)\].*")

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool(
    "Service", "Handler", labels={"handler": "l3slice_ietfslice"}
)


RAISE_IF_DIFFERS = True


class Ipv4Info(TypedDict):
    src_lan: str
    dst_lan: str
    src_port: str
    dst_port: str
    vlan: str


class DeviceEpInfo(TypedDict):
    ipv4_info: Ipv4Info
    node_name: str
    endpoint_name: str
    one_way_delay: int
    one_way_bandwidth: int
    one_way_packet_loss: float


@dataclass
class ConnectivityConstructInfo:
    bandwidth: int = 0
    delay: int = 0
    packet_loss: float = 0.0


def get_custom_config_rule(
    service_config: ServiceConfig, resource_key: str
) -> Optional[ConfigRule]:
    """
    Returns the ConfigRule from service_config matching the provided resource_key
    if found, otherwise returns None.
    """
    for cr in service_config.config_rules:
        if (
            cr.WhichOneof("config_rule") == "custom"
            and cr.custom.resource_key == resource_key
        ):
            return cr
    return None


def get_running_candidate_ietf_slice_data_diff(service_config: ServiceConfig) -> Dict:
    """
    Loads the JSON from the running/candidate resource ConfigRules and returns
    their DeepDiff comparison.
    """
    running_cr = get_custom_config_rule(service_config, RUNNING_RESOURCE_KEY)
    candidate_cr = get_custom_config_rule(service_config, CANDIDATE_RESOURCE_KEY)
    running_value_dict = json.loads(running_cr.custom.resource_value)
    candidate_value_dict = json.loads(candidate_cr.custom.resource_value)
    return DeepDiff(running_value_dict, candidate_value_dict)


def extract_match_criterion_ipv4_info(match_criterion: Dict) -> Ipv4Info:
    """
    Extracts IPv4 info from the match criterion dictionary.
    """
    src_lan = dst_lan = src_port = dst_port = vlan = ""
    for type_value in match_criterion["match-type"]:
        m_type = type_value["type"]
        val = type_value["value"][0]
        if m_type == "ietf-network-slice-service:source-ip-prefix":
            src_lan = val
        elif m_type == "ietf-network-slice-service:destination-ip-prefix":
            dst_lan = val
        elif m_type == "ietf-network-slice-service:source-tcp-port":
            src_port = val
        elif m_type == "ietf-network-slice-service:destination-tcp-port":
            dst_port = val
        elif m_type == "ietf-network-slice-service:vlan":
            vlan = val
    return Ipv4Info(
        src_lan=src_lan,
        dst_lan=dst_lan,
        src_port=src_port,
        dst_port=dst_port,
        vlan=vlan,
    )


def get_removed_items(
    candidate_ietf_slice_dict: dict, running_ietf_slice_dict: dict
) -> dict:
    """
    For the 'iterable_item_removed' scenario, returns dict with removed sdp / connection_group / match_criterion info.
    Raises an exception if there's inconsistent data or multiple items removed (which is not supported).
    """
    removed_items = {
        "sdp": {"sdp_idx": None, "value": {}},
        "connection_group": {"connection_group_idx": None, "value": {}},
        "match_criterion": {
            "sdp_idx": None,
            "match_criterion_idx": None,
            "value": {},
        },
    }

    running_slice_services = running_ietf_slice_dict["network-slice-services"][
        "slice-service"
    ][0]
    candidate_slice_services = candidate_ietf_slice_dict["network-slice-services"][
        "slice-service"
    ][0]

    running_slice_sdps = [sdp["id"] for sdp in running_slice_services["sdps"]["sdp"]]
    candidiate_slice_sdps = [
        sdp["id"] for sdp in candidate_slice_services["sdps"]["sdp"]
    ]
    removed_sdps = set(running_slice_sdps) - set(candidiate_slice_sdps)

    if len(removed_sdps) > 1:
        raise Exception("Multiple SDPs removed - not supported.")
    removed_sdp_id = removed_sdps.pop()

    removed_items["sdp"]["sdp_idx"] = running_slice_sdps.index(removed_sdp_id)
    removed_items["sdp"]["value"] = next(
        sdp
        for sdp in running_slice_services["sdps"]["sdp"]
        if sdp["id"] == removed_sdp_id
    )

    match_criteria = removed_items["sdp"]["value"]["service-match-criteria"][
        "match-criterion"
    ]
    if len(match_criteria) > 1:
        raise Exception("Multiple match criteria found - not supported")
    match_criterion = match_criteria[0]
    connection_grp_id = match_criterion["target-connection-group-id"]
    connection_groups = running_slice_services["connection-groups"]["connection-group"]
    connection_group = next(
        (idx, cg)
        for idx, cg in enumerate(connection_groups)
        if cg["id"] == connection_grp_id
    )
    removed_items["connection_group"]["connection_group_idx"] = connection_group[0]
    removed_items["connection_group"]["value"] = connection_group[1]

    for sdp in running_slice_services["sdps"]["sdp"]:
        if sdp["id"] == removed_sdp_id:
            continue
        for mc in sdp["service-match-criteria"]["match-criterion"]:
            if mc["target-connection-group-id"] == connection_grp_id:
                removed_items["match_criterion"]["sdp_idx"] = running_slice_sdps.index(
                    sdp["id"]
                )
                removed_items["match_criterion"]["match_criterion_idx"] = sdp[
                    "service-match-criteria"
                ]["match-criterion"].index(mc)
                removed_items["match_criterion"]["value"] = mc
                break

    if (
        removed_items["match_criterion"]["sdp_idx"] is None
        or removed_items["sdp"]["sdp_idx"] is None
        or removed_items["connection_group"]["connection_group_idx"] is None
    ):
        raise Exception("sdp, connection group or match criterion not found")
    return removed_items


def gather_connectivity_construct_info(
    candidate_connection_groups: List[Dict],
) -> Dict[Tuple[str, str], ConnectivityConstructInfo]:
    """
    Creates a dict mapping (sender_sdp, receiver_sdp) -> ConnectivityConstructInfo
    from the given list of candidate connection groups.
    """
    cc_info: Dict[Tuple[str, str], ConnectivityConstructInfo] = {}
    for cg in candidate_connection_groups:
        for cc in cg["connectivity-construct"]:
            cc_sender = cc["p2p-sender-sdp"]
            cc_receiver = cc["p2p-receiver-sdp"]
            cc_key = (cc_sender, cc_receiver)
            cc_info[cc_key] = ConnectivityConstructInfo()
            for metric_bound in cc["service-slo-sle-policy"]["slo-policy"][
                "metric-bound"
            ]:
                if (
                    metric_bound["metric-type"]
                    == "ietf-network-slice-service:one-way-delay-maximum"
                    and metric_bound["metric-unit"] == "milliseconds"
                ):
                    cc_info[cc_key].delay = int(metric_bound["bound"])
                elif (
                    metric_bound["metric-type"]
                    == "ietf-network-slice-service:two-way-packet-loss"
                    and metric_bound["metric-unit"] == "percentage"
                ):
                    cc_info[cc_key].packet_loss = float(
                        metric_bound["percentile-value"]
                    )
                elif (
                    metric_bound["metric-type"]
                    == "ietf-network-slice-service:one-way-bandwidth"
                    and metric_bound["metric-unit"] == "Mbps"
                ):
                    cc_info[cc_key].bandwidth = int(metric_bound["bound"])
    return cc_info


def extract_source_destination_device_endpoint_info(
    device_ep_pairs: list, connection_group: Dict, candidate_connection_groups: List
) -> Tuple[DeviceEpInfo, DeviceEpInfo]:
    """
    Given device_ep_pairs, the relevant connection_group data, and all candidate
    connection groups, figure out the final DeviceEpInfo for source and destination.
    This includes computing the combined bandwidth, min delay, etc.
    """
    connectivity_construct = connection_group["connectivity-construct"][0]
    sender_sdp = connectivity_construct["p2p-sender-sdp"]
    receiver_sdp = connectivity_construct["p2p-receiver-sdp"]

    # If the first pair is not the sender, we invert them
    if sender_sdp == device_ep_pairs[0][4]:
        ...
    elif sender_sdp == device_ep_pairs[1][4]:
        device_ep_pairs = device_ep_pairs[::-1]
    else:
        raise Exception("Sender SDP not found in device_ep_pairs")

    # Gather info from candidate connection groups
    cc_info = gather_connectivity_construct_info(candidate_connection_groups)

    source_delay = int(1e6)
    source_bandwidth = 0
    source_packet_loss = 1.0
    destination_delay = int(1e6)
    destination_bandwidth = 0
    destination_packet_loss = 1.0

    if cc_info:
        common_sdps = set.intersection(*[set(key) for key in cc_info.keys()])
        if len(cc_info) > 2 and len(common_sdps) != 1:
            raise Exception(
                "There should be one common sdp in all connectivity constructs, otherwise, it is not supported"
            )
        if len(common_sdps) == 1:
            common_sdp = common_sdps.pop()
        elif len(common_sdps) == 2:
            # Fallback if intersection is 2 => pick sender_sdp
            common_sdp = sender_sdp
        else:
            raise Exception("Invalid number of common sdps")

    for (sender, receiver), metrics in cc_info.items():
        cc_bandwidth = metrics.bandwidth
        cc_max_delay = metrics.delay
        cc_packet_loss = metrics.packet_loss
        if sender == common_sdp:
            source_bandwidth += cc_bandwidth
            if cc_max_delay < source_delay:
                source_delay = cc_max_delay
            if cc_packet_loss < source_packet_loss:
                source_packet_loss = cc_packet_loss
        else:
            destination_bandwidth += cc_bandwidth
            if cc_max_delay < destination_delay:
                destination_delay = cc_max_delay
            if cc_packet_loss < destination_packet_loss:
                destination_packet_loss = cc_packet_loss

    source_device_ep_info = DeviceEpInfo(
        ipv4_info=device_ep_pairs[0][5],
        node_name=device_ep_pairs[0][2],
        endpoint_name=device_ep_pairs[0][3],
        one_way_delay=source_delay,
        one_way_bandwidth=source_bandwidth,
        one_way_packet_loss=source_packet_loss,
    )
    destination_device_ep_info = DeviceEpInfo(
        ipv4_info=device_ep_pairs[1][5],
        node_name=device_ep_pairs[1][2],
        endpoint_name=device_ep_pairs[1][3],
        one_way_delay=destination_delay,
        one_way_bandwidth=destination_bandwidth,
        one_way_packet_loss=destination_packet_loss,
    )

    return source_device_ep_info, destination_device_ep_info


def _parse_item_added(diff: Dict) -> dict:
    """
    Helper to parse 'iterable_item_added' from the running_candidate_diff
    and return the relevant items for sdp, connection_group, match_criterion, etc.
    """
    added_items = {
        "sdp": {"sdp_idx": None, "value": {}},
        "connection_group": {"connection_group_idx": None, "value": {}},
        "match_criterion": {
            "sdp_idx": None,
            "match_criterion_idx": None,
            "value": {},
        },
    }
    for added_key, added_value in diff["iterable_item_added"].items():
        sdp_match = SDP_DIFF_RE.match(added_key)
        connection_group_match = CONNECTION_GROUP_DIFF_RE.match(added_key)
        match_criterion_match = MATCH_CRITERION_DIFF_RE.match(added_key)
        if sdp_match:
            added_items["sdp"] = {
                "sdp_idx": int(sdp_match.groups()[0]),
                "value": added_value,
            }
        elif connection_group_match:
            added_items["connection_group"] = {
                "connection_group_idx": int(connection_group_match.groups()[0]),
                "value": added_value,
            }
        elif match_criterion_match:
            added_items["match_criterion"] = {
                "sdp_idx": int(match_criterion_match.groups()[0]),
                "match_criterion_idx": int(match_criterion_match.groups()[1]),
                "value": added_value,
            }
    return added_items


class L3NM_IETFSlice_ServiceHandler(_ServiceHandler):
    def __init__(  # pylint: disable=super-init-not-called
        self, service: Service, task_executor: TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(service.service_config, **settings)

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        chk_type("endpoints", endpoints, list)
        if len(endpoints) == 0:
            return []

        results = []
        try:
            service_config = self.__service.service_config

            # 1. Identify source and destination devices
            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[0])
            src_device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(src_device_uuid))
            )
            src_device_name = src_device_obj.name
            src_controller = self.__task_executor.get_device_controller(src_device_obj)

            dst_device_uuid, dst_endpoint_uuid = get_device_endpoint_uuids(
                endpoints[-1]
            )
            dst_device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(dst_device_uuid))
            )
            dst_device_name = dst_device_obj.name
            dst_controller = self.__task_executor.get_device_controller(dst_device_obj)

            if (
                src_controller.device_id.device_uuid.uuid
                != dst_controller.device_id.device_uuid.uuid
            ):
                raise Exception("Different Src-Dst devices not supported by now")

            controller = src_controller  # same device controller

            # 2. Determine how the candidate & running resources differ
            running_candidate_diff = get_running_candidate_ietf_slice_data_diff(
                service_config
            )
            candidate_ietf_slice_cr = get_custom_config_rule(
                service_config, CANDIDATE_RESOURCE_KEY
            )
            candidate_resource_value_dict = json.loads(
                candidate_ietf_slice_cr.custom.resource_value
            )
            running_ietf_slice_cr = get_custom_config_rule(
                service_config, RUNNING_RESOURCE_KEY
            )
            running_resource_value_dict = json.loads(
                running_ietf_slice_cr.custom.resource_value
            )
            slice_name = running_resource_value_dict["network-slice-services"][
                "slice-service"
            ][0]["id"]

            # 3. Retrieve the context links for matching endpoints
            context_client = ContextClient()
            links = context_client.ListLinks(Empty()).links

            device_ep_pairs = []
            sdp_ids = []
            target_connection_group_id = None
            operation_type = "update"  # default fallback

            # 4. Handle creation vs additions vs removals
            if not running_candidate_diff:  # Slice Creation
                # 4a. New Slice Creation
                operation_type = "create"

                candidate_slice_service = candidate_resource_value_dict[
                    "network-slice-services"
                ]["slice-service"][0]
                full_connection_groups = candidate_slice_service["connection-groups"][
                    "connection-group"
                ]
                sdps = candidate_slice_service["sdps"]["sdp"]
                sdp_ids = [sdp["node-id"] for sdp in sdps]

                # figure out which device is connected to which link
                edge_device_names = [src_device_name, dst_device_name]
                for sdp in sdps:
                    node_id = sdp["node-id"]
                    for link in links:
                        info = get_link_ep_device_names(link, context_client)
                        dev1, ep1, _, dev2, ep2, _ = info
                        if dev1 == node_id and dev2 in edge_device_names:
                            edge_device_names.remove(dev2)
                            match_criteria = sdp["service-match-criteria"][
                                "match-criterion"
                            ]
                            if len(match_criteria) != 1:
                                raise Exception(
                                    "Only one match criteria allowed for initial slice creation"
                                )
                            match_criterion = match_criteria[0]
                            ipv4_info = extract_match_criterion_ipv4_info(
                                match_criterion
                            )
                            device_ep_pairs.append(
                                (
                                    node_id,
                                    ep1,
                                    dev2,
                                    ep2,
                                    sdp["id"],
                                    ipv4_info,
                                )
                            )
                            target_connection_group_id = match_criterion[
                                "target-connection-group-id"
                            ]
                            sdp_ids.remove(node_id)
                            break

                # find the second link
                if not edge_device_names:
                    raise Exception("Edge device names exhausted unexpectedly.")

                # second link logic
                for link in links:
                    info = get_link_ep_device_names(link, context_client)
                    dev1, ep1, device_obj_1, dev2, ep2, device_obj_2 = info
                    if (
                        dev1 == edge_device_names[0]
                        and device_obj_2.controller_id != device_obj_1.controller_id
                    ):
                        for sdp in sdps:
                            if sdp["node-id"] != sdp_ids[0]:
                                continue
                            match_criteria = sdp["service-match-criteria"][
                                "match-criterion"
                            ]
                            if len(match_criteria) != 1:
                                raise Exception(
                                    "Only one match criteria allowed for initial slice creation"
                                )
                            match_criterion = match_criteria[0]
                            ipv4_info = extract_match_criterion_ipv4_info(
                                match_criterion
                            )
                            device_ep_pairs.append(
                                (
                                    dev2,
                                    ep2,
                                    dev1,
                                    ep1,
                                    sdp["id"],
                                    ipv4_info,
                                )
                            )
                            break
                        else:
                            raise Exception("No matching sdp found for second link.")
                        break
                else:
                    raise Exception("sdp between the domains not found")

            elif "iterable_item_added" in running_candidate_diff:  # new SDP added
                # 4b. A new SDP was added
                operation_type = "update"

                candidate_slice_service = candidate_resource_value_dict[
                    "network-slice-services"
                ]["slice-service"][0]
                sdps = candidate_slice_service["sdps"]["sdp"]
                full_connection_groups = candidate_slice_service["connection-groups"][
                    "connection-group"
                ]
                added_items = _parse_item_added(running_candidate_diff)

                new_sdp = sdps[added_items["sdp"]["sdp_idx"]]
                src_sdp_name = new_sdp["node-id"]
                dst_sdp_idx = sdps[added_items["match_criterion"]["sdp_idx"]]["id"]
                dst_sdp_name = sdps[added_items["match_criterion"]["sdp_idx"]][
                    "node-id"
                ]
                for link in links:
                    info = get_link_ep_device_names(link, context_client)
                    dev1, ep1, device_obj_1, dev2, ep2, device_obj_2 = info
                    if (
                        dev1 == src_sdp_name
                        and device_obj_2.controller_id != device_obj_1.controller_id
                    ):
                        for sdp in sdps:
                            if sdp["node-id"] != src_sdp_name:
                                continue
                            match_criteria = sdp["service-match-criteria"][
                                "match-criterion"
                            ]
                            if len(match_criteria) != 1:
                                raise Exception(
                                    "Only one match criteria allowed for initial slice creation"
                                )
                            match_criterion = match_criteria[0]
                            ipv4_info = extract_match_criterion_ipv4_info(
                                match_criterion
                            )
                            device_ep_pairs.append(
                                (
                                    dev2,
                                    ep2,
                                    dev1,
                                    ep1,
                                    sdp["id"],
                                    ipv4_info,
                                )
                            )
                            target_connection_group_id = match_criterion[
                                "target-connection-group-id"
                            ]
                        break
                else:
                    raise Exception("sdp between the domains not found")
                for link in links:
                    info = get_link_ep_device_names(link, context_client)
                    dev1, ep1, device_obj_1, dev2, ep2, device_obj_2 = info
                    if (
                        dev1 == dst_sdp_name
                        and device_obj_2.controller_id != device_obj_1.controller_id
                    ):
                        for sdp in sdps:
                            if sdp["node-id"] != dst_sdp_name:
                                continue
                            match_criteria = sdp["service-match-criteria"][
                                "match-criterion"
                            ]
                            vlan_id = set()
                            for match in match_criteria:
                                for type_value in match["match-type"]:
                                    if (
                                        type_value["type"]
                                        == "ietf-network-slice-service:vlan"
                                    ):
                                        vlan_id.add(type_value["value"][0])
                            if len(vlan_id) != 1:
                                raise Exception(
                                    "one vlan id found in SDP match criteria"
                                )
                            match_criterion = match_criteria[
                                added_items["match_criterion"]["match_criterion_idx"]
                            ]
                            ipv4_info = extract_match_criterion_ipv4_info(
                                match_criterion
                            )
                            device_ep_pairs.append(
                                (
                                    dev2,
                                    ep2,
                                    dev1,
                                    ep1,
                                    sdp["id"],
                                    ipv4_info,
                                )
                            )
                        break
                else:
                    raise Exception("sdp between the domains not found")
            elif "iterable_item_removed" in running_candidate_diff:  # an SDP removed
                # 4c. An existing SDP was removed
                operation_type = "update"

                slice_services = running_resource_value_dict["network-slice-services"][
                    "slice-service"
                ]
                candidate_slice_services = candidate_resource_value_dict[
                    "network-slice-services"
                ]["slice-service"]
                candidate_slice_service = candidate_slice_services[0]
                slice_service = slice_services[0]
                full_connection_groups = slice_service["connection-groups"][
                    "connection-group"
                ]
                sdps = slice_service["sdps"]["sdp"]
                removed_items = get_removed_items(
                    candidate_resource_value_dict, running_resource_value_dict
                )
                new_sdp = sdps[removed_items["sdp"]["sdp_idx"]]
                src_sdp_name = new_sdp["node-id"]
                dst_sdp_idx = sdps[removed_items["match_criterion"]["sdp_idx"]]["id"]
                dst_sdp_name = sdps[removed_items["match_criterion"]["sdp_idx"]][
                    "node-id"
                ]
                for link in links:
                    (
                        device_obj_name_1,
                        ep_name_1,
                        device_obj_1,
                        device_obj_name_2,
                        ep_name_2,
                        device_obj_2,
                    ) = get_link_ep_device_names(link, context_client)
                    if (
                        device_obj_name_1 == src_sdp_name
                        and device_obj_2.controller_id != device_obj_1.controller_id
                    ):
                        for sdp in sdps:
                            if sdp["node-id"] != src_sdp_name:
                                continue
                            match_criteria = sdp["service-match-criteria"][
                                "match-criterion"
                            ]
                            if len(match_criteria) != 1:
                                raise Exception(
                                    "Only one match criteria allowed for new SDP addition"
                                )
                            match_criterion = match_criteria[0]
                            ipv4_info = extract_match_criterion_ipv4_info(
                                match_criterion
                            )
                            device_ep_pairs.append(
                                (
                                    device_obj_name_2,
                                    ep_name_2,
                                    device_obj_name_1,
                                    ep_name_1,
                                    sdp["id"],
                                    ipv4_info,
                                )
                            )
                            target_connection_group_id = match_criterion[
                                "target-connection-group-id"
                            ]
                        break
                else:
                    raise Exception("sdp between the domains not found")
                for link in links:
                    (
                        device_obj_name_1,
                        ep_name_1,
                        device_obj_1,
                        device_obj_name_2,
                        ep_name_2,
                        device_obj_2,
                    ) = get_link_ep_device_names(link, context_client)
                    if (
                        device_obj_name_1 == dst_sdp_name
                        and device_obj_2.controller_id != device_obj_1.controller_id
                    ):
                        for sdp in sdps:
                            if sdp["node-id"] != dst_sdp_name:
                                continue
                            match_criteria = sdp["service-match-criteria"][
                                "match-criterion"
                            ]
                            vlan_id = set()
                            for match in match_criteria:
                                for type_value in match["match-type"]:
                                    if (
                                        type_value["type"]
                                        == "ietf-network-slice-service:vlan"
                                    ):
                                        vlan_id.add(type_value["value"][0])
                            if len(vlan_id) != 1:
                                raise Exception(
                                    "one vlan id found in SDP match criteria"
                                )
                            match_criterion = match_criteria[
                                removed_items["match_criterion"]["match_criterion_idx"]
                            ]
                            ipv4_info = extract_match_criterion_ipv4_info(
                                match_criterion
                            )
                            device_ep_pairs.append(
                                (
                                    device_obj_name_2,
                                    ep_name_2,
                                    device_obj_name_1,
                                    ep_name_1,
                                    sdp["id"],
                                    ipv4_info,
                                )
                            )
                        break
                else:
                    raise Exception("sdp between the domains not found")
            else:
                raise Exception(
                    "transition from candidate to running info not supported"
                )

            candidate_connection_groups = candidate_slice_service["connection-groups"][
                "connection-group"
            ]

            if (
                len(
                    candidate_resource_value_dict["network-slice-services"][
                        "slice-service"
                    ][0]["connection-groups"]["connection-group"]
                )
                == 0
            ):
                # 5. If connection_groups is now empty => operation = delete
                operation_type = "delete"

            # 6. Retrieve actual target connection_group from the full connection groups
            if not target_connection_group_id:
                raise Exception("No target_connection_group_id found.")
            target_connection_group = next(
                cg
                for cg in full_connection_groups
                if cg["id"] == target_connection_group_id
            )

            # 7. Build source/destination device info
            source_device_ep_info, destination_device_ep_info = (
                extract_source_destination_device_endpoint_info(
                    device_ep_pairs,
                    target_connection_group,
                    candidate_connection_groups,
                )
            )
            resource_value_dict = {
                "uuid": slice_name,
                "operation_type": operation_type,
                "src_node_id": source_device_ep_info["node_name"],
                "src_mgmt_ip_address": source_device_ep_info["node_name"],
                "src_ac_node_id": source_device_ep_info["node_name"],
                "src_ac_ep_id": source_device_ep_info["endpoint_name"],
                "src_vlan": source_device_ep_info["ipv4_info"]["vlan"],
                "src_source_ip_prefix": source_device_ep_info["ipv4_info"]["src_lan"],
                "src_source_tcp_port": source_device_ep_info["ipv4_info"]["src_port"],
                "src_destination_ip_prefix": source_device_ep_info["ipv4_info"][
                    "dst_lan"
                ],
                "src_destination_tcp_port": source_device_ep_info["ipv4_info"][
                    "dst_port"
                ],
                "source_one_way_delay": source_device_ep_info["one_way_delay"],
                "source_one_way_bandwidth": source_device_ep_info["one_way_bandwidth"],
                "source_one_way_packet_loss": source_device_ep_info[
                    "one_way_packet_loss"
                ],
                "dst_node_id": destination_device_ep_info["node_name"],
                "dst_mgmt_ip_address": destination_device_ep_info["node_name"],
                "dst_ac_node_id": destination_device_ep_info["node_name"],
                "dst_ac_ep_id": destination_device_ep_info["endpoint_name"],
                "dst_vlan": destination_device_ep_info["ipv4_info"]["vlan"],
                "dst_source_ip_prefix": destination_device_ep_info["ipv4_info"][
                    "src_lan"
                ],
                "dst_source_tcp_port": destination_device_ep_info["ipv4_info"][
                    "src_port"
                ],
                "dst_destination_ip_prefix": destination_device_ep_info["ipv4_info"][
                    "dst_lan"
                ],
                "dst_destination_tcp_port": destination_device_ep_info["ipv4_info"][
                    "dst_port"
                ],
                "destination_one_way_delay": destination_device_ep_info[
                    "one_way_delay"
                ],
                "destination_one_way_bandwidth": destination_device_ep_info[
                    "one_way_bandwidth"
                ],
                "destination_one_way_packet_loss": destination_device_ep_info[
                    "one_way_packet_loss"
                ],
                "slice_id": slice_name,
            }

            # 9. Create config rules and configure device
            json_config_rules = setup_config_rules(slice_name, resource_value_dict)
            del controller.device_config.config_rules[:]
            for jcr in json_config_rules:
                controller.device_config.config_rules.append(ConfigRule(**jcr))

            self.__task_executor.configure_device(controller)
        except Exception as e:  # pylint: disable=broad-except
            raise e
            results.append(e)
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        chk_type("endpoints", endpoints, list)
        if len(endpoints) == 0:
            return []
        service_uuid = self.__service.service_id.service_uuid.uuid
        results = []
        try:
            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[0])
            src_device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(src_device_uuid))
            )
            controller = self.__task_executor.get_device_controller(src_device_obj)
            json_config_rules = teardown_config_rules(service_uuid, {})
            if len(json_config_rules) > 0:
                del controller.device_config.config_rules[:]
                for json_config_rule in json_config_rules:
                    controller.device_config.config_rules.append(
                        ConfigRule(**json_config_rule)
                    )
                self.__task_executor.configure_device(controller)
            results.append(True)
        except Exception as e:  # pylint: disable=broad-except
            results.append(e)
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConstraint(
        self, constraints: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type("constraints", constraints, list)
        if len(constraints) == 0:
            return []

        msg = "[SetConstraint] Method not implemented. Constraints({:s}) are being ignored."
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConstraint(
        self, constraints: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type("constraints", constraints, list)
        if len(constraints) == 0:
            return []

        msg = "[DeleteConstraint] Method not implemented. Constraints({:s}) are being ignored."
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(
        self, resources: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type("resources", resources, list)
        if len(resources) == 0:
            return []

        results = []
        for resource in resources:
            try:
                resource_value = json.loads(resource[1])
                self.__settings_handler.set(resource[0], resource_value)
                results.append(True)
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception("Unable to SetConfig({:s})".format(str(resource)))
                results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(
        self, resources: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type("resources", resources, list)
        if len(resources) == 0:
            return []

        results = []
        for resource in resources:
            try:
                self.__settings_handler.delete(resource[0])
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception("Unable to DeleteConfig({:s})".format(str(resource)))
                results.append(e)

        return results
