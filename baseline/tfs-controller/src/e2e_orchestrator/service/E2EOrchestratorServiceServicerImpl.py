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

import copy, grpc, logging, networkx
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.e2eorchestrator_pb2 import E2EOrchestratorRequest, E2EOrchestratorReply
from common.proto.context_pb2 import Empty, Connection, EndPointId
from common.proto.e2eorchestrator_pb2_grpc import E2EOrchestratorServiceServicer
from context.client.ContextClient import ContextClient
from context.service.database.uuids.EndPoint import endpoint_get_uuid

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool("E2EOrchestrator", "RPC")

class E2EOrchestratorServiceServicerImpl(E2EOrchestratorServiceServicer):
    def __init__(self):
        LOGGER.debug('Creating Servicer...')
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def Compute(
        self, request: E2EOrchestratorRequest, context: grpc.ServicerContext
    ) -> E2EOrchestratorReply:
        endpoints_ids = [
            endpoint_get_uuid(endpoint_id)[2]
            for endpoint_id in request.service.service_endpoint_ids
        ]

        graph = networkx.Graph()

        context_client = ContextClient()
        devices = context_client.ListDevices(Empty()).devices
        for device in devices:
            endpoints_uuids = [
                endpoint.endpoint_id.endpoint_uuid.uuid
                for endpoint in device.device_endpoints
            ]
            for ep in endpoints_uuids:
                graph.add_node(ep)

            for ep_i in endpoints_uuids:
                for ep_j in endpoints_uuids:
                    if ep_i == ep_j:
                        continue
                    graph.add_edge(ep_i, ep_j)

        links = context_client.ListLinks(Empty()).links
        for link in links:
            eps = []
            for endpoint_id in link.link_endpoint_ids:
                eps.append(endpoint_id.endpoint_uuid.uuid)
            graph.add_edge(eps[0], eps[1])


        shortest = networkx.shortest_path(
            graph, endpoints_ids[0], endpoints_ids[1]
        )

        path = E2EOrchestratorReply()
        path.services.append(copy.deepcopy(request.service))
        for i in range(0, int(len(shortest)/2)):
            conn = Connection()
            ep_a_uuid = str(shortest[i*2])
            ep_z_uuid = str(shortest[i*2+1])

            conn.connection_id.connection_uuid.uuid = str(ep_a_uuid) + '_->_' + str(ep_z_uuid)

            ep_a_id = EndPointId()
            ep_a_id.endpoint_uuid.uuid = ep_a_uuid
            conn.path_hops_endpoint_ids.append(ep_a_id)

            ep_z_id = EndPointId()
            ep_z_id.endpoint_uuid.uuid = ep_z_uuid
            conn.path_hops_endpoint_ids.append(ep_z_id)

            path.connections.append(conn)

        return path
