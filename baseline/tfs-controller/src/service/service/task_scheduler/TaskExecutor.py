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

import json, logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Union
from common.DeviceTypes import DeviceTypeEnum
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.proto.qkd_app_pb2 import QKDAppStatusEnum
from common.proto.context_pb2 import (
    Connection, ConnectionId, Device, DeviceDriverEnum, DeviceId, Service, ServiceId,
    OpticalConfig, OpticalConfigId, ConnectionList, ServiceConfigRule
)
from common.proto.qkd_app_pb2 import App, AppId
from common.proto.context_pb2 import ContextId
from common.tools.context_queries.Connection import get_connection_by_id
from common.tools.context_queries.Device import get_device
from common.tools.context_queries.Service import get_service_by_id
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Device import json_device_id
from context.client.ContextClient import ContextClient
from device.client.DeviceClient import DeviceClient
from qkd_app.client.QKDAppClient import QKDAppClient
from service.service.service_handler_api.Exceptions import (
    UnsatisfiedFilterException, UnsupportedFilterFieldException, UnsupportedFilterFieldValueException
)
from service.service.service_handler_api.ServiceHandlerFactory import ServiceHandlerFactory, get_service_handler_class
from service.service.tools.ObjectKeys import get_connection_key, get_device_key, get_service_key, get_qkd_app_key
from service.service.tools.object_uuid import opticalconfig_get_uuid

if TYPE_CHECKING:
    from service.service.service_handler_api._ServiceHandler import _ServiceHandler

LOGGER = logging.getLogger(__name__)

CacheableObject = Union[Connection, Device, Service]

class CacheableObjectType(Enum):
    CONNECTION = 'connection'
    DEVICE     = 'device'
    SERVICE    = 'service'
    QKD_APP    = 'qkd-app'

CONTROLLER_DEVICE_TYPES = {
    DeviceTypeEnum.EMULATED_IP_SDN_CONTROLLER,
    DeviceTypeEnum.EMULATED_MICROWAVE_RADIO_SYSTEM,
    DeviceTypeEnum.EMULATED_OPEN_LINE_SYSTEM,
    DeviceTypeEnum.IETF_SLICE,
    DeviceTypeEnum.IP_SDN_CONTROLLER,
    DeviceTypeEnum.MICROWAVE_RADIO_SYSTEM,
    DeviceTypeEnum.NCE,
    DeviceTypeEnum.OPEN_LINE_SYSTEM,
    DeviceTypeEnum.OPENFLOW_RYU_CONTROLLER,
    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER,
}
EXPANSION_CONTROLLER_DEVICE_TYPES = {
    DeviceTypeEnum.IETF_SLICE,
    DeviceTypeEnum.NCE,
    DeviceTypeEnum.OPENFLOW_RYU_CONTROLLER,
}

