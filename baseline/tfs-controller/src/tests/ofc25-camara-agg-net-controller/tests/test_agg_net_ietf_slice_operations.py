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

TARGET_L3VPN_SLICE1_STAGES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "target-l3vpn-slice1-stages.json",
)

TARGET_L3VPN_SLICE2_STAGES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "target-l3vpn-slice2-stages.json",
)

OP1_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "pc1_slice1_post_ietf_network_slice.json",
)

OP2_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "pc2_slice1_put_ietf_network_slice.json",
)

OP3_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "pc1_slice2_post_ietf_network_slice.json",
)

OP4_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "pc2_slice2_put_ietf_network_slice.json",
)

OP6_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "pc1_slice1_put_ietf_network_slice.json",
)

OP8_IETF_SLICE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "pc1_slice2_put_ietf_network_slice.json",
)

NBI_ADDRESS = "localhost"
NBI_PORT = "80"
NBI_USERNAME = "admin"
NBI_PASSWORD = "admin"

IP_ADDRESS = "localhost"
IP_PORT = 9092

BASE_IETF_SLICE_URL = f"http://{NBI_ADDRESS}:{NBI_PORT}/restconf/data/ietf-network-slice-service:network-slice-services"
IP_L3VPN_URL = f"http://{IP_ADDRESS}:{IP_PORT}/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services"

# pylint: disable=redefined-outer-name, unused-argument
def test_ietf_slice_creation_removal():
    # Issue service creation request
    with open(OP1_IETF_SLICE, "r", encoding="UTF-8") as f:
        op1_ietf_slice = json.load(f)
    with open(OP2_IETF_SLICE, "r", encoding="UTF-8") as f:
        op2_ietf_slice = json.load(f)
    with open(OP3_IETF_SLICE, "r", encoding="UTF-8") as f:
        op3_ietf_slice = json.load(f)
    with open(OP4_IETF_SLICE, "r", encoding="UTF-8") as f:
        op4_ietf_slice = json.load(f)
    with open(OP6_IETF_SLICE, "r", encoding="UTF-8") as f:
        op6_ietf_slice = json.load(f)
    with open(OP8_IETF_SLICE, "r", encoding="UTF-8") as f:
        op8_ietf_slice = json.load(f)
    with open(TARGET_L3VPN_SLICE1_STAGES, "r", encoding="UTF-8") as f:
        target_l3vpn_slice1_stages = json.load(f)
    with open(TARGET_L3VPN_SLICE2_STAGES, "r", encoding="UTF-8") as f:
        target_l3vpn_slice2_stages = json.load(f)

    # op 1
    URL = BASE_IETF_SLICE_URL
    requests.post(URL, headers=HEADERS, json=op1_ietf_slice)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice1"
    diff = DeepDiff(target_l3vpn_slice1_stages[0], l3vpns[slice_name])
    assert not diff

    # op 2
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1/connection-groups/connection-group=line1"
    requests.put(URL, headers=HEADERS, json=op2_ietf_slice)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice1"
    diff = DeepDiff(target_l3vpn_slice1_stages[1], l3vpns[slice_name])
    assert not diff

    # op 3
    URL = BASE_IETF_SLICE_URL
    requests.post(URL, headers=HEADERS, json=op3_ietf_slice)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice2"
    diff = DeepDiff(target_l3vpn_slice2_stages[0], l3vpns[slice_name])
    assert not diff

    # op 4
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2/connection-groups/connection-group=line1"
    requests.put(URL, headers=HEADERS, json=op4_ietf_slice)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice2"
    diff = DeepDiff(target_l3vpn_slice2_stages[1], l3vpns[slice_name])
    assert not diff

    # op 5


    # op 6
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1/connection-groups/connection-group=line1"
    requests.put(URL, headers=HEADERS, json=op6_ietf_slice)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice1"
    diff = DeepDiff(target_l3vpn_slice1_stages[2], l3vpns[slice_name])
    assert not diff

    # op 7
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice1"
    requests.delete(URL)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice1"
    assert slice_name not in l3vpns

    # op 8
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2/connection-groups/connection-group=line1"
    requests.put(URL, headers=HEADERS, json=op8_ietf_slice)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice2"
    diff = DeepDiff(target_l3vpn_slice2_stages[2], l3vpns[slice_name])
    assert not diff

    # op 9
    URL = BASE_IETF_SLICE_URL + "/slice-service=slice2"
    requests.delete(URL)

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    slice_name = "slice2"
    assert slice_name not in l3vpns

    # op 10

    URL = IP_L3VPN_URL
    l3vpns = requests.get(URL).json()

    assert not l3vpns
