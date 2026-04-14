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
import pytest
from l3_attackmitigator.Config import GRPC_SERVICE_PORT, GRPC_MAX_WORKERS, GRPC_GRACE_PERIOD
from l3_attackmitigator.client.l3_attackmitigatorClient import l3_attackmitigatorClient
from l3_attackmitigator.service.l3_attackmitigatorService import l3_attackmitigatorService
from common.proto.l3_attackmitigator_pb2 import (
    Output,
)

port = 10000 + GRPC_SERVICE_PORT  # avoid privileged ports

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture(scope='session')
def l3_attackmitigator_service():
    _service = l3_attackmitigatorService(
        port=port, max_workers=GRPC_MAX_WORKERS, grace_period=GRPC_GRACE_PERIOD)
    _service.start()
    LOGGER.info('Server started on '+str(port))
    yield _service
    _service.stop()


@pytest.fixture(scope='session')
def l3_attackmitigator_client(l3_attackmitigator_service):
    _client = l3_attackmitigatorClient(address='127.0.0.1', port=port)
    yield _client
    _client.close()


def test_demo():
    LOGGER.info('Demo Test')
    pass

def test_grpc_server(l3_attackmitigator_client):
    output_message = {
        "confidence": 0.8,
        "timestamp": "date",
        "ip_o": "randomIP",
        "tag_name": "HTTP",
        "tag": 0,
        "flow_id": "FlowID",
        "protocol": "RandomProtocol",
        "port_d": "3456",
        "ml_id": "RandomForest",
        "time_start": 0.0,
        "time_end": 10.0,
    }
    response = l3_attackmitigator_client.SendOutput(Output(**output_message))
    LOGGER.info("Inferencer send_input sent and received: " +
                str(response.message))
    LOGGER.info('Success!')
