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



from yattag import Doc, indent
import logging
from .common  import seperate_port_config ,filter_config ,convert_Thz
from decimal import Decimal



or_device_ns_1='urn:ietf:params:xml:ns:netconf:base:1.0'
or_device_ns="http://org/openroadm/device"
 

def define_interface_name_old (type:str,interface_list:str,freq:int)->str:
    
    if interface_list :
        interface_str = interface_list.split('-')
        port_rank=''
        port_type=''
        if (len(interface_str)==4):
            port_rank=interface_str[1]
            port_type=interface_str[3]
        elif (len(interface_str)==5):
            port_rank=interface_str[2]
            port_type=interface_str[3]
        elif (len(interface_str)==2):
            port_rank=interface_str[0]
            port_type=interface_str[1]
            
        else :
            port_rank=interface_list
            port_type=interface_list+'type'    
            
            
        return f'{type.upper()}-{port_rank}-{port_type}-{freq}' 
    return ''
        
def define_interface_name (type:str,port:str,freq:int)->str:
         
    return f'{type.upper()}-{port.upper()}-{freq}' 
   

       
def create_network_media_channel (resources,port,cross_conn_resources,interfaces):
    
    band=next((r for r in resources if r['resource_key']== 'band'),None)
    frequency_dict=next((r for r in resources if r['resource_key']== 'frequency'),None)
    freq_thz=None
    if frequency_dict and frequency_dict['value']:
        freq_thz=frequency_dict['value']
        
    doc, tag, text = Doc().tagtext()
   
    if port: 
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
          with tag('org-openroadm-device', ('xmlns',or_device_ns)): 
            #port,i_list,circuit=infer_opposite_port(i,interface_list["value"])
            interface_list =next((r for r in resources if r['resource_key']== 'interface_list'+'-'+port),None)
            circuit_pack =next((r for r in resources if r['resource_key']=='supporting-circuit-pack-name'+'-'+port),None)
            nmc_name = define_interface_name(f'nmc',port,freq_thz)
            cross_conn_resources[f'nmc_name_{port}']=nmc_name
            cross_conn_resources[f'nmc_port_{port}']=port
            cross_conn_resources['count']+=1
            interfaces.append({
                    "name"                : nmc_name,
                    "type"                : 'nmc',
                    "administrative_state": 'inService',
                    "circuit_pack_name"   : circuit_pack["value"],
                    "port"                : port,
                    "interface_list"      : interface_list["value"],
                    "frequency"           : freq_thz,
                    "width"               : band['value'],
                    "roadm_uuid"          : ""
                })

            with tag('interface'):
                
                    with tag('name'):text(nmc_name)
                    with tag('description'):text(f'Media-channel-{freq_thz}THz')
                    with tag('type'):text("openROADM-if:networkMediaChannelConnectionTerminationPoint")
                    with tag('administrative-state'):text("inService")
                    with tag('supporting-circuit-pack-name'):text(circuit_pack['value'])
                    with tag('supporting-port'):text(port)
                    with tag('supporting-interface-list'):text(interface_list["value"])
                    with tag('nmc-ctp',xmlns="http://org/openroadm/network-media-channel-interfaces"):
                        with tag('frequency'):text(freq_thz)
                        with tag('width'):text(band['value'])
                      
    result = indent(
                    doc.getvalue(),
                    indentation = ' '*2,
                    newline = ''
                )

    return result


