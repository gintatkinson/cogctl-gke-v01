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
    json_device_connect_rules, json_device_id, json_device_p4_disabled)
from common.tools.object_factory.Service import get_service_uuid, json_service_p4_planned
from common.tools.object_factory.EndPoint import json_endpoint_ids, json_endpoints
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
DEVICE_SW1_IP_ADDR          = '192.168.5.131'
DEVICE_SW1_PORT             = '50001'
DEVICE_SW1_VENDOR           = 'Open Networking Foundation'
DEVICE_SW1_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW1_SW_VER           = 'Stratum'

DEVICE_SW1_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW1_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW1_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port'),
                               json_endpoint_descriptor('3', 'port'),
                               json_endpoint_descriptor('4', 'port')]
DEVICE_SW1_ENDPOINTS        = json_endpoints(DEVICE_SW1_ID, DEVICE_SW1_ENDPOINT_DEFS)
DEVICE_SW1_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW1_ID, DEVICE_SW1_ENDPOINT_DEFS)
ENDPOINT_ID_SW1_1           = DEVICE_SW1_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW1_2           = DEVICE_SW1_ENDPOINTS[1]['endpoint_id']
ENDPOINT_ID_SW1_3           = DEVICE_SW1_ENDPOINTS[2]['endpoint_id']
ENDPOINT_ID_SW1_4           = DEVICE_SW1_ENDPOINTS[3]['endpoint_id']

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
DEVICE_SW2_IP_ADDR          = '192.168.5.131'
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
DEVICE_SW3_IP_ADDR          = '192.168.5.131'
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
DEVICE_SW4_IP_ADDR          = '192.168.5.131'
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
DEVICE_SW5_IP_ADDR          = '192.168.5.131'
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
DEVICE_SW6_IP_ADDR          = '192.168.5.131'
DEVICE_SW6_PORT             = '50006'
DEVICE_SW6_VENDOR           = 'Open Networking Foundation'
DEVICE_SW6_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW6_SW_VER           = 'Stratum'

DEVICE_SW6_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW6_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW6_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port')]
DEVICE_SW6_ENDPOINTS        = json_endpoints(DEVICE_SW6_ID, DEVICE_SW6_ENDPOINT_DEFS)
DEVICE_SW6_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW6_ID, DEVICE_SW6_ENDPOINT_DEFS)
ENDPOINT_ID_SW6_1           = DEVICE_SW6_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW6_2           = DEVICE_SW6_ENDPOINTS[1]['endpoint_id']

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

DEVICE_SW7_UUID             = 'SW7'
DEVICE_SW7_TIMEOUT          = 60
DEVICE_SW7_ID               = json_device_id(DEVICE_SW7_UUID)
DEVICE_SW7                  = json_device_p4_disabled(DEVICE_SW7_UUID)

DEVICE_SW7_DPID             = 1
DEVICE_SW7_NAME             = DEVICE_SW7_UUID
DEVICE_SW7_IP_ADDR          = '192.168.5.131'
DEVICE_SW7_PORT             = '50007'
DEVICE_SW7_VENDOR           = 'Open Networking Foundation'
DEVICE_SW7_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW7_SW_VER           = 'Stratum'

DEVICE_SW7_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW7_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW7_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port')]
DEVICE_SW7_ENDPOINTS        = json_endpoints(DEVICE_SW7_ID, DEVICE_SW7_ENDPOINT_DEFS)
DEVICE_SW7_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW7_ID, DEVICE_SW7_ENDPOINT_DEFS)
ENDPOINT_ID_SW7_1           = DEVICE_SW7_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW7_2           = DEVICE_SW7_ENDPOINTS[1]['endpoint_id']

DEVICE_SW7_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW7_IP_ADDR,
    DEVICE_SW7_PORT,
    {
        'id':       DEVICE_SW7_DPID,
        'name':     DEVICE_SW7_NAME,
        'vendor':   DEVICE_SW7_VENDOR,
        'hw_ver':   DEVICE_SW7_HW_VER,
        'sw_ver':   DEVICE_SW7_SW_VER,
        'timeout':  DEVICE_SW7_TIMEOUT,
        'p4bin':    DEVICE_SW7_BIN_PATH,
        'p4info':   DEVICE_SW7_INFO_PATH
    }
)

