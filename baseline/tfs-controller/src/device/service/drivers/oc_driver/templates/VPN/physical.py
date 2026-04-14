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

def seperate_port_config(resources:list,unwanted_keys:list[str])->list[list,dict,str]:
    config=[]
    ports={}
    index=None
    for item in resources :
      
        if (item['value'] is not None and (item['resource_key']  not in unwanted_keys)):
             config.append({'resource_key':item['resource_key'], 'value':item['value']} )
        #if (item['resource_key'] == 'destination_port' or item['resource_key'] == 'source_port') and item['value'] is not None:
        #     ports[item['resource_key']]=item['value']
        if (item['resource_key'] == 'destination_port' or item['resource_key'] == 'source_port'):
            ports[item['resource_key']]=item['value']
        if (item['resource_key']=='index' and item['value'] is not None)     :
            index=item['value']
      
    return [config,ports,index]


def create_optical_channel(resources:list[dict],ports:list[dict],config:list[dict] ):
  
    #unwanted_keys=['destination_port','source_port','channel_namespace','optical-band-parent','index', 'name','admin-state']
    results =[]
    data ={}
    data["channel_namespace"]=next((i["value"] for i in resources if i["resource_key"] == "channel_namespace"), None)
    #config,ports,index=seperate_port_config(resources,unwanted_keys=unwanted_keys)

    port_val = ""
    if 'destination_port' in ports and ports['destination_port'][0] is not None:
        port_val = ports['destination_port'][0]
    else:
        port_val = ports['source_port'][0]

    
    doc, tag, text = Doc().tagtext()
    #with tag('config'):
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
        with tag('components', xmlns="http://openconfig.net/yang/platform"):
            with tag('component'):
                with tag('name'):text("channel-{}".format(port_val))
                with tag('config'):
                    with tag('name'):text("channel-{}".format(port_val))
                #with tag('optical-channel', xmlns="http://example.com/flexscale-terminal-device"):
                with tag('optical-channel', xmlns=data["channel_namespace"]):
                    with tag('config'):
                        for resource in config:
                            with tag(resource['resource_key']):text(resource['value'])
    #    with tag('terminal-device', xmlns="http://openconfig.net/yang/terminal-device"):
    #        with tag('logical-channels'):
    #            with tag('channel'):
    #                with tag('index'):text("{}".format(port_val))
    #                with tag('config'):
    #                    with tag('index'):text("{}".format(port_val))
    #                    with tag('admin-state'):text("ENABLED")
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = ''
    )
    results.append(result)


    return results

def add_transceiver (transceiver_name:str):
 
    doc, tag, text = Doc().tagtext()
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
        with tag('components', xmlns="http://openconfig.net/yang/platform"):
            with tag('component'):
                with tag('name'):text(transceiver_name)
                with tag("config"):
                    with tag('name'):text(transceiver_name)
                with tag("state"):
                    with tag('name'):text(transceiver_name) 
                    with tag("type",('xmlns:oc-platform-types',"http://openconfig.net/yang/platform-types")):text("oc-platform-types:TRANSCEIVER")
                with tag("transceiver",xmlns="http://openconfig.net/yang/platform/transceiver"):
                    with tag("config"):
                        with tag("enabled"):text("true")
                        with tag("form-factor-preconf",("xmlns:oc-opt-types","http://openconfig.net/yang/transport-types")):text("oc-opt-types:QSFP56_DD_TYPE1")
                        with tag("ethernet-pmd-preconf",("xmlns:oc-opt-types","http://openconfig.net/yang/transport-types")):text("oc-opt-types:ETH_400GBASE_ZR")
                        with tag("fec-mode",("xmlns:oc-platform-types","http://openconfig.net/yang/platform-types")):text("oc-platform-types:FEC_AUTO")
                        with tag("module-functional-type",("xmlns:oc-opt-types","http://openconfig.net/yang/transport-types")):text("oc-opt-types:TYPE_DIGITAL_COHERENT_OPTIC")
                    with tag("state"):
                        with tag("enabled"):text("true")
                        with tag("form-factor-preconf",("xmlns:oc-opt-types","http://openconfig.net/yang/transport-types")):text("oc-opt-types:QSFP56_DD_TYPE1")
                        with tag("ethernet-pmd-preconf",("xmlns:oc-opt-types","http://openconfig.net/yang/transport-types")):text("oc-opt-types:ETH_400GBASE_ZR")
                        with tag("fec-mode",("xmlns:oc-platform-types","http://openconfig.net/yang/platform-types")):text("oc-platform-types:FEC_AUTO")
                        with tag("module-functional-type",("xmlns:oc-opt-types","http://openconfig.net/yang/transport-types")):text("oc-opt-types:TYPE_DIGITAL_COHERENT_OPTIC")
                        with tag("vendor"):text("Cisco")
                        with tag("vendor-part"):text("400zr-QSFP-DD")
                        with tag("vendor-rev"):text("01")
                        with tag("serial-no"):text("1567321")
                    with tag("physical-channels"):
                        with tag("channel"):
                            with tag("index"):text("1")
                            with tag("config"):
                                with tag("index"):text("1")
                                with tag("associated-optical-channel"):text("channel-4")    
    result = indent(
                doc.getvalue(),
                indentation = ' '*2,
                newline = ''
            )
         
   
    return result               
    
