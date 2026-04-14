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
    json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled, json_device_id)
from common.tools.object_factory.EndPoint import json_endpoint_descriptor
from common.tools.object_factory.Link import json_link, json_link_id
from common.tools.object_factory.Topology import json_topology, json_topology_id
from .Tools import get_link_uuid, json_endpoint_ids

# ----- Context --------------------------------------------------------------------------------------------------------
D2_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
D2_CONTEXT    = json_context(DEFAULT_CONTEXT_NAME)

# ----- Topology -------------------------------------------------------------------------------------------------------
D2_TOPOLOGY_ID = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=D2_CONTEXT_ID)
D2_TOPOLOGY    = json_topology(DEFAULT_TOPOLOGY_NAME, context_id=D2_CONTEXT_ID)

# ----- Devices --------------------------------------------------------------------------------------------------------
# Assume all devices have the same architecture of endpoints
D2_DEVICE_ENDPOINT_DEFS = [
    # Trunk ports
    json_endpoint_descriptor('1/1', '25Gbps'),
    json_endpoint_descriptor('1/2', '25Gbps'),
    json_endpoint_descriptor('1/3', '25Gbps'),
    json_endpoint_descriptor('1/4', '25Gbps'),

    # Inter-domain ports
    json_endpoint_descriptor('2/1', '100Gbps'),
    json_endpoint_descriptor('2/2', '100Gbps'),

    # Access ports
    json_endpoint_descriptor('3/1', '10Gbps'),
    json_endpoint_descriptor('3/2', '10Gbps'),
    json_endpoint_descriptor('3/3', '10Gbps'),
    json_endpoint_descriptor('3/4', '10Gbps'),
    json_endpoint_descriptor('3/5', '10Gbps'),
    json_endpoint_descriptor('3/6', '10Gbps'),
    json_endpoint_descriptor('3/7', '10Gbps'),
    json_endpoint_descriptor('3/8', '10Gbps'),
]

D2_DEVICE_D2R1_UUID          = 'R1@D2'
D2_DEVICE_D2R1_ID            = json_device_id(D2_DEVICE_D2R1_UUID)
D2_DEVICE_D2R1               = json_device_emulated_packet_router_disabled(D2_DEVICE_D2R1_UUID)
D2_DEVICE_D2R1_CONNECT_RULES = json_device_emulated_connect_rules(D2_DEVICE_ENDPOINT_DEFS)

D2_DEVICE_D2R2_UUID          = 'R2@D2'
D2_DEVICE_D2R2_ID            = json_device_id(D2_DEVICE_D2R2_UUID)
D2_DEVICE_D2R2               = json_device_emulated_packet_router_disabled(D2_DEVICE_D2R2_UUID)
D2_DEVICE_D2R2_CONNECT_RULES = json_device_emulated_connect_rules(D2_DEVICE_ENDPOINT_DEFS)

D2_DEVICE_D2R3_UUID          = 'R3@D2'
D2_DEVICE_D2R3_ID            = json_device_id(D2_DEVICE_D2R3_UUID)
D2_DEVICE_D2R3               = json_device_emulated_packet_router_disabled(D2_DEVICE_D2R3_UUID)
D2_DEVICE_D2R3_CONNECT_RULES = json_device_emulated_connect_rules(D2_DEVICE_ENDPOINT_DEFS)

D2_DEVICE_D2R4_UUID          = 'R4@D2'
D2_DEVICE_D2R4_ID            = json_device_id(D2_DEVICE_D2R4_UUID)
D2_DEVICE_D2R4               = json_device_emulated_packet_router_disabled(D2_DEVICE_D2R4_UUID)
D2_DEVICE_D2R4_CONNECT_RULES = json_device_emulated_connect_rules(D2_DEVICE_ENDPOINT_DEFS)

# Virtual devices on remote domains
D2_DEVICE_D1R1_UUID          = 'R1@D1'
D2_DEVICE_D1R1_ID            = json_device_id(D2_DEVICE_D1R1_UUID)
D2_DEVICE_D1R1               = json_device_emulated_packet_router_disabled(D2_DEVICE_D1R1_UUID)
D2_DEVICE_D1R1_CONNECT_RULES = json_device_emulated_connect_rules(D2_DEVICE_ENDPOINT_DEFS)

D2_DEVICE_D1R4_UUID          = 'R4@D1'
D2_DEVICE_D1R4_ID            = json_device_id(D2_DEVICE_D1R4_UUID)
D2_DEVICE_D1R4               = json_device_emulated_packet_router_disabled(D2_DEVICE_D1R4_UUID)
D2_DEVICE_D1R4_CONNECT_RULES = json_device_emulated_connect_rules(D2_DEVICE_ENDPOINT_DEFS)

