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
Internal P4 driver tests.
"""

import pytest
from common.type_checkers.Checkers import chk_address_mac, \
    chk_address_ipv4, chk_address_ipv6
from device.service.drivers.p4.p4_driver import P4Driver
from device.service.drivers.p4.p4_common import (
    encode_mac, decode_mac, encode,
    encode_ipv4, decode_ipv4,
    encode_ipv6, decode_ipv6,
    encode_num, decode_num
)
from .device_p4 import(
        DEVICE_P4_IP_ADDR, DEVICE_P4_PORT, DEVICE_P4_DPID, DEVICE_P4_NAME,
        DEVICE_P4_VENDOR, DEVICE_P4_HW_VER, DEVICE_P4_SW_VER,
        DEVICE_P4_WORKERS, DEVICE_P4_GRACE_PERIOD,
        DEVICE_P4_CONFIG_TABLE_ENTRY, DEVICE_P4_DECONFIG_TABLE_ENTRY)
from .mock_p4runtime_service import MockP4RuntimeService


@pytest.fixture(scope='session')
def p4runtime_service():
    """
    Spawn a mock P4Runtime server.

    :return: void
    """
    _service = MockP4RuntimeService(
        address=DEVICE_P4_IP_ADDR, port=DEVICE_P4_PORT,
        max_workers=DEVICE_P4_WORKERS,
        grace_period=DEVICE_P4_GRACE_PERIOD)
    _service.start()
    yield _service
    _service.stop()


@pytest.fixture(scope='session')
def device_driverapi_p4():
    """
    Invoke an instance of the P4 driver.

    :return: void
    """
    _driver = P4Driver(
        address=DEVICE_P4_IP_ADDR,
        port=DEVICE_P4_PORT,
        id=DEVICE_P4_DPID,
        name=DEVICE_P4_NAME,
        vendor=DEVICE_P4_VENDOR,
        hw_ver=DEVICE_P4_HW_VER,
        sw_ver=DEVICE_P4_SW_VER)
    _driver.Connect()
    yield _driver
    _driver.Disconnect()


def test_device_driverapi_p4_setconfig(
        p4runtime_service: MockP4RuntimeService,
        device_driverapi_p4: P4Driver):
    """
    Test the SetConfig RPC of the P4 driver API.

    :param p4runtime_service: Mock P4Runtime service
    :param device_driverapi_p4: instance of the P4 device driver
    :return: void
    """
    result = device_driverapi_p4.SetConfig(
        DEVICE_P4_CONFIG_TABLE_ENTRY
    )
    assert list(result)


def test_device_driverapi_p4_getconfig(
        p4runtime_service: MockP4RuntimeService,
        device_driverapi_p4: P4Driver):
    """
    Test the GetConfig RPC of the P4 driver API.

    :param p4runtime_service: Mock P4Runtime service
    :param device_driverapi_p4: instance of the P4 device driver
    :return: void
    """
    pytest.skip('Skipping test: GetConfig')


def test_device_driverapi_p4_getresource(
        p4runtime_service: MockP4RuntimeService,
        device_driverapi_p4: P4Driver):
    """
    Test the GetResource RPC of the P4 driver API.

    :param p4runtime_service: Mock P4Runtime service
    :param device_driverapi_p4: instance of the P4 device driver
    :return: void
    """
    pytest.skip('Skipping test: GetResource')


def test_device_driverapi_p4_deleteconfig(
        p4runtime_service: MockP4RuntimeService,
        device_driverapi_p4: P4Driver):
    """
    Test the DeleteConfig RPC of the P4 driver API.

    :param p4runtime_service: Mock P4Runtime service
    :param device_driverapi_p4: instance of the P4 device driver
    :return: void
    """
    result = device_driverapi_p4.DeleteConfig(
        DEVICE_P4_DECONFIG_TABLE_ENTRY
    )
    assert list(result)


def test_device_driverapi_p4_subscribe_state(
        p4runtime_service: MockP4RuntimeService,
        device_driverapi_p4: P4Driver):
    """
    Test the SubscribeState RPC of the P4 driver API.

    :param p4runtime_service: Mock P4Runtime service
    :param device_driverapi_p4: instance of the P4 device driver
    :return: void
    """
    pytest.skip('Skipping test: SubscribeState')


def test_device_driverapi_p4_getstate(
        p4runtime_service: MockP4RuntimeService,
        device_driverapi_p4: P4Driver):
    """
    Test the GetState RPC of the P4 driver API.

    :param p4runtime_service: Mock P4Runtime service
    :param device_driverapi_p4: instance of the P4 device driver
    :return: void
    """
    pytest.skip('Skipping test: GetState')


def test_device_driverapi_p4_unsubscribe_state(
        p4runtime_service: MockP4RuntimeService,
        device_driverapi_p4: P4Driver):
    """
    Test the UnsubscribeState RPC of the P4 driver API.

    :param p4runtime_service: Mock P4Runtime service
    :param device_driverapi_p4: instance of the P4 device driver
    :return: void
    """
    pytest.skip('Skipping test: UnsubscribeState')


def test_p4_common_mac():
    """
    Test MAC converters.

    :return: void
    """
    wrong_mac = "aa:bb:cc:dd:ee"
    assert not chk_address_mac(wrong_mac)

    mac = "aa:bb:cc:dd:ee:fe"
    assert chk_address_mac(mac)
    enc_mac = encode_mac(mac)
    assert enc_mac == b'\xaa\xbb\xcc\xdd\xee\xfe',\
        "String-based MAC address to bytes failed"
    enc_mac = encode(mac, 6*8)
    assert enc_mac == b'\xaa\xbb\xcc\xdd\xee\xfe',\
        "String-based MAC address to bytes failed"
    dec_mac = decode_mac(enc_mac)
    assert mac == dec_mac,\
        "MAC address bytes to string failed"


def test_p4_common_ipv4():
    """
    Test IPv4 converters.

    :return: void
    """
    assert not chk_address_ipv4("10.0.0.1.5")
    assert not chk_address_ipv4("256.0.0.1")
    assert not chk_address_ipv4("256.0.1")
    assert not chk_address_ipv4("10001")

    ipv4 = "10.0.0.1"
    assert chk_address_ipv4(ipv4)
    enc_ipv4 = encode_ipv4(ipv4)
    assert enc_ipv4 == b'\x0a\x00\x00\x01',\
        "String-based IPv4 address to bytes failed"
    dec_ipv4 = decode_ipv4(enc_ipv4)
    assert ipv4 == dec_ipv4,\
        "IPv4 address bytes to string failed"


def test_p4_common_ipv6():
    """
    Test IPv6 converters.

    :return: void
    """
    assert not chk_address_ipv6('10.0.0.1')
    assert chk_address_ipv6('2001:0000:85a3::8a2e:370:1111')

    ipv6 = "1:2:3:4:5:6:7:8"
    assert chk_address_ipv6(ipv6)
    enc_ipv6 = encode_ipv6(ipv6)
    assert enc_ipv6 == \
           b'\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06\x00\x07\x00\x08',\
           "String-based IPv6 address to bytes failed"
    dec_ipv6 = decode_ipv6(enc_ipv6)
    assert ipv6 == dec_ipv6,\
        "IPv6 address bytes to string failed"


def test_p4_common_numbers():
    """
    Test numerical converters.

    :return: void
    """
    num = 1337
    byte_len = 5
    enc_num = encode_num(num, byte_len * 8)
    assert enc_num == b'\x00\x00\x00\x05\x39',\
        "Number to bytes conversion failed"
    dec_num = decode_num(enc_num)
    assert num == dec_num,\
        "Bytes to number conversion failed"
    assert encode((num,), byte_len * 8) == enc_num
    assert encode([num], byte_len * 8) == enc_num

    num = 256
    try:
        encode_num(num, 8)
    except OverflowError:
        pass
