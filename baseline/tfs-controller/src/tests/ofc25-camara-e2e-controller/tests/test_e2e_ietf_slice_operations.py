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

import json, logging, os
import requests
from deepdiff import DeepDiff


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

HEADERS = {"Content-Type": "application/json"}

POST_NETWORK_SLICE1 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_network_slice1.json",
)
POST_NETWORK_SLICE2 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_network_slice2.json",
)
POST_CONNECTION_GROUP_TO_NETWORK_SLICE1 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_connection_group_to_network_slice1.json",
)
POST_CONNECTION_GROUP_TO_NETWORK_SLICE2 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_connection_group_to_network_slice2.json",
)
POST_MATCH_CRITERIA_TO_SDP1_IN_SLICE1 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_match_criteria_to_sdp1_in_slice1.json",
)
POST_MATCH_CRITERIA_TO_SDP1_IN_SLICE2 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_match_criteria_to_sdp1_in_slice2.json",
)
POST_SDP_TO_NETWORK_SLICE1 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_sdp_to_network_slice1.json",
)
POST_SDP_TO_NETWORK_SLICE2 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "post_sdp_to_network_slice2.json",
)
TARGET_NCE_APP_FLOWS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "target-nce-app-flows.json",
)
TARGET_NCE_APPS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "target-nce-apps.json",
)
TARGET_FULL_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "slice",
    "target-full-ietf-slice.json",
)
TARGET_FULL_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "target-full-ietf-slice.json",
)
TARGET_IETF_SLICE_POSTED_SLICES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "target-ietf-slice-posted-slices.json",
)
TARGET_IETF_SLICE_PUT_CONNECTION_GROUPS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "target-ietf-slice-put-connection-groups.json",
)

NBI_ADDRESS = "localhost"
NBI_PORT = "80"
NBI_USERNAME = "admin"
NBI_PASSWORD = "admin"

NCE_ADDRESS = "localhost"
NCE_PORT = 9090

AGG_TFS_ADDRESS = "localhost"
AGG_TFS_PORT = 9091

BASE_IETF_SLICE_URL = f"http://{NBI_ADDRESS}:{NBI_PORT}/restconf/data/ietf-network-slice-service:network-slice-services"
NCE_APP_DATA_URL = f"http://{NCE_ADDRESS}:{NCE_PORT}/restconf/v1/data/app-flows/apps"
NCE_APP_FLOW_DATA_URL = f"http://{NCE_ADDRESS}:{NCE_PORT}/restconf/v1/data/app-flows"
AGG_TFS_IETF_SLICE_URL = f"http://{AGG_TFS_ADDRESS}:{AGG_TFS_PORT}/restconf/data/ietf-network-slice-service:network-slice-services"


