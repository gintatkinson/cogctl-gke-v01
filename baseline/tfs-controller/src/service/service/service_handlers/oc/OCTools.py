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

import logging, json
from typing import Dict, List, Optional, Tuple
from common.proto.context_pb2 import DeviceId, Service
from common.tools.object_factory.Device import json_device_id
from service.service.service_handler_api.Tools import get_endpoint_matching

log = logging.getLogger(__name__)



def convert_endpoints_to_flows(endpoints : List[Tuple[str, str, Optional[str]]])->Dict:

    entries = {}
    end = len(endpoints)
    i = 0
    bidir = 0
    log.debug("end={}".format(end))
    while(i < end):
        endpoint = endpoints[i]
        device_uuid, endpoint_uuid = endpoint[0:2]
        if device_uuid not in entries.keys():
            entries[device_uuid] = []
        if i == 0:
            entry_tuple = "0", endpoint_uuid
            entries[device_uuid].append(entry_tuple)
            next_endpoint = endpoints[i+1]
            next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
            if next_device_uuid == device_uuid :
                bidir = 1
                log.info("connection is bidirectional")
                entry_tuple = next_endpoint_uuid, "0"
                entries[device_uuid].append(entry_tuple)
                i = i + 1
            else:
                log.debug("connection is unidirectional")
        else:
            if not bidir:
                if i == end-1:
                    #is the last node
                    entry_tuple = endpoint_uuid, "0"
                    entries[device_uuid].append(entry_tuple)
                else:
                    #it is a transit node
                    next_endpoint = endpoints[i+1]
                    next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
                    if next_device_uuid == device_uuid:
                        entry_tuple = endpoint_uuid, next_endpoint_uuid
                        entries[device_uuid].append(entry_tuple)
                        i = i + 1
                    else:
                        log.debug("ERROR in unidirectional connection 4")
                        return {}
            else:
                log.debug("Ocheck i {}, {}, {}".format(i, i+1, end-1))
                if i + 1 == end-1:
                    log.debug("current OCTools step {}, {}, {}".format(i, device_uuid, endpoint_uuid))
                    #is the last node
                    entry_tuple = endpoint_uuid, "0"
                    entries[device_uuid].append(entry_tuple)
                    next_endpoint = endpoints[i+1]
                    log.debug("OCTools i+1 step {}, {}, {}".format(i+1, next_device_uuid, device_uuid))

                    next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
                    if next_device_uuid == device_uuid:
                        entry_tuple = "0", next_endpoint_uuid
                        entries[device_uuid].append(entry_tuple)
                        i = i + 1
                    else:
                        log.debug("ERROR in bidirectional connection 2")
                        return entries
                else:
                    log.debug("OCTools i+1+2+3 step {}, {}, {}".format(i+1, next_device_uuid, device_uuid))
                    #i+1
                    next_endpoint = endpoints[i+1]
                    next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
                    if next_device_uuid == device_uuid:
                        entry_tuple = endpoint_uuid, next_endpoint_uuid
                        entries[device_uuid].append(entry_tuple)
                    else:
                        log.debug("ERROR in bidirectional connection 3")
                        log.debug("{}, {}, {}".format(i, next_device_uuid, device_uuid))
                        return entries
                    #i+2
                    next_2_endpoint = endpoints[i+2]
                    next_2_device_uuid, next_2_endpoint_uuid = next_2_endpoint[0:2]                    
                    #i+3
                    next_3_endpoint = endpoints[i+3]
                    next_3_device_uuid, next_3_endpoint_uuid = next_3_endpoint[0:2]
                    log.debug(f"de {device_uuid} and i {i}")
                    log.debug(f"de2 {next_2_device_uuid} and dev3 {next_3_device_uuid}")
                    if next_2_device_uuid == next_3_device_uuid and next_3_device_uuid == device_uuid:
                        entry_tuple = next_2_endpoint_uuid, next_3_endpoint_uuid
                        entries[device_uuid].append(entry_tuple)
                        i = i + 3
                    else:
                        log.debug("ERROR in bidirection connection 4")
                        return {}
        i = i + 1
    return entries




