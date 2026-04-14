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
import time
from typing import Dict
import json
# from common.tools.context_queries.EndPoint import get_endpoint_names
#from .EndPoint import get_endpoint_names        # modofied version of get_endpoint_names
from common.tools.kafka.Variables import KafkaTopic
from .add_devices import load_topology
from .Fixtures import context_client, device_client, service_client, kpi_manager_client
from .messages import create_collector_request, _create_kpi_descriptor, _create_kpi_id
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import EndPointId, DeviceId, TopologyId, ContextId , Empty
from common.proto.kpi_manager_pb2 import KpiId
from common.tools.context_queries.Device import get_device, add_device_to_topology
from common.tools.context_queries.Topology import get_topology
from telemetry.backend.service.HelperMethods import get_subscription_parameters
from telemetry.backend.service.TelemetryBackendService import TelemetryBackendService

from telemetry.backend.service.HelperMethods import get_collector_by_kpi_id
from telemetry.backend.service.collector_api.DriverFactory import DriverFactory
from telemetry.backend.service.collector_api.DriverInstanceCache import DriverInstanceCache, preload_drivers
from telemetry.backend.service.collectors import COLLECTORS
from telemetry.backend.service.collectors.gnmi_oc.GnmiOpenConfigCollector import GNMIOpenConfigCollector
from confluent_kafka import Producer as KafkaProducer
from common.tools.kafka.Variables import KafkaConfig, KafkaTopic

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


# --------------------------------------------------------------
# -------------------- HELPER METHODS --------------------------
# --------------------------------------------------------------

def publish_request_on_kafka(collector_obj, collector_uuid):
    kafka_producer = KafkaProducer({'bootstrap.servers' : KafkaConfig.get_kafka_address()})
    kafka_producer.produce(
            KafkaTopic.TELEMETRY_REQUEST.value,
            key      = collector_uuid,
            value    = json.dumps(collector_obj),
            callback = delivery_callback
        )
    LOGGER.info("Collector Request Generated: Collector Id: {:}, Value: {:}".format(collector_uuid, collector_obj))
    kafka_producer.flush()

def delivery_callback(err, msg):
    if err:
        LOGGER.warning('Message delivery failed: {:}'.format(err))

# --------------------------------------------------------------
# -------------------- FIXTURES --------------------------------
# --------------------------------------------------------------

@pytest.fixture(autouse=True)
def log_all_methods(request):
    '''
    This fixture logs messages before and after each test function runs, indicating the start and end of the test.
    The autouse=True parameter ensures that this logging happens automatically for all tests in the module.
    '''
    LOGGER.info(f" >>>>> Starting test: {request.node.name} ")
    yield
    LOGGER.info(f" <<<<< Finished test: {request.node.name} ")

@pytest.fixture
def telemetry_backend_service():
    LOGGER.info('Initializing TelemetryBackendService...')

    KafkaTopic.create_all_topics()

    driver_factory        = DriverFactory(COLLECTORS)
    driver_instance_cache = DriverInstanceCache(driver_factory)

    _service              = TelemetryBackendService(driver_instance_cache)
    _service.start()

    # LOGGER.info('Preloading collectors...')
    # preload_drivers(driver_instance_cache)

    LOGGER.info('Yielding TelemetryBackendService...')
    yield _service

    LOGGER.info('Terminating TelemetryBackendService...')
    _service.stop()
    LOGGER.info('Terminated TelemetryBackendService...')


# --------------------------------------------------------------
# -------------------- TESTS -----------------------------------
# --------------------------------------------------------------

# TODO: To test complete cycle of collector creation, subscription, and data retrieval, and termination by unsubscribing.
# ----- overall collector lifecycle test -----
# 1. Start telemetry backend service
# 2. Generate request on Kafka

