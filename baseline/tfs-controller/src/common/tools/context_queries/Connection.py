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

import grpc, logging
from typing import Optional
from common.proto.context_pb2 import Connection, ConnectionId
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

def get_connection_by_id(
    context_client : ContextClient, connection_id : ConnectionId, rw_copy : bool = False
) -> Optional[Connection]:
    try:
        ro_connection : Connection = context_client.GetConnection(connection_id)
        if not rw_copy: return ro_connection
        rw_connection = Connection()
        rw_connection.CopyFrom(ro_connection)
        return rw_connection
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.NOT_FOUND: raise # pylint: disable=no-member
        #connection_uuid = connection_id.connection_uuid.uuid
        #LOGGER.exception('Unable to get connection({:s})'.format(str(connection_uuid)))
        return None

def get_connection_by_uuid(
    context_client : ContextClient, connection_uuid : str, rw_copy : bool = False
) -> Optional[Connection]:
    # pylint: disable=no-member
    connection_id = ConnectionId()
    connection_id.connection_uuid.uuid = connection_uuid
    return get_connection_by_id(context_client, connection_id, rw_copy=rw_copy)
