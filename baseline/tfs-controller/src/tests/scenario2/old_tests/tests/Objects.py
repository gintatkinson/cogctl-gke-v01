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
from common.Constants import DEFAULT_CONTEXT_UUID, DEFAULT_TOPOLOGY_UUID
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled,
    json_device_emulated_tapi_disabled, json_device_id, json_device_packetrouter_disabled, json_device_tapi_disabled)
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_descriptor, json_endpoint_id
from common.tools.object_factory.Link import json_link, json_link_id
from common.tools.object_factory.Topology import json_topology, json_topology_id
from common.proto.kpi_sample_types_pb2 import KpiSampleType

# ----- Context --------------------------------------------------------------------------------------------------------
CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_UUID)
CONTEXT    = json_context(DEFAULT_CONTEXT_UUID)

# ----- Topology -------------------------------------------------------------------------------------------------------
TOPOLOGY_ID = json_topology_id(DEFAULT_TOPOLOGY_UUID, context_id=CONTEXT_ID)
TOPOLOGY    = json_topology(DEFAULT_TOPOLOGY_UUID, context_id=CONTEXT_ID)

# ----- Monitoring Samples ---------------------------------------------------------------------------------------------
PACKET_PORT_SAMPLE_TYPES = [
    KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED,
    KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED,
]

# ----- Device Credentials and Settings --------------------------------------------------------------------------------
try:
    from .Credentials import DEVICE_R1_ADDRESS, DEVICE_R1_PORT, DEVICE_R1_USERNAME, DEVICE_R1_PASSWORD
    from .Credentials import DEVICE_R3_ADDRESS, DEVICE_R3_PORT, DEVICE_R3_USERNAME, DEVICE_R3_PASSWORD
    from .Credentials import DEVICE_O1_ADDRESS, DEVICE_O1_PORT
    USE_REAL_DEVICES = True     # Use real devices
except ImportError:
    USE_REAL_DEVICES = False    # Use emulated devices

    DEVICE_R1_ADDRESS  = '0.0.0.0'
    DEVICE_R1_PORT     = 830
    DEVICE_R1_USERNAME = 'admin'
    DEVICE_R1_PASSWORD = 'admin'

    DEVICE_R3_ADDRESS  = '0.0.0.0'
    DEVICE_R3_PORT     = 830
    DEVICE_R3_USERNAME = 'admin'
    DEVICE_R3_PASSWORD = 'admin'

    DEVICE_O1_ADDRESS  = '0.0.0.0'
    DEVICE_O1_PORT     = 4900

#USE_REAL_DEVICES = False     # Uncomment to force to use emulated devices

def json_endpoint_ids(device_id : Dict, endpoint_descriptors : List[Dict]]):
    return [
        json_endpoint_id(device_id, ep_data['uuid'], topology_id=None)
        for ep_data in endpoint_descriptors
    ]

def json_endpoints(device_id : Dict, endpoint_descriptors : List[Dict]]):
    return [
        json_endpoint(
            device_id, ep_data['uuid'], ep_data['type'], topology_id=None,
            kpi_sample_types=ep_data['sample_types'])
        for ep_data in endpoint_descriptors
    ]

def get_link_uuid(a_device_id : Dict, a_endpoint_id : Dict, z_device_id : Dict, z_endpoint_id : Dict) -> str:
    return '{:s}/{:s}=={:s}/{:s}'.format(
        a_device_id['device_uuid']['uuid'], a_endpoint_id['endpoint_uuid']['uuid'],
        z_device_id['device_uuid']['uuid'], z_endpoint_id['endpoint_uuid']['uuid'])


# ----- Devices --------------------------------------------------------------------------------------------------------
if not USE_REAL_DEVICES:
    json_device_packetrouter_disabled = json_device_emulated_packet_router_disabled
    json_device_tapi_disabled         = json_device_emulated_tapi_disabled

