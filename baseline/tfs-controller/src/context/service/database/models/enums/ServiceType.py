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

import enum, functools
from common.proto.context_pb2 import ServiceTypeEnum
from ._GrpcToEnum import grpc_to_enum

# IMPORTANT: Entries of enum class ORM_ServiceTypeEnum should be named as in
#            the proto files removing the prefixes. For example, proto item
#            ConfigActionEnum.CONFIGACTION_SET should be declared as SET.
#            If item name does not match, automatic mapping of proto enums to
#            database enums will fail.
class ORM_ServiceTypeEnum(enum.Enum):
    UNKNOWN                   = ServiceTypeEnum.SERVICETYPE_UNKNOWN
    L3NM                      = ServiceTypeEnum.SERVICETYPE_L3NM
    L2NM                      = ServiceTypeEnum.SERVICETYPE_L2NM
    TAPI_CONNECTIVITY_SERVICE = ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE
    TE                        = ServiceTypeEnum.SERVICETYPE_TE
    E2E                       = ServiceTypeEnum.SERVICETYPE_E2E
    OPTICAL_CONNECTIVITY      = ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY
    QKD                       = ServiceTypeEnum.SERVICETYPE_QKD
    L1NM                      = ServiceTypeEnum.SERVICETYPE_L1NM
    INT                       = ServiceTypeEnum.SERVICETYPE_INT
    ACL                       = ServiceTypeEnum.SERVICETYPE_ACL
    IP_LINK                   = ServiceTypeEnum.SERVICETYPE_IP_LINK
    IPOWDM                    = ServiceTypeEnum.SERVICETYPE_IPOWDM
    TAPI_LSP                  = ServiceTypeEnum.SERVICETYPE_TAPI_LSP

grpc_to_enum__service_type = functools.partial(
    grpc_to_enum, ServiceTypeEnum, ORM_ServiceTypeEnum)
