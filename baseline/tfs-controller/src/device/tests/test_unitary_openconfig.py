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

import calendar, copy, dateutil.parser, grpc, logging, pytest, queue, time
from datetime import datetime, timezone
from common.proto.context_pb2 import ConfigActionEnum, Device, DeviceId
from common.proto.device_pb2 import MonitoringSettings
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.EndPoint import json_endpoint_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from device.service.DeviceService import DeviceService
from device.service.driver_api._Driver import _Driver
from .MockService_Dependencies import MockService_Dependencies
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    mock_service, device_service, context_client, device_client, monitoring_client, test_prepare_environment)

try:
    #from .Device_OpenConfig_Infinera1 import(
    #from .Device_OpenConfig_Infinera2 import(
    #from .Device_OpenConfig_Adva import(
    #from .Device_OpenConfig_Adva_149 import(
    from .Device_OpenConfig_Adva_155 import(
    #from .Device_OpenConfig_Cisco import(
        DEVICE_OC, DEVICE_OC_CONFIG_RULES, DEVICE_OC_DECONFIG_RULES, DEVICE_OC_CONNECT_RULES, DEVICE_OC_ID,
        DEVICE_OC_UUID)
    ENABLE_OPENCONFIG = True
except ImportError:
    ENABLE_OPENCONFIG = False

ENABLE_OPENCONFIG_CONFIGURE   = True
ENABLE_OPENCONFIG_MONITOR     = False
ENABLE_OPENCONFIG_DECONFIGURE = True

logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
logging.getLogger('apscheduler.scheduler').setLevel(logging.WARNING)
logging.getLogger('monitoring-client').setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


# ----- Test Device Driver OpenConfig ------------------------------------------

def test_device_openconfig_add_error_cases(
    context_client : ContextClient,     # pylint: disable=redefined-outer-name
    device_client : DeviceClient,       # pylint: disable=redefined-outer-name
    device_service : DeviceService):    # pylint: disable=redefined-outer-name

    if not ENABLE_OPENCONFIG: pytest.skip('Skipping test: No OpenConfig device has been configured')

    with pytest.raises(grpc.RpcError) as e:
        DEVICE_OC_WITH_EXTRA_RULES = copy.deepcopy(DEVICE_OC)
        DEVICE_OC_WITH_EXTRA_RULES['device_config']['config_rules'].extend(DEVICE_OC_CONNECT_RULES)
        DEVICE_OC_WITH_EXTRA_RULES['device_config']['config_rules'].extend(DEVICE_OC_CONFIG_RULES)
        device_client.AddDevice(Device(**DEVICE_OC_WITH_EXTRA_RULES))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    msg_head = 'device.device_config.config_rules(['
    msg_tail = ']) is invalid; RPC method AddDevice only accepts connection Config Rules that should start '\
               'with "_connect/" tag. Others should be configured after adding the device.'
    except_msg = str(e.value.details())
    assert except_msg.startswith(msg_head) and except_msg.endswith(msg_tail)


def test_device_openconfig_add_correct(
    context_client : ContextClient,     # pylint: disable=redefined-outer-name
    device_client : DeviceClient,       # pylint: disable=redefined-outer-name
    device_service : DeviceService):    # pylint: disable=redefined-outer-name

    if not ENABLE_OPENCONFIG: pytest.skip('Skipping test: No OpenConfig device has been configured')

    DEVICE_OC_WITH_CONNECT_RULES = copy.deepcopy(DEVICE_OC)
    DEVICE_OC_WITH_CONNECT_RULES['device_config']['config_rules'].extend(DEVICE_OC_CONNECT_RULES)
    device_client.AddDevice(Device(**DEVICE_OC_WITH_CONNECT_RULES))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_OC_UUID) # we know the driver exists now
    assert driver is not None

    device_data = context_client.GetDevice(DeviceId(**DEVICE_OC_ID))
    config_rules = [
        (ConfigActionEnum.Name(config_rule.action), config_rule.custom.resource_key, config_rule.custom.resource_value)
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(['{:s} {:s} = {:s}'.format(*config_rule) for config_rule in config_rules])))


def test_device_openconfig_get(
    context_client : ContextClient,     # pylint: disable=redefined-outer-name
    device_client : DeviceClient,       # pylint: disable=redefined-outer-name
    device_service : DeviceService):    # pylint: disable=redefined-outer-name

    if not ENABLE_OPENCONFIG: pytest.skip('Skipping test: No OpenConfig device has been configured')

    initial_config = device_client.GetInitialConfig(DeviceId(**DEVICE_OC_ID))
    LOGGER.info('initial_config = {:s}'.format(grpc_message_to_json_string(initial_config)))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_OC_ID))
    LOGGER.info('device_data = {:s}'.format(grpc_message_to_json_string(device_data)))


