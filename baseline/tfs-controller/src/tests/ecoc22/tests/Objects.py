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

from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from tests.tools.mock_osm.Tools import connection_point, wim_mapping

# ----- WIM Service Settings -------------------------------------------------------------------------------------------
# PRI = primary // BKP = backup

SITE_ID_DC1   = 'DC1'
DEV_ID_DC1    = json_device_id('DC1-GW')
EP_ID_DC1_PRI = json_endpoint_id(DEV_ID_DC1, 'eth1')
EP_ID_DC1_BKP = json_endpoint_id(DEV_ID_DC1, 'eth2')
DEV_ID_CS1GW1 = json_device_id('CS1-GW1')
DEV_ID_CS1GW2 = json_device_id('CS1-GW2')

SITE_ID_DC2   = 'DC2'
DEV_ID_DC2    = json_device_id('DC2-GW')
EP_ID_DC2_PRI = json_endpoint_id(DEV_ID_DC2, 'eth1')
EP_ID_DC2_BKP = json_endpoint_id(DEV_ID_DC2, 'eth2')
DEV_ID_CS2GW1 = json_device_id('CS2-GW1')
DEV_ID_CS2GW2 = json_device_id('CS2-GW2')

WIM_SEP_DC1_PRI, WIM_MAP_DC1_PRI = wim_mapping(SITE_ID_DC1, EP_ID_DC1_PRI, DEV_ID_CS1GW1, priority=10, redundant=['DC1:DC1-GW:eth2'])
WIM_SEP_DC1_BKP, WIM_MAP_DC1_BKP = wim_mapping(SITE_ID_DC1, EP_ID_DC1_BKP, DEV_ID_CS1GW2, priority=20, redundant=['DC1:DC1-GW:eth1'])
WIM_SEP_DC2_PRI, WIM_MAP_DC2_PRI = wim_mapping(SITE_ID_DC2, EP_ID_DC2_PRI, DEV_ID_CS2GW1, priority=10, redundant=['DC2:DC2-GW:eth2'])
WIM_SEP_DC2_BKP, WIM_MAP_DC2_BKP = wim_mapping(SITE_ID_DC2, EP_ID_DC2_BKP, DEV_ID_CS2GW2, priority=20, redundant=['DC2:DC2-GW:eth1'])

WIM_MAPPING  = [
    WIM_MAP_DC1_PRI, WIM_MAP_DC1_BKP,
    WIM_MAP_DC2_PRI, WIM_MAP_DC2_BKP,
]

WIM_SRV_VLAN_ID = 300
WIM_SERVICE_TYPE = 'ELAN'
WIM_SERVICE_CONNECTION_POINTS = [
    connection_point(WIM_SEP_DC1_PRI, 'dot1q', WIM_SRV_VLAN_ID),
    connection_point(WIM_SEP_DC2_PRI, 'dot1q', WIM_SRV_VLAN_ID),
]
