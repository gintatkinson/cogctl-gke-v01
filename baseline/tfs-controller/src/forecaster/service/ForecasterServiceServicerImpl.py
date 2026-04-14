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

from typing import Dict, List
import grpc, logging
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.proto.context_pb2 import LinkAttributes, LinkId
from common.proto.forecaster_pb2 import (
    ForecastLinkCapacityReply, ForecastLinkCapacityRequest,
    ForecastTopologyCapacityReply, ForecastTopologyCapacityRequest
)
from common.proto.forecaster_pb2_grpc import ForecasterServiceServicer
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.context_queries.Link import get_link
from common.tools.context_queries.Topology import get_topology_details
from common.tools.timestamp.Converters import timestamp_utcnow_to_float
from context.client.ContextClient import ContextClient
from forecaster.Config import FORECAST_TO_HISTORY_RATIO
from forecaster.service.Forecaster import compute_forecast
from forecaster.service.KpiManager import KpiManager

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Forecaster', 'RPC')

class ForecasterServiceServicerImpl(ForecasterServiceServicer):
    def __init__(self) -> None:
        LOGGER.debug('Creating Servicer...')
        self._kpi_manager = KpiManager()
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ForecastLinkCapacity(
        self, request : ForecastLinkCapacityRequest, context : grpc.ServicerContext
    ) -> ForecastLinkCapacityReply:
        forecast_window_seconds = request.forecast_window_seconds

        # history_window_seconds indicates the size of the train-set based on the
        # requested size of the test-set and the configured history ratio
        history_window_seconds = FORECAST_TO_HISTORY_RATIO * forecast_window_seconds

        link_id = request.link_id
        link_uuid = link_id.link_uuid.uuid

        context_client = ContextClient()
        link = get_link(context_client, link_uuid)
        if link is None: raise NotFoundException('Link', link_uuid)

        kpi_id_map = self._kpi_manager.get_kpi_ids_from_link_ids([link_id])
        link_uuid__to__kpi_id = {
            _link_uuid : _kpi_id
            for (_link_uuid, _kpi_sample_type), _kpi_id in kpi_id_map.items()
            if _kpi_sample_type == KpiSampleType.KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS
        }
        kpi_id = link_uuid__to__kpi_id[link_uuid]

        end_timestamp   = timestamp_utcnow_to_float()
        start_timestamp = end_timestamp - history_window_seconds
        df_historical_data = self._kpi_manager.get_kpi_id_samples([kpi_id], start_timestamp, end_timestamp)
        forecast_used_capacity_gbps = compute_forecast(df_historical_data, kpi_id)

        reply = ForecastLinkCapacityReply()
        reply.link_id.link_uuid.uuid      = link_uuid
        reply.total_capacity_gbps         = link.attributes.total_capacity_gbps
        reply.current_used_capacity_gbps  = link.attributes.used_capacity_gbps
        reply.forecast_used_capacity_gbps = forecast_used_capacity_gbps
        return reply

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ForecastTopologyCapacity(
        self, request : ForecastTopologyCapacityRequest, context : grpc.ServicerContext
    ) -> ForecastTopologyCapacityReply:
        forecast_window_seconds = request.forecast_window_seconds

        # history_window_seconds indicates the size of the train-set based on the
        # requested size of the test-set and the configured history ratio
        history_window_seconds = FORECAST_TO_HISTORY_RATIO * forecast_window_seconds

        context_uuid  = request.topology_id.context_id.context_uuid.uuid
        topology_uuid = request.topology_id.topology_uuid.uuid
        context_client = ContextClient()
        topology_details = get_topology_details(context_client, topology_uuid, context_uuid=context_uuid)
        if topology_details is None:
            topology_uuid = '{:s}/{:s}'.format(context_uuid, topology_uuid)
            raise NotFoundException('Topology', topology_uuid)

        link_ids        : List[LinkId]              = list()
        link_capacities : Dict[str, LinkAttributes] = dict()
        for link in topology_details.links:
            link_ids.append(link.link_id)
            link_capacities[link.link_id.link_uuid.uuid] = link.attributes

        kpi_id_map = self._kpi_manager.get_kpi_ids_from_link_ids(link_ids)
        link_uuid__to__kpi_id = {
            _link_id : _kpi_id
            for (_link_id, _kpi_sample_type), _kpi_id in kpi_id_map.items()
            if _kpi_sample_type == KpiSampleType.KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS
        }

        kpi_ids = list(link_uuid__to__kpi_id.values())
        end_timestamp   = timestamp_utcnow_to_float()
        start_timestamp = end_timestamp - history_window_seconds
        df_historical_data = self._kpi_manager.get_kpi_id_samples(kpi_ids, start_timestamp, end_timestamp)

        reply = ForecastTopologyCapacityReply()
        for link_uuid, kpi_id in link_uuid__to__kpi_id.items():
            link_attributes = link_capacities[link_uuid]
            forecast_used_capacity_gbps = compute_forecast(df_historical_data, kpi_id)
            link_capacity : ForecastLinkCapacityReply = reply.link_capacities.add() # pylint: disable=no-member
            link_capacity.link_id.link_uuid.uuid      = link_uuid
            link_capacity.total_capacity_gbps         = link_attributes.total_capacity_gbps
            link_capacity.current_used_capacity_gbps  = link_attributes.used_capacity_gbps
            link_capacity.forecast_used_capacity_gbps = forecast_used_capacity_gbps
        return reply
