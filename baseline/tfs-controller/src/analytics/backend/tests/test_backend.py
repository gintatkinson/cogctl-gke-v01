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

import time
import json
import pytest
import logging
import pandas as pd

from unittest.mock      import MagicMock, patch
from .messages_analyzer import get_batch, get_input_kpi_list, get_output_kpi_list, get_thresholds, \
                               get_windows_size, get_batch_size, get_agg_df, get_duration

from common.tools.kafka.Variables                      import KafkaTopic
from analytics.backend.service.Streamer                import DaskStreamer
from analytics.backend.service.AnalyzerHandlers        import aggregation_handler, threshold_handler
from analytics.backend.service.AnalyticsBackendService import AnalyticsBackendService


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s -  %(levelname)s - %(message)s')


# ----
# Test fixtures and helper functions
# ----

@pytest.fixture(autouse=True)
def log_all_methods(request):
    '''
    This fixture logs messages before and after each test function runs, indicating the start and end of the test.
    The autouse=True parameter ensures that this logging happens automatically for all tests in the module.
    '''
    logger.info(f" >>>>> Starting test: {request.node.name} ")
    yield
    logger.info(f" <<<<< Finished test: {request.node.name} ")

@pytest.fixture
def mock_kafka_producer():
    mock_producer         = MagicMock()
    mock_producer.produce = MagicMock()
    mock_producer.flush   = MagicMock()
    return mock_producer

@pytest.fixture
def mock_dask_cluster():
    mock_cluster       = MagicMock()
    mock_cluster.close = MagicMock()
    return mock_cluster

@pytest.fixture
def mock_dask_client():
    mock_client        = MagicMock()
    mock_client.status = 'running'
    mock_client.submit = MagicMock()
    return mock_client

@pytest.fixture()
def mock_kafka_consumer():
    mock_consumer           = MagicMock()
    mock_consumer.subscribe = MagicMock()
    return mock_consumer

@pytest.fixture()
def mock_streamer_start():
    mock_streamer = MagicMock()
    mock_streamer.start = MagicMock()
    return mock_streamer

###########################
# funtionality pytest cases with specific fixtures for AnalyticsBackendService class sub-methods
###########################

@pytest.fixture
def analytics_service(mock_kafka_producer, mock_dask_cluster, mock_dask_client, mock_kafka_consumer, mock_streamer_start):
    with patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_kafka_producer', return_value = mock_kafka_producer), \
         patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_dask_cluster',   return_value = mock_dask_cluster  ), \
         patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_dask_client',    return_value = mock_dask_client   ), \
         patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_kafka_consumer', return_value = mock_kafka_consumer), \
         patch('analytics.backend.service.Streamer.DaskStreamer.run',                               return_value = mock_streamer_start):
         
        service = AnalyticsBackendService()
        yield service
        service.close()

@pytest.fixture
def analyzer_data():
    return {
        'algo_name'          : 'test_algorithm',
        'oper_mode'          : 'test_mode',
        'input_kpis'         : get_input_kpi_list(),
        'output_kpis'        : get_output_kpi_list(),
        'thresholds'         : get_thresholds(),
        'duration'           : get_duration(),
        'batch_size_min'     : get_batch_size(),
        'window_size'        : get_windows_size(),
        'batch_duration_min' : get_duration(),
    }

def test_start_streamer(analytics_service, analyzer_data):
    analyzer_uuid = "test-analyzer-uuid"
    # Start streamer
    result = analytics_service.StartStreamer(analyzer_uuid, analyzer_data)
    assert result is True
    assert analyzer_uuid in analytics_service.active_streamers

