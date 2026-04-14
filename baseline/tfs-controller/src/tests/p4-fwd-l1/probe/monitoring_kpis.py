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

# File to monitor the latest *n* samples from the KPI ID *id*
# and updates it every *i* seconds
#
# Author: Carlos Natalino <carlos.natalino@chalmers.se>

import argparse
import datetime
import time

from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2 import KpiDescriptor, KpiId, KpiQuery
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.timestamp.Converters import timestamp_float_to_string
from monitoring.client.MonitoringClient import MonitoringClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--last-n-samples",
        default=10,
        type=int,
        help="Number of latest samples of the KPI to show.",
    )
    parser.add_argument(
        "-s",
        "--sleep",
        default=5,
        type=int,
        help="Seconds between consecutive refreshes.",
    )
    parser.add_argument("-id", "--kpi-id", help="KPI ID, if known.")
    args = parser.parse_args()

    monitoring_client = MonitoringClient()

    if args.kpi_id is None:
        service_uuid = "608df176-90b8-5950-b50d-1810c6eaaa5d"
        kpi_description: KpiDescriptor = KpiDescriptor()
        kpi_description.kpi_description = "Security status of service {}".format(
            service_uuid
        )
        kpi_description.service_id.service_uuid.uuid = service_uuid
        kpi_description.kpi_sample_type = KpiSampleType.KPISAMPLETYPE_UNKNOWN
        new_kpi = monitoring_client.SetKpi(kpi_description)
        print("Created KPI {}: ".format(grpc_message_to_json_string(new_kpi)))
        kpi_id = new_kpi.kpi_id.uuid
    else:
        kpi_id = args.kpi_id

    query = KpiQuery()
    query.kpi_ids.append(KpiId(**{"kpi_id": {"uuid": kpi_id}}))
    query.last_n_samples = args.last_n_samples

    while True:
        print(chr(27) + "[2J")
        response = monitoring_client.QueryKpiData(query)
        print("{}\t{}\t{:<20}\t{}".format("Index", "KPI ID", "Timestamp", "Value"))
        for kpi in response.raw_kpi_lists:
            cur_kpi_id = kpi.kpi_id.kpi_id.uuid
            for i, raw_kpi in enumerate(kpi.raw_kpis):
                print(
                    "{}\t{}\t{}\t{}".format(
                        i,
                        cur_kpi_id,
                        timestamp_float_to_string(raw_kpi.timestamp.timestamp),
                        raw_kpi.kpi_value.floatVal,
                    )
                )
        print("Last update:", datetime.datetime.now().strftime("%H:%M:%S"))
        time.sleep(args.sleep)
