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
import uuid
from typing import Dict, List, Optional

from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import (
    ConfigRule,
    Constraint,
    DeviceId,
    Device,
    Empty,
    EndPointId,
    ServiceConfig,
    Slice,
    SliceStatusEnum,
)
from common.tools.context_queries.Slice import get_slice_by_defualt_name
from common.tools.grpc.ConfigRules import update_config_rule_custom
from common.tools.object_factory.Device import json_device_id
from common.DeviceTypes import DeviceTypeEnum
from context.client import ContextClient

from .YangValidator import YangValidator

LOGGER = logging.getLogger(__name__)


RUNNING_RESOURCE_KEY = "running_ietf_slice"
CANDIDATE_RESOURCE_KEY = "candidate_ietf_slice"
ADDRESS_PREFIX = 24
RAISE_IF_DIFFERS = False


def validate_ietf_slice_data(request_data: Dict) -> None:
    """
    Validate the provided IETF slice data against the YANG model.
    """
    yang_validator = YangValidator("ietf-network-slice-service")
    _ = yang_validator.parse_to_dict(request_data)
    yang_validator.destroy()


def get_custom_config_rule(
    service_config: ServiceConfig, resource_key: str
) -> Optional[ConfigRule]:
    """
    Retrieve the custom config rule with the given resource_key from a ServiceConfig.
    """
    for cr in service_config.config_rules:
        if (
            cr.WhichOneof("config_rule") == "custom"
            and cr.custom.resource_key == resource_key
        ):
            return cr
    return None


def get_ietf_data_from_config(slice_request: Slice, resource_key: str) -> Dict:
    """
    Retrieve the IETF data (as a Python dict) from a slice's config rule for the specified resource_key.
    Raises an exception if not found.
    """
    config_rule = get_custom_config_rule(slice_request.slice_config, resource_key)
    if not config_rule:
        raise Exception(f"IETF data not found for resource_key: {resource_key}")
    return json.loads(config_rule.custom.resource_value)


def update_ietf_data_in_config(
    slice_request: Slice, resource_key: str, ietf_data: Dict
) -> None:
    """
    Update the slice config rule (identified by resource_key) with the provided IETF data.
    """
    fields = {name: (value, RAISE_IF_DIFFERS) for name, value in ietf_data.items()}
    update_config_rule_custom(
        slice_request.slice_config.config_rules, resource_key, fields
    )


def build_constraints_from_connection_group(connection_group: dict) -> List[Constraint]:
    """
    Build a list of Constraints from the 'metric-bound' data in a connection group.
    """
    constraints = []
    metric_bounds = connection_group["connectivity-construct"][0][
        "service-slo-sle-policy"
    ]["slo-policy"]["metric-bound"]

    for metric in metric_bounds:
        metric_type = str(metric['metric-type'])
        metric_type = metric_type.replace('ietf-network-slice-service:', 'ietf-nss:')

        if metric_type == 'ietf-nss:one-way-delay-maximum':
            value = float(metric['bound'])
            unit  = str(metric['metric-unit'])

            if unit == 'nanoseconds':
                factor = 1.0e6
            elif unit == 'microseconds':
                factor = 1.0e3
            elif unit == 'milliseconds':
                factor = 1.0
            else:
                MSG = 'Unsupported unit({:s}) for metric({:s})'
                raise Exception(MSG.format(unit, metric_type))

            constraint = Constraint()
            constraint.sla_latency.e2e_latency_ms = value / factor
            constraints.append(constraint)

        elif metric_type == 'ietf-nss:one-way-bandwidth':
            value = float(metric['bound'])
            unit  = str(metric['metric-unit'])

            if unit == 'bps':
                factor = 1.0e9
            elif unit == 'Kbps':
                factor = 1.0e6
            elif unit == 'Mbps':
                factor = 1.0e3
            elif unit == 'Gbps':
                factor = 1.0
            else:
                MSG = 'Unsupported unit({:s}) for metric({:s})'
                raise Exception(MSG.format(unit, metric_type))

            constraint = Constraint()
            constraint.sla_capacity.capacity_gbps = value / factor
            constraints.append(constraint)

        elif metric_type == "ietf-nss:two-way-packet-loss":
            value = float(metric["percentile-value"])
            unit  = str(metric['metric-unit'])

            if unit != 'percentage':
                MSG = 'Unsupported unit({:s}) for metric({:s})'
                raise Exception(MSG.format(unit, metric_type))

            constraint = Constraint()
            constraint.sla_availability.num_disjoint_paths = 1
            constraint.sla_availability.all_active = True
            constraint.sla_availability.availability = 100.0 - value
            constraints.append(constraint)

        else:
            MSG = 'Unsupported metric({:s})'
            raise Exception(MSG.format(str(metric)))

    return constraints


