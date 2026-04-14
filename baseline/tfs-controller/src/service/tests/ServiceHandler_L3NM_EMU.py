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

from typing import Dict, List, Tuple

from common.tools.object_factory.Location import json_location, json_gps_position
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Constraint import json_constraint_custom, json_constraint_endpoint_location_gps
from common.tools.object_factory.Device import (
    json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled,
    json_device_emulated_tapi_disabled, json_device_id)
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_descriptor, json_endpoint_id
from common.tools.object_factory.Link import json_link, json_link_id
from common.tools.object_factory.Service import json_service_id, json_service_l3nm_planned
from .CommonObjects import CONTEXT, CONTEXT_ID, PACKET_PORT_SAMPLE_TYPES, TOPOLOGY, TOPOLOGY_ID

SERVICE_HANDLER_NAME = 'l3nm_emulated'

def json_endpoint_ids(device_id : Dict, endpoint_descriptors : List[Dict]):
    return [
        json_endpoint_id(device_id, ep_data['uuid'])
        for ep_data in endpoint_descriptors
    ]

def json_endpoints(device_id : Dict, endpoint_descriptors : List[Dict]):
    return [
        json_endpoint(
            device_id, ep_data['uuid'], ep_data['type'], kpi_sample_types=PACKET_PORT_SAMPLE_TYPES,
            location=ep_data.get('location'))
        for ep_data in endpoint_descriptors
    ]


BARCELONA_GPS = (41.386726, 2.170107)
MALAGA_GPS = (36.721162, -4.418339)
ZARAGOZA_GPS = (41.655552, -0.876442)
MADRID_GPS = (40.416741, -3.703285)
TOLEDO_GPS = (39.862947, -4.027485)
ANDORRA_GPS = (42.506017, 1.525923)
SANTIAGO_GPS = (42.876254, -8.543588)
GRANADA_GPS =    (37.178106, -3.599816)
PONFERRADA_GPS = (42.550116, -6.597930)
ALBACETE_GPS = (38.998249, -1.858145)


# ----- Devices --------------------------------------------------------------------------------------------------------
DEVICE_R1_UUID          = 'R1'
DEVICE_R1_ENDPOINT_DEFS = [
    json_endpoint_descriptor('EP1', 'optical', location=json_location(gps_position=json_gps_position(*BARCELONA_GPS))),
    json_endpoint_descriptor('EP100', 'copper', location=json_location(gps_position=json_gps_position(*BARCELONA_GPS)))
]
DEVICE_R1_ID            = json_device_id(DEVICE_R1_UUID)
DEVICE_R1_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_R1_ENDPOINT_DEFS)
DEVICE_R1               = json_device_emulated_packet_router_disabled(
    DEVICE_R1_UUID, config_rules=DEVICE_R1_CONNECT_RULES)
DEVICE_R1_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_R1_ID, DEVICE_R1_ENDPOINT_DEFS)
ENDPOINT_ID_R1_EP1      = DEVICE_R1_ENDPOINT_IDS[0]
ENDPOINT_ID_R1_EP100    = DEVICE_R1_ENDPOINT_IDS[1]

DEVICE_R2_UUID          = 'R2'
DEVICE_R2_ENDPOINT_DEFS = [
    json_endpoint_descriptor('EP1', 'optical', location=json_location(gps_position=json_gps_position(*MADRID_GPS))),
    json_endpoint_descriptor('EP100', 'copper', location=json_location(gps_position=json_gps_position(*MADRID_GPS)))
]
DEVICE_R2_ID            = json_device_id(DEVICE_R2_UUID)
DEVICE_R2_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_R2_ENDPOINT_DEFS)
DEVICE_R2               = json_device_emulated_packet_router_disabled(
    DEVICE_R2_UUID, config_rules=DEVICE_R2_CONNECT_RULES)
DEVICE_R2_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_R2_ID, DEVICE_R2_ENDPOINT_DEFS)
ENDPOINT_ID_R2_EP1      = DEVICE_R2_ENDPOINT_IDS[0]
ENDPOINT_ID_R2_EP100    = DEVICE_R2_ENDPOINT_IDS[1]

