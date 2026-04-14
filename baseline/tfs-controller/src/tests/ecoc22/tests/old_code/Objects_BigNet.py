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
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import (
    json_device_emulated_connect_rules, json_device_emulated_datacenter_disabled,
    json_device_emulated_packet_router_disabled, json_device_id)
from common.tools.object_factory.EndPoint import json_endpoint_descriptor
from common.tools.object_factory.Topology import json_topology, json_topology_id
from .Tools import compose_bearer, compose_service_endpoint_id, json_endpoint_ids, link

# ----- Context --------------------------------------------------------------------------------------------------------
CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
CONTEXT    = json_context(DEFAULT_CONTEXT_NAME)


# ----- Topology -------------------------------------------------------------------------------------------------------
TOPOLOGY_ID = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)
TOPOLOGY    = json_topology(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)


# ----- Customer Equipment (CE) Devices --------------------------------------------------------------------------------
DEVICE_CE1_UUID          = 'CE1'
DEVICE_CE1_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper')]
DEVICE_CE1_ID            = json_device_id(DEVICE_CE1_UUID)
DEVICE_CE1_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_CE1_ID, DEVICE_CE1_ENDPOINT_DEFS)
DEVICE_CE1               = json_device_emulated_packet_router_disabled(DEVICE_CE1_UUID)
ENDPOINT_ID_CE1_1_1      = DEVICE_CE1_ENDPOINT_IDS[0]
DEVICE_CE1_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_CE1_ENDPOINT_DEFS)

DEVICE_CE2_UUID          = 'CE2'
DEVICE_CE2_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper')]
DEVICE_CE2_ID            = json_device_id(DEVICE_CE2_UUID)
DEVICE_CE2_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_CE2_ID, DEVICE_CE2_ENDPOINT_DEFS)
DEVICE_CE2               = json_device_emulated_packet_router_disabled(DEVICE_CE2_UUID)
ENDPOINT_ID_CE2_1_1      = DEVICE_CE2_ENDPOINT_IDS[0]
DEVICE_CE2_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_CE2_ENDPOINT_DEFS)

DEVICE_CE3_UUID          = 'CE3'
DEVICE_CE3_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper')]
DEVICE_CE3_ID            = json_device_id(DEVICE_CE3_UUID)
DEVICE_CE3_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_CE3_ID, DEVICE_CE3_ENDPOINT_DEFS)
DEVICE_CE3               = json_device_emulated_packet_router_disabled(DEVICE_CE3_UUID)
ENDPOINT_ID_CE3_1_1      = DEVICE_CE3_ENDPOINT_IDS[0]
DEVICE_CE3_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_CE3_ENDPOINT_DEFS)

DEVICE_CE4_UUID          = 'CE4'
DEVICE_CE4_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper')]
DEVICE_CE4_ID            = json_device_id(DEVICE_CE4_UUID)
DEVICE_CE4_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_CE4_ID, DEVICE_CE4_ENDPOINT_DEFS)
DEVICE_CE4               = json_device_emulated_packet_router_disabled(DEVICE_CE4_UUID)
ENDPOINT_ID_CE4_1_1      = DEVICE_CE4_ENDPOINT_IDS[0]
DEVICE_CE4_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_CE4_ENDPOINT_DEFS)

# ----- Provider Equipment (PE) Devices --------------------------------------------------------------------------------
DEVICE_PE1_UUID          = 'PE1'
DEVICE_PE1_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper')]
DEVICE_PE1_ID            = json_device_id(DEVICE_PE1_UUID)
DEVICE_PE1_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_PE1_ID, DEVICE_PE1_ENDPOINT_DEFS)
DEVICE_PE1               = json_device_emulated_packet_router_disabled(DEVICE_PE1_UUID)
ENDPOINT_ID_PE1_1_1      = DEVICE_PE1_ENDPOINT_IDS[0]
ENDPOINT_ID_PE1_2_1      = DEVICE_PE1_ENDPOINT_IDS[1]
ENDPOINT_ID_PE1_2_2      = DEVICE_PE1_ENDPOINT_IDS[2]
DEVICE_PE1_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_PE1_ENDPOINT_DEFS)

