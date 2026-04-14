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

import copy, grpc, logging, pytest
from common.proto.context_pb2 import ConfigActionEnum, Device, DeviceId
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from device.service.DeviceService import DeviceService
from device.service.driver_api._Driver import _Driver
from .PrepareTestScenario import ( # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    mock_service, device_service, context_client, device_client, monitoring_client, test_prepare_environment)

try:
    from .Device_Transport_Api_CTTC import (
        DEVICE_TAPI, DEVICE_TAPI_CONNECT_RULES, DEVICE_TAPI_UUID, DEVICE_TAPI_ID, DEVICE_TAPI_CONFIG_RULES,
        DEVICE_TAPI_DECONFIG_RULES)
    ENABLE_TAPI = True
except ImportError:
    ENABLE_TAPI = False

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


# ----- Test Device Driver TAPI ------------------------------------------------

def test_device_tapi_add_error_cases(
    device_client : DeviceClient):      # pylint: disable=redefined-outer-name

    if not ENABLE_TAPI: pytest.skip('Skipping test: No TAPI device has been configured')

    with pytest.raises(grpc.RpcError) as e:
        DEVICE_TAPI_WITH_EXTRA_RULES = copy.deepcopy(DEVICE_TAPI)
        DEVICE_TAPI_WITH_EXTRA_RULES['device_config']['config_rules'].extend(DEVICE_TAPI_CONNECT_RULES)
        DEVICE_TAPI_WITH_EXTRA_RULES['device_config']['config_rules'].extend(DEVICE_TAPI_CONFIG_RULES)
        device_client.AddDevice(Device(**DEVICE_TAPI_WITH_EXTRA_RULES))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    msg_head = 'device.device_config.config_rules(['
    msg_tail = ']) is invalid; RPC method AddDevice only accepts connection Config Rules that should start '\
               'with "_connect/" tag. Others should be configured after adding the device.'
    except_msg = str(e.value.details())
    assert except_msg.startswith(msg_head) and except_msg.endswith(msg_tail)


def test_device_tapi_add_correct(
    device_client: DeviceClient,        # pylint: disable=redefined-outer-name
    device_service: DeviceService):     # pylint: disable=redefined-outer-name

    if not ENABLE_TAPI: pytest.skip('Skipping test: No TAPI device has been configured')

    DEVICE_TAPI_WITH_CONNECT_RULES = copy.deepcopy(DEVICE_TAPI)
    DEVICE_TAPI_WITH_CONNECT_RULES['device_config']['config_rules'].extend(DEVICE_TAPI_CONNECT_RULES)
    device_client.AddDevice(Device(**DEVICE_TAPI_WITH_CONNECT_RULES))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver: _Driver = driver_instance_cache.get(DEVICE_TAPI_UUID)
    assert driver is not None


def test_device_tapi_get(
    context_client: ContextClient,      # pylint: disable=redefined-outer-name
    device_client: DeviceClient):       # pylint: disable=redefined-outer-name

    if not ENABLE_TAPI: pytest.skip('Skipping test: No TAPI device has been configured')

    initial_config = device_client.GetInitialConfig(DeviceId(**DEVICE_TAPI_ID))
    LOGGER.info('initial_config = {:s}'.format(grpc_message_to_json_string(initial_config)))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_TAPI_ID))
    LOGGER.info('device_data = {:s}'.format(grpc_message_to_json_string(device_data)))


def test_device_tapi_configure(
    context_client: ContextClient,      # pylint: disable=redefined-outer-name
    device_client: DeviceClient,        # pylint: disable=redefined-outer-name
    device_service: DeviceService):     # pylint: disable=redefined-outer-name

    if not ENABLE_TAPI: pytest.skip('Skipping test: No TAPI device has been configured')

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_TAPI_UUID)
    assert driver is not None

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    DEVICE_TAPI_WITH_CONFIG_RULES = copy.deepcopy(DEVICE_TAPI)
    DEVICE_TAPI_WITH_CONFIG_RULES['device_config']['config_rules'].extend(DEVICE_TAPI_CONFIG_RULES)
    device_client.ConfigureDevice(Device(**DEVICE_TAPI_WITH_CONFIG_RULES))

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_TAPI_ID))
    config_rules = [
        (ConfigActionEnum.Name(config_rule.action), config_rule.custom.resource_key, config_rule.custom.resource_value)
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(['{:s} {:s} = {:s}'.format(*config_rule) for config_rule in config_rules])))
    for config_rule in DEVICE_TAPI_CONFIG_RULES:
        assert 'custom' in config_rule
        config_rule = (
            ConfigActionEnum.Name(config_rule['action']), config_rule['custom']['resource_key'],
            config_rule['custom']['resource_value'])
        assert config_rule in config_rules


def test_device_tapi_deconfigure(
    context_client: ContextClient,      # pylint: disable=redefined-outer-name
    device_client: DeviceClient,        # pylint: disable=redefined-outer-name
    device_service: DeviceService):     # pylint: disable=redefined-outer-name

    if not ENABLE_TAPI: pytest.skip('Skipping test: No TAPI device has been configured')

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver: _Driver = driver_instance_cache.get(DEVICE_TAPI_UUID)
    assert driver is not None

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    DEVICE_TAPI_WITH_DECONFIG_RULES = copy.deepcopy(DEVICE_TAPI)
    DEVICE_TAPI_WITH_DECONFIG_RULES['device_config']['config_rules'].extend(DEVICE_TAPI_DECONFIG_RULES)
    device_client.ConfigureDevice(Device(**DEVICE_TAPI_WITH_DECONFIG_RULES))

    # Requires to retrieve data from device; might be slow. Uncomment only when needed and test does not pass directly.
    #driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    #LOGGER.info('driver_config = {:s}'.format(str(driver_config)))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_TAPI_ID))
    config_rules = [
        (ConfigActionEnum.Name(config_rule.action), config_rule.custom.resource_key, config_rule.custom.resource_value)
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(['{:s} {:s} = {:s}'.format(*config_rule) for config_rule in config_rules])))
    for config_rule in DEVICE_TAPI_DECONFIG_RULES:
        assert 'custom' in config_rule
        action_set = ConfigActionEnum.Name(ConfigActionEnum.CONFIGACTION_SET)
        config_rule = (action_set, config_rule['custom']['resource_key'], config_rule['custom']['resource_value'])
        assert config_rule not in config_rules


def test_device_tapi_delete(
    device_client : DeviceClient,       # pylint: disable=redefined-outer-name
    device_service : DeviceService):    # pylint: disable=redefined-outer-name

    if not ENABLE_TAPI: pytest.skip('Skipping test: No TAPI device has been configured')

    device_client.DeleteDevice(DeviceId(**DEVICE_TAPI_ID))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver : _Driver = driver_instance_cache.get(DEVICE_TAPI_UUID, {})
    assert driver is None