DEVICE_R3_UUID          = 'R3'
DEVICE_R3_ENDPOINT_DEFS = [
    json_endpoint_descriptor('EP1', 'optical', location=json_location(gps_position=json_gps_position(*MALAGA_GPS))),
    json_endpoint_descriptor('EP100', 'copper', location=json_location(gps_position=json_gps_position(*MALAGA_GPS)))
]
DEVICE_R3_ID            = json_device_id(DEVICE_R3_UUID)
DEVICE_R2_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_R2_ENDPOINT_DEFS)
DEVICE_R3               = json_device_emulated_packet_router_disabled(
    DEVICE_R3_UUID, config_rules=DEVICE_R2_CONNECT_RULES)
DEVICE_R3_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_R3_ID, DEVICE_R3_ENDPOINT_DEFS)
ENDPOINT_ID_R3_EP1      = DEVICE_R3_ENDPOINT_IDS[0]
ENDPOINT_ID_R3_EP100    = DEVICE_R3_ENDPOINT_IDS[1]

DEVICE_O1_UUID          = 'O1'
DEVICE_O1_ENDPOINT_DEFS = [
    json_endpoint_descriptor('EP1', 'optical', location=json_location(gps_position=json_gps_position(*PONFERRADA_GPS))),
    json_endpoint_descriptor('EP2', 'optical', location=json_location(gps_position=json_gps_position(*PONFERRADA_GPS))),
    json_endpoint_descriptor('EP3', 'optical', location=json_location(gps_position=json_gps_position(*PONFERRADA_GPS)))
]
DEVICE_O1_ID            = json_device_id(DEVICE_O1_UUID)
DEVICE_O1_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_O1_ENDPOINT_DEFS)
DEVICE_O1               = json_device_emulated_tapi_disabled(DEVICE_O1_UUID, config_rules=DEVICE_O1_CONNECT_RULES)
DEVICE_O1_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_O1_ID, DEVICE_O1_ENDPOINT_DEFS)
ENDPOINT_ID_O1_EP1      = DEVICE_O1_ENDPOINT_IDS[0]
ENDPOINT_ID_O1_EP2      = DEVICE_O1_ENDPOINT_IDS[1]
ENDPOINT_ID_O1_EP3      = DEVICE_O1_ENDPOINT_IDS[2]


# ----- Links ----------------------------------------------------------------------------------------------------------
LINK_R1_O1_UUID = '{:s}/{:s}-{:s}/{:s}'.format(
    DEVICE_R1_UUID, ENDPOINT_ID_R1_EP1['endpoint_uuid']['uuid'],
    DEVICE_O1_UUID, ENDPOINT_ID_O1_EP1['endpoint_uuid']['uuid'])
LINK_R1_O1_ID   = json_link_id(LINK_R1_O1_UUID)
LINK_R1_O1      = json_link(LINK_R1_O1_UUID, [ENDPOINT_ID_R1_EP1, ENDPOINT_ID_O1_EP1])

LINK_R2_O1_UUID = '{:s}/{:s}-{:s}/{:s}'.format(
    DEVICE_R2_UUID, ENDPOINT_ID_R2_EP1['endpoint_uuid']['uuid'],
    DEVICE_O1_UUID, ENDPOINT_ID_O1_EP2['endpoint_uuid']['uuid'])
LINK_R2_O1_ID   = json_link_id(LINK_R2_O1_UUID)
LINK_R2_O1      = json_link(LINK_R2_O1_UUID, [ENDPOINT_ID_R2_EP1, ENDPOINT_ID_O1_EP2])

LINK_R3_O1_UUID = '{:s}/{:s}-{:s}/{:s}'.format(
    DEVICE_R3_UUID, ENDPOINT_ID_R3_EP1['endpoint_uuid']['uuid'],
    DEVICE_O1_UUID, ENDPOINT_ID_O1_EP3['endpoint_uuid']['uuid'])
