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

import logging
import uuid
import queue
import time
from unittest.mock import patch

import pytest

from common.proto import dbscanserving_pb2 as dbscan
from common.proto.optical_attack_detector_pb2 import DetectionRequest

from opticalattackdetector.client.OpticalAttackDetectorClient import \
    OpticalAttackDetectorClient
from opticalattackdetector.service.OpticalAttackDetectorService import \
    OpticalAttackDetectorService

# from .example_objects import CONTEXT_ID, CONTEXT_ID_2, SERVICE_DEV1_DEV2

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def optical_attack_detector_service():
    _service = OpticalAttackDetectorService()
    _service.start()
    time.sleep(2)
    yield _service
    _service.stop()


@pytest.fixture(scope="session")
def optical_attack_detector_client(optical_attack_detector_service: OpticalAttackDetectorService):
    _client = OpticalAttackDetectorClient(
        host="127.0.0.1",
        port=optical_attack_detector_service.bind_port,
    )
    yield _client
    _client.close()


def test_detect_attack(
    optical_attack_detector_service: OpticalAttackDetectorService,
    optical_attack_detector_client: OpticalAttackDetectorClient,
):
    message = dbscan.DetectionResponse()
    message.cluster_indices.extend([0, 1] * 5 + [-1] * 10)

    with patch(
        "opticalattackdetector.service.OpticalAttackDetectorServiceServicerImpl.attack_mitigator_client"
    ) as mitigator, patch(
        "opticalattackdetector.service.OpticalAttackDetectorServiceServicerImpl.monitoring_client.IncludeKpi",
    ) as monitoring, patch(
        "opticalattackdetector.service.OpticalAttackDetectorServiceServicerImpl.dbscanserving_client.Detect",
        return_value=message,
    ) as dbscanserving:
        request: DetectionRequest = DetectionRequest()
        request.service_id.context_id.context_uuid.uuid = str(uuid.uuid4())
        request.service_id.service_uuid.uuid = str(uuid.uuid4())
        request.kpi_id.kpi_id.uuid = "1"
        optical_attack_detector_client.DetectAttack(request)
        dbscanserving.assert_called()
        monitoring.assert_called()
