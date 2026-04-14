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

import uuid
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.tools.object_factory.Constraint import json_constraint_sla_capacity, json_constraint_sla_latency
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import (
    json_device_emulated_connect_rules, json_device_emulated_datacenter_disabled,
    json_device_emulated_packet_router_disabled, json_device_emulated_tapi_disabled,
    json_device_id)
from common.tools.object_factory.EndPoint import json_endpoint_descriptor, json_endpoints
from common.tools.object_factory.Link import get_link_uuid, json_link, json_link_id
from common.tools.object_factory.Service import get_service_uuid, json_service_l3nm_planned
from common.tools.object_factory.Topology import json_topology, json_topology_id

# if true, Device component is present and will infeer the endpoints from connect-rules
# if false, Device component is not present and device objects must contain preconfigured endpoints
ADD_CONNECT_RULES_TO_DEVICES = False

def compose_router(device_uuid, endpoint_uuids, topology_id=None):
    device_id = json_device_id(device_uuid)
    r_endpoints = [json_endpoint_descriptor(endpoint_uuid, 'copper') for endpoint_uuid in endpoint_uuids]
    config_rules = json_device_emulated_connect_rules(r_endpoints) if ADD_CONNECT_RULES_TO_DEVICES else []
    endpoints = json_endpoints(device_id, r_endpoints, topology_id=topology_id)
    j_endpoints = [] if ADD_CONNECT_RULES_TO_DEVICES else endpoints
    device = json_device_emulated_packet_router_disabled(device_uuid, config_rules=config_rules, endpoints=j_endpoints)
    return device_id, endpoints, device

def compose_ols(device_uuid, endpoint_uuids, topology_id=None):
    device_id = json_device_id(device_uuid)
    r_endpoints = [json_endpoint_descriptor(endpoint_uuid, 'optical') for endpoint_uuid in endpoint_uuids]
    config_rules = json_device_emulated_connect_rules(r_endpoints) if ADD_CONNECT_RULES_TO_DEVICES else []
    endpoints = json_endpoints(device_id, r_endpoints, topology_id=topology_id)
    j_endpoints = [] if ADD_CONNECT_RULES_TO_DEVICES else endpoints
    device = json_device_emulated_tapi_disabled(device_uuid, config_rules=config_rules, endpoints=j_endpoints)
    return device_id, endpoints, device

def compose_datacenter(device_uuid, endpoint_uuids, topology_id=None):
    device_id = json_device_id(device_uuid)
    r_endpoints = [json_endpoint_descriptor(endpoint_uuid, 'copper') for endpoint_uuid in endpoint_uuids]
    config_rules = json_device_emulated_connect_rules(r_endpoints) if ADD_CONNECT_RULES_TO_DEVICES else []
    endpoints = json_endpoints(device_id, r_endpoints, topology_id=topology_id)
    j_endpoints = [] if ADD_CONNECT_RULES_TO_DEVICES else endpoints
    device = json_device_emulated_datacenter_disabled(device_uuid, config_rules=config_rules, endpoints=j_endpoints)
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
# Overall network topology
TOPO_ADMIN_UUID = DEFAULT_TOPOLOGY_NAME
TOPO_ADMIN_ID   = json_topology_id(TOPO_ADMIN_UUID, context_id=CONTEXT_ID)
TOPO_ADMIN      = json_topology(TOPO_ADMIN_UUID, context_id=CONTEXT_ID)

# DataCenter #1 Network
TOPO_DC1_UUID = 'DC1'
TOPO_DC1_ID   = json_topology_id(TOPO_DC1_UUID, context_id=CONTEXT_ID)
TOPO_DC1      = json_topology(TOPO_DC1_UUID, context_id=CONTEXT_ID)

# DataCenter #2 Network
TOPO_DC2_UUID = 'DC2'
TOPO_DC2_ID   = json_topology_id(TOPO_DC2_UUID, context_id=CONTEXT_ID)
TOPO_DC2      = json_topology(TOPO_DC2_UUID, context_id=CONTEXT_ID)

# CellSite #1 Network
TOPO_CS1_UUID = 'CS1'
TOPO_CS1_ID   = json_topology_id(TOPO_CS1_UUID, context_id=CONTEXT_ID)
TOPO_CS1      = json_topology(TOPO_CS1_UUID, context_id=CONTEXT_ID)

