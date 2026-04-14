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
from common.proto.kpi_manager_pb2 import KpiId

# ----------------------- "2nd" Iteration --------------------------------
def create_collector_id():
    _collector_id                   = telemetry_frontend_pb2.CollectorId()
    # _collector_id.collector_id.uuid = str(uuid.uuid4())
    _collector_id.collector_id.uuid = "efef4d95-1cf1-43c4-9742-95c283dddddd"
    return _collector_id

def create_collector_request():
    _create_collector_request                                = telemetry_frontend_pb2.Collector()
    # _create_collector_request.collector_id.collector_id.uuid = str(uuid.uuid4()) 
    _create_collector_request.collector_id.collector_id.uuid = "efef4d95-1cf1-43c4-9742-95c283dddddd"
    # _create_collector_request.kpi_id.kpi_id.uuid             = str(uuid.uuid4())
    # _create_collector_request.kpi_id.kpi_id.uuid             = "6e22f180-ba28-4641-b190-2287bf448888"
    _create_collector_request.kpi_id.kpi_id.uuid             = "8c5ca114-cdc7-4081-b128-b667fd159832"
    # _create_collector_request.duration_s                     = float(random.randint(8, 16))
    _create_collector_request.duration_s                     = float(random.randint(40, 60))
    _create_collector_request.interval_s                     = float(random.randint(5, 7))
    return _create_collector_request

def create_collector_filter():
    _create_collector_filter = telemetry_frontend_pb2.CollectorFilter()
    kpi_id_obj               = KpiId()
    # kpi_id_obj.kpi_id.uuid   = str(uuid.uuid4())
    kpi_id_obj.kpi_id.uuid   = "8c5ca114-cdc7-4081-b128-b667fd159832"
    _create_collector_filter.kpi_id.append(kpi_id_obj)
    return _create_collector_filter
