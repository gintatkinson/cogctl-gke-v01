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


import json, logging, uuid
from typing import Any, Dict, List, Optional, Tuple, Union
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.proto.context_pb2 import ConfigRule, DeviceId, Service
from common.proto.qkd_app_pb2 import App, AppId, QKDAppStatusEnum, QKDAppTypesEnum
from common.proto.context_pb2 import ContextId, Uuid
from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import json_device_id
from common.type_checkers.Checkers import chk_type
from service.service.service_handler_api.Tools import get_device_endpoint_uuids, get_endpoint_matching
from service.service.service_handler_api._ServiceHandler import _ServiceHandler
from service.service.service_handler_api.SettingsHandler import SettingsHandler
from service.service.task_scheduler.TaskExecutor import TaskExecutor

LOGGER = logging.getLogger(__name__)

def get_endpoint_name_by_uuid(device, uuid):
    for device_endpoint in device.device_endpoints:
        if device_endpoint.endpoint_id.endpoint_uuid.uuid == uuid:
            return device_endpoint.name
    return None

class QKDServiceHandler(_ServiceHandler):
    def __init__(   # pylint: disable=super-init-not-called
        self, service : Service, task_executor : TaskExecutor, **settings
    ) -> None:
        self.__service = service
        self.__task_executor = task_executor
        self.__settings_handler = SettingsHandler(service.service_config, **settings)
        self.qkd_app_client = task_executor._qkd_app_client  # Initialize qkd_app_client


    # Optare: This function is where the service is created
    # Optare: It already receives the path provided by pathcomp in endpoints variable
    # Optare: It then checks for each respective QKD Node and requests SBI to inform of the new connection
    # Optare: It also requests app module for a creation of internal service if the service is virtual
    def SetEndpoint(
        self, endpoints : List[Tuple[str, str, Optional[str]]],
        connection_uuid : Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        chk_type('endpoints', endpoints, list)
        if len(endpoints) < 2 or len(endpoints) % 2: return []

        LOGGER.info('Endpoints: ' + str(endpoints))
        

        service_uuid = self.__service.service_id.service_uuid.uuid
        settings = self.__settings_handler.get('/settings')

        context_uuid = self.__service.service_id.context_id.context_uuid.uuid

        results = []
        try:

            if len(endpoints) > 4:
                is_virtual = True
            else:
                is_virtual = False
            
            devices    = []
            qkdn_ids   = []
            interfaces = []
            links      = []

            # Optare: First a big iteration through all devices is done in order to obtain all information needed for the whole operation
            # Optare: This is a way to minimize time of operation. Otherwise it would require many O(N) operations. This way we can reduce it to one

            # Populate devices and QKDN ids
            for idx, endpoint in enumerate(endpoints[::2]):
                device_uuid, endpoint_left_uuid = get_device_endpoint_uuids(endpoint)
                _, endpoint_right_uuid = get_device_endpoint_uuids(endpoints[2 * idx + 1])

                device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
                devices.append(device)
                interfaces.append([0,0])
                links.append([])

                endpoint_left =  get_endpoint_name_by_uuid(device, endpoint_left_uuid) if idx > 0 else None
                endpoint_right = get_endpoint_name_by_uuid(device, endpoint_right_uuid) if 2 * idx + 2 < len(endpoints) else None

                for config_rule in device.device_config.config_rules:
                    resource_key = config_rule.custom.resource_key

                    if resource_key == '__node__':
                        value = json.loads(config_rule.custom.resource_value)
                        qkdn_ids.append(value['qkdn_id'])
                    
                    elif resource_key.startswith('/interface'):
                        value = json.loads(config_rule.custom.resource_value)
                        try:
                            endpoint_str = value['qkdi_att_point']['uuid']
                            LOGGER.info("A: " + str(endpoint_str) + "....." + str(endpoint_left) + "....." + str(endpoint_right))

                            if endpoint_str == endpoint_left:
                                interfaces[idx][0] = value['qkdi_id']
                            elif endpoint_str == endpoint_right:
                                interfaces[idx][1] = value['qkdi_id']
                        except KeyError:
                            pass
                    
                    elif resource_key.startswith('/link'):
                        value = json.loads(config_rule.custom.resource_value)
                        links[idx].append(( value['uuid'],
                            (value['src_qkdn_id'], value['src_interface_id']), 
                            (value['dst_qkdn_id'], value['dst_interface_id'])
                        ))


            LOGGER.info("IFs: " + str(interfaces))
            LOGGER.info("Links: " + str(links))
            LOGGER.info("context_: " + context_uuid)


            # Optare: From here now is where the work is really done. It iterates over every device in use for the service (ordered)

            src_device_uuid, src_endpoint_uuid = get_device_endpoint_uuids(endpoints[0])
            src_device = devices[0]
            src_endpoint = get_endpoint_matching(src_device, src_endpoint_uuid)

            dst_device_uuid, dst_endpoint_uuid = get_device_endpoint_uuids(endpoints[-1])
            dst_device = devices[-1]
            dst_endpoint = get_endpoint_matching(dst_device, dst_endpoint_uuid)

            src_qkdn_id = qkdn_ids[0]
            dst_qkdn_id = qkdn_ids[-1]

            src_interface_id = interfaces[0][1]
            dst_interface_id = interfaces[-1][0]

            service_qkdl_id_src_dst = str(uuid.uuid4())
            service_qkdl_id_dst_src = str(uuid.uuid4())

            
            for idx, device in enumerate(devices):

                # Even though we always create them together. There is a chance the admin deletes one of the rules manually
                phys_qkdl_id_right = None if idx == (len(devices) - 1) else '' # None == impossible
                phys_qkdl_id_left = None if idx == 0 else '' # None == impossible

                for link_uuid, link_src, link_dst in links[idx]:
                    qkdn_link_src, qkdn_interface_src = link_src
                    qkdn_link_dst, qkdn_interface_dst = link_dst

                    if phys_qkdl_id_right == '' and \
                        qkdn_link_src == qkdn_ids[idx] and qkdn_interface_src == interfaces[idx][1] and \
                        qkdn_link_dst[idx+1] and qkdn_interface_dst == interfaces[idx+1][0]:
                        phys_qkdl_id_right = link_uuid


                    if phys_qkdl_id_left == '' and \
                        qkdn_link_src == qkdn_ids[idx] and qkdn_interface_src == interfaces[idx][0] and \
                        qkdn_link_dst[idx-1] and qkdn_interface_dst == interfaces[idx-1][1]:
                        phys_qkdl_id_left = link_uuid


                # Optare: Before adding information to config_rules you have to delete the list first otherwise old content will be called again
                del device.device_config.config_rules[:]


                if phys_qkdl_id_right:
                    if not is_virtual:
                        service_qkdl_id_src_dst = phys_qkdl_id_right

                elif phys_qkdl_id_right == '':
                    qkdl_id_src_dst = str(uuid.uuid4()) if is_virtual else service_qkdl_id_src_dst

                    json_config_rule = json_config_rule_set('/link/link[{:s}]'.format(qkdl_id_src_dst), {
                        'uuid'               : qkdl_id_src_dst,
                        'type'               : 'DIRECT',
                        'src_qkdn_id'        : qkdn_ids[idx],
                        'src_interface_id'   : interfaces[idx][1],
                        'dst_qkdn_id'        : qkdn_ids[idx+1],
                        'dst_interface_id'   : interfaces[idx+1][0],
                    })

                    device.device_config.config_rules.append(ConfigRule(**json_config_rule))


                if phys_qkdl_id_left:
                    if not is_virtual:
                        service_qkdl_id_dst_src = phys_qkdl_id_left

                elif phys_qkdl_id_left == '':
                    qkdl_id_dst_src = str(uuid.uuid4()) if is_virtual else service_qkdl_id_dst_src

                    json_config_rule = json_config_rule_set('/link/link[{:s}]'.format(qkdl_id_dst_src), {
                        'uuid'               : qkdl_id_dst_src,
                        'type'               : 'DIRECT',
                        'src_qkdn_id'        : qkdn_ids[idx],
                        'src_interface_id'   : interfaces[idx][0],
                        'dst_qkdn_id'        : qkdn_ids[idx-1],
                        'dst_interface_id'   : interfaces[idx-1][1],
                    })

                    device.device_config.config_rules.append(ConfigRule(**json_config_rule))
                


                if is_virtual:
                    if idx < len(qkdn_ids) - 1:
                        json_config_rule = json_config_rule_set('/link/link[{:s}]'.format(service_qkdl_id_src_dst), {
                            'uuid'               : service_qkdl_id_src_dst,
                            'type'               : 'VIRTUAL',
                            'src_qkdn_id'        : src_qkdn_id,
                            'src_interface_id'   : src_interface_id,
                            'dst_qkdn_id'        : dst_qkdn_id,
                            'dst_interface_id'   : dst_interface_id,
                            'virt_prev_hop'      : qkdn_ids[idx-1] if idx > 0 else None,
                            'virt_next_hops'     : qkdn_ids[idx+1:],
                            'virt_bandwidth'     : 0,
                        })

                        device.device_config.config_rules.append(ConfigRule(**json_config_rule))

                    if idx > 0:
                        json_config_rule = json_config_rule_set('/link/link[{:s}]'.format(service_qkdl_id_dst_src), {
                            'uuid'               : service_qkdl_id_dst_src,
                            'type'               : 'VIRTUAL',
                            'src_qkdn_id'        : dst_qkdn_id,
                            'src_interface_id'   : dst_interface_id,
                            'dst_qkdn_id'        : src_qkdn_id,
                            'dst_interface_id'   : src_interface_id,
                            'virt_prev_hop'      : qkdn_ids[idx+1] if idx < len(qkdn_ids) - 1 else None,
                            'virt_next_hops'     : qkdn_ids[idx-1::-1],
                            'virt_bandwidth'     : 0,
                        })

                        device.device_config.config_rules.append(ConfigRule(**json_config_rule))



                json_config_rule = json_config_rule_set('/services/service[{:s}]'.format(service_uuid), {
                    'uuid'               : service_uuid,
                    'qkdl_id_src_dst'    : service_qkdl_id_src_dst,
                    'qkdl_id_dst_src'    : service_qkdl_id_dst_src,
                })

                device.device_config.config_rules.append(ConfigRule(**json_config_rule))
                self.__task_executor.configure_device(device)


            if is_virtual:

                # Register App
                internal_app_src_dst = {
                    'app_id': {'context_id': {'context_uuid': {'uuid': context_uuid}}, 'app_uuid': {'uuid': str(uuid.uuid4())}},
                    'app_status': QKDAppStatusEnum.QKDAPPSTATUS_ON,
                    'app_type': QKDAppTypesEnum.QKDAPPTYPES_INTERNAL,
                    'server_app_id': '',
                    'client_app_id': [],
                    'backing_qkdl_id': [{'qkdl_uuid': {'uuid': service_qkdl_id_src_dst}}],
                    'local_device_id': src_device.device_id,
                    'remote_device_id': dst_device.device_id,
                }

                self.__task_executor.register_qkd_app(App(**internal_app_src_dst))
                

                # Register App
                internal_app_dst_src = {
                    'app_id': {'context_id': {'context_uuid': {'uuid': context_uuid}}, 'app_uuid': {'uuid': str(uuid.uuid4())}},
                    'app_status': QKDAppStatusEnum.QKDAPPSTATUS_ON,
                    'app_type': QKDAppTypesEnum.QKDAPPTYPES_INTERNAL,
                    'server_app_id': '',
                    'client_app_id': [],
                    'backing_qkdl_id': [{'qkdl_uuid': {'uuid': service_qkdl_id_dst_src}}],
                    'local_device_id': dst_device.device_id,
                    'remote_device_id': src_device.device_id,
                }

                self.__task_executor.register_qkd_app(App(**internal_app_dst_src))

            results.append(True)
        except Exception as e: # pylint: disable=broad-except
            LOGGER.exception('Unable to SetEndpoint for Service({:s})'.format(str(service_uuid)))
            results.append(e)

        return results

    # Optare: This will be to delete a service
    def DeleteEndpoint(
        self, endpoints: List[Tuple[str, str, Optional[str]]], connection_uuid: Optional[str] = None
    ) -> List[Union[bool, Exception]]:
        chk_type('endpoints', endpoints, list)
        if len(endpoints) == 0:
            return []

        LOGGER.info(f'Deleting Endpoints: {endpoints}')
        LOGGER.info(f'Connection UUID: {connection_uuid}')

        service_uuid = self.__service.service_id.service_uuid.uuid
        context_uuid = self.__service.service_id.context_id.context_uuid.uuid
        LOGGER.info(f'Service UUID: {service_uuid}, Context UUID: {context_uuid}')

        results = []
        apps = list()  # Initialize apps as an empty list, in case fetching fails
        try:
            # Initialize device lists and QKDN IDs
            devices = []
            qkdn_ids = []
            interfaces = []
            links = []

            # Populate devices and QKDN ids from endpoints
            for idx, endpoint in enumerate(endpoints[::2]):
                device_uuid, endpoint_left_uuid = get_device_endpoint_uuids(endpoint)
                _, endpoint_right_uuid = get_device_endpoint_uuids(endpoints[2 * idx + 1])

                device = self.__task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
                LOGGER.info(f'Device: {device}, Endpoint Left: {endpoint_left_uuid}, Endpoint Right: {endpoint_right_uuid}')

                devices.append(device)
                interfaces.append([0, 0])
                links.append([])

                for config_rule in device.device_config.config_rules:
                    resource_key = config_rule.custom.resource_key

                    if resource_key == '__node__':
                        value = json.loads(config_rule.custom.resource_value)
                        qkdn_ids.append(value['qkdn_id'])

                    elif resource_key.startswith('/interface'):
                        value = json.loads(config_rule.custom.resource_value)
                        try:
                            endpoint_str = value['qkdi_att_point']['uuid']
                            if endpoint_str == endpoint_left_uuid:
                                interfaces[idx][0] = value['qkdi_id']
                            elif endpoint_str == endpoint_right_uuid:
                                interfaces[idx][1] = value['qkdi_id']
                        except KeyError:
                            pass

                    elif resource_key.startswith('/link'):
                        value = json.loads(config_rule.custom.resource_value)
                        links[idx].append((
                            value['uuid'],
                            (value['src_qkdn_id'], value['src_interface_id']),
                            (value['dst_qkdn_id'], value['dst_interface_id'])
                        ))

            LOGGER.info(f'Interfaces: {interfaces}, Links: {links}, QKDN IDs: {qkdn_ids}')

            # Fetch the related apps for the service using the same pattern as in routes.py
            try:
                context_id = ContextId(context_uuid=Uuid(uuid=context_uuid))
                apps_response = self.__task_executor._qkd_app_client.ListApps(context_id)
                apps = apps_response.apps  # Assign the apps to the list, if successful
                LOGGER.info(f"Apps retrieved: {apps}")
            except grpc.RpcError as e:
                LOGGER.error(f"gRPC error while fetching apps: {e.details()}")
                if e.code() != grpc.StatusCode.NOT_FOUND: 
                    raise
                apps = list()  # If an error occurs, ensure `apps` is still an empty list

            # Filter related internal apps
            related_apps = [
                app for app in apps
                if app.server_app_id == service_uuid and app.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL
            ]

            # Log each app's details
            for app in related_apps:
                LOGGER.info(f"App ID: {app.app_id.app_uuid.uuid}, Status: {app.app_status}")

            # Update each app status to DISCONNECTED before deletion
            for app in related_apps:
                self.__task_executor.update_qkd_app_status(app, QKDAppStatusEnum.QKDAPPSTATUS_DISCONNECTED)

            results.append(True)

        except Exception as e:  # pylint: disable=broad-except
            LOGGER.error(f"Failed to delete QKD service: {str(e)}")
            results.append(e)

        return results

    def fetch_related_internal_apps(self, context_uuid: str, service_uuid: str) -> List[App]:
        try:
            context_id = ContextId(context_uuid=Uuid(uuid=context_uuid))
            apps_response = self.qkd_app_client.ListApps(context_id)
            
            # Log the apps retrieved to ensure they exist and have a status
            LOGGER.info(f"Apps retrieved: {apps_response.apps}")
            
            internal_apps = [
                app for app in apps_response.apps
                if app.app_type == QKDAppTypesEnum.QKDAPPTYPES_INTERNAL 
                and app.server_app_id == service_uuid
                and app.app_status == QKDAppStatusEnum.ACTIVE  # Ensure you are checking status
            ]
            
            LOGGER.info(f"Filtered internal apps: {internal_apps}")
            return internal_apps

        except Exception as e:
            LOGGER.error(f"Error fetching related internal apps: {e}")
            return []

    # Optare: Can be ingored. It's in case if a service is later updated. Not required to proper functioning

    def SetConstraint(self, constraints: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
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
        results = []
        try:
            for constraint_type, constraint_value in constraints:
                LOGGER.info(f"Setting constraint: {constraint_type} with value: {constraint_value}")

                # Assuming you store constraints as part of service config rules
                constraint_key = f"/constraints/{constraint_type}"
                json_config_rule = json_config_rule_set(constraint_key, constraint_value)

                # Apply the configuration rule to the service
                self.__service.service_config.config_rules.append(ConfigRule(**json_config_rule))

            # Reconfigure the service with new constraints
            self.__task_executor.configure_service(self.__service)

            results.append(True)

        except Exception as e:
            LOGGER.error(f"Failed to set constraints: {str(e)}")
            results.append(e)

        return results

    def DeleteConstraint(self, constraints: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
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
        results = []
        try:
            for constraint_type, _ in constraints:
                LOGGER.info(f"Deleting constraint: {constraint_type}")

                # Remove the constraint from the service config rules
                constraint_key = f"/constraints/{constraint_type}"
                json_config_rule = json_config_rule_delete(constraint_key)

                for rule in self.__service.service_config.config_rules:
                    if rule.custom.resource_key == constraint_key:
                        self.__service.service_config.config_rules.remove(rule)

            # Reconfigure the service after removing constraints
            self.__task_executor.configure_service(self.__service)

            results.append(True)

        except Exception as e:
            LOGGER.error(f"Failed to delete constraints: {str(e)}")
            results.append(e)

        return results

    def SetConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
        """ Create/Update configuration for a list of service resources.
            Parameters:
                resources: List[Tuple[str, Any]]
                    List of tuples, each containing a resource_key pointing to
                    the resource to be modified, and a resource_value containing
                    the new value to be set.
            Returns:
                results: List[Union[bool, Exception]]
                    List of results for resource key changes requested.
                    Return values must be in the same order as the requested
                    resource keys. If a resource is properly set, True must be
                    returned; otherwise, the Exception that is raised during
                    the processing must be returned.
        """
        results = []
        try:
            for resource_key, resource_value in resources:
                LOGGER.info(f"Setting config: {resource_key} with value: {resource_value}")

                json_config_rule = json_config_rule_set(resource_key, resource_value)

                # Apply the configuration rule to the service
                self.__service.service_config.config_rules.append(ConfigRule(**json_config_rule))

            # Reconfigure the service with new configurations
            self.__task_executor.configure_service(self.__service)

            results.append(True)

        except Exception as e:
            LOGGER.error(f"Failed to set config: {str(e)}")
            results.append(e)

        return results

    def DeleteConfig(self, resources: List[Tuple[str, Any]]) -> List[Union[bool, Exception]]:
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
        results = []
        try:
            for resource_key, _ in resources:
                LOGGER.info(f"Deleting config: {resource_key}")

                json_config_rule = json_config_rule_delete(resource_key)

                # Remove the matching configuration rule
                for rule in self.__service.service_config.config_rules:
                    if rule.custom.resource_key == resource_key:
                        self.__service.service_config.config_rules.remove(rule)

            # Reconfigure the service after deleting configurations
            self.__task_executor.configure_service(self.__service)

            results.append(True)

        except Exception as e:
            LOGGER.error(f"Failed to delete config: {str(e)}")
            results.append(e)

        return results