def convert_or_endpoints_to_flows(endpoints : List[Tuple[str, str, Optional[str]]],bidir:bool)->Dict:

    entries = {}
    end = len(endpoints)
    i = 0
    if bidir:
        log.info(f"i starts with {i} ")
        i = i + 1
        while(i < end-2):
            #i
            endpoint = endpoints[i]
            device_uuid, endpoint_uuid = endpoint[0:2]

            if device_uuid not in entries.keys():
                entries[device_uuid] = []
            #i+1
            next_endpoint = endpoints[i+1]
            next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
            if next_device_uuid == device_uuid:
                entry_tuple = endpoint_uuid, next_endpoint_uuid
                entries[device_uuid].append(entry_tuple)
            else:

                return {} 
            #i+2
            
            next_2_endpoint = endpoints[i+2]
            next_2_device_uuid, next_2_endpoint_uuid = next_2_endpoint[0:2]                    
            #i+3
            next_3_endpoint = endpoints[i+3]
            next_3_device_uuid, next_3_endpoint_uuid = next_3_endpoint[0:2]
            log.info(f"dev {device_uuid} ")
            log.info(f"dev2 {next_2_device_uuid} dev3 {next_3_device_uuid} ")
            if next_2_device_uuid == next_3_device_uuid and next_3_device_uuid == device_uuid:
                entry_tuple = next_2_endpoint_uuid, next_3_endpoint_uuid
                entries[device_uuid].append(entry_tuple)
                i = i + 4
            else:

                return {}
    else:
        i +=1 
        while(i < end-1):
            #i
            endpoint = endpoints[i]
            device_uuid, endpoint_uuid = endpoint[0:2]

            if device_uuid not in entries.keys():
                entries[device_uuid] = []
            #i+1
            next_endpoint = endpoints[i+1]
            next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
            if next_device_uuid == device_uuid:
                entry_tuple = endpoint_uuid, next_endpoint_uuid
                entries[device_uuid].append(entry_tuple)
                i = i + 2
            else:
                return {}
        
    return entries



def ob_flows(endpoints : List[Tuple[str, str, Optional[str]]], bidir : int):
    entries = {}
    end = len(endpoints)
    i = 0
    if bidir:
        endpoint = endpoints[i]
        device_uuid, endpoint_uuid = endpoint[0:2]

        if device_uuid not in entries.keys():
            entries[device_uuid] = []
        entry_tuple = "0", endpoint_uuid
        entries[device_uuid].append(entry_tuple)
        next_endpoint = endpoints[i+1]
        next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
        if next_device_uuid == device_uuid:
            if next_device_uuid not in entries.keys():
                entries[next_device_uuid] = []
            entry_tuple = next_endpoint_uuid, "0"
            entries[next_device_uuid].append(entry_tuple)
        else:
            log.info("error expected device_id {}, found {}".format(device_uuid, next_device_uuid))
            return {} 
        i = i + 2
        if end > 4:
        
            while(i < end-2):
                #i
                endpoint = endpoints[i]
                device_uuid, endpoint_uuid = endpoint[0:2]
                log.debug("current OCTools step {}, {}, {}".format(i, device_uuid, endpoint_uuid))
                if device_uuid not in entries.keys():
                    entries[device_uuid] = []
                #i+1
                next_endpoint = endpoints[i+1]
                next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
                if next_device_uuid == device_uuid:
                    entry_tuple = endpoint_uuid, next_endpoint_uuid
                    entries[device_uuid].append(entry_tuple)
                else:
                    log.debug("ERROR in bidirectional ob")
                    log.debug("{}, {}, {}".format(i, next_device_uuid, device_uuid))
                    return {} 
                #i+2
                next_2_endpoint = endpoints[i+2]
                next_2_device_uuid, next_2_endpoint_uuid = next_2_endpoint[0:2]                    
                #i+3
                next_3_endpoint = endpoints[i+3]
                next_3_device_uuid, next_3_endpoint_uuid = next_3_endpoint[0:2]
                if next_2_device_uuid == next_3_device_uuid and next_3_device_uuid == device_uuid:
                    entry_tuple = next_2_endpoint_uuid, next_3_endpoint_uuid
                    entries[device_uuid].append(entry_tuple)
                    i = i + 4
                else:
                    log.debug("ERROR in bidirection ob")
                    return {}            
        endpoint = endpoints[i]
        device_uuid, endpoint_uuid = endpoint[0:2]
        if device_uuid not in entries.keys():
            entries[device_uuid] = []
        entry_tuple = endpoint_uuid, "0", 
        entries[device_uuid].append(entry_tuple)
        next_endpoint = endpoints[i+1]
        next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
        if next_device_uuid == device_uuid:
            if next_device_uuid not in entries.keys():
                entries[next_device_uuid] = []
            entry_tuple = "0", next_endpoint_uuid
            entries[next_device_uuid].append(entry_tuple)
        else:
            log.debug("error expected device_id {}, found {}".format(device_uuid, next_device_uuid))
    else:
        endpoint = endpoints[i]
        device_uuid, endpoint_uuid = endpoint[0:2]

        if device_uuid not in entries.keys():
            entries[device_uuid] = []
        entry_tuple = "0", endpoint_uuid
        entries[device_uuid].append(entry_tuple)
        i = i + 1
        if end > 2:

            while(i < end-1):
                #i
                endpoint = endpoints[i]
                device_uuid, endpoint_uuid = endpoint[0:2]

                if device_uuid not in entries.keys():
                    entries[device_uuid] = []
                #i+1
                next_endpoint = endpoints[i+1]
                next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
                if next_device_uuid == device_uuid:
                    entry_tuple = endpoint_uuid, next_endpoint_uuid
                    entries[device_uuid].append(entry_tuple)
                else:
                    log.debug("ERROR in bidirectional ob")
                    log.debug("{}, {}, {}".format(i, next_device_uuid, device_uuid))
                    return {}
                i = i + 2 
        next_endpoint = endpoints[i]
        next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
        if next_device_uuid not in entries.keys():
            entries[next_device_uuid] = []
        entry_tuple = next_endpoint_uuid, "0"
        entries[next_device_uuid].append(entry_tuple)
    return entries
    
             
