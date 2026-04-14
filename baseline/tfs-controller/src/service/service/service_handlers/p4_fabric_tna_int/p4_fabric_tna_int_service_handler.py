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
Service handler for P4-based In-band Network Telemetry (INT) v0.5.
The spec. is based on P4.org Application WG INT Dataplane
Specification v0.5 (2017-12):

https://p4.org/p4-spec/docs/INT_v0_5.pdf
"""

import logging
from typing import Any, List, Optional, Tuple, Union
from uuid import uuid4
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigActionEnum, ContextIdList, DeviceId, Service, Device, Empty
from common.proto.kpi_manager_pb2 import KpiId, KpiDescriptor
from common.proto.kpi_sample_types_pb2 import KpiSampleType
from common.proto.telemetry_frontend_pb2 import Collector, CollectorId
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type, chk_address_mac, chk_address_ipv4,\
    chk_transport_port, chk_vlan_id
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.service_handlers.p4_fabric_tna_commons.p4_fabric_tna_commons import *
from service.service.task_scheduler.TaskExecutor import TaskExecutor

from context.client.ContextClient import ContextClient
from kpi_manager.client.KpiManagerClient import KpiManagerClient
from telemetry.frontend.client.TelemetryFrontendClient import TelemetryFrontendClient

from .p4_fabric_tna_int_config import *

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'p4_fabric_tna_int'})

class P4FabricINTServiceHandler(_ServiceHandler):
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
        self.__service_label = "P4 In-band Network Telemetry (INT) connectivity service"
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(self.__service.service_config, **settings)

        self._init_settings()
        self._parse_settings()
        self._print_settings()

        # TODO: Check whether the Telemetry service is up before issuing this call
        self._start_collector()

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
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
            device_uuid, _ = endpoint[0:2]
            device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))

            # Skip already visited devices
            if device.name in visited:
                continue
            LOGGER.info("Device {} - Setting up In-band Network Telemetry (INT) configuration".format(
                device.name))

            rules = []
            actual_rules = -1
            applied_rules, failed_rules = 0, -1

            # Create and apply rules
            try:
                rules = self._create_rules(device_obj=device, action=ConfigActionEnum.CONFIGACTION_SET)
                actual_rules = len(rules)
                applied_rules, failed_rules = apply_rules(
                    task_executor=self.__task_executor,
                    device_obj=device,
                    json_config_rules=rules
                )
            except Exception as ex:
                LOGGER.error("Failed to insert INT rules on device {} due to {}".format(device.name, ex))
                results.append(ex)
            finally:
                rules.clear()

            # Ensure correct status
            if (failed_rules == 0) and (applied_rules == actual_rules):
                LOGGER.info("Installed {}/{} INT rules on device {}".format(
                    applied_rules, actual_rules, device.name))
                results.append(True)

            # You should no longer visit this device again
            visited.add(device.name)

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]], connection_uuid : Optional[str] = None
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
            device_uuid, _ = endpoint[0:2]
            device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))

            # Skip already visited devices
            if device.name in visited:
                continue
            LOGGER.info("Device {} - Removing In-band Network Telemetry (INT) configuration".format(
                device.name))

            rules = []
            actual_rules = -1
            applied_rules, failed_rules = 0, -1

            # Create and apply rules
            try:
                rules = self._create_rules(device_obj=device, action=ConfigActionEnum.CONFIGACTION_DELETE)
                actual_rules = len(rules)
                applied_rules, failed_rules = apply_rules(
                task_executor=self.__task_executor, device_obj=device, json_config_rules=rules)
            except Exception as ex:
                LOGGER.error("Failed to delete INT rules from device {} due to {}".format(device.name, ex))
                results.append(ex)
            finally:
                rules.clear()

            # Ensure correct status
            if (failed_rules == 0) and (applied_rules == actual_rules):
                LOGGER.info("Deleted {}/{} INT rules from device {}".format(
                    applied_rules, actual_rules, device.name))
                results.append(True)

            # You should no longer visit this device again
            visited.add(device.name)

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
        self.__int_collector_info = {}
        self.__int_collector_iface = ""
        self.__int_collector_mac = ""
        self.__int_collector_ip = ""
        self.__int_collector_port = -1
        self.__int_vlan_id = DEF_VLAN
        self.__int_collector_duration_s = DEF_DURATION_SEC
        self.__int_collector_interval_s = DEF_INTERVAL_SEC

        try:
            self.__settings = self.__settings_handler.get('/settings')
            LOGGER.info("{} with settings: {}".format(self.__service_label, self.__settings))
        except Exception as ex:
            LOGGER.error("Failed to retrieve service settings: {}".format(ex))
            raise Exception(ex)

    def _parse_settings(self):
        try:
            switch_info = self.__settings.value[SWITCH_INFO]
            assert isinstance(switch_info, list), "Switch info object must be a list"
        except Exception as ex:
            LOGGER.error("Failed to parse service settings: {}".format(ex))
            raise Exception(ex)

        for switch in switch_info:
            for switch_name, sw_info in switch.items():
                try:
                    assert switch_name, "Invalid P4 switch name"
                    assert isinstance(sw_info, dict), "Switch {} info must be a map with arch, dpid, mac, ip, and int_port items)"
                    assert sw_info[ARCH] in SUPPORTED_TARGET_ARCH_LIST, \
                        "Switch {} - Supported P4 architectures are: {}".format(switch_name, ','.join(SUPPORTED_TARGET_ARCH_LIST))
                    assert sw_info[DPID] > 0, "Switch {} - P4 switch dataplane ID must be a positive integer".format(switch_name, sw_info[DPID])
                    assert chk_address_mac(sw_info[MAC]), "Switch {} - Invalid source Ethernet address".format(switch_name)
                    assert chk_address_ipv4(sw_info[IP]), "Switch {} - Invalid source IP address".format(switch_name)
                    assert isinstance(sw_info[PORT_INT], dict), "Switch {} - INT port object must be a map with port_id and port_type items".format(switch_name)
                    assert sw_info[PORT_INT][PORT_ID] >= 0, "Switch {} - Invalid P4 switch port ID".format(switch_name)
                    assert sw_info[PORT_INT][PORT_TYPE] in PORT_TYPES_STR_VALID, "Switch {} - Valid P4 switch port types are: {}".format(
                        switch_name, ','.join(PORT_TYPES_STR_VALID))
                    if arch_tna(sw_info[ARCH]):
                        sw_info[RECIRCULATION_PORT_LIST] = RECIRCULATION_PORTS_TNA
                        sw_info[INT_REPORT_MIRROR_ID_LIST] = INT_REPORT_MIRROR_ID_LIST_TNA
                    else:
                        sw_info[RECIRCULATION_PORT_LIST] = RECIRCULATION_PORTS_V1MODEL
                        sw_info[INT_REPORT_MIRROR_ID_LIST] = INT_REPORT_MIRROR_ID_LIST_V1MODEL
                    assert isinstance(sw_info[RECIRCULATION_PORT_LIST], list), "Switch {} - Recirculation ports must be described as a list".format(switch_name)
                except Exception as ex:
                    LOGGER.error("Failed to parse switch {} information".format(switch_name))
                    return
                self.__switch_info[switch_name] = sw_info

        try:
            self.__int_collector_info = self.__settings.value[INT_COLLECTOR_INFO]
            assert isinstance(self.__int_collector_info, dict), "INT collector info object must be a map with mac, ip, port, and vlan_id keys)"

            self.__int_collector_iface = self.__int_collector_info[IFACE]
            assert self.__int_collector_iface, "Invalid P4 INT collector network interface"

            self.__int_collector_mac = self.__int_collector_info[MAC]
            assert chk_address_mac(self.__int_collector_mac), "Invalid P4 INT collector MAC address"

            self.__int_collector_ip = self.__int_collector_info[IP]
            assert chk_address_ipv4(self.__int_collector_ip), "Invalid P4 INT collector IPv4 address"

            self.__int_collector_port = self.__int_collector_info[PORT]
            assert chk_transport_port(self.__int_collector_port), "Invalid P4 INT collector transport port"

            if self.__int_collector_info[VLAN_ID] > 0:
                self.__int_vlan_id = self.__int_collector_info[VLAN_ID]
                assert chk_vlan_id(self.__int_vlan_id), "Invalid VLAN ID for INT"
            else:
                LOGGER.warning("No or invalid INT VLAN ID is provided. Default VLAN ID is set to {} (No VLAN)".\
                               format(self.__int_vlan_id))

            if self.__int_collector_info[DURATION_SEC] > 0:
                self.__int_collector_duration_s = self.__int_collector_info[DURATION_SEC]
            else:
                LOGGER.warning("No or invalid INT collection duration is provided. Default duration is set to {} seconds".\
                               format(self.__int_collector_duration_s))

            if self.__int_collector_info[INTERVAL_SEC] > 0:
                self.__int_collector_interval_s = self.__int_collector_info[INTERVAL_SEC]
            else:
                LOGGER.warning("No or invalid INT collection interval is provided. Default interval is set to {} seconds".\
                               format(self.__int_collector_interval_s))
        except Exception as ex:
            LOGGER.error("Failed to parse INT collector information")
            return

    def _print_settings(self):
        LOGGER.info("-------------------- {} settings --------------------".format(self.__service.name))
        LOGGER.info("--- Topology info")
        for switch_name, switch_info in self.__switch_info.items():
            LOGGER.info("\t Device {}".format(switch_name))
            LOGGER.info("\t\t|  Target P4 architecture: {}".format(switch_info[ARCH]))
            LOGGER.info("\t\t|           Data plane ID: {}".format(switch_info[DPID]))
            LOGGER.info("\t\t|      Source MAC address: {}".format(switch_info[MAC]))
            LOGGER.info("\t\t|      Source  IP address: {}".format(switch_info[IP]))
            LOGGER.info("\t\t|           INT port   ID: {}".format(switch_info[PORT_INT][PORT_ID]))
            LOGGER.info("\t\t|           INT port type: {}".format(switch_info[PORT_INT][PORT_TYPE]))
            LOGGER.info("\t\t| Recirculation port list: {}".format(switch_info[RECIRCULATION_PORT_LIST]))
            LOGGER.info("\t\t|   Report mirror ID list: {}".format(switch_info[INT_REPORT_MIRROR_ID_LIST]))
        LOGGER.info("--- INT collector interface: {}".format(self.__int_collector_iface))
        LOGGER.info("--- INT collector       MAC: {}".format(self.__int_collector_mac))
        LOGGER.info("--- INT collector        IP: {}".format(self.__int_collector_ip))
        LOGGER.info("--- INT collector      port: {}".format(self.__int_collector_port))
        LOGGER.info("--- INT             VLAN ID: {}".format(self.__int_vlan_id))
        LOGGER.info("--- INT collector  duration: {} sec".format(self.__int_collector_duration_s))
        LOGGER.info("--- INT collector  interval: {} sec".format(self.__int_collector_interval_s))
        LOGGER.info("-----------------------------------------------------------------")

    def _create_rules(self, device_obj : Device, action : ConfigActionEnum): # type: ignore
        dev_name = device_obj.name
        rules  = []

        ### INT reporting rules
        try:
            rules += rules_set_up_int_watchlist(action=action)
        except Exception as ex:
            LOGGER.error("Error while creating INT watchlist rules")
            raise Exception(ex)

        try:
            rules += rules_set_up_int_recirculation_ports(
                recirculation_port_list=self.__switch_info[dev_name][RECIRCULATION_PORT_LIST],
                port_type=PORT_TYPE_INT,
                fwd_type=FORWARDING_TYPE_UNICAST_IPV4,
                vlan_id=self.__int_vlan_id,
                action=action
            )
        except Exception as ex:
            LOGGER.error("Error while creating INT recirculation rules")
            raise Exception(ex)

        try:
            rules += rules_set_up_int_report_collector(
                int_collector_ip=self.__int_collector_ip,
                action=action
            )
        except Exception as ex:
            LOGGER.error("Error while creating INT report collector rules")
            raise Exception(ex)

        try:
            rules += rules_set_up_int_report_flow(
                switch_id=self.__switch_info[dev_name][DPID],
                src_ip=self.__switch_info[dev_name][IP],
                int_collector_ip=self.__int_collector_ip,
                int_collector_port=self.__int_collector_port,
                action=action
            )
        except Exception as ex:
            LOGGER.error("Error while creating INT report flow rules")
            raise Exception(ex)

        try:
            rules += rules_set_up_report_mirror_flow(
                recirculation_port_list=self.__switch_info[dev_name][RECIRCULATION_PORT_LIST],
                report_mirror_id_list=self.__switch_info[dev_name][INT_REPORT_MIRROR_ID_LIST],
                action=action
            )
        except Exception as ex:
            LOGGER.error("Error while creating report mirror flow rules")
            raise Exception(ex)

        ### INT port setup rules
        try:
            rules += rules_set_up_port(
                port=self.__switch_info[dev_name][PORT_INT][PORT_ID],
                port_type=PORT_TYPE_HOST,
                fwd_type=FORWARDING_TYPE_BRIDGING,
                vlan_id=self.__int_vlan_id,
                action=action
            )
        except Exception as ex:
            LOGGER.error("Error while creating INT port rules")
            raise Exception(ex)

        ### INT port forwarding rules
        try:
            rules += rules_set_up_fwd_bridging(
                vlan_id=self.__int_vlan_id,
                eth_dst=self.__int_collector_mac,
                egress_port=self.__switch_info[dev_name][PORT_INT][PORT_ID],
                action=action
            )
            rules += rules_set_up_next_output_simple(
                egress_port=self.__switch_info[dev_name][PORT_INT][PORT_ID],
                action=action
            )
        except Exception as ex:
            LOGGER.error("Error while creating INT bridging rules")
            raise Exception(ex)

        ### INT packet routing rules
        try:
            rules += rules_set_up_next_routing_simple(
                egress_port=self.__switch_info[dev_name][PORT_INT][PORT_ID],
                eth_src=self.__switch_info[dev_name][MAC],
                eth_dst=self.__int_collector_mac,
                action=action
            )
            rules += rules_set_up_routing(
                ipv4_dst=self.__int_collector_ip,
                ipv4_prefix_len=32,
                egress_port=self.__switch_info[dev_name][PORT_INT][PORT_ID],
                action=action
            )
        except Exception as ex:
            LOGGER.error("Error while creating INT routing rules")
            raise Exception(ex)

        return rules

    def _retrieve_context_for_int_collector(self):
        ctx_id = service_id = dev_id = ep_id = None

        try:
            context_client = ContextClient()
            response : ContextIdList = context_client.ListContextIds(Empty()) # type: ignore

            # Get the context
            ctx_id = response.context_ids[0].context_uuid.uuid
            assert ctx_id, "Cannot create INT collector with invalid context ID"
            LOGGER.debug("Context ID: {}".format(ctx_id))

            service_id = self.__service.service_id.service_uuid.uuid
            assert service_id, "Cannot create INT collector with invalid service ID"
            LOGGER.debug("Service ID: {}".format(service_id))

            # Get a service endpoint
            svc_endpoints = self.__service.service_endpoint_ids[0]
            assert svc_endpoints, "Cannot create INT collector: No service endpoints are established"

            # Get a P4 device associated with this endpoint
            dev_id = svc_endpoints.device_id.device_uuid.uuid
            assert dev_id, "Cannot create INT collector with invalid device ID"
            LOGGER.debug("Device ID: {}".format(dev_id))

            # Get the endpoint ID
            ep_id = svc_endpoints.endpoint_uuid.uuid
            assert ep_id, "Cannot create INT collector with invalid endpoint ID"
            LOGGER.debug("Endpoint ID: {}".format(ep_id))
        except Exception as ex:
            LOGGER.error("Failed to retrieve context for starting the INT collector: {}".format(ex))
            raise ex

        return ctx_id, service_id, dev_id, ep_id

    def _start_collector(self):
        ctx_id = service_id = dev_id = ep_id = None
        try:
            ctx_id, service_id, dev_id, ep_id = self._retrieve_context_for_int_collector()
        except Exception:
            LOGGER.error("INT collector cannot be initialized due to missing information")
            return

        # Create a "virtual" INT KPI associated with this context and P4 dataplane
        kpi_id_int = None
        try:
            kpi_descriptor_int = KpiDescriptor()
            kpi_descriptor_int.kpi_sample_type = KpiSampleType.KPISAMPLETYPE_UNKNOWN
            kpi_descriptor_int.service_id.service_uuid.uuid = service_id
            kpi_descriptor_int.device_id.device_uuid.uuid = dev_id
            kpi_descriptor_int.endpoint_id.endpoint_uuid.uuid = ep_id
            kpi_descriptor_int.kpi_id.kpi_id.uuid = str(uuid4())

            # Set this new KPI
            kpi_manager_client = KpiManagerClient()
            kpi_id_int: KpiId = kpi_manager_client.SetKpiDescriptor(kpi_descriptor_int) # type: ignore
            LOGGER.debug("INT KPI ID: {}".format(kpi_id_int))
        except Exception:
            LOGGER.error("INT collector cannot be initialized due to failed KPI initialization")
            return

        # Initialize an INT collector object
        try:
            collect_int = Collector()
            collect_int.collector_id.collector_id.uuid = str(uuid4())
            collect_int.kpi_id.kpi_id.uuid = kpi_id_int.kpi_id.uuid
            collect_int.duration_s = self.__int_collector_duration_s
            collect_int.interval_s = self.__int_collector_interval_s
            collect_int.int_collector.interface = self.__int_collector_iface
            collect_int.int_collector.transport_port = self.__int_collector_port
            collect_int.int_collector.service_id = service_id
            collect_int.int_collector.context_id = ctx_id
            LOGGER.info("INT Collector: {}".format(str(collect_int)))

            telemetry_frontend_client = TelemetryFrontendClient()
            collect_id: CollectorId = telemetry_frontend_client.StartCollector(collect_int) # type: ignore
            assert collect_id.uuid, "INT collector failed to start"
        except Exception:
            LOGGER.error("INT collector cannot be initialized")
            return

        LOGGER.info("INT collector with ID {} is successfully invoked".format(collect_id))
