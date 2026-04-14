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
import logging

from context.client.ContextClient        import ContextClient
from device.client.DeviceClient          import DeviceClient
from service.client.ServiceClient        import ServiceClient
from kpi_manager.client.KpiManagerClient import KpiManagerClient


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


@pytest.fixture(scope='session')
def context_client():
    _client = ContextClient(host="10.152.183.180")
    _client.connect()
    LOGGER.info('Yielding Connected ContextClient...')
    yield _client
    LOGGER.info('Closing ContextClient...')
    _client.close()

@pytest.fixture(scope='session')
def device_client():
    _client = DeviceClient(host="10.152.183.212")
    _client.connect()
    LOGGER.info('Yielding Connected DeviceClient...')
    yield _client
    LOGGER.info('Closing DeviceClient...')
    _client.close()

@pytest.fixture(scope='session')
def service_client():
    _client = ServiceClient(host="10.152.183.98")
    _client.connect()
    LOGGER.info('Yielding Connected ServiceClient...')
    yield _client
    LOGGER.info('Closing ServiceClient...')
    _client.close()

@pytest.fixture(scope='session')
def kpi_manager_client():
    _client = KpiManagerClient(host="10.152.183.108")
    _client.connect()
    LOGGER.info('Yielding Connected KpiManagerClient...')
    yield _client
    LOGGER.info('Closed KpiManagerClient...')
    _client.close()

