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
from typing import Any, List, Optional, Tuple, TypedDict, Union

from deepdiff import DeepDiff

from common.DeviceTypes import DeviceTypeEnum
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import (
    ConfigRule,
    Device,
    DeviceId,
    Service,
    ServiceConfig,
)
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.Tools import (
    get_device_endpoint_uuids,
    get_endpoint_matching,
)
from service.service.task_scheduler.TaskExecutor import TaskExecutor

from .ConfigRules import setup_config_rules, teardown_config_rules

RUNNING_RESOURCE_KEY = "running_ietf_slice"
CANDIDATE_RESOURCE_KEY = "candidate_ietf_slice"
MTU = 1500

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool("Service", "Handler", labels={"handler": "l3nm_ietf_l3vpn"})


class LANPrefixesDict(TypedDict):
    lan: str
    lan_tag: str


class Ipv4Info(TypedDict):
    src_lan: str
    dst_lan: str
    src_port: str
    dst_port: str
    vlan: str


class QoSInfo(TypedDict):
    src_qos_profile_latency: int
    src_input_bw: int
    src_output_bw: int
    dst_qos_profile_latency: int
    dst_input_bw: int
    dst_output_bw: int


def get_custom_config_rule(
    service_config: ServiceConfig, resource_key: str
) -> Optional[ConfigRule]:
    """
    Return the custom ConfigRule from the ServiceConfig matching the given resource_key,
    or None if not found.
    """
    for cr in service_config.config_rules:
        if (
            cr.WhichOneof("config_rule") == "custom"
            and cr.custom.resource_key == resource_key
        ):
            return cr
    return None


def load_json_rule_data(service_config: ServiceConfig) -> Tuple[dict, dict]:
    """
    Loads the running/candidate JSON data from the service_config for IETF slice data.
    Raises an exception if either is missing.
    """
    running_cr = get_custom_config_rule(service_config, RUNNING_RESOURCE_KEY)
    candidate_cr = get_custom_config_rule(service_config, CANDIDATE_RESOURCE_KEY)

    if not running_cr or not candidate_cr:
        raise ValueError("Missing running/candidate IETF slice config rules.")

    running_data = json.loads(running_cr.custom.resource_value)
    candidate_data = json.loads(candidate_cr.custom.resource_value)
    return running_data, candidate_data


def extract_match_criterion_ipv4_info(match_criterion: dict) -> Ipv4Info:
    """
    Extracts IPv4 match criteria data (src/dst IP, ports, VLAN) from a match_criterion dict.
    """
    src_lan = dst_lan = src_port = dst_port = vlan = ""
    for type_value in match_criterion["match-type"]:
        value = type_value["value"][0]
        if type_value["type"] == "ietf-network-slice-service:source-ip-prefix":
            src_lan = value
        elif type_value["type"] == "ietf-network-slice-service:destination-ip-prefix":
            dst_lan = value
        elif type_value["type"] == "ietf-network-slice-service:source-tcp-port":
            src_port = value
        elif type_value["type"] == "ietf-network-slice-service:destination-tcp-port":
            dst_port = value
        elif type_value["type"] == "ietf-network-slice-service:vlan":
            vlan = value

    return Ipv4Info(
        src_lan=src_lan,
        dst_lan=dst_lan,
        src_port=src_port,
        dst_port=dst_port,
        vlan=vlan,
    )


