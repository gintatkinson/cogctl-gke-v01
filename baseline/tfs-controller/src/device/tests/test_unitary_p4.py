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

"""
P4 unit tests.
"""

import copy
import logging
import operator
import grpc
import pytest
from common.proto.context_pb2 import ConfigActionEnum, Device, DeviceId,\
    DeviceOperationalStatusEnum
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from device.service.DeviceService import DeviceService
from device.service.driver_api._Driver import _Driver
from .PrepareTestScenario import (  # pylint: disable=unused-import
    # be careful, order of symbols is important here!
    mock_service, device_service, context_client, device_client,
    monitoring_client, test_prepare_environment)

from .mock_p4runtime_service import MockP4RuntimeService
try:
    from .device_p4 import(
        DEVICE_P4, DEVICE_P4_ID, DEVICE_P4_UUID,
        DEVICE_P4_IP_ADDR, DEVICE_P4_PORT, DEVICE_P4_WORKERS,
        DEVICE_P4_GRACE_PERIOD, DEVICE_P4_CONNECT_RULES,
        DEVICE_P4_CONFIG_TABLE_ENTRY, DEVICE_P4_DECONFIG_TABLE_ENTRY)
    ENABLE_P4 = True
except ImportError:
    ENABLE_P4 = False

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


@pytest.fixture(scope='session')
def p4runtime_service():
    """
    Spawn a mock P4Runtime server.

    :return: void
    """
    _service = MockP4RuntimeService(
        address=DEVICE_P4_IP_ADDR,
        port=DEVICE_P4_PORT,
        max_workers=DEVICE_P4_WORKERS,
        grace_period=DEVICE_P4_GRACE_PERIOD)
    _service.start()
    yield _service
    _service.stop()


# ----- Test Device Driver P4 --------------------------------------------------
def test_device_p4_add_error_cases(
        context_client: ContextClient,   # pylint: disable=redefined-outer-name
        device_client: DeviceClient,     # pylint: disable=redefined-outer-name
        device_service: DeviceService):  # pylint: disable=redefined-outer-name
    """
    Test AddDevice RPC with wrong inputs.

    :param context_client: context component client
    :param device_client: device component client
    :param device_service: device component service
    :return:
    """

    if not ENABLE_P4:
        pytest.skip('Skipping test: No P4 device has been configured')

    with pytest.raises(grpc.RpcError) as ex:
        device_p4_with_extra_rules = copy.deepcopy(DEVICE_P4)
        device_p4_with_extra_rules['device_config']['config_rules'].extend(
            DEVICE_P4_CONNECT_RULES)
        device_p4_with_extra_rules['device_config']['config_rules'].extend(
            DEVICE_P4_CONFIG_TABLE_ENTRY)
        device_client.AddDevice(Device(**device_p4_with_extra_rules))
    assert ex.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    msg_head = 'device.device_config.config_rules(['
    msg_tail = ']) is invalid; RPC method AddDevice only accepts connection '\
               'Config Rules that should start with "_connect/" tag. '\
               'Others should be configured after adding the device.'
    except_msg = str(ex.value.details())
    assert except_msg.startswith(msg_head) and except_msg.endswith(msg_tail)


def test_device_p4_add_correct(
        context_client: ContextClient,              # pylint: disable=redefined-outer-name
        device_client: DeviceClient,                # pylint: disable=redefined-outer-name
        device_service: DeviceService,              # pylint: disable=redefined-outer-name
        p4runtime_service: MockP4RuntimeService):   # pylint: disable=redefined-outer-name
    """
    Test AddDevice RPC with correct inputs.

    :param context_client: context component client
    :param device_client: device component client
    :param device_service: device component service
    :param p4runtime_service: Mock P4Runtime service
    :return:
    """

    if not ENABLE_P4:
        pytest.skip('Skipping test: No P4 device has been configured')

    device_p4_with_connect_rules = copy.deepcopy(DEVICE_P4)
    device_p4_with_connect_rules['device_config']['config_rules'].extend(
        DEVICE_P4_CONNECT_RULES)
    device_client.AddDevice(Device(**device_p4_with_connect_rules))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver: _Driver = driver_instance_cache.get(DEVICE_P4_UUID)
    assert driver is not None

    device_data = context_client.GetDevice(DeviceId(**DEVICE_P4_ID))
    config_rules = [
        (
            ConfigActionEnum.Name(config_rule.action),
            config_rule.custom.resource_key,
            config_rule.custom.resource_value
        )
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(['{:s} {:s} = {:s}'.format(*config_rule)
                   for config_rule in config_rules])))


def test_device_p4_get(
        context_client: ContextClient,              # pylint: disable=redefined-outer-name
        device_client: DeviceClient,                # pylint: disable=redefined-outer-name
        device_service: DeviceService,              # pylint: disable=redefined-outer-name
        p4runtime_service: MockP4RuntimeService):   # pylint: disable=redefined-outer-name
    """
    Test GetDevice RPC.

    :param context_client: context component client
    :param device_client: device component client
    :param device_service: device component service
    :param p4runtime_service: Mock P4Runtime service
    :return:
    """

    if not ENABLE_P4:
        pytest.skip('Skipping test: No P4 device has been configured')

    initial_config = device_client.GetInitialConfig(DeviceId(**DEVICE_P4_ID))
    assert len(initial_config.config_rules) == 0
    LOGGER.info('initial_config = %s',
                grpc_message_to_json_string(initial_config))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_P4_ID))
    LOGGER.info('device_data = %s', grpc_message_to_json_string(device_data))


