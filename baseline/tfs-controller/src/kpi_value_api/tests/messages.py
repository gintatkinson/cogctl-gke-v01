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
from common.proto import kpi_manager_pb2
from common.proto.kpi_value_api_pb2 import KpiValue, KpiValueList


def create_kpi_id_request():
    _create_kpi_id = kpi_manager_pb2.KpiId()
    _create_kpi_id.kpi_id.uuid = "6e22f180-ba28-4641-b190-2287bf448888"
    # _create_kpi_id.kpi_id.uuid = str(uuid.uuid4())
    return _create_kpi_id

def create_kpi_value_list():
    _create_kpi_value_list = KpiValueList()
    # To run this experiment sucessfully, add an existing UUID of a KPI Descriptor from the KPI DB.
    # This UUID is used to get the descriptor form the KPI DB. If the Kpi ID does not exists, 
    # some part of the code won't execute.
    EXISTING_KPI_IDs = ["725ce3ad-ac67-4373-bd35-8cd9d6a86e09",
                        str(uuid.uuid4()), 
                        str(uuid.uuid4())]

    for kpi_id_uuid in EXISTING_KPI_IDs:
        kpi_value_object = KpiValue()
        kpi_value_object.kpi_id.kpi_id.uuid      = kpi_id_uuid
        kpi_value_object.timestamp.timestamp     = float(time.time())
        kpi_value_object.kpi_value_type.floatVal = 100

        _create_kpi_value_list.kpi_value_list.append(kpi_value_object)

    return _create_kpi_value_list
