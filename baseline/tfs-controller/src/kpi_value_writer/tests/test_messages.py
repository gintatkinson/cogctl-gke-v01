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

import uuid, time
import random
from common.proto import kpi_manager_pb2
from common.proto.kpi_value_api_pb2 import KpiValue
from common.proto.kpi_sample_types_pb2 import KpiSampleType

def create_kpi_id_request():
    _create_kpi_id = kpi_manager_pb2.KpiId()
    _create_kpi_id.kpi_id.uuid = str(uuid.uuid4())
    return _create_kpi_id

def create_kpi_descriptor_request(description: str = "Test Description"):
    _create_kpi_request                                    = kpi_manager_pb2.KpiDescriptor()
    # _create_kpi_request.kpi_id.kpi_id.uuid                 = str(uuid.uuid4())
    _create_kpi_request.kpi_id.kpi_id.uuid                 = "efef4d95-1cf1-43c4-9742-95c283dddddd"
    _create_kpi_request.kpi_description                    = description
    _create_kpi_request.kpi_sample_type                    = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.device_id.device_uuid.uuid         = 'DEV4'  
    _create_kpi_request.service_id.service_uuid.uuid       = 'SERV3' 
    _create_kpi_request.slice_id.slice_uuid.uuid           = 'SLC3'  
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid     = 'END2'  
    _create_kpi_request.connection_id.connection_uuid.uuid = 'CON2'  
    _create_kpi_request.link_id.link_uuid.uuid             = 'LNK2'  
    return _create_kpi_request

def create_kpi_value_request():
    _create_kpi_value_request                         = KpiValue()
    _create_kpi_value_request.kpi_id.kpi_id.uuid      = str(uuid.uuid4())
    _create_kpi_value_request.timestamp.timestamp     = time.time()
    _create_kpi_value_request.kpi_value_type.floatVal = random.randint(10, 10000)
    return _create_kpi_value_request
