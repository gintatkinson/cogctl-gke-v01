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
from typing import Dict, List, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled,
    json_device_connect_rules, json_device_id, json_device_p4_disabled,
    json_device_emulated_tapi_disabled, json_device_id, json_device_packetrouter_disabled, json_device_tapi_disabled)
from common.tools.object_factory.Service import (
    get_service_uuid, json_service_l3nm_planned,json_service_p4_planned)
from common.tools.object_factory.ConfigRule import (
    json_config_rule_set, json_config_rule_delete)
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_ids, json_endpoints, json_endpoint_id
from common.tools.object_factory.EndPoint import json_endpoint_descriptor
from common.tools.object_factory.Link import get_link_uuid, json_link, json_link_id
from common.tools.object_factory.Topology import json_topology, json_topology_id
from common.proto.kpi_sample_types_pb2 import KpiSampleType

# ----- Context --------------------------------------------------------------------------------------------------------
CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
CONTEXT    = json_context(DEFAULT_CONTEXT_NAME)

# ----- Topology -------------------------------------------------------------------------------------------------------
TOPOLOGY_ID = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)
TOPOLOGY    = json_topology(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)

# ----- Monitoring Samples ---------------------------------------------------------------------------------------------
PACKET_PORT_SAMPLE_TYPES = [
    KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED,
    KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED,
]

# ----- Device Credentials and Settings --------------------------------------------------------------------------------


# ----- Devices --------------------------------------------------------------------------------------------------------

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

DEVICE_SW1_UUID             = 'SW1'
DEVICE_SW1_TIMEOUT          = 60
DEVICE_SW1_ID               = json_device_id(DEVICE_SW1_UUID)
DEVICE_SW1                  = json_device_p4_disabled(DEVICE_SW1_UUID)

DEVICE_SW1_DPID             = 1
DEVICE_SW1_NAME             = DEVICE_SW1_UUID
DEVICE_SW1_IP_ADDR          = '10.0.2.10'
DEVICE_SW1_PORT             = '50001'
DEVICE_SW1_VENDOR           = 'Open Networking Foundation'
DEVICE_SW1_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW1_SW_VER           = 'Stratum'

DEVICE_SW1_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW1_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW1_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port'),
                               json_endpoint_descriptor('3', 'port')]
DEVICE_SW1_ENDPOINTS        = json_endpoints(DEVICE_SW1_ID, DEVICE_SW1_ENDPOINT_DEFS)
DEVICE_SW1_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW1_ID, DEVICE_SW1_ENDPOINT_DEFS)
ENDPOINT_ID_SW1_1           = DEVICE_SW1_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW1_2           = DEVICE_SW1_ENDPOINTS[1]['endpoint_id']
ENDPOINT_ID_SW1_3           = DEVICE_SW1_ENDPOINTS[2]['endpoint_id']

DEVICE_SW1_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW1_IP_ADDR,
    DEVICE_SW1_PORT,
    {
        'id':       DEVICE_SW1_DPID,
        'name':     DEVICE_SW1_NAME,
        'vendor':   DEVICE_SW1_VENDOR,
        'hw_ver':   DEVICE_SW1_HW_VER,
        'sw_ver':   DEVICE_SW1_SW_VER,
        'timeout':  DEVICE_SW1_TIMEOUT,
        'p4bin':    DEVICE_SW1_BIN_PATH,
        'p4info':   DEVICE_SW1_INFO_PATH
    }
)

DEVICE_SW2_UUID             = 'SW2'
DEVICE_SW2_TIMEOUT          = 60
DEVICE_SW2_ID               = json_device_id(DEVICE_SW2_UUID)
DEVICE_SW2                  = json_device_p4_disabled(DEVICE_SW2_UUID)

DEVICE_SW2_DPID             = 1
DEVICE_SW2_NAME             = DEVICE_SW2_UUID
DEVICE_SW2_IP_ADDR          = '10.0.2.10'
DEVICE_SW2_PORT             = '50002'
DEVICE_SW2_VENDOR           = 'Open Networking Foundation'
DEVICE_SW2_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW2_SW_VER           = 'Stratum'

