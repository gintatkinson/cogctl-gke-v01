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

from .common  import seperate_port_config

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
    

def create_optical_channel(resources:list[dict],ports:list[dict],config:list[dict] ):
  
    # unwanted_keys=['bidir','source_port','destination_port','handled_flow','name','channel_namespace','admin-state'
    #                ,'optical-band-parent']
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
                with tag('optical-channel',xmlns=data["channel_namespace"]):
                    with tag('config'):
                        for resource in config:
                            with tag(resource['resource_key']):text(resource['value'])
        with tag('terminal-device', xmlns="http://openconfig.net/yang/terminal-device"):
            with tag('logical-channels'):
                with tag('channel'):
                    with tag('index'):text("{}".format(port_val))
                    with tag('config'):
                        with tag('index'):text("{}".format(port_val))
                        with tag('admin-state'):text("ENABLED")
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = ''
    )
    results.append(result)


    return results


def disable_optical_channel(ports:list[dict] ):
  
    # unwanted_keys=['bidir','source_port','destination_port','handled_flow','name','channel_namespace','admin-state'
    #                ,'optical-band-parent']
    results =[]
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
                with tag('optical-channel',xmlns="http://openconfig.net/yang/terminal-device"):
                    with tag('config'):
                        with tag('frequency'):text('199000000')
                        with tag('target-output-power'):text('-40')
                        with tag('operational-mode'):text('0')                 
        with tag('terminal-device', xmlns="http://openconfig.net/yang/terminal-device"):
            with tag('logical-channels'):
                with tag('channel'):
                    with tag('index'):text("{}".format(port_val))
                    with tag('config'):
                        with tag('index'):text("{}".format(port_val))
                        with tag('admin-state'):text("DISABLED")
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = ''
    )
    results.append(result)


    return results



def change_optical_channel_status (state:str,ports:list[dict]) :
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

    unwanted_keys=['destination_port','source_port','channel_namespace'
                   ,'optical-band-parent','index', 'name','admin-state','handled_flow','bidir']
    config,ports,index=seperate_port_config(resources,unwanted_keys=unwanted_keys)
    results = []
    # channel_name=next((i["value"] for i in resources if i["resource_key"]=="channel_name" and i["value"] != None),None)
    # admin_state= next((i["value"] for i in resources if i["resource_key"]== "admin-state" and i["value"] != None) , None)
    


    # results.extend(change_optical_channel_status(state=admin_state,ports=ports))
    # else :    

    results.extend(create_optical_channel(resources=resources,ports=ports,config=config)  )
    
    return results
