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

# Convert the Explicit Route Object (ERO)-like paths produced by the PathComp component (response['path']) into
# explicit hops with ingress and egress endpoints per device (path_hops).
#
# response['path'] = [{
#     'path-capacity': {'total-size': {'value': 200, 'unit': 0}},
#     'path-latency': {'fixed-latency-characteristic': '12.000000'},
#     'path-cost': {'cost-name': '', 'cost-value': '6.000000', 'cost-algorithm': '0.000000'},
#     'devices': [
#         {'device_id': 'DC1-GW', 'endpoint_uuid': 'int'},
#         {'device_id': 'DC1-GW', 'endpoint_uuid': 'eth1'},
#         {'device_id': 'CS1-GW1', 'endpoint_uuid': '1/2'},
#         {'device_id': 'TN-R2', 'endpoint_uuid': '2/1'},
#         {'device_id': 'TN-OLS', 'endpoint_uuid': 'ca46812e8ad7'},
#         {'device_id': 'TN-R3', 'endpoint_uuid': '1/1'},
#         {'device_id': 'CS2-GW1', 'endpoint_uuid': '10/1'},
#         {'device_id': 'DC2-GW', 'endpoint_uuid': 'int'}
#     ]
# }]
#
# path_hops = [
#   {'device': 'DC1-GW', 'ingress_ep': 'int', 'egress_ep': 'eth1'},
#   {'device': 'CS1-GW1', 'ingress_ep': '10/1', 'egress_ep': '1/2'},
#   {'device': 'TN-R2', 'ingress_ep': '1/2', 'egress_ep': '2/1'},
#   {'device': 'TN-OLS', 'ingress_ep': '951f2f57e4a4', 'egress_ep': 'ca46812e8ad7'},
#   {'device': 'TN-R3', 'ingress_ep': '2/1', 'egress_ep': '1/1'},
#   {'device': 'CS2-GW1', 'ingress_ep': '1/1', 'egress_ep': '10/1'},
#   {'device': 'DC2-GW', 'ingress_ep': 'eth1', 'egress_ep': 'int'}
# ]
#

import logging
from typing import Dict, List, Tuple
from common.proto.context_pb2 import Link

LOGGER = logging.getLogger(__name__)

