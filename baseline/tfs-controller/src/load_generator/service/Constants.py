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

from common.proto.load_generator_pb2 import RequestTypeEnum
from load_generator.load_gen.Constants import RequestType

REQUEST_TYPE_MAP = {
    RequestTypeEnum.REQUESTTYPE_SERVICE_L2NM : RequestType.SERVICE_L2NM,
    RequestTypeEnum.REQUESTTYPE_SERVICE_L3NM : RequestType.SERVICE_L3NM,
    RequestTypeEnum.REQUESTTYPE_SERVICE_MW   : RequestType.SERVICE_MW,
    RequestTypeEnum.REQUESTTYPE_SERVICE_TAPI : RequestType.SERVICE_TAPI,
    RequestTypeEnum.REQUESTTYPE_SLICE_L2NM   : RequestType.SLICE_L2NM,
    RequestTypeEnum.REQUESTTYPE_SLICE_L3NM   : RequestType.SLICE_L3NM,
}

REQUEST_TYPE_REVERSE_MAP = {v:k for k,v in REQUEST_TYPE_MAP.items()}
