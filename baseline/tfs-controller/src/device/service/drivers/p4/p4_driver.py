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
P4 driver plugin for the TeraFlow SDN controller.
"""

import os
import json
import logging
import threading
from typing import Any, Iterator, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.type_checkers.Checkers import chk_type, chk_length, chk_string, \
    chk_address_ipv4, chk_address_ipv6, chk_transport_port
from device.service.driver_api._Driver import RESOURCE_ENDPOINTS, RESOURCE_RULES
from .p4_common import compose_resource_endpoints,\
    P4_ATTR_DEV_ID, P4_ATTR_DEV_NAME, P4_ATTR_DEV_ENDPOINTS,\
    P4_ATTR_DEV_VENDOR, P4_ATTR_DEV_HW_VER, P4_ATTR_DEV_SW_VER,\
    P4_ATTR_DEV_P4BIN, P4_ATTR_DEV_P4INFO, P4_ATTR_DEV_TIMEOUT,\
    P4_VAL_DEF_VENDOR, P4_VAL_DEF_HW_VER, P4_VAL_DEF_SW_VER,\
    P4_VAL_DEF_TIMEOUT
from .p4_manager import P4Manager, \
    KEY_TABLE, KEY_ACTION, KEY_ACTION_PROFILE, \
    KEY_COUNTER, KEY_DIR_COUNTER, KEY_METER, KEY_DIR_METER,\
    KEY_CTL_PKT_METADATA, KEY_DIGEST, KEY_CLONE_SESSION,\
    KEY_ENDPOINT
from .p4_client import WriteOperation

try:
    from _Driver import _Driver
except ImportError:
    from device.service.driver_api._Driver import _Driver

LOGGER = logging.getLogger(__name__)

DRIVER_NAME = 'p4'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})

class P4Driver(_Driver):
    """
    P4Driver class inherits the abstract _Driver class to support P4 devices.

    Attributes
    ----------
    address : str
        IP address of the P4Runtime server running on the P4 device
    port : int
        transport port number of the P4Runtime server running on the P4 device
    **settings : map
        id : int
            P4 device datapath ID (Mandatory)
        name : str
            P4 device name (Optional)
        endpoints : list
            List of P4 device endpoints, i.e., ports (Optional)
        vendor : str
            P4 device vendor (Optional)
        hw_ver : str
            Hardware version of the P4 device (Optional)
        sw_ver : str
            Software version of the P4 device (Optional)
        p4bin : str
            Path to P4 binary file (Optional, but must be combined with p4info)
        p4info : str
            Path to P4 info file (Optional, but must be combined with p4bin)
        timeout : int
            P4 device timeout in seconds (Optional)
        rules : list
            List of rules to configure the P4 device's pipeline
    """

    def __init__(self, address: str, port: int, **settings) -> None:
        super().__init__(name=DRIVER_NAME, address=address, port=port, setting=settings)
        self.__manager = None
        self.__address = address
        self.__port = int(port)
        self.__grpc_endpoint = None
        self.__settings = settings
        self.__id = None
        self.__name = None
        self.__endpoints = []
        self.__rules = {}
        self.__vendor = P4_VAL_DEF_VENDOR
        self.__hw_version = P4_VAL_DEF_HW_VER
        self.__sw_version = P4_VAL_DEF_SW_VER
        self.__p4bin_path = None
        self.__p4info_path = None
        self.__timeout = P4_VAL_DEF_TIMEOUT
        self.__lock = threading.Lock()
        self.__started = threading.Event()
        self.__terminate = threading.Event()

        self.__parse_and_validate_settings()

        LOGGER.info("Initializing P4 device at %s:%d with settings:",
                    self.__address, self.__port)

        for key, value in settings.items():
            LOGGER.info("\t%9s = %s", key, value)

    def Connect(self) -> bool:
        """
        Establish a connection between the P4 device driver and a P4 device.

        :return: boolean connection status.
        """
        LOGGER.info("Connecting to P4 device %s ...", self.__grpc_endpoint)

        with self.__lock:
            # Skip if already connected
            if self.__started.is_set():
                return True

            # TODO: Dynamically devise an election ID
            election_id = (1, 0)

            # Spawn a P4 manager for this device
            self.__manager = P4Manager(
                device_id=self.__id,
                ip_address=self.__address,
                port=self.__port,
                election_id=election_id)
            assert self.__manager

            # Start the P4 manager
            try:
                self.__manager.start(self.__p4bin_path, self.__p4info_path)
            except Exception as ex:  # pylint: disable=broad-except
                raise Exception(ex) from ex

            LOGGER.info("\tConnected via P4Runtime")
            self.__started.set()

            return True

    def Disconnect(self) -> bool:
        """
        Terminate the connection between the P4 device driver and a P4 device.

        :return: boolean disconnection status.
        """
        LOGGER.info("Disconnecting from P4 device %s ...", self.__grpc_endpoint)

        # If not started, assume it is already disconnected
        if not self.__started.is_set():
            return True

        # P4 manager must already be instantiated
        assert self.__manager

        # Trigger termination of loops and processes
        self.__terminate.set()

        # Trigger connection tear down with the P4Runtime server
        self.__manager.stop()
        self.__manager = None

        LOGGER.info("\tDisconnected!")

        return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        """
        Retrieve the initial configuration of a P4 device.

        :return: list of initial configuration items.
        """

        resource_keys = [RESOURCE_ENDPOINTS] if self.__endpoints else []

        with self.__lock:
            if not resource_keys:
                LOGGER.warning("No initial configuration for P4 device {} ...".format(self.__grpc_endpoint))
                return []
            LOGGER.info("Initial configuration for P4 device {}:".format(self.__grpc_endpoint))
            return self.GetConfig(resource_keys)

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys: List[str] = [])\
            -> List[Tuple[str, Union[Any, None, Exception]]]:
        """
        Retrieve the current configuration of a P4 device.

        :param resource_keys: P4 resource keys to retrieve.
        :return: list of values associated with the requested resource keys or
        None/Exception.
        """
        LOGGER.info(
            "Getting configuration from P4 device %s ...", self.__grpc_endpoint)

        # No resource keys means fetch all configuration
        if len(resource_keys) == 0:
            LOGGER.warning(
                "GetConfig with no resource keys "
                "implies getting all resource keys!")
            resource_keys = [
                obj_name for obj_name, _ in self.__manager.p4_objects.items()
            ] + [RESOURCE_ENDPOINTS] + [RESOURCE_RULES]

        # Verify the input type
        chk_type("resources", resource_keys, list)

        with self.__lock:
            return self.__get_resources(resource_keys)

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]])\
            -> List[Union[bool, Exception]]:
        """
        Submit a new configuration to a P4 device.

        :param resources: P4 resources to set.
        :return: list of boolean results or Exceptions for resource key
        changes requested.
        """
        LOGGER.info(
            "Setting configuration to P4 device %s ...", self.__grpc_endpoint)

        if not resources or len(resources) == 0:
            LOGGER.warning(
                "SetConfig requires a list of resources to store "
                "into the device. Nothing is provided though.")
            return []

        assert isinstance(resources, list)

        with self.__lock:
            return self.__set_resources(resources)

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]])\
            -> List[Union[bool, Exception]]:
        """
        Revoke P4 device configuration.

        :param resources: list of tuples with resource keys to be deleted.
        :return: list of boolean results or Exceptions for resource key
        deletions requested.
        """
        LOGGER.info(
            "Deleting configuration from P4 device %s ...", self.__grpc_endpoint)

        if not resources or len(resources) == 0:
            LOGGER.warning(
                "DeleteConfig requires a list of resources to delete "
                "from the device. Nothing is provided though.")
            return []

        with self.__lock:
            return self.__delete_resources(resources)

    def GetResource(self, endpoint_uuid: str) -> Optional[str]:
        """
        Retrieve a certain resource from a P4 device.

        :param endpoint_uuid: target endpoint UUID.
        :return: The path of the endpoint or None if not found.
        """
        LOGGER.warning("GetResource() RPC not yet implemented by the P4 driver")
        return ""

    def GetState(self,
                 blocking=False,
                 terminate: Optional[threading.Event] = None) -> \
                 Iterator[Tuple[str, Any]]:
        """
        Retrieve the state of a P4 device.

        :param blocking: if non-blocking, the driver terminates the loop and
        returns.
        :param terminate: termination flag.
        :return: sequences of state sample.
        """
        LOGGER.warning("GetState() RPC not yet implemented by the P4 driver")
        return []

    @metered_subclass_method(METRICS_POOL)
    def SubscribeState(self, subscriptions: List[Tuple[str, float, float]])\
            -> List[Union[bool, Exception]]:
        """
        Subscribe to certain state information.

        :param subscriptions: list of tuples with resources to be subscribed.
        :return: list of results for resource subscriptions requested.
        """
        LOGGER.warning(
            "SubscribeState() RPC not yet implemented by the P4 driver")
        return [False for _ in subscriptions]

    @metered_subclass_method(METRICS_POOL)
    def UnsubscribeState(self, subscriptions: List[Tuple[str, float, float]])\
            -> List[Union[bool, Exception]]:
        """
        Unsubscribe from certain state information.

        :param subscriptions: list of tuples with resources to be unsubscribed.
        :return: list of results for resource un-subscriptions requested.
        """
        LOGGER.warning(
            "UnsubscribeState() RPC not yet implemented by the P4 driver")
        return [False for _ in subscriptions]

    def get_manager(self):
        """
        Get an instance of the P4 manager.

        :return: P4 manager instance
        """
        return self.__manager

    def is_started(self):
        """
        Check if an instance of the P4 manager is started.

        :return: boolean P4 manager instance status
        """
        return self.__started.is_set()

    def __parse_and_validate_settings(self):
        """
        Verify that the driver inputs comply to what is expected.

        :return: void or exception in case of validation error
        """
        # Device endpoint information
        assert chk_address_ipv4(self.__address) or (chk_address_ipv6(self.__address)),\
            f"{self.__address} not a valid IPv4 or IPv6 address"
        assert chk_transport_port(self.__port), \
            f"{self.__port} not a valid transport port"
        self.__grpc_endpoint = f"{self.__address}:{self.__port}"

        # Device ID
        try:
            self.__id = self.__settings.get(P4_ATTR_DEV_ID)
        except Exception as ex:
            LOGGER.error("P4 device ID is a mandatory setting")
            raise Exception from ex

        # Device name
        if P4_ATTR_DEV_NAME in self.__settings:
            self.__name = self.__settings.get(P4_ATTR_DEV_NAME)
        else:
            self.__name = str(self.__id)
            LOGGER.warning(
                "No device name is provided. Setting default name: %s",
                self.__name)

        # Device endpoints
        if P4_ATTR_DEV_ENDPOINTS in self.__settings:
            endpoints = self.__settings.get(P4_ATTR_DEV_ENDPOINTS, [])
            endpoint_resources = compose_resource_endpoints(endpoints)
            if endpoint_resources:
                LOGGER.info("Setting endpoints: {}".format(endpoint_resources))
                self.SetConfig(endpoint_resources)
        else:
            LOGGER.warning("No device endpoints are provided.")

        # Device vendor
        if P4_ATTR_DEV_VENDOR in self.__settings:
            self.__vendor = self.__settings.get(P4_ATTR_DEV_VENDOR)
        else:
            LOGGER.warning(
                "No device vendor is provided. Setting default vendor: %s",
                self.__vendor)

        # Device hardware version
        if P4_ATTR_DEV_HW_VER in self.__settings:
            self.__hw_version = self.__settings.get(P4_ATTR_DEV_HW_VER)
        else:
            LOGGER.warning(
                "No HW version is provided. Setting default HW version: %s",
                self.__hw_version)

        # Device software version
        if P4_ATTR_DEV_SW_VER in self.__settings:
            self.__sw_version = self.__settings.get(P4_ATTR_DEV_SW_VER)
        else:
            LOGGER.warning(
                "No SW version is provided. Setting default SW version: %s",
                self.__sw_version)

        # Path to P4 binary file
        if P4_ATTR_DEV_P4BIN in self.__settings:
            self.__p4bin_path = self.__settings.get(P4_ATTR_DEV_P4BIN)
            if not os.path.exists(self.__p4bin_path):
                LOGGER.warning(
                    "Invalid path to p4bin file: {}".format(self.__p4bin_path))
                self.__p4bin_path = ""
            else:
                assert P4_ATTR_DEV_P4INFO in self.__settings,\
                    "p4info and p4bin settings must be provided together"

        # Path to P4 info file
        if P4_ATTR_DEV_P4INFO in self.__settings:
            self.__p4info_path = self.__settings.get(P4_ATTR_DEV_P4INFO)
            if not os.path.exists(self.__p4info_path):
                LOGGER.warning(
                    "Invalid path to p4info file: {}".format(self.__p4info_path))
                self.__p4info_path = ""
            else:
                assert P4_ATTR_DEV_P4BIN in self.__settings,\
                    "p4info and p4bin settings must be provided together"

        if (not self.__p4bin_path) or (not self.__p4info_path):
            LOGGER.warning(
                "No P4 binary and info files are provided, hence "
                "no pipeline will be installed on the whitebox device.\n"
                "This driver will attempt to manage whatever pipeline "
                "is available on the target device.")

        # Device timeout
        if P4_ATTR_DEV_TIMEOUT in self.__settings:
            self.__timeout = self.__settings.get(P4_ATTR_DEV_TIMEOUT)
            assert self.__timeout > 0,\
                "Device timeout must be a positive integer"
        else:
            LOGGER.warning(
                "No device timeout is provided. Setting default timeout: %s",
                self.__timeout)

    def __get_resources(self, resource_keys):
        """
        Retrieve the current configuration of a P4 device.

        :param resource_keys: P4 resource keys to retrieve.
        :return: list of values associated with the requested resource keys or
        None/Exception.
        """
        resources = []

        LOGGER.info("GetConfig() -> Keys: {}".format(resource_keys))

        for resource_key in resource_keys:
            entries = []
            try:
                if KEY_TABLE == resource_key:
                    for table_name in self.__manager.get_table_names():
                        t_entries = self.__manager.table_entries_to_json(
                            table_name)
                        if t_entries:
                            entries.append(t_entries)
                elif KEY_COUNTER == resource_key:
                    for cnt_name in self.__manager.get_counter_names():
                        c_entries = self.__manager.counter_entries_to_json(
                            cnt_name)
                        if c_entries:
                            entries.append(c_entries)
                elif KEY_DIR_COUNTER == resource_key:
                    for d_cnt_name in self.__manager.get_direct_counter_names():
                        dc_entries = self.__manager.direct_counter_entries_to_json(
                                d_cnt_name)
                        if dc_entries:
                            entries.append(dc_entries)
                elif KEY_METER == resource_key:
                    for meter_name in self.__manager.get_meter_names():
                        m_entries = self.__manager.meter_entries_to_json(
                            meter_name)
                        if m_entries:
                            entries.append(m_entries)
                elif KEY_DIR_METER == resource_key:
                    for d_meter_name in self.__manager.get_direct_meter_names():
                        dm_entries = self.__manager.direct_meter_entries_to_json(
                                d_meter_name)
                        if dm_entries:
                            entries.append(dm_entries)
                elif KEY_ACTION_PROFILE == resource_key:
                    for ap_name in self.__manager.get_action_profile_names():
                        ap_entries = self.__manager.action_prof_member_entries_to_json(
                                ap_name)
                        if ap_entries:
                            entries.append(ap_entries)
                elif KEY_ACTION == resource_key:
                    # To be implemented or deprecated
                    pass
                elif KEY_CTL_PKT_METADATA == resource_key:
                    #TODO: Handle controller packet metadata
                    msg = f"{resource_key.capitalize()} is not a " \
                          f"retrievable resource"
                    LOGGER.warning("%s", msg)
                elif KEY_DIGEST == resource_key:
                    #TODO: Handle digests
                    msg = f"{resource_key.capitalize()} is not a " \
                          f"retrievable resource"
                    LOGGER.warning("%s", msg)
                elif RESOURCE_ENDPOINTS == resource_key:
                    resources += self.__endpoints
                    continue
                elif RESOURCE_RULES == resource_key:
                     resources = self.__rules_into_resources()
                     continue
                else:
                    msg = f"GetConfig failed due to invalid " \
                          f"resource key: {resource_key}"
                    raise Exception(msg)
                resources.append(
                    (resource_key, entries if entries else None)
                )
            except Exception as e:  # pylint: disable=broad-except
                resources.append((resource_key, e))

        LOGGER.info("GetConfig() -> Results: %s", resources)

        return resources

    def __set_resources(self, resources):
        """
        Submit a new configuration to a P4 device.

        :param resources: P4 resources to set.
        :return: list of boolean results or Exceptions for resource key
        changes requested.
        """
        results = []

        LOGGER.info("SetConfig -> Resources {}".format(resources))

        for i, resource in enumerate(resources):
            str_resource_name = f"resources[#{i}]"
            resource_key = ""
            try:
                chk_type(
                    str_resource_name, resource, (list, tuple))
                chk_length(
                    str_resource_name, resource, min_length=2, max_length=2)
                resource_key, resource_value = resource
                chk_string(
                    str_resource_name, resource_key, allow_empty=False)
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception(
                    "Exception validating %s: %s",
                    str_resource_name, str(resource_key))
                results.append(e)  # store the exception if validation fails
                continue

            try:
                # Rules are JSON-based, endpoints are not
                if "endpoint" not in resource_key:
                    resource_value = json.loads(resource_value)
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception("Exception validating resource value {}".format(resource_value))
                results.append(e)
                continue

            LOGGER.info(
                "SetConfig() -> Key: %s - Value: %s",
                resource_key, resource_value)

            # Default operation is insert.
            # P4 manager has internal logic to judge whether an entry
            # to be inserted already exists, thus simply needs an update.
            operation = WriteOperation.insert

            # Dataplane and cache rule insertion process
            try:
                r2, r3 = False, True
                r1 = self.__cache_rule_insert(resource_key, resource_value, operation)
                # Cache insertion succeeded, proceed to dataplane
                if r1:
                    r2 = self.__apply_operation(resource_key, resource_value, operation)
                # Dataplane insertion did not succeed --> Revert caching
                if not r2 and r1:
                    r3 = self.__cache_rule_remove(resource_key)
                results.append(r1 & r2 & r3)
            except Exception as e:  # pylint: disable=broad-except
                results.append(e)
                continue

        LOGGER.info("SetConfig() -> Results: {}".format(results))

        return results

    def __delete_resources(self, resources):
        """
        Revoke P4 device configuration.

        :param resources: list of tuples with resource keys to be deleted.
        :return: list of boolean results or Exceptions for resource key
        deletions requested.
        """
        results = []

        for i, resource in enumerate(resources):
            str_resource_name = f"resources[#{i}]"
            resource_key = ""
            try:
                chk_type(
                    str_resource_name, resource, (list, tuple))
                chk_length(
                    str_resource_name, resource, min_length=2, max_length=2)
                resource_key, resource_value = resource
                chk_string(
                    str_resource_name, resource_key, allow_empty=False)
            except Exception as e:  # pylint: disable=broad-except
                LOGGER.exception(
                    "Exception validating %s: %s",
                    str_resource_name, str(resource_key))
                results.append(e)  # store the exception if validation fails
                continue

            try:
                resource_value = json.loads(resource_value)
            except Exception as e:  # pylint: disable=broad-except
                results.append(e)
                continue

            LOGGER.info("DeleteConfig() -> Key: %s - Value: %s",
                         resource_key, resource_value)

            operation = WriteOperation.delete

            # Dataplane and cache rule removal process
            try:
                r2, r3 = False, True
                r1 = self.__cache_rule_remove(resource_key)
                # Cache removal succeeded, proceed to dataplane
                if r1:
                    r2 = self.__apply_operation(resource_key, resource_value, operation)
                # Dataplane removal did not succeed --> Revert caching
                if not r2 and r1:
                    r3 = self.__cache_rule_insert(resource_key, resource_value, WriteOperation.insert)
                results.append(r1 & r2 & r3)
            except Exception as e:  # pylint: disable=broad-except
                results.append(e)
                continue

        LOGGER.info("DeleteConfig() -> Results: {}".format(results))

        return results

    def __apply_operation(
            self, resource_key, resource_value, operation: WriteOperation):
        """
        Apply a write operation to a P4 resource.

        :param resource_key: P4 resource key
        :param resource_value: P4 resource value in JSON format
        :param operation: write operation (i.e., insert, update, delete)
        to apply
        :return: True if operation is successfully applied or raise Exception
        """

        # Apply settings to the various tables
        if KEY_TABLE in resource_key:
            self.__manager.table_entry_operation_from_json(
                resource_value, operation)
        elif KEY_COUNTER in resource_key:
            self.__manager.counter_entry_operation_from_json(
                resource_value, operation)
        elif KEY_DIR_COUNTER in resource_key:
            self.__manager.direct_counter_entry_operation_from_json(
                resource_value, operation)
        elif KEY_METER in resource_key:
            self.__manager.meter_entry_operation_from_json(
                resource_value, operation)
        elif KEY_DIR_METER in resource_key:
            self.__manager.direct_meter_entry_operation_from_json(
                resource_value, operation)
        elif KEY_ACTION_PROFILE in resource_key:
            self.__manager.action_prof_member_entry_operation_from_json(
                resource_value, operation)
            self.__manager.action_prof_group_entry_operation_from_json(
                resource_value, operation)
        elif KEY_CLONE_SESSION in resource_key:
            self.__manager.clone_session_entry_operation_from_json(
                resource_value, operation)
        elif KEY_CTL_PKT_METADATA in resource_key:
            msg = f"{resource_key.capitalize()} is not a " \
                  f"configurable resource"
            raise Exception(msg)
        elif KEY_DIGEST in resource_key:
            msg = f"{resource_key.capitalize()} is not a " \
                  f"configurable resource"
            raise Exception(msg)
        elif KEY_ENDPOINT in resource_key:
            self.__endpoints.append((resource_key, resource_value))
        else:
            msg = f"{operation} on invalid key {resource_key}"
            LOGGER.error(msg)
            raise Exception(msg)

        return True

    def __cache_rule_insert(self, resource_key, resource_value, operation):
        """
        Insert a new rule into the rule cache or update an existing one.

        :param resource_key: P4 resource key
        :param resource_value: P4 resource value in JSON format
        :param operation: write operation (i.e., insert, update) to apply
        :return: True if new rule is inserted or existing is updated, otherwise False
        """
        if (resource_key in self.__rules.keys()) and (operation == WriteOperation.insert):
            LOGGER.error("Attempting to insert an existing rule key: {}".format(resource_key))
            return False
        elif (resource_key not in self.__rules.keys()) and (operation == WriteOperation.update):
            LOGGER.error("Attempting to update a non-existing rule key: {}".format(resource_key))
            return False
        elif (resource_key in self.__rules.keys()) and (operation == WriteOperation.update):
            LOGGER.warning("Updating an existing rule key: {}".format(resource_key))
        self.__rules[resource_key] = resource_value
        return True

    def __cache_rule_remove(self, resource_key):
        """
        Remove an existing rule from the rule cache.

        :param resource_key: P4 resource key
        :return: True if existing rule is removed, otherwise False
        """
        if resource_key not in self.__rules.keys():
            LOGGER.error("Attempting to remove a non-existing rule key: {}".format(resource_key))
            return False
        self.__rules.pop(resource_key)
        return True

    def __rules_into_resources(self):
        """
        Transform rules from the driver's rule map into
        resources exposed through the SBI API.
        """
        resource_list = []
        for rule_key, rule_val in self.__rules.items():
            resource_list.append((rule_key, rule_val))
        return resource_list
