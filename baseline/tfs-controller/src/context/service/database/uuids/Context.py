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

from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from ._Builder import get_uuid_from_string, get_uuid_random

def context_get_uuid(
    context_id : ContextId, context_name : str = '', allow_random : bool = False, allow_default : bool = False
) -> str:
    context_uuid = context_id.context_uuid.uuid

    if len(context_uuid) > 0:
        return get_uuid_from_string(context_uuid)
    if len(context_name) > 0:
        return get_uuid_from_string(context_name)
    if allow_default:
        return get_uuid_from_string(DEFAULT_CONTEXT_NAME)
    if allow_random:
        return get_uuid_random()

    raise InvalidArgumentsException([
        ('context_id.context_uuid.uuid', context_uuid),
        ('name', context_name),
    ], extra_details=['At least one is required to produce a Context UUID'])
