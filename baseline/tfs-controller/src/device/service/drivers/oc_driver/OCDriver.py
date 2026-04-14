# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import json
import logging, pytz, re, threading
from typing import Any, List, Tuple, Union
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from ncclient.manager import Manager, connect_ssh
from common.method_wrappers.Decorator import MetricsPool, metered_subclass_method
from common.tools.client.RetryDecorator import delay_exponential
from common.type_checkers.Checkers import chk_length, chk_string, chk_type
from device.service.driver_api.Exceptions import UnsupportedResourceKeyException
from device.service.driver_api._Driver import _Driver
from .templates import compose_config, cli_compose_config, ufi_interface, cisco_interface
from .templates.VPN.common import seperate_port_config
from .templates.VPN.roadms import (
    create_optical_band, disable_media_channel, delete_optical_band, create_media_channel, 
)
from .templates.VPN.transponder import edit_optical_channel, change_optical_channel_status, disable_optical_channel
from .RetryDecorator import retry
from context.client.ContextClient import ContextClient
from common.proto.context_pb2 import OpticalConfig
from .templates.discovery_tool.transponders import  transponder_values_extractor
from .templates.discovery_tool.roadms import roadm_values_extractor



DEBUG_MODE = False
logging.getLogger('ncclient.manager').setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
logging.getLogger('ncclient.transport.ssh').setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
logging.getLogger('apscheduler.executors.default').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)
logging.getLogger('apscheduler.scheduler').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)
logging.getLogger('monitoring-client').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)

RE_GET_ENDPOINT_FROM_INTERFACE_KEY = re.compile(r'.*interface\[([^\]]+)\].*')
RE_GET_ENDPOINT_FROM_INTERFACE_XPATH = re.compile(r".*interface\[oci\:name\='([^\]]+)'\].*")


SAMPLE_EVICTION_SECONDS = 30.0 # seconds
SAMPLE_RESOURCE_KEY = 'interfaces/interface/state/counters'
transponder_filter_fields = ["frequency", "target-output-power", "operational-mode", "line-port", "admin-state"]
MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')
context_client= ContextClient()
port_xml_filter=f"/components/component[state[type='oc-platform-types:PORT']]/*"
transceiver_xml_filter="/components/component[state[type='oc-platform-types:TRANSCEIVER']]/*"

class NetconfSessionHandler:
    def __init__(self, address : str, port : int, **settings) -> None:
        self.__lock = threading.RLock()
        self.__connected = threading.Event()
        self.__address = address
        self.__port = int(port)
        self.__username         = settings.get('username')
        self.__password         = settings.get('password')
        self.__vendor           = settings.get('vendor',None)
        self.__version          = settings.get('version', "1")
        self.__key_filename     = settings.get('key_filename')
        self.__hostkey_verify   = settings.get('hostkey_verify', True)
        self.__look_for_keys    = settings.get('look_for_keys', True)
        self.__allow_agent      = settings.get('allow_agent', True)
        self.__force_running    = settings.get('force_running', False)
        self.__commit_per_rule  = settings.get('commit_per_rule', False)
        self.__device_params    = settings.get('device_params', {})
        self.__manager_params   = settings.get('manager_params', {})
        self.__nc_params        = settings.get('nc_params', {})
        self.__message_renderer = settings.get('message_renderer','jinja')
      
        self.__manager : Manager   = None
        self.__candidate_supported = False
       
    def connect(self):
        with self.__lock:
            self.__manager = connect_ssh(
                host=self.__address, port=self.__port, username=self.__username, password=self.__password,
                device_params=self.__device_params, manager_params=self.__manager_params, nc_params=self.__nc_params,
                key_filename=self.__key_filename, hostkey_verify=self.__hostkey_verify, allow_agent=self.__allow_agent,
                look_for_keys=self.__look_for_keys)
            self.__candidate_supported = ':candidate' in self.__manager.server_capabilities
            self.__connected.set()

    def disconnect(self):
        if not self.__connected.is_set(): return
        with self.__lock:
            self.__manager.close_session()

    @property
    def use_candidate(self): return self.__candidate_supported and not self.__force_running

    @property
    def commit_per_rule(self): return self.__commit_per_rule 

    @property
    def vendor(self): return self.__vendor

    @property
    def version(self): return self.__version

    @property
    def message_renderer(self): return self.__message_renderer

    @RETRY_DECORATOR
    def get(self, filter=None, with_defaults=None): # pylint: disable=redefined-builtin
        with self.__lock:
            config=self.__manager.get(filter=filter, with_defaults=with_defaults)
            return config

    @RETRY_DECORATOR
    def edit_config(
        self, config, target='running', default_operation=None, test_option=None,
        error_option=None, format='xml'                                             # pylint: disable=redefined-builtin
    ):
        response = None
        with self.__lock:
            response= self.__manager.edit_config(
                config, target=target, default_operation=default_operation, test_option=test_option,
                error_option=error_option, format=format)

        str_respones = str(response)  
        if re.search(r'<ok/>', str_respones):
           return None
        return str_respones

    @RETRY_DECORATOR
    def locked(self, target):
        return self.__manager.locked(target=target)

    @RETRY_DECORATOR
    def commit(self, confirmed=False, timeout=None, persist=None, persist_id=None):
        return self.__manager.commit(confirmed=confirmed, timeout=timeout, persist=persist, persist_id=persist_id)

