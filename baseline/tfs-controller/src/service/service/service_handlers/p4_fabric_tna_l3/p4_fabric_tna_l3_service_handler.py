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
Service handler for P4-based static L3 routing using the SD-Fabric P4 dataplane
for BMv2 and Intel Tofino switches.
"""

import logging
from typing import Any, List, Dict, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigActionEnum, DeviceId, Service, Device
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type, chk_address_mac, chk_address_ipv4, chk_prefix_len_ipv4
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.service_handlers.p4_fabric_tna_commons.p4_fabric_tna_commons import *
from service.service.task_scheduler.TaskExecutor import TaskExecutor

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'p4_fabric_tna_l3'})

class P4FabricL3ServiceHandler(_ServiceHandler):
    def __init__(   # pylint: disable=super-init-not-called
        self, service : Service, task_executor : TaskExecutor, **settings # type: ignore
    ) -> None:
        """ Initialize Driver.
            Parameters:
                service
                    The service instance (gRPC message) to be managed.
                task_executor
                    An instance of Task Executor providing access to the
                    service handlers factory, the context and device clients,
                    and an internal cache of already-loaded gRPC entities.
                **settings
                    Extra settings required by the service handler.

        """
        self.__service_label = "P4 static L3 connectivity service"
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(self.__service.service_config, **settings)

        self._init_settings()
        self._parse_settings()
        self._print_settings()

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]],
        connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        """ Create/Update service endpoints from a list.
            Parameters:
                endpoints: List[Tuple[str, str, Optional[str]]]
                    List of tuples, each containing a device_uuid,
                    endpoint_uuid and, optionally, the topology_uuid
                    of the endpoint to be added.
                connection_uuid : Optional[str]
                    If specified, is the UUID of the connection this endpoint is associated to.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for endpoint changes requested.
                    Return values must be in the same order as the requested
                    endpoints. If an endpoint is properly added, True must be
                    returned; otherwise, the Exception that is raised during
                    the processing must be returned.
        """
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []

        LOGGER.info("{} - Provision service configuration".format(
            self.__service_label))

        visited = set()
        results = []
        for endpoint in endpoints:
            device_uuid, endpoint_uuid = endpoint[0:2]
            device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
            device_name = device.name

            LOGGER.info("Device {}".format(device_name))
            LOGGER.info("\t | Service endpoint UUID: {}".format(endpoint_uuid))

            port_id = find_port_id_in_endpoint_list(device.device_endpoints, endpoint_uuid)
            LOGGER.info("\t | Service port ID: {}".format(port_id))

            dev_port_key = device_name + "-" + PORT_PREFIX + str(port_id)

            # Skip already visited device ports
            if dev_port_key in visited:
                continue

            rules = []
            actual_rules = -1
            applied_rules, failed_rules = 0, -1

            # Create and apply rules
            try:
                rules = self._create_rules(
                    device_obj=device, port_id=port_id, action=ConfigActionEnum.CONFIGACTION_SET)
                actual_rules = len(rules)
                applied_rules, failed_rules = apply_rules(
                    task_executor=self.__task_executor,
                    device_obj=device,
                    json_config_rules=rules
                )
            except Exception as ex:
                LOGGER.error("Failed to insert L3 rules on device {} due to {}".format(device.name, ex))
                results.append(ex)
            finally:
                rules.clear()

            # Ensure correct status
            if (failed_rules == 0) and (applied_rules == actual_rules):
                LOGGER.info("Installed {}/{} ACL rules on device {} and port {}".format(
                    applied_rules, actual_rules, device_name, port_id))
                results.append(True)

            # You should no longer visit this device port again
            visited.add(dev_port_key)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]],
        connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        """ Delete service endpoints from a list.
            Parameters:
                endpoints: List[Tuple[str, str, Optional[str]]]
                    List of tuples, each containing a device_uuid,
                    endpoint_uuid, and the topology_uuid of the endpoint
                    to be removed.
                connection_uuid : Optional[str]
                    If specified, is the UUID of the connection this endpoint is associated to.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for endpoint deletions requested.
                    Return values must be in the same order as the requested
                    endpoints. If an endpoint is properly deleted, True must be
                    returned; otherwise, the Exception that is raised during
                    the processing must be returned.
        """
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0: return []

        LOGGER.info("{} - Deprovision service configuration".format(
            self.__service_label))

        visited = set()
        results = []
        for endpoint in endpoints:
            device_uuid, endpoint_uuid = endpoint[0:2]
            device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
            device_name = device.name

            LOGGER.info("Device {}".format(device_name))
            LOGGER.info("\t | Service endpoint UUID: {}".format(endpoint_uuid))

            port_id = find_port_id_in_endpoint_list(device.device_endpoints, endpoint_uuid)
            LOGGER.info("\t | Service port ID: {}".format(port_id))

            dev_port_key = device_name + "-" + PORT_PREFIX + str(port_id)

            # Skip already visited device ports
            if dev_port_key in visited:
                continue

            rules = []
            actual_rules = -1
            applied_rules, failed_rules = 0, -1

            # Create and apply rules
            try:
                rules = self._create_rules(
                    device_obj=device, port_id=port_id, action=ConfigActionEnum.CONFIGACTION_DELETE)
                actual_rules = len(rules)
                applied_rules, failed_rules = apply_rules(
                    task_executor=self.__task_executor,
                    device_obj=device,
                    json_config_rules=rules
                )
            except Exception as ex:
                LOGGER.error("Failed to delete L3 rules from device {} due to {}".format(device.name, ex))
                results.append(ex)
            finally:
                rules.clear()

            # Ensure correct status
            if (failed_rules == 0) and (applied_rules == actual_rules):
                LOGGER.info("Deleted {}/{} L3 rules from device {} and port {}".format(
                    applied_rules, actual_rules, device_name, port_id))
                results.append(True)

            # You should no longer visit this device port again
            visited.add(dev_port_key)

        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConstraint(self, constraints: List[Tuple[str, Any]]) \
            -> List[Union[bool, Exception]]:
        """ Create/Update service constraints.
            Parameters:
                constraints: List[Tuple[str, Any]]
                    List of tuples, each containing a constraint_type and the
                    new constraint_value to be set.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for constraint changes requested.
                    Return values must be in the same order as the requested
                    constraints. If a constraint is properly set, True must be
                    returned; otherwise, the Exception that is raised during
                    the processing must be returned.
        """
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []

        msg = '[SetConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConstraint(self, constraints: List[Tuple[str, Any]]) \
            -> List[Union[bool, Exception]]:
        """ Delete service constraints.
            Parameters:
                constraints: List[Tuple[str, Any]]
                    List of tuples, each containing a constraint_type pointing
                    to the constraint to be deleted, and a constraint_value
                    containing possible additionally required values to locate
                    the constraint to be removed.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for constraint deletions requested.
                    Return values must be in the same order as the requested
                    constraints. If a constraint is properly deleted, True must
                    be returned; otherwise, the Exception that is raised during
                    the processing must be returned.
        """
        chk_type('constraints', constraints, list)
        if len(constraints) == 0: return []

        msg = '[DeleteConstraint] Method not implemented. Constraints({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(constraints)))
        return [True for _ in range(len(constraints))]

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources: List[Tuple[str, Any]]) \
            -> List[Union[bool, Exception]]:
        """ Create/Update configuration for a list of service resources.
            Parameters:
                resources: List[Tuple[str, Any]]
                    List of tuples, each containing a resource_key pointing to
                    the resource to be modified, and a resource_value
                    containing the new value to be set.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for resource key changes requested.
                    Return values must be in the same order as the requested
                    resource keys. If a resource is properly set, True must be
                    returned; otherwise, the Exception that is raised during
                    the processing must be returned.
        """
        chk_type('resources', resources, list)
        if len(resources) == 0: return []

        msg = '[SetConfig] Method not implemented. Resources({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(resources)))
        return [True for _ in range(len(resources))]

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(self, resources: List[Tuple[str, Any]]) \
            -> List[Union[bool, Exception]]:
        """ Delete configuration for a list of service resources.
            Parameters:
                resources: List[Tuple[str, Any]]
                    List of tuples, each containing a resource_key pointing to
                    the resource to be modified, and a resource_value containing
                    possible additionally required values to locate the value
                    to be removed.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for resource key deletions requested.
                    Return values must be in the same order as the requested
                    resource keys. If a resource is properly deleted, True must
                    be returned; otherwise, the Exception that is raised during
                    the processing must be returned.
        """
        chk_type('resources', resources, list)
        if len(resources) == 0: return []

        msg = '[SetConfig] Method not implemented. Resources({:s}) are being ignored.'
        LOGGER.warning(msg.format(str(resources)))
        return [True for _ in range(len(resources))]

    def _init_settings(self):
        self.__switch_info = {}
        self.__port_map = {}

        try:
            self.__settings = self.__settings_handler.get('/settings')
            LOGGER.info("{} with settings: {}".format(self.__service_label, self.__settings))
        except Exception as ex:
            LOGGER.error("Failed to retrieve service settings: {}".format(ex))
            raise Exception(ex)

    def _parse_settings(self):
        try:
            switch_info = self.__settings.value[SWITCH_INFO]
        except Exception as ex:
            LOGGER.error("Failed to parse service settings: {}".format(ex))
            raise Exception(ex)
        assert isinstance(switch_info, list), "Switch info object must be a list"

        for switch in switch_info:
            for switch_name, sw_info in switch.items():
                assert switch_name, "Invalid P4 switch name"
                assert isinstance(sw_info, dict), "Switch {} info must be a map with arch, dpid, and fwd_list items)"
                assert sw_info[ARCH] in SUPPORTED_TARGET_ARCH_LIST, \
                    "Switch {} - Supported P4 architectures are: {}".format(switch_name, ','.join(SUPPORTED_TARGET_ARCH_LIST))
                switch_dpid = sw_info[DPID]
                assert switch_dpid > 0, "Switch {} - P4 switch dataplane ID must be a positive integer".format(switch_name, sw_info[DPID])

                # Port list
                port_list = sw_info[PORT_LIST]
                assert isinstance(port_list, list),\
                    "Switch {} port list must be a list with port_id and port_type items".format(switch_name)
                for port in port_list:
                    port_id = port[PORT_ID]
                    assert port_id >= 0, "Switch {} - Invalid P4 switch port ID".format(switch_name)
                    port_type = port[PORT_TYPE]
                    assert port_type in PORT_TYPES_STR_VALID, "Switch {} - Valid P4 switch port types are: {}".format(
                        switch_name, ','.join(PORT_TYPES_STR_VALID))

                    if switch_name not in self.__port_map:
                        self.__port_map[switch_name] = {}
                    port_key = PORT_PREFIX + str(port_id)
                    if port_key not in self.__port_map[switch_name]:
                        self.__port_map[switch_name][port_key] = {}
                    self.__port_map[switch_name][port_key][PORT_ID] = port_id
                    self.__port_map[switch_name][port_key][PORT_TYPE] = port_type
                    self.__port_map[switch_name][port_key][ROUTING_LIST] = []

                # Routing list
                routing_list = sw_info[ROUTING_LIST]
                assert isinstance(routing_list, list), "Switch {} routing list must be a list".format(switch_name)
                for rt_entry in routing_list:
                    port_id = rt_entry[PORT_ID]
                    assert port_id >= 0, "Invalid port ID: {}".format(port_id)
                    ipv4_dst = rt_entry[IPV4_DST]
                    assert chk_address_ipv4(ipv4_dst), "Invalid destination IPv4 address {}".format(ipv4_dst)
                    ipv4_prefix_len = rt_entry[IPV4_PREFIX_LEN]
                    assert chk_prefix_len_ipv4(ipv4_prefix_len), "Invalid IPv4 address prefix length {}".format(ipv4_prefix_len)
                    mac_src = rt_entry[MAC_SRC]
                    assert chk_address_mac(mac_src), "Invalid source MAC address {}".format(mac_src)
                    mac_dst = rt_entry[MAC_DST]
                    assert chk_address_mac(mac_dst), "Invalid destination MAC address {}".format(mac_dst)

                    # Retrieve entry from the port map
                    switch_port_entry = self._get_switch_port_in_port_map(switch_name, port_id)

                    # Add routing entry
                    switch_port_entry[ROUTING_LIST].append(
                        {
                            PORT_ID: port_id,
                            IPV4_DST: ipv4_dst,
                            IPV4_PREFIX_LEN: ipv4_prefix_len,
                            MAC_SRC: mac_src,
                            MAC_DST: mac_dst
                        }
                    )
                self.__switch_info[switch_name] = sw_info

    def _print_settings(self):
        LOGGER.info("--------------- {} settings ---------------".format(self.__service.name))
        LOGGER.info("--- Topology info")
        for switch_name, switch_info in self.__switch_info.items():
            LOGGER.info("\t Device {}".format(switch_name))
            LOGGER.info("\t\t| Target P4 architecture: {}".format(switch_info[ARCH]))
            LOGGER.info("\t\t|          Data plane ID: {}".format(switch_info[DPID]))
            LOGGER.info("\t\t|               Port map: {}".format(self.__port_map[switch_name]))
        LOGGER.info("-------------------------------------------------------")

    def _get_switch_port_in_port_map(self, switch_name : str, port_id : int) -> Dict:
        assert switch_name, "A valid switch name must be used as a key to the port map"
        assert port_id > 0, "A valid switch port ID must be used as a key to a switch's port map"
        switch_entry = self.__port_map[switch_name]
        assert switch_entry, "Switch {} does not exist in the port map".format(switch_name)
        port_key = PORT_PREFIX + str(port_id)
        assert switch_entry[port_key], "Port with ID {} does not exist in the switch map".format(port_id)

        return switch_entry[port_key]

    def _get_routing_list_of_switch_port(self, switch_name : str, port_id : int) -> List [Tuple]:
        switch_port_entry = self._get_switch_port_in_port_map(switch_name, port_id)
        return switch_port_entry[ROUTING_LIST]

    def _create_rules(self, device_obj : Device, port_id : int, action : ConfigActionEnum): # type: ignore
        dev_name = device_obj.name

        rules  = []

        ### Static routing rules
        routing_list = self._get_routing_list_of_switch_port(switch_name=dev_name, port_id=port_id)
        for rt_entry in routing_list:
            try:
                rules += rules_set_up_next_routing_simple(
                    egress_port=port_id,
                    eth_src=rt_entry[MAC_SRC],
                    eth_dst=rt_entry[MAC_DST],
                    action=action
                )
                rules += rules_set_up_routing(
                    ipv4_dst=rt_entry[IPV4_DST],
                    ipv4_prefix_len=rt_entry[IPV4_PREFIX_LEN],
                    egress_port=port_id,
                    action=action
                )
            except Exception as ex:
                LOGGER.error("Error while creating static L3 routing rules")
                raise Exception(ex)

        return rules
