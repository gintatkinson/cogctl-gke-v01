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

from typing import Tuple
from common.proto.context_pb2 import SliceId
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from ._Builder import get_uuid_from_string, get_uuid_random
from .Context import context_get_uuid

def slice_get_uuid(
    slice_id : SliceId, slice_name : str = '', allow_random : bool = False
) -> Tuple[str, str]:
    context_uuid = context_get_uuid(slice_id.context_id, allow_random=False)
    raw_slice_uuid = slice_id.slice_uuid.uuid

    if len(raw_slice_uuid) > 0:
        return context_uuid, get_uuid_from_string(raw_slice_uuid, prefix_for_name=context_uuid)
    if len(slice_name) > 0:
        return context_uuid, get_uuid_from_string(slice_name, prefix_for_name=context_uuid)
    if allow_random:
        return context_uuid, get_uuid_random()

    raise InvalidArgumentsException([
        ('slice_id.slice_uuid.uuid', raw_slice_uuid),
        ('name', slice_name),
    ], extra_details=['At least one is required to produce a Slice UUID'])