DEVICE_SW2_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW2_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW2_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port')]
DEVICE_SW2_ENDPOINTS        = json_endpoints(DEVICE_SW2_ID, DEVICE_SW2_ENDPOINT_DEFS)
DEVICE_SW2_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW2_ID, DEVICE_SW2_ENDPOINT_DEFS)
ENDPOINT_ID_SW2_1           = DEVICE_SW2_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW2_2           = DEVICE_SW2_ENDPOINTS[1]['endpoint_id']

DEVICE_SW2_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW2_IP_ADDR,
    DEVICE_SW2_PORT,
    {
        'id':       DEVICE_SW2_DPID,
        'name':     DEVICE_SW2_NAME,
        'vendor':   DEVICE_SW2_VENDOR,
        'hw_ver':   DEVICE_SW2_HW_VER,
        'sw_ver':   DEVICE_SW2_SW_VER,
        'timeout':  DEVICE_SW2_TIMEOUT,
        'p4bin':    DEVICE_SW2_BIN_PATH,
        'p4info':   DEVICE_SW2_INFO_PATH
    }
)

DEVICE_SW3_UUID             = 'SW3'
DEVICE_SW3_TIMEOUT          = 60
DEVICE_SW3_ID               = json_device_id(DEVICE_SW3_UUID)
DEVICE_SW3                  = json_device_p4_disabled(DEVICE_SW3_UUID)

DEVICE_SW3_DPID             = 1
DEVICE_SW3_NAME             = DEVICE_SW3_UUID
DEVICE_SW3_IP_ADDR          = '10.0.2.10'
DEVICE_SW3_PORT             = '50003'
DEVICE_SW3_VENDOR           = 'Open Networking Foundation'
DEVICE_SW3_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW3_SW_VER           = 'Stratum'

DEVICE_SW3_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW3_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW3_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port')]
DEVICE_SW3_ENDPOINTS        = json_endpoints(DEVICE_SW3_ID, DEVICE_SW3_ENDPOINT_DEFS)
DEVICE_SW3_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW3_ID, DEVICE_SW3_ENDPOINT_DEFS)
ENDPOINT_ID_SW3_1           = DEVICE_SW3_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW3_2           = DEVICE_SW3_ENDPOINTS[1]['endpoint_id']

DEVICE_SW3_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW3_IP_ADDR,
    DEVICE_SW3_PORT,
    {
        'id':       DEVICE_SW3_DPID,
        'name':     DEVICE_SW3_NAME,
        'vendor':   DEVICE_SW3_VENDOR,
        'hw_ver':   DEVICE_SW3_HW_VER,
        'sw_ver':   DEVICE_SW3_SW_VER,
        'timeout':  DEVICE_SW3_TIMEOUT,
        'p4bin':    DEVICE_SW3_BIN_PATH,
        'p4info':   DEVICE_SW3_INFO_PATH
    }
)

DEVICE_SW4_UUID             = 'SW4'
DEVICE_SW4_TIMEOUT          = 60
DEVICE_SW4_ID               = json_device_id(DEVICE_SW4_UUID)
DEVICE_SW4                  = json_device_p4_disabled(DEVICE_SW4_UUID)

DEVICE_SW4_DPID             = 1
DEVICE_SW4_NAME             = DEVICE_SW4_UUID
DEVICE_SW4_IP_ADDR          = '10.0.2.10'
DEVICE_SW4_PORT             = '50004'
DEVICE_SW4_VENDOR           = 'Open Networking Foundation'
DEVICE_SW4_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW4_SW_VER           = 'Stratum'

DEVICE_SW4_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW4_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW4_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port')]
DEVICE_SW4_ENDPOINTS        = json_endpoints(DEVICE_SW4_ID, DEVICE_SW4_ENDPOINT_DEFS)
DEVICE_SW4_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW4_ID, DEVICE_SW4_ENDPOINT_DEFS)
ENDPOINT_ID_SW4_1           = DEVICE_SW4_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW4_2           = DEVICE_SW4_ENDPOINTS[1]['endpoint_id']

DEVICE_SW4_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW4_IP_ADDR,
    DEVICE_SW4_PORT,
    {
        'id':       DEVICE_SW4_DPID,
        'name':     DEVICE_SW4_NAME,
        'vendor':   DEVICE_SW4_VENDOR,
        'hw_ver':   DEVICE_SW4_HW_VER,
        'sw_ver':   DEVICE_SW4_SW_VER,
        'timeout':  DEVICE_SW4_TIMEOUT,
        'p4bin':    DEVICE_SW4_BIN_PATH,
        'p4info':   DEVICE_SW4_INFO_PATH
    }
)

