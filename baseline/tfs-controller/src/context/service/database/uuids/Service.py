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
from common.proto.context_pb2 import ServiceId
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from ._Builder import get_uuid_from_string, get_uuid_random
from .Context import context_get_uuid

def service_get_uuid(
    service_id : ServiceId, service_name : str = '', allow_random : bool = False
) -> Tuple[str, str]:
    context_uuid = context_get_uuid(service_id.context_id, allow_random=False)
    raw_service_uuid = service_id.service_uuid.uuid

    if len(raw_service_uuid) > 0:
        return context_uuid, get_uuid_from_string(raw_service_uuid, prefix_for_name=context_uuid)
    if len(service_name) > 0:
        return context_uuid, get_uuid_from_string(service_name, prefix_for_name=context_uuid)
    if allow_random:
        return context_uuid, get_uuid_random()

    raise InvalidArgumentsException([
        ('service_id.service_uuid.uuid', raw_service_uuid),
        ('name', service_name),
    ], extra_details=['At least one is required to produce a Service UUID'])
