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
This package contains several helper functions for encoding to and decoding from
byte strings:
- integers
- IPv4 address strings
- IPv6 address strings
- Ethernet address strings
as well as static variables used by various P4 driver components.
"""

import logging
import ipaddress
import macaddress
import math
import socket
from typing import Any, Dict, List, Optional, Tuple

from common.type_checkers.Checkers import \
    chk_attribute, chk_string, chk_type, chk_issubclass,\
    chk_address_mac, chk_address_ipv4, chk_address_ipv6
try:
    from .p4_exception import UserBadValueError
except ImportError:
    from p4_exception import UserBadValueError

P4_ATTR_DEV_ID = "id"
P4_ATTR_DEV_NAME = "name"
P4_ATTR_DEV_ENDPOINTS = "endpoints"
P4_ATTR_DEV_VENDOR = "vendor"
P4_ATTR_DEV_HW_VER = "hw_ver"
P4_ATTR_DEV_SW_VER = "sw_ver"
P4_ATTR_DEV_P4BIN = "p4bin"
P4_ATTR_DEV_P4INFO = "p4info"
P4_ATTR_DEV_TIMEOUT = "timeout"

P4_VAL_DEF_VENDOR = "Unknown"
P4_VAL_DEF_HW_VER = "BMv2 simple_switch"
P4_VAL_DEF_SW_VER = "Stratum"
P4_VAL_DEF_TIMEOUT = 60

RESOURCE_ENDPOINTS_ROOT_PATH = "/endpoints"

# Logger instance
LOGGER = logging.getLogger(__name__)


# MAC address encoding/decoding


def encode_mac(mac_addr_string):
    """
    Convert string-based MAC address into bytes.

    :param mac_addr_string: string-based MAC address
    :return: MAC address in bytes
    """
    return bytes(macaddress.MAC(mac_addr_string))


def decode_mac(encoded_mac_addr):
    """
    Convert a MAC address in bytes into string-based MAC address.

    :param encoded_mac_addr: MAC address in bytes
    :return: string-based MAC address
    """
    return str(macaddress.MAC(encoded_mac_addr)).replace("-", ":").lower()


# IP address encoding/decoding


def encode_ipv4(ip_addr_string):
    """
    Convert string-based IPv4 address into bytes.

    :param ip_addr_string: string-based IPv4 address
    :return: IPv4 address in bytes
    """
    return socket.inet_aton(ip_addr_string)


def decode_ipv4(encoded_ip_addr):
    """
    Convert an IPv4 address in bytes into string-based IPv4 address.

    :param encoded_ip_addr: IPv4 address in bytes
    :return: string-based IPv4 address
    """
    return socket.inet_ntoa(encoded_ip_addr)


def encode_ipv6(ip_addr_string):
    """
    Convert string-based IPv6 address into bytes.

    :param ip_addr_string: string-based IPv6 address
    :return: IPv6 address in bytes
    """
    return socket.inet_pton(socket.AF_INET6, ip_addr_string)


def decode_ipv6(encoded_ip_addr):
    """
    Convert an IPv6 address in bytes into string-based IPv6 address.

    :param encoded_ip_addr: IPv6 address in bytes
    :return: string-based IPv6 address
    """
    return str(ipaddress.ip_address(encoded_ip_addr))


# Numerical encoding/decoding


def bitwidth_to_bytes(bitwidth):
    """
    Convert number of bits to number of bytes.

    :param bitwidth: number of bits
    :return: number of bytes
    """
    return int(math.ceil(bitwidth / 8.0))


def encode_num(number, bitwidth):
    """
    Convert number into bytes.

    :param number: number to convert
    :param bitwidth: number of bits
    :return: number in bytes
    """
    byte_len = bitwidth_to_bytes(bitwidth)
    return number.to_bytes(byte_len, byteorder="big")


def decode_num(encoded_number):
    """
    Convert number in bytes into its numerical form.

    :param encoded_number: number in bytes to convert
    :return: numerical number form
    """
    return int.from_bytes(encoded_number, "big")


# Umbrella encoder


def encode(variable, bitwidth):
    """
    Tries to infer the type of `input` and encode it.

    :param variable: target variable
    :param bitwidth: size of variable in bits
    :return: encoded bytes
    """
    byte_len = bitwidth_to_bytes(bitwidth)
    if isinstance(variable, (list, tuple)) and len(variable) == 1:
        variable = variable[0]

    if isinstance(variable, int):
        encoded_bytes = encode_num(variable, bitwidth)
    elif isinstance(variable, str):
        if chk_address_mac(variable):
            encoded_bytes = encode_mac(variable)
        elif chk_address_ipv4(variable):
            encoded_bytes = encode_ipv4(variable)
        elif chk_address_ipv6(variable):
            encoded_bytes = encode_ipv6(variable)
        else:
            try:
                value = int(variable, 0)
            except ValueError as ex:
                raise UserBadValueError(
                    f"Invalid value '{variable}': "
                    "could not cast to integer, try in hex with 0x prefix")\
                    from ex
            encoded_bytes = value.to_bytes(byte_len, byteorder="big")
    else:
        raise Exception(
            f"Encoding objects of {type(variable)} is not supported")
    assert len(encoded_bytes) == byte_len
    return encoded_bytes


# Parsers


def get_match_field_value(match_field):
    """
    Retrieve the value of a certain match field by name.

    :param match_field: match field
    :return: match filed value
    """
    match_type = match_field.WhichOneof("field_match_type")
    if match_type == "valid":
        return match_field.valid.value
    if match_type == "exact":
        return match_field.exact.value
    if match_type == "lpm":
        return match_field.lpm.value, match_field.lpm.prefix_len
    if match_type == "ternary":
        return match_field.ternary.value, match_field.ternary.mask
    if match_type == "range":
        return match_field.range.low, match_field.range.high
    raise Exception(f"Unsupported match type with type {match_type}")


def parse_resource_string_from_json(resource, resource_str="table-name"):
    """
    Parse a given resource name within a JSON-based object.

    :param resource: JSON-based object
    :param resource_str: resource string to parse
    :return: value of the parsed resource string
    """
    if not resource or (resource_str not in resource):
        LOGGER.warning("JSON entry misses '%s' attribute", resource_str)
        return None
    chk_type(resource_str, resource[resource_str], str)
    return resource[resource_str]


def parse_resource_number_from_json(resource, resource_nb):
    """
    Parse a given resource number within a JSON-based object.

    :param resource: JSON-based object
    :param resource_nb: resource number to parse
    :return: value of the parsed resource number
    """
    if not resource or (resource_nb not in resource):
        LOGGER.warning(
            "JSON entry misses '%s' attribute", resource_nb)
        return None
    chk_type(resource_nb, resource[resource_nb], int)
    return resource[resource_nb]


def parse_resource_integer_from_json(resource, resource_nb):
    """
    Parse a given integer number within a JSON-based object.

    :param resource: JSON-based object
    :param resource_nb: resource number to parse
    :return: value of the parsed resource number
    """
    num = parse_resource_number_from_json(resource, resource_nb)
    if num:
        return int(num)
    return -1


def parse_resource_float_from_json(resource, resource_nb):
    """
    Parse a given floating point number within a JSON-based object.

    :param resource: JSON-based object
    :param resource_nb: resource number to parse
    :return: value of the parsed resource number
    """
    num = parse_resource_number_from_json(resource, resource_nb)
    if num:
        return float(num)
    return -1.0


def parse_resource_bytes_from_json(resource, resource_bytes):
    """
    Parse given resource bytes within a JSON-based object.

    :param resource: JSON-based object
    :param resource_bytes: resource bytes to parse
    :return: value of the parsed resource bytes
    """
    if not resource or (resource_bytes not in resource):
        LOGGER.debug(
            "JSON entry misses '%s' attribute", resource_bytes)
        return None

    if resource_bytes in resource:
        chk_type(resource_bytes, resource[resource_bytes], bytes)
        return resource[resource_bytes]
    return None


def parse_match_operations_from_json(resource):
    """
    Parse the match operations within a JSON-based object.

    :param resource: JSON-based object
    :return: map of match operations
    """
    if not resource or ("match-fields" not in resource):
        LOGGER.warning(
            "JSON entry misses 'match-fields' list of attributes")
        return {}
    chk_type("match-fields", resource["match-fields"], list)

    match_map = {}
    for mf_entry in resource["match-fields"]:
        if ("match-field" not in mf_entry) or \
                ("match-value" not in mf_entry):
            LOGGER.warning(
                "JSON entry misses 'match-field' and/or "
                "'match-value' attributes")
            return None
        chk_type("match-field", mf_entry["match-field"], str)
        chk_type("match-value", mf_entry["match-value"], str)
        match_map[mf_entry["match-field"]] = mf_entry["match-value"]

    return match_map


def parse_action_parameters_from_json(resource):
    """
    Parse the action parameters within a JSON-based object.

    :param resource: JSON-based object
    :return: map of action parameters
    """
    if not resource or ("action-params" not in resource):
        LOGGER.warning(
            "JSON entry misses 'action-params' list of attributes")
        return None
    chk_type("action-params", resource["action-params"], list)

    action_name = parse_resource_string_from_json(resource, "action-name")

    action_params = {}
    for ac_entry in resource["action-params"]:
        if not ac_entry:
            LOGGER.debug(
                "Missing action parameter for action %s", action_name)
            continue
        chk_type("action-param", ac_entry["action-param"], str)
        chk_type("action-value", ac_entry["action-value"], str)
        action_params[ac_entry["action-param"]] = \
            ac_entry["action-value"]

    return action_params


def parse_replicas_from_json(resource):
    """
    Parse the session replicas within a JSON-based object.

    :param resource: JSON-based object
    :return: map of replicas
    """
    if not resource or ("replicas" not in resource):
        LOGGER.warning(
            "JSON entry misses 'replicas' list of attributes")
        return None
    chk_type("replicas", resource["replicas"], list)

    replicas = {}
    for rep in resource["replicas"]:
        chk_type("egress-port", rep["egress-port"], int)
        chk_type("instance", rep["instance"], int)
        replicas[rep["egress-port"]] = rep["instance"]

    return replicas


def parse_integer_list_from_json(resource, resource_list, resource_item):
    """
    Parse the list of integers within a JSON-based object.

    :param resource: JSON-based object
    :param resource_list: name of the resource list
    :param resource_item: name of the resource item
    :return: list of integers
    """
    if not resource or (resource_list not in resource):
        LOGGER.warning(
            "JSON entry misses '%s' list of attributes", resource_list)
        return []
    chk_type(resource_list, resource[resource_list], list)

    integers_list = []
    for item in resource[resource_list]:
        chk_type(resource_item, item[resource_item], int)
        integers_list.append(item[resource_item])

    return integers_list

def process_optional_string_field(
    #TODO: Consider adding this in common methods as it is taken by the Emulated driver
    endpoint_data : Dict[str, Any], field_name : str, endpoint_resource_value : Dict[str, Any]
) -> None:
    field_value = chk_attribute(field_name, endpoint_data, 'endpoint_data', default=None)
    if field_value is None: return
    chk_string('endpoint_data.{:s}'.format(field_name), field_value)
    if len(field_value) > 0: endpoint_resource_value[field_name] = field_value

def compose_resource_endpoints(endpoints_list : List[Tuple[str, Any]]):
    #TODO: Consider adding this in common methods; currently taken by the Emulated driver
    endpoint_resources = []
    for i, endpoint in enumerate(endpoints_list):
        LOGGER.debug("P4 endpoint {}: {}".format(i, endpoint))
        endpoint_resource = compose_resource_endpoint(endpoint)
        if endpoint_resource is None: continue
        endpoint_resources.append(endpoint_resource)
    return endpoint_resources

def compose_resource_endpoint(endpoint_data : Dict[str, Any]) -> Optional[Tuple[str, Dict]]:
    #TODO: Consider adding this in common methods; currently taken by the Emulated driver
    try:
        endpoint_uuid = chk_attribute('uuid', endpoint_data, 'endpoint_data')
        chk_string('endpoint_data.uuid', endpoint_uuid, min_length=1)
        endpoint_resource_path = RESOURCE_ENDPOINTS_ROOT_PATH
        endpoint_resource_key = '{:s}/endpoint[{:s}]'.format(endpoint_resource_path, endpoint_uuid)
        endpoint_resource_value = {'uuid': endpoint_uuid}

        # Check endpoint's optional string fields
        process_optional_string_field(endpoint_data, 'name', endpoint_resource_value)
        process_optional_string_field(endpoint_data, 'type', endpoint_resource_value)
        process_optional_string_field(endpoint_data, 'context_uuid', endpoint_resource_value)
        process_optional_string_field(endpoint_data, 'topology_uuid', endpoint_resource_value)

        return endpoint_resource_key, endpoint_resource_value
    except: # pylint: disable=bare-except
        LOGGER.error('Problem composing endpoint({:s})'.format(str(endpoint_data)))
        return None

def compose_resource_rules(rules_list : List[Tuple[str, Any]]):
    rule_resources = []
    for i, rule in enumerate(rules_list):
        rule_resource = compose_resource_rule(rule_data=rule, rule_cnt=i)
        if rule_resource is None: continue
        rule_resources.append(rule_resource)
    return rule_resources

def compose_resource_rule(rule_data : Dict[str, Any], rule_cnt : int) -> Optional[Tuple[str, Dict]]:
    try:
        LOGGER.info("Rule: {}".format(rule_data))

        rule_resource_key = chk_attribute('resource_key', rule_data, 'rule_data')
        chk_string('rule_data.resource_key', rule_resource_key, min_length=1)

        rule_resource_value = chk_attribute('resource_value', rule_data, 'rule_data')
        chk_issubclass('rule_data.resource_value', rule_resource_value, dict)

        rule_key_unique = ""

        if "table" == rule_resource_key:
            table_name = parse_resource_string_from_json(rule_resource_value, "table-name")
            assert table_name, "Invalid table name in rule"
            rule_key_unique = '/{0}s/{0}/{1}[{2}]'.format(rule_resource_key, table_name, rule_cnt)
        else:
            msg = f"Parsed an invalid key {rule_resource_key}"
            LOGGER.error(msg)
            raise Exception(msg)

        assert rule_key_unique, "Invalid unique resource key"
        return rule_key_unique, rule_resource_value
    except: # pylint: disable=bare-except
        LOGGER.error('Problem composing rule({:s})'.format(str(rule_data)))
        return None