# CellSite #2 Network
TOPO_CS2_UUID = 'CS2'
TOPO_CS2_ID   = json_topology_id(TOPO_CS2_UUID, context_id=CONTEXT_ID)
TOPO_CS2      = json_topology(TOPO_CS2_UUID, context_id=CONTEXT_ID)

# Transport Network Network
TOPO_TN_UUID = 'TN'
TOPO_TN_ID   = json_topology_id(TOPO_TN_UUID, context_id=CONTEXT_ID)
TOPO_TN      = json_topology(TOPO_TN_UUID, context_id=CONTEXT_ID)


# ----- Devices --------------------------------------------------------------------------------------------------------
# DataCenters
DEV_DC1GW_ID, DEV_DC1GW_EPS, DEV_DC1GW = compose_datacenter('DC1-GW', ['eth1', 'eth2', 'int'])
DEV_DC2GW_ID, DEV_DC2GW_EPS, DEV_DC2GW = compose_datacenter('DC2-GW', ['eth1', 'eth2', 'int'])

# CellSites
DEV_CS1GW1_ID, DEV_CS1GW1_EPS, DEV_CS1GW1 = compose_router('CS1-GW1', ['10/1', '1/1', '1/2'])
DEV_CS1GW2_ID, DEV_CS1GW2_EPS, DEV_CS1GW2 = compose_router('CS1-GW2', ['10/1', '1/1', '1/2'])
DEV_CS2GW1_ID, DEV_CS2GW1_EPS, DEV_CS2GW1 = compose_router('CS2-GW1', ['10/1', '1/1', '1/2'])
DEV_CS2GW2_ID, DEV_CS2GW2_EPS, DEV_CS2GW2 = compose_router('CS2-GW2', ['10/1', '1/1', '1/2'])

# Transport Network
DEV_TNR1_ID, DEV_TNR1_EPS, DEV_TNR1 = compose_router('TN-R1', ['1/1', '1/2', '2/1'])
DEV_TNR2_ID, DEV_TNR2_EPS, DEV_TNR2 = compose_router('TN-R2', ['1/1', '1/2', '2/1'])
DEV_TNR3_ID, DEV_TNR3_EPS, DEV_TNR3 = compose_router('TN-R3', ['1/1', '1/2', '2/1'])
DEV_TNR4_ID, DEV_TNR4_EPS, DEV_TNR4 = compose_router('TN-R4', ['1/1', '1/2', '2/1'])
tols_ep_uuids = [str(uuid.uuid4()).split('-')[-1] for _ in range(4)]
DEV_TOLS_ID, DEV_TOLS_EPS, DEV_TOLS = compose_ols('TN-OLS', tols_ep_uuids)


# ----- Links ----------------------------------------------------------------------------------------------------------
# InterDomain DC-CSGW
LINK_DC1GW_CS1GW1_ID, LINK_DC1GW_CS1GW1 = compose_link(DEV_DC1GW_EPS[0], DEV_CS1GW1_EPS[0])
LINK_DC1GW_CS1GW2_ID, LINK_DC1GW_CS1GW2 = compose_link(DEV_DC1GW_EPS[1], DEV_CS1GW2_EPS[0])
LINK_DC2GW_CS2GW1_ID, LINK_DC2GW_CS2GW1 = compose_link(DEV_DC2GW_EPS[0], DEV_CS2GW1_EPS[0])
LINK_DC2GW_CS2GW2_ID, LINK_DC2GW_CS2GW2 = compose_link(DEV_DC2GW_EPS[1], DEV_CS2GW2_EPS[0])

LINK_CS1GW1_DC1GW_ID, LINK_CS1GW1_DC1GW = compose_link(DEV_CS1GW1_EPS[0], DEV_DC1GW_EPS[0])
LINK_CS1GW2_DC1GW_ID, LINK_CS1GW2_DC1GW = compose_link(DEV_CS1GW2_EPS[0], DEV_DC1GW_EPS[1])
LINK_CS2GW1_DC2GW_ID, LINK_CS2GW1_DC2GW = compose_link(DEV_CS2GW1_EPS[0], DEV_DC2GW_EPS[0])
LINK_CS2GW2_DC2GW_ID, LINK_CS2GW2_DC2GW = compose_link(DEV_CS2GW2_EPS[0], DEV_DC2GW_EPS[1])

