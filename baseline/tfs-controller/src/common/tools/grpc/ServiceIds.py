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

# RFC 8466 - L2VPN Service Model (L2SM)
# Ref: https://datatracker.ietf.org/doc/html/rfc8466


from common.proto.context_pb2 import ServiceId

def update_service_ids(service_ids, context_uuid : str, service_uuid : str) -> ServiceId:
    for service_id in service_ids:
        if service_id.service_uuid.uuid != service_uuid: continue
        if service_id.context_id.context_uuid.uuid != context_uuid: continue
        break   # found, do nothing
    else:
        # not found, add it
        service_id = service_ids.add()    # pylint: disable=no-member
        service_id.service_uuid.uuid = service_uuid
        service_id.context_id.context_uuid.uuid = context_uuid
    return service_id

def copy_service_ids(source_service_ids, target_service_ids):
    for source_service_id in source_service_ids:
        context_uuid = source_service_id.context_id.context_uuid.uuid
        service_uuid = source_service_id.service_uuid.uuid
        update_service_ids(target_service_ids, context_uuid, service_uuid)
