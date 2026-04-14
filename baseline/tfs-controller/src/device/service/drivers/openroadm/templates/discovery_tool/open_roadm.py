  
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

import re,logging
import json
import lxml.etree as ET
from typing import Collection, Dict, Any
from common.proto.context_pb2 import  Location
from decimal import Decimal

def extract_roadm_circuits_pack (xml_data:str):
    xml_bytes = xml_data.encode("utf-8")
    root = ET.fromstring(xml_bytes)
    # with open('xml.log', 'w') as f:
    #      print(xml_bytes, file=f)

    namespace = {'oc': "http://org/openroadm/device"}

    circuits = root.findall('.//oc:circuit-packs',namespace)

    circuits_list =[]
    # print(f"component {components}")

    if (circuits is not None):
        for circuit  in circuits:
            circuit_info ={}
            circuit_ports=[]
            circuit_name = circuit.find(".//oc:circuit-pack-name",namespace)
            circuit_type=circuit.find(".//oc:circuit-pack-type",namespace)
            circuit_adminstrative_status=circuit.find(".//oc:administrative-state",namespace)
            circuit_equipment_state=circuit.find("./oc:equipment-state",namespace)
            circuit_mode=circuit.find("./oc:circuit-pack-mode",namespace)
            slot= circuit.find("./oc:slot",namespace)
            shelf= circuit.find("./oc:shelf",namespace)
            ports = circuit.findall("./oc:ports",namespace)
           
            
            if (ports is not None):
                
                for port in ports :
                    port_info={}
                    port_name=port.find('./oc:port-name',namespace)
                    port_qual= port.find("./oc:port-qual",namespace)
                    #if  port_qual is not None and port_qual.text  != 'roadm-external':continue
                    if port_name is not None :
                        port_info["port_name"]=port_name.text
                    if port_qual is not None :
                        port_info["port_qual"]=port_qual.text
                    circuit_ports.append(port_info)      
                    # if port_info["port_qual"] == 'roadm-external':
                    #    circuit_ports.append(port_info)            
            if (circuit_name is not None):
                circuit_info["circuit_pack_name"]=circuit_name.text
                circuit_info["interface_uuid"]=circuit_name.text
            if (circuit_type is not None):
                circuit_info["circuit_type"]=circuit_type.text
            if (circuit_adminstrative_status is not None):
                circuit_info["administrative_state"]=circuit_adminstrative_status.text
            if (circuit_equipment_state is not None):
                circuit_info["circuit_equipment_state"]=circuit_equipment_state.text
            if (circuit_mode is not None):
                circuit_info["circuit_mode"]=circuit_mode.text
            if (slot is not None):
                circuit_info["slot"]=slot.text
            if (shelf is not None):
                circuit_info["shelf"]=shelf.text      
            circuit_info["port"]=circuit_ports 
            if len(circuit_info["port"])==0 : continue                       
            circuits_list.append(circuit_info)   

    return circuits_list            



def extract_openroadm_info(xml_data:str):
    roadm_info={"node-id":None,"node-number":None,"node-type":None,'clli':None}
    xml_bytes = xml_data.encode("utf-8")
    root = ET.fromstring(xml_bytes)
    namespace = {'oc': "http://org/openroadm/device"}
    info = root.findall('.//oc:info',namespace)
    if info is not None :
        for i in info :
            node_id= i.find('.//oc:node-id',namespace)
            node_number= i.find('.//oc:node-number',namespace)
            node_type=i.find('.//oc:node-type',namespace)
            clli=i.find('.//oc:clli',namespace)
            if (node_id is not None):
                roadm_info['node-id']=node_id.text
            if (node_number is not None):
                roadm_info['node-number']=node_number.text
            if (node_type is not None):
                roadm_info['node-type']=node_type.text
            if (clli is not None):
                roadm_info['clli']=clli.text
 
    return roadm_info     