DEVICE_PE2_UUID          = 'PE2'
DEVICE_PE2_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper')]
DEVICE_PE2_ID            = json_device_id(DEVICE_PE2_UUID)
DEVICE_PE2_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_PE2_ID, DEVICE_PE2_ENDPOINT_DEFS)
DEVICE_PE2               = json_device_emulated_packet_router_disabled(DEVICE_PE2_UUID)
ENDPOINT_ID_PE2_1_1      = DEVICE_PE2_ENDPOINT_IDS[0]
ENDPOINT_ID_PE2_2_1      = DEVICE_PE2_ENDPOINT_IDS[1]
ENDPOINT_ID_PE2_2_2      = DEVICE_PE2_ENDPOINT_IDS[2]
DEVICE_PE2_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_PE2_ENDPOINT_DEFS)

DEVICE_PE3_UUID          = 'PE3'
DEVICE_PE3_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper')]
DEVICE_PE3_ID            = json_device_id(DEVICE_PE3_UUID)
DEVICE_PE3_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_PE3_ID, DEVICE_PE3_ENDPOINT_DEFS)
DEVICE_PE3               = json_device_emulated_packet_router_disabled(DEVICE_PE3_UUID)
ENDPOINT_ID_PE3_1_1      = DEVICE_PE3_ENDPOINT_IDS[0]
ENDPOINT_ID_PE3_2_1      = DEVICE_PE3_ENDPOINT_IDS[1]
ENDPOINT_ID_PE3_2_2      = DEVICE_PE3_ENDPOINT_IDS[2]
DEVICE_PE3_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_PE3_ENDPOINT_DEFS)

DEVICE_PE4_UUID          = 'PE4'
DEVICE_PE4_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper')]
DEVICE_PE4_ID            = json_device_id(DEVICE_PE4_UUID)
DEVICE_PE4_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_PE4_ID, DEVICE_PE4_ENDPOINT_DEFS)
DEVICE_PE4               = json_device_emulated_packet_router_disabled(DEVICE_PE4_UUID)
ENDPOINT_ID_PE4_1_1      = DEVICE_PE4_ENDPOINT_IDS[0]
ENDPOINT_ID_PE4_2_1      = DEVICE_PE4_ENDPOINT_IDS[1]
ENDPOINT_ID_PE4_2_2      = DEVICE_PE4_ENDPOINT_IDS[2]
DEVICE_PE4_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_PE4_ENDPOINT_DEFS)

# ----- BackBone (BB) Devices ------------------------------------------------------------------------------------------
DEVICE_BB1_UUID          = 'BB1'
DEVICE_BB1_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('1/2', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper'),
                            json_endpoint_descriptor('2/3', 'copper')]
DEVICE_BB1_ID            = json_device_id(DEVICE_BB1_UUID)
DEVICE_BB1_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_BB1_ID, DEVICE_BB1_ENDPOINT_DEFS)
DEVICE_BB1               = json_device_emulated_packet_router_disabled(DEVICE_BB1_UUID)
ENDPOINT_ID_BB1_1_1      = DEVICE_BB1_ENDPOINT_IDS[0]
ENDPOINT_ID_BB1_1_2      = DEVICE_BB1_ENDPOINT_IDS[1]
ENDPOINT_ID_BB1_2_1      = DEVICE_BB1_ENDPOINT_IDS[2]
ENDPOINT_ID_BB1_2_2      = DEVICE_BB1_ENDPOINT_IDS[3]
ENDPOINT_ID_BB1_2_3      = DEVICE_BB1_ENDPOINT_IDS[4]
DEVICE_BB1_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_BB1_ENDPOINT_DEFS)

DEVICE_BB2_UUID          = 'BB2'
DEVICE_BB2_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('1/2', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper'),
                            json_endpoint_descriptor('2/3', 'copper')]
