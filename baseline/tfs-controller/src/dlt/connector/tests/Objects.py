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

from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import json_device_emulated_packet_router_disabled, json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_descriptor, json_endpoints
from common.tools.object_factory.Link import compose_link
from common.tools.object_factory.Topology import json_topology, json_topology_id

def compose_device(
    device_uuid, endpoint_uuids, endpoint_type='copper', endpoint_topology_id=None, endpoint_sample_types=[]
):
    device_id = json_device_id(device_uuid)
    endpoints = [
        json_endpoint_descriptor(endpoint_uuid, endpoint_type, endpoint_sample_types)
        for endpoint_uuid in endpoint_uuids
    ]
    endpoints = json_endpoints(device_id, endpoints, topology_id=endpoint_topology_id)
    device = json_device_emulated_packet_router_disabled(device_uuid, endpoints=endpoints)
    return device_id, endpoints, device

# ===== Domain A =======================================================================================================

# ----- Context --------------------------------------------------------------------------------------------------------
DA_CONTEXT_ADMIN_ID = json_context_id('A')
DA_CONTEXT_ADMIN    = json_context('A')

# ----- Topology -------------------------------------------------------------------------------------------------------
DA_TOPOLOGY_ADMIN_ID = json_topology_id('A', context_id=DA_CONTEXT_ADMIN_ID)
DA_TOPOLOGY_ADMIN    = json_topology('A', context_id=DA_CONTEXT_ADMIN_ID)

# ----- Devices --------------------------------------------------------------------------------------------------------
DA_DEVICE_DEV1_ID, DA_DEVICE_DEV1_ENDPOINTS, DA_DEVICE_DEV1 = compose_device('DEV1@A', ['1', '2'])
DA_DEVICE_DEV2_ID, DA_DEVICE_DEV2_ENDPOINTS, DA_DEVICE_DEV2 = compose_device('DEV2@A', ['1', '2'])
DA_DEVICE_DEV3_ID, DA_DEVICE_DEV3_ENDPOINTS, DA_DEVICE_DEV3 = compose_device('DEV3@A', ['1', '2'])

# ----- Links ----------------------------------------------------------------------------------------------------------
DA_LINK_DEV1_DEV2_ID, DA_LINK_DEV1_DEV2 = compose_link(DA_DEVICE_DEV1_ENDPOINTS[0], DA_DEVICE_DEV2_ENDPOINTS[0])
DA_LINK_DEV1_DEV3_ID, DA_LINK_DEV1_DEV3 = compose_link(DA_DEVICE_DEV1_ENDPOINTS[1], DA_DEVICE_DEV3_ENDPOINTS[0])
DA_LINK_DEV2_DEV3_ID, DA_LINK_DEV2_DEV3 = compose_link(DA_DEVICE_DEV2_ENDPOINTS[1], DA_DEVICE_DEV3_ENDPOINTS[1])

# ----- Containers -----------------------------------------------------------------------------------------------------
DA_CONTEXTS   = [DA_CONTEXT_ADMIN]
DA_TOPOLOGIES = [DA_TOPOLOGY_ADMIN]
DA_DEVICES    = [DA_DEVICE_DEV1, DA_DEVICE_DEV2, DA_DEVICE_DEV3]
DA_LINKS      = [DA_LINK_DEV1_DEV2, DA_LINK_DEV1_DEV3, DA_LINK_DEV2_DEV3]


# ===== Domain B =======================================================================================================

# ----- Context --------------------------------------------------------------------------------------------------------
DB_CONTEXT_ADMIN_ID = json_context_id('B')
DB_CONTEXT_ADMIN    = json_context('B')

# ----- Topology -------------------------------------------------------------------------------------------------------
DB_TOPOLOGY_ADMIN_ID = json_topology_id('B', context_id=DB_CONTEXT_ADMIN_ID)
DB_TOPOLOGY_ADMIN    = json_topology('B', context_id=DB_CONTEXT_ADMIN_ID)

# ----- Devices --------------------------------------------------------------------------------------------------------
DB_DEVICE_DEV1_ID, DB_DEVICE_DEV1_ENDPOINTS, DB_DEVICE_DEV1 = compose_device('DEV1@B', ['1', '2'])
DB_DEVICE_DEV2_ID, DB_DEVICE_DEV2_ENDPOINTS, DB_DEVICE_DEV2 = compose_device('DEV2@B', ['1', '2'])
DB_DEVICE_DEV3_ID, DB_DEVICE_DEV3_ENDPOINTS, DB_DEVICE_DEV3 = compose_device('DEV3@B', ['1', '2'])

# ----- Links ----------------------------------------------------------------------------------------------------------
DB_LINK_DEV1_DEV2_ID, DB_LINK_DEV1_DEV2 = compose_link(DB_DEVICE_DEV1_ENDPOINTS[0], DB_DEVICE_DEV2_ENDPOINTS[0])
DB_LINK_DEV1_DEV3_ID, DB_LINK_DEV1_DEV3 = compose_link(DB_DEVICE_DEV1_ENDPOINTS[1], DB_DEVICE_DEV3_ENDPOINTS[0])
DB_LINK_DEV2_DEV3_ID, DB_LINK_DEV2_DEV3 = compose_link(DB_DEVICE_DEV2_ENDPOINTS[1], DB_DEVICE_DEV3_ENDPOINTS[1])

# ----- Containers -----------------------------------------------------------------------------------------------------
DB_CONTEXTS   = [DB_CONTEXT_ADMIN]
DB_TOPOLOGIES = [DB_TOPOLOGY_ADMIN]
DB_DEVICES    = [DB_DEVICE_DEV1, DB_DEVICE_DEV2, DB_DEVICE_DEV3]
DB_LINKS      = [DB_LINK_DEV1_DEV2, DB_LINK_DEV1_DEV3, DB_LINK_DEV2_DEV3]