MAP_TAPI_UUIDS = {
    "c3dbaa44-9cda-5d54-8f99-0f282362be65": "5b835e46-53f7-52e8-9c8a-077322679e36", # node-1-port-13-input => node-1-port-13-output
    "1fb9ac86-b7ad-5d6d-87b1-a09d995f1ddd": "c9df6ece-1650-5078-876a-1e488a453625", # node-1-port-14-input => node-1-port-14-output
    "aa109937-8291-5a09-853a-97bff463e569": "b245480f-027c-53a0-9320-fca5b9d7a1e1", # node-1-port-15-input => node-1-port-15-output
    "6653ae16-42a3-56b5-adf3-71adda024a61": "ac356900-ce2f-5c15-b038-1b05e6f50bf7", # node-1-port-17-input => node-1-port-17-output
    "d782ef85-a473-50b4-93b5-2af86024a42a": "dcfeedd3-2d47-5bc8-b31c-ed9f973d8b76", # node-2-port-13-input => node-2-port-13-output
    "bbbd83ef-6053-55dc-ab08-06fb0c2bd081": "57bcf45b-eb47-5a9c-86d1-d9cff0c910fd", # node-2-port-14-input => node-2-port-14-output
    "27cdf70d-4e48-53ff-bc4f-20addf6524c0": "fd31eff5-392e-5fb5-a6f4-6dfca583344d", # node-2-port-15-input => node-2-port-15-output
    "55ac2364-fad8-5a05-ac2b-5003997ff89e": "d12a2591-7f4a-575d-8fda-0bc3d6b7ca32", # node-2-port-17-input => node-2-port-17-output
    "59f44a3c-32a5-5abf-af58-45e6fa7ca657": "1977ef5c-4383-5195-9221-0cdf8ee26cb7", # node-3-port-13-input => node-3-port-13-output
    "1be3f905-d553-5291-9906-47c0772d45aa": "9def067b-9a75-54df-8867-853f35a42e87", # node-3-port-14-input => node-3-port-14-output
    "fb4ece7a-2dd1-593a-b6ca-a787b3b59fc5": "1f294257-132a-54ad-b653-ef8b7517c9d8", # node-3-port-15-input => node-3-port-15-output
    "a571d2fe-c7f8-5ac8-b2af-8e5b92a558b0": "5b60a688-deac-567a-8e36-0d52e56fd4fc", # node-3-port-16-input => node-3-port-16-output
    "9ea9dc53-2d6a-5f28-b81a-e930f7cbedf9": "2aec14c1-3a84-5cba-8f22-783bd0273cd0", # node-3-port-17-input => node-3-port-17-output
    "9ec8e0f3-3378-55e0-bed1-be1fe120a1a9": "ece2ed55-ce16-59d3-8137-3f4cf17e67ab", # node-3-port-18-input => node-3-port-18-output
    "a7e114aa-a3b6-52ae-b7b7-0e5fe4dd4d1c": "0a05e43d-a13c-5276-9839-613600f3ff28", # node-4-port-13-input => node-4-port-13-output
    "4ca8357a-3468-51e6-bba8-65137486666f": "18926fdf-de5c-5a52-be88-cccc065e5e03", # node-4-port-14-input => node-4-port-14-output
    "a7e9f06f-6fd2-594e-8a0c-25bfe8c652d7": "1adb9e17-e499-58dc-8aa2-881ed5ce9670", # node-4-port-15-input => node-4-port-15-output
    "9f6a23b2-c71c-5559-8fb3-f76421bea1d9": "049bb1f1-cc04-5b72-8c0f-43891d9637bf", # node-4-port-16-input => node-4-port-16-output
    "f1d74c96-41f5-5eb9-a160-a38463184934": "2206440b-ef66-5d3e-8da5-40608fb00a10", # node-4-port-17-input => node-4-port-17-output

    "5b835e46-53f7-52e8-9c8a-077322679e36": "c3dbaa44-9cda-5d54-8f99-0f282362be65", # node-1-port-13-output => node-1-port-13-input
    "c9df6ece-1650-5078-876a-1e488a453625": "1fb9ac86-b7ad-5d6d-87b1-a09d995f1ddd", # node-1-port-14-output => node-1-port-14-input
    "b245480f-027c-53a0-9320-fca5b9d7a1e1": "aa109937-8291-5a09-853a-97bff463e569", # node-1-port-15-output => node-1-port-15-input
    "ac356900-ce2f-5c15-b038-1b05e6f50bf7": "6653ae16-42a3-56b5-adf3-71adda024a61", # node-1-port-17-output => node-1-port-17-input
    "dcfeedd3-2d47-5bc8-b31c-ed9f973d8b76": "d782ef85-a473-50b4-93b5-2af86024a42a", # node-2-port-13-output => node-2-port-13-input
    "57bcf45b-eb47-5a9c-86d1-d9cff0c910fd": "bbbd83ef-6053-55dc-ab08-06fb0c2bd081", # node-2-port-14-output => node-2-port-14-input
    "fd31eff5-392e-5fb5-a6f4-6dfca583344d": "27cdf70d-4e48-53ff-bc4f-20addf6524c0", # node-2-port-15-output => node-2-port-15-input
    "d12a2591-7f4a-575d-8fda-0bc3d6b7ca32": "55ac2364-fad8-5a05-ac2b-5003997ff89e", # node-2-port-17-output => node-2-port-17-input
    "1977ef5c-4383-5195-9221-0cdf8ee26cb7": "59f44a3c-32a5-5abf-af58-45e6fa7ca657", # node-3-port-13-output => node-3-port-13-input
    "9def067b-9a75-54df-8867-853f35a42e87": "1be3f905-d553-5291-9906-47c0772d45aa", # node-3-port-14-output => node-3-port-14-input
    "1f294257-132a-54ad-b653-ef8b7517c9d8": "fb4ece7a-2dd1-593a-b6ca-a787b3b59fc5", # node-3-port-15-output => node-3-port-15-input
    "5b60a688-deac-567a-8e36-0d52e56fd4fc": "a571d2fe-c7f8-5ac8-b2af-8e5b92a558b0", # node-3-port-16-output => node-3-port-16-input
    "2aec14c1-3a84-5cba-8f22-783bd0273cd0": "9ea9dc53-2d6a-5f28-b81a-e930f7cbedf9", # node-3-port-17-output => node-3-port-17-input
    "ece2ed55-ce16-59d3-8137-3f4cf17e67ab": "9ec8e0f3-3378-55e0-bed1-be1fe120a1a9", # node-3-port-18-output => node-3-port-18-input
    "0a05e43d-a13c-5276-9839-613600f3ff28": "a7e114aa-a3b6-52ae-b7b7-0e5fe4dd4d1c", # node-4-port-13-output => node-4-port-13-input
    "18926fdf-de5c-5a52-be88-cccc065e5e03": "4ca8357a-3468-51e6-bba8-65137486666f", # node-4-port-14-output => node-4-port-14-input
    "1adb9e17-e499-58dc-8aa2-881ed5ce9670": "a7e9f06f-6fd2-594e-8a0c-25bfe8c652d7", # node-4-port-15-output => node-4-port-15-input
    "049bb1f1-cc04-5b72-8c0f-43891d9637bf": "9f6a23b2-c71c-5559-8fb3-f76421bea1d9", # node-4-port-16-output => node-4-port-16-input
    "2206440b-ef66-5d3e-8da5-40608fb00a10": "f1d74c96-41f5-5eb9-a160-a38463184934", # node-4-port-17-output => node-4-port-17-input
}