def test_device_openconfig_configure(
    context_client : ContextClient,     # pylint: disable=redefined-outer-name
    device_client : DeviceClient,       # pylint: disable=redefined-outer-name
    device_service : DeviceService):    # pylint: disable=redefined-outer-name

    if not ENABLE_OPENCONFIG: pytest.skip('Skipping test: No OpenConfig device has been configured')
    if not ENABLE_OPENCONFIG_CONFIGURE: pytest.skip('Skipping test OpenConfig configure')

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_OC_UUID) # we know the driver exists now
    assert driver is not None

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    DEVICE_OC_WITH_CONFIG_RULES = copy.deepcopy(DEVICE_OC)
    DEVICE_OC_WITH_CONFIG_RULES['device_config']['config_rules'].extend(DEVICE_OC_CONFIG_RULES)
    device_client.ConfigureDevice(Device(**DEVICE_OC_WITH_CONFIG_RULES))

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_OC_ID))
    config_rules = [
        (ConfigActionEnum.Name(config_rule.action), config_rule.custom.resource_key, config_rule.custom.resource_value)
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(['{:s} {:s} = {:s}'.format(*config_rule) for config_rule in config_rules])))
    for config_rule in DEVICE_OC_CONFIG_RULES:
        assert 'custom' in config_rule
        config_rule = (
            ConfigActionEnum.Name(config_rule['action']), config_rule['custom']['resource_key'],
            config_rule['custom']['resource_value'])
        assert config_rule in config_rules


def test_device_openconfig_monitor(
    context_client : ContextClient,             # pylint: disable=redefined-outer-name
    device_client : DeviceClient,               # pylint: disable=redefined-outer-name
    device_service : DeviceService,             # pylint: disable=redefined-outer-name
    mock_service : MockService_Dependencies):   # pylint: disable=redefined-outer-name

    if not ENABLE_OPENCONFIG: pytest.skip('Skipping test: No OpenConfig device has been configured')
    if not ENABLE_OPENCONFIG_MONITOR: pytest.skip('Skipping test OpenConfig monitor')

    device_uuid = DEVICE_OC_UUID
    json_device_id = DEVICE_OC_ID
    device_id = DeviceId(**json_device_id)
    device_data = context_client.GetDevice(device_id)
    #LOGGER.info('device_data = \n{:s}'.format(str(device_data)))

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(device_uuid) # we know the driver exists now
    assert driver is not None

    SAMPLING_DURATION_SEC = 60.0
    SAMPLING_INTERVAL_SEC = 15.0

    MONITORING_SETTINGS_LIST = []
    KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED = {}
    for endpoint in device_data.device_endpoints:
        endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
        for sample_type_id in endpoint.kpi_sample_types:
            sample_type_name = str(KpiSampleType.Name(sample_type_id)).upper().replace('KPISAMPLETYPE_', '')
            kpi_uuid = '{:s}-{:s}-{:s}-kpi_uuid'.format(device_uuid, endpoint_uuid, str(sample_type_id))
            monitoring_settings = {
                'kpi_id'        : {'kpi_id': {'uuid': kpi_uuid}},
                'kpi_descriptor': {
                    'kpi_description': 'Metric {:s} for Endpoint {:s} in Device {:s}'.format(
                        sample_type_name, endpoint_uuid, device_uuid),
                    'kpi_sample_type': sample_type_id,
                    'device_id': json_device_id,
                    'endpoint_id': json_endpoint_id(json_device_id, endpoint_uuid),
                },
                'sampling_duration_s': SAMPLING_DURATION_SEC,
                'sampling_interval_s': SAMPLING_INTERVAL_SEC,
            }
            MONITORING_SETTINGS_LIST.append(monitoring_settings)
            KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED[kpi_uuid] = 0

    NUM_SAMPLES_EXPECTED_PER_KPI = SAMPLING_DURATION_SEC / SAMPLING_INTERVAL_SEC
    NUM_SAMPLES_EXPECTED = len(MONITORING_SETTINGS_LIST) * NUM_SAMPLES_EXPECTED_PER_KPI

    # Start monitoring the device
    t_start_monitoring = datetime.timestamp(datetime.utcnow())
    for monitoring_settings in MONITORING_SETTINGS_LIST:
        device_client.MonitorDeviceKpi(MonitoringSettings(**monitoring_settings))

    # wait to receive the expected number of samples
    # if takes more than 1.5 times the sampling duration, assume there is an error
    time_ini = time.time()
    queue_samples : queue.Queue = mock_service.queue_samples
    received_samples = []
    while (len(received_samples) < NUM_SAMPLES_EXPECTED) and (time.time() - time_ini < SAMPLING_DURATION_SEC * 1.5):
        try:
            received_sample = queue_samples.get(block=True, timeout=SAMPLING_INTERVAL_SEC / NUM_SAMPLES_EXPECTED)
            #LOGGER.info('received_sample = {:s}'.format(str(received_sample)))
            received_samples.append(received_sample)
        except queue.Empty:
            continue

    t_end_monitoring = datetime.timestamp(datetime.utcnow())

    #LOGGER.info('received_samples = {:s}'.format(str(received_samples)))
    LOGGER.info('len(received_samples) = {:s}'.format(str(len(received_samples))))
    LOGGER.info('NUM_SAMPLES_EXPECTED = {:s}'.format(str(NUM_SAMPLES_EXPECTED)))
    #assert len(received_samples) == NUM_SAMPLES_EXPECTED
    for received_sample in received_samples:
        kpi_uuid = received_sample.kpi_id.kpi_id.uuid
        assert kpi_uuid in KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED
        assert isinstance(received_sample.timestamp, str)
        try:
            timestamp = float(received_sample.timestamp)
        except ValueError:
            dt_time = dateutil.parser.isoparse(received_sample.timestamp).replace(tzinfo=timezone.utc)
            timestamp = float(calendar.timegm(dt_time.timetuple())) + (dt_time.microsecond / 1.e6)
        assert timestamp > t_start_monitoring
        assert timestamp < t_end_monitoring
        assert received_sample.kpi_value.HasField('floatVal') or received_sample.kpi_value.HasField('intVal')
        kpi_value = getattr(received_sample.kpi_value, received_sample.kpi_value.WhichOneof('value'))
        assert isinstance(kpi_value, (float, int))
        KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED[kpi_uuid] += 1

    LOGGER.info('KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED = {:s}'.format(str(KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED)))
    # TODO: review why num_samples_received per KPI != NUM_SAMPLES_EXPECTED_PER_KPI
    #for kpi_uuid, num_samples_received in KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED.items():
    #    assert num_samples_received == NUM_SAMPLES_EXPECTED_PER_KPI

    # Unsubscribe monitoring
    for kpi_uuid in KPI_UUIDS__TO__NUM_SAMPLES_RECEIVED:
        MONITORING_SETTINGS_UNSUBSCRIBE = {
            'kpi_id'             : {'kpi_id': {'uuid': kpi_uuid}},
            'sampling_duration_s': -1, # negative value in sampling_duration_s or sampling_interval_s means unsibscribe
            'sampling_interval_s': -1, # kpi_id is mandatory to unsibscribe
        }
        device_client.MonitorDeviceKpi(MonitoringSettings(**MONITORING_SETTINGS_UNSUBSCRIBE))


