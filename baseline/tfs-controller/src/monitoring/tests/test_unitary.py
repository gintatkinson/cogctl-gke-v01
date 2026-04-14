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

import copy, os, pytest #, threading, time
import logging, json
#from queue import Queue
from random import random
from time import sleep
from typing import Union #, Tuple
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED
from grpc._channel import _MultiThreadedRendezvous
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, get_env_var_name, get_service_port_grpc)
from common.proto.context_pb2 import ConfigActionEnum, Context, ContextId, DeviceOperationalStatusEnum, EventTypeEnum, DeviceEvent, Device, Empty, Topology, TopologyId
from common.proto.context_pb2_grpc import add_ContextServiceServicer_to_server
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.monitoring_pb2 import KpiId, KpiDescriptor, SubsDescriptor, SubsList, AlarmID, \
    AlarmDescriptor, AlarmList, KpiDescriptorList, SubsResponse, AlarmResponse, RawKpiTable #, Kpi, KpiList
from common.tests.MockServicerImpl_Context import MockServicerImpl_Context
from common.tools.object_factory.ConfigRule import json_config_rule_set
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Topology import json_topology, json_topology_id
from common.tools.service.GenericGrpcService import GenericGrpcService
from common.tools.timestamp.Converters import timestamp_utcnow_to_float #, timestamp_string_to_float
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from device.service.driver_api.DriverFactory import DriverFactory
from device.service.driver_api.DriverInstanceCache import DriverInstanceCache
from monitoring.client.MonitoringClient import MonitoringClient
#from monitoring.service.AlarmManager import AlarmManager
from monitoring.service.EventTools import EventsDeviceCollector
from monitoring.service.ManagementDBTools import ManagementDB
from monitoring.service.MetricsDBTools import MetricsDB
from monitoring.service.MonitoringService import MonitoringService
from monitoring.service.NameMapping import NameMapping
#from monitoring.service.SubscriptionManager import SubscriptionManager
from monitoring.tests.Messages import create_kpi_request, create_kpi_request_d, include_kpi_request, monitor_kpi_request, \
    create_kpi_request_c, kpi_query, subs_descriptor, alarm_descriptor, alarm_subscription #, create_kpi_request_b
from monitoring.tests.Objects import DEVICE_DEV1, DEVICE_DEV1_CONNECT_RULES, DEVICE_DEV1_UUID, ENDPOINT_END1_UUID

os.environ['DEVICE_EMULATED_ONLY'] = 'TRUE'
from device.service.DeviceService import DeviceService  # pylint: disable=wrong-import-position,ungrouped-imports
from device.service.drivers import DRIVERS              # pylint: disable=wrong-import-position,ungrouped-imports


###########################
# Tests Setup
###########################

LOCAL_HOST = '127.0.0.1'
MOCKSERVICE_PORT = 10000
os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.CONTEXT, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(MOCKSERVICE_PORT)