DEVICE_SW8_UUID             = 'SW8'
DEVICE_SW8_TIMEOUT          = 60
DEVICE_SW8_ID               = json_device_id(DEVICE_SW8_UUID)
DEVICE_SW8                  = json_device_p4_disabled(DEVICE_SW8_UUID)

DEVICE_SW8_DPID             = 1
DEVICE_SW8_NAME             = DEVICE_SW8_UUID
DEVICE_SW8_IP_ADDR          = '192.168.5.131'
DEVICE_SW8_PORT             = '50008'
DEVICE_SW8_VENDOR           = 'Open Networking Foundation'
DEVICE_SW8_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW8_SW_VER           = 'Stratum'

DEVICE_SW8_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW8_INFO_PATH        = '/root/p4/p4info.txt'

DEVICE_SW8_ENDPOINT_DEFS    = [json_endpoint_descriptor('1', 'port'),
                               json_endpoint_descriptor('2', 'port'),
                               json_endpoint_descriptor('3', 'port'),
                               json_endpoint_descriptor('4', 'port')]
DEVICE_SW8_ENDPOINTS        = json_endpoints(DEVICE_SW8_ID, DEVICE_SW8_ENDPOINT_DEFS)
DEVICE_SW8_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_SW8_ID, DEVICE_SW8_ENDPOINT_DEFS)
ENDPOINT_ID_SW8_1           = DEVICE_SW8_ENDPOINTS[0]['endpoint_id']
ENDPOINT_ID_SW8_2           = DEVICE_SW8_ENDPOINTS[1]['endpoint_id']
ENDPOINT_ID_SW8_3           = DEVICE_SW8_ENDPOINTS[2]['endpoint_id']
ENDPOINT_ID_SW8_4           = DEVICE_SW8_ENDPOINTS[3]['endpoint_id']

DEVICE_SW8_CONNECT_RULES    = json_device_connect_rules(
    DEVICE_SW8_IP_ADDR,
    DEVICE_SW8_PORT,
    {
        'id':       DEVICE_SW8_DPID,
        'name':     DEVICE_SW8_NAME,
        'vendor':   DEVICE_SW8_VENDOR,
        'hw_ver':   DEVICE_SW8_HW_VER,
        'sw_ver':   DEVICE_SW8_SW_VER,
        'timeout':  DEVICE_SW8_TIMEOUT,
        'p4bin':    DEVICE_SW8_BIN_PATH,
        'p4info':   DEVICE_SW8_INFO_PATH
    }
)

# ----- Links ----------------------------------------------------------------------------------------------------------

# Leftmost links (SW1-SW{2n})
# SW1_1 - SW2_1
LINK_SW1_SW2_UUID           = get_link_uuid(ENDPOINT_ID_SW1_1, ENDPOINT_ID_SW2_1)
LINK_SW1_SW2_ID             = json_link_id(LINK_SW1_SW2_UUID)
LINK_SW1_SW2                = json_link(LINK_SW1_SW2_UUID, [ENDPOINT_ID_SW1_1, ENDPOINT_ID_SW2_1])

# SW2_1 - SW1_1
LINK_SW2_SW1_UUID           = get_link_uuid(ENDPOINT_ID_SW2_1, ENDPOINT_ID_SW1_1)
LINK_SW2_SW1_ID             = json_link_id(LINK_SW2_SW1_UUID)
LINK_SW2_SW1                = json_link(LINK_SW2_SW1_UUID, [ENDPOINT_ID_SW2_1, ENDPOINT_ID_SW1_1])

# SW1_2 - SW4_1
LINK_SW1_SW4_UUID           = get_link_uuid(ENDPOINT_ID_SW1_2, ENDPOINT_ID_SW4_1)
LINK_SW1_SW4_ID             = json_link_id(LINK_SW1_SW4_UUID)
LINK_SW1_SW4                = json_link(LINK_SW1_SW4_UUID, [ENDPOINT_ID_SW1_2, ENDPOINT_ID_SW4_1])