# def test_collector_lifecycle(
#         telemetry_backend_service, kpi_manager_client, context_client
#         ):
#     time.sleep(5)  # Wait for the service to start
#     LOGGER.info('------ Waiting time for telemetry backend service is finished ------')
#     # Create a collector request
#     collector_obj : Dict = {
#         "kpi_id": "6e22f180-ba28-4641-b190-2287bf447777",
#         "duration": 10.0,
#         "interval": 3.0
#     }
#     collector_id = "6e22f180-ba28-4641-b190-2287bf444444"
#     publish_request_on_kafka(collector_obj, collector_id)
#     # Wait for the collector to be created and started
#     LOGGER.info('Waiting for collector to be created and started...')
#     time.sleep(30)  # Adjust the sleep time as needed for your environment

#     LOGGER.info('Test terminated.')

# The following conditions to completly test this method (not for Gitlab CI/CD)
# 1. A KPI Descriptor must be added in KPI DB with correct device_id. (gNMI OpenConfig driver)
# 2. A collector must be created for the KPI ID.
# 3. A container lab should be running with the gNMI OpenConfig device. 

# def test_generic_collector_handler(
#         telemetry_backend_service, kpi_manager_client, context_client
#         ):
#     telemetry_backend_service.GenericCollectorHandler(
#         collector_id="xxx",
#         kpi_id="6e22f180-ba28-4641-b190-2287bf447777",
#         duration=10.0,
#         interval=5.0,
#         stop_event=""
#     )


# def test_helper_get_subscription_parameters(kpi_manager_client, context_client):
#     """
#     This test validates the correct retrieval of subscription parameters based on a KPI ID.
#     Preconditions:
#         - A KPI Descriptor must be added in KPI DB with correct device_id.
#     """
#     kpi_id = "6e22f180-ba28-4641-b190-2287bf447777"  # Example KPI ID
#     subscription_params = get_subscription_parameters(
#         kpi_id, kpi_manager_client, context_client, 10.0, 5.0
#         )
#     LOGGER.info(f"Subscription Parameters: {subscription_params}")
#     assert subscription_params is not None

#  -------------------------------------------------------------------
#  ---------------------------- OLD TESTS ----------------------------
# --------------------------------------------------------------------

# # ----- Add Topology -----
# def test_add_to_topology(context_client, device_client, service_client):
#     load_topology(context_client, device_client)

# # ----- Add Device to Topology ------
# def test_add_device_to_topology(context_client):
#     context_id = ContextId()
#     context_id.context_uuid.uuid = "43813baf-195e-5da6-af20-b3d0922e71a7"
#     topology_uuid = "c76135e3-24a8-5e92-9bed-c3c9139359c8"
#     device_uuid   = "69a3a3f0-5237-5f9e-bc96-d450d0c6c03a"
#     response      = add_device_to_topology( context_client = context_client, 
#                                             context_id     = context_id, 
#                                             topology_uuid  = topology_uuid,
#                                             device_uuid    = device_uuid
#                                           )
#     LOGGER.info(f"Device added to topology: {response}")
#     assert response is True

# # ----- Get Topology -----
# def test_get_topology(context_client, device_client):
#     response = get_topology(context_client = context_client, topology_uuid = "test1", context_uuid = "test1")
#     LOGGER.info(f"Topology: {response}")
#     assert response is not None

# def test_set_kpi_descriptor_and_get_device_id(kpi_manager_client):
#     kpi_descriptor = _create_kpi_descriptor("1290fb71-bf15-5528-8b69-2d2fabe1fa18")
#     kpi_id         = kpi_manager_client.SetKpiDescriptor(kpi_descriptor)
#     LOGGER.info(f"KPI Descriptor set: {kpi_id}")
#     assert kpi_id is not None

#     response = kpi_manager_client.GetKpiDescriptor(kpi_id)
#     # response = kpi_manager_client.GetKpiDescriptor(_create_kpi_id())

#     assert response is not None
#     LOGGER.info(f"KPI Descriptor: {response}")
#     LOGGER.info(f"Device Id:   {response.device_id.device_uuid.uuid}")
#     LOGGER.info(f"Endpoint Id: {response.endpoint_id.endpoint_uuid.uuid}")