def get_endpoint_controller_type(
    endpoint: EndPointId, context_client: ContextClient
) -> str:
    """
    Retrieve the device type of an endpoint's controller device, if any; otherwise returns an empty string.
    """
    endpoint_device: Device = context_client.GetDevice(endpoint.device_id)
    if endpoint_device.controller_id == DeviceId():
        return ""
    controller = context_client.GetDevice(endpoint_device.controller_id)
    if controller is None:
        controller_uuid = endpoint_device.controller_id.device_uuid.uuid
        raise Exception(f"Controller device {controller_uuid} not found")
    return controller.device_type


def sort_endpoints(
    endpoints_list: List[EndPointId],
    sdps: List,
    connection_group: Dict,
    context_client: ContextClient,
) -> List[EndPointId]:
    """
    Sort the endpoints_list based on controller type:
      - If the first endpoint is an NCE, keep order.
      - If the last endpoint is an NCE, reverse order.
      - Otherwise, use the 'p2p-sender-sdp' from the connection group to decide.
    """
    if not endpoints_list:
        return endpoints_list

    first_ep = endpoints_list[0]
    last_ep = endpoints_list[-1]
    first_controller_type = get_endpoint_controller_type(first_ep, context_client)
    last_controller_type = get_endpoint_controller_type(last_ep, context_client)

    if first_controller_type == DeviceTypeEnum.NCE.value:
        return endpoints_list
    elif last_controller_type == DeviceTypeEnum.NCE.value:
        return endpoints_list[::-1]

    src_sdp_id = connection_group["connectivity-construct"][0]["p2p-sender-sdp"]
    sdp_id_name_mapping = {sdp["id"]: sdp["node-id"] for sdp in sdps}
    if endpoints_list[0].device_id.device_uuid.uuid == sdp_id_name_mapping[src_sdp_id]:
        return endpoints_list
    return endpoints_list[::-1]


def replace_ont_endpoint_with_emu_dc(
    endpoint_list: List[EndPointId], context_client: ContextClient
) -> List[EndPointId]:
    """
    Replace an ONT endpoint in endpoint_list with an 'emu-datacenter' endpoint if found.
    One endpoint must be managed (controller_id != empty), the other must be unmanaged.
    """
    if len(endpoint_list) != 2:
        raise Exception(
            "Expecting exactly two endpoints to handle ONT -> emu-dc replacement"
        )

    link_list = context_client.ListLinks(Empty())
    links = list(link_list.links)
    devices_list = context_client.ListDevices(Empty())
    devices = devices_list.devices

    uuid_name_map = {d.device_id.device_uuid.uuid: d.name for d in devices}
    uuid_device_map = {d.device_id.device_uuid.uuid: d for d in devices}
    name_device_map = {d.name: d for d in devices}

    endpoint_id_1, endpoint_id_2 = endpoint_list
    device_uuid_1 = endpoint_id_1.device_id.device_uuid.uuid
    device_uuid_2 = endpoint_id_2.device_id.device_uuid.uuid

    device_1 = name_device_map.get(device_uuid_1)
    device_2 = name_device_map.get(device_uuid_2)

    if not device_1 or not device_2:
        raise Exception("One or both devices not found in name_device_map")

    # Check if the first endpoint is managed
    if device_1.controller_id != DeviceId():
        for link in links:
            link_endpoints = list(link.link_endpoint_ids)
            link_ep_1, link_ep_2 = link_endpoints
            if (
                device_uuid_1 == uuid_name_map.get(link_ep_1.device_id.device_uuid.uuid)
                and uuid_device_map[link_ep_2.device_id.device_uuid.uuid].device_type
                == "emu-datacenter"
            ):
                endpoint_list[0] = link_ep_2
                break
    # Otherwise, check if the second endpoint is managed
    elif device_2.controller_id != DeviceId():
        for link in links:
            link_endpoints = list(link.link_endpoint_ids)
            link_ep_1, link_ep_2 = link_endpoints
            if (
                device_uuid_2 == uuid_name_map.get(link_ep_1.device_id.device_uuid.uuid)
                and uuid_device_map[link_ep_2.device_id.device_uuid.uuid].device_type
                == "emu-datacenter"
            ):
                endpoint_list[1] = link_ep_2
                break
    else:
        raise Exception(
            "One endpoint should be managed by a controller and the other should not be"
        )

    return endpoint_list