# InterDomain CSGW-TN
LINK_CS1GW1_TNR1_ID, LINK_CS1GW1_TNR1 = compose_link(DEV_CS1GW1_EPS[1], DEV_TNR1_EPS[0])
LINK_CS1GW2_TNR2_ID, LINK_CS1GW2_TNR2 = compose_link(DEV_CS1GW2_EPS[1], DEV_TNR2_EPS[0])
LINK_CS1GW1_TNR2_ID, LINK_CS1GW1_TNR2 = compose_link(DEV_CS1GW1_EPS[2], DEV_TNR2_EPS[1])
LINK_CS1GW2_TNR1_ID, LINK_CS1GW2_TNR1 = compose_link(DEV_CS1GW2_EPS[2], DEV_TNR1_EPS[1])
LINK_CS2GW1_TNR3_ID, LINK_CS2GW1_TNR3 = compose_link(DEV_CS2GW1_EPS[1], DEV_TNR3_EPS[0])
LINK_CS2GW2_TNR4_ID, LINK_CS2GW2_TNR4 = compose_link(DEV_CS2GW2_EPS[1], DEV_TNR4_EPS[0])
LINK_CS2GW1_TNR4_ID, LINK_CS2GW1_TNR4 = compose_link(DEV_CS2GW1_EPS[2], DEV_TNR4_EPS[1])
LINK_CS2GW2_TNR3_ID, LINK_CS2GW2_TNR3 = compose_link(DEV_CS2GW2_EPS[2], DEV_TNR3_EPS[1])

LINK_TNR1_CS1GW1_ID, LINK_TNR1_CS1GW1 = compose_link(DEV_TNR1_EPS[0], DEV_CS1GW1_EPS[1])
LINK_TNR2_CS1GW2_ID, LINK_TNR2_CS1GW2 = compose_link(DEV_TNR2_EPS[0], DEV_CS1GW2_EPS[1])
LINK_TNR2_CS1GW1_ID, LINK_TNR2_CS1GW1 = compose_link(DEV_TNR2_EPS[1], DEV_CS1GW1_EPS[2])
LINK_TNR1_CS1GW2_ID, LINK_TNR1_CS1GW2 = compose_link(DEV_TNR1_EPS[1], DEV_CS1GW2_EPS[2])
LINK_TNR3_CS2GW1_ID, LINK_TNR3_CS2GW1 = compose_link(DEV_TNR3_EPS[0], DEV_CS2GW1_EPS[1])
LINK_TNR4_CS2GW2_ID, LINK_TNR4_CS2GW2 = compose_link(DEV_TNR4_EPS[0], DEV_CS2GW2_EPS[1])
LINK_TNR4_CS2GW1_ID, LINK_TNR4_CS2GW1 = compose_link(DEV_TNR4_EPS[1], DEV_CS2GW1_EPS[2])
LINK_TNR3_CS2GW2_ID, LINK_TNR3_CS2GW2 = compose_link(DEV_TNR3_EPS[1], DEV_CS2GW2_EPS[2])

# IntraDomain TN
LINK_TNR1_TOLS_ID, LINK_TNR1_TOLS = compose_link(DEV_TNR1_EPS[2], DEV_TOLS_EPS[0])
LINK_TNR2_TOLS_ID, LINK_TNR2_TOLS = compose_link(DEV_TNR2_EPS[2], DEV_TOLS_EPS[1])
LINK_TNR3_TOLS_ID, LINK_TNR3_TOLS = compose_link(DEV_TNR3_EPS[2], DEV_TOLS_EPS[2])
LINK_TNR4_TOLS_ID, LINK_TNR4_TOLS = compose_link(DEV_TNR4_EPS[2], DEV_TOLS_EPS[3])

LINK_TOLS_TNR1_ID, LINK_TOLS_TNR1 = compose_link(DEV_TOLS_EPS[0], DEV_TNR1_EPS[2])
LINK_TOLS_TNR2_ID, LINK_TOLS_TNR2 = compose_link(DEV_TOLS_EPS[1], DEV_TNR2_EPS[2])
LINK_TOLS_TNR3_ID, LINK_TOLS_TNR3 = compose_link(DEV_TOLS_EPS[2], DEV_TNR3_EPS[2])
LINK_TOLS_TNR4_ID, LINK_TOLS_TNR4 = compose_link(DEV_TOLS_EPS[3], DEV_TNR4_EPS[2])


