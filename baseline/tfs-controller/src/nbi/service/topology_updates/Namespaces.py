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

import logging
from flask import request
from flask_socketio import Namespace, join_room, leave_room
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.proto.context_pb2 import TopologyId
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from .Constants import SIO_NAMESPACE, SIO_ROOM
from .TopoUpdatesThread import TopoUpdatesThread

LOGGER = logging.getLogger(__name__)

class TopoUpdatesServerNamespace(Namespace):
    def __init__(self):
        super().__init__(namespace=SIO_NAMESPACE)
        self._thread = TopoUpdatesThread(self)
        self._thread.start()

    def stop_thread(self) -> None:
        self._thread.stop()

    def on_connect(self, auth):
        MSG = '[on_connect] Client connect: sid={:s}, auth={:s}'
        LOGGER.info(MSG.format(str(request.sid), str(auth)))
        join_room(SIO_ROOM, namespace=SIO_NAMESPACE)

        LOGGER.debug('[on_connect] emitting topology snapshot...')

        context_id = json_context_id(DEFAULT_CONTEXT_NAME)
        topology_id = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id)

        try:
            context_client = ContextClient()
            topology_details = context_client.GetTopologyDetails(
                TopologyId(**topology_id)
            )
        except: # pylint: disable=bare-except
            MSG = 'Unable to retrieve topology snapshot: {:s}'
            LOGGER.exception(MSG.format(str(topology_id)))
        else:
            topology_snapshot = grpc_message_to_json_string(topology_details)
            self.emit('topology-snapshot', topology_snapshot)

    def on_disconnect(self, reason):
        MSG = '[on_disconnect] Client disconnect: sid={:s}, reason={:s}'
        LOGGER.info(MSG.format(str(request.sid), str(reason)))
        leave_room(SIO_ROOM, namespace=SIO_NAMESPACE)
