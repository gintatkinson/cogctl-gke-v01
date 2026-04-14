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

from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.tools.object_factory.Constraint import json_constraint_sla_capacity, json_constraint_sla_latency
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import json_device_emulated_packet_router_disabled, json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_descriptor, json_endpoints
from common.tools.object_factory.Link import get_link_uuid, json_link, json_link_id
from common.tools.object_factory.Service import get_service_uuid, json_service_l3nm_planned
from common.tools.object_factory.Topology import json_topology, json_topology_id

def compose_device(device_uuid, endpoint_uuids, topology_id=None):
    device_id = json_device_id(device_uuid)
    endpoints = [json_endpoint_descriptor(endpoint_uuid, 'copper', []) for endpoint_uuid in endpoint_uuids]
    endpoints = json_endpoints(device_id, endpoints, topology_id=topology_id)
    device = json_device_emulated_packet_router_disabled(device_uuid, endpoints=endpoints)
    return device_id, endpoints, device

def compose_link(endpoint_a, endpoint_z):
    link_uuid = get_link_uuid(endpoint_a['endpoint_id'], endpoint_z['endpoint_id'])
    link_id   = json_link_id(link_uuid)
    link      = json_link(link_uuid, [endpoint_a['endpoint_id'], endpoint_z['endpoint_id']])
    return link_id, link

def compose_service(endpoint_a, endpoint_z, constraints=[]):
    service_uuid = get_service_uuid(endpoint_a['endpoint_id'], endpoint_z['endpoint_id'])
    endpoint_ids = [endpoint_a['endpoint_id'], endpoint_z['endpoint_id']]
    service = json_service_l3nm_planned(service_uuid, endpoint_ids=endpoint_ids, constraints=constraints)
    return service

# ----- Context --------------------------------------------------------------------------------------------------------
CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
CONTEXT    = json_context(DEFAULT_CONTEXT_NAME)

# ----- Domains --------------------------------------------------------------------------------------------------------
TOPOLOGY_ADMIN_UUID = DEFAULT_TOPOLOGY_NAME
TOPOLOGY_ADMIN_ID   = json_topology_id(TOPOLOGY_ADMIN_UUID, context_id=CONTEXT_ID)
TOPOLOGY_ADMIN      = json_topology(TOPOLOGY_ADMIN_UUID, context_id=CONTEXT_ID)

TOPOLOGY_A_UUID = 'A'
TOPOLOGY_A_ID   = json_topology_id(TOPOLOGY_A_UUID, context_id=CONTEXT_ID)
TOPOLOGY_A      = json_topology(TOPOLOGY_A_UUID, context_id=CONTEXT_ID)

TOPOLOGY_B_UUID = 'B'
TOPOLOGY_B_ID   = json_topology_id(TOPOLOGY_B_UUID, context_id=CONTEXT_ID)
TOPOLOGY_B      = json_topology(TOPOLOGY_B_UUID, context_id=CONTEXT_ID)

TOPOLOGY_C_UUID = 'C'
TOPOLOGY_C_ID   = json_topology_id(TOPOLOGY_C_UUID, context_id=CONTEXT_ID)
TOPOLOGY_C      = json_topology(TOPOLOGY_C_UUID, context_id=CONTEXT_ID)

# ----- Devices Domain A -----------------------------------------------------------------------------------------------
DEVICE_A1_ID, DEVICE_A1_ENDPOINTS, DEVICE_A1 = compose_device('A1', ['1', '2', '2000'], topology_id=TOPOLOGY_A_ID)
DEVICE_A2_ID, DEVICE_A2_ENDPOINTS, DEVICE_A2 = compose_device('A2', ['1', '2', '1001'], topology_id=TOPOLOGY_A_ID)
DEVICE_A3_ID, DEVICE_A3_ENDPOINTS, DEVICE_A3 = compose_device('A3', ['1', '2'        ], topology_id=TOPOLOGY_A_ID)

