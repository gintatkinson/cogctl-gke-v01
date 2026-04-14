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

import copy, grpc, json, logging, networkx, requests, threading
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.e2eorchestrator_pb2 import E2EOrchestratorRequest, E2EOrchestratorReply
from common.proto.context_pb2 import (
    Empty, Connection, EndPointId, Link, LinkId, TopologyDetails, Topology, Context, Service, ServiceId,
    ServiceTypeEnum, ServiceStatusEnum)
from common.proto.e2eorchestrator_pb2_grpc import E2EOrchestratorServiceServicer
from common.proto.vnt_manager_pb2 import VNTSubscriptionRequest
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.Settings import get_setting
from context.client.ContextClient import ContextClient
from context.service.database.uuids.EndPoint import endpoint_get_uuid
from context.service.database.uuids.Device import device_get_uuid
from service.client.ServiceClient import ServiceClient
from websockets.sync.client import connect
from websockets.sync.server import serve


LOGGER = logging.getLogger(__name__)
logging.getLogger("websockets").propagate = True
logging.getLogger("requests.packages.urllib3").propagate = True

METRICS_POOL = MetricsPool("E2EOrchestrator", "RPC")


context_client: ContextClient = ContextClient()
service_client: ServiceClient = ServiceClient()

EXT_HOST = str(get_setting('WS_IP_HOST'))
EXT_PORT = int(get_setting('WS_IP_PORT'))
EXT_URL  = 'ws://{:s}:{:d}'.format(EXT_HOST, EXT_PORT)

OWN_HOST = str(get_setting('WS_E2E_HOST'))
OWN_PORT = int(get_setting('WS_E2E_PORT'))

ALL_HOSTS = '0.0.0.0'

class SubscriptionServer(threading.Thread):
    def run(self):
        request = VNTSubscriptionRequest()
        request.host = OWN_HOST
        request.port = OWN_PORT
        try: 
            LOGGER.debug('Trying to connect to {:s}'.format(EXT_URL))
            websocket = connect(EXT_URL)
        except: # pylint: disable=bare-except
            LOGGER.exception('Error connecting to {:s}'.format(EXT_URL))
        else:
            with websocket:
                LOGGER.debug('Connected to {:s}'.format(EXT_URL))
                send = grpc_message_to_json_string(request)
                websocket.send(send)
                LOGGER.debug('Sent: {:s}'.format(send))
                try:
                    message = websocket.recv()
                    LOGGER.debug('Received message from WebSocket: {:s}'.format(message))
                except Exception as ex:
                    LOGGER.error('Exception receiving from WebSocket: {:s}'.format(ex))
            self._events_server()


    def _events_server(self):
        try:
            server = serve(self._event_received, ALL_HOSTS, int(OWN_PORT))
        except: # pylint: disable=bare-except
            LOGGER.exception('Error starting server on {:s}:{:d}'.format(ALL_HOSTS, OWN_PORT))
        else:
            with server:
                LOGGER.info('Running events server...: {:s}:{:d}'.format(ALL_HOSTS, OWN_PORT))
                server.serve_forever()


    def _event_received(self, connection):
        LOGGER.debug('Event received')
        for message in connection:
            message_json = json.loads(message)

            # Link creation
            if 'link_id' in message_json:
                LOGGER.debug('Link creation')
                link = Link(**message_json)

                service = Service()
                service.service_id.service_uuid.uuid = link.link_id.link_uuid.uuid
                service.service_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
                service.service_type = ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY
                service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED
                service_client.CreateService(service)

                a_device_uuid = device_get_uuid(link.link_endpoint_ids[0].device_id)
                a_endpoint_uuid = endpoint_get_uuid(link.link_endpoint_ids[0])[2]
                z_device_uuid = device_get_uuid(link.link_endpoint_ids[1].device_id)
                z_endpoint_uuid = endpoint_get_uuid(link.link_endpoint_ids[1])[2]

                links = context_client.ListLinks(Empty()).links
                for _link in links:
                    for _endpoint_id in _link.link_endpoint_ids:
                        if _endpoint_id.device_id.device_uuid.uuid == a_device_uuid and \
                        _endpoint_id.endpoint_uuid.uuid == a_endpoint_uuid:
                            a_ep_id = _endpoint_id
                        elif _endpoint_id.device_id.device_uuid.uuid == z_device_uuid and \
                        _endpoint_id.endpoint_uuid.uuid == z_endpoint_uuid:
                            z_ep_id = _endpoint_id

                if (not 'a_ep_id' in locals()) or (not 'z_ep_id' in locals()):
                    error_msg = f'Could not get VNT link endpoints\
                                    \n\ta_endpoint_uuid= {a_endpoint_uuid}\
                                    \n\tz_endpoint_uuid= {z_device_uuid}'
                    LOGGER.error(error_msg)
                    connection.send(error_msg)
                    return

                service.service_endpoint_ids.append(copy.deepcopy(a_ep_id))
                service.service_endpoint_ids.append(copy.deepcopy(z_ep_id))

                service_client.UpdateService(service)
                re_svc = context_client.GetService(service.service_id)
                connection.send(grpc_message_to_json_string(link))
                context_client.SetLink(link)
            elif 'link_uuid' in message_json:
                LOGGER.debug('Link removal')
                link_id = LinkId(**message_json)

                service_id = ServiceId()
                service_id.service_uuid.uuid = link_id.link_uuid.uuid
                service_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
                service_client.DeleteService(service_id)
                connection.send(grpc_message_to_json_string(link_id))
                context_client.RemoveLink(link_id)
            else:
                LOGGER.debug('Topology received')
                topology_details = TopologyDetails(**message_json)

                context = Context()
                context.context_id.context_uuid.uuid = topology_details.topology_id.context_id.context_uuid.uuid
                context_client.SetContext(context)

                topology = Topology()
                topology.topology_id.context_id.CopyFrom(context.context_id)
                topology.topology_id.topology_uuid.uuid = topology_details.topology_id.topology_uuid.uuid
                context_client.SetTopology(topology)

                for device in topology_details.devices:
                    context_client.SetDevice(device)

                for link in topology_details.links:
                    context_client.SetLink(link)
