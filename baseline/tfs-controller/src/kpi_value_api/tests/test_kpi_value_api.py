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


import os, logging, pytest
from common.proto.context_pb2 import Empty
from common.Constants import ServiceNameEnum
from common.tools.kafka.Variables import KafkaTopic
from common.Settings import ( 
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name, get_service_port_grpc)
from kpi_value_api.service.KpiValueApiService import KpiValueApiService
from kpi_value_api.client.KpiValueApiClient import KpiValueApiClient
from kpi_value_api.tests.messages import create_kpi_value_list, create_kpi_id_request
from common.proto.kpi_value_api_pb2 import KpiAlarms

LOCAL_HOST = '127.0.0.1'
KPIVALUEAPI_SERVICE_PORT = get_service_port_grpc(ServiceNameEnum.KPIVALUEAPI)  # type: ignore
os.environ[get_env_var_name(ServiceNameEnum.KPIVALUEAPI, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.KPIVALUEAPI, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(KPIVALUEAPI_SERVICE_PORT)
LOGGER = logging.getLogger(__name__)

# This fixture will be requested by test cases and last during testing session
@pytest.fixture(scope='session')
def kpi_value_api_service():
    LOGGER.info('Initializing KpiValueApiService...')
    # _service = MonitoringService(name_mapping)
    _service = KpiValueApiService()
    _service.start()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding KpiValueApiService...')
    yield _service

    LOGGER.info('Terminating KpiValueApiService...')
    _service.stop()

    LOGGER.info('Terminated KpiValueApiService...')

# This fixture will be requested by test cases and last during testing session.
# The client requires the server, so client fixture has the server as dependency.
@pytest.fixture(scope='session')
def kpi_value_api_client(kpi_value_api_service : KpiValueApiService ):
    LOGGER.info('Initializing KpiValueApiClient...')
    _client = KpiValueApiClient()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding KpiValueApiClient...')
    yield _client

    LOGGER.info('Closing KpiValueApiClient...')
    _client.close()

    LOGGER.info('Closed KpiValueApiClient...')

##################################################
# Prepare Environment, should be the first test
##################################################

# To be added here

###########################
# Tests Implementation of Kpi Value Api
###########################

def test_validate_kafka_topics():
    LOGGER.debug(" >>> test_validate_kafka_topics: START <<< ")
    response = KafkaTopic.create_all_topics()
    assert isinstance(response, bool)

# def test_GetKpiAlarms(kpi_value_api_client):
#     LOGGER.debug(" >>> test_GetKpiAlarms")
#     stream = kpi_value_api_client.GetKpiAlarms(create_kpi_id_request())
#     for response in stream:
#         LOGGER.debug(str(response))
#     assert isinstance(response, KpiAlarms)

# def test_store_kpi_values(kpi_value_api_client):
#     LOGGER.debug(" >>> test_set_list_of_KPIs: START <<< ")
#     response = kpi_value_api_client.StoreKpiValues(create_kpi_value_list())
#     assert isinstance(response, Empty)
