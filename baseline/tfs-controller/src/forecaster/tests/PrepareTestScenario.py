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

import pytest, os
from common.Constants import ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name, get_service_port_grpc)
from context.client.ContextClient import ContextClient
from forecaster.client.ForecasterClient import ForecasterClient
from forecaster.service.ForecasterService import ForecasterService
from monitoring.client.MonitoringClient import MonitoringClient
from .MockService_Dependencies import MockService_Dependencies

LOCAL_HOST = '127.0.0.1'
MOCKSERVICE_PORT = 10000
# avoid privileged ports
FORECASTER_SERVICE_PORT = MOCKSERVICE_PORT + int(get_service_port_grpc(ServiceNameEnum.FORECASTER))
os.environ[get_env_var_name(ServiceNameEnum.FORECASTER, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.FORECASTER, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(FORECASTER_SERVICE_PORT)

@pytest.fixture(scope='session')
def mock_service():
    _service = MockService_Dependencies(MOCKSERVICE_PORT)
    _service.configure_env_vars()
    _service.start()
    yield _service
    _service.stop()

@pytest.fixture(scope='session')
def context_client(mock_service : MockService_Dependencies): # pylint: disable=redefined-outer-name
    _client = ContextClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def monitoring_client(mock_service : MockService_Dependencies): # pylint: disable=redefined-outer-name
    _client = MonitoringClient()
    yield _client
    _client.close()

@pytest.fixture(scope='session')
def forecaster_service(
    context_client : ContextClient,         # pylint: disable=redefined-outer-name
    monitoring_client : MonitoringClient,   # pylint: disable=redefined-outer-name
):
    _service = ForecasterService()
    _service.start()
    yield _service
    _service.stop()

@pytest.fixture(scope='session')
def forecaster_client(forecaster_service : ForecasterService):    # pylint: disable=redefined-outer-name
    _client = ForecasterClient()
    yield _client
    _client.close()