DRIVER_NAME = 'oc'
METRICS_POOL = MetricsPool('Device', 'Driver', labels={'driver': DRIVER_NAME})
def edit_config(                                                                                                            # edit the configuration of openconfig devices
    netconf_handler : NetconfSessionHandler, logger : logging.Logger, resources : List[Tuple[str, Any]]
    ,conditions, delete=False,
    commit_per_rule=False, target='running', default_operation='merge', test_option=None, error_option=None,
    format='xml' 
):
    str_method = 'DeleteConfig' if delete else 'SetConfig'
    results = []
    new_config = {}
    str_config_messages=[]
    if netconf_handler.vendor is None : 
        if str_method == 'SetConfig':
            if (conditions['edit_type']=='optical-channel'):
                #transponder
                str_config_messages =  edit_optical_channel(resources)
            elif (conditions['edit_type']=='optical-band'):
                #roadm optical-band
                str_config_messages = create_optical_band(resources)
            else :
                #roadm media-channel
                str_config_messages=create_media_channel(resources)
        #Disabling of the Configuration         
        else:
            # Device type is Transponder
            if (conditions['edit_type'] == "optical-channel"):
                _,ports,_=seperate_port_config(resources)
                #str_config_messages=change_optical_channel_status(state="DISABLED",ports=ports)
                str_config_messages=disable_optical_channel(ports=ports)
                
            #  Device type is Roadm     
            elif (conditions['edit_type']=='optical-band'):    
                str_config_messages=delete_optical_band(resources)
            else :
                str_config_messages=disable_media_channel(resources)

        for str_config_message in str_config_messages:  
            # configuration of the received templates 
            if str_config_message is None: raise UnsupportedResourceKeyException("CONFIG")
            result= netconf_handler.edit_config(                                                                               # configure the device
                config=str_config_message, target=target, default_operation=default_operation,
                test_option=test_option, error_option=error_option, format=format)
            if commit_per_rule:
                netconf_handler.commit()                                                                               # configuration commit
            results.append(result)
               
    else : 
        if netconf_handler.vendor == "CISCO":
            if "L2VSI" in resources[0][1]:
                #Configure by CLI
                logger.warning("CLI Configuration")
                cli_compose_config(resources, 
                                delete=delete, 
                                host= netconf_handler._NetconfSessionHandler__address, 
                                user=netconf_handler._NetconfSessionHandler__username, 
                                passw=netconf_handler._NetconfSessionHandler__password)        
                for i,resource in enumerate(resources):
                    results.append(True)
            else: 
                logger.warning("CLI Configuration CISCO INTERFACE")
                cisco_interface(resources, 
                                delete=delete,
                                host= netconf_handler._NetconfSessionHandler__address
                                , user=netconf_handler._NetconfSessionHandler__username,
                                passw=netconf_handler._NetconfSessionHandler__password)        
                for i,resource in enumerate(resources):
                    results.append(True)
        elif netconf_handler.vendor == "UFISPACE": 
            #Configure by CLI
            logger.warning("CLI Configuration: {:s}".format(resources))
            ufi_interface(resources, 
                        delete=delete, 
                        host= netconf_handler._NetconfSessionHandler__address,
                        user=netconf_handler._NetconfSessionHandler__username,
                        passw=netconf_handler._NetconfSessionHandler__password)        
            for i,resource in enumerate(resources):
                results.append(True)
        else:
            for i,resource in enumerate(resources):
                str_resource_name = 'resources[#{:d}]'.format(i)
                try:
                    logger.debug('[{:s}] resource = {:s}'.format(str_method, str(resource)))
                    chk_type(str_resource_name, resource, (list, tuple))
                    chk_length(str_resource_name, resource, min_length=2, max_length=2)
                    resource_key,resource_value = resource
                    chk_string(str_resource_name + '.key', resource_key, allow_empty=False)
                    str_config_messages = compose_config(                                                                        
                                            resource_key, 
                                            resource_value, 
                                            delete=delete,
                                            vendor=netconf_handler.vendor, 
                                            message_renderer=netconf_handler.message_renderer)
                    for str_config_message in str_config_messages:                                                                
                        if str_config_message is None: raise UnsupportedResourceKeyException(resource_key)
                        logger.debug('[{:s}] str_config_message[{:d}] = {:s}'.format(
                        str_method, len(str_config_message), str(str_config_message)))
                        netconf_handler.edit_config(                                                                               
                            config=str_config_message, target=target, default_operation=default_operation,
                            test_option=test_option, error_option=error_option, format=format)
                        if commit_per_rule:
                            netconf_handler.commit()                                                                             
                        if 'table_connections' in resource_key:
                            time.sleep(5) 
                    
                    #results[i] = True
                    results.append(True)
                except Exception as e: # pylint: disable=broad-except
                    str_operation = 'preparing' if target == 'candidate' else ('deleting' if delete else 'setting')
                    msg = '[{:s}] Exception {:s} {:s}: {:s}'
                    logger.exception(msg.format(str_method, str_operation, str_resource_name, str(resource)))
                    #results[i] = e # if validation fails, store the exception
                    results.append(e)

            if not commit_per_rule:
                try:
                    netconf_handler.commit()
                except Exception as e: # pylint: disable=broad-except
                    msg = '[{:s}] Exception committing: {:s}'
                    str_operation = 'preparing' if target == 'candidate' else ('deleting' if delete else 'setting')
                    logger.exception(msg.format(str_method, str_operation, str(resources)))
                    results = [e for _ in resources] # if commit fails, set exception in each resource

    return [results,new_config]         