DEVICE_BB2_ID            = json_device_id(DEVICE_BB2_UUID)
DEVICE_BB2_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_BB2_ID, DEVICE_BB2_ENDPOINT_DEFS)
DEVICE_BB2               = json_device_emulated_packet_router_disabled(DEVICE_BB2_UUID)
ENDPOINT_ID_BB2_1_1      = DEVICE_BB2_ENDPOINT_IDS[0]
ENDPOINT_ID_BB2_1_2      = DEVICE_BB2_ENDPOINT_IDS[1]
ENDPOINT_ID_BB2_2_1      = DEVICE_BB2_ENDPOINT_IDS[2]
ENDPOINT_ID_BB2_2_2      = DEVICE_BB2_ENDPOINT_IDS[3]
ENDPOINT_ID_BB2_2_3      = DEVICE_BB2_ENDPOINT_IDS[4]
DEVICE_BB2_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_BB2_ENDPOINT_DEFS)

DEVICE_BB3_UUID          = 'BB3'
DEVICE_BB3_ENDPOINT_DEFS = [json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper'),
                            json_endpoint_descriptor('2/3', 'copper')]
DEVICE_BB3_ID            = json_device_id(DEVICE_BB3_UUID)
DEVICE_BB3_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_BB3_ID, DEVICE_BB3_ENDPOINT_DEFS)
DEVICE_BB3               = json_device_emulated_packet_router_disabled(DEVICE_BB3_UUID)
ENDPOINT_ID_BB3_2_1      = DEVICE_BB3_ENDPOINT_IDS[0]
ENDPOINT_ID_BB3_2_2      = DEVICE_BB3_ENDPOINT_IDS[1]
ENDPOINT_ID_BB3_2_3      = DEVICE_BB3_ENDPOINT_IDS[2]
DEVICE_BB3_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_BB3_ENDPOINT_DEFS)

DEVICE_BB4_UUID          = 'BB4'
DEVICE_BB4_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('1/2', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper'),
                            json_endpoint_descriptor('2/3', 'copper')]
DEVICE_BB4_ID            = json_device_id(DEVICE_BB4_UUID)
DEVICE_BB4_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_BB4_ID, DEVICE_BB4_ENDPOINT_DEFS)
DEVICE_BB4               = json_device_emulated_packet_router_disabled(DEVICE_BB4_UUID)
ENDPOINT_ID_BB4_1_1      = DEVICE_BB4_ENDPOINT_IDS[0]
ENDPOINT_ID_BB4_1_2      = DEVICE_BB4_ENDPOINT_IDS[1]
ENDPOINT_ID_BB4_2_1      = DEVICE_BB4_ENDPOINT_IDS[2]
ENDPOINT_ID_BB4_2_2      = DEVICE_BB4_ENDPOINT_IDS[3]
ENDPOINT_ID_BB4_2_3      = DEVICE_BB4_ENDPOINT_IDS[4]
DEVICE_BB4_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_BB4_ENDPOINT_DEFS)

DEVICE_BB5_UUID          = 'BB5'
DEVICE_BB5_ENDPOINT_DEFS = [json_endpoint_descriptor('1/1', 'copper'),
                            json_endpoint_descriptor('1/2', 'copper'),
                            json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper'),
                            json_endpoint_descriptor('2/3', 'copper')]
DEVICE_BB5_ID            = json_device_id(DEVICE_BB5_UUID)
DEVICE_BB5_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_BB5_ID, DEVICE_BB5_ENDPOINT_DEFS)
DEVICE_BB5               = json_device_emulated_packet_router_disabled(DEVICE_BB5_UUID)
ENDPOINT_ID_BB5_1_1      = DEVICE_BB5_ENDPOINT_IDS[0]
ENDPOINT_ID_BB5_1_2      = DEVICE_BB5_ENDPOINT_IDS[1]
ENDPOINT_ID_BB5_2_1      = DEVICE_BB5_ENDPOINT_IDS[2]
ENDPOINT_ID_BB5_2_2      = DEVICE_BB5_ENDPOINT_IDS[3]
ENDPOINT_ID_BB5_2_3      = DEVICE_BB5_ENDPOINT_IDS[4]
DEVICE_BB5_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_BB5_ENDPOINT_DEFS)

