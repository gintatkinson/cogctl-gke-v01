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

from common.proto.context_pb2 import ServiceTypeEnum
from ..zsm_handler_api.ZSMFilterFields import ZSMFilterFieldEnum
from automation.service.zsm_handlers.P4INTZSMPlugin import P4INTZSMPlugin

ZSM_SERVICE_HANDLERS = [
    (P4INTZSMPlugin, [
        {
            ZSMFilterFieldEnum.TARGET_SERVICE_TYPE  : ServiceTypeEnum.SERVICETYPE_L2NM,
            ZSMFilterFieldEnum.TELEMETRY_SERVICE_TYPE : ServiceTypeEnum.SERVICETYPE_INT,
        }
    ])
]
