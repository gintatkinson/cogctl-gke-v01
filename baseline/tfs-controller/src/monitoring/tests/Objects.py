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

from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.object_factory.Device import (
    json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled)
from common.tools.object_factory.EndPoint import json_endpoint_descriptor

PACKET_PORT_SAMPLE_TYPES = [
    KpiSampleType.KPISAMPLETYPE_PACKETS_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED,
    KpiSampleType.KPISAMPLETYPE_BYTES_TRANSMITTED,
    KpiSampleType.KPISAMPLETYPE_BYTES_RECEIVED,
]

DEVICE_DEV1_UUID          = 'DEV1'
ENDPOINT_END1_UUID        = 'END1'
DEVICE_DEV1_ENDPOINT_DEFS = [
    json_endpoint_descriptor(ENDPOINT_END1_UUID, 'copper', sample_types=PACKET_PORT_SAMPLE_TYPES)
]
DEVICE_DEV1               = json_device_emulated_packet_router_disabled(DEVICE_DEV1_UUID)
DEVICE_DEV1_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_DEV1_ENDPOINT_DEFS)