def create_optical_band (resources) :
    results =[]
    unwanted_keys=['destination_port','source_port','channel_namespace','frequency','optical-band-parent']
    config,ports,index= seperate_port_config(resources,unwanted_keys=unwanted_keys)
  
    doc, tag, text = Doc().tagtext()
    #with tag('config'):
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
      with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
        with tag('optical-bands',xmlns="http://flex-scale-project.eu/yang/flex-scale-mg-on"):
            n = 0
            if 'destination_port' in ports:
                n = len(ports['destination_port'])
            else:
                n = len(ports['source_port'])
            for i in range(0, n):
                #with tag('optical-band', operation="create"):
                with tag('optical-band'):
                    if index is not None:
                        with tag('index'):text(str(int(index)+i))
                    with tag('config'):
                        #if index is not None:
                        #    with tag('index'):text(str(int(index)+i))
                        for resource in config:       
                            if resource['resource_key'] == "index":
                                with tag('index'):text(str(int(index)+i))
                            else:
                                with tag(resource['resource_key']):text(resource['value'])
                        with tag('admin-status'):text('ENABLED')       
                        #with tag('fiber-parent'):text(ports['destination_port'] if 'destination_port' in ports else ports['source_port'])       
                    if ('destination_port' in ports) and (ports['destination_port'][i] is not None):        
                        with tag('dest'):
                            with tag('config'):
                                with tag('port-name'):text(ports['destination_port'][i])
                    if ('source_port' in ports) and (ports['source_port'][i] is not None):        
                        with tag('source'):
                            with tag('config'):  
                                with tag('port-name'):text(ports['source_port'][i])   
                            
                                
    result = indent(
                doc.getvalue(),
                indentation = ' '*2,
                newline = ''
            )
    results.append(result)
    return results
         
def create_media_channel (resources):
        results=[]
        unwanted_keys=['destination_port','source_port','channel_namespace','frequency','operational-mode', 'optical-band-parent']
        config,ports,index= seperate_port_config(resources,unwanted_keys=unwanted_keys)
    
        doc, tag, text = Doc().tagtext()
        #with tag('config'):
        with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
            with tag('wavelength-router', xmlns="http://openconfig.net/yang/wavelength-router"):
                with tag('media-channels'):
                    n = 0
                    if 'destination_port' in ports:
                        n = len(ports['destination_port'])
                    else:
                        n = len(ports['source_port'])
                    for i in range(0, n):
                        #with tag('channel', operation="create"):
                        with tag('channel'):
                            with tag('index'):text(str(int(index)+i))
                            with tag('config'):
                                #with tag('index'):text(index)
                                for resource in config:
                                   
                                    if resource['resource_key'] == "index":
                                        with tag('index'):text(str(int(index)+i))
                                    else:
                                        with tag(resource['resource_key']):text(resource['value'])
                            if ('destination_port' in ports) and (ports['destination_port'][i] is not None):         
                                with tag('dest'):
                                    with tag('config'):  
                                        with tag('port-name'):text(ports['destination_port'][i])   
                            if ('source_port' in ports) and (ports['source_port'][i] is not None):                    
                                with tag('source'):
                                        with tag('config'):  
                                            with tag('port-name'):text(ports['source_port'][i])     
                            
                            
        result = indent(
                    doc.getvalue(),
                    indentation = ' '*2,
                    newline = ''
                )
        results.append(result)
        return results
             

def change_optical_channel_status (channel_name:str,state:str,ports:list[dict]) :
    port_val=""
    if 'destination_port' in ports and ports['destination_port'][0] is not None:
        port_val = ports['destination_port'][0]
    else:
        port_val = ports['source_port'][0]

    results=[]
    doc, tag, text = Doc().tagtext()
    #with tag('config'):
    with tag('config',xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"):
      
        with tag('terminal-device',xmlns="http://openconfig.net/yang/terminal-device"):
            with tag("logical-channels"):
                with tag('channel'):
                    with tag('index'):text("{}".format(port_val))
                    with tag('config'):
                        with tag('admin-state'):text("{}".format(state))
                       
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = ''
    )
    results.append(result)


    return results


def edit_optical_channel (resources:list[dict]):
    unwanted_keys=['destination_port','source_port','channel_namespace','optical-band-parent','index', 'name','admin-state']
    config,ports,index=seperate_port_config(resources,unwanted_keys=unwanted_keys)
    results = []
    channel_name=next((i["value"] for i in resources if i["resource_key"]=="channel_name" and i["value"] != None),None)
    admin_state= next((i["value"] for i in resources if i["resource_key"]== "admin-state" and i["value"] != None) , None)
    
 
    if channel_name is not None :
        if (admin_state is not None):
            results.extend(change_optical_channel_status(channel_name=channel_name,state=admin_state,ports=ports))
    if admin_state is None :        
        results.extend(create_optical_channel(resources=resources,ports=ports,config=config)  )
    
    return results
