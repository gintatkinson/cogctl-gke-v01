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
from common.proto.context_pb2 import SliceStatusEnum
from ._GrpcToEnum import grpc_to_enum

# IMPORTANT: Entries of enum class ORM_SliceStatusEnum should be named as in
#            the proto file but removing the prefixes. For example, proto item
#            SliceStatusEnum.SLICESTATUS_PLANNED should be declared as PLANNED.
#            If item name does not match, automatic mapping of proto enums to
#            database enums will fail.
class ORM_SliceStatusEnum(enum.Enum):
    UNDEFINED = SliceStatusEnum.SLICESTATUS_UNDEFINED
    PLANNED   = SliceStatusEnum.SLICESTATUS_PLANNED
    INIT      = SliceStatusEnum.SLICESTATUS_INIT
    ACTIVE    = SliceStatusEnum.SLICESTATUS_ACTIVE
    DEINIT    = SliceStatusEnum.SLICESTATUS_DEINIT

grpc_to_enum__slice_status = functools.partial(
    grpc_to_enum, SliceStatusEnum, ORM_SliceStatusEnum)