def or_create_media_channel (resources,port,cross_conn_resources,interfaces):
    frequency_dict=next((r for r in resources if r['resource_key']== 'frequency'),None)
    freq_thz=None
    if frequency_dict and frequency_dict['value']:
        freq_thz=frequency_dict['value']
    band=next((r for r in resources if r['resource_key']== 'band'),None)
    min_freq=  int(Decimal(frequency_dict["value"])) - (int(band["value"])/2)
    max_freq =int(Decimal(frequency_dict["value"])) + (int(band["value"])/2)
    results=[]
    doc, tag, text = Doc().tagtext()
                
    if port:
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('org-openroadm-device', ('xmlns',or_device_ns)): 
        
                interface_list =next((r for r in resources if r['resource_key']== 'interface_list'+'-'+port),None)
                circuit_pack =next((r for r in resources if r['resource_key']=='supporting-circuit-pack-name'+'-'+port),None)
                mc_name = define_interface_name(f'mc-ttp',port,freq_thz)
                interfaces.append({
                    "name"                 : mc_name,
                    "type"                 : 'mc',
                    "administrative_state" : 'inService',
                    "circuit_pack_name"    : circuit_pack["value"],
                    "port"                 : port,
                    "interface_list"       : interface_list["value"],
                    "frequency"            : freq_thz,
                    "width"                : band["value"],
                    "roadm_uuid"           : ""
                })

                with tag('interface'):
                    
                        with tag('name'):text(mc_name)
                        with tag('description'):text(f'Media-channel-{freq_thz}THz')
                        with tag('type'):text("openROADM-if:mediaChannelTrailTerminationPoint")
                        with tag('administrative-state'):text("inService")
                        with tag('supporting-circuit-pack-name'):text(circuit_pack["value"])
                        with tag('supporting-port'):text(port)
                        with tag('supporting-interface-list'):text(interface_list["value"])
                        with tag('mc-ttp',xmlns="http://org/openroadm/media-channel-interfaces"):
                            with tag('max-freq'):text(max_freq)
                            with tag('min-freq'):text(min_freq)
    result = indent(
                    doc.getvalue(),
                    indentation = ' '*2,
                    newline = ''
                )
    
    results.append(result)
    nmc_result = create_network_media_channel(resources,port,cross_conn_resources,interfaces)
    results.append(nmc_result)
    return results
 
 
 
 
def create_cross_connection (resources):
  
  src,dst = resources['ports']
  connection_name=resources[f'nmc_name_{src}']+' to '+resources[f'nmc_name_{dst}']
  doc, tag, text = Doc().tagtext()
  with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):  
    with tag('org-openroadm-device', ('xmlns',or_device_ns)):
        with tag ('roadm-connections'):
                with tag('connection-name'):text(connection_name)
                with tag('opticalControlMode'):text('off')
                with tag('target-output-power'):text('0')
                with tag('source'):
                    with tag('src-if'):text(resources[f'nmc_name_{src}'])
                with tag('destination')    :
                    with tag('dst-if'):text(resources[f'nmc_name_{dst}'])

  result = indent(
                  doc.getvalue(),
                  indentation = ' '*2,
                  newline = ''
              )
  
  # logging.info(f"nmc message {results}")
  return result
  
 
        

def srg_network_media_channel_handle (resources,port,cross_conn_resources,interfaces):


  band=next((r for r in resources if r['resource_key']== 'band'),None)
  frequency_dict=next((r for r in resources if r['resource_key']== 'frequency'),None)
  freq_thz= frequency_dict["value"]
  doc, tag, text = Doc().tagtext()
  if port : 
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('org-openroadm-device', ('xmlns',or_device_ns)):

                interface_list =next((r for r in resources if r['resource_key']== 'interface_list'+'-'+port),None)
                circuit_pack =next((r for r in resources if r['resource_key']=='supporting-circuit-pack-name'+'-'+port),None)
                srg_name = define_interface_name(f'nmc-srg',port,freq_thz)
                cross_conn_resources[f'nmc_name_{port}']=srg_name
                cross_conn_resources[f'nmc_port_{port}']=port
                cross_conn_resources['count']+=1
                
                interfaces.append({
                        "name"                 : srg_name,
                        "type"                 : 'srg',
                        "administrative_state" : 'inService',
                        "circuit_pack_name"    : circuit_pack["value"],
                        "port"                 : port,
                        "interface_list"       : interface_list["value"],
                        "frequency"            : freq_thz, 
                        "roadm_uuid"           : ""
                    })

                with tag('interface'):
                    
                        with tag('name'):text(srg_name)
                        with tag('description'):text(f'Network-Media-Channel-CTP-{freq_thz}THz')
                        with tag('type'):text("openROADM-if:networkMediaChannelConnectionTerminationPoint")
                        with tag('administrative-state'):text("inService")
                        with tag('supporting-circuit-pack-name'):text(circuit_pack["value"])
                        with tag('supporting-port'):text(port)
                        with tag('nmc-ctp',xmlns="http://org/openroadm/network-media-channel-interfaces"):
                                with tag('frequency'):text(freq_thz)
                                with tag('width'):text(band['value'])   
  result = indent(
                  doc.getvalue(),
                  indentation = ' '*2,
                  newline = ''
              )

  return result