DEVICE_R1_UUID          = 'R1-EMU'
DEVICE_R1_TIMEOUT       = 120
DEVICE_R1_ENDPOINT_DEFS = [json_endpoint_descriptor('13/0/0', 'optical'),
                           json_endpoint_descriptor('13/1/2', 'copper', sample_types=PACKET_PORT_SAMPLE_TYPES)]
DEVICE_R1_ID            = json_device_id(DEVICE_R1_UUID)
#DEVICE_R1_ENDPOINTS     = json_endpoints(DEVICE_R1_ID, DEVICE_R1_ENDPOINT_DEFS)
DEVICE_R1_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_R1_ID, DEVICE_R1_ENDPOINT_DEFS)
DEVICE_R1               = json_device_packetrouter_disabled(DEVICE_R1_UUID)
ENDPOINT_ID_R1_13_0_0   = DEVICE_R1_ENDPOINT_IDS[0]
ENDPOINT_ID_R1_13_1_2   = DEVICE_R1_ENDPOINT_IDS[1]
DEVICE_R1_CONNECT_RULES = json_device_connect_rules(DEVICE_R1_ADDRESS, DEVICE_R1_PORT, {
    'username': DEVICE_R1_USERNAME,
    'password': DEVICE_R1_PASSWORD,
    'timeout' : DEVICE_R1_TIMEOUT,
}) if USE_REAL_DEVICES else json_device_emulated_connect_rules(DEVICE_R1_ENDPOINT_DEFS)


DEVICE_R2_UUID          = 'R2-EMU'
DEVICE_R2_ENDPOINT_DEFS = [json_endpoint_descriptor('13/0/0', 'optical'),
                           json_endpoint_descriptor('13/1/2', 'copper', sample_types=PACKET_PORT_SAMPLE_TYPES)]
DEVICE_R2_ID            = json_device_id(DEVICE_R2_UUID)
#DEVICE_R2_ENDPOINTS     = json_endpoints(DEVICE_R2_ID, DEVICE_R2_ENDPOINT_DEFS)
DEVICE_R2_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_R2_ID, DEVICE_R2_ENDPOINT_DEFS)
DEVICE_R2               = json_device_emulated_packet_router_disabled(DEVICE_R2_UUID)
ENDPOINT_ID_R2_13_0_0   = DEVICE_R2_ENDPOINT_IDS[0]
ENDPOINT_ID_R2_13_1_2   = DEVICE_R2_ENDPOINT_IDS[1]
DEVICE_R2_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_R2_ENDPOINT_DEFS)


DEVICE_R3_UUID          = 'R3-EMU'
DEVICE_R3_TIMEOUT       = 120
DEVICE_R3_ENDPOINT_DEFS = [json_endpoint_descriptor('13/0/0', 'optical'),
                           json_endpoint_descriptor('13/1/2', 'copper', sample_types=PACKET_PORT_SAMPLE_TYPES)]
DEVICE_R3_ID            = json_device_id(DEVICE_R3_UUID)
#DEVICE_R3_ENDPOINTS     = json_endpoints(DEVICE_R3_ID, DEVICE_R3_ENDPOINT_DEFS)
DEVICE_R3_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_R3_ID, DEVICE_R3_ENDPOINT_DEFS)
DEVICE_R3               = json_device_packetrouter_disabled(DEVICE_R3_UUID)
ENDPOINT_ID_R3_13_0_0   = DEVICE_R3_ENDPOINT_IDS[0]
ENDPOINT_ID_R3_13_1_2   = DEVICE_R3_ENDPOINT_IDS[1]
DEVICE_R3_CONNECT_RULES = json_device_connect_rules(DEVICE_R3_ADDRESS, DEVICE_R3_PORT, {
    'username': DEVICE_R3_USERNAME,
    'password': DEVICE_R3_PASSWORD,
    'timeout' : DEVICE_R3_TIMEOUT,
}) if USE_REAL_DEVICES else json_device_emulated_connect_rules(DEVICE_R3_ENDPOINT_DEFS)