class TaskExecutor:
    def __init__(self, service_handler_factory : ServiceHandlerFactory) -> None:
        self._service_handler_factory = service_handler_factory
        self._context_client = ContextClient()
        # DEPENDENCY QKD
        self._qkd_app_client = QKDAppClient()
        self._device_client = DeviceClient()
        self._grpc_objects_cache : Dict[str, CacheableObject] = dict()

    @property
    def service_handler_factory(self) -> ServiceHandlerFactory: return self._service_handler_factory

    # ----- Common methods ---------------------------------------------------------------------------------------------

    def _load_grpc_object(self, object_type : CacheableObjectType, object_key : str) -> Optional[CacheableObject]:
        object_key = '{:s}:{:s}'.format(object_type.value, object_key)
        return self._grpc_objects_cache.get(object_key)

    def _store_grpc_object(self, object_type : CacheableObjectType, object_key : str, grpc_object) -> None:
        object_key = '{:s}:{:s}'.format(object_type.value, object_key)
        self._grpc_objects_cache[object_key] = grpc_object
    
    def _delete_grpc_object(self, object_type : CacheableObjectType, object_key : str) -> None:
        object_key = '{:s}:{:s}'.format(object_type.value, object_key)
        self._grpc_objects_cache.pop(object_key, None)

    def _store_editable_grpc_object(
        self, object_type : CacheableObjectType, object_key : str, grpc_class, grpc_ro_object
    ) -> Any:
        grpc_rw_object = grpc_class()
        grpc_rw_object.CopyFrom(grpc_ro_object)
        self._store_grpc_object(object_type, object_key, grpc_rw_object)
        return grpc_rw_object

    # ----- Connection-related methods ---------------------------------------------------------------------------------

    def get_connection(self, connection_id : ConnectionId) -> Connection:
        connection_key = get_connection_key(connection_id)
        connection = self._load_grpc_object(CacheableObjectType.CONNECTION, connection_key)
        if connection is None:
            connection = get_connection_by_id(self._context_client, connection_id)
            if connection is None: raise NotFoundException('Connection', connection_key)
            connection : Connection = self._store_editable_grpc_object(
                CacheableObjectType.CONNECTION, connection_key, Connection, connection)
        return connection

    def set_connection(self, connection : Connection) -> None:
        connection_key = get_connection_key(connection.connection_id)
        self._context_client.SetConnection(connection)
        self._store_grpc_object(CacheableObjectType.CONNECTION, connection_key, connection)

    def delete_connection(self, connection_id : ConnectionId) -> None:
        connection_key = get_connection_key(connection_id)
        self._context_client.RemoveConnection(connection_id)
        self._delete_grpc_object(CacheableObjectType.CONNECTION, connection_key)

    # ----- Device-related methods -------------------------------------------------------------------------------------

    def get_device(self, device_id : DeviceId) -> Device:
        device_key = get_device_key(device_id)
        device = self._load_grpc_object(CacheableObjectType.DEVICE, device_key)
        if device is None:
            device = get_device(self._context_client, device_id.device_uuid.uuid)
            if device is None: raise NotFoundException('Device', device_key)
            device : Device = self._store_editable_grpc_object(
                CacheableObjectType.DEVICE, device_key, Device, device)
        return device

    def configure_device(self, device : Device) -> None:
        device_key = get_device_key(device.device_id)
        self._device_client.ConfigureDevice(device)
        self._store_grpc_object(CacheableObjectType.DEVICE, device_key, device)
    
    # New function Andrea for Optical Devices
    def configure_optical_device(
        self, device : Device, settings : str, flows : list, is_opticalband : bool,
        connection_uuid:str
    ):
        device_key = get_device_key(device.device_id)
        optical_config_id = OpticalConfigId()
        optical_config_id.opticalconfig_uuid = opticalconfig_get_uuid(device.device_id)

        optical_config = OpticalConfig()

        setting = settings.value if settings else ""
        config_type = None

        try:
            result = self._context_client.SelectOpticalConfig(optical_config_id)

            new_config = json.loads(result.config)
            if is_opticalband : new_config['connection_uuid']=connection_uuid
            if 'type' in new_config:
                config_type=new_config['type']
            if config_type == 'optical-transponder':
                setting['status']='ENABLED'    
            if result is not None :
                new_config["new_config"] = setting
                new_config["is_opticalband"] = is_opticalband
                new_config["flow"] = flows
                result.config = json.dumps(new_config)
                optical_config.CopyFrom(result)
                self._device_client.ConfigureOpticalDevice(optical_config)
            self._store_grpc_object(CacheableObjectType.DEVICE, device_key, device)
        except Exception as e:
            LOGGER.info("error in configure_optical_device  %s",e)

    # Deconfiguring Optical Devices ( CNIT )   
    def deconfigure_optical_device(
        self, device : Device
        , channel_indexes : list
        , is_opticalband : bool
        , dev_flow : list
        ,bidir=None
    ):
        errors = []
        flows = []
        indexes = {}
        new_config = {}
        optical_config_id = OpticalConfigId()
        optical_config_id.opticalconfig_uuid = opticalconfig_get_uuid(device.device_id)
        # if transponder the channel index is same as its endpoint
        if device.device_type == DeviceTypeEnum.OPTICAL_TRANSPONDER._value_:
            for index in channel_indexes :
                flows.append(index)
        # if Roadm the channel index is the flow_id  ,or ob_id       
        else:
            for index in channel_indexes:
                if not is_opticalband:
                    indexes["flow_id"] = index  
                else:
                    indexes["ob_id"] = index

        try:
            result = self._context_client.SelectOpticalConfig(optical_config_id)
            # for extractor in device service to extract the index , dummy data for freq and band required
            indexes["frequency"] = None
            indexes["band"] = None
            indexes["bidir"]=bidir
            if result is not None:
                new_config = json.loads(result.config)
                new_config["new_config"]=indexes
                new_config["flow"] = flows if len(flows)>0 else dev_flow
                new_config["is_opticalband"] = is_opticalband
                result.config = json.dumps(new_config)
                # new_optical_config.config= json.dumps(new_config)
                # new_optical_config.opticalconfig_id.CopyFrom (optical_config_id)
                # new_optical_config.device_id.CopyFrom(device.device_id)
                LOGGER.info(f"SSSSSSS->{result}")
                self._device_client.DisableOpticalDevice(result)
        except Exception as e:
            errors.append(e)
            LOGGER.info("error in deconfigure_optical_device  %s",e)   
        return errors    

    def delete_setting(
        self, service_id : ServiceId, config_key : str, config_value : str
    ):
        service_configRule = ServiceConfigRule()
        service_configRule.service_id.CopyFrom(service_id)
        service_configRule.configrule_custom.resource_key = config_key
        service_configRule.configrule_custom.resource_value = config_value
        try:
            ctxt = ContextClient()
            ctxt.connect()
            ctxt.DeleteServiceConfigRule(service_configRule)
            ctxt.close()
        except Exception as e :
            LOGGER.info("error in delete service config rule  %s",e)   

    def check_service_for_media_channel(self, connections : ConnectionList, item) -> bool:
        service = item
        if (isinstance(item, ServiceId)):
            service = self.get_service(item)
        service_handler = None
        service_handler_settings = {}
        for connection in connections.connections:
            connection_uuid=connection.connection_id.connection_uuid
            if service_handler is None:
                service_handlers = self.get_service_handlers(
                    connection, service, **service_handler_settings
                )
                # TODO: improve to select different service handlers when needed
                # By now, assume a single service handler is retrieved for all the
                # device types in the path, i.e., all entries carry the same
                # service handler, so we choose the first one retrieved.
                if len(service_handlers) < 1:
                    raise Exception('Unsupported case: {:s}'.format(str(service_handlers)))
                service_handler,_ = list(service_handlers.values())[0]
            if service_handler.check_media_channel(connection_uuid):
                return True
        return False

    def check_connection_for_media_channel(
        self, connection : Connection, service : Service
    ) -> bool:
        service_handler_settings = {}
        connection_uuid = connection.connection_id.connection_uuid
        classes_service_handlers = self.get_service_handlers(
            connection, service, **service_handler_settings
        )
        # TODO: improve to select different service handlers when needed
        # By now, assume a single service handler is retrieved for all the
        # device types in the path, i.e., all entries carry the same
        # service handler, so we choose the first one retrieved.
        if len(classes_service_handlers) < 1:
            raise Exception('Unsupported case: {:s}'.format(str(classes_service_handlers)))
        service_handler_class,_ = list(classes_service_handlers.values())[0]
        return service_handler_class.check_media_channel(connection_uuid)

    def get_device_controller(self, device : Device) -> Optional[Device]:
        controller_uuid = device.controller_id.device_uuid.uuid
        if len(controller_uuid) == 0: return None
        controller = self.get_device(DeviceId(**json_device_id(controller_uuid)))
        if controller is None: raise Exception('Device({:s}) not found'.format(str(controller_uuid)))
        if len(controller.controller_id.device_uuid.uuid) == 0:
            return controller
        else:
            # in case controller is an under-underlay controller
            return self.get_device_controller(controller)

    def get_devices_from_connection(
        self, connection : Connection, exclude_managed_by_controller : bool = False
    ) -> Dict[DeviceTypeEnum, Dict[str, Device]]:
        devices : Dict[DeviceTypeEnum, Dict[str, Device]] = dict()
        #controllers : Dict[DeviceTypeEnum, Dict[str, Device]] = dict()
        for endpoint_id in connection.path_hops_endpoint_ids:
            device = self.get_device(endpoint_id.device_id)
            device_uuid = endpoint_id.device_id.device_uuid.uuid
            if device is None: raise Exception('Device({:s}) not found'.format(str(device_uuid)))

            controller = self.get_device_controller(device)
            if controller is None:
                device_type = DeviceTypeEnum._value2member_map_[device.device_type]
                #if device_type in CONTROLLER_DEVICE_TYPES:
                #    controllers.setdefault(device_type, dict())[device_uuid] = device
                #else:
                #    devices.setdefault(device_type, dict())[device_uuid] = device
                devices.setdefault(device_type, dict())[device_uuid] = device
            else:
                # ===== Ryu original test ========================================================================
                #if not exclude_managed_by_controller:
                #    LOGGER.debug('device managed by controller = {:s}'.format(str(device_uuid)))
                #    device_type = DeviceTypeEnum._value2member_map_[controller.device_type]
                #    LOGGER.debug('device_type not exlude by controller = {:s}'.format(str(device_type)))
                #    devices.setdefault(device_type, dict())[device_uuid] = device
                #else:
                #    device_type = DeviceTypeEnum._value2member_map_[controller.device_type]
                #    LOGGER.debug('device_type = {:s}'.format(str(device_type)))
                #    devices.setdefault(device_type, dict())[controller.device_id.device_uuid.uuid] = controller
                # ================================================================================================

                if not exclude_managed_by_controller:
                    # Controller device types for those underlying path is needed by service handler
                    device_type = DeviceTypeEnum._value2member_map_[controller.device_type]
                    if device_type not in EXPANSION_CONTROLLER_DEVICE_TYPES:
                        device_type = DeviceTypeEnum._value2member_map_[device.device_type]
                    devices.setdefault(device_type, dict())[device_uuid] = device
                
                device_type = DeviceTypeEnum._value2member_map_[controller.device_type]
                #controllers.setdefault(device_type, dict())[controller.device_id.device_uuid.uuid] = controller
                devices.setdefault(device_type, dict())[controller.device_id.device_uuid.uuid] = controller
        
        LOGGER.debug('[get_devices_from_connection] devices = {:s}'.format(str(devices)))
        #LOGGER.debug('[get_devices_from_connection] controllers = {:s}'.format(str(controllers)))
        #if len(devices) == 0 and len(controllers) > 0:
        #    return controllers
        #else:
        #    return devices
        return devices
    
    
    def set_optical_band(self, connection : ConnectionId,device:DeviceId) -> None:
        device_key = get_device_key(device.device_id)
        self._device_client.ConfigureDevice(device)
        self._store_grpc_object(CacheableObjectType.DEVICE, device_key, device)


    def get_device_type_drivers_for_connection(
        self, connection : Connection
    ) -> Dict[DeviceTypeEnum, Dict[str, Tuple[Device, Set[int]]]]:

        devices : Dict[DeviceTypeEnum, Dict[str, Tuple[Device, Set[int]]]] = dict()

        for endpoint_id in connection.path_hops_endpoint_ids:
            device = self.get_device(endpoint_id.device_id)
            device_uuid = endpoint_id.device_id.device_uuid.uuid
            if device is None: raise Exception('Device({:s}) not found'.format(str(device_uuid)))

            controller = self.get_device_controller(device)
            if controller is None:
                device_type = DeviceTypeEnum._value2member_map_[device.device_type]
                device_drivers = set(driver for driver in device.device_drivers)
                devices.setdefault(device_type, dict())[device_uuid] = (device, device_drivers)
            else:
                # Controller device types for those underlying path is needed by service handler
                device_type = DeviceTypeEnum._value2member_map_[controller.device_type]
                controller_drivers = set(driver for driver in controller.device_drivers)

                if device_type not in EXPANSION_CONTROLLER_DEVICE_TYPES:
                    devices.setdefault(device_type, dict())[device_uuid] = (device, controller_drivers)
                else:
                    controller_uuid = controller.device_id.device_uuid.uuid
                    devices.setdefault(device_type, dict())[controller_uuid] = (controller, controller_drivers)

        LOGGER.debug('[get_devices_from_connection] devices = {:s}'.format(str(devices)))
        return devices


    # ----- Service-related methods ------------------------------------------------------------------------------------

    def get_service(self, service_id : ServiceId) -> Service:
        service_key = get_service_key(service_id)
        service = self._load_grpc_object(CacheableObjectType.SERVICE, service_key)
        if service is None:
            service = get_service_by_id(self._context_client, service_id)
            if service is None: raise NotFoundException('Service', service_key)
            service : service = self._store_editable_grpc_object(
                CacheableObjectType.SERVICE, service_key, Service, service)
        return service

    def set_service(self, service : Service) -> None:
        service_key = get_service_key(service.service_id)
        self._context_client.SetService(service)
        self._store_grpc_object(CacheableObjectType.SERVICE, service_key, service)

    def delete_service(self, service_id : ServiceId) -> None:
        service_key = get_service_key(service_id)
        self._context_client.RemoveService(service_id)
        self._delete_grpc_object(CacheableObjectType.SERVICE, service_key)

    # ----- Service Handler Factory ------------------------------------------------------------------------------------

    def get_service_handlers(
        self, connection : Connection, service : Service, **service_handler_settings
    ) -> Dict[DeviceTypeEnum, Tuple['_ServiceHandler', Dict[str, Device]]]:
        # ===== Ryu original test ========================================================================
        ## WARNING: exclude_managed_by_controller should be True, changed to False for test purposes.
        ## For Ryu SDN controller we need to know the underlying devices we are traversing.
        ## Elaborate proper logic to resolve this case.
        #connection_device_types_excluded : Dict[DeviceTypeEnum, Dict[str, Device]] = self.get_devices_from_connection(
        #    connection, exclude_managed_by_controller=True
        #)
        #LOGGER.debug('connection_device_types_excluded = {:s}'.format(str(connection_device_types_excluded)))
        #connection_device_types_included : Dict[DeviceTypeEnum, Dict[str, Device]] = self.get_devices_from_connection(
        #    connection, exclude_managed_by_controller=False
        #)
        #LOGGER.debug('connection_device_types_included = {:s}'.format(str(connection_device_types_included)))
        # ================================================================================================

        device_type_to_device_and_drivers : Dict[DeviceTypeEnum, Dict[str, Tuple[Device, Set[int]]]] = \
            self.get_device_type_drivers_for_connection(connection)

        service_handlers : Dict[DeviceTypeEnum, Tuple['_ServiceHandler', Dict[str, Device]]] = dict()
        # ===== Ryu original test ========================================================================
        #for device_type, connection_devices in connection_device_types_excluded.items():
        # ================================================================================================
        for device_type, device_and_drivers in device_type_to_device_and_drivers.items():
            try:
                service_handler_class = get_service_handler_class(
                    self._service_handler_factory, service, device_and_drivers
                )
                connection_devices = {
                    device_uuid : device
                    for device_uuid, (device, _) in device_and_drivers.items()
                }
                # ===== Ryu original test ========================================================================
                #LOGGER.debug('service_handler_class IN CONNECTION DEVICE TYPE EXCLUDED = {:s}'.format(str(service_handler_class.__name__)))
                #service_handler = service_handler_class(service, self, **service_handler_settings)
                #LOGGER.debug('service_handler IN CONNECTION DEVICE TYPE EXCLUDED = {:s}'.format(str(service_handler)))
                #connection_devices_included = connection_device_types_included.get(device_type, connection_devices)
                #LOGGER.debug('connection_devices_included IN CONNECTION DEVICE TYPE EXCLUDED = {:s}'.format(str(connection_devices_included)))
                #service_handlers[device_type] = (service_handler, connection_devices_included)
                #LOGGER.debug('service_handlers IN CONNECTION DEVICE TYPE EXCLUDED = {:s}'.format(str(service_handlers)))
                # ================================================================================================
                service_handler = service_handler_class(service, self, **service_handler_settings)
                service_handlers[device_type] = (service_handler, connection_devices)
            except (
                UnsatisfiedFilterException, UnsupportedFilterFieldException,
                UnsupportedFilterFieldValueException
            ):
                dict_connection_devices = {
                    cd_data.name : (
                        cd_uuid,
                        cd_data.name,
                        {
                            (device_driver, DeviceDriverEnum.Name(device_driver))
                            for device_driver in cd_data.device_drivers
                        }, {
                            (device_driver, DeviceDriverEnum.Name(device_driver))
                            for device_driver in drivers
                        }
                    )
                    for cd_uuid,(cd_data, drivers) in device_and_drivers.items()
                }
                MSG = 'Unable to select service handler. service={:s} connection={:s} connection_devices={:s}'
                LOGGER.exception(MSG.format(
                    grpc_message_to_json_string(service), grpc_message_to_json_string(connection),
                    str(dict_connection_devices)
                ))
        return service_handlers


    # ----- QkdApp-related methods -------------------------------------------------------------------------------------

    def register_qkd_app(self, app: App) -> None:
        """
        Registers a QKD App and stores it in the cache.
        """
        qkd_app_key = get_qkd_app_key(app.app_id)
        self._qkd_app_client.RegisterApp(app)
        LOGGER.info("QKD app registered with key: %s", qkd_app_key)
        self._store_grpc_object(CacheableObjectType.QKD_APP, qkd_app_key, app)

    def update_qkd_app_status(self, app: App, new_status: QKDAppStatusEnum) -> None:
        """
        Updates the status of a QKD app and persists it to the database.
        """
        try:
            app.app_status = new_status
            LOGGER.info(f"Attempting to update app {app.app_id.app_uuid.uuid} to status {new_status}")
            self._qkd_app_client.UpdateApp(app)
            LOGGER.info(f"Successfully updated app {app.app_id.app_uuid.uuid} to status {new_status}")
        except Exception as e:
            LOGGER.error(f"Failed to update QKD app {app.app_id.app_uuid.uuid}: {str(e)}")
            raise e

    def list_qkd_apps(self, context_id: ContextId) -> List[App]:
        """
        Retrieves a list of QKD apps from the QKD App service.
        """
        try:
            apps_response = self._qkd_app_client.ListApps(context_id)
            LOGGER.info(f"ListApps retrieved: {len(apps_response.apps)} apps with status")
            
            # Ensure that the status is logged and used
            for app in apps_response.apps:
                LOGGER.info(f"App ID: {app.app_id.app_uuid.uuid}, Status: {app.app_status}")
            
            return apps_response.apps
        except Exception as e:
            LOGGER.error(f"Failed to list QKD apps: {str(e)}")
            return []

    def delete_qkd_app(self, app_id: AppId) -> None:
        """
        Deletes a QKD App by its AppId and removes it from the cache.
        """
        qkd_app_key = get_qkd_app_key(app_id)
        try:
            LOGGER.info(f"Attempting to delete QKD app with AppId: {app_id}")
            self._qkd_app_client.DeleteApp(app_id)
            LOGGER.info(f"QKD app deleted with key: {qkd_app_key}")
            self._delete_grpc_object(CacheableObjectType.QKD_APP, qkd_app_key)
        except Exception as e:
            LOGGER.error(f"Failed to delete QKD app with AppId {app_id}: {str(e)}")
            raise e