LINK_R3_O1_ID   = json_link_id(LINK_R3_O1_UUID)
LINK_R3_O1      = json_link(LINK_R3_O1_UUID, [ENDPOINT_ID_R3_EP1, ENDPOINT_ID_O1_EP3])


# ----- Service --------------------------------------------------------------------------------------------------------
SERVICE_R1_R3_UUID         = 'SVC:{:s}/{:s}-{:s}/{:s}'.format(
    DEVICE_R1_UUID, ENDPOINT_ID_R1_EP100['endpoint_uuid']['uuid'],
    DEVICE_R3_UUID, ENDPOINT_ID_R3_EP100['endpoint_uuid']['uuid'])
SERVICE_R1_R3_ENDPOINT_IDS = [ENDPOINT_ID_R1_EP100, ENDPOINT_ID_R3_EP100]
SERVICE_R1_R3_CONSTRAINTS  = [
    json_constraint_custom('latency_ms', 15.2),
    json_constraint_custom('jitter_us', 1.2),
]

SERVICE_R1_R3_CONSTRAINTS_LOCATION = [
    json_constraint_endpoint_location_gps(None, ZARAGOZA_GPS[0], ZARAGOZA_GPS[1]),
    json_constraint_endpoint_location_gps(None, TOLEDO_GPS[0], TOLEDO_GPS[1]),
]
SERVICE_R1_R3_CONSTRAINTS_LOCATION_NEW = [
    json_constraint_endpoint_location_gps(None, SANTIAGO_GPS[0], SANTIAGO_GPS[1]),
    json_constraint_endpoint_location_gps(None, GRANADA_GPS[0], GRANADA_GPS[1]),
]

SERVICE_R1_R3_CONFIG_RULES = [
    json_config_rule_set(
        '/settings',
        {'mtu': 1512, 'address_families': ['IPV4'], 'bgp_as': 65000, 'bgp_route_target': '65000:333'}),
    json_config_rule_set(
        '/device[{:s}]/endpoint[{:s}]/settings'.format(DEVICE_R1_UUID, ENDPOINT_ID_R1_EP100['endpoint_uuid']['uuid']),
        {'router_id': '10.10.10.1', 'route_distinguisher': '65000:123', 'sub_interface_index': 400, 'vlan_id': 400,
        'address_ip': '3.3.2.1', 'address_prefix': 24}),
    json_config_rule_set(
        '/device[{:s}]/endpoint[{:s}]/settings'.format(DEVICE_R3_UUID, ENDPOINT_ID_R3_EP100['endpoint_uuid']['uuid']),
        {'router_id': '20.20.20.1', 'route_distinguisher': '65000:321', 'sub_interface_index': 400, 'vlan_id': 500,
        'address_ip': '3.3.1.1', 'address_prefix': 24}),
]
SERVICE_R1_R3_ID           = json_service_id(SERVICE_R1_R3_UUID, context_id=CONTEXT_ID)
SERVICE_R1_R3_DESCRIPTOR   = json_service_l3nm_planned(SERVICE_R1_R3_UUID)


# ----- Test Descriptor ------------------------------------------------------------------------------------------------
TEST_SERVICE_HANDLER = (SERVICE_HANDLER_NAME, {
    'contexts'                          : [CONTEXT],
    'topologies'                        : [TOPOLOGY],
    'devices'                           : [DEVICE_R1, DEVICE_R2, DEVICE_R3, DEVICE_O1],
    'links'                             : [LINK_R1_O1, LINK_R2_O1, LINK_R3_O1],
    'service_id'                        : SERVICE_R1_R3_ID,
    'service_descriptor'                : SERVICE_R1_R3_DESCRIPTOR,
    'service_endpoint_ids'              : SERVICE_R1_R3_ENDPOINT_IDS,
    'service_config_rules'              : SERVICE_R1_R3_CONFIG_RULES,
    'service_constraints'               : SERVICE_R1_R3_CONSTRAINTS,
    'service_constraints_location'      : SERVICE_R1_R3_CONSTRAINTS_LOCATION,
    'service_constraints_location_new'  : SERVICE_R1_R3_CONSTRAINTS_LOCATION_NEW,
})