DEVICE_SW5_UUID             = 'SW5'
DEVICE_SW5_TIMEOUT          = 60
DEVICE_SW5_ID               = json_device_id(DEVICE_SW5_UUID)
DEVICE_SW5                  = json_device_p4_disabled(DEVICE_SW5_UUID)

DEVICE_SW5_DPID             = 1
DEVICE_SW5_NAME             = DEVICE_SW5_UUID
DEVICE_SW5_IP_ADDR          = '10.0.2.10'
DEVICE_SW5_PORT             = '50005'
DEVICE_SW5_VENDOR           = 'Open Networking Foundation'
DEVICE_SW5_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW5_SW_VER           = 'Stratum'

DEVICE_SW5_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW5_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW5_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port')]
DEVICE_SW5_ENDPOINTS        = json_endpoints(DEVICE_SW5_ID, DEVICE_SW5_ENDPOINT_DEFS)
DEVICE_SW5_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW5_ID, DEVICE_SW5_ENDPOINT_DEFS)
ENDPOINT_ID_SW5_1           = DEVICE_SW5_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW5_2           = DEVICE_SW5_ENDPOINTS[1]['endpoint_id']

DEVICE_SW5_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW5_IP_ADDR,
    DEVICE_SW5_PORT,
    {
        'id':       DEVICE_SW5_DPID,
        'name':     DEVICE_SW5_NAME,
        'vendor':   DEVICE_SW5_VENDOR,
        'hw_ver':   DEVICE_SW5_HW_VER,
        'sw_ver':   DEVICE_SW5_SW_VER,
        'timeout':  DEVICE_SW5_TIMEOUT,
        'p4bin':    DEVICE_SW5_BIN_PATH,
        'p4info':   DEVICE_SW5_INFO_PATH
    }
)

DEVICE_SW6_UUID             = 'SW6'
DEVICE_SW6_TIMEOUT          = 60
DEVICE_SW6_ID               = json_device_id(DEVICE_SW6_UUID)
DEVICE_SW6                  = json_device_p4_disabled(DEVICE_SW6_UUID)

DEVICE_SW6_DPID             = 1
DEVICE_SW6_NAME             = DEVICE_SW6_UUID
DEVICE_SW6_IP_ADDR          = '10.0.2.10'
DEVICE_SW6_PORT             = '50006'
DEVICE_SW6_VENDOR           = 'Open Networking Foundation'
DEVICE_SW6_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW6_SW_VER           = 'Stratum'

DEVICE_SW6_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW6_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW6_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port'),
                               json_endpoint_descriptor('3', 'port')]
DEVICE_SW6_ENDPOINTS        = json_endpoints(DEVICE_SW6_ID, DEVICE_SW6_ENDPOINT_DEFS)
DEVICE_SW6_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW6_ID, DEVICE_SW6_ENDPOINT_DEFS)
ENDPOINT_ID_SW6_1           = DEVICE_SW6_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW6_2           = DEVICE_SW6_ENDPOINTS[1]['endpoint_id']
ENDPOINT_ID_SW6_3           = DEVICE_SW6_ENDPOINTS[2]['endpoint_id']

DEVICE_SW6_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW6_IP_ADDR,
    DEVICE_SW6_PORT,
    {
        'id':       DEVICE_SW6_DPID,
        'name':     DEVICE_SW6_NAME,
        'vendor':   DEVICE_SW6_VENDOR,
        'hw_ver':   DEVICE_SW6_HW_VER,
        'sw_ver':   DEVICE_SW6_SW_VER,
        'timeout':  DEVICE_SW6_TIMEOUT,
        'p4bin':    DEVICE_SW6_BIN_PATH,
        'p4info':   DEVICE_SW6_INFO_PATH
    }
)

