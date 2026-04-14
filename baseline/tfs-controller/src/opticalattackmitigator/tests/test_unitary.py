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
import os
from unittest.mock import patch

import pytest
from common.proto.optical_attack_mitigator_pb2 import AttackDescription

from opticalattackmitigator.client.OpticalAttackMitigatorClient import \
    OpticalAttackMitigatorClient
from opticalattackmitigator.service.OpticalAttackMitigatorService import \
    OpticalAttackMitigatorService

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


@pytest.fixture(scope="session")
def optical_attack_mitigator_service():
    _service = OpticalAttackMitigatorService()
    _service.start()
    yield _service
    _service.stop()


@pytest.fixture(scope="session")
def optical_attack_mitigator_client(optical_attack_mitigator_service):
    with patch.dict(
        os.environ,
        {
            "OPTICALATTACKMITIGATORSERVICE_SERVICE_HOST": "127.0.0.1",
            "OPTICALATTACKMITIGATORSERVICE_SERVICE_PORT_GRPC": str(optical_attack_mitigator_service.bind_port),
        },
        clear=True,
    ):
        _client = OpticalAttackMitigatorClient()
        yield _client
    _client.close()


def test_call_service(optical_attack_mitigator_client: OpticalAttackMitigatorClient):
    request = AttackDescription()
    optical_attack_mitigator_client.NotifyAttack(request)
