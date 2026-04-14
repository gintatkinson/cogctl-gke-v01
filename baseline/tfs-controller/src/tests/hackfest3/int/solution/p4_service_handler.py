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
P4 service handler for the TeraFlowSDN controller.
"""

import logging
from typing import Any, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, DeviceId, Service
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.task_scheduler.TaskExecutor import TaskExecutor

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'Handler', labels={'handler': 'p4'})

def create_rule_set(endpoint_a, endpoint_b):
    return json_config_rule_set(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_exact_table',
            'match-fields': [
                {
                    'match-field': 'standard_metadata.ingress_port',
                    'match-value': endpoint_a
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port',
                    'action-value': endpoint_b
                }
            ]
        }
    )

def create_rule_del(endpoint_a, endpoint_b):
    return json_config_rule_delete(
        'table',
        {
            'table-name': 'IngressPipeImpl.l2_exact_table',
            'match-fields': [
                {
                    'match-field': 'standard_metadata.ingress_port',
                    'match-value': endpoint_a
                }
            ],
            'action-name': 'IngressPipeImpl.set_egress_port',
            'action-params': [
                {
                    'action-param': 'port',
                    'action-value': endpoint_b
                }
            ]
        }
    )
    
def create_int_set(endpoint_a, id):
    return json_config_rule_set(
        'table',
        {
            'table-name': 'EgressPipeImpl.int_table',
       	    'match-fields': [
                {
                    'match-field': 'standard_metadata.ingress_port',
                    'match-value': endpoint_a
                }
            ],
            'action-name': 'EgressPipeImpl.add_int_header',
            'action-params': [
                {
                    'action-param': 'swid',
                    'action-value': id
                }
            ]
        }
    )
    
def create_int_del(endpoint_a, id):
    return json_config_rule_delete(
        'table',
        {
            'table-name': 'EgressPipeImpl.int_table',
       	    'match-fields': [
                {
                    'match-field': 'standard_metadata.ingress_port',
                    'match-value': endpoint_a
                }
            ],
            'action-name': 'EgressPipeImpl.add_int_header',
            'action-params': [
                {
                    'action-param': 'swid',
                    'action-value': id
                }
            ]
        }
    )

def find_names(uuid_a, uuid_b, device_endpoints):
    endpoint_a, endpoint_b = None, None
    for endpoint in device_endpoints:
        if endpoint.endpoint_id.endpoint_uuid.uuid == uuid_a:
            endpoint_a = endpoint.name
        elif endpoint.endpoint_id.endpoint_uuid.uuid == uuid_b:
            endpoint_b = endpoint.name
            
    return (endpoint_a, endpoint_b)

class P4ServiceHandler(_ServiceHandler):
    def __init__(self,
                 service: Service,
                 task_executor : TaskExecutor,
                 **settings) -> None:
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
        self.__service = service
        self.__task_executor = task_executor # pylint: disable=unused-private-member

    @metered_subclass_method(METRICS_POOL)
    def SetEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]],
        connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        """ Create/Update service endpoints form a list.
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

        service_uuid = self.__service.service_id.service_uuid.uuid

        history = {}
        
        results = []
        index = {}
        i = 0
        for endpoint in endpoints:        
            device_uuid, endpoint_uuid = endpoint[0:2] # ignore topology_uuid by now
            if device_uuid in history:       
                try:
                    matched_endpoint_uuid = history.pop(device_uuid)
                    device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))

                    del device.device_config.config_rules[:]
                    
                    # Find names from uuids
                    (endpoint_a, endpoint_b) = find_names(matched_endpoint_uuid, endpoint_uuid, device.device_endpoints)
                    if endpoint_a is None:
                        LOGGER.exception('Unable to find name of endpoint({:s})'.format(str(matched_endpoint_uuid)))
                        raise Exception('Unable to find name of endpoint({:s})'.format(str(matched_endpoint_uuid)))
                    if endpoint_b is None:
                        LOGGER.exception('Unable to find name of endpoint({:s})'.format(str(endpoint_uuid)))
                        raise Exception('Unable to find name of endpoint({:s})'.format(str(endpoint_uuid)))

                    # One way
                    rule = create_rule_set(endpoint_a, endpoint_b) 
                    device.device_config.config_rules.append(ConfigRule(**rule))
                    # The other way
                    rule = create_rule_set(endpoint_b, endpoint_a) 
                    device.device_config.config_rules.append(ConfigRule(**rule))
                    
                    rule = create_int_set(endpoint_a, device.name[-1])
                    device.device_config.config_rules.append(ConfigRule(**rule))

                    self.__task_executor.configure_device(device)
            
                    results.append(True)
                    results[index[device_uuid]] = True
                except Exception as e:
                    LOGGER.exception('Unable to SetEndpoint({:s})'.format(str(endpoint)))
                    results.append(e)
            else:
                history[device_uuid] = endpoint_uuid
                index[device_uuid] = i
                results.append(False)
            i = i+1

        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]],
        connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        """ Delete service endpoints form a list.
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

        service_uuid = self.__service.service_id.service_uuid.uuid

        history = {}
        
        results = []
        index = {}
        i = 0
        for endpoint in endpoints:        
            device_uuid, endpoint_uuid = endpoint[0:2] # ignore topology_uuid by now
            if device_uuid in history:       
                try:
                    matched_endpoint_uuid = history.pop(device_uuid)
                    device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))

                    del device.device_config.config_rules[:]

                    # Find names from uuids
                    (endpoint_a, endpoint_b) = find_names(matched_endpoint_uuid, endpoint_uuid, device.device_endpoints)
                    if endpoint_a is None:
                        LOGGER.exception('Unable to find name of endpoint({:s})'.format(str(matched_endpoint_uuid)))
                        raise Exception('Unable to find name of endpoint({:s})'.format(str(matched_endpoint_uuid)))
                    if endpoint_b is None:
                        LOGGER.exception('Unable to find name of endpoint({:s})'.format(str(endpoint_uuid)))
                        raise Exception('Unable to find name of endpoint({:s})'.format(str(endpoint_uuid)))

                    # One way
                    rule = create_rule_del(endpoint_a, endpoint_b) 
                    device.device_config.config_rules.append(ConfigRule(**rule))
                    # The other way
                    rule = create_rule_del(endpoint_b, endpoint_a) 
                    device.device_config.config_rules.append(ConfigRule(**rule))

                    rule = create_int_del(endpoint_a, device.name[-1])
                    device.device_config.config_rules.append(ConfigRule(**rule))

                    self.__task_executor.configure_device(device)
            
                    results.append(True)
                    results[index[device_uuid]] = True
                except Exception as e:
                    LOGGER.exception('Unable to SetEndpoint({:s})'.format(str(endpoint)))
                    results.append(e)
            else:
                history[device_uuid] = endpoint_uuid
                index[device_uuid] = i
                results.append(False)
            i = i+1

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