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

import asyncio
import logging
import traceback

from grpclib.client import Channel

from common.proto.asyncio.optical_attack_detector_grpc import \
    OpticalAttackDetectorServiceStub
from common.proto.asyncio.optical_attack_detector_pb2 import DetectionRequest

LOGGER = logging.getLogger(__name__)


async def detect_attack(
    host: str,
    port: int,
    context_id: str,
    service_id: str,
    kpi_id: str,
    timeout: float = 20.0,
) -> None:
    try:
        LOGGER.debug("Sending request for {}...".format(service_id))
        async with Channel(host, port) as channel:
            stub = OpticalAttackDetectorServiceStub(channel)

            request: DetectionRequest = DetectionRequest()
            request.service_id.context_id.context_uuid.uuid = context_id
            request.service_id.service_uuid.uuid = str(service_id)

            request.kpi_id.kpi_id.uuid = kpi_id

            await stub.DetectAttack(request, timeout=timeout)
        LOGGER.debug("Monitoring finished for {}/{}".format(service_id, kpi_id))
    except Exception as e:
        LOGGER.warning(
            "Exception while processing service_id {}/{}: {}".format(service_id, kpi_id, e)
        )
        traceback.print_exc()


def delegate_services(
    service_list,
    start_index: int,
    end_index: int,
    host: str,
    port: str,
    monitoring_interval: float,
):
    async def run_internal_loop():
        tasks = []
        for service in service_list[start_index:end_index]:
            aw = detect_attack(
                host,
                port,
                service["context"],
                service["service"],
                service["kpi"],
                # allow at most 90% of the monitoring interval to succeed
                monitoring_interval * 0.9,
            )
            tasks.append(aw)
        [await aw for aw in tasks]

    asyncio.run(run_internal_loop())
