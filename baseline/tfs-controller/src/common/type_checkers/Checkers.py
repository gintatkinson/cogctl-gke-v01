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

import re
import ipaddress
from ctypes import c_uint16, sizeof
from typing import Any, Container, Dict, List, Optional, Pattern, Set, Sized, Tuple, Union

def chk_none(name : str, value : Any, reason=None) -> Any:
    if value is None: return value
    if reason is None: reason = 'must be None.'
    raise ValueError('{}({}) {}'.format(str(name), str(value), str(reason)))

def chk_not_none(name : str, value : Any, reason=None) -> Any:
    if value is not None: return value
    if reason is None: reason = 'must not be None.'
    raise ValueError('{}({}) {}'.format(str(name), str(value), str(reason)))

def chk_attribute(name : str, container : Dict, container_name : str, **kwargs):
    if name in container: return container[name]
    if 'default' in kwargs: return kwargs['default']
    raise AttributeError('Missing object({:s}) in container({:s})'.format(str(name), str(container_name)))

def chk_type(name : str, value : Any, type_or_types : Union[type, Set[type], Tuple[type]] = set()) -> Any:
    if isinstance(value, type_or_types): return value
    msg = '{}({}) is of a wrong type({}). Accepted type_or_types({}).'
    raise TypeError(msg.format(str(name), str(value), type(value).__name__, str(type_or_types)))

def chk_issubclass(name : str, value : type, class_or_classes : Union[type, Set[type]] = set()) -> Any:
    if issubclass(value, class_or_classes): return value
    msg = '{}({}) is of a wrong class({}). Accepted class_or_classes({}).'
    raise TypeError(msg.format(str(name), str(value), type(value).__name__, str(class_or_classes)))

def chk_length(
    name : str, value : Sized, allow_empty : bool = False,
    min_length : Optional[int] = None, max_length : Optional[int] = None) -> Any:

    length = len(chk_type(name, value, Sized))

    allow_empty = chk_type('allow_empty for {}'.format(name), allow_empty, bool)
    if not allow_empty and length == 0:
        raise ValueError('{}({}) is out of range: allow_empty({}).'.format(str(name), str(value), str(allow_empty)))

    if min_length is not None:
        min_length = chk_type('min_length for {}'.format(name), min_length, int)
        if length < min_length:
            raise ValueError('{}({}) is out of range: min_length({}).'.format(str(name), str(value), str(min_length)))

    if max_length is not None:
        max_length = chk_type('max_length for {}'.format(name), max_length, int)
        if length > max_length:
            raise ValueError('{}({}) is out of range: max_value({}).'.format(str(name), str(value), str(max_length)))

    return value

def chk_boolean(name : str, value : Any) -> bool:
    return chk_type(name, value, bool)

def chk_string(
    name : str, value : Any, allow_empty : bool = False,
    min_length : Optional[int] = None, max_length : Optional[int] = None,
    pattern : Optional[Union[Pattern, str]] = None) -> str:

    chk_type(name, value, str)
    chk_length(name, value, allow_empty=allow_empty, min_length=min_length, max_length=max_length)
    if pattern is None: return value
    pattern = re.compile(pattern)
    if pattern.match(value): return value
    raise ValueError('{}({}) does not match pattern({}).'.format(str(name), str(value), str(pattern)))

def chk_float(
    name : str, value : Any, type_or_types : Union[type, Set[type], List[type], Tuple[type]] = (int, float),
    min_value : Optional[Union[int, float]] = None, max_value : Optional[Union[int, float]] = None) -> float:

    chk_not_none(name, value)
    chk_type(name, value, type_or_types)
    if min_value is not None:
        chk_type(name, value, type_or_types)
        if value < min_value:
            msg = '{}({}) lower than min_value({}).'
            raise ValueError(msg.format(str(name), str(value), str(min_value)))
    if max_value is not None:
        chk_type(name, value, type_or_types)
        if value > max_value:
            msg = '{}({}) greater than max_value({}).'
            raise ValueError(msg.format(str(name), str(value), str(max_value)))
    return float(value)

def chk_integer(
    name : str, value : Any,
    min_value : Optional[Union[int, float]] = None, max_value : Optional[Union[int, float]] = None) -> int:

    return int(chk_float(name, value, type_or_types=int, min_value=min_value, max_value=max_value))

def chk_options(name : str, value : Any, options : Container) -> Any:
    chk_not_none(name, value)
    if value not in options:
        msg = '{}({}) is not one of options({}).'
        raise ValueError(msg.format(str(name), str(value), str(options)))
    return value

# MAC address checker
mac_pattern = re.compile(r"^([\da-fA-F]{2}:){5}([\da-fA-F]{2})$")

def chk_address_mac(mac_addr : str):
    """
    Check whether input string is a valid MAC address or not.

    :param mac_addr: string-based MAC address
    :return: boolean status
    """
    return mac_pattern.match(mac_addr) is not None

# IPv4/IPv6 address checkers
IPV4_LOCALHOST = "localhost"

def chk_address_ipv4(ip_addr : str):
    """
    Check whether input string is a valid IPv4 address or not.

    :param ip_addr: string-based IPv4 address
    :return: boolean status
    """
    if ip_addr == IPV4_LOCALHOST:
        return True
    try:
        addr = ipaddress.ip_address(ip_addr)
        return isinstance(addr, ipaddress.IPv4Address)
    except ValueError:
        return False

def chk_prefix_len_ipv4(ip_prefix_len : int):
    """
    Check whether input integer is a valid IPv4 address prefix length.

    :param ip_prefix_len: IPv4 address prefix length
    :return: boolean status
    """
    return 0 <= ip_prefix_len <= 32

def chk_address_ipv6(ip_addr : str):
    """
    Check whether input string is a valid IPv6 address or not.

    :param ip_addr: string-based IPv6 address
    :return: boolean status
    """
    try:
        addr = ipaddress.ip_address(ip_addr)
        return isinstance(addr, ipaddress.IPv6Address)
    except ValueError:
        return False


# VLAN ID checker
VLAN_ID_MIN = 1
VLAN_ID_MAX = 4094

def chk_vlan_id(vlan_id : int):
    return VLAN_ID_MIN <= vlan_id <= VLAN_ID_MAX


# Transport port checker

def limits(c_int_type):
    """
    Discover limits of numerical type.

    :param c_int_type: numerical type
    :return: tuple of numerical type's limits
    """
    signed = c_int_type(-1).value < c_int_type(0).value
    bit_size = sizeof(c_int_type) * 8
    signed_limit = 2 ** (bit_size - 1)
    return (-signed_limit, signed_limit - 1) \
        if signed else (0, 2 * signed_limit - 1)

def chk_transport_port(trans_port : int):
    """
    Check whether input is a valid transport port number or not.

    :param trans_port: transport port number
    :return: boolean status
    """
    lim = limits(c_uint16)
    return lim[0] <= trans_port <= lim[1]
