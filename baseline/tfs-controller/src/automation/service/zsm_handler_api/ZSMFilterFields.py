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

from enum import Enum
from common.proto.context_pb2 import ServiceTypeEnum

class ZSMFilterFieldEnum(Enum):
    TARGET_SERVICE_TYPE  = 'target_service_type'
    TELEMETRY_SERVICE_TYPE = 'telemetry_service_type'

TARGET_SERVICE_TYPE_VALUES = {
    ServiceTypeEnum.SERVICETYPE_L2NM
}

TELEMETRY_SERVICE_TYPE_VALUES = {
    ServiceTypeEnum.SERVICETYPE_INT
}

# Maps filter fields to allowed values per Filter field. # If no restriction (free text) None is specified
ZSM_FILTER_FIELD_ALLOWED_VALUES = {
    ZSMFilterFieldEnum.TARGET_SERVICE_TYPE.value  : TARGET_SERVICE_TYPE_VALUES,
    ZSMFilterFieldEnum.TELEMETRY_SERVICE_TYPE.value : TELEMETRY_SERVICE_TYPE_VALUES,
}
