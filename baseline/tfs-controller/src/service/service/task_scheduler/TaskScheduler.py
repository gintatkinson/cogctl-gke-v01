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

import graphlib, logging, queue, time
from common.method_wrappers.ServiceExceptions import NotFoundException
from typing import TYPE_CHECKING, Dict, Tuple
from common.proto.context_pb2 import (
    Connection, ConnectionId, Service, ServiceId, ServiceStatusEnum, ConnectionList,
    OpticalBand
)
from common.proto.pathcomp_pb2 import PathCompReply
from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from service.service.tools.ObjectKeys import get_connection_key, get_service_key
from .tasks._Task import _Task
from .tasks.Task_ConnectionConfigure import Task_ConnectionConfigure
from .tasks.Task_OpticalConnectionConfigure import Task_OpticalConnectionConfigure
from .tasks.Task_OpticalConnectionDeconfigure import Task_OpticalConnectionDeconfigure

from .tasks.Task_OpticalServiceDelete import Task_OpticalServiceDelete
from .tasks.Task_ConnectionDeconfigure import Task_ConnectionDeconfigure
from .tasks.Task_ServiceDelete import Task_ServiceDelete
from .tasks.Task_ServiceSetStatus import Task_ServiceSetStatus
from .TaskExecutor import CacheableObjectType, TaskExecutor
from .tasks.Task_OpticalServiceConfigDelete import Task_OpticalServiceConfigDelete
from service.service.tools.OpticalTools import delete_lightpath ,DelFlexLightpath
from common.Constants import OpticalServiceType
if TYPE_CHECKING:
    from service.service.service_handler_api.ServiceHandlerFactory import ServiceHandlerFactory

LOGGER = logging.getLogger(__name__)

