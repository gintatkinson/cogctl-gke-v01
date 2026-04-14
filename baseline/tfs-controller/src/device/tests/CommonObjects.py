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
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Topology import json_topology, json_topology_id

# ----- Context --------------------------------------------------------------------------------------------------------
CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
CONTEXT    = json_context(DEFAULT_CONTEXT_NAME)


# ----- Topology -------------------------------------------------------------------------------------------------------
TOPOLOGY_ID = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)
TOPOLOGY    = json_topology(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)


# ----- KPI Sample Types -----------------------------------------------------------------------------------------------
PACKET_PORT_SAMPLE_TYPES = [
    KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED,
    KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED,
]