# pylint: disable=redefined-outer-name, unused-argument
def test_ietf_slice_creation_removal():
    # Issue service creation request
    with open(POST_NETWORK_SLICE1, "r", encoding="UTF-8") as f:
        post_network_slice1 = json.load(f)
    with open(POST_NETWORK_SLICE2, "r", encoding="UTF-8") as f:
        post_network_slice2 = json.load(f)
    with open(POST_CONNECTION_GROUP_TO_NETWORK_SLICE1, "r", encoding="UTF-8") as f:
        post_connection_group_to_network_slice1 = json.load(f)
    with open(POST_CONNECTION_GROUP_TO_NETWORK_SLICE2, "r", encoding="UTF-8") as f:
        post_connection_group_to_network_slice2 = json.load(f)
    with open(POST_MATCH_CRITERIA_TO_SDP1_IN_SLICE1, "r", encoding="UTF-8") as f:
        post_match_criteria_to_sdp1_in_slice1 = json.load(f)
    with open(POST_MATCH_CRITERIA_TO_SDP1_IN_SLICE2, "r", encoding="UTF-8") as f:
        post_match_criteria_to_sdp1_in_slice2 = json.load(f)
    with open(POST_SDP_TO_NETWORK_SLICE1, "r", encoding="UTF-8") as f:
        post_sdp_to_network_slice1 = json.load(f)
    with open(POST_SDP_TO_NETWORK_SLICE2, "r", encoding="UTF-8") as f:
        post_sdp_to_network_slice2 = json.load(f)
    with open(TARGET_NCE_APPS, "r", encoding="UTF-8") as f:
        target_nce_apps = json.load(f)
    with open(TARGET_NCE_APP_FLOWS, "r", encoding="UTF-8") as f:
        target_nce_app_flows = json.load(f)
    with open(TARGET_FULL_IETF_SLICE, "r", encoding="UTF-8") as f:
        target_full_ietf_slice = json.load(f)
    with open(TARGET_IETF_SLICE_POSTED_SLICES, "r", encoding="UTF-8") as f:
        target_ietf_slice_posted_slices = json.load(f)
    with open(TARGET_IETF_SLICE_PUT_CONNECTION_GROUPS, "r", encoding="UTF-8") as f:
        target_ietf_slice_put_connection_groups = json.load(f)

    # op 1
    URL = BASE_IETF_SLICE_URL
    requests.post(URL, headers=HEADERS, json=post_network_slice1)

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    app_name = "App_Flow_2_1_slice1"
    apps_diff = DeepDiff(apps_response[app_name], target_nce_apps[app_name])
    app_flows_diff = DeepDiff(
        app_flows_response[app_name],
        target_nce_app_flows[app_name],
        exclude_regex_paths=r"root\['app-flow'\]\[\d+\]\['user-id'\]",
    )
    assert not apps_diff
    assert not app_flows_diff
    assert len(apps_response) == 1 and len(app_flows_response) == 1

    assert len(ietf_slice_connection_groups) == 0
    assert len(ietf_slice_services) == 1
    slice_diff = DeepDiff(
        ietf_slice_services["slice1"], target_ietf_slice_posted_slices[0]
    )
    assert not slice_diff

    # op 2
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1/sdps"
    requests.post(URL, headers=HEADERS, json=post_sdp_to_network_slice1)
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1/connection-groups"
    requests.post(URL, headers=HEADERS, json=post_connection_group_to_network_slice1)
    URL = (
        BASE_IETF_SLICE_URL + "/slice-service=slice1/sdps/sdp=1/service-match-criteria"
    )
    requests.post(URL, headers=HEADERS, json=post_match_criteria_to_sdp1_in_slice1)

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    app_name = "App_Flow_3_1_slice1"
    apps_diff = DeepDiff(apps_response[app_name], target_nce_apps[app_name])
    app_flows_diff = DeepDiff(
        app_flows_response[app_name],
        target_nce_app_flows[app_name],
        exclude_regex_paths=r"root\['app-flow'\]\[\d+\]\['user-id'\]",
    )
    assert not apps_diff
    assert not app_flows_diff
    assert len(apps_response) == 2 and len(app_flows_response) == 2

    assert len(ietf_slice_connection_groups) == 1
    assert len(ietf_slice_services) == 1
    connection_group_diff = DeepDiff(
        ietf_slice_connection_groups[0], target_ietf_slice_put_connection_groups[0]
    )
    assert not connection_group_diff

    # op 3
    URL = BASE_IETF_SLICE_URL
    requests.post(URL, headers=HEADERS, json=post_network_slice2)

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    app_name = "App_Flow_2_1_slice2"
    apps_diff = DeepDiff(apps_response[app_name], target_nce_apps[app_name])
    app_flows_diff = DeepDiff(
        app_flows_response[app_name],
        target_nce_app_flows[app_name],
        exclude_regex_paths=r"root\['app-flow'\]\[\d+\]\['user-id'\]",
    )
    assert not apps_diff
    assert not app_flows_diff
    assert len(apps_response) == 3 and len(app_flows_response) == 3

    assert len(ietf_slice_connection_groups) == 1
    assert len(ietf_slice_services) == 2
    slice_diff = DeepDiff(
        ietf_slice_services["slice2"], target_ietf_slice_posted_slices[1]
    )
    assert not slice_diff

    # op 4
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2/sdps"
    requests.post(URL, headers=HEADERS, json=post_sdp_to_network_slice2)
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2/connection-groups"
    requests.post(URL, headers=HEADERS, json=post_connection_group_to_network_slice2)
    URL = (
        BASE_IETF_SLICE_URL + "/slice-service=slice2/sdps/sdp=1/service-match-criteria"
    )
    requests.post(URL, headers=HEADERS, json=post_match_criteria_to_sdp1_in_slice2)

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    app_name = "App_Flow_3_1_slice2"
    apps_diff = DeepDiff(apps_response[app_name], target_nce_apps[app_name])
    app_flows_diff = DeepDiff(
        app_flows_response[app_name],
        target_nce_app_flows[app_name],
        exclude_regex_paths=r"root\['app-flow'\]\[\d+\]\['user-id'\]",
    )
    assert not apps_diff
    assert not app_flows_diff
    assert len(apps_response) == 4 and len(app_flows_response) == 4

    assert len(ietf_slice_connection_groups) == 2
    assert len(ietf_slice_services) == 2
    connection_group_diff = DeepDiff(
        ietf_slice_connection_groups[1], target_ietf_slice_put_connection_groups[1]
    )
    assert not connection_group_diff

    # op 5
    ietf_slices_full_retrieved = requests.get(BASE_IETF_SLICE_URL).json()
    ietf_slice_data = DeepDiff(ietf_slices_full_retrieved, target_full_ietf_slice)
    assert not ietf_slice_data

    # op 6
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1/sdps/sdp=2"
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice1/sdps/sdp=1/service-match-criteria/match-criterion=1"
    )
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice1/connection-groups/connection-group=line1"
    )
    requests.delete(URL)

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    app_name = "App_Flow_2_1_slice1"
    assert app_name not in apps_response
    assert app_name not in app_flows_response
    assert len(apps_response) == 3 and len(app_flows_response) == 3

    assert len(ietf_slice_connection_groups) == 3
    assert len(ietf_slice_services) == 2
    connection_group_diff = DeepDiff(
        ietf_slice_connection_groups[2], target_ietf_slice_put_connection_groups[2]
    )
    assert not connection_group_diff

    # op 7
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1/sdps/sdp=3"
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice1/sdps/sdp=1/service-match-criteria/match-criterion=2"
    )
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice1/connection-groups/connection-group=line2"
    )
    requests.delete(URL)
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1/sdps/sdp=1"

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    requests.delete(URL)
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1"
    requests.delete(URL)

    app_name = "App_Flow_3_1_slice1"
    assert app_name not in apps_response
    assert app_name not in app_flows_response
    assert len(apps_response) == 2 and len(app_flows_response) == 2

    assert len(ietf_slice_connection_groups) == 3
    assert len(ietf_slice_services) == 1
    assert "slice1" not in ietf_slice_services

    # op 8
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2/sdps/sdp=2"
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice2/sdps/sdp=1/service-match-criteria/match-criterion=1"
    )
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice2/connection-groups/connection-group=line1"
    )
    requests.delete(URL)

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    app_name = "App_Flow_2_1_slice2"
    assert app_name not in apps_response
    assert app_name not in app_flows_response
    assert len(apps_response) == 1 and len(app_flows_response) == 1

    assert len(ietf_slice_connection_groups) == 4
    assert len(ietf_slice_services) == 1
    connection_group_diff = DeepDiff(
        ietf_slice_connection_groups[3], target_ietf_slice_put_connection_groups[3]
    )
    assert not connection_group_diff

    # op 9
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2/sdps/sdp=3"
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice2/sdps/sdp=1/service-match-criteria/match-criterion=2"
    )
    requests.delete(URL)
    URL = (
        BASE_IETF_SLICE_URL
        + "/slice-service=slice2/connection-groups/connection-group=line2"
    )
    requests.delete(URL)

    URL = NCE_APP_DATA_URL
    apps_response = requests.get(URL).json()
    URL = NCE_APP_FLOW_DATA_URL
    app_flows_response = requests.get(URL).json()
    URL = AGG_TFS_IETF_SLICE_URL
    ietf_slice_services = requests.get(URL).json()
    URL = (
        AGG_TFS_IETF_SLICE_URL
        + "/slice-service=dummy/connection-groups/connection-group=dummy"
    )
    ietf_slice_connection_groups = requests.get(URL).json()

    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2/sdps/sdp=1"
    requests.delete(URL)
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2"
    requests.delete(URL)

    app_name = "App_Flow_3_1_slice2"
    assert app_name not in apps_response
    assert app_name not in app_flows_response
    assert len(apps_response) == 0 and len(app_flows_response) == 0

    assert len(ietf_slice_connection_groups) == 4
    assert len(ietf_slice_services) == 0

    # op 10
    ietf_slices_full_retrieved = requests.get(BASE_IETF_SLICE_URL).json()
    empty_ietf_slices = {"network-slice-services": {"slice-service": []}}
    ietf_slice_data = DeepDiff(ietf_slices_full_retrieved, empty_ietf_slices)
    assert not ietf_slice_data