# # ----- Get endpoint detail using device ID -----
# def test_get_device_details(context_client):
#     response = get_device(context_client = context_client, device_uuid = "1290fb71-bf15-5528-8b69-2d2fabe1fa18", include_config_rules = False, include_components = False)
#     if response:
#         LOGGER.info(f"Device type: {response.device_type}")
#         for endpoint in response.device_endpoints:
#             if endpoint.endpoint_id.endpoint_uuid.uuid == '36571df2-bac1-5909-a27d-5f42491d2ff0':
#                 endpoint_dict    = {}
#                 kpi_sample_types = []
#                 # LOGGER.info(f"Endpoint: {endpoint}")
#                 # LOGGER.info(f"Enpoint_uuid: {endpoint.endpoint_id.endpoint_uuid.uuid}")
#                 endpoint_dict["uuid"] = endpoint.endpoint_id.endpoint_uuid.uuid
#                 # LOGGER.info(f"Enpoint_name: {endpoint.name}")
#                 endpoint_dict["name"] = endpoint.name
#                 # LOGGER.info(f"Enpoint_type: {endpoint.endpoint_type}")
#                 endpoint_dict["type"] = endpoint.endpoint_type
#                 for sample_type in endpoint.kpi_sample_types:
#                     # LOGGER.info(f"Enpoint_sample_types: {sample_type}")
#                     kpi_sample_types.append(sample_type)
#                 endpoint_dict["sample_types"] = kpi_sample_types
#                 LOGGER.info(f"Extracted endpoint dict: {endpoint_dict}")
#             else:
#                 LOGGER.info(f"Endpoint not matched")
#     LOGGER.info(f"Device Type: {type(response)}")
#     assert response is not None

# # ----- List Conetxts -----
# def test_list_contextIds(context_client):
#     empty = Empty()
#     response = context_client.ListContexts(empty)
#     LOGGER.info(f"Contexts: {response}")
#     assert response

# # ----- List Devices -----
# def test_list_devices(context_client):
#     empty = Empty()
#     response = context_client.ListDeviceIds(empty)
#     LOGGER.info(f"Devices: {response}")
#     assert response

# ----- Get Endpoints ----- TODO: get_endpoint_names method doesn't return KPI samples types
# def test_get_endpoints(context_client):
#     device_id = DeviceId()
#     device_id.device_uuid.uuid = "1290fb71-bf15-5528-8b69-2d2fabe1fa18"
#     endpoint_id = EndPointId()
#     endpoint_id.endpoint_uuid.uuid = "43b817fa-246f-5e0a-a2e3-2aad0b3e16ca"
#     endpoint_id.device_id.CopyFrom(device_id)
#     response = get_endpoint_names(context_client = context_client, endpoint_ids = [endpoint_id])
#     LOGGER.info(f"Endpoints: {response}")
#     assert response is not None

# # ----- List Topologies -----
# def test_list_topologies(context_client):
#     context_id = ContextId()
#     context_id.context_uuid.uuid = "e7d46baa-d38d-5b72-a082-f344274b63ef"
#     respone = context_client.ListTopologies(context_id)
#     LOGGER.info(f"Topologies: {respone}")

# # ----- Remove Topology -----
# def test_remove_topology(context_client):
#     context_id = ContextId()
#     context_id.context_uuid.uuid = "e7d46baa-d38d-5b72-a082-f344274b63ef"
#     topology_id = TopologyId()
#     topology_id.topology_uuid.uuid = "9ef0118c-4bca-5e81-808b-dc8f60e2cda4"
#     topology_id.context_id.CopyFrom(context_id)

#     response = context_client.RemoveTopology(topology_id)
#     LOGGER.info(f"Topology removed: {response}")

# # ----- Remove context -----
# def test_remove_context(context_client):
#     context_id = ContextId()
#     context_id.context_uuid.uuid = "e7d46baa-d38d-5b72-a082-f344274b63ef"
#     response = context_client.RemoveContext(context_id)
#     LOGGER.info(f"Context removed: {response}")
