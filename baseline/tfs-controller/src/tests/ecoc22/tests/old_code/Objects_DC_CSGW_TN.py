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

import os
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import (
    json_device_emulated_connect_rules, json_device_emulated_datacenter_disabled,
    json_device_emulated_packet_router_disabled, json_device_id)
from common.tools.object_factory.EndPoint import json_endpoint_descriptor, json_endpoints
from common.tools.object_factory.Link import get_link_uuid, json_link, json_link_id
from common.tools.object_factory.Service import get_service_uuid, json_service_l3nm_planned
from common.tools.object_factory.Topology import json_topology, json_topology_id

# if true, Device component is present and will infeer the endpoints from connect-rules
# if false, Device component is not present and device objects must contain preconfigured endpoints
ADD_CONNECT_RULES_TO_DEVICES = os.environ.get('ADD_CONNECT_RULES_TO_DEVICES', 'True')
ADD_CONNECT_RULES_TO_DEVICES = ADD_CONNECT_RULES_TO_DEVICES.upper() in {'T', 'TRUE', '1', 'Y', 'YES'}

def compose_router(device_uuid, endpoint_uuids, topology_id=None):
    device_id = json_device_id(device_uuid)
    r_endpoints = [json_endpoint_descriptor(endpoint_uuid, 'copper') for endpoint_uuid in endpoint_uuids]
    config_rules = json_device_emulated_connect_rules(r_endpoints) if ADD_CONNECT_RULES_TO_DEVICES else []
    endpoints = json_endpoints(device_id, r_endpoints, topology_id=topology_id)
    j_endpoints = [] if ADD_CONNECT_RULES_TO_DEVICES else endpoints
    device = json_device_emulated_packet_router_disabled(device_uuid, config_rules=config_rules, endpoints=j_endpoints)
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
DEV_TNR1_ID, DEV_TNR1_EPS, DEV_TNR1 = compose_router('TN-R1', ['1/1', '1/2', '2/1', '2/2', '2/3'])
DEV_TNR2_ID, DEV_TNR2_EPS, DEV_TNR2 = compose_router('TN-R2', ['1/1', '1/2', '2/1', '2/2', '2/3'])
DEV_TNR3_ID, DEV_TNR3_EPS, DEV_TNR3 = compose_router('TN-R3', ['1/1', '1/2', '2/1', '2/2', '2/3'])
DEV_TNR4_ID, DEV_TNR4_EPS, DEV_TNR4 = compose_router('TN-R4', ['1/1', '1/2', '2/1', '2/2', '2/3'])


# ----- Links ----------------------------------------------------------------------------------------------------------
# InterDomain DC-CSGW
LINK_DC1GW_CS1GW1_ID, LINK_DC1GW_CS1GW1 = compose_link(DEV_DC1GW_EPS[0], DEV_CS1GW1_EPS[0])
LINK_DC1GW_CS1GW2_ID, LINK_DC1GW_CS1GW2 = compose_link(DEV_DC1GW_EPS[1], DEV_CS1GW2_EPS[0])
LINK_DC2GW_CS2GW1_ID, LINK_DC2GW_CS2GW1 = compose_link(DEV_DC2GW_EPS[0], DEV_CS2GW1_EPS[0])
LINK_DC2GW_CS2GW2_ID, LINK_DC2GW_CS2GW2 = compose_link(DEV_DC2GW_EPS[1], DEV_CS2GW2_EPS[0])

