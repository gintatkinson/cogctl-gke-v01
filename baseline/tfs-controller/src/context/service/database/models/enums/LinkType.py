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
from common.proto.context_pb2 import LinkTypeEnum
from ._GrpcToEnum import grpc_to_enum

# IMPORTANT: Entries of enum class ORM_LinkTypeEnum should be named as in
#            the proto files removing the prefixes. For example, proto item
#            LinkTypeEnum.COPPER should be included as COPPER.
#            If item name does not match, automatic mapping of proto enums
#            to database enums will fail.
class ORM_LinkTypeEnum(enum.Enum):
    UNKNOWN    = LinkTypeEnum.LINKTYPE_UNKNOWN
    COPPER     = LinkTypeEnum.LINKTYPE_COPPER
    FIBER      = LinkTypeEnum.LINKTYPE_FIBER
    RADIO      = LinkTypeEnum.LINKTYPE_RADIO
    VIRTUAL    = LinkTypeEnum.LINKTYPE_VIRTUAL
    MANAGEMENT = LinkTypeEnum.LINKTYPE_MANAGEMENT
    REMOTE     = LinkTypeEnum.LINKTYPE_REMOTE

grpc_to_enum__link_type_enum = functools.partial(
    grpc_to_enum, LinkTypeEnum, ORM_LinkTypeEnum
)
