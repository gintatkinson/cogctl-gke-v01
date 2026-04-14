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

import json, logging, re
from typing import Any, List, Optional, Tuple, Union, TypedDict, Dict
from uuid import uuid4

from deepdiff import DeepDiff

from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, DeviceId, Empty, Service, ServiceConfig
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from context.client.ContextClient import ContextClient
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.Tools import (
    get_device_endpoint_uuids,
)
from service.service.task_scheduler.TaskExecutor import TaskExecutor

from .ConfigRules import setup_config_rules, teardown_config_rules

RUNNING_RESOURCE_KEY = "running_ietf_slice"
CANDIDATE_RESOURCE_KEY = "candidate_ietf_slice"

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool("Service", "Handler", labels={"handler": "l3nm_nce"})

SDP_DIFF_RE = re.compile(
    r"^root\[\'network-slice-services\'\]\[\'slice-service\'\]\[0\]\[\'sdps\'\]\[\'sdp\'\]\[(\d)\]$"
)
CONNECTION_GROUP_DIFF_RE = re.compile(
    r"^root\[\'network-slice-services\'\]\[\'slice-service\'\]\[0\]\[\'connection-groups\'\]\[\'connection-group\'\]\[(\d)\]$"
)
MATCH_CRITERION_DIFF_RE = re.compile(
    r"^root\[\'network-slice-services\'\]\[\'slice-service\'\]\[0\]\[\'sdps\'\]\[\'sdp\'\]\[(\d)\]\[\'service-match-criteria\'\]\[\'match-criterion\'\]\[(\d)\]$"
)


class Ipv4Info(TypedDict):
    src_ip: str
    dst_ip: str
    src_port: str
    dst_port: str


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


def extract_qos_info(
    connection_groups: List, connection_grp_id: str, src_sdp_idx: str, dst_sdp_idx: str
) -> Dict:
    """
    Extract QoS information from connection groups based on the connection group ID.
    """
    qos_info = {
        "upstream": {"max_delay": "0", "bw": "0", "packet_loss": "0"},
        "downstream": {"max_delay": "0", "bw": "0", "packet_loss": "0"},
    }
    connection_group = next(
        (cg for cg in connection_groups if cg["id"] == connection_grp_id), None
    )

    if not connection_group:
        return qos_info

    for cc in connection_group["connectivity-construct"]:
        if (
            cc["p2p-sender-sdp"] == src_sdp_idx
            and cc["p2p-receiver-sdp"] == dst_sdp_idx
        ):
            direction = "upstream"
        elif (
            cc["p2p-sender-sdp"] == dst_sdp_idx
            and cc["p2p-receiver-sdp"] == src_sdp_idx
        ):
            direction = "downstream"
        else:
            raise Exception("invalid sender and receiver sdp ids")
        for metric_bound in cc["service-slo-sle-policy"]["slo-policy"]["metric-bound"]:
            if (
                metric_bound["metric-type"]
                == "ietf-network-slice-service:one-way-delay-maximum"
                and metric_bound["metric-unit"] == "milliseconds"
            ):
                qos_info[direction]["max_delay"] = metric_bound["bound"]
            elif (
                metric_bound["metric-type"]
                == "ietf-network-slice-service:one-way-bandwidth"
                and metric_bound["metric-unit"] == "Mbps"
            ):
                qos_info[direction]["bw"] = metric_bound["bound"]
            elif (
                metric_bound["metric-type"]
                == "ietf-network-slice-service:two-way-packet-loss"
                and metric_bound["metric-unit"] == "percentage"
            ):
                qos_info[direction]["packet_loss"] = metric_bound["percentile-value"]

    return qos_info


def extract_match_criterion_ipv4_info(match_criterion: Dict) -> Ipv4Info:
    """
    Extracts IPv4 info from the match criterion dictionary.
    """
    src_ip = dst_ip = src_port = dst_port = ""

    for type_value in match_criterion["match-type"]:
        m_type = type_value["type"]
        val = type_value["value"][0]
        if m_type == "ietf-network-slice-service:source-ip-prefix":
            src_ip = val.split("/")[0]
        elif m_type == "ietf-network-slice-service:destination-ip-prefix":
            dst_ip = val.split("/")[0]
        elif m_type == "ietf-network-slice-service:source-tcp-port":
            src_port = val
        elif m_type == "ietf-network-slice-service:destination-tcp-port":
            dst_port = val

    return Ipv4Info(
        src_ip=src_ip,
        dst_ip=dst_ip,
        src_port=src_port,
        dst_port=dst_port,
    )