DEVICE_R4_UUID          = 'R4-EMU'
DEVICE_R4_ENDPOINT_DEFS = [json_endpoint_descriptor('13/0/0', 'optical'),
                           json_endpoint_descriptor('13/1/2', 'copper', sample_types=PACKET_PORT_SAMPLE_TYPES)]
DEVICE_R4_ID            = json_device_id(DEVICE_R4_UUID)
#DEVICE_R4_ENDPOINTS     = json_endpoints(DEVICE_R4_ID, DEVICE_R4_ENDPOINT_DEFS)
DEVICE_R4_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_R4_ID, DEVICE_R4_ENDPOINT_DEFS)
DEVICE_R4               = json_device_emulated_packet_router_disabled(DEVICE_R4_UUID)
ENDPOINT_ID_R4_13_0_0   = DEVICE_R4_ENDPOINT_IDS[0]
ENDPOINT_ID_R4_13_1_2   = DEVICE_R4_ENDPOINT_IDS[1]
DEVICE_R4_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_R4_ENDPOINT_DEFS)


DEVICE_O1_UUID          = 'O1-OLS'
DEVICE_O1_TIMEOUT       = 120
DEVICE_O1_ENDPOINT_DEFS = [
    json_endpoint_descriptor('aade6001-f00b-5e2f-a357-6a0a9d3de870', 'optical', endpoint_name='node_1_port_13'),
    json_endpoint_descriptor('eb287d83-f05e-53ec-ab5a-adf6bd2b5418', 'optical', endpoint_name='node_2_port_13'),
    json_endpoint_descriptor('0ef74f99-1acc-57bd-ab9d-4b958b06c513', 'optical', endpoint_name='node_3_port_13'),
    json_endpoint_descriptor('50296d99-58cc-5ce7-82f5-fc8ee4eec2ec', 'optical', endpoint_name='node_4_port_13'),
]
DEVICE_O1_ID            = json_device_id(DEVICE_O1_UUID)
DEVICE_O1               = json_device_tapi_disabled(DEVICE_O1_UUID)
#DEVICE_O1_ENDPOINTS     = json_endpoints(DEVICE_O1_ID, DEVICE_O1_ENDPOINT_DEFS)
DEVICE_O1_ENDPOINT_IDS  = json_endpoint_ids(DEVICE_O1_ID, DEVICE_O1_ENDPOINT_DEFS)
ENDPOINT_ID_O1_EP1      = DEVICE_O1_ENDPOINT_IDS[0]
ENDPOINT_ID_O1_EP2      = DEVICE_O1_ENDPOINT_IDS[1]
ENDPOINT_ID_O1_EP3      = DEVICE_O1_ENDPOINT_IDS[2]
ENDPOINT_ID_O1_EP4      = DEVICE_O1_ENDPOINT_IDS[3]
DEVICE_O1_CONNECT_RULES = json_device_connect_rules(DEVICE_O1_ADDRESS, DEVICE_O1_PORT, {
    'timeout' : DEVICE_O1_TIMEOUT,
}) if USE_REAL_DEVICES else json_device_emulated_connect_rules(DEVICE_O1_ENDPOINT_DEFS)


# ----- Links ----------------------------------------------------------------------------------------------------------
LINK_R1_O1_UUID = get_link_uuid(DEVICE_R1_ID, ENDPOINT_ID_R1_13_0_0, DEVICE_O1_ID, ENDPOINT_ID_O1_EP1)
LINK_R1_O1_ID   = json_link_id(LINK_R1_O1_UUID)
LINK_R1_O1      = json_link(LINK_R1_O1_UUID, [ENDPOINT_ID_R1_13_0_0, ENDPOINT_ID_O1_EP1])

