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

import re
from enum import Enum
from typing import Any, Optional

# Enumeration classes are redundant with gRPC classes, but gRPC does not provide a programmatical method to retrieve
# the values it expects from strings containing the desired value symbol or its integer value, so a kind of mapping is
# required. Besides, ORM Models expect Enum classes in EnumeratedFields; we create specific and conveniently defined
# Enum classes to serve both purposes.

def grpc_to_enum(
    grpc_enum_class, orm_enum_class : Enum, grpc_enum_value, grpc_enum_prefix : Optional[str] = None,
    fail_if_not_found : bool = False
) -> Optional[Any]:
    enum_name = grpc_enum_class.Name(grpc_enum_value)
    _orig_enum_name = enum_name

    _orig_grpc_enum_prefix = grpc_enum_prefix
    if grpc_enum_prefix is None:
        grpc_enum_prefix = orm_enum_class.__name__.upper()
        #grpc_enum_prefix = re.sub(r'^ORM_(.+)$', r'\1', grpc_enum_prefix)
        #grpc_enum_prefix = re.sub(r'^(.+)ENUM$', r'\1', grpc_enum_prefix)
        #grpc_enum_prefix = grpc_enum_prefix + '_'
        grpc_enum_prefix = re.sub(r'^ORM_(.+)ENUM$', r'\1_', grpc_enum_prefix)

    if len(grpc_enum_prefix) > 0:
        enum_name = enum_name.replace(grpc_enum_prefix, '')

    orm_enum_value = orm_enum_class._member_map_.get(enum_name)
    if orm_enum_value is None and fail_if_not_found:
        MSG = 'Unable to map gRPC Enum Value ({:s} / {:s}) to ORM Enum Value; grpc_enum_prefix={:s}'
        raise Exception(MSG.format(str(grpc_enum_value), str(_orig_enum_name), str(_orig_grpc_enum_prefix)))
    return orm_enum_value