def extract_qos_info_from_connection_group(
    src_sdp_id: str, dst_sdp_id: str, connectivity_constructs: list
) -> QoSInfo:
    """
    Given a pair of SDP ids and a list of connectivity constructs, extract QoS info
    such as latency and bandwidth (for both directions).
    """

    def _extract_qos_fields(cc: dict) -> Tuple[int, int]:
        max_delay = 0
        bandwidth = 0
        metric_bounds = cc["service-slo-sle-policy"]["slo-policy"]["metric-bound"]
        for metric_bound in metric_bounds:
            if (
                metric_bound["metric-type"]
                == "ietf-network-slice-service:one-way-delay-maximum"
                and metric_bound["metric-unit"] == "milliseconds"
            ):
                max_delay = int(metric_bound["bound"])
            elif (
                metric_bound["metric-type"]
                == "ietf-network-slice-service:one-way-bandwidth"
                and metric_bound["metric-unit"] == "Mbps"
            ):
                # Convert from Mbps to bps
                bandwidth = int(metric_bound["bound"]) * 1000000
        return max_delay, bandwidth

    src_cc = next(
        cc
        for cc in connectivity_constructs
        if cc["p2p-sender-sdp"] == src_sdp_id and cc["p2p-receiver-sdp"] == dst_sdp_id
    )
    dst_cc = next(
        cc
        for cc in connectivity_constructs
        if cc["p2p-sender-sdp"] == dst_sdp_id and cc["p2p-receiver-sdp"] == src_sdp_id
    )
    src_max_delay, src_bandwidth = _extract_qos_fields(src_cc)
    dst_max_delay, dst_bandwidth = _extract_qos_fields(dst_cc)

    return QoSInfo(
        src_qos_profile_latency=src_max_delay,
        src_input_bw=src_bandwidth,
        src_output_bw=dst_bandwidth,
        dst_qos_profile_latency=dst_max_delay,
        dst_input_bw=dst_bandwidth,
        dst_output_bw=src_bandwidth,
    )


def get_endpoint_settings(device_obj: Device, endpoint_name: str) -> dict:
    """
    Helper to retrieve endpoint settings from a device's config rules given an endpoint name.
    Raises an exception if not found.
    """
    for rule in device_obj.device_config.config_rules:
        if (
            rule.WhichOneof("config_rule") == "custom"
            and rule.custom.resource_key == f"/endpoints/endpoint[{endpoint_name}]"
        ):
            return json.loads(rule.custom.resource_value)
    raise ValueError(f"Endpoint settings not found for endpoint {endpoint_name}")


PACKET_SDN_CONTROLLERS = {
    DeviceTypeEnum.IP_SDN_CONTROLLER.value,
    DeviceTypeEnum.EMULATED_IP_SDN_CONTROLLER.value,
    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER.value,
}

