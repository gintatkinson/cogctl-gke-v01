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

import json, logging, lxml.etree as ET, re
import time
from typing import Any, Dict, Optional
from jinja2 import Environment, PackageLoader, select_autoescape
import paramiko
from .Tools import generate_templates

LOGGER = logging.getLogger(__name__)



LOGGER = logging.getLogger(__name__)
RE_REMOVE_FILTERS = re.compile(r'\[[^\]]+\]')
RE_REMOVE_FILTERS_2 = re.compile(r'\/[a-z]+:')
EMPTY_CONFIG = '<config></config>'
EMPTY_FILTER = '<filter></filter>'
JINJA_ENV = Environment(loader=PackageLoader('device.service.drivers.openconfig'), autoescape=select_autoescape())

"""
# Method Name: compose_config
  
# Parameters:
  - resource_key:    [str]  Variable to identify the rule to be executed.
  - resource_value:  [str]  Variable with the configuration parameters of the rule to be executed.
  - delete:          [bool] Variable to identify whether to create or delete the rule.
  - vendor:          [str]  Variable to identify the vendor of the equipment to be configured.
  - message_renderer [str]  Variable to dientify template generation method. Can be "jinja" or "pyangbind".
  
# Functionality:
  This method calls the function obtains the equipment configuration template according to the value of the variable "message_renderer".
  Depending on the value of this variable, it gets the template with "jinja" or "pyangbind". 
  
# Return:
  [dict] Set of templates obtained according to the configuration method
"""

def compose_config( # template generation
    resource_key : str, resource_value : str, delete : bool = False, vendor : Optional[str] = None, message_renderer = str
) -> str:

    if (message_renderer == "pyangbind"):
        templates = (generate_templates(resource_key, resource_value, delete, vendor))
        return [
            '<config>{:s}</config>'.format(template) # format correction
            for template in templates
            ]

    elif (message_renderer == "jinja"):
        templates = []
        template_name = '{:s}/edit_config.xml'.format(RE_REMOVE_FILTERS.sub('', resource_key))
        templates.append(JINJA_ENV.get_template(template_name))
        data : Dict[str, Any] = json.loads(resource_value)

        operation = 'delete' if delete else 'merge' # others
        #operation = 'delete' if delete else '' # ipinfusion?

        return [
            '<config>{:s}</config>'.format(
            template.render(**data, operation=operation, vendor=vendor).strip())
            for template in templates
            ]
        
    else:
        raise ValueError('Invalid message_renderer value: {}'.format(message_renderer)) 

"""
# Method Name: cli_compose_config
  
# Parameters:
  - resource_key:    [str]  Variable to identify the rule to be executed.
  - resource_value:  [str]  Variable with the configuration parameters of the rule to be executed.
  - delete:          [bool] Variable to identify whether to create or delete the rule.
  - vendor:          [str]  Variable to identify the vendor of the equipment to be configured.
  - message_renderer [str]  Variable to dientify template generation method. Can be "jinja" or "pyangbind".
  
# Functionality:
  This method calls the function obtains the equipment configuration template according to the value of the variable "message_renderer".
  Depending on the value of this variable, it gets the template with "jinja" or "pyangbind". 
  
# Return:
  [dict] Set of templates obtained according to the configuration method
"""

