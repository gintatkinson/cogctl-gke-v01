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

from typing import Dict, List, Optional, Tuple
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Connection import json_connection, json_connection_id
from common.tools.object_factory.Constraint import json_constraint_custom, json_constraint_sla_latency
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Device import json_device_id, json_device_packetrouter_disabled
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_id
from common.tools.object_factory.Link import json_link, json_link_id
from common.tools.object_factory.Service import json_service_id, json_service_l3nm_planned
from common.tools.object_factory.Slice import json_slice_id, json_slice
from common.tools.object_factory.Topology import json_topology, json_topology_id
from common.tools.object_factory.PolicyRule import json_policyrule, json_policyrule_id


# ----- Context --------------------------------------------------------------------------------------------------------
CONTEXT_NAME = DEFAULT_CONTEXT_NAME
CONTEXT_ID   = json_context_id(CONTEXT_NAME)
CONTEXT      = json_context(CONTEXT_NAME, name=CONTEXT_NAME)


# ----- Topology -------------------------------------------------------------------------------------------------------
TOPOLOGY_NAME = DEFAULT_TOPOLOGY_NAME
TOPOLOGY_ID   = json_topology_id(TOPOLOGY_NAME, context_id=CONTEXT_ID)
TOPOLOGY      = json_topology(TOPOLOGY_NAME, context_id=CONTEXT_ID, name=TOPOLOGY_NAME)


# ----- KPI Sample Types -----------------------------------------------------------------------------------------------
PACKET_PORT_SAMPLE_TYPES = [
    KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED,
    KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED,
]


# ----- Device ---------------------------------------------------------------------------------------------------------
def compose_device(name : str, endpoint_names : List[str]) -> Tuple[str, Dict, Dict]:
    device_id = json_device_id(name)
    endpoints = [
        json_endpoint(device_id, endpoint_name, 'copper', topology_id=TOPOLOGY_ID,
            kpi_sample_types=PACKET_PORT_SAMPLE_TYPES)
        for endpoint_name in endpoint_names
    ]
    config_rules = [
        json_config_rule_set('dev/rsrc1/value', 'value1'),
        json_config_rule_set('dev/rsrc2/value', 'value2'),
        json_config_rule_set('dev/rsrc3/value', 'value3'),
    ]
    device = json_device_packetrouter_disabled(name, endpoints=endpoints, config_rules=config_rules)
    return name, device_id, device

DEVICE_R1_NAME, DEVICE_R1_ID, DEVICE_R1 = compose_device('R1', ['1.2', '1.3', '2.2', '2.3'])
DEVICE_R2_NAME, DEVICE_R2_ID, DEVICE_R2 = compose_device('R2', ['1.1', '1.3', '2.1', '2.3'])
DEVICE_R3_NAME, DEVICE_R3_ID, DEVICE_R3 = compose_device('R3', ['1.1', '1.2', '2.1', '2.2'])


# ----- Link -----------------------------------------------------------------------------------------------------------
def compose_link(
    name : str, endpoint_ids : List[Tuple[str, str]],
    total_capacity_gbps : Optional[float] = None, used_capacity_gbps : Optional[float] = None
) -> Tuple[str, Dict, Dict]:
    link_id = json_link_id(name)
    endpoint_ids = [
        json_endpoint_id(device_id, endpoint_name, topology_id=TOPOLOGY_ID)
        for device_id, endpoint_name in endpoint_ids
    ]
    link = json_link(
        name, endpoint_ids, total_capacity_gbps=total_capacity_gbps, used_capacity_gbps=used_capacity_gbps
    )
    return name, link_id, link

LINK_R1_R2_NAME, LINK_R1_R2_ID, LINK_R1_R2 = compose_link(
    'R1==R2', [(DEVICE_R1_ID, '1.2'), (DEVICE_R2_ID, '1.1')],
    total_capacity_gbps=100, # used_capacity_gbps=None => used_capacity_gbps=total_capacity_gbps
)
LINK_R2_R3_NAME, LINK_R2_R3_ID, LINK_R2_R3 = compose_link(
    'R2==R3', [(DEVICE_R2_ID, '1.3'), (DEVICE_R3_ID, '1.2')],
    total_capacity_gbps=100, # used_capacity_gbps=None => used_capacity_gbps=total_capacity_gbps
)
LINK_R1_R3_NAME, LINK_R1_R3_ID, LINK_R1_R3 = compose_link(
    'R1==R3', [(DEVICE_R1_ID, '1.3'), (DEVICE_R3_ID, '1.1')],
    total_capacity_gbps=100, # used_capacity_gbps=None => used_capacity_gbps=total_capacity_gbps
)


