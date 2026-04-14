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

# Enable eventlet for async networking
# NOTE: monkey_patch needs to be executed before importing any other module.
import eventlet
eventlet.monkey_patch()

#pylint: disable=wrong-import-position
import json
from typing import Optional

from common.proto.context_pb2 import ConfigRule, ServiceConfig, SliceList
from context.client.ContextClient import ContextClient
from nbi.service.ietf_network_slice.ietf_slice_handler import (
    IETFSliceHandler,
)


def get_custom_config_rule(
    service_config: ServiceConfig, resource_key: str
) -> Optional[ConfigRule]:
    for cr in service_config.config_rules:
        if (
            cr.WhichOneof("config_rule") == "custom"
            and cr.custom.resource_key == resource_key
        ):
            return cr


RUNNING_RESOURCE_KEY = "running_ietf_slice"
CANDIDATE_RESOURCE_KEY = "candidate_ietf_slice"

context_client = ContextClient()

with open("nbi/tests/data/slice/post_network_slice1.json", mode="r") as f:
    post_slice_request = json.load(f)

with open("nbi/tests/data/slice/post_sdp_to_network_slice1.json", mode="r") as f:
    post_sdp_request = json.load(f)

with open(
    "nbi/tests/data/slice/post_connection_group_to_network_slice1.json", mode="r"
) as f:
    post_connection_group_request = json.load(f)

with open(
    "nbi/tests/data/slice/post_match_criteria_to_sdp1_in_slice1.json", mode="r"
) as f:
    post_match_criteria_request = json.load(f)

slice_1 = None


def select_slice(*args) -> SliceList:
    slice_list = SliceList()
    slice_list.slices.extend([slice_1])
    return slice_list


def test_create_slice():
    global slice_1

    slice_1 = IETFSliceHandler.create_slice_service(post_slice_request)
    candidate_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, CANDIDATE_RESOURCE_KEY
        ).custom.resource_value
    )
    assert candidate_ietf_data["network-slice-services"] == post_slice_request
    assert slice_1.slice_endpoint_ids[0].device_id.device_uuid.uuid == "172.16.204.220"
    assert slice_1.slice_endpoint_ids[1].device_id.device_uuid.uuid == "172.16.61.10"
    assert slice_1.slice_id.slice_uuid.uuid == "slice1"


def test_create_sdp(monkeypatch):
    global slice_1

    monkeypatch.setattr(context_client, "SelectSlice", select_slice)

    slice_1 = IETFSliceHandler.create_sdp(post_sdp_request, "slice1", context_client)
    candidate_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, CANDIDATE_RESOURCE_KEY
        ).custom.resource_value
    )
    slice_services = candidate_ietf_data["network-slice-services"]["slice-service"]
    slice_service = slice_services[0]
    slice_sdps = slice_service["sdps"]["sdp"]
    assert len(slice_sdps) == 3


def test_create_connection_group(monkeypatch):
    global slice_1

    monkeypatch.setattr(context_client, "SelectSlice", select_slice)

    slice_1 = IETFSliceHandler.create_connection_group(
        post_connection_group_request, "slice1", context_client
    )
    candidate_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, CANDIDATE_RESOURCE_KEY
        ).custom.resource_value
    )
    slice_services = candidate_ietf_data["network-slice-services"]["slice-service"]
    slice_service = slice_services[0]
    slice_connection_groups = slice_service["connection-groups"]["connection-group"]

    assert slice_connection_groups[0]["id"] == "line1"
    assert slice_connection_groups[1]["id"] == "line2"
    assert len(slice_connection_groups) == 2


def test_create_match_criteria(monkeypatch):
    global slice_1

    monkeypatch.setattr(context_client, "SelectSlice", select_slice)

    slice_1 = IETFSliceHandler.create_match_criteria(
        post_match_criteria_request, "slice1", "1", context_client
    )
    candidate_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, CANDIDATE_RESOURCE_KEY
        ).custom.resource_value
    )
    slice_services = candidate_ietf_data["network-slice-services"]["slice-service"]
    slice_service = slice_services[0]
    slice_sdps = slice_service["sdps"]["sdp"]
    sdp1_match_criteria = slice_sdps[0]["service-match-criteria"]["match-criterion"]

    slice_1 = IETFSliceHandler.copy_candidate_ietf_slice_data_to_running("slice1", context_client)
    assert len(sdp1_match_criteria) == 2
    assert sdp1_match_criteria[0]["target-connection-group-id"] == "line1"
    assert sdp1_match_criteria[1]["target-connection-group-id"] == "line2"
    assert slice_1.slice_endpoint_ids[0].device_id.device_uuid.uuid == "172.16.204.220"
    assert slice_1.slice_endpoint_ids[1].device_id.device_uuid.uuid == "172.16.61.11"


def test_delete_sdp(monkeypatch):
    global slice_1

    monkeypatch.setattr(context_client, "SelectSlice", select_slice)

    slice_1 = IETFSliceHandler.delete_sdp("slice1", "3", context_client)
    candidate_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, CANDIDATE_RESOURCE_KEY
        ).custom.resource_value
    )
    slice_services = candidate_ietf_data["network-slice-services"]["slice-service"]
    slice_service = slice_services[0]
    slice_sdps = slice_service["sdps"]["sdp"]
    assert len(slice_sdps) == 2
    assert "3" not in (sdp["id"] for sdp in slice_sdps)


def test_delete_connection_group(monkeypatch):
    global slice_1

    monkeypatch.setattr(context_client, "SelectSlice", select_slice)
    running_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, RUNNING_RESOURCE_KEY
        ).custom.resource_value
    )
    slice_1 = IETFSliceHandler.delete_connection_group(
        "slice1", "line2", context_client
    )
    
    candidate_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, CANDIDATE_RESOURCE_KEY
        ).custom.resource_value
    )
    slice_services = candidate_ietf_data["network-slice-services"]["slice-service"]
    slice_service = slice_services[0]
    slice_connection_groups = slice_service["connection-groups"]["connection-group"]
    assert len(slice_connection_groups) == 1
    assert slice_connection_groups[0]["id"] == "line1"


def test_delete_match_criteria(monkeypatch):
    global slice_1

    monkeypatch.setattr(context_client, "SelectSlice", select_slice)

    slice_1 = IETFSliceHandler.delete_match_criteria("slice1", "1", 2, context_client)
    candidate_ietf_data = json.loads(
        get_custom_config_rule(
            slice_1.slice_config, CANDIDATE_RESOURCE_KEY
        ).custom.resource_value
    )
    slice_services = candidate_ietf_data["network-slice-services"]["slice-service"]
    slice_service = slice_services[0]
    slice_sdps = slice_service["sdps"]["sdp"]
    sdp1_match_criteria = slice_sdps[0]["service-match-criteria"]["match-criterion"]
    assert len(sdp1_match_criteria) == 1
    assert sdp1_match_criteria[0]["target-connection-group-id"] == "line1"
