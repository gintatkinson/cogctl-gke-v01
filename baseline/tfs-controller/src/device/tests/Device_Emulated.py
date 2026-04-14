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
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import (
    json_device_emulated_connect_rules, json_device_emulated_packet_router_disabled, json_device_id)
from common.tools.object_factory.EndPoint import json_endpoint_descriptor
from device.tests.CommonObjects import PACKET_PORT_SAMPLE_TYPES

DEVICE_EMU_UUID     = 'R1-EMU'
DEVICE_EMU_ID       = json_device_id(DEVICE_EMU_UUID)
DEVICE_EMU          = json_device_emulated_packet_router_disabled(DEVICE_EMU_UUID)
DEVICE_EMU_EP_UUIDS = ['EP1', 'EP2', 'EP3', 'EP4']
DEVICE_EMU_EP_DESCS = [
    json_endpoint_descriptor(ep_uuid, '10Gbps', sample_types=PACKET_PORT_SAMPLE_TYPES)
    for ep_uuid in DEVICE_EMU_EP_UUIDS
]
DEVICE_EMU_CONNECT_RULES = json_device_emulated_connect_rules(DEVICE_EMU_EP_DESCS)

RSRC_EP       = '/endpoints/endpoint[{:s}]'
RSRC_SUBIF    = RSRC_EP    + '/subinterfaces/subinterface[{:d}]'
RSRC_ADDRIPV4 = RSRC_SUBIF + '/ipv4/address[{:s}]'

DEVICE_EMU_ENDPOINTS_COOKED = []
for endpoint_data in DEVICE_EMU_EP_DESCS:
    endpoint_uuid = endpoint_data['uuid']
    endpoint_type = endpoint_data['type']
    endpoint_sample_types = endpoint_data['sample_types']
    endpoint_resource_key = RSRC_EP.format(str(endpoint_uuid))
    sample_types = {}
    for endpoint_sample_type in endpoint_sample_types:
        sample_type_name = KpiSampleType.Name(endpoint_sample_type).lower().replace('kpisampletype_', '')
        sample_types[endpoint_sample_type] = '{:s}/state/{:s}'.format(endpoint_resource_key, sample_type_name)
    endpoint_resource_value = {'uuid': endpoint_uuid, 'type': endpoint_type, 'sample_types': sample_types}
    DEVICE_EMU_ENDPOINTS_COOKED.append((endpoint_resource_key, endpoint_resource_value))

DEVICE_EMU_CONFIG_ENDPOINTS = [
    json_config_rule_set(RSRC_EP.format('EP1'), {'enabled' : True}),
    json_config_rule_set(RSRC_EP.format('EP2'), {'enabled' : True}),
    json_config_rule_set(RSRC_EP.format('EP3'), {'enabled' : True}),
    json_config_rule_set(RSRC_EP.format('EP4'), {'enabled' : True}),
]

DEVICE_EMU_CONFIG_ADDRESSES = [
    json_config_rule_set(RSRC_SUBIF   .format('EP1', 0), {'index': 0}),
    json_config_rule_set(RSRC_ADDRIPV4.format('EP1', 0, '10.1.0.1'), {'ip': '10.1.0.1', 'prefix_length': 24}),

    json_config_rule_set(RSRC_SUBIF   .format('EP2', 0), {'index': 0}),
    json_config_rule_set(RSRC_ADDRIPV4.format('EP2', 0, '10.2.0.1'), {'ip': '10.2.0.1', 'prefix_length': 24}),

    json_config_rule_set(RSRC_SUBIF   .format('EP3', 0), {'index': 0}),
    json_config_rule_set(RSRC_ADDRIPV4.format('EP3', 0, '10.3.0.1'), {'ip': '10.3.0.1', 'prefix_length': 24}),

    json_config_rule_set(RSRC_SUBIF   .format('EP4', 0), {'index': 0}),
    json_config_rule_set(RSRC_ADDRIPV4.format('EP4', 0, '10.4.0.1'), {'ip': '10.4.0.1', 'prefix_length': 24}),
]

DEVICE_EMU_RECONFIG_ADDRESSES = [
    json_config_rule_delete(RSRC_SUBIF   .format('EP2', 0), {}),
    json_config_rule_delete(RSRC_ADDRIPV4.format('EP2', 0, '10.2.0.1'), {'ip': '10.2.0.1', 'prefix_length': 24}),

    json_config_rule_set   (RSRC_SUBIF   .format('EP2', 1), {'index': 1}),
    json_config_rule_set   (RSRC_ADDRIPV4.format('EP2', 1, '10.2.1.1'), {'ip': '10.2.1.1', 'prefix_length': 24}),
]

DEVICE_EMU_DECONFIG_ADDRESSES = [
    json_config_rule_delete(RSRC_SUBIF   .format('EP1', 0), {}),
    json_config_rule_delete(RSRC_ADDRIPV4.format('EP1', 0, '10.1.0.1'), {}),

    json_config_rule_delete(RSRC_SUBIF   .format('EP2', 1), {}),
    json_config_rule_delete(RSRC_ADDRIPV4.format('EP2', 1, '10.2.1.1'), {}),

    json_config_rule_delete(RSRC_SUBIF   .format('EP3', 0), {}),
    json_config_rule_delete(RSRC_ADDRIPV4.format('EP3', 0, '10.3.0.1'), {}),

    json_config_rule_delete(RSRC_SUBIF   .format('EP4', 0), {}),
    json_config_rule_delete(RSRC_ADDRIPV4.format('EP4', 0, '10.4.0.1'), {}),
]

DEVICE_EMU_DECONFIG_ENDPOINTS = [
    json_config_rule_delete(RSRC_EP.format('EP1'), {}),
    json_config_rule_delete(RSRC_EP.format('EP2'), {}),
    json_config_rule_delete(RSRC_EP.format('EP3'), {}),
    json_config_rule_delete(RSRC_EP.format('EP4'), {}),
]