def test_stop_streamer(analytics_service, analyzer_data):
    analyzer_uuid = "test-analyzer-uuid"

    # Start streamer for stopping it later
    analytics_service.StartStreamer(analyzer_uuid, analyzer_data)
    assert analyzer_uuid in analytics_service.active_streamers

    # Stop streamer
    with patch('time.sleep', return_value=None):
        result = analytics_service.StopStreamer(analyzer_uuid)
    assert result is True
    assert analyzer_uuid not in analytics_service.active_streamers

    # Verify that the streamer was stopped
    assert analyzer_uuid not in analytics_service.active_streamers

def test_close(analytics_service, mock_kafka_producer, mock_dask_cluster):
    analytics_service.close()

    mock_kafka_producer.flush.assert_called_once()
    mock_dask_cluster.close.assert_called_once()

###########################
# funtionality pytest with specific fixtures for streamer class sub methods
###########################

@pytest.fixture
def dask_streamer(mock_kafka_producer, mock_dask_cluster, mock_dask_client, mock_kafka_consumer):
    with patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_kafka_producer', return_value = mock_kafka_producer), \
         patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_dask_cluster',   return_value = mock_dask_cluster  ), \
         patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_dask_client',    return_value = mock_dask_client   ), \
         patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_kafka_consumer', return_value = mock_kafka_consumer):
        
        return DaskStreamer(
            key               = "test_key",
            input_kpis        = get_input_kpi_list(),
            output_kpis       = get_output_kpi_list(),
            thresholds        = get_thresholds(),
            batch_size        = get_batch_size(),
            window_size       = get_windows_size(),
            cluster_instance  = mock_dask_cluster(),
            producer_instance = mock_kafka_producer(),
        )

def test_dask_streamer_initialization(dask_streamer):
    """Test if the DaskStreamer initializes correctly."""
    assert dask_streamer.key         == "test_key"
    assert dask_streamer.batch_size  == get_batch_size()
    assert dask_streamer.window_size is None
    assert dask_streamer.consumer    is not None
    assert dask_streamer.producer    is not None
    assert dask_streamer.client      is not None

def test_run_stops_on_no_consumer(dask_streamer):
    """Test if the run method exits when the consumer is not initialized."""
    dask_streamer.consumer = None
    with patch('time.sleep', return_value=None):
        dask_streamer.run()

    assert not dask_streamer.running

def test_task_handler_selector_valid_handler(dask_streamer, mock_dask_client):
    """Test task handler selection with a valid handler."""
    with patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.initialize_dask_client', return_value = mock_dask_client):

        dask_streamer.task_handler_selector()
        assert dask_streamer.client.status == 'running'

def test_task_handler_selector_invalid_handler(dask_streamer):
    """Test task handler selection with an invalid handler."""
    with patch('analytics.backend.service.AnalyzerHandlers.Handlers.is_valid_handler', return_value=False):
        dask_streamer.task_handler_selector()
        assert dask_streamer.batch == []

def test_produce_result(dask_streamer):
    """Test if produce_result sends records to Kafka."""
    result = [{"kpi_id": "kpi1", "value": 100}]
    with patch('analytics.backend.service.AnalyzerHelper.AnalyzerHelper.delivery_report', return_value=None) as mock_delivery_report, \
         patch.object(dask_streamer.producer, 'produce') as mock_produce:
        dask_streamer.produce_result(result, "test_topic")
        mock_produce.assert_called_once_with(
            "test_topic",
            key="kpi1",
            value=json.dumps({"kpi_id": "kpi1", "value": 100}),
            callback=mock_delivery_report
        )

def test_stop(dask_streamer):
    """Test the cleanup method."""
    with patch.object(dask_streamer.consumer, 'close') as mock_consumer_close, \
         patch.object(dask_streamer.client,   'close') as mock_client_close, \
         patch('time.sleep', return_value=0):
        
        # Mock the conditions required for the close calls
        dask_streamer.client.status = 'running'
        
        dask_streamer.stop()

        mock_consumer_close.assert_called_once()
        mock_client_close.assert_called_once()

