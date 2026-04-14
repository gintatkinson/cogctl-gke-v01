# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging, uuid
from typing import Optional
from common.proto.context_pb2 import ConnectionId, DeviceId, EndPointId, LinkId, ServiceId, SliceId
from common.proto.kpi_manager_pb2 import KpiDescriptor, KpiId
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.telemetry_frontend_pb2 import Collector, CollectorId
from kpi_manager.client.KpiManagerClient import KpiManagerClient
from telemetry.frontend.client.TelemetryFrontendClient import TelemetryFrontendClient

LOGGER = logging.getLogger(__name__)

def create_kpi_descriptor(
    kpi_manager_client : KpiManagerClient,
    kpi_sample_type    : KpiSampleType,
    device_id          : Optional[DeviceId    ] = None,
    endpoint_id        : Optional[EndPointId  ] = None,
    service_id         : Optional[ServiceId   ] = None,
    slice_id           : Optional[SliceId     ] = None,
    connection_id      : Optional[ConnectionId] = None,
    link_id            : Optional[LinkId      ] = None,
) -> KpiId:
    kpi_descriptor = KpiDescriptor()
    kpi_descriptor.kpi_id.kpi_id.uuid = str(uuid.uuid4())
    kpi_descriptor.kpi_description = ''
    kpi_descriptor.kpi_sample_type = kpi_sample_type

    if device_id     is not None: kpi_descriptor.device_id    .CopyFrom(device_id    )
    if endpoint_id   is not None: kpi_descriptor.endpoint_id  .CopyFrom(endpoint_id  )
    if service_id    is not None: kpi_descriptor.service_id   .CopyFrom(service_id   )
    if slice_id      is not None: kpi_descriptor.slice_id     .CopyFrom(slice_id     )
    if connection_id is not None: kpi_descriptor.connection_id.CopyFrom(connection_id)
    if link_id       is not None: kpi_descriptor.link_id      .CopyFrom(link_id      )

    kpi_id : KpiId = kpi_manager_client.SetKpiDescriptor(kpi_descriptor)
    return kpi_id

def start_collector(
    telemetry_client : TelemetryFrontendClient,
    kpi_id : KpiId,
    duration_seconds : float,
    interval_seconds : float
) -> CollectorId:
    collector = Collector()
    collector.collector_id.collector_id.uuid = str(uuid.uuid4())
    collector.kpi_id.CopyFrom(kpi_id)
    collector.duration_s = duration_seconds
    collector.interval_s = interval_seconds
    collector_id : CollectorId = telemetry_client.StartCollector(collector)
    return collector_id