def test_device_p4_configure(
        context_client: ContextClient,              # pylint: disable=redefined-outer-name
        device_client: DeviceClient,                # pylint: disable=redefined-outer-name
        device_service: DeviceService,              # pylint: disable=redefined-outer-name
        p4runtime_service: MockP4RuntimeService):   # pylint: disable=redefined-outer-name
    """
    Test ConfigureDevice RPC.

    :param context_client: context component client
    :param device_client: device component client
    :param device_service: device component service
    :param p4runtime_service: Mock P4Runtime service
    :return:
    """

    if not ENABLE_P4:
        pytest.skip('Skipping test: No P4 device has been configured')

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver: _Driver = driver_instance_cache.get(DEVICE_P4_UUID)
    assert driver is not None

    # No entries should exist at this point in time
    driver_config = sorted(driver.GetConfig(), key=operator.itemgetter(0))
    assert len(driver_config) == len(driver.get_manager().get_resource_keys())
    assert driver.get_manager().count_active_entries() == 0

    # Flip the operational status and check it is correctly flipped in Context
    device_p4_with_operational_status = copy.deepcopy(DEVICE_P4)
    device_p4_with_operational_status['device_operational_status'] = \
        DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED
    device_client.ConfigureDevice(Device(**device_p4_with_operational_status))
    device_data = context_client.GetDevice(DeviceId(**DEVICE_P4_ID))
    assert device_data.device_operational_status == \
           DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_ENABLED

    # Insert a new table entry
    device_p4_with_config_rules = copy.deepcopy(DEVICE_P4)
    device_p4_with_config_rules['device_config']['config_rules'].extend(
        DEVICE_P4_CONFIG_TABLE_ENTRY)
    device_client.ConfigureDevice(Device(**device_p4_with_config_rules))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_P4_ID))
    config_rules = [
        (ConfigActionEnum.Name(config_rule.action),
         config_rule.custom.resource_key,
         config_rule.custom.resource_value)
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(
            ['{:s} {:s} = {:s}'.format(*config_rule)
             for config_rule in config_rules]))
    )
    for config_rule in DEVICE_P4_CONFIG_TABLE_ENTRY:
        assert 'custom' in config_rule


def test_device_p4_deconfigure(
        context_client: ContextClient,              # pylint: disable=redefined-outer-name
        device_client: DeviceClient,                # pylint: disable=redefined-outer-name
        device_service: DeviceService,              # pylint: disable=redefined-outer-name
        p4runtime_service: MockP4RuntimeService):   # pylint: disable=redefined-outer-name
    """
    Test DeconfigureDevice RPC.

    :param context_client: context component client
    :param device_client: device component client
    :param device_service: device component service
    :param p4runtime_service: Mock P4Runtime service
    :return:
    """

    if not ENABLE_P4:
        pytest.skip('Skipping test: No P4 device has been configured')

    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver: _Driver = driver_instance_cache.get(DEVICE_P4_UUID)
    assert driver is not None

    # Delete a table entry
    device_p4_with_config_rules = copy.deepcopy(DEVICE_P4)
    device_p4_with_config_rules['device_config']['config_rules'].extend(
        DEVICE_P4_DECONFIG_TABLE_ENTRY)
    device_client.ConfigureDevice(Device(**device_p4_with_config_rules))

    device_data = context_client.GetDevice(DeviceId(**DEVICE_P4_ID))
    config_rules = [
        (ConfigActionEnum.Name(config_rule.action),
         config_rule.custom.resource_key,
         config_rule.custom.resource_value)
        for config_rule in device_data.device_config.config_rules
        if config_rule.WhichOneof('config_rule') == 'custom'
    ]
    LOGGER.info('device_data.device_config.config_rules = \n{:s}'.format(
        '\n'.join(
            ['{:s} {:s} = {:s}'.format(*config_rule)
             for config_rule in config_rules]))
    )
    for config_rule in DEVICE_P4_CONFIG_TABLE_ENTRY:
        assert 'custom' in config_rule

    # Flip the operational status and check it is correctly flipped in Context
    device_p4_with_operational_status = copy.deepcopy(DEVICE_P4)
    device_p4_with_operational_status['device_operational_status'] = \
        DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED
    device_client.ConfigureDevice(Device(**device_p4_with_operational_status))
    device_data = context_client.GetDevice(DeviceId(**DEVICE_P4_ID))
    assert device_data.device_operational_status == \
           DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_DISABLED


def test_device_p4_delete(
        context_client: ContextClient,              # pylint: disable=redefined-outer-name
        device_client: DeviceClient,                # pylint: disable=redefined-outer-name
        device_service: DeviceService,              # pylint: disable=redefined-outer-name
        p4runtime_service: MockP4RuntimeService):   # pylint: disable=redefined-outer-name
    """
    Test DeleteDevice RPC.

    :param context_client: context component client
    :param device_client: device component client
    :param device_service: device component service
    :param p4runtime_service: Mock P4Runtime service
    :return:
    """

    if not ENABLE_P4:
        pytest.skip('Skipping test: No P4 device has been configured')

    device_client.DeleteDevice(DeviceId(**DEVICE_P4_ID))
    driver_instance_cache = device_service.device_servicer.driver_instance_cache
    driver: _Driver = driver_instance_cache.get(DEVICE_P4_UUID)
    assert driver is None