# InterDomain CSGW-TN
LINK_CS1GW1_TNR1_ID, LINK_CS1GW1_TNR1 = compose_link(DEV_CS1GW1_EPS[1], DEV_TNR1_EPS[0])
LINK_CS1GW2_TNR2_ID, LINK_CS1GW2_TNR2 = compose_link(DEV_CS1GW2_EPS[1], DEV_TNR2_EPS[0])
LINK_CS1GW1_TNR2_ID, LINK_CS1GW1_TNR2 = compose_link(DEV_CS1GW1_EPS[2], DEV_TNR2_EPS[1])
LINK_CS1GW2_TNR1_ID, LINK_CS1GW2_TNR1 = compose_link(DEV_CS1GW2_EPS[2], DEV_TNR1_EPS[1])
LINK_CS2GW1_TNR3_ID, LINK_CS2GW1_TNR3 = compose_link(DEV_CS2GW1_EPS[1], DEV_TNR3_EPS[0])
LINK_CS2GW2_TNR4_ID, LINK_CS2GW2_TNR4 = compose_link(DEV_CS2GW2_EPS[1], DEV_TNR4_EPS[0])
LINK_CS2GW1_TNR4_ID, LINK_CS2GW1_TNR4 = compose_link(DEV_CS2GW1_EPS[2], DEV_TNR4_EPS[1])
LINK_CS2GW2_TNR3_ID, LINK_CS2GW2_TNR3 = compose_link(DEV_CS2GW2_EPS[2], DEV_TNR3_EPS[1])

# IntraDomain TN
LINK_TNR1_TNR2_ID, LINK_TNR1_TNR2 = compose_link(DEV_TNR1_EPS[2], DEV_TNR2_EPS[3])
LINK_TNR2_TNR3_ID, LINK_TNR2_TNR3 = compose_link(DEV_TNR2_EPS[2], DEV_TNR3_EPS[3])
LINK_TNR3_TNR4_ID, LINK_TNR3_TNR4 = compose_link(DEV_TNR3_EPS[2], DEV_TNR4_EPS[3])
LINK_TNR4_TNR1_ID, LINK_TNR4_TNR1 = compose_link(DEV_TNR4_EPS[2], DEV_TNR1_EPS[3])
LINK_TNR1_TNR3_ID, LINK_TNR1_TNR3 = compose_link(DEV_TNR1_EPS[4], DEV_TNR3_EPS[4])
LINK_TNR2_TNR4_ID, LINK_TNR2_TNR4 = compose_link(DEV_TNR2_EPS[4], DEV_TNR4_EPS[4])


# ----- WIM Service Settings -------------------------------------------------------------------------------------------
WIM_USERNAME = 'admin'
WIM_PASSWORD = 'admin'

def mapping(site_id, ce_endpoint_id, pe_device_id, priority=None, redundant=[]):
    ce_endpoint_id = ce_endpoint_id['endpoint_id']
    ce_device_uuid = ce_endpoint_id['device_id']['device_uuid']['uuid']
    ce_endpoint_uuid = ce_endpoint_id['endpoint_uuid']['uuid']
    pe_device_uuid = pe_device_id['device_uuid']['uuid']
    service_endpoint_id = '{:s}:{:s}:{:s}'.format(site_id, ce_device_uuid, ce_endpoint_uuid)
    bearer = '{:s}:{:s}'.format(ce_device_uuid, pe_device_uuid)
    _mapping = {
        'service_endpoint_id': service_endpoint_id,
        'datacenter_id': site_id, 'device_id': ce_device_uuid, 'device_interface_id': ce_endpoint_uuid,
        'service_mapping_info': {
            'site-id': site_id,
            'bearer': {'bearer-reference': bearer},
        }
    }
    if priority is not None: _mapping['service_mapping_info']['priority'] = priority
    if len(redundant) > 0: _mapping['service_mapping_info']['redundant'] = redundant
    return service_endpoint_id, _mapping

WIM_SEP_DC1_PRI, WIM_MAP_DC1_PRI = mapping('DC1', DEV_DC1GW_EPS[0], DEV_CS1GW1_ID, priority=10, redundant=['DC1:DC1-GW:eth2'])
WIM_SEP_DC1_SEC, WIM_MAP_DC1_SEC = mapping('DC1', DEV_DC1GW_EPS[1], DEV_CS1GW2_ID, priority=20, redundant=['DC1:DC1-GW:eth1'])
WIM_SEP_DC2_PRI, WIM_MAP_DC2_PRI = mapping('DC2', DEV_DC2GW_EPS[0], DEV_CS2GW1_ID, priority=10, redundant=['DC2:DC2-GW:eth2'])
WIM_SEP_DC2_SEC, WIM_MAP_DC2_SEC = mapping('DC2', DEV_DC2GW_EPS[1], DEV_CS2GW2_ID, priority=20, redundant=['DC2:DC2-GW:eth1'])