def extract_openroadm_interface (xml_data:str):
    or_config=[]
    or_interfaces=[]
    
    xml_bytes = xml_data.encode("utf-8")
    root = ET.fromstring(xml_bytes)
    # with open('xml.log', 'w') as f:
    #      print(xml_bytes, file=f)
    
    
    namespace = {'oc': "http://org/openroadm/device" 
                 , 'mc':"http://org/openroadm/media-channel-interfaces"
                 ,'nmc':"http://org/openroadm/network-media-channel-interfaces"
                 ,'or-type':'http://org/openroadm/interfaces'}
    
    interfaces = root.findall('.//oc:interface',namespace)
    for interface in interfaces :
      mc = interface.find('.//mc:mc-ttp',namespace)
      name = interface.find('.//oc:name',namespace)
      description = interface.find('.//oc:description',namespace)
      type=interface.find('.//oc:type',namespace)
      administrative_state=interface.find('.//oc:administrative-state',namespace)
      circuit_pack_name=interface.find('.//oc:supporting-circuit-pack-name',namespace)
      port=interface.find('.//oc:supporting-port',namespace)
      interface_list =interface.find('.//oc:supporting-interface-list',namespace)
      
      or_interfaces.append({
          'interface_list'        : name.text if name is not None else None,
          'administrative_state'  : administrative_state.text if administrative_state is not None else None,
          'circuit_pack_name'     : circuit_pack_name.text if circuit_pack_name is not None else None,
          'port'                  : port.text if port is not None else None ,
          'type'                  : type.text if type is not None else None
      })
      if mc is not None :
        frequency=None
        width=None
        min_frequency = mc.find('.//mc:min-freq',namespace)
        max_frequency = mc.find('.//mc:max-freq',namespace)
        if min_frequency is not None and max_frequency is not None:
            frequency = (Decimal(max_frequency.text) + Decimal(min_frequency.text) )/2
            width = int(( Decimal(max_frequency.text) - Decimal(min_frequency.text)) * 1000)
            
  
        mc= {
          'name'                : name.text if name is not None else None,
          'description'         : description.text if description is not None else None ,
          'type'                : "mc",
          'administrative_state': administrative_state.text if administrative_state is not None else None,
          'circuit_pack_name'   : circuit_pack_name.text if circuit_pack_name is not None else None,
          'port'                : port.text if port is not None else None ,
          'interface_list'      : interface_list.text if interface_list is not None else None,
           'frequency'          : str(frequency),
           'width'              : width
        } 
        or_config.append(mc)
        
      else :
        nmc = interface.find('.//nmc:nmc-ctp',namespace)
                  

        if nmc is not None :
          frequency = nmc.find('.//nmc:frequency',namespace)
          width=nmc.find('.//nmc:width',namespace)
          nmc= {
            'name'                : name.text if name is not None else None,
            'description'         : description.text if description is not None else None ,
            'type'                : "nmc" if interface_list is not None else "srg",
            'administrative_state': administrative_state.text if administrative_state is not None else None,
            'circuit_pack_name'   : circuit_pack_name.text if circuit_pack_name is not None else None,
            'port'                : port.text if port is not None else None ,
            'interface_list'      : interface_list.text if interface_list is not None else None,
            'frequency'           : frequency.text if frequency is not None else None,
            'width'               : width.text if width is not None else None
          } 
          or_config.append(nmc)
    return [or_interfaces,or_config]    
               

def  openroadm_values_extractor (data_xml:str,resource_keys:list,dic:dict):
    ports_result=[]
    openroadm_info= extract_openroadm_info(data_xml)
    circuits_list = extract_roadm_circuits_pack(data_xml)
    interfaces,config = extract_openroadm_interface(data_xml)
    dic["openroadm_info"]=openroadm_info
    dic["circuits"]=circuits_list
    dic['interfaces']=config
    
    for circuit in circuits_list :
        circuit_name=circuit['circuit_pack_name']
        location = Location()
        location.circuit_pack=circuit_name
        for port in circuit['port']:
            if port is not None and  'port_name' in port :
                resource_key = '/endpoints/endpoint[{:s}]'.format(port["port_name"])
                resource_value = {
                                   'uuid'    : port["port_name"]
                                 , 'type'    : port["port_qual"] if "port_qual" in port else None,
                                   'location': {"circuit_pack":location.circuit_pack}
                                 }
                ports_result.append((resource_key, resource_value))
      
    for interface in interfaces:
         existed=False
         circuit_name=interface['circuit_pack_name']
         interface_list=interface['interface_list']
         if 'circuits' in dic and len (dic['circuits']): 
            target= next((item for item in dic['circuits'] if item.get('circuit_pack_name') == circuit_name), None)
            if target : 
                target ['interface_list'] = interface_list
         location_interface=f'{interface_list}/{circuit_name}'
         port = interface["port"]
         type = interface['type']
         if port is not None:
                for i , (key,value) in enumerate(ports_result):
                   if value['uuid'] == port:
                       new_value = value
                       merged_interface=None
                       if 'interface' in value['location']:
                           merged_interface= f"{value['location']['interface']},{location_interface}"
                       if merged_interface is not None :
                           new_value['location']={"interface":merged_interface}
                       else :
                           new_value['location']={"interface":location_interface}
                              
                       ports_result[i]= (key,new_value )
                       existed=True
                       break
                
                if not existed:
                    resource_key = '/endpoints/endpoint[{:s}]'.format(port)
                    resource_value = {
                                      'uuid'    : f'{port}'
                                    , 'type'    : type ,
                                      'location': {"interface":location_interface}
                                    }
                    ports_result.append((resource_key, resource_value))

    return [dic,ports_result]            