LINK_R2_O1_UUID = get_link_uuid(DEVICE_R2_ID, ENDPOINT_ID_R2_13_0_0, DEVICE_O1_ID, ENDPOINT_ID_O1_EP2)
LINK_R2_O1_ID   = json_link_id(LINK_R2_O1_UUID)
LINK_R2_O1      = json_link(LINK_R2_O1_UUID, [ENDPOINT_ID_R2_13_0_0, ENDPOINT_ID_O1_EP2])

LINK_R3_O1_UUID = get_link_uuid(DEVICE_R3_ID, ENDPOINT_ID_R3_13_0_0, DEVICE_O1_ID, ENDPOINT_ID_O1_EP3)
LINK_R3_O1_ID   = json_link_id(LINK_R3_O1_UUID)
LINK_R3_O1      = json_link(LINK_R3_O1_UUID, [ENDPOINT_ID_R3_13_0_0, ENDPOINT_ID_O1_EP3])

LINK_R4_O1_UUID = get_link_uuid(DEVICE_R4_ID, ENDPOINT_ID_R4_13_0_0, DEVICE_O1_ID, ENDPOINT_ID_O1_EP4)
LINK_R4_O1_ID   = json_link_id(LINK_R4_O1_UUID)
LINK_R4_O1      = json_link(LINK_R4_O1_UUID, [ENDPOINT_ID_R4_13_0_0, ENDPOINT_ID_O1_EP4])


# ----- WIM Service Settings -------------------------------------------------------------------------------------------

def compose_service_endpoint_id(endpoint_id):
    device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
    endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
    return ':'.join([device_uuid, endpoint_uuid])

WIM_SEP_R1_ID      = compose_service_endpoint_id(ENDPOINT_ID_R1_13_1_2)
WIM_SEP_R1_SITE_ID = '1'
WIM_SEP_R1_BEARER  = WIM_SEP_R1_ID
WIM_SRV_R1_VLAN_ID = 400

WIM_SEP_R3_ID      = compose_service_endpoint_id(ENDPOINT_ID_R3_13_1_2)
WIM_SEP_R3_SITE_ID = '2'
WIM_SEP_R3_BEARER  = WIM_SEP_R3_ID
WIM_SRV_R3_VLAN_ID = 500

WIM_USERNAME = 'admin'
WIM_PASSWORD = 'admin'

WIM_MAPPING  = [
    {'device-id': DEVICE_R1_UUID, 'service_endpoint_id': WIM_SEP_R1_ID,
     'service_mapping_info': {'bearer': {'bearer-reference': WIM_SEP_R1_BEARER}, 'site-id': WIM_SEP_R1_SITE_ID}},
    {'device-id': DEVICE_R3_UUID, 'service_endpoint_id': WIM_SEP_R3_ID,
     'service_mapping_info': {'bearer': {'bearer-reference': WIM_SEP_R3_BEARER}, 'site-id': WIM_SEP_R3_SITE_ID}},
]
WIM_SERVICE_TYPE = 'ELINE'
WIM_SERVICE_CONNECTION_POINTS = [
    {'service_endpoint_id': WIM_SEP_R1_ID,
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': WIM_SRV_R1_VLAN_ID}},
    {'service_endpoint_id': WIM_SEP_R3_ID,
        'service_endpoint_encapsulation_type': 'dot1q',
        'service_endpoint_encapsulation_info': {'vlan': WIM_SRV_R3_VLAN_ID}},
]

# ----- Object Collections ---------------------------------------------------------------------------------------------

CONTEXTS = [CONTEXT]
TOPOLOGIES = [TOPOLOGY]

DEVICES = [
    (DEVICE_R1, DEVICE_R1_CONNECT_RULES),
    (DEVICE_R2, DEVICE_R2_CONNECT_RULES),
    (DEVICE_R3, DEVICE_R3_CONNECT_RULES),
    (DEVICE_R4, DEVICE_R4_CONNECT_RULES),
    (DEVICE_O1, DEVICE_O1_CONNECT_RULES),
]

LINKS = [LINK_R1_O1, LINK_R2_O1, LINK_R3_O1, LINK_R4_O1]