D2_ENDPOINT_IDS = {}
D2_ENDPOINT_IDS.update(json_endpoint_ids(D2_DEVICE_D2R1_ID, D2_DEVICE_ENDPOINT_DEFS))
D2_ENDPOINT_IDS.update(json_endpoint_ids(D2_DEVICE_D2R2_ID, D2_DEVICE_ENDPOINT_DEFS))
D2_ENDPOINT_IDS.update(json_endpoint_ids(D2_DEVICE_D2R3_ID, D2_DEVICE_ENDPOINT_DEFS))
D2_ENDPOINT_IDS.update(json_endpoint_ids(D2_DEVICE_D2R4_ID, D2_DEVICE_ENDPOINT_DEFS))
D2_ENDPOINT_IDS.update(json_endpoint_ids(D2_DEVICE_D1R1_ID, D2_DEVICE_ENDPOINT_DEFS))
D2_ENDPOINT_IDS.update(json_endpoint_ids(D2_DEVICE_D1R4_ID, D2_DEVICE_ENDPOINT_DEFS))


# ----- Links ----------------------------------------------------------------------------------------------------------
# Intra-domain links
D2_LINK_D2R1_D2R2_UUID = get_link_uuid(
    D2_ENDPOINT_IDS[D2_DEVICE_D2R1_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R2_UUID]['1/1'])
D2_LINK_D2R1_D2R2_ID   = json_link_id(D2_LINK_D2R1_D2R2_UUID)
D2_LINK_D2R1_D2R2      = json_link(D2_LINK_D2R1_D2R2_UUID, [
    D2_ENDPOINT_IDS[D2_DEVICE_D2R1_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R2_UUID]['1/1']])

D2_LINK_D2R2_D2R3_UUID = get_link_uuid(
    D2_ENDPOINT_IDS[D2_DEVICE_D2R2_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R3_UUID]['1/1'])
D2_LINK_D2R2_D2R3_ID   = json_link_id(D2_LINK_D2R2_D2R3_UUID)
D2_LINK_D2R2_D2R3      = json_link(D2_LINK_D2R2_D2R3_UUID, [
    D2_ENDPOINT_IDS[D2_DEVICE_D2R2_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R3_UUID]['1/1']])

D2_LINK_D2R3_D2R4_UUID = get_link_uuid(
    D2_ENDPOINT_IDS[D2_DEVICE_D2R3_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['1/1'])
D2_LINK_D2R3_D2R4_ID   = json_link_id(D2_LINK_D2R3_D2R4_UUID)
D2_LINK_D2R3_D2R4      = json_link(D2_LINK_D2R3_D2R4_UUID, [
    D2_ENDPOINT_IDS[D2_DEVICE_D2R3_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['1/1']])

D2_LINK_D2R4_D2R1_UUID = get_link_uuid(
    D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R1_UUID]['1/1'])
D2_LINK_D2R4_D2R1_ID   = json_link_id(D2_LINK_D2R4_D2R1_UUID)
D2_LINK_D2R4_D2R1      = json_link(D2_LINK_D2R4_D2R1_UUID, [
    D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['1/2'], D2_ENDPOINT_IDS[D2_DEVICE_D2R1_UUID]['1/1']])

# Inter-domain links
D2_LINK_D2R4_D1R1_UUID = get_link_uuid(
    D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['2/1'], D2_ENDPOINT_IDS[D2_DEVICE_D1R1_UUID]['2/1'])
D2_LINK_D2R4_D1R1_ID   = json_link_id(D2_LINK_D2R4_D1R1_UUID)
D2_LINK_D2R4_D1R1      = json_link(D2_LINK_D2R4_D1R1_UUID, [
    D2_ENDPOINT_IDS[D2_DEVICE_D2R4_UUID]['2/1'], D2_ENDPOINT_IDS[D2_DEVICE_D1R1_UUID]['2/1']])

# ----- Object Collections ---------------------------------------------------------------------------------------------

D2_CONTEXTS = [D2_CONTEXT]
D2_TOPOLOGIES = [D2_TOPOLOGY]

D2_DEVICES = [
    (D2_DEVICE_D2R1, D2_DEVICE_D2R1_CONNECT_RULES),
    (D2_DEVICE_D2R2, D2_DEVICE_D2R2_CONNECT_RULES),
    (D2_DEVICE_D2R3, D2_DEVICE_D2R3_CONNECT_RULES),
    (D2_DEVICE_D2R4, D2_DEVICE_D2R4_CONNECT_RULES),
    (D2_DEVICE_D1R1, D2_DEVICE_D1R1_CONNECT_RULES),
    (D2_DEVICE_D1R4, D2_DEVICE_D1R4_CONNECT_RULES),
]

D2_LINKS = [
    D2_LINK_D2R1_D2R2, D2_LINK_D2R2_D2R3, D2_LINK_D2R3_D2R4, D2_LINK_D2R4_D2R1,
    D2_LINK_D2R4_D1R1,
]
