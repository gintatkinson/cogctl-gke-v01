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

import logging, socketio, threading
from common.proto.context_pb2 import TopologyId
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from .Constants import SIO_NAMESPACE, SIO_ROOM

LOGGER = logging.getLogger(__name__)

ADMIN_TOPOLOGY_ID = TopologyId(
    **json_topology_id(
        DEFAULT_TOPOLOGY_NAME,
        context_id=json_context_id(DEFAULT_CONTEXT_NAME)
    )
)

GET_EVENT_TIMEOUT = 1.0

class TopoUpdatesThread(threading.Thread):
    def __init__(self, namespace : socketio.Namespace):
        super().__init__(daemon=True)
        self._terminate = threading.Event()
        self._namespace = namespace

    def start(self):
        self._terminate.clear()
        return super().start()

    def stop(self) -> None:
        self._terminate.set()

    def run(self):
        LOGGER.info('[run] Starting...')
        try:
            context_client = ContextClient()
            events_collector = EventsCollector(
                context_client,
                log_events_received            = True,
                activate_context_collector     = True,
                activate_topology_collector    = True,
                activate_device_collector      = True,
                activate_link_collector        = True,
                activate_service_collector     = False,
                activate_slice_collector       = False,
                activate_connection_collector  = False,
            )
            events_collector.start()

            LOGGER.info('[run] Running...')
            while not self._terminate.is_set():
                event = events_collector.get_event(block=True, timeout=GET_EVENT_TIMEOUT)
                if event is None: continue
                MSG = '[run] Event: {:s}'
                LOGGER.debug(MSG.format(grpc_message_to_json_string(event)))

                # TODO: ideally, each event should trigger a notification containing
                # the type of event and the relevant data for the event. To simplify,
                # for now, the entire topology is sent.

                topology_details = context_client.GetTopologyDetails(ADMIN_TOPOLOGY_ID)
                topology_update = grpc_message_to_json_string(topology_details)

                LOGGER.debug('[run] checking server namespace...')
                server : socketio.Server = self._namespace.server
                if server is None: continue

                LOGGER.debug('[run] emitting topology update...')
                server.emit('topology-update', topology_update, namespace=SIO_NAMESPACE, to=SIO_ROOM)
                LOGGER.debug('[run] emitted')

            LOGGER.info('[run] Exiting')
            events_collector.stop()
        except: # pylint: disable=bare-except
            LOGGER.exception('[run] Unexpected Thread Exception')
        LOGGER.info('[run] Terminated')
