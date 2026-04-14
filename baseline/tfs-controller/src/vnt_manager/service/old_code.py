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
import json
import logging
import threading
import time
from websockets.sync.client import connect
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import ContextId, Empty, Link, LinkId, LinkList, TopologyId
from common.proto.vnt_manager_pb2 import VNTSubscriptionRequest, VNTSubscriptionReply
from common.proto.vnt_manager_pb2_grpc import VNTManagerServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json, grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from context.client.EventsCollector import EventsCollector
from .vntm_config_device import configure, deconfigure

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool("VNTManager", "RPC")

context_client: ContextClient = ContextClient()

JSON_ADMIN_CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
ADMIN_CONTEXT_ID = ContextId(**JSON_ADMIN_CONTEXT_ID)
ADMIN_TOPOLOGY_ID = TopologyId(**json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=JSON_ADMIN_CONTEXT_ID))

GET_EVENT_TIMEOUT = 0.5


class VNTMEventDispatcher(threading.Thread):
    def __init__(self, host, port) -> None:
        LOGGER.debug('Creating VNTM connector...')
        self.host = host
        self.port = port
        super().__init__(name='VNTMEventDispatcher', daemon=True)
        self._terminate = threading.Event()
        LOGGER.debug('VNTM connector created')

    def start(self) -> None:
        self._terminate.clear()
        return super().start()

    def stop(self):
        self._terminate.set()

    def send_msg(self, msg):
        try:
            self.websocket.send(msg)
        except Exception as e:
            LOGGER.exception('Unable to send message')

    def recv_msg(self):
        message = self.websocket.recv()
        return message

    def run(self) -> None:
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

        try:
            url = "ws://" + str(self.host) + ":" + str(self.port)
            LOGGER.info("Connecting to events server...: {:s}".format(url))
            self.websocket = connect(url)
        except Exception as ex:
            MSG = 'Error connecting to {:s}'
            LOGGER.exception(MSG.format(str(url)))
        else:
            LOGGER.info('Connected to {:s}'.format(url))
            context_id = json_context_id(DEFAULT_CONTEXT_NAME)
            topology_id = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id)
            
            try:
                topology_details = context_client.GetTopologyDetails(TopologyId(**topology_id))
            except Exception as ex:
                LOGGER.warning('No topology found')
            else:
                self.send_msg(grpc_message_to_json_string(topology_details))

            while not self._terminate.is_set():
                event = events_collector.get_event(block=True, timeout=GET_EVENT_TIMEOUT)
                if event is None: continue
                LOGGER.debug('Event type: {}'.format(event))
                topology_details = context_client.GetTopologyDetails(TopologyId(**topology_id))
                to_send = grpc_message_to_json_string(topology_details)
                self.send_msg(to_send)
        
            LOGGER.info('Exiting')
            events_collector.stop()


class VNTManagerServiceServicerImpl(VNTManagerServiceServicer):
    def __init__(self):
        LOGGER.debug("Creating Servicer...")
        LOGGER.debug("Servicer Created")
        self.links = []

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListVirtualLinks(self, request : Empty, context : grpc.ServicerContext) -> LinkList:
        links = context_client.ListLinks(Empty()).links
        return [link for link in links if link.virtual]

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetVirtualLink(self, request : LinkId, context : grpc.ServicerContext) -> Link:
        link = context_client.GetLink(request)
        return link if link.virtual else Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def SetVirtualLink(self, request : Link, context : grpc.ServicerContext) -> LinkId:
        try:
            LOGGER.info('SETTING virtual link')
            self.event_dispatcher.send_msg(grpc_message_to_json_string(request))
            # configure('CSGW1', 'xe5', 'CSGW2', 'xe5', 'ecoc2024-1')
            response = self.event_dispatcher.recv_msg()
            message_json = json.loads(response)
            link = Link(**message_json)
            context_client.SetLink(link)
        except Exception as e:
            MSG = 'Exception setting virtual link={:s}')
            LOGGER.exception(MSG.format(str(request.link_id.link_uuid.uuid)))
        return request.link_id

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RemoveVirtualLink(self, request : LinkId, context : grpc.ServicerContext) -> Empty:
        try:
            LOGGER.debug('Removing virtual link')
            self.event_dispatcher.send_msg(grpc_message_to_json_string(request))
            # deconfigure('CSGW1', 'xe5', 'CSGW2', 'xe5', 'ecoc2024-1')
            response = self.event_dispatcher.recv_msg()
            message_json = json.loads(response)
            link_id = LinkId(**message_json)
            context_client.RemoveLink(link_id)

            LOGGER.info('Removed')
        except Exception as e:
            MSG = 'Exception removing virtual link={:s}'
            LOGGER.exception(MSG.format(str(request.link_uuid.uuid)))
            return msg_error
        else:
            context_client.RemoveLink(request)
            LOGGER.info('Removed')

        return Empty()