def conn_flows(endpoints : List[Tuple[str, str, Optional[str]]], bidir : int):
    entries = {}
    end = len(endpoints)
    i = 0
    #tx tp
    endpoint = endpoints[i]
    device_uuid, endpoint_uuid = endpoint[0:2]

    if device_uuid not in entries.keys():
        entries[device_uuid] = []
    entry_tuple = "0", endpoint_uuid
    entries[device_uuid].append(entry_tuple)
    i = i + 1
    #if bidir reading 4 endpoints per node
    if bidir:
        log.info(f"i starts with {i} ")
        i = i + 1
        while(i < end-2):
            #i
            endpoint = endpoints[i]
            device_uuid, endpoint_uuid = endpoint[0:2]

            if device_uuid not in entries.keys():
                entries[device_uuid] = []
            #i+1
            next_endpoint = endpoints[i+1]
            next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
            if next_device_uuid == device_uuid:
                entry_tuple = endpoint_uuid, next_endpoint_uuid
                entries[device_uuid].append(entry_tuple)
            else:

                return {} 
            #i+2
            
            next_2_endpoint = endpoints[i+2]
            next_2_device_uuid, next_2_endpoint_uuid = next_2_endpoint[0:2]                    
            #i+3
            next_3_endpoint = endpoints[i+3]
            next_3_device_uuid, next_3_endpoint_uuid = next_3_endpoint[0:2]
            log.info(f"dev {device_uuid} ")
            log.info(f"dev2 {next_2_device_uuid} dev3 {next_3_device_uuid} ")
            if next_2_device_uuid == next_3_device_uuid and next_3_device_uuid == device_uuid:
                entry_tuple = next_2_endpoint_uuid, next_3_endpoint_uuid
                entries[device_uuid].append(entry_tuple)
                i = i + 4
            else:

                return {}
    else:
        while(i < end-1):
            #i
            endpoint = endpoints[i]
            device_uuid, endpoint_uuid = endpoint[0:2]

            if device_uuid not in entries.keys():
                entries[device_uuid] = []
            #i+1
            next_endpoint = endpoints[i+1]
            next_device_uuid, next_endpoint_uuid = next_endpoint[0:2]
            if next_device_uuid == device_uuid:
                entry_tuple = endpoint_uuid, next_endpoint_uuid
                entries[device_uuid].append(entry_tuple)
                i = i + 2
            else:
                return {}
    #rx tp   
    endpoint = endpoints[i]
    device_uuid, endpoint_uuid = endpoint[0:2]
    if device_uuid not in entries.keys():
        entries[device_uuid] = []
    entry_tuple = endpoint_uuid, "0", 
    entries[device_uuid].append(entry_tuple)
    return entries



def endpoints_to_flows(endpoints : List[Tuple[str, str, Optional[str]]], bidir : int, is_ob: bool)->Dict:
    if is_ob:
        entries = ob_flows(endpoints, bidir)
    else:
        entries = conn_flows(endpoints, bidir)
        
    return entries

def get_device_endpint_name(endpoint_uuid : str, device_uuid : str, task_executor) -> Tuple:
    device_obj = task_executor.get_device(DeviceId(**json_device_id(device_uuid)))
    endpoint_obj = get_endpoint_matching(device_obj, endpoint_uuid)
    endpoint_name = endpoint_obj.name
    return (device_obj.name, endpoint_name)

def handle_flows_names(task_executor, flows : dict) -> Dict:
    new_flows = {}
    for index, (device_uuid_key, device_endpoints_list) in enumerate(flows.items()):
        for endpoint_tupple in device_endpoints_list:
            source_port = None 
            destination_port = None
            device_name = ""
            source_endpoint, destination_endpoint = endpoint_tupple
            if source_endpoint != '0':
                if get_device_endpint_name(source_endpoint, device_uuid_key, task_executor) is not None:
                    device_name, source_port = get_device_endpint_name(
                        source_endpoint, device_uuid_key, task_executor
                    )
            if destination_endpoint != '0':
                if get_device_endpint_name(destination_endpoint, device_uuid_key, task_executor) is not None:
                    device_name, destination_port = get_device_endpint_name(
                        destination_endpoint, device_uuid_key, task_executor
                    )
            if device_name not in new_flows:
                new_flows[device_name] = []
            new_flows[device_name].append((source_port, destination_port))
    return new_flows

def check_media_channel_existance(service : Service):
    has_media_channel = False
    for config_rule in service.service_config.config_rules:
        if isinstance(config_rule.custom.resource_value, str):
           settings = json.dumps(config_rule.custom.resource_value)
           if "flow_id" in settings:
               has_media_channel = True
    return has_media_channel
