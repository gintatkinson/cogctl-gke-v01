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

import uuid
from common.proto import kpi_manager_pb2
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from src.telemetry.backend.service.collectors.gnmi_oc.KPI import KPI

# Test device connection parameters
devices = {
    'device1': {
        'host': '10.1.1.86',
        'port': '6030',
        'username': 'ocnos',
        'password': 'ocnos',
        'insecure': True,
    },
    'device2': {
        'host': '10.1.1.87',
        'port': '6030',
        'username': 'ocnos',
        'password': 'ocnos',
        'insecure': True,
    },
    'device3': {
        'host': '172.20.20.101',
        'port': '6030',
        'username': 'admin',
        'password': 'admin',
        'insecure': True,
    },
}

def creat_basic_sub_request_parameters(
        resource: str = 'interface',
        endpoint: str = 'Management0',   # 'Ethernet1',
        kpi: KPI = KPI.PACKETS_RECEIVED, # It should be KPI Id not name? Need to be replaced with KPI id.
) -> dict:

    device = devices['device3']
    return {
        'target'            : (device['host'], device['port']),
        'username'          : device['username'],
        'password'          : device['password'],
        'connect_timeout'   : 15,
        'insecure'          : device['insecure'],
        'mode'              : 'on_change',            # Subscription internal mode posibly: on_change, poll, sample
        'sample_interval_ns': '3s',  
        'sample_interval'   : '10s',
        'kpi'               : kpi,
        'resource'          : resource,
        'endpoint'          : endpoint,
    }

def create_kpi_descriptor_request(descriptor_name: str = "Test_name"):
    _create_kpi_request                                    = kpi_manager_pb2.KpiDescriptor()
    # _create_kpi_request.kpi_id.kpi_id.uuid                 = str(uuid.uuid4())
    _create_kpi_request.kpi_id.kpi_id.uuid                 = "6e22f180-ba28-4641-b190-2287bf447777"
    _create_kpi_request.kpi_description                    = descriptor_name
    _create_kpi_request.kpi_sample_type                    = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    # _create_kpi_request.device_id.device_uuid.uuid         = str(uuid.uuid4())
    _create_kpi_request.device_id.device_uuid.uuid         = "a8695f53-ba2e-57bd-b586-edf2b5e054b1"
    _create_kpi_request.service_id.service_uuid.uuid       = 'SERV2'
    _create_kpi_request.slice_id.slice_uuid.uuid           = 'SLC1'
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid     = str(uuid.uuid4())
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON1' 
    _create_kpi_request.link_id.link_uuid.uuid             = 'LNK1' 
    return _create_kpi_request