def test_device_openconfig_deconfigure(
    context_client : ContextClient,     # pylint: disable=redefined-outer-name
    device_client : DeviceClient,       # pylint: disable=redefined-outer-name
    device_service : DeviceService):    # pylint: disable=redefined-outer-name

    if not ENABLE_OPENCONFIG: pytest.skip('Skipping test: No OpenConfig device has been configured')
    if not ENABLE_OPENCONFIG_DECONFIGURE: pytest.skip('Skipping test OpenConfig deconfigure')

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_OC_UUID) # we know the driver exists now
    assert driver is not None

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    DEVICE_OC_WITH_DECONFIG_RULES = copy.deepcopy(DEVICE_OC)
    DEVICE_OC_WITH_DECONFIG_RULES['device_config']['config_rules'].extend(DEVICE_OC_DECONFIG_RULES)
    device_client.ConfigureDevice(Device(**DEVICE_OC_WITH_DECONFIG_RULES))

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_OC_ID))
    config_rules = [
        (ConfigActionEnum.Name(config_rule.action), config_rule.custom.resource_key, config_rule.custom.resource_value)
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(['{:s} {:s} = {:s}'.format(*config_rule) for config_rule in config_rules])))
    for config_rule in DEVICE_OC_DECONFIG_RULES:
        assert 'custom' in config_rule
        action_set = ConfigActionEnum.Name(ConfigActionEnum.CONFIGACTION_SET)
        config_rule = (action_set, config_rule['custom']['resource_key'], config_rule['custom']['resource_value'])
        assert config_rule not in config_rules


def test_device_openconfig_delete(
    context_client : ContextClient,     # pylint: disable=redefined-outer-name
    device_client : DeviceClient,       # pylint: disable=redefined-outer-name
    device_service : DeviceService):    # pylint: disable=redefined-outer-name

    if not ENABLE_OPENCONFIG: pytest.skip('Skipping test: No OpenConfig device has been configured')

    device_client.DeleteDevice(DeviceId(**DEVICE_OC_ID))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_OC_UUID, {})
    assert driver is None
