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

import logging, math
from typing import Dict, Optional
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, ServiceNameEnum
from common.Settings import ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, find_environment_variables, get_env_var_name
from common.method_wrappers.ServiceExceptions import InvalidArgumentException
from common.proto.context_pb2 import Constraint_Schedule, Service, TopologyDetails
from common.proto.forecaster_pb2 import ForecastLinkCapacityReply, ForecastTopologyCapacityRequest
from common.proto.pathcomp_pb2 import PathCompRequest
from common.tools.context_queries.Topology import get_topology_details
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from forecaster.client.ForecasterClient import ForecasterClient

LOGGER = logging.getLogger(__name__)

def get_service_schedule(service : Service) -> Optional[Constraint_Schedule]:
    for constraint in service.service_constraints:
        if constraint.WhichOneof('constraint') != 'schedule': continue
        return constraint.schedule
    return None

def get_pathcomp_topology_details(request : PathCompRequest, allow_forecasting : bool = False) -> TopologyDetails:
    context_client = ContextClient()
    topology_details = get_topology_details(
        context_client, DEFAULT_TOPOLOGY_NAME, context_uuid=DEFAULT_CONTEXT_NAME, rw_copy=True
    )

    if len(request.services) == 0:
        raise InvalidArgumentException('services', grpc_message_to_json_string(request), 'must not be empty')

    if not allow_forecasting:
        LOGGER.warning('Forecaster is explicitly disabled')
        return topology_details

    env_vars = find_environment_variables([
        get_env_var_name(ServiceNameEnum.FORECASTER, ENVVAR_SUFIX_SERVICE_HOST     ),
        get_env_var_name(ServiceNameEnum.FORECASTER, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
    ])
    if len(env_vars) != 2:
        LOGGER.warning('Forecaster is not deployed')
        return topology_details

    if len(request.services) > 1:
        LOGGER.warning('Forecaster does not support multiple services')
        return topology_details

    service = request.services[0]
    service_schedule = get_service_schedule(service)
    if service_schedule is None:
        LOGGER.warning('Service provides no schedule constraint; forecast cannot be used')
        return topology_details

    #start_timestamp = service_schedule.start_timestamp
    duration_days = service_schedule.duration_days
    if float(duration_days) <= 1.e-12:
        LOGGER.warning('Service schedule constraint does not define a duration; forecast cannot be used')
        return topology_details

    forecaster_client = ForecasterClient()
    forecaster_client.connect()

    forecast_request = ForecastTopologyCapacityRequest(
        topology_id=topology_details.topology_id,
        forecast_window_seconds = duration_days * 24 * 60 * 60
    )

    forecast_reply = forecaster_client.ForecastTopologyCapacity(forecast_request)

    forecasted_link_capacities : Dict[str, ForecastLinkCapacityReply] = {
        link_capacity.link_id.link_uuid.uuid : link_capacity
        for link_capacity in forecast_reply.link_capacities
    }

    for link in topology_details.links:
        link_uuid = link.link_id.link_uuid.uuid
        forecasted_link_capacity = forecasted_link_capacities.get(link_uuid)
        if forecasted_link_capacity is None: continue
        link.attributes.used_capacity_gbps = forecasted_link_capacity.forecast_used_capacity_gbps
        if link.attributes.total_capacity_gbps < link.attributes.used_capacity_gbps:
            total_capacity_gbps = link.attributes.used_capacity_gbps
            total_capacity_gbps = math.ceil(total_capacity_gbps / 100) * 100 # round up in steps of 100
            link.attributes.total_capacity_gbps = total_capacity_gbps

    return topology_details
