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

import grpc, json, logging, random, uuid
from typing import Dict, Optional
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.method_wrappers.ServiceExceptions import (
    AlreadyExistsException, InvalidArgumentException, NotFoundException, NotImplementedException,
    OperationFailedException
)
from common.proto.context_pb2 import (
    Connection, ConstraintActionEnum, Empty, Service, ServiceId, ServiceStatusEnum,
    ServiceTypeEnum, TopologyId
)
from common.proto.pathcomp_pb2 import PathCompRequest
from common.proto.e2eorchestrator_pb2 import E2EOrchestratorRequest
from common.proto.service_pb2_grpc import ServiceServiceServicer
from common.tools.context_queries.Service import get_service_by_id
from common.tools.grpc.Tools import grpc_message_to_json, grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology_id
from common.Constants import OpticalServiceType, DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.Settings import (
    is_deployed_e2e_orch, is_deployed_optical, is_deployed_te
)
from context.client.ContextClient import ContextClient
from e2e_orchestrator.client.E2EOrchestratorClient import E2EOrchestratorClient
from pathcomp.frontend.client.PathCompClient import PathCompClient
from service.service.tools.ConnectionToString import connection_to_string
from service.client.TEServiceClient import TEServiceClient
from .service_handler_api.ServiceHandlerFactory import ServiceHandlerFactory
from .task_scheduler.TaskScheduler import TasksScheduler
from .tools.GeodesicDistance import gps_distance
from .tools.OpticalTools import (
    add_flex_lightpath, add_lightpath, delete_lightpath, adapt_reply, get_device_name_from_uuid,
    get_optical_band, refresh_opticalcontroller, DelFlexLightpath , extend_optical_band

)


LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'RPC')

