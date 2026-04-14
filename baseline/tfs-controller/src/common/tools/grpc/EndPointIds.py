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


from typing import Optional
from common.proto.context_pb2 import EndPointId

def update_endpoint_ids(
    endpoint_ids, device_uuid : str, endpoint_uuid : str,
    context_uuid : Optional[str] = None, topology_uuid : Optional[str] = None
) -> EndPointId:
    for endpoint_id in endpoint_ids:
        if endpoint_id.endpoint_uuid.uuid != endpoint_uuid: continue
        if endpoint_id.device_id.device_uuid.uuid != device_uuid: continue
        topology_id = endpoint_id.topology_id
        if topology_uuid is not None and topology_id.topology_uuid.uuid != topology_uuid: continue
        if context_uuid is not None and topology_id.context_id.context_uuid.uuid != context_uuid: continue
        break   # found, do nothing
    else:
        # not found, add it
        endpoint_id = endpoint_ids.add()    # pylint: disable=no-member
        endpoint_id.endpoint_uuid.uuid = endpoint_uuid
        endpoint_id.device_id.device_uuid.uuid = device_uuid
        if topology_uuid is not None: endpoint_id.topology_id.topology_uuid.uuid = topology_uuid
        if context_uuid is not None: endpoint_id.topology_id.context_id.context_uuid.uuid = context_uuid
    return endpoint_id

def copy_endpoint_ids(source_endpoint_ids, target_endpoint_ids):
    for source_endpoint_id in source_endpoint_ids:
        device_uuid = source_endpoint_id.device_id.device_uuid.uuid
        endpoint_uuid = source_endpoint_id.endpoint_uuid.uuid
        source_topology_id = source_endpoint_id.topology_id
        context_uuid = source_topology_id.context_id.context_uuid.uuid
        topology_uuid = source_topology_id.topology_uuid.uuid
        update_endpoint_ids(
            target_endpoint_ids, device_uuid, endpoint_uuid, context_uuid=context_uuid, topology_uuid=topology_uuid)
