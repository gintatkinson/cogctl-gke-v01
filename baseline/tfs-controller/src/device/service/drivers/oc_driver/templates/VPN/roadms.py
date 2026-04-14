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
from .common  import seperate_port_config ,filter_config





 

         
def create_media_channel (resources):
    optical_band_namespaces="http://flex-scale-project.eu/yang/flex-scale-mg-on"
    results=[]
    unwanted_keys=['destination_port','source_port','channel_namespace'
                ,'frequency','operational-mode','target-output-power',
               "handled_flow","channel_num",'bidir']

    bidir = next(i['value'] for i in resources if i['resource_key'] == 'bidir')
    config,ports,index=filter_config(resources,unwanted_keys)
    logging.info(f'bidir {bidir}')

    n = 0

    for flow in ports:
        doc, tag, text = Doc().tagtext()
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
                    with tag('media-channels'):
                            src,dest=flow
                            with tag('channel', operation="create"):
                            #with tag('channel'):
                                with tag('index'):text(str(int(index)+n))
                                with tag('config'):
                                    #with tag('index'):text(index)
                                    for resource in config:
                                        
                                        if resource['resource_key'] == "index":
                                            with tag('index'):text(str(int(index)+n))
                                        elif resource['resource_key']== 'optical-band-parent'    :
                                            with tag('optical-band-parent',xmlns=optical_band_namespaces):text(int(resource['value'])+int(n))
                                        elif resource['resource_key']== 'admin-state'    :
                                            with tag('admin-status'):text(resource['value'])
                                        else:
                                            with tag(resource['resource_key']):text(resource['value'])

                                if src is not None and src != '0':                    
                                    with tag('source'):
                                            with tag('config'):  
                                                with tag('port-name'):text(src)     
                                if dest is not None and dest != '0':                    
                                    with tag('dest'):
                                            with tag('config'):  
                                                with tag('port-name'):text(dest)  
                                                       
        n+=1           
        result = indent(
                    doc.getvalue(),
                    indentation = ' '*2,
                    newline = ''
                )
        results.append(result)
        if not bidir  : break      
    return results
        


def create_optical_band (resources) :
    results =[]
    unwanted_keys=['destination_port','source_port','channel_namespace'
                   ,'frequency','optical-band-parent'
                   ,'handled_flow','bidir']
    config,ports,index= filter_config(resources,unwanted_keys=unwanted_keys)
    n = 0
    for flow in ports:
        doc, tag, text = Doc().tagtext()
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
                with tag('optical-bands',xmlns="http://flex-scale-project.eu/yang/flex-scale-mg-on"):
                        src,dest=flow
                        with tag('optical-band'):
                            if index is not None:
                                with tag('index'):text(str(int(index)+n))
                            with tag('config'):
                                for resource in config:       
                                    if resource['resource_key'] == "index":
                                        with tag('index'):text(str(int(index)+n))
                                    else:
                                        with tag(resource['resource_key']):text(resource['value'])
                                with tag('admin-status'):text('ENABLED')       
                                #with tag('fiber-parent'):text(ports['destination_port'] if 'destination_port' in ports else ports['source_port'])       
                            if dest is not None and dest != '0':        
                                with tag('dest'):
                                    with tag('config'):
                                        with tag('port-name'):text(dest)
                            if src is not None and src !='0':        
                                with tag('source'):
                                    with tag('config'):  
                                        with tag('port-name'):text(src)   
        n +=1                
        result = indent(
                    doc.getvalue(),
                    indentation = ' '*2,
                    newline = ''
                )
        results.append(result)
    return results


def disable_media_channel (resources):
    
    results=[]
    bidir = next(i['value'] for i in resources if i['resource_key'] == 'bidir')
    unwanted_keys=['destination_port','source_port'
                   ,'channel_namespace','frequency'
                   ,'operational-mode', 'optical-band-parent'
                   ,'bidir'
                   ]
    config,ports,index= seperate_port_config(resources,unwanted_keys=unwanted_keys)
    
    n = 0
    for flow in ports:
        doc, tag, text = Doc().tagtext()
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
                with tag('media-channels'):
                    with tag("channel",operation="delete"):
                        with tag('index'):text(str(int(index) + n))
                        with tag('config'):
                            with tag('index'):text(str(int(index) + n))

        n +=1                        
        result = indent(
                    doc.getvalue(),
                    indentation = ' '*2,
                    newline = ''
                )
        results.append(result)
        if not bidir: break
    return results
                        
def disable_optical_band (resources:list,state:str):
    results=[]
    unwanted_keys=['destination_port','source_port'
                   ,'channel_namespace','frequency'
                   ,'operational-mode', 'optical-band-parent'
                   ,"bidir"]
    _,_,index= seperate_port_config(resources,unwanted_keys=unwanted_keys)
    doc, tag, text = Doc().tagtext()
    #with tag('config'):
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
      with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
        with tag('optical-bands',xmlns="http://flex-scale-project.eu/yang/flex-scale-mg-on"):
            with tag('optical-band'):
                if index is not None:
                    with tag('index'):text(index)
                with tag('config'):
                    with tag('index'):text(index)
                    with tag('admin-status'):text(state)  
    result = indent(
                doc.getvalue(),
                indentation = ' '*2,
                newline = ''
            )
    results.append(result)
    return results          




def disable_optical_band_v2 (resources:list,state:str):
    results=[]
    unwanted_keys=['destination_port','source_port','channel_namespace','frequency','operational-mode', 'optical-band-parent']
    _,ports,index= seperate_port_config(resources,unwanted_keys=unwanted_keys)
    n = 0
    for flow in ports:
        doc, tag, text = Doc().tagtext()
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
                with tag('optical-bands',xmlns="http://flex-scale-project.eu/yang/flex-scale-mg-on"):
                    with tag('optical-band',operation="delete"):
                        if index is not None:
                            with tag('index'):text(str(int(index) + n))
                        with tag('config'):
                            with tag('index'):text(str(int(index) + n))
    
        n +=1                
        result = indent(
                    doc.getvalue(),
                    indentation = ' '*2,
                    newline = ''
                )
        results.append(result)
    return results               
               


def delete_optical_band (resources:list):
    results=[]
    unwanted_keys=['destination_port','source_port','channel_namespace','frequency','operational-mode', 'optical-band-parent']
    _,ports,index= seperate_port_config(resources,unwanted_keys=unwanted_keys)
    n = 0
    for key,v in ports.items():
        if isinstance(v,list): 
            if len(v)==1 and v[0] is None : continue
        else : 
            if v is None : continue    
        doc, tag, text = Doc().tagtext()
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
                with tag('optical-bands',xmlns="http://flex-scale-project.eu/yang/flex-scale-mg-on"):
                    with tag('optical-band',operation="delete"):
                        if index is not None:
                            with tag('index'):text(str(int(index) + n))
                        with tag('config'):
                            with tag('index'):text(str(int(index) + n))
    
        n +=1                
        result = indent(
                    doc.getvalue(),
                    indentation = ' '*2, 
                    newline = ''
                )
        results.append(result)
    return results                          
