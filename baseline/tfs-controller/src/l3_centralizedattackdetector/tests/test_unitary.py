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
from l3_centralizedattackdetector.Config import GRPC_SERVICE_PORT, GRPC_MAX_WORKERS, GRPC_GRACE_PERIOD
from l3_centralizedattackdetector.client.l3_centralizedattackdetectorClient import l3_centralizedattackdetectorClient
from l3_centralizedattackdetector.service.l3_centralizedattackdetectorService import l3_centralizedattackdetectorService
from common.proto.l3_centralizedattackdetector_pb2 import (
    ModelInput,
)

port = 10000 + GRPC_SERVICE_PORT  # avoid privileged ports

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture(scope='session')
def l3_centralizedattackdetector_service():
    _service = l3_centralizedattackdetectorService(
        port=port, max_workers=GRPC_MAX_WORKERS, grace_period=GRPC_GRACE_PERIOD)
    _service.start()
    yield _service
    _service.stop()


@pytest.fixture(scope='session')
def l3_centralizedattackdetector_client(l3_centralizedattackdetector_service):
    _client = l3_centralizedattackdetectorClient(address='127.0.0.1', port=port)
    yield _client
    _client.close()

def test_demo():
    LOGGER.info('Demo Test')
    pass


def test_system(l3_centralizedattackdetector_client):
    inference_information = {
        "n_packets_server_seconds": 5.0,
        "n_packets_client_seconds": 5.0,
        "n_bits_server_seconds": 5.0,
        "n_bits_client_seconds": 5.0,
        "n_bits_server_n_packets_server": 5.0,
        "n_bits_client_n_packets_client": 5.0,
        "n_packets_server_n_packets_client": 5.0,
        "n_bits_server_n_bits_client": 5.0,
        "ip_o": "ipo",
        "port_o": "porto",
        "ip_d": "ipd",
        "port_d": "portd",
        "flow_id": "flowid",
        "protocol": "protocol",
        "time_start": 0.0,
        "time_end": 10.0,
    }
    response = l3_centralizedattackdetector_client.SendInput(
        ModelInput(**inference_information))
    LOGGER.info("Cad send_input sent and received: "+str(response.message))
    LOGGER.info('Success!')

    