# ----- Service --------------------------------------------------------------------------------------------------------
SERVICE_DC1GW_DC2GW = compose_service(DEV_DC1GW_EPS[2], DEV_DC2GW_EPS[2], constraints=[
    json_constraint_sla_capacity(10.0),
    json_constraint_sla_latency(20.0),
])

# ----- Containers -----------------------------------------------------------------------------------------------------
CONTEXTS   = [  CONTEXT ]
TOPOLOGIES = [  TOPO_ADMIN, TOPO_DC1, TOPO_DC2, TOPO_CS1, TOPO_CS2, TOPO_TN ]
DEVICES    = [  DEV_DC1GW, DEV_DC2GW,
                DEV_CS1GW1, DEV_CS1GW2, DEV_CS2GW1, DEV_CS2GW2,
                DEV_TNR1, DEV_TNR2, DEV_TNR3, DEV_TNR4,
                DEV_TOLS,
            ]
LINKS      = [  LINK_DC1GW_CS1GW1, LINK_DC1GW_CS1GW2, LINK_DC2GW_CS2GW1, LINK_DC2GW_CS2GW2,
                LINK_CS1GW1_DC1GW, LINK_CS1GW2_DC1GW, LINK_CS2GW1_DC2GW, LINK_CS2GW2_DC2GW,

                LINK_CS1GW1_TNR1, LINK_CS1GW2_TNR2, LINK_CS1GW1_TNR2, LINK_CS1GW2_TNR1,
                LINK_CS2GW1_TNR3, LINK_CS2GW2_TNR4, LINK_CS2GW1_TNR4, LINK_CS2GW2_TNR3,
                LINK_TNR1_CS1GW1, LINK_TNR2_CS1GW2, LINK_TNR2_CS1GW1, LINK_TNR1_CS1GW2,
                LINK_TNR3_CS2GW1, LINK_TNR4_CS2GW2, LINK_TNR4_CS2GW1, LINK_TNR3_CS2GW2,

                LINK_TNR1_TOLS, LINK_TNR2_TOLS, LINK_TNR3_TOLS, LINK_TNR4_TOLS,
                LINK_TOLS_TNR1, LINK_TOLS_TNR2, LINK_TOLS_TNR3, LINK_TOLS_TNR4,
            ]
SERVICES   = [  SERVICE_DC1GW_DC2GW   ]

#OBJECTS_PER_TOPOLOGY = [
#    (TOPO_ADMIN_ID,
#        [   DEV_DC1GW_ID, DEV_DC2GW_ID,
#            DEV_CS1GW1_ID, DEV_CS1GW2_ID, DEV_CS2GW1_ID, DEV_CS2GW2_ID,
#            DEV_TNR1_ID, DEV_TNR2_ID, DEV_TNR3_ID, DEV_TNR4_ID,
#            DEV_TOLS_ID,
#        ],
#        [   LINK_DC1GW_CS1GW1_ID, LINK_DC1GW_CS1GW2_ID, LINK_DC2GW_CS2GW1_ID, LINK_DC2GW_CS2GW2_ID,
#            LINK_CS1GW1_TNR1_ID, LINK_CS1GW2_TNR2_ID, LINK_CS1GW1_TNR2_ID, LINK_CS1GW2_TNR1_ID,
#            LINK_CS2GW1_TNR3_ID, LINK_CS2GW2_TNR4_ID, LINK_CS2GW1_TNR4_ID, LINK_CS2GW2_TNR3_ID,
#            LINK_TNR1_TOLS_ID, LINK_TNR2_TOLS_ID, LINK_TNR3_TOLS_ID, LINK_TNR4_TOLS_ID,
#        ],
#    ),
#    (TOPO_DC1_ID,
#        [DEV_DC1GW_ID],
#        []),
#    (TOPO_DC2_ID,
#        [DEV_DC2GW_ID],
#        []),
#    (TOPO_CS1_ID,
#        [DEV_CS1GW1_ID, DEV_CS1GW2_ID],
#        []),
#    (TOPO_CS2_ID,
#        [DEV_CS2GW1_ID, DEV_CS2GW2_ID],
#        []),
#    (TOPO_TN_ID,
#        [   DEV_TNR1_ID, DEV_TNR2_ID, DEV_TNR3_ID, DEV_TNR4_ID,
#            DEV_TOLS_ID,
#        ],
#        [   LINK_TNR1_TOLS_ID, LINK_TNR2_TOLS_ID, LINK_TNR3_TOLS_ID, LINK_TNR4_TOLS_ID,
#        ]),
#]