class ServiceServiceServicerImpl(ServiceServiceServicer):
    def __init__(self, service_handler_factory : ServiceHandlerFactory) -> None:
        LOGGER.debug('Creating Servicer...')
        self.service_handler_factory = service_handler_factory
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def CreateService(self, request : Service, context : grpc.ServicerContext) -> ServiceId:
        if len(request.service_endpoint_ids) > 0:
            unexpected_endpoints = []
            for service_endpoint_id in request.service_endpoint_ids:
                unexpected_endpoints.append(grpc_message_to_json(service_endpoint_id))
            str_unexpected_endpoints = json.dumps(unexpected_endpoints, sort_keys=True)
            raise InvalidArgumentException(
                'service.service_endpoint_ids', str_unexpected_endpoints,
                extra_details='RPC method CreateService does not accept Endpoints. '\
                              'Endpoints should be configured after creating the service.')

        if len(request.service_constraints) > 0:
            unexpected_constraints = []
            for service_constraint in request.service_constraints:
                unexpected_constraints.append(grpc_message_to_json(service_constraint))
            str_unexpected_constraints = json.dumps(unexpected_constraints, sort_keys=True)
            raise InvalidArgumentException(
                'service.service_constraints', str_unexpected_constraints,
                extra_details='RPC method CreateService does not accept Constraints. '\
                              'Constraints should be configured after creating the service.')

        if len(request.service_config.config_rules) > 0:
            unexpected_config_rules = grpc_message_to_json(request.service_config)
            unexpected_config_rules = unexpected_config_rules['config_rules']
            str_unexpected_config_rules = json.dumps(unexpected_config_rules, sort_keys=True)
            raise InvalidArgumentException(
                'service.service_config.config_rules', str_unexpected_config_rules,
                extra_details='RPC method CreateService does not accept Config Rules. '\
                              'Config Rules should be configured after creating the service.')

        # check that service does not exist
        context_client = ContextClient()
        current_service = get_service_by_id(
            context_client, request.service_id, rw_copy=False,
            include_config_rules=False, include_constraints=False, include_endpoint_ids=False)
        if current_service is not None:
            context_uuid = request.service_id.context_id.context_uuid.uuid
            service_uuid = request.service_id.service_uuid.uuid
            raise AlreadyExistsException(
                'Service', service_uuid, extra_details='context_uuid={:s}'.format(str(context_uuid)))

        # just create the service in the Context database to lock the service_id
        # update will perform changes on the resources
        service_id = context_client.SetService(request)
        return service_id

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def UpdateService(self, request : Service, context : grpc.ServicerContext) -> ServiceId:
        # Set service status to "SERVICESTATUS_PLANNED" to ensure rest of components are aware the service is
        # being modified.
        context_client = ContextClient()
        _service : Optional[Service] = get_service_by_id(
            context_client, request.service_id, rw_copy=False,
            include_config_rules=True, include_constraints=True, include_endpoint_ids=True)

        # Identify service constraints
        num_disjoint_paths = None
        is_diverse = False
        gps_location_aware = False
        for constraint in request.service_constraints:
            constraint_kind = constraint.WhichOneof('constraint')
            if constraint_kind == 'sla_availability':
                num_disjoint_paths = constraint.sla_availability.num_disjoint_paths
            elif constraint_kind == 'custom':
                if constraint.custom.constraint_type == 'diversity': is_diverse = True
            elif constraint_kind == 'endpoint_location':
                location = constraint.endpoint_location.location
                if location.WhichOneof('location') == 'gps_position': gps_location_aware = True
            else:
                continue

        LOGGER.debug('num_disjoint_paths={:s}'.format(str(num_disjoint_paths)))
        LOGGER.debug('is_diverse={:s}'.format(str(is_diverse)))
        LOGGER.debug('gps_location_aware={:s}'.format(str(gps_location_aware)))

        if _service is not None and num_disjoint_paths is None and not is_diverse and gps_location_aware:
            LOGGER.debug('  Removing previous service')
            tasks_scheduler = TasksScheduler(self.service_handler_factory)
            tasks_scheduler.compose_from_service(_service, is_delete=True)
            tasks_scheduler.execute_all()

        service = Service()
        service.CopyFrom(request if _service is None else _service)

        if service.service_type == ServiceTypeEnum.SERVICETYPE_UNKNOWN:                     # pylint: disable=no-member
            service.service_type = request.service_type                                     # pylint: disable=no-member
        service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED     # pylint: disable=no-member

        if is_deployed_te() and service.service_type == ServiceTypeEnum.SERVICETYPE_TE:
            # TE service:
            context_client.SetService(request)

            te_service_client = TEServiceClient()
            service_status = te_service_client.RequestLSP(service)

            if service_status.service_status == ServiceStatusEnum.SERVICESTATUS_ACTIVE:
                _service : Optional[Service] = get_service_by_id(
                    context_client, request.service_id, rw_copy=True,
                    include_config_rules=False, include_constraints=False, include_endpoint_ids=False)
                _service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_ACTIVE
                service_id = context_client.SetService(_service)
                return service_id
            else:
                MSG = 'RequestLSP for Service({:s}) returned ServiceStatus({:s})'
                context_uuid = request.service_id.context_id.context_uuid.uuid
                service_uuid = request.service_id.service_uuid.uuid
                service_key = '{:s}/{:s}'.format(context_uuid, service_uuid)
                str_service_status = ServiceStatusEnum.Name(service_status.service_status)
                raise Exception(MSG.format(service_key, str_service_status))

        if is_deployed_e2e_orch() and service.service_type == ServiceTypeEnum.SERVICETYPE_E2E:
            # End-to-End service:
            service_id_with_uuids = context_client.SetService(request)

            service_with_uuids = get_service_by_id(
                context_client, service_id_with_uuids, rw_copy=False,
                include_config_rules=True, include_constraints=True, include_endpoint_ids=True)

            e2e_orch_request = E2EOrchestratorRequest()
            e2e_orch_request.service.CopyFrom(service_with_uuids)

            e2e_orch_client = E2EOrchestratorClient()
            e2e_orch_reply = e2e_orch_client.Compute(e2e_orch_request)

            # Feed TaskScheduler with this end-to-end orchestrator reply. TaskScheduler identifies
            # inter-dependencies among the services and connections retrieved and produces a
            # schedule of tasks (an ordered list of tasks to be executed) to implement the
            # requested create/update operation.
            tasks_scheduler = TasksScheduler(self.service_handler_factory)
            # e2e_orch_reply should be compatible with pathcomp_reply
            # TODO: if we extend e2e_orch_reply, implement method TasksScheduler::compose_from_e2eorchreply()
            tasks_scheduler.compose_from_pathcompreply(e2e_orch_reply, is_delete=False)
            tasks_scheduler.execute_all()
            return service_with_uuids.service_id


        # Normal service
        del service.service_endpoint_ids[:] # pylint: disable=no-member
        for endpoint_id in request.service_endpoint_ids:
            service.service_endpoint_ids.add().CopyFrom(endpoint_id)    # pylint: disable=no-member

        device_list = context_client.ListDevices(Empty())

        LOGGER.debug('[before] request={:s}'.format(grpc_message_to_json_string(request)))
        for constraint in request.service_constraints:
            if constraint.action == ConstraintActionEnum.CONSTRAINTACTION_UNDEFINED:
                # Field action is new; assume if not set, it means SET
                constraint.action = ConstraintActionEnum.CONSTRAINTACTION_SET

            if constraint.action != ConstraintActionEnum.CONSTRAINTACTION_SET: continue
            if constraint.WhichOneof('constraint') != 'endpoint_location': continue
            if constraint.endpoint_location.HasField('endpoint_id'): continue

            service_location = constraint.endpoint_location.location
            distances = {}
            for device in device_list.devices:
                for endpoint in device.device_endpoints:
                    if not endpoint.endpoint_location.HasField('gps_position'): continue
                    distance = gps_distance(service_location.gps_position, endpoint.endpoint_location.gps_position)
                    distances[distance] = endpoint.endpoint_id

            closer_endpoint_id = distances[min(distances)]
            constraint.endpoint_location.endpoint_id.CopyFrom(closer_endpoint_id)

            service_endpoint_ids = [
                endpoint_id.endpoint_uuid
                for endpoint_id in service.service_endpoint_ids
            ]
            if closer_endpoint_id not in service_endpoint_ids:
                service.service_endpoint_ids.append(closer_endpoint_id)

        LOGGER.debug('[after] request={:s}'.format(grpc_message_to_json_string(request)))
        LOGGER.debug('[after] service={:s}'.format(grpc_message_to_json_string(service)))

        del service.service_constraints[:]  # pylint: disable=no-member
        for constraint in request.service_constraints:
            service.service_constraints.add().CopyFrom(constraint)  # pylint: disable=no-member

        del service.service_config.config_rules[:]  # pylint: disable=no-member
        for config_rule in request.service_config.config_rules:
            service.service_config.config_rules.add().CopyFrom(config_rule) # pylint: disable=no-member

        service_id_with_uuids = context_client.SetService(service)

        # PathComp requires endpoints, constraints and config rules
        service_with_uuids = get_service_by_id(
            context_client, service_id_with_uuids, rw_copy=False,
            include_config_rules=True, include_constraints=True, include_endpoint_ids=True)

        num_disjoint_paths = 1 if num_disjoint_paths is None or num_disjoint_paths == 0 else num_disjoint_paths
        num_expected_endpoints = num_disjoint_paths * 2

        tasks_scheduler = TasksScheduler(self.service_handler_factory)

        if is_deployed_optical() and service.service_type == ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY:
            context_id_x = json_context_id(DEFAULT_CONTEXT_NAME)
            topology_id_x = json_topology_id(
                DEFAULT_TOPOLOGY_NAME, context_id_x)
            topology_details = context_client.GetTopologyDetails(
                TopologyId(**topology_id_x))

            refresh_opticalcontroller(topology_id_x)
            # devices = get_devices_in_topology(context_client, TopologyId(**topology_id_x), ContextId(**context_id_x))
            devices = topology_details.devices
            context_uuid_x = topology_details.topology_id.context_id.context_uuid.uuid
            topology_uuid_x = topology_details.topology_id.topology_uuid.uuid

            device_names : Dict[str, str] = dict()
            for device in devices:
                device_uuid = device.device_id.device_uuid.uuid
                device_names[device_uuid] = device.name
                device_names[device.name] = device.name

            devs = []
            ports = []
            for endpoint_id in service.service_endpoint_ids:
                endpoint_device_uuid = endpoint_id.device_id.device_uuid.uuid
                if "." in endpoint_device_uuid:
                    endpoint_device_name = endpoint_device_uuid
                else:
                    endpoint_device_name = device_names[endpoint_device_uuid]
                devs.append(endpoint_device_name)
                ports.append(endpoint_id.endpoint_uuid.uuid)

            src = devs[0]
            dst = devs[1]
            bidir = None
            ob_band = None
            oc_type = 1
            bitrate = 100
            for constraint in service.service_constraints:
                if "bandwidth" in constraint.custom.constraint_type:
                    bitrate = int(float(constraint.custom.constraint_value))
                elif "bidirectionality" in constraint.custom.constraint_type:
                    bidir = int(constraint.custom.constraint_value)
                elif "optical-band-width" in constraint.custom.constraint_type:
                    ob_band = int(constraint.custom.constraint_value)
                elif "type" in constraint.custom.constraint_type:
                    oc_type = OpticalServiceType(str(constraint.custom.constraint_value))

            reply_txt = ""
            # to get the reply form the optical module
            #multi-granular
            if oc_type == 1:
                reply_txt = add_flex_lightpath(src, dst, bitrate, bidir, ob_band)
            elif oc_type == 2:
                reply_txt = add_lightpath(src, dst, bitrate, bidir)
            else:
                reply_txt = add_flex_lightpath(src, dst, bitrate, bidir, ob_band)

            reply_json = json.loads(reply_txt)
            LOGGER.debug('[optical] reply_json[{:s}]={:s}'.format(str(type(reply_json)), str(reply_json)))
            optical_band_txt = ""

            if "new_optical_band" in reply_json.keys():
                if reply_json["new_optical_band"] == 1:
                    if reply_json["parent_opt_band"]:
                        if "parent_opt_band" in reply_json.keys():
                            parent_ob = reply_json["parent_opt_band"]
                            LOGGER.debug('Parent optical-band={}'.format(parent_ob))
                            optical_band_txt = get_optical_band(parent_ob)

                        else:
                            LOGGER.debug('expected optical band not found')
                    else:
                        LOGGER.debug('expected optical band not found')
                elif reply_json["new_optical_band"]==2 :
                    parent_ob = reply_json["parent_opt_band"]
                    LOGGER.debug('Parent optical-band={}'.format(parent_ob))
                    optical_band_txt = get_optical_band(parent_ob)


                    service_expansion= extend_optical_band(reply_json,optical_band_txt)
                    tasks_scheduler.compose_from_service_expansion(service_expansion)


                else:
                    LOGGER.debug('Using existing optical band')
            else:
                LOGGER.debug('Using existing optical band')

            if reply_txt is not None:
                optical_reply = adapt_reply(
                    devices, _service, reply_json, context_uuid_x, topology_uuid_x, optical_band_txt
                )

                tasks_scheduler.compose_from_opticalcontroller_reply(
                    optical_reply, is_delete=False)
        else:
            if len(service_with_uuids.service_endpoint_ids) >= num_expected_endpoints:
                pathcomp_request = PathCompRequest()
                pathcomp_request.services.append(service_with_uuids)    # pylint: disable=no-member

                if num_disjoint_paths is None or num_disjoint_paths in {0, 1} :
                    pathcomp_request.shortest_path.Clear()              # pylint: disable=no-member
                else:
                    pathcomp_request.k_disjoint_path.num_disjoint = num_disjoint_paths  # pylint: disable=no-member

                pathcomp = PathCompClient()
                pathcomp_reply = pathcomp.Compute(pathcomp_request)
                pathcomp.close()

                # Feed TaskScheduler with this path computation reply. TaskScheduler identifies inter-dependencies among
                # the services and connections retrieved and produces a schedule of tasks (an ordered list of tasks to be
                # executed) to implement the requested create/update operation.
                tasks_scheduler.compose_from_pathcompreply(pathcomp_reply, is_delete=False)

        tasks_scheduler.execute_all()
        return service_with_uuids.service_id

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteService(self, request : ServiceId, context : grpc.ServicerContext) -> Empty:
        context_client = ContextClient()

        # Set service status to "SERVICESTATUS_PENDING_REMOVAL" to ensure rest of components are aware the service is
        # being modified.
        service : Optional[Service] = get_service_by_id(context_client, request, rw_copy=True)
        if service is None: raise Exception('Service({:s}) not found'.format(grpc_message_to_json_string(request)))
        # pylint: disable=no-member
        service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PENDING_REMOVAL

        if service.service_type == ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY:
             service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_ACTIVE

        context_client.SetService(service)

        if is_deployed_te() and service.service_type == ServiceTypeEnum.SERVICETYPE_TE:
            # TE service
            te_service_client = TEServiceClient()
            te_service_client.DeleteLSP(request)
            context_client.RemoveService(request)
            return Empty()

        if is_deployed_optical() and service.service_type == ServiceTypeEnum.SERVICETYPE_OPTICAL_CONNECTIVITY:
            params = {
                "src"     : None,
                "dst"     : None,
                "bitrate" : None,
                'ob_id'   : None,
                'bidir'   : None,
                'flow_id' : None
            }
            devs = []

            context_id_x = json_context_id(DEFAULT_CONTEXT_NAME)
            topology_id_x = json_topology_id(
                DEFAULT_TOPOLOGY_NAME, context_id_x)
            topology_details = context_client.GetTopologyDetails(
                TopologyId(**topology_id_x))
            devices = topology_details.devices
            for endpoint_id in service.service_endpoint_ids:
                devs.append(endpoint_id.device_id.device_uuid.uuid)
            src = get_device_name_from_uuid(devices, devs[0])
            dst = get_device_name_from_uuid(devices, devs[1])
            bitrate = 100
            bidir = 0
            oc_type = 1
            for constraint in service.service_constraints:
                if "bandwidth" in constraint.custom.constraint_type:
                    bitrate = int(float(constraint.custom.constraint_value))
                if "type" in constraint.custom.constraint_type:
                    oc_type = OpticalServiceType(str(constraint.custom.constraint_value))
            '''
            if service.service_constraints:
                bitrate = int(float(
                    service.service_constraints[0].custom.constraint_value
            ))
            '''
            #multi-granular
            if oc_type == 1:
                if len(service.service_config.config_rules) > 0:
                    c_rules_dict = json.loads(
                        service.service_config.config_rules[0].custom.resource_value
                    )
                    ob_id = None
                    flow_id = None
                    if "ob_id" in c_rules_dict:
                        ob_id = c_rules_dict["ob_id"]
                    if ("flow_id" in c_rules_dict):
                        flow_id = c_rules_dict["flow_id"]
                        #if ("ob_id" in c_rules_dict):
                        #    ob_id = c_rules_dict["ob_id"]
                    params['bitrate'] = bitrate
                    params['dst'    ] = dst
                    params['src'    ] = src
                    params['ob_id'  ] = ob_id
                    params['flow_id'] = flow_id
                    params['bidir'  ] = bidir


                tasks_scheduler = TasksScheduler(self.service_handler_factory)
                tasks_scheduler.compose_from_optical_service(service, params=params, is_delete=True)
                tasks_scheduler.execute_all()
                return Empty()
            elif oc_type ==2 :

                if len(service.service_config.config_rules) > 0:
                    c_rules_dict = json.loads(
                    service.service_config.config_rules[0].custom.resource_value)
                    ob_id=None
                    flow_id=None

                    if ("flow_id" in c_rules_dict):
                        flow_id = c_rules_dict["flow_id"]
                        #if ("ob_id" in c_rules_dict):
                        #    ob_id = c_rules_dict["ob_id"]
                    params['bitrate']=bitrate
                    params['dst']=dst
                    params['src']=src
                    params['ob_id']=ob_id
                    params['flow_id']=flow_id
                    params['bidir'] = bidir


                tasks_scheduler = TasksScheduler(self.service_handler_factory)
                tasks_scheduler.compose_from_optical_service(service, params=params, is_delete=True)
                tasks_scheduler.execute_all()
                return Empty()

        # Normal service
        # Feed TaskScheduler with this service and the sub-services and sub-connections related to this service.
        # TaskScheduler identifies inter-dependencies among them and produces a schedule of tasks (an ordered list of
        # tasks to be executed) to implement the requested delete operation.
        tasks_scheduler = TasksScheduler(self.service_handler_factory)
        tasks_scheduler.compose_from_service(service, is_delete=True)
        tasks_scheduler.execute_all()
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RecomputeConnections(self, request : Service, context : grpc.ServicerContext) -> Empty:
        if len(request.service_endpoint_ids) > 0:
            raise NotImplementedException('update-endpoints')

        if len(request.service_constraints) > 0:
            raise NotImplementedException('update-constraints')

        if len(request.service_config.config_rules) > 0:
            raise NotImplementedException('update-config-rules')

        context_client = ContextClient()

        updated_service : Optional[Service] = get_service_by_id(
            context_client, request.service_id, rw_copy=True,
            include_config_rules=False, include_constraints=False, include_endpoint_ids=False)

        if updated_service is None:
            raise NotFoundException('service', request.service_id.service_uuid.uuid)

        # pylint: disable=no-member
        if updated_service.service_type == ServiceTypeEnum.SERVICETYPE_UNKNOWN:
            raise InvalidArgumentException(
                'request.service_type', ServiceTypeEnum.Name(updated_service.service_type)
            )

        # Set service status to "SERVICESTATUS_UPDATING" to ensure rest of components are aware the service is
        # being modified.
        # pylint: disable=no-member
        updated_service.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_UPDATING

        # Update endpoints
        # pylint: disable=no-member
        #del updated_service.service_endpoint_ids[:]
        #updated_service.service_endpoint_ids.extend(request.service_endpoint_ids)

        # Update constraints
        # pylint: disable=no-member
        #del updated_service.service_constraints[:]
        #updated_service.service_constraints.extend(request.service_constraints)

        # Update config rules
        # pylint: disable=no-member
        #del updated_service.service_config.config_rules[:]
        #updated_service.service_config.config_rules.extend(request.service_config.config_rules)

        updated_service_id_with_uuids = context_client.SetService(updated_service)

        # PathComp requires endpoints, constraints and config rules
        updated_service_with_uuids = get_service_by_id(
            context_client, updated_service_id_with_uuids, rw_copy=True,
            include_config_rules=True, include_constraints=True, include_endpoint_ids=True)

        # Get active connection
        connections = context_client.ListConnections(updated_service_id_with_uuids)
        if len(connections.connections) == 0:
            MSG = 'Service({:s}) has no connections'
            str_service_id = grpc_message_to_json_string(updated_service_id_with_uuids)
            str_extra_details = MSG.format(str_service_id)
            raise NotImplementedException('service-with-no-connections', extra_details=str_extra_details)
        if len(connections.connections) > 1:
            MSG = 'Service({:s}) has multiple ({:d}) connections({:s})'
            str_service_id = grpc_message_to_json_string(updated_service_id_with_uuids)
            num_connections = len(connections.connections)
            str_connections = grpc_message_to_json_string(connections)
            str_extra_details = MSG.format(str_service_id, num_connections, str_connections)
            raise NotImplementedException('service-with-multiple-connections', extra_details=str_extra_details)

        old_connection = connections.connections[0]
        if len(old_connection.sub_service_ids) > 0:
            MSG = 'Service({:s})/Connection({:s}) has sub-services: {:s}'
            str_service_id = grpc_message_to_json_string(updated_service_id_with_uuids)
            str_connection_id = grpc_message_to_json_string(old_connection.connection_id)
            str_connection = grpc_message_to_json_string(old_connection)
            str_extra_details = MSG.format(str_service_id, str_connection_id, str_connection)
            raise NotImplementedException('service-connection-with-subservices', extra_details=str_extra_details)

        # Find alternative connections
        # pylint: disable=no-member
        pathcomp_request = PathCompRequest()
        pathcomp_request.services.append(updated_service_with_uuids)
        #pathcomp_request.k_disjoint_path.num_disjoint = 100
        pathcomp_request.k_shortest_path.k_inspection = 100
        pathcomp_request.k_shortest_path.k_return = 3

        LOGGER.debug('pathcomp_request={:s}'.format(grpc_message_to_json_string(pathcomp_request)))
        pathcomp = PathCompClient()
        pathcomp_reply = pathcomp.Compute(pathcomp_request)
        pathcomp.close()
        LOGGER.debug('pathcomp_reply={:s}'.format(grpc_message_to_json_string(pathcomp_reply)))

        if len(pathcomp_reply.services) == 0:
            MSG = 'KDisjointPath reported no services for Service({:s}): {:s}'
            str_service_id = grpc_message_to_json_string(updated_service_id_with_uuids)
            str_pathcomp_reply = grpc_message_to_json_string(pathcomp_reply)
            str_extra_details = MSG.format(str_service_id, str_pathcomp_reply)
            raise NotImplementedException('kdisjointpath-no-services', extra_details=str_extra_details)

        if len(pathcomp_reply.services) > 1:
            MSG = 'KDisjointPath reported subservices for Service({:s}): {:s}'
            str_service_id = grpc_message_to_json_string(updated_service_id_with_uuids)
            str_pathcomp_reply = grpc_message_to_json_string(pathcomp_reply)
            str_extra_details = MSG.format(str_service_id, str_pathcomp_reply)
            raise NotImplementedException('kdisjointpath-subservices', extra_details=str_extra_details)

        if len(pathcomp_reply.connections) == 0:
            MSG = 'KDisjointPath reported no connections for Service({:s}): {:s}'
            str_service_id = grpc_message_to_json_string(updated_service_id_with_uuids)
            str_pathcomp_reply = grpc_message_to_json_string(pathcomp_reply)
            str_extra_details = MSG.format(str_service_id, str_pathcomp_reply)
            raise NotImplementedException('kdisjointpath-no-connections', extra_details=str_extra_details)

        # compute a string representing the old connection
        str_old_connection = connection_to_string(old_connection)

        LOGGER.debug('old_connection={:s}'.format(grpc_message_to_json_string(old_connection)))

        candidate_new_connections = list()
        for candidate_new_connection in pathcomp_reply.connections:
            str_candidate_new_connection = connection_to_string(candidate_new_connection)
            if str_candidate_new_connection == str_old_connection: continue
            candidate_new_connections.append(candidate_new_connection)

        if len(candidate_new_connections) == 0:
            MSG = 'Unable to find a new suitable path: pathcomp_request={:s} pathcomp_reply={:s} old_connection={:s}'
            str_pathcomp_request = grpc_message_to_json_string(pathcomp_request)
            str_pathcomp_reply = grpc_message_to_json_string(pathcomp_reply)
            str_old_connection = grpc_message_to_json_string(old_connection)
            extra_details = MSG.format(str_pathcomp_request, str_pathcomp_reply, str_old_connection)
            raise OperationFailedException('no-new-path-found', extra_details=extra_details)

        str_candidate_new_connections = [
            grpc_message_to_json_string(candidate_new_connection)
            for candidate_new_connection in candidate_new_connections
        ]
        LOGGER.debug('candidate_new_connections={:s}'.format(str(str_candidate_new_connections)))

        new_connection = random.choice(candidate_new_connections)
        LOGGER.debug('new_connection={:s}'.format(grpc_message_to_json_string(new_connection)))

        # Change UUID of new connection to prevent collisions
        tmp_connection = Connection()
        tmp_connection.CopyFrom(new_connection)
        tmp_connection.connection_id.connection_uuid.uuid = str(uuid.uuid4())
        new_connection = tmp_connection

        # Feed TaskScheduler with the service to update, the old connection to
        # deconfigure and the new connection to configure. It will produce a
        # schedule of tasks (an ordered list of tasks to be executed) to
        # implement the requested changes.
        tasks_scheduler = TasksScheduler(self.service_handler_factory)
        tasks_scheduler.compose_service_connection_update(
            updated_service_with_uuids, old_connection, new_connection)
        tasks_scheduler.execute_all()

        return Empty()