DEVICE_BB6_UUID          = 'BB6'
DEVICE_BB6_ENDPOINT_DEFS = [json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper'),
                            json_endpoint_descriptor('2/3', 'copper')]
DEVICE_BB6_ID            = json_device_id(DEVICE_BB6_UUID)
DEVICE_BB6_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_BB6_ID, DEVICE_BB6_ENDPOINT_DEFS)
DEVICE_BB6               = json_device_emulated_packet_router_disabled(DEVICE_BB6_UUID)
ENDPOINT_ID_BB6_2_1      = DEVICE_BB6_ENDPOINT_IDS[0]
ENDPOINT_ID_BB6_2_2      = DEVICE_BB6_ENDPOINT_IDS[1]
ENDPOINT_ID_BB6_2_3      = DEVICE_BB6_ENDPOINT_IDS[2]
DEVICE_BB6_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_BB6_ENDPOINT_DEFS)

DEVICE_BB7_UUID          = 'BB7'
DEVICE_BB7_ENDPOINT_DEFS = [json_endpoint_descriptor('2/1', 'copper'),
                            json_endpoint_descriptor('2/2', 'copper'),
                            json_endpoint_descriptor('2/3', 'copper'),
                            json_endpoint_descriptor('2/4', 'copper'),
                            json_endpoint_descriptor('2/5', 'copper'),
                            json_endpoint_descriptor('2/6', 'copper')]
DEVICE_BB7_ID            = json_device_id(DEVICE_BB7_UUID)
DEVICE_BB7_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_BB7_ID, DEVICE_BB7_ENDPOINT_DEFS)
DEVICE_BB7               = json_device_emulated_packet_router_disabled(DEVICE_BB7_UUID)
ENDPOINT_ID_BB7_2_1      = DEVICE_BB7_ENDPOINT_IDS[0]
ENDPOINT_ID_BB7_2_2      = DEVICE_BB7_ENDPOINT_IDS[1]
ENDPOINT_ID_BB7_2_3      = DEVICE_BB7_ENDPOINT_IDS[2]
ENDPOINT_ID_BB7_2_4      = DEVICE_BB7_ENDPOINT_IDS[3]
ENDPOINT_ID_BB7_2_5      = DEVICE_BB7_ENDPOINT_IDS[4]
ENDPOINT_ID_BB7_2_6      = DEVICE_BB7_ENDPOINT_IDS[5]
DEVICE_BB7_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_BB7_ENDPOINT_DEFS)


# ----- Links ----------------------------------------------------------------------------------------------------------
LINK_CE1_PE1_UUID, LINK_CE1_PE1_ID, LINK_CE1_PE1 = link(ENDPOINT_ID_CE1_1_1, ENDPOINT_ID_PE1_1_1)
LINK_CE2_PE2_UUID, LINK_CE2_PE2_ID, LINK_CE2_PE2 = link(ENDPOINT_ID_CE2_1_1, ENDPOINT_ID_PE2_1_1)
LINK_CE3_PE3_UUID, LINK_CE3_PE3_ID, LINK_CE3_PE3 = link(ENDPOINT_ID_CE3_1_1, ENDPOINT_ID_PE3_1_1)
LINK_CE4_PE4_UUID, LINK_CE4_PE4_ID, LINK_CE4_PE4 = link(ENDPOINT_ID_CE4_1_1, ENDPOINT_ID_PE4_1_1)