DEVICE_SERVICE_PORT = MOCKSERVICE_PORT + get_service_port_grpc(ServiceNameEnum.DEVICE) # avoid privileged ports
os.environ[get_env_var_name(ServiceNameEnum.DEVICE, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.DEVICE, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(DEVICE_SERVICE_PORT)

MONITORING_SERVICE_PORT = MOCKSERVICE_PORT + get_service_port_grpc(ServiceNameEnum.MONITORING) # avoid privileged ports
os.environ[get_env_var_name(ServiceNameEnum.MONITORING, ENVVAR_SUFIX_SERVICE_HOST     )] = str(LOCAL_HOST)
os.environ[get_env_var_name(ServiceNameEnum.MONITORING, ENVVAR_SUFIX_SERVICE_PORT_GRPC)] = str(MONITORING_SERVICE_PORT)

METRICSDB_HOSTNAME = os.environ.get('METRICSDB_HOSTNAME')
METRICSDB_ILP_PORT = os.environ.get('METRICSDB_ILP_PORT')
METRICSDB_REST_PORT = os.environ.get('METRICSDB_REST_PORT')
METRICSDB_TABLE_MONITORING_KPIS = os.environ.get('METRICSDB_TABLE_MONITORING_KPIS')

LOGGER = logging.getLogger(__name__)

class MockContextService(GenericGrpcService):
    # Mock Service implementing Context to simplify unitary tests of Monitoring

    def __init__(self, bind_port: Union[str, int]) -> None:
        super().__init__(bind_port, LOCAL_HOST, enable_health_servicer=False, cls_name='MockService')

    # pylint: disable=attribute-defined-outside-init
    def install_servicers(self):
        self.context_servicer = MockServicerImpl_Context()
        add_ContextServiceServicer_to_server(self.context_servicer, self.server)

@pytest.fixture(scope='session')
def context_service():
    LOGGER.info('Initializing MockContextService...')
    _service = MockContextService(MOCKSERVICE_PORT)
    _service.start()
    
    LOGGER.info('Yielding MockContextService...')
    yield _service

    LOGGER.info('Terminating MockContextService...')
    _service.context_servicer.msg_broker.terminate()
    _service.stop()

    LOGGER.info('Terminated MockContextService...')

@pytest.fixture(scope='session')
def context_client(context_service : MockContextService): # pylint: disable=redefined-outer-name,unused-argument
    LOGGER.info('Initializing ContextClient...')
    _client = ContextClient()
    
    LOGGER.info('Yielding ContextClient...')
    yield _client

    LOGGER.info('Closing ContextClient...')
    _client.close()

    LOGGER.info('Closed ContextClient...')

@pytest.fixture(scope='session')
def device_service(context_service : MockContextService): # pylint: disable=redefined-outer-name,unused-argument
    LOGGER.info('Initializing DeviceService...')
    driver_factory = DriverFactory(DRIVERS)
    driver_instance_cache = DriverInstanceCache(driver_factory)
    _service = DeviceService(driver_instance_cache)
    _service.start()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding DeviceService...')
    yield _service

    LOGGER.info('Terminating DeviceService...')
    _service.stop()

    LOGGER.info('Terminated DeviceService...')

@pytest.fixture(scope='session')
def device_client(device_service : DeviceService): # pylint: disable=redefined-outer-name,unused-argument
    LOGGER.info('Initializing DeviceClient...')
    _client = DeviceClient()

    LOGGER.info('Yielding DeviceClient...')
    yield _client

    LOGGER.info('Closing DeviceClient...')
    _client.close()

    LOGGER.info('Closed DeviceClient...')

# This fixture will be requested by test cases and last during testing session
@pytest.fixture(scope='session')
def monitoring_service(
        context_service : MockContextService,  # pylint: disable=redefined-outer-name,unused-argument
        device_service : DeviceService     # pylint: disable=redefined-outer-name,unused-argument
    ):
    LOGGER.info('Initializing MonitoringService...')
    name_mapping = NameMapping()
    _service = MonitoringService(name_mapping)
    _service.start()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding MonitoringService...')
    yield _service

    LOGGER.info('Terminating MonitoringService...')
    _service.stop()

    LOGGER.info('Terminated MonitoringService...')

# This fixture will be requested by test cases and last during testing session.
# The client requires the server, so client fixture has the server as dependency.
@pytest.fixture(scope='session')
def monitoring_client(monitoring_service : MonitoringService): # pylint: disable=redefined-outer-name,unused-argument
    LOGGER.info('Initializing MonitoringClient...')
    _client = MonitoringClient()

    # yield the server, when test finishes, execution will resume to stop it
    LOGGER.info('Yielding MonitoringClient...')
    yield _client

    LOGGER.info('Closing MonitoringClient...')
    _client.close()

    LOGGER.info('Closed MonitoringClient...')

@pytest.fixture(scope='session')
def management_db():
    _management_db = ManagementDB('monitoring.db')
    return _management_db

@pytest.fixture(scope='session')
def metrics_db(monitoring_service : MonitoringService): # pylint: disable=redefined-outer-name
    return monitoring_service.monitoring_servicer.metrics_db
    #_metrics_db = MetricsDBTools.MetricsDB(
    #    METRICSDB_HOSTNAME, METRICSDB_ILP_PORT, METRICSDB_REST_PORT, METRICSDB_TABLE_MONITORING_KPIS)
    #return _metrics_db

@pytest.fixture(scope='session')
def subs_scheduler():
    _scheduler = BackgroundScheduler(executors={'processpool': ProcessPoolExecutor(max_workers=20)})
    _scheduler.start()

    return _scheduler

def ingestion_data(kpi_id_int):
    # pylint: disable=redefined-outer-name,unused-argument
    metrics_db = MetricsDB('localhost', '9009', '9000', 'monitoring')

    kpiSampleType = KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED
    kpiSampleType_name = KpiSampleType.Name(kpiSampleType).upper().replace('KPISAMPLETYPE_', '')
    for _ in range(50):
        kpiSampleType   = kpiSampleType_name
        kpiId           = kpi_id_int
        deviceId        = 'DEV'+ str(kpi_id_int)
        endpointId      = 'END' + str(kpi_id_int)
        serviceId       = 'SERV' + str(kpi_id_int)
        sliceId         = 'SLC' + str(kpi_id_int)
        connectionId    = 'CON' + str(kpi_id_int)
        time_stamp      = timestamp_utcnow_to_float()
        kpi_value       = 500*random()

        metrics_db.write_KPI(time_stamp, kpiId, kpiSampleType, deviceId, endpointId, serviceId, sliceId, connectionId,
                                  kpi_value)
        sleep(0.1)

##################################################
# Prepare Environment, should be the first test
##################################################

def test_prepare_environment(
    context_client : ContextClient,                 # pylint: disable=redefined-outer-name,unused-argument
):
    context_id = json_context_id(DEFAULT_CONTEXT_NAME)
    context_client.SetContext(Context(**json_context(DEFAULT_CONTEXT_NAME)))
    context_client.SetTopology(Topology(**json_topology(DEFAULT_TOPOLOGY_NAME, context_id=context_id)))


###########################
# Tests Implementation
###########################

# Test case that makes use of client fixture to test server's CreateKpi method
def test_set_kpi(monitoring_client): # pylint: disable=redefined-outer-name
    # make call to server
    LOGGER.warning('test_create_kpi requesting')
    for i in range(3):
        response = monitoring_client.SetKpi(create_kpi_request(str(i+1)))
        LOGGER.debug(str(response))
        assert isinstance(response, KpiId)


# Test case that makes use of client fixture to test server's DeleteKpi method
def test_delete_kpi(monitoring_client): # pylint: disable=redefined-outer-name
    # make call to server
    LOGGER.warning('delete_kpi requesting')
    response = monitoring_client.SetKpi(create_kpi_request('4'))
    response = monitoring_client.DeleteKpi(response)
    LOGGER.debug(str(response))
    assert isinstance(response, Empty)

# Test case that makes use of client fixture to test server's GetKpiDescriptor method
def test_get_kpidescritor(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_getkpidescritor_kpi begin')
    response = monitoring_client.SetKpi(create_kpi_request('1'))
    response = monitoring_client.GetKpiDescriptor(response)
    LOGGER.debug(str(response))
    assert isinstance(response, KpiDescriptor)

# Test case that makes use of client fixture to test server's GetKpiDescriptor method
def test_get_kpi_descriptor_list(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_getkpidescritor_kpi begin')
    response = monitoring_client.GetKpiDescriptorList(Empty())
    LOGGER.debug(str(response))
    assert isinstance(response, KpiDescriptorList)

# Test case that makes use of client fixture to test server's IncludeKpi method
def test_include_kpi(monitoring_client): # pylint: disable=redefined-outer-name
    # make call to server
    LOGGER.warning('test_include_kpi requesting')
    kpi_id = monitoring_client.SetKpi(create_kpi_request('1'))
    LOGGER.debug(str(kpi_id))
    response = monitoring_client.IncludeKpi(include_kpi_request(kpi_id))
    LOGGER.debug(str(response))
    assert isinstance(response, Empty)

# Test case that makes use of client fixture to test server's MonitorKpi method
def test_monitor_kpi(
        context_client : ContextClient,                 # pylint: disable=redefined-outer-name,unused-argument
        device_client : DeviceClient,                   # pylint: disable=redefined-outer-name
        monitoring_client : MonitoringClient,           # pylint: disable=redefined-outer-name
    ):
    LOGGER.info('test_monitor_kpi begin')

    # ----- Update the object ------------------------------------------------------------------------------------------
    LOGGER.info('Adding Device {:s}'.format(DEVICE_DEV1_UUID))
    device_with_connect_rules = copy.deepcopy(DEVICE_DEV1)
    device_with_connect_rules['device_config']['config_rules'].extend(DEVICE_DEV1_CONNECT_RULES)
    device_id = device_client.AddDevice(Device(**device_with_connect_rules))
    assert device_id.device_uuid.uuid == DEVICE_DEV1_UUID

    response = monitoring_client.SetKpi(create_kpi_request('1'))
    _monitor_kpi_request = monitor_kpi_request(response.kpi_id.uuid, 120, 5) # pylint: disable=maybe-no-member
    response = monitoring_client.MonitorKpi(_monitor_kpi_request)
    LOGGER.debug(str(response))
    assert isinstance(response, Empty)

    device_client.DeleteDevice(device_id)

# Test case that makes use of client fixture to test server's QueryKpiData method
def test_query_kpi_data(monitoring_client,subs_scheduler): # pylint: disable=redefined-outer-name

    kpi_id_list = []
    for i in range(2):
        kpi_id = monitoring_client.SetKpi(create_kpi_request(str(i+1)))
        subs_scheduler.add_job(ingestion_data, args=[kpi_id.kpi_id.uuid])
        kpi_id_list.append(kpi_id)
    LOGGER.warning('test_query_kpi_data')
    sleep(5)
    response = monitoring_client.QueryKpiData(kpi_query(kpi_id_list))
    LOGGER.debug(str(response))
    assert isinstance(response, RawKpiTable)
    if (subs_scheduler.state != STATE_STOPPED):
        subs_scheduler.shutdown()

# Test case that makes use of client fixture to test server's SetKpiSubscription method
def test_set_kpi_subscription(monitoring_client,subs_scheduler): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_set_kpi_subscription')
    kpi_id = monitoring_client.SetKpi(create_kpi_request('1'))
    subs_scheduler.add_job(ingestion_data, args=[kpi_id.kpi_id.uuid])
    response = monitoring_client.SetKpiSubscription(subs_descriptor(kpi_id))
    assert isinstance(response, _MultiThreadedRendezvous)
    for item in response:
        LOGGER.debug(item)
        assert isinstance(item, SubsResponse)
    if (subs_scheduler.state != STATE_STOPPED):
        subs_scheduler.shutdown()

# Test case that makes use of client fixture to test server's GetSubsDescriptor method
def test_get_subs_descriptor(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_get_subs_descriptor')
    kpi_id = monitoring_client.SetKpi(create_kpi_request_c())
    monitoring_client.IncludeKpi(include_kpi_request(kpi_id))
    response = monitoring_client.SetKpiSubscription(subs_descriptor(kpi_id))
    for item in response:
        response = monitoring_client.GetSubsDescriptor(item.subs_id)
        LOGGER.debug(response)
        assert isinstance(response, SubsDescriptor)

# Test case that makes use of client fixture to test server's GetSubscriptions method
def test_get_subscriptions(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_get_subscriptions')
    response = monitoring_client.GetSubscriptions(Empty())
    LOGGER.debug(response)
    assert isinstance(response, SubsList)

# Test case that makes use of client fixture to test server's DeleteSubscription method
def test_delete_subscription(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_delete_subscription')
    kpi_id = monitoring_client.SetKpi(create_kpi_request_c())
    monitoring_client.IncludeKpi(include_kpi_request(kpi_id))
    subs = monitoring_client.SetKpiSubscription(subs_descriptor(kpi_id))
    for item in subs:
        response = monitoring_client.DeleteSubscription(item.subs_id)
        assert isinstance(response, Empty)

# Test case that makes use of client fixture to test server's SetKpiAlarm method
def test_set_kpi_alarm(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_set_kpi_alarm')
    kpi_id = monitoring_client.SetKpi(create_kpi_request_c())
    response = monitoring_client.SetKpiAlarm(alarm_descriptor(kpi_id))
    LOGGER.debug(str(response))
    assert isinstance(response, AlarmID)

# Test case that makes use of client fixture to test server's GetAlarms method
def test_get_alarms(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_get_alarms')
    response = monitoring_client.GetAlarms(Empty())
    LOGGER.debug(response)
    assert isinstance(response, AlarmList)

# Test case that makes use of client fixture to test server's GetAlarmDescriptor method
def test_get_alarm_descriptor(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_get_alarm_descriptor')
    _kpi_id = monitoring_client.SetKpi(create_kpi_request_c())
    _alarm_id = monitoring_client.SetKpiAlarm(alarm_descriptor(_kpi_id))
    _response = monitoring_client.GetAlarmDescriptor(_alarm_id)
    LOGGER.debug(_response)
    assert isinstance(_response, AlarmDescriptor)

# Test case that makes use of client fixture to test server's GetAlarmResponseStream method
def test_get_alarm_response_stream(monitoring_client,subs_scheduler): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_get_alarm_descriptor')
    _kpi_id = monitoring_client.SetKpi(create_kpi_request('3'))
    _alarm_id = monitoring_client.SetKpiAlarm(alarm_descriptor(_kpi_id))
    subs_scheduler.add_job(ingestion_data,args=[_kpi_id.kpi_id.uuid])
    _response = monitoring_client.GetAlarmResponseStream(alarm_subscription(_alarm_id))
    assert isinstance(_response, _MultiThreadedRendezvous)
    for item in _response:
        LOGGER.debug(item)
        assert isinstance(item,AlarmResponse)

    if(subs_scheduler.state != STATE_STOPPED):
        subs_scheduler.shutdown()

# Test case that makes use of client fixture to test server's DeleteAlarm method
def test_delete_alarm(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_delete_alarm')
    _kpi_id = monitoring_client.SetKpi(create_kpi_request_c())
    _alarm_id = monitoring_client.SetKpiAlarm(alarm_descriptor(_kpi_id))
    _response = monitoring_client.DeleteAlarm(_alarm_id)
    LOGGER.debug(type(_response))
    assert isinstance(_response, Empty)

# Test case that makes use of client fixture to test server's GetStreamKpi method
def test_get_stream_kpi(monitoring_client): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_getstream_kpi begin')
    _kpi_id = monitoring_client.SetKpi(create_kpi_request_d())
    response = monitoring_client.GetStreamKpi(_kpi_id)
    LOGGER.debug(str(response))
    assert isinstance(response, _MultiThreadedRendezvous)

# Test case that makes use of client fixture to test server's GetInstantKpi method
# def test_get_instant_kpi(monitoring_client): # pylint: disable=redefined-outer-name
#     LOGGER.warning('test_getinstant_kpi begin')
#     kpi_id = monitoring_client.SetKpi(KpiId())
#     monitoring_client.IncludeKpi(include_kpi_request(kpi_id))
#     sleep(0.3)
#     response = monitoring_client.GetInstantKpi(kpi_id)
#     LOGGER.debug(response)
#     assert isinstance(response, Kpi)

def test_managementdb_tools_kpis(management_db): # pylint: disable=redefined-outer-name
    LOGGER.warning('test_managementdb_tools_kpis begin')
    _create_kpi_request = create_kpi_request('5')
    kpi_description    = _create_kpi_request.kpi_description                    # pylint: disable=maybe-no-member
    kpi_sample_type    = _create_kpi_request.kpi_sample_type                    # pylint: disable=maybe-no-member
    kpi_device_id      = _create_kpi_request.device_id.device_uuid.uuid         # pylint: disable=maybe-no-member
    kpi_endpoint_id    = _create_kpi_request.endpoint_id.endpoint_uuid.uuid     # pylint: disable=maybe-no-member
    kpi_service_id     = _create_kpi_request.service_id.service_uuid.uuid       # pylint: disable=maybe-no-member
    kpi_slice_id       = _create_kpi_request.slice_id.slice_uuid.uuid           # pylint: disable=maybe-no-member
    kpi_connection_id  = _create_kpi_request.connection_id.connection_uuid.uuid # pylint: disable=maybe-no-member
    link_id            = _create_kpi_request.link_id.link_uuid.uuid             # pylint: disable=maybe-no-member

    _kpi_id = management_db.insert_KPI(
        kpi_description, kpi_sample_type, kpi_device_id, kpi_endpoint_id, kpi_service_id,
        kpi_slice_id, kpi_connection_id, link_id)
    assert isinstance(_kpi_id, int)

    response = management_db.get_KPI(_kpi_id)
    assert isinstance(response, tuple)

    response = management_db.set_monitoring_flag(_kpi_id,True)
    assert response is True
    response = management_db.check_monitoring_flag(_kpi_id)
    assert response is True
    management_db.set_monitoring_flag(_kpi_id, False)
    response = management_db.check_monitoring_flag(_kpi_id)
    assert response is False

    response = management_db.get_KPIS()
    assert isinstance(response, list)

    response = management_db.delete_KPI(_kpi_id)
    assert response


def test_managementdb_tools_insert_alarm(management_db):
    LOGGER.warning('test_managementdb_tools_insert_alarm begin')

    _alarm_description  = "Alarm Description"
    _alarm_name         = "Alarm Name"
    _kpi_id             = "3"
    _kpi_min_value      = 0.0
    _kpi_max_value      = 250.0
    _in_range           = True
    _include_min_value  = False
    _include_max_value  = True

    _alarm_id = management_db.insert_alarm(_alarm_description, _alarm_name, _kpi_id, _kpi_min_value,
                                               _kpi_max_value,
                                               _in_range, _include_min_value, _include_max_value)
    LOGGER.debug(_alarm_id)
    assert isinstance(_alarm_id,int)
#
# def test_metrics_db_tools(metrics_db): # pylint: disable=redefined-outer-name
#     LOGGER.warning('test_metric_sdb_tools_write_kpi begin')
#     _kpiId = "6"
#
#     for i in range(50):
#         _kpiSampleType = KpiSampleType.Name(KpiSampleType.KPISAMPLETYPE_PACKETS_RECEIVED).upper().replace('KPISAMPLETYPE_', '')
#         _deviceId = 'DEV4'
#         _endpointId = 'END4'
#         _serviceId = 'SERV4'
#         _sliceId = 'SLC4'
#         _connectionId = 'CON4'
#         _time_stamp = timestamp_utcnow_to_float()
#         _kpi_value = 500*random()
#
#         metrics_db.write_KPI(_time_stamp, _kpiId, _kpiSampleType, _deviceId, _endpointId, _serviceId, _sliceId, _connectionId,
#                                   _kpi_value)
#         sleep(0.05)
#
#     _query = f"SELECT * FROM monitoring WHERE kpi_id ='{_kpiId}'"
#     _data = metrics_db.run_query(_query)
#     assert len(_data) >= 50
#
# def test_subscription_manager_create_subscription(management_db,metrics_db,subs_scheduler):
#     LOGGER.warning('test_subscription_manager_create_subscription begin')
#     subs_queue = Queue()
#
#     subs_manager = SubscriptionManager(metrics_db)
#
#     subs_scheduler.add_job(ingestion_data)
#
#     kpi_id = "3"
#     sampling_duration_s = 20
#     sampling_interval_s = 3
#     real_start_time     = timestamp_utcnow_to_float()
#     start_timestamp     = real_start_time
#     end_timestamp       = start_timestamp + sampling_duration_s
#
#     subs_id = management_db.insert_subscription(kpi_id, "localhost", sampling_duration_s,
#                                                sampling_interval_s,start_timestamp,end_timestamp)
#     subs_manager.create_subscription(subs_queue,subs_id,kpi_id,sampling_interval_s,
#                                      sampling_duration_s,start_timestamp,end_timestamp)
#
#     # This is here to simulate application activity (which keeps the main thread alive).
#     total_points = 0
#     while True:
#         while not subs_queue.empty():
#             list = subs_queue.get_nowait()
#             kpi_list = KpiList()
#             for item in list:
#                 kpi = Kpi()
#                 kpi.kpi_id.kpi_id.uuid = item[0]
#                 kpi.timestamp.timestamp = timestamp_string_to_float(item[1])
#                 kpi.kpi_value.floatVal = item[2]
#                 kpi_list.kpi.append(kpi)
#                 total_points += 1
#             LOGGER.debug(kpi_list)
#         if timestamp_utcnow_to_float() > end_timestamp:
#             break
#
#     assert total_points != 0

def test_events_tools(
        context_client : ContextClient,                 # pylint: disable=redefined-outer-name,unused-argument
        device_client : DeviceClient,                   # pylint: disable=redefined-outer-name
        monitoring_client : MonitoringClient,           # pylint: disable=redefined-outer-name,unused-argument
        metrics_db : MetricsDB,                         # pylint: disable=redefined-outer-name
    ):
    LOGGER.warning('test_get_device_events begin')

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    events_collector = EventsDeviceCollector(metrics_db.name_mapping)
    events_collector.start()

    # ----- Update the object ------------------------------------------------------------------------------------------
    LOGGER.info('Adding Device {:s}'.format(DEVICE_DEV1_UUID))
    device_with_connect_rules = copy.deepcopy(DEVICE_DEV1)
    device_with_connect_rules['device_config']['config_rules'].extend(DEVICE_DEV1_CONNECT_RULES)
    response = device_client.AddDevice(Device(**device_with_connect_rules))
    assert response.device_uuid.uuid == DEVICE_DEV1_UUID

    device_client.DeleteDevice(response)
    events_collector.stop()

    LOGGER.warning('test_get_device_events end')


def test_get_device_events(
        context_client : ContextClient,                 # pylint: disable=redefined-outer-name,unused-argument
        device_client : DeviceClient,                   # pylint: disable=redefined-outer-name
        monitoring_client : MonitoringClient,           # pylint: disable=redefined-outer-name,unused-argument
        metrics_db : MetricsDB,                         # pylint: disable=redefined-outer-name
    ):

    LOGGER.warning('test_get_device_events begin')

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    events_collector = EventsDeviceCollector(metrics_db.name_mapping)
    events_collector.start()

    # ----- Check create event -----------------------------------------------------------------------------------------
    LOGGER.info('Adding Device {:s}'.format(DEVICE_DEV1_UUID))
    device_with_connect_rules = copy.deepcopy(DEVICE_DEV1)
    device_with_connect_rules['device_config']['config_rules'].extend(DEVICE_DEV1_CONNECT_RULES)
    response = device_client.AddDevice(Device(**device_with_connect_rules))
    assert response.device_uuid.uuid == DEVICE_DEV1_UUID

    event = events_collector.get_event(block=True)
    assert isinstance(event, DeviceEvent)
    assert event.event.event_type == EventTypeEnum.EVENTTYPE_CREATE
    assert event.device_id.device_uuid.uuid == DEVICE_DEV1_UUID

    device_client.DeleteDevice(response)
    events_collector.stop()

    LOGGER.warning('test_get_device_events end')

def test_listen_events(
        context_client : ContextClient,                 # pylint: disable=redefined-outer-name,unused-argument
        device_client : DeviceClient,                   # pylint: disable=redefined-outer-name
        monitoring_client : MonitoringClient,           # pylint: disable=redefined-outer-name,unused-argument
        metrics_db : MetricsDB,                         # pylint: disable=redefined-outer-name
    ):

    LOGGER.warning('test_listen_events begin')

    # ----- Initialize the EventsCollector -----------------------------------------------------------------------------
    events_collector = EventsDeviceCollector(metrics_db.name_mapping)
    events_collector.start()

    LOGGER.info('Adding Device {:s}'.format(DEVICE_DEV1_UUID))
    device_with_connect_rules = copy.deepcopy(DEVICE_DEV1)
    device_with_connect_rules['device_config']['config_rules'].extend(DEVICE_DEV1_CONNECT_RULES)
    response = device_client.AddDevice(Device(**device_with_connect_rules))
    assert response.device_uuid.uuid == DEVICE_DEV1_UUID

    LOGGER.info('Activating Device {:s}'.format(DEVICE_DEV1_UUID))
    device = context_client.GetDevice(response)
    device_with_op_state = Device()
    device_with_op_state.CopyFrom(device)
    device_with_op_state.device_operational_status = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED
    config_rule = device_with_op_state.device_config.config_rules.add()
    config_rule.action = ConfigActionEnum.CONFIGACTION_SET
    config_rule.custom.resource_key = '/interface[{:s}]'.format(ENDPOINT_END1_UUID)
    config_rule.custom.resource_value = json.dumps({'name': ENDPOINT_END1_UUID, 'enabled': True})
    response = context_client.SetDevice(device_with_op_state)
    assert response.device_uuid.uuid == DEVICE_DEV1_UUID

    sleep(1.0)

    kpi_id_list = events_collector.listen_events()
    assert len(kpi_id_list) > 0

    device_client.DeleteDevice(response)
    events_collector.stop()

    LOGGER.warning('test_listen_events end')


##################################################
# Cleanup Environment, should be the last test
##################################################
def test_cleanup_environment(
    context_client : ContextClient,                 # pylint: disable=redefined-outer-name,unused-argument
):
    context_id = json_context_id(DEFAULT_CONTEXT_NAME)
    context_client.RemoveTopology(TopologyId(**json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=context_id)))
    context_client.RemoveContext(ContextId(**context_id))
