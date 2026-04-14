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
from common.proto.context_pb2 import EndPointId
from common.method_wrappers.ServiceExceptions import InvalidArgumentsException
from ._Builder import get_uuid_from_string, get_uuid_random
from .Device import device_get_uuid
from .Topology import topology_get_uuid

def endpoint_get_uuid(
    endpoint_id : EndPointId, endpoint_name : str = '', allow_random : bool = False
) -> Tuple[str, str, str]:
    device_uuid = device_get_uuid(endpoint_id.device_id, allow_random=False)
    _,topology_uuid = topology_get_uuid(endpoint_id.topology_id, allow_random=False, allow_default=True)
    raw_endpoint_uuid = endpoint_id.endpoint_uuid.uuid

    if len(raw_endpoint_uuid) > 0:
        prefix_for_name = '{:s}/{:s}'.format(topology_uuid, device_uuid)
        return topology_uuid, device_uuid, get_uuid_from_string(raw_endpoint_uuid, prefix_for_name=prefix_for_name)
    if len(endpoint_name) > 0:
        prefix_for_name = '{:s}/{:s}'.format(topology_uuid, device_uuid)
        return topology_uuid, device_uuid, get_uuid_from_string(endpoint_name, prefix_for_name=prefix_for_name)
    if allow_random:
        return topology_uuid, device_uuid, get_uuid_random()

    raise InvalidArgumentsException([
        ('endpoint_id.endpoint_uuid.uuid', raw_endpoint_uuid),
        ('name', endpoint_name),
    ], extra_details=['At least one is required to produce a EndPoint UUID'])