def cli_compose_config(resources, delete: bool, host: str, user: str, passw: str):     #Method used for configuring via CLI directly L2VPN in CISCO devices
      
    key_value_data = {}

    for path, json_str in resources:
        key_value_data[path] = json_str

    # Iterate through the resources and extract parameter values dynamically
    for path, json_str in resources:
        data = json.loads(json_str)
        if 'VC_ID' in data:            vc_id = data['VC_ID']
        if 'connection_point' in data: connection_point = data['connection_point']
        if 'remote_system' in data:    remote_system = data['remote_system']
        if 'interface' in data:
            interface = data['interface']
            interface = interface.split("-")                       #New Line To Avoid Bad Endpoint Name In CISCO
            interface = interface[1]
        if 'vlan_id' in data:          vlan_id = data['vlan_id']
        if 'name' in data:             ni_name = data['name']
        if 'type' in data:             ni_type = data['type']
        if 'index' in data:            subif_index = data['index']
        if 'description' in data:      description = data['description']
        else:                          description = " "
      
    # initialize the SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    # add to known hosts
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    try:
        ssh_client.connect(hostname=host, username=user, password=passw, look_for_keys=False)
        #print("Connection successful")
        LOGGER.warning("Connection successful")
    except:
        #print("[!] Cannot connect to the SSH Server")
        LOGGER.warning("[!] Cannot connect to the SSH Server")
        exit()
        
    try:
        # Open an SSH shell
        channel = ssh_client.invoke_shell()
        channel.send('enable\n')
        time.sleep(1)
        channel.send('conf term\n')
        time.sleep(0.1)
        channel.send(f"interface {interface} l2transport\n")
        time.sleep(0.1)
        channel.send('description l2vpn_vpws_example\n')
        time.sleep(0.1)
        channel.send(f"encapsulation dot1q {vlan_id}\n")
        time.sleep(0.1)
        channel.send('mtu 9088\n')
        time.sleep(0.1)
        channel.send('commit\n')
        time.sleep(0.1)
        
        channel.send('l2vpn\n')
        time.sleep(0.1)
        channel.send('load-balancing flow src-dst-ip\n')
        time.sleep(0.1)
        channel.send('pw-class l2vpn_vpws_profile_example\n')
        time.sleep(0.1)
        channel.send('encapsulation mpls\n')
        time.sleep(0.1)
        channel.send('transport-mode vlan passthrough\n')
        time.sleep(0.1)
        channel.send('control-word\n')
        time.sleep(0.1)
        channel.send('exit\n')
        time.sleep(0.1)
        channel.send('l2vpn\n')
        time.sleep(0.1)
        channel.send('xconnect group l2vpn_vpws_group_example\n')
        time.sleep(0.1)
        channel.send(f"p2p {ni_name}\n")
        time.sleep(0.1)
        channel.send(f"interface {interface}\n")                                #Ignore the VlanID because the interface already includes the vlanid tag
        time.sleep(0.1)
        channel.send(f"neighbor ipv4 {remote_system} pw-id {vc_id}\n")
        time.sleep(0.1)
        channel.send('pw-class l2vpn_vpws_profile_example\n')
        time.sleep(0.1)
        channel.send('exit\n')
        time.sleep(0.1)
        channel.send(f"description {description}\n")
        time.sleep(0.1)
        channel.send('commit\n')
        time.sleep(0.1) 
        # Capturar la salida del comando
        output = channel.recv(65535).decode('utf-8')
        #print(output)
        LOGGER.warning(output)
        # Close the SSH shell
        channel.close()

    except Exception as e:
        LOGGER.exception(f"Error with the CLI configuration: {e}")

    # Close the SSH client
    ssh_client.close()
    
def ufi_interface(resources, delete: bool, host: str, user: str, passw: str):     #Method used for configuring via CLI directly L2VPN in CISCO devices

    key_value_data = {}

    for path, json_str in resources:
        key_value_data[path] = json_str

    # initialize the SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    # add to known hosts
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=host, username=user, password=passw, look_for_keys=False)
        LOGGER.warning("Connection successful")
    except:
        LOGGER.warning("[!] Cannot connect to the SSH Server")
        exit()
    interface = 'ge100-0/0/3/1'  
    ip = '1.1.1.1'
    mask = '24'
    vlan = '1212'
    try:
        # Open an SSH shell
        channel = ssh_client.invoke_shell()
        time.sleep(5)
        channel.send('config\n')
        time.sleep(1)
        channel.send(f'interfaces {interface} \n')
        time.sleep(1)
        channel.send('admin-state enabled \n')
        time.sleep(1)
        channel.send(f'ipv4-address {ip}/{mask} \n')
        time.sleep(1)
        channel.send(f'vlan-id {vlan} \n')
        time.sleep(1)
        channel.send('commit\n')
        time.sleep(1)

        output = channel.recv(65535).decode('utf-8')
        LOGGER.warning(output)
        # Close the SSH shell
        channel.close()

    except Exception as e:
        LOGGER.exception(f"Error with the CLI configuration: {e}")

    # Close the SSH client
    ssh_client.close()

def cisco_interface(resources, delete: bool, host: str, user: str, passw: str):     #Method used for configuring via CLI directly L2VPN in CISCO devices

    key_value_data = {}
    for path, json_str in resources:
        key_value_data[path] = json_str

    # initialize the SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    # add to known hosts
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=host, username=user, password=passw, look_for_keys=False)
        LOGGER.warning("Connection successful")
    except:
        LOGGER.warning("[!] Cannot connect to the SSH Server")
        exit()
    interface = 'FourHundredGigE0/0/0/10.1212'  
    ip = '1.1.1.1'
    mask = '24'
    vlan = '1212'
    try:
        # Open an SSH shell
        channel = ssh_client.invoke_shell()
        time.sleep(1)
        channel.send('config\n')
        time.sleep(0.1)
        channel.send(f'interface {interface} \n')
        time.sleep(0.1)
        channel.send('no shutdown\n')
        time.sleep(0.1)
        channel.send(f'ipv4 address {ip}/{mask} \n')
        time.sleep(0.1)
        channel.send(f'encapsulation dot1q {vlan} \n')
        time.sleep(0.1)
        channel.send('commit\n')
        time.sleep(0.1)

        output = channel.recv(65535).decode('utf-8')
        LOGGER.warning(output)
        # Close the SSH shell
        channel.close()

    except Exception as e:
        LOGGER.exception(f"Error with the CLI configuration: {e}")

    # Close the SSH client
    ssh_client.close()  
