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

from typing import Any, List, Optional, Tuple, Union
from common.proto.context_pb2 import Service
from service.service.task_scheduler.TaskExecutor import TaskExecutor

class _ServiceHandler:
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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()
    
    
    def SetOpticalConfig (
        self, endpoints : List[Tuple[str, str, Optional[str]]],
        connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]: 
        
          """ Create/Update Optical configuration related to optical service.
            Parameters:
                endpoints: List[Tuple[str, str, Optional[str]]]
                    List of tuples, each containing a device_uuid,
                    endpoint_uuid and, optionally, the topology_uuid
                    of the endpoint to be added.
                connection_uuid : Optional[str]
                    If specified, is the UUID of the connection this endpoint is associated to.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for configurations changes requested. 
                    Return values must be in the same order as the requested
                    configurtations.   
        """
        
