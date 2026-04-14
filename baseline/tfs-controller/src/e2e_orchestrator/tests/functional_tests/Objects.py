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



DEVICE_R1_UUID             = 'R1'
DEVICE_R2_UUID             = 'R2'

DEVICE_R1_ID               = json_device_id(DEVICE_R1_UUID)
DEVICE_R1_ENDPOINT_DEFS    = [json_endpoint_descriptor('2/2', 'port')]
DEVICE_R2_ID               = json_device_id(DEVICE_R2_UUID)
DEVICE_R2_ENDPOINT_DEFS    = [json_endpoint_descriptor('2/2', 'port')]

DEVICE_R1_ENDPOINTS        = json_endpoints(DEVICE_R1_ID, DEVICE_R1_ENDPOINT_DEFS)
DEVICE_R2_ENDPOINTS        = json_endpoints(DEVICE_R2_ID, DEVICE_R2_ENDPOINT_DEFS)


DEVICE_R1_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_R1_ID, DEVICE_R1_ENDPOINT_DEFS)
ENDPOINT_ID_R1             = DEVICE_R1_ENDPOINTS[0]['endpoint_id']
DEVICE_R2_ENDPOINT_IDS     = json_endpoint_ids(DEVICE_R2_ID, DEVICE_R2_ENDPOINT_DEFS)
ENDPOINT_ID_R2             = DEVICE_R2_ENDPOINTS[0]['endpoint_id']


# ----- Service ----------------------------------------------------------------------------------------------------------


SERVICE_R1_R2_UUID          = get_service_uuid(ENDPOINT_ID_R1, ENDPOINT_ID_R2)
SERVICE_R1_R2               = json_service_p4_planned(SERVICE_R1_R2_UUID)
SERVICE_R1_R2_ENDPOINT_IDS  = [DEVICE_R1_ENDPOINT_IDS[0], DEVICE_R2_ENDPOINT_IDS[0]]


SERVICES = [
    (SERVICE_R1_R2, SERVICE_R1_R2_ENDPOINT_IDS)
]
