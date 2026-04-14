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

import pytest
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from monitoring.client.MonitoringClient import MonitoringClient
from e2e_orchestrator.client.E2EOrchestratorClient import E2EOrchestratorClient
from service.client.ServiceClient import ServiceClient


@pytest.fixture(scope='session')
def context_client():
    _client = ContextClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def device_client():
    _client = DeviceClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def e2eorchestrator_client():
    _client = E2EOrchestratorClient()
    yield _client
    _client.close()
