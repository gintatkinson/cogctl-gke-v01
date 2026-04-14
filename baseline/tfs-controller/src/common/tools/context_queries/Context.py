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

import grpc
from typing import Optional
from common.proto.context_pb2 import Context, ContextId, Empty
from common.tools.object_factory.Context import json_context
from context.client.ContextClient import ContextClient

def create_context(
    context_client : ContextClient, context_uuid : str, name : Optional[str] = None
) -> None:
    existing_context_ids = context_client.ListContextIds(Empty())
    existing_context_uuids = {context_id.context_uuid.uuid for context_id in existing_context_ids.context_ids}
    if context_uuid in existing_context_uuids: return
    context_client.SetContext(Context(**json_context(context_uuid, name=name)))

def get_context(context_client : ContextClient, context_uuid : str, rw_copy : bool = False) -> Optional[Context]:
    try:
        # pylint: disable=no-member
        context_id = ContextId()
        context_id.context_uuid.uuid = context_uuid
        ro_context = context_client.GetContext(context_id)
        if not rw_copy: return ro_context
        rw_context = Context()
        rw_context.CopyFrom(ro_context)
        return rw_context
    except grpc.RpcError:
        #LOGGER.exception('Unable to get Context({:s})'.format(str(context_uuid)))
        return None
