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

import grpc, logging, threading
#from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
#from common.proto.context_pb2 import ContextId, Empty, TopologyId
from common.proto.pathcomp_pb2 import PathCompReply, PathCompRequest
from common.proto.pathcomp_pb2_grpc import PathCompServiceServicer
#from common.tools.context_queries.Device import get_devices_in_topology
#from common.tools.context_queries.Link import get_links_in_topology
#from common.tools.context_queries.InterDomain import is_inter_domain
from common.tools.grpc.Tools import grpc_message_to_json_string
from pathcomp.frontend.Config import is_forecaster_enabled
#from common.tools.object_factory.Context import json_context_id
#from common.tools.object_factory.Topology import json_topology_id
#from context.client.ContextClient import ContextClient
from pathcomp.frontend.service.TopologyTools import get_pathcomp_topology_details
from pathcomp.frontend.service.algorithms.Factory import get_algorithm

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('PathComp', 'RPC')

#ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))

class PathCompServiceServicerImpl(PathCompServiceServicer):
    def __init__(self) -> None:
        LOGGER.debug('Creating Servicer...')
        self._lock = threading.Lock()
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def Compute(self, request : PathCompRequest, context : grpc.ServicerContext) -> PathCompReply:
        LOGGER.debug('[Compute] begin ; request = {:s}'.format(grpc_message_to_json_string(request)))

        #context_client = ContextClient()
        # TODO: improve definition of topologies; for interdomain the current topology design might be not convenient
        #if (len(request.services) == 1) and is_inter_domain(context_client, request.services[0].service_endpoint_ids):
        #    #devices = get_devices_in_topology(context_client, ADMIN_CONTEXT_ID, INTERDOMAIN_TOPOLOGY_NAME)
        #    #links = get_links_in_topology(context_client, ADMIN_CONTEXT_ID, INTERDOMAIN_TOPOLOGY_NAME)
        #    topology_id = json_topology_id(INTERDOMAIN_TOPOLOGY_NAME, context_id)
        #else:
        #    # TODO: improve filtering of devices and links
        #    # TODO: add contexts, topologies, and membership of devices/links in topologies
        #    #devices = context_client.ListDevices(Empty())
        #    #links = context_client.ListLinks(Empty())
        #    context_id = json_context_id(DEFAULT_CONTEXT_NAME)
        #    topology_id = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id)

        allow_forecasting = is_forecaster_enabled()
        topology_details = get_pathcomp_topology_details(request, allow_forecasting=allow_forecasting)

        algorithm = get_algorithm(request)
        algorithm.add_devices(topology_details.devices)
        algorithm.add_links(topology_details.links)
        algorithm.add_service_requests(request)

        #LOGGER.debug('device_list = {:s}'  .format(str(algorithm.device_list  )))
        #LOGGER.debug('endpoint_dict = {:s}'.format(str(algorithm.endpoint_dict)))
        #LOGGER.debug('link_list = {:s}'    .format(str(algorithm.link_list    )))
        #LOGGER.debug('service_list = {:s}' .format(str(algorithm.service_list )))
        #LOGGER.debug('service_dict = {:s}' .format(str(algorithm.service_dict )))

        #import time
        #ts = time.time()
        #algorithm.execute('request-{:f}.json'.format(ts), 'reply-{:f}.json'.format(ts))
        with self._lock:
            # ensure backend receives requests one at a time
            algorithm.execute()

        reply = algorithm.get_reply()
        LOGGER.debug('[Compute] end ; reply = {:s}'.format(grpc_message_to_json_string(reply)))
        return reply
