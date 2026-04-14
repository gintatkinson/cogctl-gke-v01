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
import random
from common.proto import telemetry_frontend_pb2
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.kpi_manager_pb2 import KpiDescriptor, KpiId

def create_collector_request():
    _create_collector_request                                = telemetry_frontend_pb2.Collector()
    _create_collector_request.collector_id.collector_id.uuid = str(uuid.uuid4()) 
    # _create_collector_request.collector_id.collector_id.uuid = "efef4d95-1cf1-43c4-9742-95c283dddddd"
    _create_collector_request.kpi_id.kpi_id.uuid             = str(uuid.uuid4())
    # _create_collector_request.kpi_id.kpi_id.uuid             = "6e22f180-ba28-4641-b190-2287bf448888"
    _create_collector_request.duration_s                     = float(random.randint(30, 50))
    # _create_collector_request.duration_s                     = -1
    _create_collector_request.interval_s                     = float(random.randint(2, 4)) 
    return _create_collector_request

def _create_kpi_descriptor(device_id : str = ""):
    _create_kpi_request                                    = KpiDescriptor()
    _create_kpi_request.kpi_id.kpi_id.uuid                 = str(uuid.uuid4())
    _create_kpi_request.kpi_description                    = "Test Description"
    _create_kpi_request.kpi_sample_type                    = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid         = device_id
    _create_kpi_request.service_id.service_uuid.uuid       = 'SERV3'
    _create_kpi_request.slice_id.slice_uuid.uuid           = 'SLC3' 
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid     = '36571df2-bac1-5909-a27d-5f42491d2ff0' 
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON2' 
    _create_kpi_request.link_id.link_uuid.uuid             = 'LNK2' 
    return _create_kpi_request

def _create_kpi_id(kpi_id : str = "fc046641-0c9a-4750-b4d9-9f98401714e2"):
    _create_kpi_id_request = KpiId()
    _create_kpi_id_request.kpi_id.uuid = kpi_id
    return _create_kpi_id_request
