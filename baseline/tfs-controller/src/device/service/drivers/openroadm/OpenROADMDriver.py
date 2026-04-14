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


from .RetryDecorator import retry
from context.client.ContextClient import ContextClient
from common.proto.context_pb2 import OpticalConfig

from .templates.discovery_tool.open_roadm import openroadm_values_extractor
from .templates.Provisioning.openroadm import (
                                      or_handler 
                                      , srg_network_media_channel_handle
                                      ,handle_or_deconfiguration
                                      )

DEBUG_MODE = False
logging.getLogger('ncclient.manager').setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
logging.getLogger('ncclient.transport.ssh').setLevel(logging.DEBUG if DEBUG_MODE else logging.WARNING)
logging.getLogger('apscheduler.executors.default').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)
logging.getLogger('apscheduler.scheduler').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)
logging.getLogger('monitoring-client').setLevel(logging.INFO if DEBUG_MODE else logging.ERROR)



SAMPLE_EVICTION_SECONDS = 30.0 # seconds
SAMPLE_RESOURCE_KEY = 'interfaces/interface/state/counters'

MAX_RETRIES = 15
DELAY_FUNCTION = delay_exponential(initial=0.01, increment=2.0, maximum=5.0)
RETRY_DECORATOR = retry(max_retries=MAX_RETRIES, delay_function=DELAY_FUNCTION, prepare_method_name='connect')
context_client= ContextClient()


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
    commit_per_rule=False, target='running', test_option=None, error_option=None,
    format='xml' 
):
    str_method = 'DeleteConfig' if delete else 'SetConfig'
    results = []
    new_config = {}
    str_config_messages=[]
    if netconf_handler.vendor is None : 
        if str_method == 'SetConfig':

            if (conditions['edit_type']== 'or'):
                    str_config_messages,interfaces= or_handler(resources)
                    new_config['interfaces']= interfaces 

        #Disabling of the Configuration         
        else:
            if (conditions['edit_type']=='or'):    
                str_config_messages,interfaces=handle_or_deconfiguration(resources)   
                new_config["interfaces"]=interfaces
          
                
        for index,str_config_message in enumerate(str_config_messages):  
            # configuration of the received templates 
            if str_config_message is None: raise UnsupportedResourceKeyException("CONFIG")
            result= netconf_handler.edit_config(                                                                               # configure the device
                config=str_config_message, target='running',
                test_option=test_option, error_option=error_option, format=format)
            if commit_per_rule:
                if index == len(str_config_messages) - 1 :
                    netconf_handler.commit()                                                                               # configuration commit

            #results[i] = True
            results.append(result)
               
   

    return [results,new_config]         

class OpenROADMDriver(_Driver):
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
        self.__type = self.settings.get("type","openroadm")
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
                
               
                if (self.__type =='openroadm'):
                   extracted_values=openroadm_values_extractor(data_xml=xml_data, resource_keys=[], dic=oc_values)
                   ports_result = extracted_values[1]
                   oc_values['interfaces'] = extracted_values[0]['interfaces']
                   oc_values ['circuits'] = extracted_values[0]['circuits']
               


            #///////////////////////// store optical configurtaion  ////////////////////////////////////////////////////////

                opticalConfig.config=json.dumps(oc_values)
                if self.__device_uuid is not None:
                    opticalConfig.device_id.device_uuid.uuid=self.__device_uuid
                results.append((f"/opticalconfigs/opticalconfig/{self.__device_uuid}",{"opticalconfig":opticalConfig}))
               
            except Exception as e: # pylint: disable=broad-except
                MSG = 'Exception retrieving {:s}'
                self.__logger.info("error from getConfig %s",e)
                self.__logger.exception(MSG.format(e))

        if len(ports_result) > 0: results.extend(ports_result)
        return results

    @metered_subclass_method(METRICS_POOL)
    def SetConfig(self, resources : List[Tuple[str, Any]],conditions:dict) -> List[Union[bool, Exception]]:
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
