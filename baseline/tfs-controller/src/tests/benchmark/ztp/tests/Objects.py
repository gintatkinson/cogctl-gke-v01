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
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled,
    json_device_emulated_tapi_disabled, json_device_id, json_device_packetrouter_disabled, json_device_tapi_disabled)
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_descriptor, json_endpoint_id
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

# ----- Devices --------------------------------------------------------------------------------------------------------
DEVICE_ENDPOINT_DEFS = [json_endpoint_descriptor('13/0/0', 'optical'),
                        json_endpoint_descriptor('13/1/2', 'copper', sample_types=PACKET_PORT_SAMPLE_TYPES)]
DEVICE_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_ENDPOINT_DEFS)

# ----- Object Collections ---------------------------------------------------------------------------------------------
CONTEXTS = [CONTEXT]
TOPOLOGIES = [TOPOLOGY]

DEVICES = []
for x in range(1, 1000):
  DEVICE_UUID = 'EMU-' + str(x)
  DEVICE = json_device_emulated_packet_router_disabled(DEVICE_UUID)
  DEVICES.append((DEVICE, DEVICE_CONNECT_RULES))