def delete_interface (interface_name) : 
    doc, tag, text = Doc().tagtext()
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
        with tag('org-openroadm-device', xmlns=or_device_ns, **{'xmlns:nc': or_device_ns_1}):
            with tag('interface', **{'nc:operation': 'delete'}):
                with tag('name'):text(interface_name)
        
    result = indent(
                        doc.getvalue(),
                        indentation = ' '*2,
                        newline = ''
                    )  
    return result
    
def delete_coss_connection (resources) : 

    src,dst = resources['ports']
    connection_name=resources[f'nmc_name_{src}']+' to '+resources[f'nmc_name_{dst}']
    doc, tag, text = Doc().tagtext()
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
        with tag('org-openroadm-device', xmlns=or_device_ns, **{'xmlns:nc': or_device_ns_1}):    
            with tag ('roadm-connections', **{'nc:operation': 'delete'}):
                with tag('connection-name'):text(connection_name)
   
    result = indent(
                  doc.getvalue(),
                  indentation = ' '*2,
                  newline = ''
              ) 
               
    return result

def or_handler (resources): 

  _,ports,_= filter_config(resources,unwanted_keys=[])
  edit_templates= []
  interfaces= []
  cross_conn_resources={"count":0}
  doc, tag, text = Doc().tagtext()
  logging.info(f'or_handler {resources} ')
  with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
    with tag('org-openroadm-device', ('xmlns',or_device_ns)):
        for lst_i in [list(j) for j in ports ] :
            for i in lst_i:
            
                if 'SRG' in i :
                      edit_templates.append (
                          srg_network_media_channel_handle(resources,i,cross_conn_resources,interfaces)
                      )
                
                else : 
                
                    edit_templates.extend(or_create_media_channel(resources ,i,cross_conn_resources,interfaces))

            if  cross_conn_resources['count']==2 : 
                cross_conn_resources['ports']=lst_i
                edit_templates.append(create_cross_connection(cross_conn_resources))
                cross_conn_resources["count"]=0     
  return (edit_templates,interfaces)                      
                  
  
def delete_mc (mc_interfaces): 
    
    results = []
    for i in mc_interfaces:
        results.append( delete_interface(i))
    return results 
    
def handle_or_deconfiguration (resources): 

    _,ports,_= filter_config(resources,unwanted_keys=[])
    edit_templates= []
    interfaces= []
    mcs_to_delete=[]
    cross_conn_resources={"count":0}

    for lst_i in [list(j) for j in ports ] :
        for p in lst_i : 
            if p :
                if 'SRG' in p : 
                    interface_list = interface_list =next((r for r in resources if r['resource_key']== 'interface_name'+'-'+p+'-srg'),None)
                    if interface_list : 
                        cross_conn_resources[f'nmc_name_{p}']=interface_list['value']
                        cross_conn_resources[f'nmc_port_{p}']=p
                        cross_conn_resources['count']+=1
                        interfaces.append({
                            'interface_name':interface_list['value']
                        })
                        
                        edit_templates.append(delete_interface(interface_list['value']))
                else : 
                    nmc_interface = interface_list =next((r for r in resources if r['resource_key']== 'interface_name'+'-'+p+'-nmc'),None)
                    if nmc_interface :
                        cross_conn_resources[f'nmc_name_{p}']=nmc_interface['value']
                        cross_conn_resources[f'nmc_port_{p}']=p
                        cross_conn_resources['count']+=1
                        mc_interface =  nmc_interface['value'].replace('NMC',"MC-TTP") 
                        interfaces.extend([{
                            'interface_name':nmc_interface['value']
                        },
                                        {
                            'interface_name':mc_interface
                        }]
                                        
                                        )
                        mcs_to_delete.append(mc_interface)
                        #delete_interface(mc_interface,doc,tag,text)
                        edit_templates.append(delete_interface(nmc_interface['value']))
        if  cross_conn_resources['count']==2 : 
            logging.info("should cross connection be initiated")
            cross_conn_resources['ports']=lst_i
            edit_templates.insert(0,delete_coss_connection(cross_conn_resources))
            cross_conn_resources["count"]=0      
    edit_templates.extend(delete_mc(mcs_to_delete))                          
    return (edit_templates,interfaces)                