LINK_PE1_BB1_UUID, LINK_PE1_BB1_ID, LINK_PE1_BB1 = link(ENDPOINT_ID_PE1_2_1, ENDPOINT_ID_BB1_1_1)
LINK_PE1_BB2_UUID, LINK_PE1_BB2_ID, LINK_PE1_BB2 = link(ENDPOINT_ID_PE1_2_2, ENDPOINT_ID_BB2_1_1)
LINK_PE2_BB1_UUID, LINK_PE2_BB1_ID, LINK_PE2_BB1 = link(ENDPOINT_ID_PE2_2_1, ENDPOINT_ID_BB1_1_2)
LINK_PE2_BB2_UUID, LINK_PE2_BB2_ID, LINK_PE2_BB2 = link(ENDPOINT_ID_PE2_2_2, ENDPOINT_ID_BB2_1_2)

LINK_PE3_BB4_UUID, LINK_PE3_BB4_ID, LINK_PE3_BB4 = link(ENDPOINT_ID_PE3_2_1, ENDPOINT_ID_BB4_1_1)
LINK_PE3_BB5_UUID, LINK_PE3_BB5_ID, LINK_PE3_BB5 = link(ENDPOINT_ID_PE3_2_2, ENDPOINT_ID_BB5_1_1)
LINK_PE4_BB4_UUID, LINK_PE4_BB4_ID, LINK_PE4_BB4 = link(ENDPOINT_ID_PE4_2_1, ENDPOINT_ID_BB4_1_2)
LINK_PE4_BB5_UUID, LINK_PE4_BB5_ID, LINK_PE4_BB5 = link(ENDPOINT_ID_PE4_2_2, ENDPOINT_ID_BB5_1_2)

LINK_BB1_BB2_UUID, LINK_BB1_BB2_ID, LINK_BB1_BB2 = link(ENDPOINT_ID_BB1_2_1, ENDPOINT_ID_BB2_2_2)
LINK_BB2_BB3_UUID, LINK_BB2_BB3_ID, LINK_BB2_BB3 = link(ENDPOINT_ID_BB2_2_1, ENDPOINT_ID_BB3_2_2)
LINK_BB3_BB4_UUID, LINK_BB3_BB4_ID, LINK_BB3_BB4 = link(ENDPOINT_ID_BB3_2_1, ENDPOINT_ID_BB4_2_2)
LINK_BB4_BB5_UUID, LINK_BB4_BB5_ID, LINK_BB4_BB5 = link(ENDPOINT_ID_BB4_2_1, ENDPOINT_ID_BB5_2_2)
LINK_BB5_BB6_UUID, LINK_BB5_BB6_ID, LINK_BB5_BB6 = link(ENDPOINT_ID_BB5_2_1, ENDPOINT_ID_BB6_2_2)
LINK_BB6_BB1_UUID, LINK_BB6_BB1_ID, LINK_BB6_BB1 = link(ENDPOINT_ID_BB6_2_1, ENDPOINT_ID_BB1_2_2)

LINK_BB1_BB7_UUID, LINK_BB1_BB7_ID, LINK_BB1_BB7 = link(ENDPOINT_ID_BB1_2_3, ENDPOINT_ID_BB7_2_1)
LINK_BB2_BB7_UUID, LINK_BB2_BB7_ID, LINK_BB2_BB7 = link(ENDPOINT_ID_BB2_2_3, ENDPOINT_ID_BB7_2_2)
LINK_BB3_BB7_UUID, LINK_BB3_BB7_ID, LINK_BB3_BB7 = link(ENDPOINT_ID_BB3_2_3, ENDPOINT_ID_BB7_2_3)
LINK_BB4_BB7_UUID, LINK_BB4_BB7_ID, LINK_BB4_BB7 = link(ENDPOINT_ID_BB4_2_3, ENDPOINT_ID_BB7_2_4)
LINK_BB5_BB7_UUID, LINK_BB5_BB7_ID, LINK_BB5_BB7 = link(ENDPOINT_ID_BB5_2_3, ENDPOINT_ID_BB7_2_5)
LINK_BB6_BB7_UUID, LINK_BB6_BB7_ID, LINK_BB6_BB7 = link(ENDPOINT_ID_BB6_2_3, ENDPOINT_ID_BB7_2_6)


