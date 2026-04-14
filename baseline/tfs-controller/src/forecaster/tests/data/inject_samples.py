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


import logging, sys
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2 import Kpi, KpiDescriptor
from common.tools.timestamp.Converters import timestamp_datetime_to_float
from forecaster.tests.Tools import read_csv
from monitoring.client.MonitoringClient import MonitoringClient

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
logging.getLogger('monitoring.client.MonitoringClient').setLevel(logging.INFO)

CSV_DATA_FILE = 'src/forecaster/tests/data/dataset.csv'

def main() -> int:
    monitoring_client = MonitoringClient()
    link_uuid_to_kpi_kpi_uuid = dict()

    df = read_csv(CSV_DATA_FILE)
    for row in df.itertuples(index=False):
        link_uuid          = row.link_id
        timestamp          = timestamp_datetime_to_float(row.timestamp)
        used_capacity_gbps = row.used_capacity_gbps

        if link_uuid in link_uuid_to_kpi_kpi_uuid:
            kpi_uuid = link_uuid_to_kpi_kpi_uuid[link_uuid]
        else:
            kpi_descriptor = KpiDescriptor()
            kpi_descriptor.kpi_description        = 'Used Capacity in Link: {:s}'.format(link_uuid)
            kpi_descriptor.kpi_sample_type        = KpiSampleType.KPISAMPLETYPE_LINK_USED_CAPACITY_GBPS
            kpi_descriptor.link_id.link_uuid.uuid = link_uuid   # pylint: disable=no-member
            kpi_id = monitoring_client.SetKpi(kpi_descriptor)
            kpi_uuid = kpi_id.kpi_id.uuid
            link_uuid_to_kpi_kpi_uuid[link_uuid] = kpi_uuid

        kpi = Kpi()
        kpi.kpi_id.kpi_id.uuid  = kpi_uuid              # pylint: disable=no-member
        kpi.timestamp.timestamp = timestamp             # pylint: disable=no-member
        kpi.kpi_value.floatVal  = used_capacity_gbps    # pylint: disable=no-member
        monitoring_client.IncludeKpi(kpi)

    return 0

if __name__ == '__main__':
    sys.exit(main())