# ----- Devices Domain B -----------------------------------------------------------------------------------------------
DEVICE_B1_ID, DEVICE_B1_ENDPOINTS, DEVICE_B1 = compose_device('B1', ['1', '2', '2000'], topology_id=TOPOLOGY_B_ID)
DEVICE_B2_ID, DEVICE_B2_ENDPOINTS, DEVICE_B2 = compose_device('B2', ['1', '2', '1002'], topology_id=TOPOLOGY_B_ID)
DEVICE_B3_ID, DEVICE_B3_ENDPOINTS, DEVICE_B3 = compose_device('B3', ['1', '2'        ], topology_id=TOPOLOGY_B_ID)

# ----- Devices Domain C -----------------------------------------------------------------------------------------------
DEVICE_C1_ID, DEVICE_C1_ENDPOINTS, DEVICE_C1 = compose_device('C1', ['1', '2', '1001'], topology_id=TOPOLOGY_C_ID)
DEVICE_C2_ID, DEVICE_C2_ENDPOINTS, DEVICE_C2 = compose_device('C2', ['1', '2'        ], topology_id=TOPOLOGY_C_ID)
DEVICE_C3_ID, DEVICE_C3_ENDPOINTS, DEVICE_C3 = compose_device('C3', ['1', '2', '1002'], topology_id=TOPOLOGY_C_ID)

# ----- InterDomain Links ----------------------------------------------------------------------------------------------
LINK_A2_C3_ID, LINK_A2_C3 = compose_link(DEVICE_A2_ENDPOINTS[2], DEVICE_C3_ENDPOINTS[2])
LINK_C1_B2_ID, LINK_C1_B2 = compose_link(DEVICE_C1_ENDPOINTS[2], DEVICE_B2_ENDPOINTS[2])

LINK_C3_A2_ID, LINK_C3_A2 = compose_link(DEVICE_C3_ENDPOINTS[2], DEVICE_A2_ENDPOINTS[2])
LINK_B2_C1_ID, LINK_B2_C1 = compose_link(DEVICE_B2_ENDPOINTS[2], DEVICE_C1_ENDPOINTS[2])

# ----- IntraDomain A Links --------------------------------------------------------------------------------------------
LINK_A1_A2_ID, LINK_A1_A2 = compose_link(DEVICE_A1_ENDPOINTS[0], DEVICE_A2_ENDPOINTS[0])
LINK_A1_A3_ID, LINK_A1_A3 = compose_link(DEVICE_A1_ENDPOINTS[1], DEVICE_A3_ENDPOINTS[0])
LINK_A2_A3_ID, LINK_A2_A3 = compose_link(DEVICE_A2_ENDPOINTS[1], DEVICE_A3_ENDPOINTS[1])

LINK_A2_A1_ID, LINK_A2_A1 = compose_link(DEVICE_A2_ENDPOINTS[0], DEVICE_A1_ENDPOINTS[0])
LINK_A3_A1_ID, LINK_A3_A1 = compose_link(DEVICE_A3_ENDPOINTS[0], DEVICE_A1_ENDPOINTS[1])
LINK_A3_A2_ID, LINK_A3_A2 = compose_link(DEVICE_A3_ENDPOINTS[1], DEVICE_A2_ENDPOINTS[1])

# ----- IntraDomain B Links --------------------------------------------------------------------------------------------
LINK_B1_B2_ID, LINK_B1_B2 = compose_link(DEVICE_B1_ENDPOINTS[0], DEVICE_B2_ENDPOINTS[0])
LINK_B1_B3_ID, LINK_B1_B3 = compose_link(DEVICE_B1_ENDPOINTS[1], DEVICE_B3_ENDPOINTS[0])
LINK_B2_B3_ID, LINK_B2_B3 = compose_link(DEVICE_B2_ENDPOINTS[1], DEVICE_B3_ENDPOINTS[1])

LINK_B2_B1_ID, LINK_B2_B1 = compose_link(DEVICE_B2_ENDPOINTS[0], DEVICE_B1_ENDPOINTS[0])
LINK_B3_B1_ID, LINK_B3_B1 = compose_link(DEVICE_B3_ENDPOINTS[0], DEVICE_B1_ENDPOINTS[1])
LINK_B3_B2_ID, LINK_B3_B2 = compose_link(DEVICE_B3_ENDPOINTS[1], DEVICE_B2_ENDPOINTS[1])

