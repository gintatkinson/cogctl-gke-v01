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

import os
import time
import json
import pytest
import logging
import threading

from common.Constants         import ServiceNameEnum
from common.proto.context_pb2 import Empty
from common.Settings          import ( get_service_port_grpc, get_env_var_name, 
                                      ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC )

from common.tools.kafka.Variables                        import KafkaTopic
from common.proto.analytics_frontend_pb2                 import AnalyzerId, AnalyzerList
from analytics.frontend.client.AnalyticsFrontendClient   import AnalyticsFrontendClient
from analytics.frontend.service.AnalyticsFrontendService import AnalyticsFrontendService
from analytics.frontend.tests.messages                   import ( create_analyzer_id, create_analyzer,
                                                                 create_analyzer_filter )
from analytics.frontend.service.AnalyticsFrontendServiceServicerImpl import AnalyticsFrontendServiceServicerImpl
from apscheduler.schedulers.background                   import BackgroundScheduler
from apscheduler.triggers.interval                       import IntervalTrigger


###########################
# Tests Setup
###########################

LOCAL_HOST = '127.0.0.1'

ANALYTICS_FRONTEND_PORT = 10000 + int(get_service_port_grpc(ServiceNameEnum.ANALYTICS))
os.environ[get_env_var_name(ServiceNameEnum.ANALYTICS, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.ANALYTICS, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(ANALYTICS_FRONTEND_PORT)

LOGGER = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def analyticsFrontend_service():
    LOGGER.info('Initializing AnalyticsFrontendService...')

    _service = AnalyticsFrontendService()
    _service.start()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding AnalyticsFrontendService...')
    yield _service

    LOGGER.info('Terminating AnalyticsFrontendService...')
    _service.stop()

    LOGGER.info('Terminated AnalyticsFrontendService...')

@pytest.fixture(scope='session')
def analyticsFrontend_client(analyticsFrontend_service : AnalyticsFrontendService):
    LOGGER.info('Initializing AnalyticsFrontendClient...')

    _client = AnalyticsFrontendClient()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding AnalyticsFrontendClient...')
    yield _client

    LOGGER.info('Closing AnalyticsFrontendClient...')
    _client.close()

    LOGGER.info('Closed AnalyticsFrontendClient...')

@pytest.fixture(autouse=True)
def log_all_methods(request):
    '''
    This fixture logs messages before and after each test function runs, indicating the start and end of the test.
    The autouse=True parameter ensures that this logging happens automatically for all tests in the module.
    '''
    LOGGER.info(f" >>>>> Starting test: {request.node.name} ")
    yield
    LOGGER.info(f" <<<<< Finished test: {request.node.name} ")

###########################
# Tests Implementation of Analytics Frontend
###########################

# --- "test_validate_kafka_topics" should be executed before the functionality tests ---
def test_validate_kafka_topics():
    LOGGER.debug(" >>> test_validate_kafka_topics: START <<< ")
    response = KafkaTopic.create_all_topics()
    assert isinstance(response, bool)

# To test start and stop listener together
def test_StartAnalyzers(analyticsFrontend_client):
    LOGGER.info(' >>> test_StartAnalyzers START: <<< ')
    added_analyzer_id = analyticsFrontend_client.StartAnalyzer(create_analyzer())
    LOGGER.debug(str(added_analyzer_id))
    # LOGGER.info(' --> Calling StartResponseListener... ')
    # class_obj = AnalyticsFrontendServiceServicerImpl()
    # response  =  class_obj.StartResponseListener(added_analyzer_id.analyzer_id.uuid)
    # LOGGER.debug(response)
    LOGGER.info("waiting for timer to complete ...")
    time.sleep(15)
    LOGGER.info('--> StopAnalyzer')
    response = analyticsFrontend_client.StopAnalyzer(added_analyzer_id)
    LOGGER.debug(str(response))

# def test_SelectAnalytics(analyticsFrontend_client):
#     LOGGER.info(' >>> test_SelectAnalytics START: <<< ')
#     response = analyticsFrontend_client.SelectAnalyzers(create_analyzer_filter())
#     LOGGER.debug(str(response))
#     assert isinstance(response, AnalyzerList)

# def test_StopAnalytic(analyticsFrontend_client):
#     LOGGER.info(' >>> test_StopAnalytic START: <<< ')
#     response = analyticsFrontend_client.StopAnalyzer(create_analyzer_id())
#     LOGGER.debug(str(response))
#     assert isinstance(response, Empty)

# def test_ResponseListener():
#         LOGGER.info(' >>> test_ResponseListener START <<< ')
#         analyzer_id = create_analyzer_id()
#         LOGGER.debug("Starting Response Listener for Analyzer ID: {:}".format(analyzer_id.analyzer_id.uuid))
#         class_obj = AnalyticsFrontendServiceServicerImpl()
#         for response in class_obj.StartResponseListener(analyzer_id.analyzer_id.uuid):
#             LOGGER.debug(response)
#             assert isinstance(response, tuple)