# ----- Links ----------------------------------------------------------------------------------------------------------
LINK_SW1_SW2_UUID           = get_link_uuid(ENDPOINT_ID_SW1_1, ENDPOINT_ID_SW2_1)
LINK_SW1_SW2_ID             = json_link_id(LINK_SW1_SW2_UUID)
LINK_SW1_SW2                = json_link(LINK_SW1_SW2_UUID, [ENDPOINT_ID_SW1_1, ENDPOINT_ID_SW2_1])

LINK_SW1_SW3_UUID           = get_link_uuid(ENDPOINT_ID_SW1_2, ENDPOINT_ID_SW3_1)
LINK_SW1_SW3_ID             = json_link_id(LINK_SW1_SW3_UUID)
LINK_SW1_SW3                = json_link(LINK_SW1_SW3_UUID, [ENDPOINT_ID_SW1_2, ENDPOINT_ID_SW3_1])

LINK_SW2_SW4_UUID           = get_link_uuid(ENDPOINT_ID_SW2_2, ENDPOINT_ID_SW4_1)
LINK_SW2_SW4_ID             = json_link_id(LINK_SW2_SW4_UUID)
LINK_SW2_SW4                = json_link(LINK_SW2_SW4_UUID, [ENDPOINT_ID_SW2_2, ENDPOINT_ID_SW4_1])

LINK_SW3_SW5_UUID           = get_link_uuid(ENDPOINT_ID_SW3_2, ENDPOINT_ID_SW5_1)
LINK_SW3_SW5_ID             = json_link_id(LINK_SW3_SW5_UUID)
LINK_SW3_SW5                = json_link(LINK_SW3_SW5_UUID, [ENDPOINT_ID_SW3_2, ENDPOINT_ID_SW5_1])

LINK_SW4_SW6_UUID           = get_link_uuid(ENDPOINT_ID_SW4_2, ENDPOINT_ID_SW6_1)
LINK_SW4_SW6_ID             = json_link_id(LINK_SW4_SW6_UUID)
LINK_SW4_SW6                = json_link(LINK_SW4_SW6_UUID, [ENDPOINT_ID_SW4_2, ENDPOINT_ID_SW6_1])

LINK_SW5_SW6_UUID           = get_link_uuid(ENDPOINT_ID_SW5_2, ENDPOINT_ID_SW6_2)
LINK_SW5_SW6_ID             = json_link_id(LINK_SW5_SW6_UUID)
LINK_SW5_SW6                = json_link(LINK_SW5_SW6_UUID, [ENDPOINT_ID_SW5_2, ENDPOINT_ID_SW6_2])

# ----- Service ----------------------------------------------------------------------------------------------------------

SERVICE_SW1_SW6_UUID            = get_service_uuid(ENDPOINT_ID_SW1_3, ENDPOINT_ID_SW6_3)
SERVICE_SW1_SW6                 = json_service_p4_planned(SERVICE_SW1_SW6_UUID)
SERVICE_SW1_SW6_ENDPOINT_IDS    = [DEVICE_SW1_ENDPOINT_IDS[2], DEVICE_SW6_ENDPOINT_IDS[2]]

# ----- Object Collections ---------------------------------------------------------------------------------------------

CONTEXTS = [CONTEXT]
TOPOLOGIES = [TOPOLOGY]

DEVICES = [
    (DEVICE_SW1, DEVICE_SW1_CONNECT_RULES, DEVICE_SW1_ENDPOINTS),
    (DEVICE_SW2, DEVICE_SW2_CONNECT_RULES, DEVICE_SW2_ENDPOINTS),
    (DEVICE_SW3, DEVICE_SW3_CONNECT_RULES, DEVICE_SW3_ENDPOINTS),
    (DEVICE_SW4, DEVICE_SW4_CONNECT_RULES, DEVICE_SW4_ENDPOINTS),
    (DEVICE_SW5, DEVICE_SW5_CONNECT_RULES, DEVICE_SW5_ENDPOINTS),
    (DEVICE_SW6, DEVICE_SW6_CONNECT_RULES, DEVICE_SW6_ENDPOINTS),
]

LINKS = [
    LINK_SW1_SW2,
    LINK_SW1_SW3,

    LINK_SW2_SW4,
    LINK_SW3_SW5,

    LINK_SW4_SW6,
    LINK_SW5_SW6
    ]

SERVICES = [(SERVICE_SW1_SW6, SERVICE_SW1_SW6_ENDPOINT_IDS)]