# SW4_1 - SW1_2
LINK_SW4_SW1_UUID           = get_link_uuid(ENDPOINT_ID_SW4_1, ENDPOINT_ID_SW1_2)
LINK_SW4_SW1_ID             = json_link_id(LINK_SW4_SW1_UUID)
LINK_SW4_SW1                = json_link(LINK_SW4_SW1_UUID, [ENDPOINT_ID_SW4_1, ENDPOINT_ID_SW1_2])

# SW1_3 - SW6_1
LINK_SW1_SW6_UUID           = get_link_uuid(ENDPOINT_ID_SW1_3, ENDPOINT_ID_SW6_1)
LINK_SW1_SW6_ID             = json_link_id(LINK_SW1_SW6_UUID)
LINK_SW1_SW6                = json_link(LINK_SW1_SW6_UUID, [ENDPOINT_ID_SW1_3, ENDPOINT_ID_SW6_1])

# SW6_1 - SW1_3
LINK_SW6_SW1_UUID           = get_link_uuid(ENDPOINT_ID_SW6_1, ENDPOINT_ID_SW1_3)
LINK_SW6_SW1_ID             = json_link_id(LINK_SW6_SW1_UUID)
LINK_SW6_SW1                = json_link(LINK_SW6_SW1_UUID, [ENDPOINT_ID_SW6_1, ENDPOINT_ID_SW1_3])

# Middle links (SW{2n}-SW{2n+1})
# SW2_2 - SW3_1
LINK_SW2_SW3_UUID           = get_link_uuid(ENDPOINT_ID_SW2_2, ENDPOINT_ID_SW3_1)
LINK_SW2_SW3_ID             = json_link_id(LINK_SW2_SW3_UUID)
LINK_SW2_SW3                = json_link(LINK_SW2_SW3_UUID, [ENDPOINT_ID_SW2_2, ENDPOINT_ID_SW3_1])

# SW3_1 - SW2_2
LINK_SW3_SW2_UUID           = get_link_uuid(ENDPOINT_ID_SW3_1, ENDPOINT_ID_SW2_2)
LINK_SW3_SW2_ID             = json_link_id(LINK_SW3_SW2_UUID)
LINK_SW3_SW2                = json_link(LINK_SW3_SW2_UUID, [ENDPOINT_ID_SW3_1, ENDPOINT_ID_SW2_2])

# SW4_2 - SW5_1
LINK_SW4_SW5_UUID           = get_link_uuid(ENDPOINT_ID_SW4_2, ENDPOINT_ID_SW5_1)
LINK_SW4_SW5_ID             = json_link_id(LINK_SW4_SW5_UUID)
LINK_SW4_SW5                = json_link(LINK_SW4_SW5_UUID, [ENDPOINT_ID_SW4_2, ENDPOINT_ID_SW5_1])

# SW5_1 - SW4_2
LINK_SW5_SW4_UUID           = get_link_uuid(ENDPOINT_ID_SW5_1, ENDPOINT_ID_SW4_2)
LINK_SW5_SW4_ID             = json_link_id(LINK_SW5_SW4_UUID)
LINK_SW5_SW4                = json_link(LINK_SW5_SW4_UUID, [ENDPOINT_ID_SW5_1, ENDPOINT_ID_SW4_2])

# SW6_2 - SW7_1
LINK_SW6_SW7_UUID           = get_link_uuid(ENDPOINT_ID_SW6_2, ENDPOINT_ID_SW7_1)
LINK_SW6_SW7_ID             = json_link_id(LINK_SW6_SW7_UUID)
LINK_SW6_SW7                = json_link(LINK_SW6_SW7_UUID, [ENDPOINT_ID_SW6_2, ENDPOINT_ID_SW7_1])

# SW7_1 - SW6_2
LINK_SW7_SW6_UUID           = get_link_uuid(ENDPOINT_ID_SW7_1, ENDPOINT_ID_SW6_2)
LINK_SW7_SW6_ID             = json_link_id(LINK_SW7_SW6_UUID)
LINK_SW7_SW6                = json_link(LINK_SW7_SW6_UUID, [ENDPOINT_ID_SW7_1, ENDPOINT_ID_SW6_2])