class TasksScheduler:
    def __init__(self, service_handler_factory : 'ServiceHandlerFactory') -> None:
        self._dag = graphlib.TopologicalSorter()
        self._executor = TaskExecutor(service_handler_factory)
        self._tasks : Dict[str, _Task] = dict()
        self._context_client = ContextClient()

    # ----- Helper methods ---------------------------------------------------------------------------------------------

    def _add_task_if_not_exists(self, task : _Task) -> str:
        task_key = task.key
        if task_key not in self._tasks:
            self._tasks[task_key] = task
        return task_key

    def _add_connection_to_executor_cache(self, connection : Connection) -> None:
        connection_key = get_connection_key(connection.connection_id)
        self._executor._store_editable_grpc_object(
            CacheableObjectType.CONNECTION, connection_key, Connection, connection)

    def _add_service_to_executor_cache(self, service : Service) -> None:
        service_key = get_service_key(service.service_id)
        self._executor._store_editable_grpc_object(
            CacheableObjectType.SERVICE, service_key, Service, service)

    # ----- Task & DAG composition methods -----------------------------------------------------------------------------

    def _service_create(self, service_id : ServiceId) -> Tuple[str, str]:
        service_planned_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_PLANNED))

        service_active_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE))

        # activating a service requires the service is in planning state
        self._dag.add(service_active_key, service_planned_key)
        return service_planned_key, service_active_key

    def _service_remove(self, service_id : ServiceId) -> Tuple[str, str]:

        service_removing_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_PENDING_REMOVAL))

        service_delete_key = self._add_task_if_not_exists(Task_ServiceDelete(self._executor, service_id))

        # deleting a service requires the service is in removing state
        self._dag.add(service_delete_key, service_removing_key)
        return service_removing_key, service_delete_key
    
    
    def _optical_service_create(self, service_id : ServiceId , has_media_channel : bool
                                , has_optical_band = True) -> Tuple[str, str]:
        service_planned_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_PLANNED))

        service_active_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE))

        # activating a service requires the service is in planning state
        self._dag.add(service_active_key, service_planned_key)
        return service_planned_key, service_active_key

    def _optical_service_remove(
        self, service_id : ServiceId, has_media_channel : bool, has_optical_band = True
    ) -> Tuple[str, str]:
        service_removing_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE
        ))

        service_delete_key = self._add_task_if_not_exists(Task_OpticalServiceDelete(
            self._executor, service_id, has_media_channel, has_optical_band
        ))

        # deleting a service requires the service is in removing state
        self._dag.add(service_delete_key, service_removing_key)
        return service_removing_key, service_delete_key

    def _connection_configure(self, connection_id : ConnectionId, service_id : ServiceId) -> str:
        connection_configure_key = self._add_task_if_not_exists(Task_ConnectionConfigure(
            self._executor, connection_id))

        # the connection configuration depends on its connection's service being in planning state
        service_planned_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_PLANNED))
        self._dag.add(connection_configure_key, service_planned_key)

        # the connection's service depends on the connection configuration to transition to active state
        service_active_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE))
        self._dag.add(service_active_key, connection_configure_key)

        return connection_configure_key

    def _connection_deconfigure(self, connection_id : ConnectionId, service_id : ServiceId) -> str:
        connection_deconfigure_key = self._add_task_if_not_exists(Task_ConnectionDeconfigure(
            self._executor, connection_id
        ))

        # the connection deconfiguration depends on its connection's service being in removing state
        service_pending_removal_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_PENDING_REMOVAL
        ))
        self._dag.add(connection_deconfigure_key, service_pending_removal_key)

        # the connection's service depends on the connection deconfiguration to transition to delete
        service_delete_key = self._add_task_if_not_exists(Task_ServiceDelete(
            self._executor, service_id
        ))
        self._dag.add(service_delete_key, connection_deconfigure_key)

        return connection_deconfigure_key
    
    
    def _optical_connection_configure(self, connection_id : ConnectionId
                                      , service_id : ServiceId ,
                                      has_media_channel : bool, has_optical_band = True) -> str:
        optical_connection_configure_key = self._add_task_if_not_exists(Task_OpticalConnectionConfigure(
            self._executor, connection_id))
        
        
        # the connection configuration depends on its connection's service being in planning state
        service_planned_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_PLANNED))
        self._dag.add(optical_connection_configure_key, service_planned_key)
        
      

        # the connection's service depends on the connection configuration to transition to active state
        service_active_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE))
        self._dag.add(service_active_key, optical_connection_configure_key)
        
       
        return optical_connection_configure_key

    def _optical_connection_deconfigure(
        self, connection_id : ConnectionId, service_id : ServiceId,
        has_media_channel : bool, has_optical_band = True
    ) -> str:
        connection_deconfigure_key = self._add_task_if_not_exists(Task_OpticalConnectionDeconfigure(
            self._executor, connection_id, has_media_channel=has_media_channel
        ))

        # the connection deconfiguration depends on its connection's service being in removing state
        service_pending_removal_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE
        ))
        self._dag.add(connection_deconfigure_key, service_pending_removal_key)

        service_delete_key = self._add_task_if_not_exists(Task_OpticalServiceDelete(
            self._executor, service_id, has_media_channel, has_optical_band
        ))
        self._dag.add(service_delete_key, connection_deconfigure_key)

        return connection_deconfigure_key
    
    def _optical_service_config_remove(
        self, connection_id : ConnectionId, service_id : ServiceId
    ) -> str:
        service_config_key = self._add_task_if_not_exists(Task_OpticalServiceConfigDelete(
            self._executor, connection_id, service_id
        ))
        service_pending_removal_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE
        ))
        self._dag.add(service_config_key, service_pending_removal_key)
        return service_config_key

    def compose_from_pathcompreply(self, pathcomp_reply : PathCompReply, is_delete : bool = False) -> None:
        t0 = time.time()
        include_service = self._service_remove if is_delete else self._service_create
        include_connection = self._connection_deconfigure if is_delete else self._connection_configure

        for service in pathcomp_reply.services:
            include_service(service.service_id)
            self._add_service_to_executor_cache(service)

        for connection in pathcomp_reply.connections:
            connection_key = include_connection(connection.connection_id, connection.service_id)
            self._add_connection_to_executor_cache(connection)
            self._executor.get_service(connection.service_id)
            for sub_service_id in connection.sub_service_ids:
                _,service_key_done = include_service(sub_service_id)
                self._executor.get_service(sub_service_id)
                self._dag.add(connection_key, service_key_done)

        t1 = time.time()
        LOGGER.debug('[compose_from_pathcompreply] elapsed_time: {:f} sec'.format(t1-t0))

    def check_service_for_media_channel(
        self, connections : ConnectionList, item
    )->Tuple[bool, bool]:
        service = item
        has_media_channel = False
        has_optical_band = False
        if isinstance(item, ServiceId):
            service = self._executor.get_service(item)
        class_service_handler = None
        service_handler_settings = {}
        for connection in connections.connections:
            connection_uuid = connection.connection_id.connection_uuid.uuid
            if class_service_handler is None:
                classes_service_handlers = self._executor.get_service_handlers(
                    connection, service, **service_handler_settings
                )
                # TODO: improve to select different service handlers when needed
                # By now, assume a single service handler is retrieved for all the
                # device types in the path, i.e., all entries carry the same
                # service handler, so we choose the first one retrieved.
                if len(classes_service_handlers) < 1:
                    raise Exception('Unsupported case: {:s}'.format(str(classes_service_handlers)))
                class_service_handler,_ = list(classes_service_handlers.values())[0]
            if class_service_handler.check_media_channel(connection_uuid):
                has_media_channel = True
            else :
                has_optical_band = True
        return (has_media_channel, has_optical_band)
    
    
    
    def compose_from_opticalcontroller_reply(
        self, pathcomp_reply : PathCompReply, is_delete : bool = False
    ) -> None:
        t0 = time.time()
        include_service = self._optical_service_remove if is_delete else self._optical_service_create
        include_connection = self._optical_connection_deconfigure if is_delete else self._optical_connection_configure

        #pending_items_to_explore.put(service)
        has_media_channel = None
        has_optical_band = None
   
        for service in pathcomp_reply.services:

                connections = self._context_client.ListConnections(service.service_id)
                has_media_channel, has_optical_band = self.check_service_for_media_channel(
                    connections=connections, item=service.service_id
                )

                
                include_service(service.service_id , has_media_channel=has_media_channel, has_optical_band=has_optical_band)
                self._add_service_to_executor_cache(service)
                
                for connection in connections.connections:
                    self._add_connection_to_executor_cache(connection)
                   
               

        for connection in pathcomp_reply.connections:
               
                connection_key = include_connection(
                    connection.connection_id, connection.service_id, has_media_channel=has_media_channel,
                    has_optical_band=has_optical_band
                ) 
                self._add_connection_to_executor_cache(connection)

                self._executor.get_service(connection.service_id)
                for sub_service_id in connection.sub_service_ids:
                    _,service_key_done = include_service(
                        sub_service_id, has_media_channel=has_media_channel,
                        has_optical_band=has_optical_band
                    )
                    self._executor.get_service(sub_service_id)
                    self._dag.add(connection_key, service_key_done)

        t1 = time.time()
        LOGGER.debug('[compose_from_service] elapsed_time: {:f} sec'.format(t1-t0))
        
        
        
    def compose_from_service_expansion(
        self, service :Service,
    ) -> None:
        t0 = time.time()
        include_service = self._optical_service_create
        include_connection = self._optical_connection_configure
    
        logging.debug(f"after setting the config {service}")
        #pending_items_to_explore.put(service)
        has_media_channel = None
        has_optical_band = None
        if service is None : raise NotFoundException('Service', service, extra_details=[
            'service  not found '
        ])
   
       
    
        connections = self._context_client.ListConnections(service.service_id)
        has_media_channel, has_optical_band = self.check_service_for_media_channel(
            connections=connections, item=service.service_id
        )
        
        _,service_key_done= include_service(service.service_id , 
                                           has_media_channel=has_media_channel, 
                                           has_optical_band=has_optical_band)
        # self._add_service_to_executor_cache(service)
        service_updating_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service.service_id, ServiceStatusEnum.SERVICESTATUS_UPDATING
        ))
        self._add_service_to_executor_cache(service)
        for connection in connections.connections:
            connection_key = include_connection(
                    connection.connection_id, connection.service_id, has_media_channel=has_media_channel,
                    has_optical_band=has_optical_band
                )
            self._add_connection_to_executor_cache(connection)
            self._dag.add(connection_key, service_updating_key)      
        t1 = time.time()
        LOGGER.debug('[compose_from_service] elapsed_time: {:f} sec'.format(t1-t0))    

    def compose_from_optical_service(self, service : Service, params:dict, is_delete : bool = False) -> None:
        t0 = time.time()
        include_service = self._optical_service_remove if is_delete else self._service_create
        include_connection = self._optical_connection_deconfigure if is_delete else self._connection_configure
        include_service_config = self._optical_service_config_remove if is_delete else None

        explored_items = set()
        pending_items_to_explore = queue.Queue()
        pending_items_to_explore.put(service)
        has_media_channel=None
        has_optical_band=None
        reply=None
        code=0
        reply_not_allowed="DELETE_NOT_ALLOWED"
        while not pending_items_to_explore.empty():
            try:
                item = pending_items_to_explore.get(block=False)

            except queue.Empty:
                break
        
            if isinstance(item, Service):
          
                str_item_key = grpc_message_to_json_string(item.service_id)
                if str_item_key in explored_items: continue
                connections = self._context_client.ListConnections(item.service_id)
                has_media_channel,has_optical_band=self.check_service_for_media_channel(connections=connections,item=item.service_id)
                oc_type = 1 
                if len(service.service_config.config_rules) > 0:
                    for constraint in service.service_constraints:
                        if "type" in constraint.custom.constraint_type:
                            oc_type =   OpticalServiceType(str(constraint.custom.constraint_value))
                    if oc_type == 2 : 
                        reply,code = delete_lightpath(
                                               params['src']
                                             , params ['dst']
                                             , params['bitrate']
                                             , flow_id= params['flow_id']
                                             )
              
                    else :             
                        reply,code = DelFlexLightpath(
                                                  params['src']
                                                , params ['dst']
                                                , params['bitrate']
                                                , params['ob_id']
                                                , delete_band=not has_media_channel
                                                , flow_id= params['flow_id']
                                                )
                
                    
                if code == 400 and reply_not_allowed in reply :
                   MSG = 'Deleteion for the service is not Allowed , Served Lightpaths is not empty'
                   raise Exception(MSG)

                include_service(item.service_id,has_media_channel=has_media_channel,has_optical_band=has_optical_band)
                self._add_service_to_executor_cache(item)
               
          
                for connection in connections.connections:
                        self._add_connection_to_executor_cache(connection)
                        pending_items_to_explore.put(connection)
                explored_items.add(str_item_key)
        

            elif isinstance(item, ServiceId):
              
                if code == 400 and reply_not_allowed in reply:break
                
                str_item_key = grpc_message_to_json_string(item)
                if str_item_key in explored_items: continue
                connections = self._context_client.ListConnections(item)
                has_media_channel,has_optical_band=self.check_service_for_media_channel(connections=connections,item=item)

            
                include_service(item,has_media_channel=has_media_channel,has_optical_band=has_optical_band)
               
                
                self._executor.get_service(item)
               
                for connection in connections.connections:
                  
                    self._add_connection_to_executor_cache(connection)
                    pending_items_to_explore.put(connection)
    
                explored_items.add(str_item_key)

            elif isinstance(item, Connection):
                if code == 400 and reply_not_allowed in reply:break
                str_item_key = grpc_message_to_json_string(item.connection_id)
                if str_item_key in explored_items: continue
                
                   
                connection_key = include_connection(  item.connection_id
                                                    , item.service_id
                                                    , has_media_channel=has_media_channel
                                                    , has_optical_band=has_optical_band ) 
                self._add_connection_to_executor_cache(connection)
                
                if include_service_config is not None : 
                   connections_list = ConnectionList()  
                   connections_list.connections.append(item)
                   
                   is_media_channel,_=self.check_service_for_media_channel(connections=connections_list,item=service)
                   
                   if has_optical_band and is_media_channel:
                        include_service_config(item.connection_id
                                                , item.service_id )
                

                self._executor.get_service(item.service_id)
                pending_items_to_explore.put(item.service_id)
              
           
                for sub_service_id in item.sub_service_ids:
                    _,service_key_done = include_service(sub_service_id
                                                         ,has_media_channel=has_media_channel
                                                         ,has_optical_band=has_optical_band)
                    self._executor.get_service(sub_service_id)
                    self._dag.add(service_key_done, connection_key)
                    pending_items_to_explore.put(sub_service_id)
                    


                explored_items.add(str_item_key)
            
                     
            else:
                MSG = 'Unsupported item {:s}({:s})'
                raise Exception(MSG.format(type(item).__name__, grpc_message_to_json_string(item)))
      
        t1 = time.time()
        LOGGER.debug('[compose_from_service] elapsed_time: {:f} sec'.format(t1-t0))


    def compose_from_service(self, service : Service, is_delete : bool = False) -> None:
        t0 = time.time()
        include_service = self._service_remove if is_delete else self._service_create
        include_connection = self._connection_deconfigure if is_delete else self._connection_configure

        explored_items = set()
        pending_items_to_explore = queue.Queue()
        pending_items_to_explore.put(service)

        while not pending_items_to_explore.empty():
            try:
                item = pending_items_to_explore.get(block=False)
            except queue.Empty:
                break

            if isinstance(item, Service):
                str_item_key = grpc_message_to_json_string(item.service_id)
                if str_item_key in explored_items: continue

                include_service(item.service_id)
                self._add_service_to_executor_cache(item)
                connections = self._context_client.ListConnections(item.service_id)
                for connection in connections.connections:
                    self._add_connection_to_executor_cache(connection)
                    pending_items_to_explore.put(connection)
                explored_items.add(str_item_key)

            elif isinstance(item, ServiceId):
                str_item_key = grpc_message_to_json_string(item)
                if str_item_key in explored_items: continue

                include_service(item)
                self._executor.get_service(item)
                connections = self._context_client.ListConnections(item)
                for connection in connections.connections:
                    self._add_connection_to_executor_cache(connection)
                    pending_items_to_explore.put(connection)
                explored_items.add(str_item_key)

            elif isinstance(item, Connection):
                str_item_key = grpc_message_to_json_string(item.connection_id)
                if str_item_key in explored_items: continue

                connection_key = include_connection(item.connection_id, item.service_id)
                self._add_connection_to_executor_cache(connection)
                self._executor.get_service(item.service_id)
                pending_items_to_explore.put(item.service_id)

                for sub_service_id in item.sub_service_ids:
                    _,service_key_done = include_service(sub_service_id)
                    self._executor.get_service(sub_service_id)
                    self._dag.add(service_key_done, connection_key)
                    pending_items_to_explore.put(sub_service_id)

                explored_items.add(str_item_key)

            else:
                MSG = 'Unsupported item {:s}({:s})'
                raise Exception(MSG.format(type(item).__name__, grpc_message_to_json_string(item)))

        t1 = time.time()
        LOGGER.debug('[compose_from_service] elapsed_time: {:f} sec'.format(t1-t0))

    def compose_service_connection_update(
        self, service : Service, old_connection : Connection, new_connection : Connection
    ) -> None:
        t0 = time.time()

        self._add_service_to_executor_cache(service)
        self._add_connection_to_executor_cache(old_connection)
        self._add_connection_to_executor_cache(new_connection)

        service_updating_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service.service_id, ServiceStatusEnum.SERVICESTATUS_UPDATING
        ))

        old_connection_deconfigure_key = self._add_task_if_not_exists(Task_ConnectionDeconfigure(
            self._executor, old_connection.connection_id
        ))

        new_connection_configure_key = self._add_task_if_not_exists(Task_ConnectionConfigure(
            self._executor, new_connection.connection_id
        ))

        service_active_key = self._add_task_if_not_exists(Task_ServiceSetStatus(
            self._executor, service.service_id, ServiceStatusEnum.SERVICESTATUS_ACTIVE
        ))

        # the old connection deconfiguration depends on service being in updating state
        self._dag.add(old_connection_deconfigure_key, service_updating_key)

        # the new connection configuration depends on service being in updating state
        self._dag.add(new_connection_configure_key, service_updating_key)

        # the new connection configuration depends on the old connection having been deconfigured
        self._dag.add(new_connection_configure_key, old_connection_deconfigure_key)

        # re-activating the service depends on the service being in updating state before
        self._dag.add(service_active_key, service_updating_key)

        # re-activating the service depends on the new connection having been configured
        self._dag.add(service_active_key, new_connection_configure_key)

        t1 = time.time()
        LOGGER.debug('[compose_service_connection_update] elapsed_time: {:f} sec'.format(t1-t0))

    def execute_all(self, dry_run : bool = False) -> None:
        ordered_task_keys = list(self._dag.static_order())
        LOGGER.info('[execute_all] ordered_task_keys={:s}'.format(str(ordered_task_keys)))

        results = []
        for task_key in ordered_task_keys:
            str_task_name = ('DRY ' if dry_run else '') + str(task_key)
            LOGGER.debug('[execute_all] starting task {:s}'.format(str_task_name))
            task = self._tasks.get(task_key)
            succeeded = True if dry_run else task.execute()
            results.append(succeeded)
            LOGGER.debug('[execute_all] finished task {:s} ; succeeded={:s}'.format(str_task_name, str(succeeded)))

        LOGGER.debug('[execute_all] results={:s}'.format(str(results)))
        return zip(ordered_task_keys, results)
