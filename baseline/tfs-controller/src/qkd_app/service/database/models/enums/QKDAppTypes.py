# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import enum
import functools
from common.proto.qkd_app_pb2 import QKDAppTypesEnum
from ._GrpcToEnum import grpc_to_enum

# Enum mapping for ORM-based app types.
class ORM_QKDAppTypesEnum(enum.Enum):
    INTERNAL = QKDAppTypesEnum.QKDAPPTYPES_INTERNAL
    CLIENT = QKDAppTypesEnum.QKDAPPTYPES_CLIENT

# Function to map between gRPC and ORM enums.
grpc_to_enum__qkd_app_types = functools.partial(
    grpc_to_enum, QKDAppTypesEnum, ORM_QKDAppTypesEnum
)