# Rightmost links (SW{2n+1}-SW8)
# SW3_2 - SW8_1
LINK_SW3_SW8_UUID           = get_link_uuid(ENDPOINT_ID_SW3_2, ENDPOINT_ID_SW8_1)
LINK_SW3_SW8_ID             = json_link_id(LINK_SW3_SW8_UUID)
LINK_SW3_SW8                = json_link(LINK_SW3_SW8_UUID, [ENDPOINT_ID_SW3_2, ENDPOINT_ID_SW8_1])

# SW8_1 - SW3_2
LINK_SW8_SW3_UUID           = get_link_uuid(ENDPOINT_ID_SW8_1, ENDPOINT_ID_SW3_2)
LINK_SW8_SW3_ID             = json_link_id(LINK_SW8_SW3_UUID)
LINK_SW8_SW3                = json_link(LINK_SW8_SW3_UUID, [ENDPOINT_ID_SW8_1, ENDPOINT_ID_SW3_2])

# SW5_2 - SW8_2
LINK_SW5_SW8_UUID           = get_link_uuid(ENDPOINT_ID_SW5_2, ENDPOINT_ID_SW8_2)
LINK_SW5_SW8_ID             = json_link_id(LINK_SW5_SW8_UUID)
LINK_SW5_SW8                = json_link(LINK_SW5_SW8_UUID, [ENDPOINT_ID_SW5_2, ENDPOINT_ID_SW8_2])

# SW8_2 - SW8_2
LINK_SW8_SW5_UUID           = get_link_uuid(ENDPOINT_ID_SW8_2, ENDPOINT_ID_SW5_2)
LINK_SW8_SW5_ID             = json_link_id(LINK_SW8_SW5_UUID)
LINK_SW8_SW5                = json_link(LINK_SW8_SW5_UUID, [ENDPOINT_ID_SW8_2, ENDPOINT_ID_SW5_2])

# SW7_2 - SW8_3
LINK_SW7_SW8_UUID           = get_link_uuid(ENDPOINT_ID_SW7_2, ENDPOINT_ID_SW8_3)
LINK_SW7_SW8_ID             = json_link_id(LINK_SW7_SW8_UUID)
LINK_SW7_SW8                = json_link(LINK_SW7_SW8_UUID, [ENDPOINT_ID_SW7_2, ENDPOINT_ID_SW8_3])

# SW8_3 - SW7_2
LINK_SW8_SW7_UUID           = get_link_uuid(ENDPOINT_ID_SW8_3, ENDPOINT_ID_SW7_2)
LINK_SW8_SW7_ID             = json_link_id(LINK_SW8_SW7_UUID)
LINK_SW8_SW7                = json_link(LINK_SW8_SW7_UUID, [ENDPOINT_ID_SW8_3, ENDPOINT_ID_SW7_2])

# ----- Service ----------------------------------------------------------------------------------------------------------

SERVICE_SW1_SW8_UUID          = get_service_uuid(ENDPOINT_ID_SW1_4, ENDPOINT_ID_SW8_4)
SERVICE_SW1_SW8               = json_service_p4_planned(SERVICE_SW1_SW8_UUID)
SERVICE_SW1_SW8_ENDPOINT_IDS  = [DEVICE_SW1_ENDPOINT_IDS[3], DEVICE_SW8_ENDPOINT_IDS[3]]

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
    (DEVICE_SW7, DEVICE_SW7_CONNECT_RULES, DEVICE_SW7_ENDPOINTS),
    (DEVICE_SW8, DEVICE_SW8_CONNECT_RULES, DEVICE_SW8_ENDPOINTS),
]

LINKS = [
    LINK_SW1_SW2,
    LINK_SW1_SW4,
    LINK_SW1_SW6,

    LINK_SW2_SW3,
    LINK_SW4_SW5,
    LINK_SW6_SW7,

    LINK_SW3_SW8,
    LINK_SW5_SW8,
    LINK_SW7_SW8,

    LINK_SW2_SW1,
    LINK_SW4_SW1,
    LINK_SW6_SW1,

    LINK_SW3_SW2,
    LINK_SW5_SW4,
    LINK_SW7_SW6,

    LINK_SW8_SW3,
    LINK_SW8_SW5,
    LINK_SW8_SW7,
]

SERVICES = [
    (SERVICE_SW1_SW8, SERVICE_SW1_SW8_ENDPOINT_IDS),
]
