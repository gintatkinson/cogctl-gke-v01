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

import time
import uuid
import random
from common.proto import telemetry_frontend_pb2
from common.proto import kpi_manager_pb2
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from telemetry.database.TelemetryModel import Collector as CollectorModel


def create_collector_request():
    _create_collector_request                                = telemetry_frontend_pb2.Collector()
    _create_collector_request.collector_id.collector_id.uuid = str(uuid.uuid4())
    _create_collector_request.kpi_id.kpi_id.uuid             = '71d58648-bf47-49ac-996f-e63a9fbfead4' # must be primary key in kpi table
    # _create_collector_request.kpi_id.kpi_id.uuid             = str(uuid.uuid4())
    _create_collector_request.duration_s                     = float(random.randint(8, 16))
    _create_collector_request.interval_s                     = float(random.randint(2, 4))
    return _create_collector_request

def create_kpi_request():
    _create_kpi_request                                     = kpi_manager_pb2.KpiDescriptor()
    _create_kpi_request.kpi_id.kpi_id.uuid                  = str(uuid.uuid4())
    _create_kpi_request.kpi_description                     = 'KPI Description Test'
    _create_kpi_request.kpi_sample_type                     = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    _create_kpi_request.service_id.service_uuid.uuid        = 'SERV' 
    _create_kpi_request.device_id.device_uuid.uuid          = 'DEV'  
    _create_kpi_request.slice_id.slice_uuid.uuid            = 'SLC'  
    _create_kpi_request.endpoint_id.endpoint_uuid.uuid      = 'END'  
    _create_kpi_request.connection_id.connection_uuid.uuid  = 'CON'  
    # _create_kpi_request.link_id.link_id.uuid                = 'LNK'
    return _create_kpi_request

def create_kpi_id_request():
    _create_kpi_id_request             = kpi_manager_pb2.KpiId()
    _create_kpi_id_request.kpi_id.uuid = '71d58648-bf47-49ac-996f-e63a9fbfead4'
    return _create_kpi_id_request

def create_collector_id_request():
    _create_collector_id_request                   = telemetry_frontend_pb2.CollectorId()
    _create_collector_id_request.collector_id.uuid = '71d58648-bf47-49ac-996f-e63a9fbfead4'
    return _create_collector_id_request

def create_kpi_filter_request():
    # create a dict as follows: 'Key' = 'KpiModel' column name and 'Value' = filter to apply.
    _create_kpi_filter_request                    = dict()
    _create_kpi_filter_request['kpi_sample_type'] = 102
    _create_kpi_filter_request['kpi_id']          = '3a17230d-8e95-4afb-8b21-6965481aee5a'
    return _create_kpi_filter_request

def create_collector_filter_request():
    # create a dict as follows: 'Key' = 'KpiModel' column name and 'Value' = filter to apply.
    _create_kpi_filter_request                        = dict()
    _create_kpi_filter_request['sampling_interval_s'] = 3.0
    # _create_kpi_filter_request['kpi_id']              = '11e2c6c6-b507-40aa-ab3a-ffd41e7125f0'
    return _create_kpi_filter_request

def create_collector_model_object():
    # Create a new Collector instance
    collector_to_insert                     = CollectorModel()
    collector_to_insert.collector_id        = str(uuid.uuid4())
    collector_to_insert.kpi_id              = '3a17230d-8e95-4afb-8b21-6965481aee5a'
    collector_to_insert.collector           = "Test collector description"
    collector_to_insert.sampling_duration_s = 15
    collector_to_insert.sampling_interval_s = 3
    collector_to_insert.start_timestamp     = time.time()
    collector_to_insert.end_timestamp       = time.time()
    return collector_to_insert