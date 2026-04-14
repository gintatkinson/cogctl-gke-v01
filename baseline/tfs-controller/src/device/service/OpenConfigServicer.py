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

import grpc, logging, json , traceback
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.proto.context_pb2 import (
    Device, DeviceId, DeviceOperationalStatusEnum, Empty, OpticalConfig,
    OpticalConfig, OpticalConfigList
)
from common.proto.device_pb2_grpc import DeviceServiceServicer
from common.tools.context_queries.Device import get_device
from common.tools.mutex_queues.MutexQueues import MutexQueues
from common.DeviceTypes import DeviceTypeEnum
from context.client.ContextClient import ContextClient
from .driver_api._Driver import _Driver
from .driver_api.DriverInstanceCache import DriverInstanceCache, get_driver
from .monitoring.MonitoringLoops import MonitoringLoops
from .Tools import extract_resources
from .Tools import check_no_endpoints

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Device', 'RPC')

METRICS_POOL_DETAILS = MetricsPool('Device', 'execution', labels={
    'driver': '', 'operation': '', 'step': '',
})

class OpenConfigServicer(DeviceServiceServicer):
    def __init__(self, driver_instance_cache : DriverInstanceCache, monitoring_loops : MonitoringLoops) -> None:
        LOGGER.debug('Creating Servicer...')
        self.driver_instance_cache = driver_instance_cache
        self.monitoring_loops = monitoring_loops
        self.mutex_queues = MutexQueues()
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def AddOpenConfigDevice(self, request : OpticalConfig, context : grpc.ServicerContext) -> DeviceId:
            device_uuid = request.device_id.device_uuid.uuid
            check_no_endpoints(request.device_endpoints)

            context_client = ContextClient()
            device = get_device(context_client, device_uuid, rw_copy=True)
            if device is None:
                # not in context, create blank one to get UUID, and populate it below
                device = Device()
                device.device_id.CopyFrom(request.device_id)            # pylint: disable=no-member
                device.name = request.name
                device.device_type = request.device_type
                device.device_operational_status = DeviceOperationalStatusEnum.DEVICEOPERATIONALSTATUS_UNDEFINED
                device.device_drivers.extend(request.device_drivers)    # pylint: disable=no-member
                device.device_config.CopyFrom(request.device_config)
                device.device_endpoints.extend(request.device_endpoints)
                # pylint: disable=no-member
                device_id = context_client.SetDevice(device)
                device = get_device(context_client, device_id.device_uuid.uuid, rw_copy=True)

            # update device_uuid to honor UUID provided by Context
            device_uuid = device.device_id.device_uuid.uuid
            self.mutex_queues.wait_my_turn(device_uuid)
            try:
                device_id = context_client.SetDevice(device)
            except Exception as error :
                LOGGER.debug("error %s",error)    

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ConfigureOpticalDevice (self, request : OpticalConfig, context : grpc.ServicerContext) -> Empty:
        device_uuid = request.device_id.device_uuid.uuid
        resources : list[dict] = []
        is_all_good = True
        config = json.loads(request.config)
        results = None
        
        LOGGER.info(f"config from service {config}")
        
        try:
            context_client = ContextClient()
            device = get_device(
                context_client, device_uuid, rw_copy=True, include_endpoints=True, include_components=False,
                include_config_rules=False)
            LOGGER.info(f"get_device  {device.name}")
            if device is None:
                raise NotFoundException('Device', device_uuid, extra_details='loading in ConfigureDevice')
            resources, conditions = extract_resources(config=config, device=device)
            LOGGER.info(f"resources  {resources}")
            LOGGER.info(f"conditions  {conditions}")
            driver : _Driver = get_driver(self.driver_instance_cache, device)
            results,new_config = driver.SetConfig(resources=resources,conditions=conditions)
        
            errors = [r for r in results if r is not None]
            if errors:
                raise Exception(f"Driver errors: {errors}")

            if is_all_good:
                #driver.GetConfig(resource_keys=[])   
                config = json.loads(request.config)
               
                handled_flow = next((i for i in resources if i['resource_key'] == 'handled_flow'), None)
                if handled_flow is not None and len(handled_flow) > 0:
                    config['flow_handled'] = handled_flow['value']
                    
                    
                if 'interfaces' in new_config and device.device_type == DeviceTypeEnum.OPEN_ROADM._value_:
                    LOGGER.info(f"with_new_config  {new_config}") 
                    config["interfaces"].extend(new_config['interfaces'])
                    LOGGER.info(f"updating_the_oc  {request}") 
                    request.config=json.dumps(config) 
                    context_client.SetOpticalConfig(request)   
                else :    
                    request.config=json.dumps(config) 
                    context_client.UpdateOpticalConfig(request) 
                
        except Exception as e:
            logging.error("Exception occurred:\n%s", traceback.format_exc())   
        finally : 
            context_client.close()   
                
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetDeviceConfiguration (self, request : OpticalConfigList, context : grpc.ServicerContext) -> Empty:
        context_client = ContextClient()

        for configs in request.opticalconfigs:
            device_uuid = configs.device_id.device_uuid.uuid
            try:
                device = get_device(
                    context_client, device_uuid, rw_copy=True, include_endpoints=True, include_components=False,
                    include_config_rules=False)
                if device is None:
                    raise NotFoundException('Device', device_uuid, extra_details='loading in ConfigureDevice')
                driver : _Driver = get_driver(self.driver_instance_cache, device)
                results = driver.GetConfig(resource_keys=[]) 
                for resource_data in results :
                    resource_key, resource_value = resource_data
                    if resource_key.startswith('/opticalconfigs/opticalconfig/'):
                        if 'opticalconfig' in resource_value:
                            context_client.SetOpticalConfig(resource_value['opticalconfig'])

                #TODO: add a control with the NETCONF get
                #driver.GetConfig(resource_keys=filter_fields)
            except Exception as e:
                raise Exception("error in configuring %s",e)                
        context_client.close()
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DisableOpticalDevice (self, request : OpticalConfig, context : grpc.ServicerContext) -> Empty:
        roadm_configuration = None
        device_uuid = request.device_id.device_uuid.uuid
        resources : list[dict] = []
        is_all_good = True
        config = json.loads(request.config)
        #LOGGER.info(f"from disable optical device {config}")
        try:
            context_client = ContextClient()
            device = get_device(
                context_client, device_uuid, rw_copy=True, include_endpoints=True, include_components=False,
                include_config_rules=False)

            if device is None:
                raise NotFoundException('Device', device_uuid, extra_details='loading in ConfigureDevice')

            resources, conditions = extract_resources(config=config, device=device)

            driver : _Driver = get_driver(self.driver_instance_cache, device)
            results,config_delete = driver.DeleteConfig(resources=resources,conditions=conditions)
            if config_delete and 'interfaces' in config_delete: 
                if 'new_config'in config  :
                    config["new_config"]=config_delete
                else :
                    config['new_config']  ={}
                    config["new_config"]=config_delete
                      
                request.config=json.dumps(config)
            for result in results:
                if  result  is not None:
                    is_all_good = False
                    raise Exception(result)
            if is_all_good:
                
                if "new_config" in config :
                    context_client.DeleteOpticalChannel(request) 
                    context_client.close()    
        except Exception as e:
            LOGGER.info("error in Disable configuring %s",e)    
        return Empty()