def test_run_with_valid_consumer(dask_streamer):
    """Test the run method with a valid Kafka consumer."""
    with patch.object(dask_streamer.consumer, 'poll')         as mock_poll, \
         patch.object(dask_streamer, 'task_handler_selector') as mock_task_handler_selector:
        
        # Simulate valid messages without errors
        mock_message_1 = MagicMock()
        mock_message_1.value.return_value = b'{"kpi_id": "kpi1", "value": 100}'
        mock_message_1.error.return_value = None  # No error

        mock_message_2 = MagicMock()
        mock_message_2.value.return_value = b'{"kpi_id": "kpi2", "value": 200}'
        mock_message_2.error.return_value = None  # No error

        # Mock `poll` to return valid messages
        mock_poll.side_effect = [mock_message_1, mock_message_2]
        
        # Run the `run` method in a limited loop
        with patch('time.sleep', return_value=None):  # Mock `sleep` to avoid delays
            dask_streamer.running = True            
            dask_streamer.batch_size = 2            
            
            # Limit the loop by breaking it after one full processing cycle
            def stop_running_after_task_handler():
                logger.info("Stopping the streamer after processing the first batch.")
                dask_streamer.running = False
            
            mock_task_handler_selector.side_effect = stop_running_after_task_handler
            dask_streamer.run()
        
        assert len(dask_streamer.batch) == 0  # Batch should be cleared after processing
        mock_task_handler_selector.assert_called_once()  # Task handler should be called once
        mock_poll.assert_any_call(timeout=1.0)  # Poll should have been called at least once

# # add a test to check the working of aggregation_handler function and threshold_handler from AnalyzerHandlers.py
def test_aggregation_handler():

    # Create a sample batch
    batch           = get_batch()
    input_kpi_list  = get_input_kpi_list()
    output_kpi_list = get_output_kpi_list()
    thresholds      = get_thresholds() 

    # Test aggregation_handler
    aggregated_df = aggregation_handler(
        "test_batch", "test_key", batch, input_kpi_list, output_kpi_list, thresholds
    )
    assert isinstance(aggregated_df, list)
    assert all(isinstance(item, dict) for item in aggregated_df)

# # Test threshold_handler
def test_threshold_handler():
    # Create a sample aggregated DataFrame
    agg_df     = get_agg_df()
    thresholds = get_thresholds()

    # Test threshold_handler
    result = threshold_handler("test_key", agg_df, thresholds["task_parameter"][0])

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 7)


###########################
# integration test of Streamer with backend service (Shouldn't be run in the CI/CD pipeline)
###########################
# This is a local machine test to check the integration of the backend service with the Streamer

# @pytest.fixture(scope='session')
# def analyticBackend_service():
#     logger.info('Initializing AnalyticsBackendService...')

#     _service = AnalyticsBackendService()
#     _service.start()

#     logger.info('Yielding AnalyticsBackendService...')
#     yield _service

#     logger.info('Terminating AnalyticsBackendService...')
#     _service.stop()
#     logger.info('Terminated AnalyticsBackendService...')


# # --- "test_validate_kafka_topics" should be run before the functionality tests ---
# def test_validate_kafka_topics():
#     logger.debug(" >>> test_validate_kafka_topics: START <<< ")
#     response = KafkaTopic.create_all_topics()
#     assert isinstance(response, bool)

# def test_backend_integration_with_frontend(analyticBackend_service: AnalyticsBackendService):
#     # backendServiceObject = AnalyticsBackendService()
#     # backendServiceObject.install_servicers()
#     logger.info(" waiting for 2 minutes for the backend service before termination  ... ")
#     time.sleep(300)
#     logger.info(" Initiating stop collector ... ")
#     status = analyticBackend_service.StopStreamer("efef4d95-1cf1-43c4-9742-95c283ddd666")
#     analyticBackend_service.close()
#     assert isinstance(status, bool)
#     assert status == True
#     logger.info(" Backend service terminated successfully ... ")
