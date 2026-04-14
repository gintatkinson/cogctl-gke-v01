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

from typing import List, Optional, Tuple
from common.proto.context_pb2 import EndPointId

def endpointids_to_raw(traversed_endpoint_ids : List[EndPointId]) -> List[Tuple[str, str, Optional[str]]]:
    raw_endpoint_ids : List[Tuple[str, str, Optional[str]]] = []
    for endpoint_id in traversed_endpoint_ids:
        device_uuid   = endpoint_id.device_id.device_uuid.uuid
        endpoint_uuid = endpoint_id.endpoint_uuid.uuid
        topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
        if len(topology_uuid) == 0: topology_uuid = None
        endpoint_id_tuple = device_uuid, endpoint_uuid, topology_uuid
        raw_endpoint_ids.append(endpoint_id_tuple)
    return raw_endpoint_ids
