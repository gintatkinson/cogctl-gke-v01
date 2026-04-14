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

from common.proto.dlt_gateway_pb2 import DLTRECORDOPERATION_UNDEFINED, DLTRECORDTYPE_UNDEFINED, DltRecord

def record_exists(record : DltRecord) -> bool:
    exists = True
    exists = exists and (len(record.record_id.domain_uuid.uuid) > 0)
    exists = exists and (record.record_id.type != DLTRECORDTYPE_UNDEFINED)
    exists = exists and (len(record.record_id.record_uuid.uuid) > 0)
    #exists = exists and (record.operation != DLTRECORDOPERATION_UNDEFINED)
    #exists = exists and (len(record.data_json) > 0) # It conflicts as sometimes records do not have a data_json.
    return exists