# ----- Service --------------------------------------------------------------------------------------------------------
def compose_service(
    name : str, endpoint_ids : List[Tuple[str, str]], latency_ms : float, jitter_us : float
) -> Tuple[str, Dict, Dict]:
    service_id = json_service_id(name, context_id=CONTEXT_ID)
    endpoint_ids = [
        json_endpoint_id(device_id, endpoint_name, topology_id=TOPOLOGY_ID)
        for device_id, endpoint_name in endpoint_ids
    ]
    constraints = [
        json_constraint_sla_latency(latency_ms),
        json_constraint_custom('jitter[us]',  str(jitter_us)),
    ]
    config_rules = [
        json_config_rule_set('svc/rsrc1/value', 'value7'),
        json_config_rule_set('svc/rsrc2/value', 'value8'),
        json_config_rule_set('svc/rsrc3/value', 'value9'),
    ]
    service = json_service_l3nm_planned(
        name, endpoint_ids=endpoint_ids, constraints=constraints, config_rules=config_rules)
    return name, service_id, service

SERVICE_R1_R2_NAME, SERVICE_R1_R2_ID, SERVICE_R1_R2 = compose_service(
    'R1-R2', [(DEVICE_R1_ID, '2.2'), (DEVICE_R2_ID, '2.1')], 15.2, 1.2)

SERVICE_R1_R3_NAME, SERVICE_R1_R3_ID, SERVICE_R1_R3 = compose_service(
    'R1-R3', [(DEVICE_R1_ID, '2.3'), (DEVICE_R3_ID, '2.1')], 5.8, 0.1)

SERVICE_R2_R3_NAME, SERVICE_R2_R3_ID, SERVICE_R2_R3 = compose_service(
    'R2-R3', [(DEVICE_R2_ID, '2.3'), (DEVICE_R3_ID, '2.2')], 23.1, 3.4)


# ----- Slice ----------------------------------------------------------------------------------------------------------
def compose_slice(
    name : str, endpoint_ids : List[Tuple[str, str]], latency_ms : float, jitter_us : float,
    service_ids : List[Dict] = [], subslice_ids : List[Dict] = [], owner : Optional[Dict] = None
) -> Tuple[str, Dict, Dict]:
    slice_id = json_slice_id(name, context_id=CONTEXT_ID)
    endpoint_ids = [
        json_endpoint_id(device_id, endpoint_name, topology_id=TOPOLOGY_ID)
        for device_id, endpoint_name in endpoint_ids
    ]
    constraints = [
        json_constraint_sla_latency(latency_ms),
        json_constraint_custom('jitter[us]',  str(jitter_us)),
    ]
    config_rules = [
        json_config_rule_set('svc/rsrc1/value', 'value7'),
        json_config_rule_set('svc/rsrc2/value', 'value8'),
        json_config_rule_set('svc/rsrc3/value', 'value9'),
    ]
    slice_ = json_slice(
        name, context_id=CONTEXT_ID, endpoint_ids=endpoint_ids, constraints=constraints, config_rules=config_rules,
        service_ids=service_ids, subslice_ids=subslice_ids, owner=owner)
    return name, slice_id, slice_

SLICE_R1_R3_NAME, SLICE_R1_R3_ID, SLICE_R1_R3 = compose_slice(
    'R1-R3', [(DEVICE_R1_ID, '2.3'), (DEVICE_R3_ID, '2.1')], 15.2, 1.2,
    service_ids=[SERVICE_R1_R2_ID, SERVICE_R2_R3_ID],
    subslice_ids=[], owner=None)


# ----- Connection -----------------------------------------------------------------------------------------------------
def compose_connection(
    name : str, service_id : Dict, endpoint_ids : List[Tuple[str, str]], sub_service_ids : List[Dict] = []
) -> Tuple[str, Dict, Dict]:
    connection_id = json_connection_id(name)
    endpoint_ids = [
        json_endpoint_id(device_id, endpoint_name, topology_id=TOPOLOGY_ID)
        for device_id, endpoint_name in endpoint_ids
    ]
    connection = json_connection(
        name, service_id=service_id, path_hops_endpoint_ids=endpoint_ids, sub_service_ids=sub_service_ids)
    return name, connection_id, connection

CONNECTION_R1_R3_NAME, CONNECTION_R1_R3_ID, CONNECTION_R1_R3 = compose_connection(
    'CON:R1/2.3-R3/2.1', SERVICE_R1_R3_ID, [
        (DEVICE_R1_ID, '2.3'),
        (DEVICE_R1_ID, '1.2'), (DEVICE_R2_ID, '1.1'),
        (DEVICE_R2_ID, '1.3'), (DEVICE_R3_ID, '1.2'),
        (DEVICE_R3_ID, '2.1')
    ], sub_service_ids=[SERVICE_R1_R2_ID, SERVICE_R2_R3_ID])


# ----- PolicyRule -------------------------------------------------------------------------------------------------------
POLICYRULE_NAME = 'my-device-policy'
POLICYRULE_ID   = json_policyrule_id(POLICYRULE_NAME)
POLICYRULE      = json_policyrule(POLICYRULE_NAME, policy_priority=1, policy_kpi_id='my-kpi-id')