class L3NM_NCEFAN_ServiceHandler(_ServiceHandler):
    def __init__(  # pylint: disable=super-init-not-called
        self, service: Service, task_executor: TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('[SetEndpoint] service={:s}'.format(grpc_message_to_json_string(self.__service)))
        LOGGER.debug('[SetEndpoint] endpoints={:s}'.format(str(endpoints)))
        LOGGER.debug('[SetEndpoint] connection_uuid={:s}'.format(str(connection_uuid)))

        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []

        results = []
        try:
            context_client = ContextClient()
            service_config = self.__service.service_config

            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[0])
            src_device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(src_device_uuid)))
            controller = self.__task_executor.get_device_controller(src_device_obj)

            list_devices = context_client.ListDevices(Empty())
            devices = list_devices.devices
            device_name_map = {d.name: d for d in devices}

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

            service_name = running_resource_value_dict["network-slice-services"][
                "slice-service"
            ][0]["id"]

            if not running_candidate_diff:  # Slice Creation
                operation_type = "create"

                slice_service = candidate_resource_value_dict["network-slice-services"][
                    "slice-service"
                ][0]
                sdps = slice_service["sdps"]["sdp"]
                connection_groups = slice_service["connection-groups"][
                    "connection-group"
                ]
                sdp_ids = [sdp["id"] for sdp in sdps]
                for sdp in sdps:
                    node_id = sdp["node-id"]
                    device_obj = device_name_map[node_id]
                    device_controller = self.__task_executor.get_device_controller(
                        device_obj
                    )
                    if (
                        device_controller is None
                        or controller.name != device_controller.name
                    ):
                        continue
                    src_sdp_idx = sdp_ids.pop(sdp_ids.index(sdp["id"]))
                    dst_sdp_idx = sdp_ids[0]
                    match_criteria = sdp["service-match-criteria"]["match-criterion"]
                    match_criterion = match_criteria[0]
                    connection_grp_id = match_criterion["target-connection-group-id"]
                    break
                else:
                    raise Exception("connection group id not found")
            elif "iterable_item_added" in running_candidate_diff:  # new SDP added
                operation_type = "create"

                slice_service = candidate_resource_value_dict["network-slice-services"][
                    "slice-service"
                ][0]
                sdps = slice_service["sdps"]["sdp"]
                connection_groups = slice_service["connection-groups"][
                    "connection-group"
                ]
                added_items = {
                    "sdp": {"sdp_idx": None, "value": {}},
                    "connection_group": {"connection_group_idx": None, "value": {}},
                    "match_criterion": {
                        "sdp_idx": None,
                        "match_criterion_idx": None,
                        "value": {},
                    },
                }
                for added_key, added_value in running_candidate_diff[
                    "iterable_item_added"
                ].items():
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
                            "connection_group_idx": int(
                                connection_group_match.groups()[0]
                            ),
                            "value": added_value,
                        }
                    elif match_criterion_match:
                        added_items["match_criterion"] = {
                            "sdp_idx": int(match_criterion_match.groups()[0]),
                            "match_criterion_idx": int(
                                match_criterion_match.groups()[1]
                            ),
                            "value": added_value,
                        }
                new_sdp = sdps[added_items["sdp"]["sdp_idx"]]
                src_sdp_idx = new_sdp["id"]
                dst_sdp_idx = sdps[added_items["match_criterion"]["sdp_idx"]]["id"]
                connection_grp_id = connection_groups[
                    added_items["connection_group"]["connection_group_idx"]
                ]["id"]

                if (
                    connection_grp_id
                    != added_items["match_criterion"]["value"][
                        "target-connection-group-id"
                    ]
                ):
                    raise Exception(
                        "connection group missmatch in destination sdp and added connection group"
                    )
                match_criteria = new_sdp["service-match-criteria"]["match-criterion"]
                match_criterion = match_criteria[0]
            elif "iterable_item_removed" in running_candidate_diff:  # new SDP added
                operation_type = "delete"

                slice_service = running_resource_value_dict["network-slice-services"][
                    "slice-service"
                ][0]
                sdps = slice_service["sdps"]["sdp"]
                connection_groups = slice_service["connection-groups"][
                    "connection-group"
                ]
                removed_items = get_removed_items(
                    candidate_resource_value_dict, running_resource_value_dict
                )
                removed_sdp = sdps[removed_items["sdp"]["sdp_idx"]]
                src_sdp_idx = removed_sdp["id"]
                dst_sdp_idx = sdps[removed_items["match_criterion"]["sdp_idx"]]["id"]
                connection_grp_id = connection_groups[
                    removed_items["connection_group"]["connection_group_idx"]
                ]["id"]

                if (
                    connection_grp_id
                    != removed_items["match_criterion"]["value"][
                        "target-connection-group-id"
                    ]
                ):
                    raise Exception(
                        "connection group missmatch in destination sdp and added connection group"
                    )
                match_criteria = removed_sdp["service-match-criteria"][
                    "match-criterion"
                ]
                match_criterion = match_criteria[0]
            else:
                raise Exception(
                    "transition from candidate to running info not supported"
                )

            ip_info = extract_match_criterion_ipv4_info(match_criterion)

            qos_info = extract_qos_info(
                connection_groups, connection_grp_id, src_sdp_idx, dst_sdp_idx
            )

            resource_value_dict = {
                "uuid": service_name,
                "operation_type": operation_type,
                "app_flow_id": f"{src_sdp_idx}_{dst_sdp_idx}_{service_name}",
                "app_flow_user_id": str(uuid4()),
                "max_latency": int(qos_info["upstream"]["max_delay"]),
                "max_jitter": 10,
                "max_loss": float(qos_info["upstream"]["packet_loss"]),
                "upstream_assure_bw": int(qos_info["upstream"]["bw"]) * 1e6,
                "upstream_max_bw": 2 * int(qos_info["upstream"]["bw"]) * 1e6,
                "downstream_assure_bw": int(qos_info["downstream"]["bw"]) * 1e6,
                "downstream_max_bw": 2 * int(qos_info["downstream"]["bw"]) * 1e6,
                "src_ip": ip_info["src_ip"],
                "src_port": ip_info["src_port"],
                "dst_ip": ip_info["dst_ip"],
                "dst_port": ip_info["dst_port"],
            }
            json_config_rules = setup_config_rules(service_name, resource_value_dict)

            del controller.device_config.config_rules[:]
            for jcr in json_config_rules:
                controller.device_config.config_rules.append(ConfigRule(**jcr))

            self.__task_executor.configure_device(controller)
            LOGGER.debug('Configured device "{:s}"'.format(controller.name))

        except Exception as e:  # pylint: disable=broad-except
            results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('[DeleteEndpoint] service={:s}'.format(grpc_message_to_json_string(self.__service)))
        LOGGER.debug('[DeleteEndpoint] endpoints={:s}'.format(str(endpoints)))
        LOGGER.debug('[DeleteEndpoint] connection_uuid={:s}'.format(str(connection_uuid)))

        chk_type("endpoints", endpoints, list)
        if len(endpoints) == 0:
            return []
        service_uuid = self.__service.service_id.service_uuid.uuid
        results = []
        try:
            context_client = ContextClient()
            service_config = self.__service.service_config

            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[0])
            src_device_obj = self.__task_executor.get_device(DeviceId(**json_device_id(src_device_uuid)))
            controller = self.__task_executor.get_device_controller(src_device_obj)

            list_devices = context_client.ListDevices(Empty())
            devices = list_devices.devices
            device_name_map = {d.name: d for d in devices}

            running_ietf_slice_cr = get_custom_config_rule(
                service_config, RUNNING_RESOURCE_KEY
            )
            running_resource_value_dict = json.loads(
                running_ietf_slice_cr.custom.resource_value
            )

            slice_service = running_resource_value_dict["network-slice-services"][
                "slice-service"
            ][0]
            service_name = slice_service["id"]
            sdps = slice_service["sdps"]["sdp"]
            sdp_ids = [sdp["id"] for sdp in sdps]
            for sdp in sdps:
                node_id = sdp["node-id"]
                device_obj = device_name_map[node_id]
                device_controller = self.__task_executor.get_device_controller(
                    device_obj
                )
                if (
                    device_controller is None
                    or controller.name != device_controller.name
                ):
                    continue
                src_sdp_idx = sdp_ids.pop(sdp_ids.index(sdp["id"]))
                dst_sdp_idx = sdp_ids[0]
                break
            else:
                raise Exception("connection group id not found")

            resource_value_dict = {
                "app_flow_id": f"{src_sdp_idx}_{dst_sdp_idx}_{service_name}",
            }
            json_config_rules = teardown_config_rules(service_name, resource_value_dict)
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
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []
        MSG = '[SetConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(constraints)))
        return [True for _ in constraints]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConstraint(
        self, constraints: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []
        MSG = '[DeleteConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(constraints)))
        return [True for _ in constraints]

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(
        self, resources: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        MSG = '[SetConfig] Method not implemented. Resources({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(resources)))
        return [True for _ in resources]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(
        self, resources: List[Tuple[str, Any]]
    ) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []
        MSG = '[DeleteConfig] Method not implemented. Resources({:s}) are being ignored.'
        LOGGER.warning(MSG.format(str(resources)))
        return [True for _ in resources]
