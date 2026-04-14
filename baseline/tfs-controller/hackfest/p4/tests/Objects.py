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
from common.tools.object_factory.ConfigRule import (
    json_config_rule_set, json_config_rule_delete)
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_id
from common.tools.object_factory.Link import json_link, json_link_id
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
DEVICE_SW1_IP_ADDR          = 'localhost'
DEVICE_SW1_PORT             = '50001'
DEVICE_SW1_VENDOR           = 'Open Networking Foundation'
DEVICE_SW1_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW1_SW_VER           = 'Stratum'

DEVICE_SW1_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW1_INFO_PATH        = '/root/p4/p4info.txt'

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
DEVICE_SW2_IP_ADDR          = 'localhost'
DEVICE_SW2_PORT             = '50002'
DEVICE_SW2_VENDOR           = 'Open Networking Foundation'
DEVICE_SW2_HW_VER           = 'BMv2 simple_switch'
DEVICE_SW2_SW_VER           = 'Stratum'

DEVICE_SW2_BIN_PATH         = '/root/p4/bmv2.json'
DEVICE_SW2_INFO_PATH        = '/root/p4/p4info.txt'

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

################################## TABLE ENTRIES ##################################

DEVICE_SW1_CONFIG_TABLE_ENTRIES = [
    json_config_rule_set(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_exact_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:11'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '1'
                }
            ]
        }
    ),
    json_config_rule_set(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_exact_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:22'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '2'
                }
            ]
        }
    )
]

DEVICE_SW2_CONFIG_TABLE_ENTRIES = DEVICE_SW1_CONFIG_TABLE_ENTRIES 


"""
DEVICE_SW1_CONFIG_TABLE_ENTRIES = [
    json_config_rule_set(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_ternary_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:11 &&& ff:ff:ff:ff:ff:ff'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '1'
                }
            ],
            'priority': 1
        }
    ),
    json_config_rule_set(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_ternary_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:22 &&& ff:ff:ff:ff:ff:ff'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '2'
                }
            ],   
            'priority': 1
        }
    ),
]
"""

################################## TABLE DECONF ##################################

DEVICE_SW1_DECONF_TABLE_ENTRIES = [
    json_config_rule_delete(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_exact_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:11'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '1'
                }
            ]
        }
    ),
    json_config_rule_delete(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_exact_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:22'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '2'
                }
            ]
        }
    )
]

DEVICE_SW2_DECONF_TABLE_ENTRIES = DEVICE_SW1_DECONF_TABLE_ENTRIES 


"""
DEVICE_SW1_DECONF_TABLE_ENTRIES = [
    json_config_rule_delete(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_ternary_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:11 &&& ff:ff:ff:ff:ff:ff'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '1'
                }
            ],
            'priority': 1
        }
    ),
    json_config_rule_delete(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_ternary_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:22 &&& ff:ff:ff:ff:ff:ff'
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port_num',
                    'action-value': '2'
                }
            ],   
            'priority': 1
        }
    ),
]
"""

# ----- Links ----------------------------------------------------------------------------------------------------------

# ----- WIM Service Settings -------------------------------------------------------------------------------------------

# ----- Object Collections ---------------------------------------------------------------------------------------------

CONTEXTS = [CONTEXT]
TOPOLOGIES = [TOPOLOGY]

DEVICES = [
    (DEVICE_SW1, DEVICE_SW1_CONNECT_RULES, DEVICE_SW1_CONFIG_TABLE_ENTRIES, DEVICE_SW1_DECONF_TABLE_ENTRIES),
    (DEVICE_SW2, DEVICE_SW2_CONNECT_RULES, DEVICE_SW2_CONFIG_TABLE_ENTRIES, DEVICE_SW2_DECONF_TABLE_ENTRIES),
]

LINKS = []
