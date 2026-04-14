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

import pandas
from typing import Dict, List, Tuple
from common.proto.context_pb2 import Empty, LinkId
from common.proto.monitoring_pb2 import KpiId, KpiQuery
from monitoring.client.MonitoringClient import MonitoringClient

class KpiManager:
    def __init__(self) -> None:
        self._monitoring_client = MonitoringClient()

    def get_kpi_ids_from_link_ids(
        self, link_ids : List[LinkId]
    ) -> Dict[Tuple[str, int], KpiId]:
        link_uuids = {link_id.link_uuid.uuid for link_id in link_ids}
        kpi_descriptors = self._monitoring_client.GetKpiDescriptorList(Empty())
        kpi_ids : Dict[Tuple[str, int], KpiId] = {
            (kpi_descriptor.link_id.link_uuid.uuid, kpi_descriptor.kpi_sample_type) : kpi_descriptor.kpi_id
            for kpi_descriptor in kpi_descriptors.kpi_descriptor_list
            if kpi_descriptor.link_id.link_uuid.uuid in link_uuids
        }
        return kpi_ids

    def get_kpi_id_samples(
        self, kpi_ids : List[KpiId], start_timestamp : float, end_timestamp : float
    ) -> pandas.DataFrame:
        kpi_query = KpiQuery()
        for kpi_id in kpi_ids: kpi_query.kpi_ids.add().kpi_id.uuid = kpi_id.kpi_id.uuid
        kpi_query.start_timestamp.timestamp = start_timestamp   # pylint: disable=no-member
        kpi_query.end_timestamp.timestamp   = end_timestamp     # pylint: disable=no-member
        raw_kpi_table = self._monitoring_client.QueryKpiData(kpi_query)

        data : List[Tuple[str, float, float]] = list()
        for raw_kpi_list in raw_kpi_table.raw_kpi_lists:
            kpi_uuid = raw_kpi_list.kpi_id.kpi_id.uuid
            for raw_kpi in raw_kpi_list.raw_kpis:
                timestamp = raw_kpi.timestamp.timestamp
                value = float(getattr(raw_kpi.kpi_value, raw_kpi.kpi_value.WhichOneof('value')))
                data.append((timestamp, kpi_uuid, value))

        df = pandas.DataFrame(data, columns=['timestamp', 'kpi_id', 'value'])
        df['timestamp'] = pandas.to_datetime(df['timestamp'].astype('int'), unit='s', utc=True)
        df.sort_values('timestamp', ascending=True, inplace=True)
        return df
