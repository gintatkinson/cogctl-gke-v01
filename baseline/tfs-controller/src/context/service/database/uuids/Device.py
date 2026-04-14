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

from common.proto.context_pb2 import DeviceId
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from ._Builder import get_uuid_from_string, get_uuid_random

def device_get_uuid(
    device_id : DeviceId, device_name : str = '', allow_random : bool = False
) -> str:
    device_uuid = device_id.device_uuid.uuid

    if len(device_uuid) > 0:
        return get_uuid_from_string(device_uuid)
    if len(device_name) > 0:
        return get_uuid_from_string(device_name)
    if allow_random: return get_uuid_random()

    raise InvalidArgumentsException([
        ('device_id.device_uuid.uuid', device_uuid),
        ('name', device_name),
    ], extra_details=['At least one is required to produce a Device UUID'])
