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
import time
import logging
from kpi_value_writer.service.KpiValueWriter import KpiValueWriter
from kpi_manager.client.KpiManagerClient import KpiManagerClient

from common.tools.kafka.Variables import KafkaTopic
from test_messages import create_kpi_descriptor_request

LOGGER = logging.getLogger(__name__)

# -------- Fixtures ----------------

@pytest.fixture(autouse=True)
def log_all_methods(request):
    '''
    This fixture logs messages before and after each test function runs, indicating the start and end of the test.
    The autouse=True parameter ensures that this logging happens automatically for all tests in the module.
    '''
    LOGGER.info(f" >>>>> Starting test: {request.node.name} ")
    yield
    LOGGER.info(f" <<<<< Finished test: {request.node.name} ")

# @pytest.fixture(scope='module')
# def kpi_manager_client():
#     LOGGER.debug("Yielding KpiManagerClient ...")
#     yield KpiManagerClient(host="10.152.183.203")
#     LOGGER.debug("KpiManagerClient is terminated.")


# -------- Initial Test ----------------
# def test_validate_kafka_topics():
#     LOGGER.debug(" >>> test_validate_kafka_topics: START <<< ")
#     response = KafkaTopic.create_all_topics()
#     assert isinstance(response, bool)

# --------------
# NOT FOR GITHUB PIPELINE (Local testing only)
# --------------
# def test_KafkaConsumer(kpi_manager_client):
#     kpidescriptor = create_kpi_descriptor_request()
#     kpi_manager_client.SetKpiDescriptor(kpidescriptor)
#     kpi_value_writer = KpiValueWriter()
#     kpi_value_writer.KafkaKpiConsumer()
#     timer = 300
#     LOGGER.debug(f" waiting for timer to finish {timer} seconds")
#     time.sleep(300)