WIM_MAPPING  = [WIM_MAP_DC1_PRI, WIM_MAP_DC1_SEC, WIM_MAP_DC2_PRI, WIM_MAP_DC2_SEC]

WIM_SRV_VLAN_ID = 300
WIM_SERVICE_TYPE = 'ELAN'
WIM_SERVICE_CONNECTION_POINTS = [
    {'service_endpoint_id': WIM_SEP_DC1_PRI,
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': WIM_SRV_VLAN_ID}},
    {'service_endpoint_id': WIM_SEP_DC2_PRI,
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': WIM_SRV_VLAN_ID}},
]


# ----- Containers -----------------------------------------------------------------------------------------------------
CONTEXTS   = [  CONTEXT ]
TOPOLOGIES = [  TOPO_ADMIN, TOPO_DC1, TOPO_DC2, TOPO_CS1, TOPO_CS2, TOPO_TN ]
DEVICES    = [  DEV_DC1GW, DEV_DC2GW,
                DEV_CS1GW1, DEV_CS1GW2, DEV_CS2GW1, DEV_CS2GW2,
                DEV_TNR1, DEV_TNR2, DEV_TNR3, DEV_TNR4,
            ]
LINKS      = [  LINK_DC1GW_CS1GW1, LINK_DC1GW_CS1GW2, LINK_DC2GW_CS2GW1, LINK_DC2GW_CS2GW2,
                LINK_CS1GW1_TNR1, LINK_CS1GW2_TNR2, LINK_CS1GW1_TNR2, LINK_CS1GW2_TNR1,
                LINK_CS2GW1_TNR3, LINK_CS2GW2_TNR4, LINK_CS2GW1_TNR4, LINK_CS2GW2_TNR3,
                LINK_TNR1_TNR2, LINK_TNR2_TNR3, LINK_TNR3_TNR4, LINK_TNR4_TNR1, LINK_TNR1_TNR3, LINK_TNR2_TNR4,
            ]

OBJECTS_PER_TOPOLOGY = [
    (TOPO_ADMIN_ID,
        [   DEV_DC1GW_ID, DEV_DC2GW_ID,
            DEV_CS1GW1_ID, DEV_CS1GW2_ID, DEV_CS2GW1_ID, DEV_CS2GW2_ID,
            DEV_TNR1_ID, DEV_TNR2_ID, DEV_TNR3_ID, DEV_TNR4_ID,
        ],
        [   LINK_DC1GW_CS1GW1_ID, LINK_DC1GW_CS1GW2_ID, LINK_DC2GW_CS2GW1_ID, LINK_DC2GW_CS2GW2_ID,
            LINK_CS1GW1_TNR1_ID, LINK_CS1GW2_TNR2_ID, LINK_CS1GW1_TNR2_ID, LINK_CS1GW2_TNR1_ID,
            LINK_CS2GW1_TNR3_ID, LINK_CS2GW2_TNR4_ID, LINK_CS2GW1_TNR4_ID, LINK_CS2GW2_TNR3_ID,
            LINK_TNR1_TNR2_ID, LINK_TNR2_TNR3_ID, LINK_TNR3_TNR4_ID, LINK_TNR4_TNR1_ID, LINK_TNR1_TNR3_ID,
            LINK_TNR2_TNR4_ID,
        ],
    ),
    (TOPO_DC1_ID,
        [DEV_DC1GW_ID],
        []),
    (TOPO_DC2_ID,
        [DEV_DC2GW_ID],
        []),
    (TOPO_CS1_ID,
        [DEV_CS1GW1_ID, DEV_CS1GW2_ID],
        []),
    (TOPO_CS2_ID,
        [DEV_CS2GW1_ID, DEV_CS2GW2_ID],
        []),
    (TOPO_TN_ID,
        [   DEV_TNR1_ID, DEV_TNR2_ID, DEV_TNR3_ID, DEV_TNR4_ID,
        ],
        [   LINK_TNR1_TNR2_ID, LINK_TNR2_TNR3_ID, LINK_TNR3_TNR4_ID, LINK_TNR4_TNR1_ID, LINK_TNR1_TNR3_ID,
            LINK_TNR2_TNR4_ID,
        ]),
]
