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

import logging


def seperate_port_config(resources:list,unwanted_keys=[])->list[list,dict,str]:
    config=[]
    ports={}
    index=None
    for item in resources :
        if len(unwanted_keys)>0:
            if (item['value'] is not None and (item['resource_key']  not in unwanted_keys)):
                config.append({'resource_key':item['resource_key'], 'value':item['value']} )
        #if (item['resource_key'] == 'destination_port' or item['resource_key'] == 'source_port') and item['value'] is not None:
        #     ports[item['resource_key']]=item['value']
        if (item['resource_key'] == 'destination_port' or item['resource_key'] == 'source_port'):
            ports[item['resource_key']]=item['value']
        if (item['resource_key']=='index' and item['value'] is not None)     :
            index=item['value']
    logging.info(f"seperate_port_config {ports}")  
    return [config,ports,index]

def extract_ports (resources:list):
    if len(resources) ==0 :return 
    ports=[]
    flow=next((i for i in resources if i['resource_key']=='handled_flow'),None)
    if flow is not None:
        ports = flow['value']
    return ports 

def filter_config(resources:list,unwanted_keys=[])->list[list,dict,str]:
    config=[]
    ports=()
    index=None
    for item in resources :
        if len(unwanted_keys)>0:
            if (item['value'] is not None and (item['resource_key']  not in unwanted_keys)):
                config.append({'resource_key':item['resource_key'], 'value':item['value']} )
        if (item['resource_key']=='index' and item['value'] is not None)     :
            index=item['value']        
        #if (item['resource_key'] == 'destination_port' or item['resource_key'] == 'source_port') and item['value'] is not None:
        #     ports[item['resource_key']]=item['value']
    ports = extract_ports(resources=resources)
    logging.info(f"filter_config {ports}")    
    return [config,ports,index]


def convert_Thz (freq_hz:int)->int : 
    freq_thz = freq_hz / 1_000_000
    freq_thz_rounded = round(freq_thz, 2) 
    return freq_thz_rounded