class L3NM_IETFL3VPN_ServiceHandler(_ServiceHandler):
    def __init__(  # pylint: disable=super-init-not-called
        self, service: Service, task_executor: TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor

    def __find_IP_transport_edge_endpoints(
        self, endpoints
    ) -> Tuple[str, str, str, str, Device]:
        """
        Searches for two endpoints whose device controllers are IP_SDN_CONTROLLER.
        Returns (src_device_uuid, src_endpoint_uuid, dst_device_uuid, dst_endpoint_uuid, controller_device).
        Raises an exception if not found or if the two IP devices differ.
        """

        # Find the first IP transport edge endpoint from the head of endpoints
        for ep in endpoints:
            device_uuid, endpoint_uuid = get_device_endpoint_uuids(ep)
            device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(device_uuid))
            )
            device_controller = self.__task_executor.get_device_controller(device_obj)
            if device_controller.device_type in PACKET_SDN_CONTROLLERS:
                src_device_uuid, src_endpoint_uuid = device_uuid, endpoint_uuid
                src_device_controller = device_controller
                break
        else:
            raise Exception("No IP transport edge endpoints found")

        # Find the second IP transport edge endpoint from the tail of endpoints
        for ep in reversed(endpoints):
            device_uuid, endpoint_uuid = get_device_endpoint_uuids(ep)
            device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(device_uuid))
            )
            device_controller = self.__task_executor.get_device_controller(device_obj)
            if device_controller.device_type in PACKET_SDN_CONTROLLERS:
                dst_device_uuid, dst_endpoint_uuid = device_uuid, endpoint_uuid
                dst_device_controller = device_controller
                break
        else:
            raise Exception("No IP transport edge endpoints found")

        if src_device_controller != dst_device_controller:
            raise Exception("Different Src-Dst devices not supported by now")

        return (
            src_device_uuid,
            src_endpoint_uuid,
            dst_device_uuid,
            dst_endpoint_uuid,
            src_device_controller,
        )

    def __build_resource_value_dict(
        self,
        service_id: str,
        src_device_obj: Device,
        dst_device_obj: Device,
        src_endpoint_name: str,
        dst_endpoint_name: str,
        qos_info: QoSInfo,
        src_endpoint_settings: dict,
        dst_endpoint_settings: dict,
        src_match_criterion_ipv4_info: Ipv4Info,
        dst_match_criterion_ipv4_info: Ipv4Info,
    ) -> dict:
        """
        Builds the final resource-value dict to be used when calling setup_config_rules().
        """
        # Prepare data for source
        src_device_name = src_device_obj.name
        src_ce_ip = src_endpoint_settings["address_ip"]
        src_ce_prefix = src_endpoint_settings["address_prefix"]
        src_lan_prefixes = [
            LANPrefixesDict(
                lan=src_match_criterion_ipv4_info["dst_lan"],
                lan_tag=src_match_criterion_ipv4_info["vlan"],
            )
        ]

        # Prepare data for destination
        dst_device_name = dst_device_obj.name
        dst_ce_ip = dst_endpoint_settings["address_ip"]
        dst_ce_prefix = dst_endpoint_settings["address_prefix"]
        dst_lan_prefixes = [
            LANPrefixesDict(
                lan=dst_match_criterion_ipv4_info["dst_lan"],
                lan_tag=dst_match_criterion_ipv4_info["vlan"],
            )
        ]

        return {
            "uuid": service_id,
            "src_device_name": src_device_name,
            "src_endpoint_name": src_endpoint_name,
            "src_site_location": src_endpoint_settings["site_location"],
            "src_ipv4_lan_prefixes": src_lan_prefixes,
            "src_ce_address": src_ce_ip,
            "src_pe_address": src_ce_ip,
            "src_ce_pe_network_prefix": src_ce_prefix,
            "src_mtu": MTU,
            "src_qos_profile_latency": qos_info["src_qos_profile_latency"],
            "src_input_bw": qos_info["src_input_bw"],
            "src_output_bw": qos_info["src_output_bw"],
            "dst_device_name": dst_device_name,
            "dst_endpoint_name": dst_endpoint_name,
            "dst_site_location": dst_endpoint_settings["site_location"],
            "dst_ipv4_lan_prefixes": dst_lan_prefixes,
            "dst_ce_address": dst_ce_ip,
            "dst_pe_address": dst_ce_ip,
            "dst_ce_pe_network_prefix": dst_ce_prefix,
            "dst_mtu": MTU,
            "dst_qos_profile_latency": qos_info["dst_qos_profile_latency"],
            "dst_input_bw": qos_info["dst_input_bw"],
            "dst_output_bw": qos_info["dst_output_bw"],
        }

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        LOGGER.debug('[SetEndpoint] service={:s}'.format(grpc_message_to_json_string(self.__service)))
        LOGGER.debug('[SetEndpoint] endpoints={:s}'.format(str(endpoints)))
        LOGGER.debug('[SetEndpoint] connection_uuid={:s}'.format(str(connection_uuid)))

        chk_type("endpoints", endpoints, list)
        if len(endpoints) < 2:
            return []

        results = []
        service_config = self.__service.service_config

        try:
            # Identify IP transport edge endpoints
            (
                src_device_uuid,
                src_endpoint_uuid,
                dst_device_uuid,
                dst_endpoint_uuid,
                controller,
            ) = self.__find_IP_transport_edge_endpoints(endpoints)

            # Retrieve device objects
            src_device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(src_device_uuid))
            )
            src_endpoint_obj = get_endpoint_matching(src_device_obj, src_endpoint_uuid)

            dst_device_obj = self.__task_executor.get_device(
                DeviceId(**json_device_id(dst_device_uuid))
            )
            dst_endpoint_obj = get_endpoint_matching(dst_device_obj, dst_endpoint_uuid)

            # Obtain endpoint settings
            src_endpoint_settings = get_endpoint_settings(
                src_device_obj, src_endpoint_obj.name
            )
            dst_endpoint_settings = get_endpoint_settings(
                dst_device_obj, dst_endpoint_obj.name
            )

            # Load running & candidate data, compute diff
            running_data, candidate_data = load_json_rule_data(service_config)
            running_candidate_diff = DeepDiff(running_data, candidate_data)

            # Determine service_id and operation_type
            slice_service = candidate_data["network-slice-services"]["slice-service"][0]
            service_id = slice_service["id"]
            if not running_candidate_diff:
                operation_type = "create"
            elif "values_changed" in running_candidate_diff:
                operation_type = "update"

            # Parse relevant connectivity data
            sdps = slice_service["sdps"]["sdp"]
            connection_group = slice_service["connection-groups"]["connection-group"][0]
            connecitivity_constructs = connection_group["connectivity-construct"]

            # The code below assumes a single connectivity construct or
            # that the relevant one is the first in the list:
            connecitivity_construct = connecitivity_constructs[0]
            src_sdp_idx = connecitivity_construct["p2p-sender-sdp"]
            dst_sdp_idx = connecitivity_construct["p2p-receiver-sdp"]

            # QoS
            qos_info = extract_qos_info_from_connection_group(
                src_sdp_idx, dst_sdp_idx, connecitivity_constructs
            )

            # Retrieve match-criterion info
            src_sdp = next(sdp for sdp in sdps if sdp["id"] == src_sdp_idx)
            dst_sdp = next(sdp for sdp in sdps if sdp["id"] == dst_sdp_idx)

            src_match_criterion = src_sdp["service-match-criteria"]["match-criterion"][
                0
            ]
            dst_match_criterion = dst_sdp["service-match-criteria"]["match-criterion"][
                0
            ]
            src_match_criterion_ipv4_info = extract_match_criterion_ipv4_info(
                src_match_criterion
            )
            dst_match_criterion_ipv4_info = extract_match_criterion_ipv4_info(
                dst_match_criterion
            )

            # Build resource dict & config rules
            resource_value_dict = self.__build_resource_value_dict(
                service_id=service_id,
                src_device_obj=src_device_obj,
                dst_device_obj=dst_device_obj,
                src_endpoint_name=src_endpoint_obj.name,
                dst_endpoint_name=dst_endpoint_obj.name,
                qos_info=qos_info,
                src_endpoint_settings=src_endpoint_settings,
                dst_endpoint_settings=dst_endpoint_settings,
                src_match_criterion_ipv4_info=src_match_criterion_ipv4_info,
                dst_match_criterion_ipv4_info=dst_match_criterion_ipv4_info,
            )
            json_config_rules = setup_config_rules(
                service_id, resource_value_dict, operation_type
            )

            # Configure device
            del controller.device_config.config_rules[:]
            for jcr in json_config_rules:
                controller.device_config.config_rules.append(ConfigRule(**jcr))
            self.__task_executor.configure_device(controller)
        except Exception as e:  # pylint: disable=broad-except
            str_service_id = grpc_message_to_json_string(self.__service.service_id)
            LOGGER.exception(
                "Unable to SetEndpoint for Service({:s})".format(str(str_service_id))
            )
            results.append(e)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self,
        endpoints: List[Tuple[str, str, Optional[str]]],
        connection_uuid: Optional[str] = None,
    ) -> List[Union[bool, Exception]]:
        chk_type("endpoints", endpoints, list)
        if len(endpoints) < 2:
            return []
        service_config = self.__service.service_config
        ietf_slice_candidate_cr = get_custom_config_rule(
            service_config, CANDIDATE_RESOURCE_KEY
        )
        candidate_resource_value_dict = json.loads(
            ietf_slice_candidate_cr.custom.resource_value
        )
        service_id = candidate_resource_value_dict["network-slice-services"][
            "slice-service"
        ][0]["id"]
        results = []
        try:
            src_device_uuid, _ = get_device_endpoint_uuids(endpoints[0])
            src_device = self.__task_executor.get_device(
                DeviceId(**json_device_id(src_device_uuid))
            )
            src_controller = self.__task_executor.get_device_controller(src_device)

            dst_device_uuid, _ = get_device_endpoint_uuids(endpoints[1])
            dst_device = self.__task_executor.get_device(
                DeviceId(**json_device_id(dst_device_uuid))
            )
            dst_controller = self.__task_executor.get_device_controller(dst_device)
            if (
                src_controller.device_id.device_uuid.uuid
                != dst_controller.device_id.device_uuid.uuid
            ):
                raise Exception("Different Src-Dst devices not supported by now")
            controller = src_controller
            json_config_rules = teardown_config_rules(service_id)
            del controller.device_config.config_rules[:]
            for jcr in json_config_rules:
                controller.device_config.config_rules.append(ConfigRule(**jcr))
            self.__task_executor.configure_device(controller)
            results.append(True)
        except Exception as e:  # pylint: disable=broad-except
            LOGGER.exception(
                "Unable to DeleteEndpoint for Service({:s})".format(str(service_id))
            )
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