# ----- WIM Service Settings -------------------------------------------------------------------------------------------
WIM_USERNAME = 'admin'
WIM_PASSWORD = 'admin'

def mapping(site_id, ce_endpoint_id, pe_device_id, priority=None, redundant=[]):
    ce_device_uuid = ce_endpoint_id['device_id']['device_uuid']['uuid']
    ce_endpoint_uuid = ce_endpoint_id['endpoint_uuid']['uuid']
    pe_device_uuid = pe_device_id['device_uuid']['uuid']
    service_endpoint_id = '{:s}-{:s}-{:s}'.format(site_id, ce_device_uuid, ce_endpoint_uuid)
    bearer = '{:s}-{:s}'.format(ce_device_uuid, pe_device_uuid)
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

WIM_SEP_DC1_PRI, WIM_MAP_DC1_PRI = mapping('DC1', ENDPOINT_ID_CE1_1_1, DEVICE_PE1_ID, priority=10, redundant=['DC1-CE2-1/1'])
WIM_SEP_DC1_SEC, WIM_MAP_DC1_SEC = mapping('DC1', ENDPOINT_ID_CE2_1_1, DEVICE_PE2_ID, priority=20)
WIM_SEP_DC2_PRI, WIM_MAP_DC2_PRI = mapping('DC2', ENDPOINT_ID_CE3_1_1, DEVICE_PE3_ID, priority=10, redundant=['DC2-CE4-1/1'])
WIM_SEP_DC2_SEC, WIM_MAP_DC2_SEC = mapping('DC2', ENDPOINT_ID_CE4_1_1, DEVICE_PE4_ID, priority=20)

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


# ----- Object Collections ---------------------------------------------------------------------------------------------

CONTEXTS = [CONTEXT]
TOPOLOGIES = [TOPOLOGY]

DEVICES = [
    (DEVICE_CE1, DEVICE_CE1_CONNECT_RULES),
    (DEVICE_CE2, DEVICE_CE2_CONNECT_RULES),
    (DEVICE_CE3, DEVICE_CE3_CONNECT_RULES),
    (DEVICE_CE4, DEVICE_CE4_CONNECT_RULES),

    (DEVICE_PE1, DEVICE_PE1_CONNECT_RULES),
    (DEVICE_PE2, DEVICE_PE2_CONNECT_RULES),
    (DEVICE_PE3, DEVICE_PE3_CONNECT_RULES),
    (DEVICE_PE4, DEVICE_PE4_CONNECT_RULES),

    (DEVICE_BB1, DEVICE_BB1_CONNECT_RULES),
    (DEVICE_BB2, DEVICE_BB2_CONNECT_RULES),
    (DEVICE_BB6, DEVICE_BB6_CONNECT_RULES),
    (DEVICE_BB7, DEVICE_BB7_CONNECT_RULES),
    (DEVICE_BB3, DEVICE_BB3_CONNECT_RULES),
    (DEVICE_BB5, DEVICE_BB5_CONNECT_RULES),
    (DEVICE_BB4, DEVICE_BB4_CONNECT_RULES),
]

LINKS = [
    LINK_CE1_PE1, LINK_CE2_PE2, LINK_CE3_PE3, LINK_CE4_PE4,
    LINK_PE1_BB1, LINK_PE1_BB2, LINK_PE2_BB1, LINK_PE2_BB2,
    LINK_PE3_BB5, LINK_PE3_BB4, LINK_PE4_BB5, LINK_PE4_BB4,
    LINK_BB1_BB2, LINK_BB2_BB3, LINK_BB3_BB4, LINK_BB4_BB5, LINK_BB5_BB6, LINK_BB6_BB1,
    LINK_BB1_BB7, LINK_BB2_BB7, LINK_BB3_BB7, LINK_BB4_BB7, LINK_BB5_BB7, LINK_BB6_BB7,
]
