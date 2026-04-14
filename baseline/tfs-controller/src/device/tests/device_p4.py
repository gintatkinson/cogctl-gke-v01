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

"""
P4 device example configuration.
"""

import os
from common.tools.object_factory.ConfigRule import (
    json_config_rule_set, json_config_rule_delete)
from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_id, json_device_p4_disabled)

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

DEVICE_P4_DPID = 1
DEVICE_P4_NAME = 'device:leaf1'
DEVICE_P4_IP_ADDR = '127.0.0.1'
DEVICE_P4_PORT = '50101'
DEVICE_P4_VENDOR = 'Open Networking Foundation'
DEVICE_P4_HW_VER = 'BMv2 simple_switch'
DEVICE_P4_SW_VER = 'Stratum'
DEVICE_P4_BIN_PATH = os.path.join(CUR_PATH, 'p4/test-bmv2.json')
DEVICE_P4_INFO_PATH = os.path.join(CUR_PATH, 'p4/test-p4info.txt')
DEVICE_P4_WORKERS = 2
DEVICE_P4_GRACE_PERIOD = 60
DEVICE_P4_TIMEOUT = 60

DEVICE_P4_UUID = DEVICE_P4_NAME
DEVICE_P4_ID = json_device_id(DEVICE_P4_UUID)
DEVICE_P4 = json_device_p4_disabled(DEVICE_P4_UUID)

DEVICE_P4_CONNECT_RULES = json_device_connect_rules(
    DEVICE_P4_IP_ADDR,
    DEVICE_P4_PORT,
    {
        'id': DEVICE_P4_DPID,
        'name': DEVICE_P4_NAME,
        'vendor': DEVICE_P4_VENDOR,
        'hw_ver': DEVICE_P4_HW_VER,
        'sw_ver': DEVICE_P4_SW_VER,
        'timeout': DEVICE_P4_TIMEOUT,
        'p4bin': DEVICE_P4_BIN_PATH,
        'p4info': DEVICE_P4_INFO_PATH
    }
)

DEVICE_P4_CONFIG_TABLE_ENTRY = [
    json_config_rule_set(
        'table',
        {
            'table-name': 'IngressPipeImpl.acl_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:22 &&& ff:ff:ff:ff:ff:ff'
                }
            ],
            'action-name': 'IngressPipeImpl.clone_to_cpu',
            'action-params': [],
            'priority': 1
        }
    )
]

DEVICE_P4_DECONFIG_TABLE_ENTRY = [
    json_config_rule_delete(
        'table',
        {
            'table-name': 'IngressPipeImpl.acl_table',
            'match-fields': [
                {
                    'match-field': 'hdr.ethernet.dst_addr',
                    'match-value': 'aa:bb:cc:dd:ee:22 &&& ff:ff:ff:ff:ff:ff'
                }
            ],
            'action-name': 'IngressPipeImpl.clone_to_cpu',
            'action-params': [],
            'priority': 1
        }
    )
]
