# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import random
import uuid
import sys
import time
import requests

from bindings.network_slice_services import NetworkSliceServices


# R1 emulated devices
# Port 13-0 is Optical
# Port 13-1 is Copper
R1_UUID = "ed2388eb-5fb9-5888-a4f4-160267d3e19b"
R1_PORT_13_0_UUID_OPTICAL = "20440915-1a6c-5e7b-a80f-b0e0e51f066d"
R1_PORT_13_1_UUID_COPPER = "ff900d5d-2ac0-576c-9628-a2d016681f9d"

# R2 emulated devices
# Port 13-0 is Optical
# Port 13-1 is Copper
R2_UUID = "49ce0312-1274-523b-97b8-24d0eca2d72d"
R2_PORT_13_0_UUID_OPTICAL = "214618cb-b63b-5e66-84c2-45c1c016e5f0"
R2_PORT_13_1_UUID_COPPER = "4e0f7fb4-5d22-56ad-a00e-20bffb4860f9"

# R3 emulated devices
# Port 13-0 is Optical
# Port 13-1 is Copper
R3_UUID = "3bc8e994-a3b9-5f60-9c77-6608b1d08313"
R3_PORT_13_0_UUID_OPTICAL = "da5196f5-d651-5def-ada6-50ed6430279d"
R3_PORT_13_1_UUID_COPPER = "43d221fa-5701-5740-a129-502131f5bda2"

# R4 emulated devices
# Port 13-0 is Optical
# Port 13-1 is Copper
R4_UUID = "b43e6361-2573-509d-9a88-1793e751b10d"
R4_PORT_13_0_UUID_OPTICAL = "241b74a7-8677-595c-ad65-cc9093c1e341"
R4_PORT_13_1_UUID_COPPER = "c57abf46-caaf-5954-90cc-1fec0a69330e"

node_dict = {R1_PORT_13_1_UUID_COPPER: R1_UUID,
             R2_PORT_13_1_UUID_COPPER: R2_UUID,
             R3_PORT_13_1_UUID_COPPER: R3_UUID,
             R4_PORT_13_1_UUID_COPPER: R4_UUID}
list_endpoints = [R1_PORT_13_1_UUID_COPPER,
                  R2_PORT_13_1_UUID_COPPER,
                  R3_PORT_13_1_UUID_COPPER,
                  R4_PORT_13_1_UUID_COPPER]

list_availability= [99, 99.9, 99.99, 99.999, 99.9999]
list_bw = [10, 40, 50, 100, 150, 200, 400]
list_owner = ["Telefonica", "CTTC", "Telenor", "ADVA", "Ubitech", "ATOS"]

URL_POST = "/restconf/data/ietf-network-slice-service:ietf-nss/network-slice-services"
URL_DELETE = "/restconf/data/ietf-network-slice-service:ietf-nss/network-slice-services/slice-service="

def generate_request(seed: str) -> (dict, str):

    ns = NetworkSliceServices()

    # Slice 1
    suuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(seed)))
    slice1 = ns.slice_service[suuid]
    slice1.service_description = "Test slice for OFC 2023 demo"
    slice1.status().admin_status().status = "Planned"  # TODO not yet mapped

    '''
    SDPS:
    R1 optical to R3 optical
    '''
    sdps1 = slice1.sdps().sdp
    while True:
        ep1_uuid = random.choice(list_endpoints)
        ep2_uuid = random.choice(list_endpoints)
        if ep1_uuid != ep2_uuid:
            break

    sdps1[ep1_uuid].node_id = node_dict.get(ep1_uuid)
    sdps1[ep2_uuid].node_id = node_dict.get(ep2_uuid)

    '''
    Connectivity group
    Connection construct and 2 sla constrains:
        - Bandwidth
        - Availability
    '''
    cg_uuid = str(uuid.uuid4())
    cg = slice1.connection_groups().connection_group
    cg1 = cg[cg_uuid]

    cc1 = cg1.connectivity_construct[0]
    cc1.cc_id = 5
    p2p = cc1.connectivity_construct_type.p2p()
    p2p.p2p_sender_sdp = ep1_uuid
    p2p.p2p_receiver_sdp = ep2_uuid

    slo_custom = cc1.slo_sle_policy.custom()
    metric_bounds = slo_custom.service_slo_sle_policy().metric_bounds().metric_bound

    # SLO Bandwidth
    slo_bandwidth = metric_bounds["service-slo-two-way-bandwidth"]
    slo_bandwidth.value_description = "Guaranteed bandwidth"
    slo_bandwidth.bound = int(random.choice(list_bw))
    slo_bandwidth.metric_unit = "Gbps"

    # SLO Availability
    slo_availability = metric_bounds["service-slo-availability"]
    slo_availability.value_description = "Guaranteed availability"
    slo_availability.metric_unit = "percentage"
    slo_availability.bound = random.choice(list_availability)

    json_request = {"data": ns.to_json()}

    #Last, add name and owner manually
    list_name_owner = [{"tag-type": "owner", "value": random.choice(list_owner)}]
    json_request["data"]["ietf-network-slice-service:network-slice-services"]["slice-service"][0]["service-tags"] = list_name_owner

    return (json_request, suuid)


if __name__ == "__main__":
    print("Generating requests...")
    num = int(sys.argv[2])
    ip = str(sys.argv[1])
    list_requests = []

    for i in range(num):
        request = generate_request(i)
        list_requests.append(request)
        print(f"HTTP.POST={request[0]}-{request[1]}")
        time.sleep(2)
        requests.post(f"http://{ip}{URL_POST}", auth=("admin", "admin"), json=request[0])

    print("Slices sent, please press Enter key to delete them...")
    input()

    for request,suuid in list_requests:
        requests.delete(f"http://{ip}{URL_DELETE}{suuid}", auth=("admin", "admin"))
        print(f"HTTP.DELETE={suuid}")
        time.sleep(2)
    print("All slices deleted!")





