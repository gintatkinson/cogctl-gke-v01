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

import enum, grpc, logging
from queue import Queue
from typing import Any, Optional
from common.proto.context_pb2 import Empty
from common.proto.monitoring_pb2 import Kpi, KpiDescriptor, KpiDescriptorList, KpiId, KpiQuery, RawKpiTable
from common.proto.monitoring_pb2_grpc import MonitoringServiceServicer
from common.tools.grpc.Tools import grpc_message_to_json_string
from .InMemoryObjectDatabase import InMemoryObjectDatabase
from .InMemoryTimeSeriesDatabase import InMemoryTimeSeriesDatabase

LOGGER = logging.getLogger(__name__)

class IMDB_ContainersEnum(enum.Enum):
    KPI_DESCRIPTORS = 'kpi_descriptor'

class MockServicerImpl_Monitoring(MonitoringServiceServicer):
    def __init__(
        self, queue_samples : Optional[Queue] = None
    ) -> None:
        LOGGER.debug('[__init__] Creating Servicer...')
        if queue_samples is None: queue_samples = Queue()
        self.queue_samples = queue_samples
        self.obj_db = InMemoryObjectDatabase()
        self.ts_db  = InMemoryTimeSeriesDatabase()
        LOGGER.debug('[__init__] Servicer Created')

    # ----- Common -----------------------------------------------------------------------------------------------------

    def _set(self, container_name, entry_uuid, entry_id_field_name, entry) -> Any:
        entry = self.obj_db.set_entry(container_name, entry_uuid, entry)
        return getattr(entry, entry_id_field_name)

    def _del(self, container_name, entry_uuid, grpc_context) -> Empty:
        self.obj_db.del_entry(container_name, entry_uuid, grpc_context)
        return Empty()

    # ----- KPI Descriptor ---------------------------------------------------------------------------------------------

    def GetKpiDescriptorList(self, request : Empty, context : grpc.ServicerContext) -> KpiDescriptorList:
        LOGGER.debug('[GetKpiDescriptorList] request={:s}'.format(grpc_message_to_json_string(request)))
        kpi_descriptor_list = self.obj_db.get_entries(IMDB_ContainersEnum.KPI_DESCRIPTORS.value)
        reply = KpiDescriptorList(kpi_descriptor_list=kpi_descriptor_list)
        LOGGER.debug('[GetKpiDescriptorList] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def GetKpiDescriptor(self, request : KpiId, context : grpc.ServicerContext) -> KpiDescriptor:
        LOGGER.debug('[GetKpiDescriptor] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self.obj_db.get_entry(IMDB_ContainersEnum.KPI_DESCRIPTORS.value, request.kpi_id.uuid, context)
        LOGGER.debug('[GetKpiDescriptor] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def SetKpi(self, request : KpiDescriptor, context : grpc.ServicerContext) -> KpiId:
        LOGGER.debug('[SetKpi] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self._set(IMDB_ContainersEnum.KPI_DESCRIPTORS.value, request.kpi_id.kpi_id.uuid, 'kpi_id', request)
        LOGGER.debug('[SetKpi] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def DeleteKpi(self, request : KpiId, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[DeleteKpi] request={:s}'.format(grpc_message_to_json_string(request)))
        reply = self._del(IMDB_ContainersEnum.KPI_DESCRIPTORS.value, request.kpi_id.kpi_id.uuid, context)
        LOGGER.debug('[DeleteKpi] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    # ----- KPI Sample -------------------------------------------------------------------------------------------------

    def IncludeKpi(self, request : Kpi, context : grpc.ServicerContext) -> Empty:
        LOGGER.debug('[IncludeKpi] request={:s}'.format(grpc_message_to_json_string(request)))
        self.queue_samples.put(request)
        reply = Empty()
        LOGGER.debug('[IncludeKpi] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply

    def QueryKpiData(self, request : KpiQuery, context : grpc.ServicerContext) -> RawKpiTable:
        LOGGER.debug('[QueryKpiData] request={:s}'.format(grpc_message_to_json_string(request)))
        # TODO: add filters for request.monitoring_window_s
        # TODO: add filters for request.last_n_samples
        kpi_uuids = [kpi_id.kpi_id.uuid for kpi_id in request.kpi_ids]

        start_timestamp = request.start_timestamp.timestamp
        if start_timestamp <= 0: start_timestamp = None

        end_timestamp = request.end_timestamp.timestamp
        if end_timestamp <= 0: end_timestamp = None

        df_samples = self.ts_db.filter(kpi_uuids, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        #LOGGER.debug('[QueryKpiData] df_samples={:s}'.format(df_samples.to_string()))
        reply = RawKpiTable()
        kpi_uuid__to__raw_kpi_list = dict()

        for df_sample in df_samples.itertuples():
            kpi_uuid  = df_sample.kpi_uuid
            if kpi_uuid in kpi_uuid__to__raw_kpi_list:
                raw_kpi_list = kpi_uuid__to__raw_kpi_list[kpi_uuid]
            else:
                raw_kpi_list = reply.raw_kpi_lists.add()    # pylint: disable=no-member
                raw_kpi_list.kpi_id.kpi_id.uuid = kpi_uuid
                kpi_uuid__to__raw_kpi_list[kpi_uuid] = raw_kpi_list

            raw_kpi = raw_kpi_list.raw_kpis.add()
            raw_kpi.timestamp.timestamp = df_sample.timestamp.timestamp()
            raw_kpi.kpi_value.floatVal  = df_sample.value

        LOGGER.debug('[QueryKpiData] reply={:s}'.format(grpc_message_to_json_string(reply)))
        return reply