class OCDriver(_Driver):
    def __init__(self, address : str, port : int,device_uuid=None, **settings) -> None:
        super().__init__(DRIVER_NAME, address, port, **settings)
        self.__logger = logging.getLogger('{:s}:[{:s}:{:s}]'.format(str(__name__), str(self.address), str(self.port)))
        self.__lock = threading.Lock()

        self.__started = threading.Event()
        self.__terminate = threading.Event()
        self.__scheduler = BackgroundScheduler(daemon=True)
        self.__scheduler.configure(
            jobstores = {'default': MemoryJobStore()},
            executors = {'default': ThreadPoolExecutor(max_workers=1)}, 
            job_defaults = {'coalesce': False, 'max_instances': 3},
            timezone=pytz.utc)
        self._temp_address=f"{address}{port}"
       
        self.__netconf_handler = NetconfSessionHandler(self.address, self.port, **(self.settings))
        self.__type = self.settings.get("type","optical-transponder")
        self.__device_uuid = device_uuid
        self.Connect()
        
    def Connect(self) -> bool:
        with self.__lock:
            if self.__started.is_set(): return True
            self.__netconf_handler.connect()
            self.__scheduler.start()
            self.__started.set()
            return True

    def Disconnect(self) -> bool:
        with self.__lock:
            self.__terminate.set()
            if not self.__started.is_set(): return True
            self.__scheduler.shutdown()
            self.__netconf_handler.disconnect()
            return True

    @metered_subclass_method(METRICS_POOL)
    def GetInitialConfig(self) -> List[Tuple[str, Any]]:
        with self.__lock:
            return []

    @metered_subclass_method(METRICS_POOL)
    def GetConfig(self, resource_keys : List[str] = []) -> List[Tuple[str, Union[Any, None, Exception]]]:
        chk_type('resources', resource_keys, list)
        results = []
        opticalConfig= OpticalConfig()

        with self.__lock:
            config = {}
            transceivers = {}
            oc_values = {}
            ports_result = []
            oc_values["type"] = self.__type
            try:
                xml_data = self.__netconf_handler.get().data_xml
                
                if self.__type == "optical-transponder":
                    extracted_values = transponder_values_extractor(
                        data_xml=xml_data, resource_keys=transponder_filter_fields, dic=config
                    )
                    interfaces,optical_channels_params,channel_namespace,endpoints,ports_result=extracted_values
                    oc_values["channels"         ] = optical_channels_params
                    oc_values["interfaces"       ] =interfaces   
                    oc_values["transceivers"     ] = transceivers
                    oc_values["channel_namespace"] = channel_namespace
                    oc_values["endpoints"        ] = endpoints
                    oc_values["ports"            ] = ports_result
               
                else:
                    extracted_values = roadm_values_extractor(data_xml=xml_data, resource_keys=[], dic=config)
                    ports_result = extracted_values[0]
                    oc_values['optical_bands' ] = extracted_values[1]
                    oc_values['media_channels'] = extracted_values[2]

                #results.append((resource_key, e)) # if validation fails, store the exception    

            #///////////////////////// store optical configurtaion  ////////////////////////////////////////////////////////

                opticalConfig.config=json.dumps(oc_values)
                if self.__device_uuid is not None:
                    opticalConfig.device_id.device_uuid.uuid=self.__device_uuid
                results.append((f"/opticalconfigs/opticalconfig/{self.__device_uuid}",{"opticalconfig":opticalConfig}))
                # context_client.connect()    
                # config_id=context_client.SetOpticalConfig(opticalConfig)
                # context_client.close()
            except Exception as e: # pylint: disable=broad-except
                MSG = 'Exception retrieving {:s}'
                self.__logger.info("error from getConfig %s",e)
                self.__logger.exception(MSG.format(e))

        if len(ports_result) > 0: results.extend(ports_result)
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources : List[Tuple[str, Any]],conditions:dict) -> List[Union[bool, Exception]]:
        logging.info(f'from driver conditions {conditions}')
        if len(resources) == 0: return []
        results = []
        with self.__lock:
            if self.__netconf_handler.use_candidate:
                with self.__netconf_handler.locked(target='candidate'):
                    results = edit_config(
                        self.__netconf_handler, self.__logger, resources, conditions, target='candidate',
                        commit_per_rule=self.__netconf_handler.commit_per_rule
                    )
            else:
                results = edit_config(
                    self.__netconf_handler, self.__logger, resources, conditions=conditions
                )
        logging.info(f"results { results}")        
        return results

    @metered_subclass_method(METRICS_POOL)
    def DeleteConfig(
        self, resources : List[Tuple[str, Any]], conditions : dict,
    
    ) -> List[Union[bool, Exception]]:
        chk_type('resources', resources, list)
        if len(resources) == 0: return []

        with self.__lock:
            if self.__netconf_handler.use_candidate:
                with self.__netconf_handler.locked(target='candidate'):
                    results = edit_config(
                        self.__netconf_handler, self.__logger, resources, target='candidate', delete=True,
                        commit_per_rule=self.__netconf_handler.commit_per_rule, conditions=conditions
                    )
            else:
                results = edit_config(
                    self.__netconf_handler, self.__logger, resources, delete=True, conditions=conditions
                )
        return results