# ----- IntraDomain C Links --------------------------------------------------------------------------------------------
LINK_C1_C2_ID, LINK_C1_C2 = compose_link(DEVICE_C1_ENDPOINTS[0], DEVICE_C2_ENDPOINTS[0])
LINK_C1_C3_ID, LINK_C1_C3 = compose_link(DEVICE_C1_ENDPOINTS[1], DEVICE_C3_ENDPOINTS[0])
LINK_C2_C3_ID, LINK_C2_C3 = compose_link(DEVICE_C2_ENDPOINTS[1], DEVICE_C3_ENDPOINTS[1])

LINK_C2_C1_ID, LINK_C2_C1 = compose_link(DEVICE_C2_ENDPOINTS[0], DEVICE_C1_ENDPOINTS[0])
LINK_C3_C1_ID, LINK_C3_C1 = compose_link(DEVICE_C3_ENDPOINTS[0], DEVICE_C1_ENDPOINTS[1])
LINK_C3_C2_ID, LINK_C3_C2 = compose_link(DEVICE_C3_ENDPOINTS[1], DEVICE_C2_ENDPOINTS[1])

# ----- Service --------------------------------------------------------------------------------------------------------
SERVICE_A1_B1 = compose_service(DEVICE_A1_ENDPOINTS[2], DEVICE_B1_ENDPOINTS[2], constraints=[
    json_constraint_sla_capacity(10.0),
    json_constraint_sla_latency(12.0),
])

# ----- Containers -----------------------------------------------------------------------------------------------------
CONTEXTS   = [  CONTEXT]
TOPOLOGIES = [  TOPOLOGY_ADMIN, TOPOLOGY_A, TOPOLOGY_B, TOPOLOGY_C]
DEVICES    = [  DEVICE_A1, DEVICE_A2, DEVICE_A3,
                DEVICE_B1, DEVICE_B2, DEVICE_B3,
                DEVICE_C1, DEVICE_C2, DEVICE_C3,    ]
LINKS      = [  LINK_A2_C3, LINK_C1_B2,
                LINK_C3_A2, LINK_B2_C1,

                LINK_A1_A2, LINK_A1_A3, LINK_A2_A3,
                LINK_A2_A1, LINK_A3_A1, LINK_A3_A2,

                LINK_B1_B2, LINK_B1_B3, LINK_B2_B3,
                LINK_B2_B1, LINK_B3_B1, LINK_B3_B2,

                LINK_C1_C2, LINK_C1_C3, LINK_C2_C3,
                LINK_C2_C1, LINK_C3_C1, LINK_C3_C2, ]
SERVICES   = [  SERVICE_A1_B1]

#OBJECTS_PER_TOPOLOGY = [
#    (TOPOLOGY_ADMIN_ID,
#        [   DEVICE_A1_ID, DEVICE_A2_ID, DEVICE_A3_ID,
#            DEVICE_B1_ID, DEVICE_B2_ID, DEVICE_B3_ID,
#            DEVICE_C1_ID, DEVICE_C2_ID, DEVICE_C3_ID,       ],
#        [   LINK_A2_C3_ID, LINK_C1_B2_ID,
#            LINK_A1_A2_ID, LINK_A1_A3_ID, LINK_A2_A3_ID,
#            LINK_B1_B2_ID, LINK_B1_B3_ID, LINK_B2_B3_ID,
#            LINK_C1_C2_ID, LINK_C1_C3_ID, LINK_C2_C3_ID,    ],
#    ),
#    (TOPOLOGY_A_ID,
#        [   DEVICE_A1_ID, DEVICE_A2_ID, DEVICE_A3_ID,       ],
#        [   LINK_A1_A2_ID, LINK_A1_A3_ID, LINK_A2_A3_ID,    ],
#    ),
#    (TOPOLOGY_B_ID,
#        [   DEVICE_B1_ID, DEVICE_B2_ID, DEVICE_B3_ID,       ],
#        [   LINK_B1_B2_ID, LINK_B1_B3_ID, LINK_B2_B3_ID,    ],
#    ),
#    (TOPOLOGY_C_ID,
#        [   DEVICE_C1_ID, DEVICE_C2_ID, DEVICE_C3_ID,       ],
#        [   LINK_C1_C2_ID, LINK_C1_C3_ID, LINK_C2_C3_ID,    ],
#    ),
#]