class IETFSliceHandler:
    @staticmethod
    def get_all_ietf_slices(context_client: ContextClient) -> Dict:
        """
        Retrieve all IETF slices from the (single) context. Expects exactly one context in the system.
        """
        existing_context_ids = context_client.ListContextIds(Empty())
        context_ids = list(existing_context_ids.context_ids)
        if len(context_ids) != 1:
            raise Exception("Number of contexts should be exactly 1")

        slices_list = context_client.ListSlices(context_ids[0])
        slices = slices_list.slices

        ietf_slices = {"network-slice-services": {"slice-service": []}}
        for slc in slices:
            candidate_cr = get_custom_config_rule(
                slc.slice_config, CANDIDATE_RESOURCE_KEY
            )
            if not candidate_cr:
                # Skip slices that don't have the candidate_ietf_slice data
                continue
            candidate_ietf_data = json.loads(candidate_cr.custom.resource_value)
            ietf_slices["network-slice-services"]["slice-service"].append(
                candidate_ietf_data["network-slice-services"]["slice-service"][0]
            )
        return ietf_slices

    @staticmethod
    def create_slice_service(
        request_data: dict, context_client: ContextClient
    ) -> Slice:
        """
        Create a new slice service from the provided IETF data, applying validations and constructing a Slice object.
        """
        # Ensure the top-level key is "network-slice-services"
        if "network-slice-services" not in request_data:
            request_data = {"network-slice-services": request_data}

        validate_ietf_slice_data(request_data)
        slice_service = request_data["network-slice-services"]["slice-service"][0]

        slice_id = slice_service["id"]
        sdps = slice_service["sdps"]["sdp"]
        if len(sdps) != 2:
            raise Exception("Number of SDPs should be exactly 2")

        connection_groups = slice_service["connection-groups"]["connection-group"]
        slice_request = Slice()
        slice_request.slice_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
        slice_request.slice_id.slice_uuid.uuid = slice_id
        slice_request.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_PLANNED

        list_endpoints = []
        endpoint_config_rules = []
        connection_group_ids = set()

        # Build endpoints from SDPs
        for sdp in sdps:
            attachment_circuits = sdp["attachment-circuits"]["attachment-circuit"]
            if len(attachment_circuits) != 1:
                raise Exception("Each SDP must have exactly 1 attachment-circuit")

            endpoint = EndPointId()
            endpoint.topology_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
            device_uuid = sdp["node-id"]
            endpoint.device_id.device_uuid.uuid = device_uuid
            endpoint_uuid = attachment_circuits[0]["ac-tp-id"]
            endpoint.endpoint_uuid.uuid = endpoint_uuid
            list_endpoints.append(endpoint)

            match_criteria = sdp["service-match-criteria"]["match-criterion"]
            if len(match_criteria) != 1:
                raise Exception('Each SDP must have exactly 1 service-match-criteria/match-criterion')
            match_criterion = match_criteria[0]

            # Keep track of connection-group-id from each SDP
            connection_group_ids.add(
                match_criterion['target-connection-group-id']
            )

            sdp_ip_addresses = sdp['sdp-ip-address']
            if len(sdp_ip_addresses) != 1:
                raise Exception('Each SDP must have exactly 1 sdp-ip-address')
            sdp_ip_address = sdp_ip_addresses[0]

            vlan_tag = None
            match_type = match_criterion['match-type']
            for match_type_item in match_type:
                item_type = match_type_item['type']
                if item_type != 'ietf-network-slice-service:vlan': continue
                vlan_tag = int(match_type_item['value'][0])
                break

            update_config_rule_custom(
                slice_request.slice_config.config_rules,
                '/settings',
                {
                    'address_families': (['IPV4'], True),
                    'mtu'             : (1500, True),
                }
            )

            static_routing_table = {
                #'{:d}-{:s}/{:d}'.format(lan_tag, ip_range, ip_prefix_len): (
                #    {
                #        'vlan-id': lan_tag,
                #        'ip-network': '{:s}/{:d}'.format(ip_range, ip_prefix_len),
                #        'next-hop': next_hop
                #    },
                #    True
                #)
                #for (ip_range, ip_prefix_len, lan_tag), next_hop in static_routing.items()
            }
            update_config_rule_custom(
                slice_request.slice_config.config_rules,
                '/static_routing', static_routing_table
            )

            # Endpoint-specific config rule fields
            endpoint_config_rule_fields = {
                'address_ip': (sdp_ip_address, RAISE_IF_DIFFERS),
                'address_prefix': (ADDRESS_PREFIX, RAISE_IF_DIFFERS),
            }
            if vlan_tag is not None:
                endpoint_config_rule_fields['vlan_tag'] = (vlan_tag, RAISE_IF_DIFFERS)
            endpoint_config_rules.append(
                (
                    f"/device[{device_uuid}]/endpoint[{endpoint_uuid}]/settings",
                    endpoint_config_rule_fields,
                )
            )

        if len(connection_group_ids) != 1:
            raise Exception("SDPs do not share a common connection-group-id")

        # Build constraints from the matching connection group
        unique_cg_id = connection_group_ids.pop()
        found_cg = next(
            (cg for cg in connection_groups if cg["id"] == unique_cg_id), None
        )
        if not found_cg:
            raise Exception("The connection group referenced by the SDPs was not found")

        list_constraints = build_constraints_from_connection_group(found_cg)

        # Sort endpoints and optionally replace the ONT endpoint
        list_endpoints = sort_endpoints(list_endpoints, sdps, found_cg, context_client)
        
        # NOTE: not sure why this is needed
        #list_endpoints = replace_ont_endpoint_with_emu_dc(
        #    list_endpoints, context_client
        #)

        slice_request.slice_endpoint_ids.extend(list_endpoints)
        slice_request.slice_constraints.extend(list_constraints)

        # Set slice owner
        slice_request.slice_owner.owner_string = slice_id
        slice_request.slice_owner.owner_uuid.uuid = str(
            uuid.uuid5(uuid.NAMESPACE_DNS, slice_id)
        )

        # Update slice config with IETF data (both running and candidate)
        ietf_slice_fields = {
            name: (value, RAISE_IF_DIFFERS) for name, value in request_data.items()
        }
        update_config_rule_custom(
            slice_request.slice_config.config_rules,
            RUNNING_RESOURCE_KEY,
            ietf_slice_fields,
        )
        update_config_rule_custom(
            slice_request.slice_config.config_rules,
            CANDIDATE_RESOURCE_KEY,
            ietf_slice_fields,
        )

        # Update endpoint config rules
        for ep_cr_key, ep_cr_fields in endpoint_config_rules:
            update_config_rule_custom(
                slice_request.slice_config.config_rules, ep_cr_key, ep_cr_fields
            )

        return slice_request

    @staticmethod
    def create_sdp(
        request_data: dict, slice_uuid: str, context_client: ContextClient
    ) -> Slice:
        """
        Add a new SDP to an existing slice, updating the candidate IETF data.
        """
        sdps = request_data["sdp"]
        if len(sdps) != 1:
            raise Exception("Number of SDPs to create must be exactly 1")

        new_sdp = sdps[0]
        slice_request = get_slice_by_defualt_name(
            context_client, slice_uuid, rw_copy=False
        )
        ietf_data = get_ietf_data_from_config(slice_request, CANDIDATE_RESOURCE_KEY)

        slice_service = ietf_data["network-slice-services"]["slice-service"][0]
        slice_sdps = slice_service["sdps"]["sdp"]
        slice_sdps.append(new_sdp)

        # Save updated IETF data
        update_ietf_data_in_config(slice_request, CANDIDATE_RESOURCE_KEY, ietf_data)
        return slice_request

    @staticmethod
    def delete_sdp(
        slice_uuid: str, sdp_id: str, context_client: ContextClient
    ) -> Slice:
        """
        Delete the specified SDP from an existing slice's candidate IETF data.
        """
        slice_request = get_slice_by_defualt_name(
            context_client, slice_uuid, rw_copy=False
        )
        ietf_data = get_ietf_data_from_config(slice_request, CANDIDATE_RESOURCE_KEY)

        slice_service = ietf_data["network-slice-services"]["slice-service"][0]
        slice_sdps = slice_service["sdps"]["sdp"]

        # Find and remove the matching SDP
        sdp_idx = next(
            (i for i, sdp in enumerate(slice_sdps) if sdp["id"] == sdp_id), None
        )
        if sdp_idx is None:
            raise Exception(f"SDP with id '{sdp_id}' not found in slice '{slice_uuid}'")
        slice_sdps.pop(sdp_idx)

        update_ietf_data_in_config(slice_request, CANDIDATE_RESOURCE_KEY, ietf_data)
        return slice_request

    @staticmethod
    def create_connection_group(
        request_data: dict, slice_id: str, context_client: ContextClient
    ) -> Slice:
        """
        Add a new connection group to an existing slice's candidate IETF data.
        """
        connection_groups = request_data["connection-group"]
        if len(connection_groups) != 1:
            raise Exception("Number of connection groups to create must be exactly 1")

        new_connection_group = connection_groups[0]
        slice_request = get_slice_by_defualt_name(
            context_client, slice_id, rw_copy=False
        )
        ietf_data = get_ietf_data_from_config(slice_request, CANDIDATE_RESOURCE_KEY)

        slice_service = ietf_data["network-slice-services"]["slice-service"][0]
        slice_connection_groups = slice_service["connection-groups"]["connection-group"]
        slice_connection_groups.append(new_connection_group)

        # Validate the updated data, then save
        validate_ietf_slice_data(ietf_data)
        update_ietf_data_in_config(slice_request, CANDIDATE_RESOURCE_KEY, ietf_data)
        return slice_request

    @staticmethod
    def update_connection_group(
        slice_name: str,
        updated_connection_group: dict,
        context_client: ContextClient,
    ) -> Slice:
        """
        Update an existing connection group in the candidate IETF data.
        """
        slice_request = get_slice_by_defualt_name(
            context_client, slice_name, rw_copy=False
        )
        candidate_ietf_data = get_ietf_data_from_config(
            slice_request, CANDIDATE_RESOURCE_KEY
        )

        slice_service = candidate_ietf_data["network-slice-services"]["slice-service"][
            0
        ]
        slice_connection_groups = slice_service["connection-groups"]["connection-group"]

        cg_id = updated_connection_group["id"]
        cg_idx = next(
            (i for i, cg in enumerate(slice_connection_groups) if cg["id"] == cg_id),
            None,
        )
        if cg_idx is None:
            raise Exception(f"Connection group with id '{cg_id}' not found")

        slice_connection_groups[cg_idx] = updated_connection_group
        update_ietf_data_in_config(
            slice_request, CANDIDATE_RESOURCE_KEY, candidate_ietf_data
        )

        slice_request.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_PLANNED
        return slice_request

    @staticmethod
    def delete_connection_group(
        slice_uuid: str, connection_group_id: str, context_client: ContextClient
    ) -> Slice:
        """
        Remove an existing connection group from the candidate IETF data of a slice.
        """
        slice_request = get_slice_by_defualt_name(
            context_client, slice_uuid, rw_copy=False
        )
        candidate_ietf_data = get_ietf_data_from_config(
            slice_request, CANDIDATE_RESOURCE_KEY
        )

        slice_service = candidate_ietf_data["network-slice-services"]["slice-service"][
            0
        ]
        slice_connection_groups = slice_service["connection-groups"]["connection-group"]

        cg_idx = next(
            (
                i
                for i, cg in enumerate(slice_connection_groups)
                if cg["id"] == connection_group_id
            ),
            None,
        )
        if cg_idx is None:
            raise Exception(
                f"Connection group with id '{connection_group_id}' not found"
            )

        slice_connection_groups.pop(cg_idx)
        update_ietf_data_in_config(
            slice_request, CANDIDATE_RESOURCE_KEY, candidate_ietf_data
        )

        slice_request.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_PLANNED
        return slice_request

    @staticmethod
    def create_match_criteria(
        request_data: dict, slice_name: str, sdp_id: str, context_client: ContextClient
    ) -> Slice:
        """
        Create a new match-criterion for the specified SDP in a slice's candidate IETF data.
        """
        match_criteria = request_data["match-criterion"]
        if len(match_criteria) != 1:
            raise Exception(
                "Number of match-criterion entries to create must be exactly 1"
            )

        new_match_criterion = match_criteria[0]
        target_connection_group_id = new_match_criterion["target-connection-group-id"]

        slice_request = get_slice_by_defualt_name(
            context_client, slice_name, rw_copy=False
        )
        ietf_data = get_ietf_data_from_config(slice_request, CANDIDATE_RESOURCE_KEY)

        slice_service = ietf_data["network-slice-services"]["slice-service"][0]
        connection_groups = slice_service["connection-groups"]["connection-group"]
        sdps = slice_service["sdps"]["sdp"]

        # Find the referenced connection group
        found_cg = next(
            (cg for cg in connection_groups if cg["id"] == target_connection_group_id),
            None,
        )
        if not found_cg:
            raise Exception(
                f"Connection group '{target_connection_group_id}' not found"
            )

        # Build constraints from that connection group
        list_constraints = build_constraints_from_connection_group(found_cg)

        # Add match-criterion to the relevant SDP
        sdp_to_update = next((s for s in sdps if s["id"] == sdp_id), None)
        if not sdp_to_update:
            raise Exception(f"SDP '{sdp_id}' not found")

        sdp_to_update["service-match-criteria"]["match-criterion"].append(
            new_match_criterion
        )

        # Update constraints at the slice level as needed
        del slice_request.slice_constraints[:]
        slice_request.slice_constraints.extend(list_constraints)
        slice_request.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_PLANNED

        update_ietf_data_in_config(slice_request, CANDIDATE_RESOURCE_KEY, ietf_data)
        return slice_request

    @staticmethod
    def delete_match_criteria(
        slice_uuid: str,
        sdp_id: str,
        match_criterion_id: int,
        context_client: ContextClient,
    ) -> Slice:
        """
        Delete the specified match-criterion from an SDP in the slice's candidate IETF data.
        """
        slice_request = get_slice_by_defualt_name(
            context_client, slice_uuid, rw_copy=False
        )
        ietf_data = get_ietf_data_from_config(slice_request, CANDIDATE_RESOURCE_KEY)

        slice_service = ietf_data["network-slice-services"]["slice-service"][0]
        sdps = slice_service["sdps"]["sdp"]

        # Find and modify the specified SDP
        sdp_to_update = next((s for s in sdps if s["id"] == sdp_id), None)
        if not sdp_to_update:
            raise Exception(f"SDP '{sdp_id}' not found in slice '{slice_uuid}'")

        match_criteria = sdp_to_update["service-match-criteria"]["match-criterion"]
        mc_index = next(
            (
                i
                for i, m in enumerate(match_criteria)
                if m["index"] == match_criterion_id
            ),
            None,
        )
        if mc_index is None:
            raise Exception(
                f"No match-criterion with index '{match_criterion_id}' found in SDP '{sdp_id}'"
            )

        match_criteria.pop(mc_index)
        update_ietf_data_in_config(slice_request, CANDIDATE_RESOURCE_KEY, ietf_data)
        return slice_request

    @staticmethod
    def copy_candidate_ietf_slice_data_to_running(
        slice_uuid: str, context_client: ContextClient
    ) -> Slice:
        """
        Copy candidate IETF slice data to the running IETF slice data for a given slice.
        """
        slice_request = get_slice_by_defualt_name(
            context_client, slice_uuid, rw_copy=False
        )
        candidate_ietf_data = get_ietf_data_from_config(
            slice_request, CANDIDATE_RESOURCE_KEY
        )
        update_ietf_data_in_config(
            slice_request, RUNNING_RESOURCE_KEY, candidate_ietf_data
        )
        return slice_request
