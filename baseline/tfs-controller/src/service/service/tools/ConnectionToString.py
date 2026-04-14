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

from typing import List
from common.proto.context_pb2 import Connection

def connection_to_string(connection : Connection) -> str:
    str_device_endpoint_uuids : List[str] = list()
    for endpoint_id in connection.path_hops_endpoint_ids:
        device_uuid = endpoint_id.device_id.device_uuid.uuid
        endpoint_uuid = endpoint_id.endpoint_uuid.uuid
        device_endpoint_uuid = '{:s}:{:s}'.format(device_uuid, endpoint_uuid)
        str_device_endpoint_uuids.append(device_endpoint_uuid)
    return ','.join(str_device_endpoint_uuids)