def eropath_to_hops(
    ero_path : List[Dict], endpoint_to_link_dict : Dict[Tuple[str, str, str], Tuple[Dict, Link]]
) -> List[Dict]:
    LOGGER.debug('ero_path = {:s}'.format(str(ero_path)))
    try:
        path_hops = []
        num_ero_hops = len(ero_path)
        for endpoint in ero_path:
            device_uuid = endpoint['device_id']
            endpoint_uuid = endpoint['endpoint_uuid']

            if len(path_hops) == 0:
                path_hops.append({'device': device_uuid, 'ingress_ep': endpoint_uuid})
                continue

            last_hop = path_hops[-1]
            if last_hop['device'] != device_uuid: raise Exception('Malformed path')
            last_hop['egress_ep'] = endpoint_uuid

            if num_ero_hops - 1 == len(path_hops): break

            endpoint_key = (last_hop['device'], last_hop['egress_ep'], 'src')
            link_tuple = endpoint_to_link_dict[endpoint_key]
            if link_tuple is None: raise Exception('Malformed path')

            ingress = next(iter([
                ep_id
                for ep_id in link_tuple[0]['link_endpoint_ids']
                if ep_id['endpoint_id']['device_id'] != device_uuid
            ]), None)

            ingress_ep = ingress['endpoint_id']['endpoint_uuid']
            ingress_ep = MAP_TAPI_UUIDS.get(ingress_ep, ingress_ep)
            path_hops.append({
                'device': ingress['endpoint_id']['device_id'],
                'ingress_ep': ingress_ep,
                'egress_ep': endpoint_uuid,
            })
        LOGGER.debug('path_hops = {:s}'.format(str(path_hops)))
        return path_hops
    except:
        LOGGER.exception('Unhandled exception: ero_path={:s} endpoint_to_link_dict={:s}'.format(
            str(ero_path), str(endpoint_to_link_dict)))
        raise
