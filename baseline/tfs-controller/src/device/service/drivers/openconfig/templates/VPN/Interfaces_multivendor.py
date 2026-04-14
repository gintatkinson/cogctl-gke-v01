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

from yattag import Doc, indent
"""
# Method Name: create_If_SubIf
  
# Parameters:
  - Interface_name:     [str]  Variable to set the name of the Interface that will be configured. [Mandatory parameter in all cases].
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - Interface_type:     [str]  Variable that specifies the type of interface, can take the value "l2vlan" or "l3ipvlan" [Only mandatory if DEL = False].
  - SubInterface_Index: [int]  Variable to set the index of the subinterface.[Only mandatory if DEL = False].
  - Description:        [str]  Variable for adding a description to the Interface   [Only mandatory if DEL = False].

# Functionality:
  This method generates the template of an Interface with subinterface, used both for L2 and L3 VPNs.
  This template will be generated for configuring a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a existent Interface or) or false (Template for creating a new Interface with Subinterface).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_If_SubIf(data,vendor, DEL):
    doc, tag, text = Doc().tagtext()

    with tag('interfaces', xmlns="http://openconfig.net/yang/interfaces"):
        if DEL == True: 
            with tag('interface' ,'xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                with tag('name'):text(data['name'])
        else:
            with tag('interface'):
                with tag('name'):text(data['name'])
                with tag('config'):
                    with tag('name'):text(data['name'])
                    with tag('type', 'xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type"'):text('ianaift:',data['type'])
                    if 'description' in data:
                        with tag('description'):text(data['description'])
                    if 'mtu' in data:
                        with tag('mtu'):text(data['mtu'])
                    with tag('enabled'):text('true')    
                with tag('subinterfaces'):
                    with tag('subinterface'):
                        if vendor is None or vendor == 'ADVA':
                            with tag('index'): text('0')
                        with tag('config'):
                            with tag('index'): text('0')
                            if vendor == 'ADVA' and not 'vlan_id'in data: 
                                with tag('untagged-allowed', 'xmlns="http://www.advaoptical.com/cim/adva-dnos-oc-interfaces"'):text('true')
                        with tag('vlan',  xmlns="http://openconfig.net/yang/vlan"):
                            with tag('match'):
                                with tag('single-tagged'):
                                    with tag('config'):
                                        with tag('vlan-id'):text(data['vlan_id'])
                        if "l3ipvlan" in data['type'] and 'address_ip' in data: 
                            with tag('ipv4',  xmlns="http://openconfig.net/yang/interfaces/ip"):
                                if 'mtu' in data:
                                    with tag('mtu'):text(data['mtu'])
                                with tag('addresses'):
                                    with tag('address'):
                                        with tag('ip'):text(data['address_ip'])
                                        with tag('config'):
                                            with tag('ip'):text(data['address_ip'])
                                            with tag('prefix-length'):text(data['address_prefix'])
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

#TESTING
'''
data = {'name'          : 'eth-1/0/22.222',
        'type'          : 'l3ipvlan',
        'mtu'           : '3000',
        'index'         : '0',
        'description'   : 'Interfaz con subinterfaz', 
        'vlan_id'       : '222',
        'address_ip'    : '172.16.55.55', 
        'address_prefix': '24'}

print('\n\t\tINTERFAZ - Create')
print(create_If_SubIf(data,'ADVA', False))
print('\n\t\tINTERFAZ - Delete')
print(create_If_SubIf(data,'ADVA', True))
'''


'''
from .openconfig_interfaces import openconfig_interfaces
from pyangbind.lib.serialise import pybindIETFXMLEncoder

"""
# Method Name: set_vlan
  
# Parameters:
  - vendor:     [str]  Variable to set the name of the vendor of the device to be configured. Depending on the vendor, the generated template may vary.
  - vlan_id:    [int]  Variable to set the value of the parameter "vlan id". 
# Functionality:
  This is an auxiliary method that helps in the creation of the Interface template. This method generates the correspondent configuration of the vlan for the interface.
  The method first checks if the parameters vendor and vlan_id are defined. If the vendor is ADVA and vlan_id = 0, an special configuration line is created. 
  Based on the values of the given parameters, the method generates the vlan configuration string.
  
# Return:
  [str] The method returns the generated vlan configuration string, that can be later used in the generation of the Interface template.
"""
def set_vlan(OptionalParams):                                   #[L2/L3] Sets a VLANID and a VENDOR that will be requested for executing the following methods
    verify = str(OptionalParams)                                #Verify transforms the received parameters into a string format for later making verifications and modifications
    
    #If the Vendor parameter is defined [OPTIONAL-PARAMETER]
    if verify.find('vendor')>0:
        Vendor = OptionalParams['vendor']  

    #If the VlanID parameter is defined [OPTIONAL-PARAMETER]
    if verify.find('vlan_id')>0:
        VlanID = OptionalParams['vlan_id'] 
        if VlanID == 0 and "ADVA" in Vendor: vlan = '  <untagged-allowed xmlns="http://www.advaoptical.com/cim/adva-dnos-oc-interfaces">true</untagged-allowed></config> \n          </config>\n        </subinterface>'
        elif VlanID != 0:                    vlan = '</config>\n          <vlan xmlns="http://openconfig.net/yang/vlan"> \n\t    <match> \n\t      <single-tagged> \n \t\t<config>\n \t\t  <vlan-id>'+str(VlanID)+'</vlan-id> \n \t\t</config> \n \t      </single-tagged> \n \t    </match> \n \t  </vlan> \n         </subinterface>'
        else:                                vlan = '</subinterface>\n          </config>'
    else:                                    vlan = '</subinterface>\n          </config>'   
    return vlan

"""
# Method Name: set_ip
  
# Parameters:
  - address_ip:     [str]  Variable that sets the value of the ip address.
  - address_prefix: [int]  Variable that specifies the prefix of the given ip address. 
# Functionality:
  This is an auxiliary method that helps in the creation of the Interface template. This method generates the correspondent configuration of the ip address for the interface.
  The method first checks if the parameter address_ip is defined. If it is defined, then it creates the configuration string that will be used later in the Interface template.
  
# Return:
  [str] The method returns the generated ip configuration string, that can be later used in the generation of the Interface template.
"""
def set_ip(OptionalParams):                                         #[L3] Sets a IPAddress that will be requested for executing the following L3VPN methods
    verify = str(OptionalParams)                                    # Verify transforms the received parameters into a string format for later making verifications and modifications
    
    #If the Address_ip parameter is defined [OPTIONAL-PARAMETER]
    if verify.find('address_ip')>0:
        IP      = OptionalParams['address_ip']  
        Prefix  = OptionalParams['address_prefix']
        address = '  <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip"> \n\t    <addresses> \n\t      <address> \n \t\t<ip>'+IP+'</ip> \n \t\t<config>\n \t\t  <ip>'+IP+'</ip> \n \t\t  <prefix-length>'+str(Prefix)+'</prefix-length> \n \t\t</config> \n \t      </address> \n \t    </addresses> \n \t  </ipv4>  \n \t</subinterface>'
    else:
        address ='</subinterface>'
    return address

"""
# Method Name: create_If_SubIf
  
# Parameters:
  - Interface_name:     [str]  Variable to set the name of the Interface that will be configured. [Mandatory parameter in all cases].
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - Interface_type:     [str]  Variable that specifies the type of interface, can take the value "l2vlan" or "l3ipvlan" [Only mandatory if DEL = False].
  - SubInterface_Index: [int]  Variable to set the index of the subinterface.[Only mandatory if DEL = False].
  - Description:        [str]  Variable for adding a description to the Interface   [Only mandatory if DEL = False].

# Functionality:
  This method generates the template of an Interface with subinterface, used both for L2 and L3 VPNs.
  This template will be generated for configuring a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a existent Interface or) or false (Template for creating a new Interface with Subinterface).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_If_SubIf(parameters):                                #[L2/L3] Creates a Interface with a Subinterface as described in /interface[{:s}]/subinterface[{:d}]
    Interface_name     = parameters['name']
    DEL                = parameters['DEL']                      # If the parameters DEL is set to "TRUE" that will mean that is for making a DELETE, ELSE is for creating
    verify             = str(parameters)                        # Verify transforms the received parameters into a string format for later making verifications and modifications

    #Create an instance of the YANG model
    InterfaceInstance = openconfig_interfaces()

    if DEL==True:                                               #DELETE OPERATION
        # Access the entry container
        InterfaceInstance_set = InterfaceInstance.interfaces.interface.add(name = Interface_name)
        
        # Dump the entire instance as RFC 7950 XML
        InterfaceInstance_set = pybindIETFXMLEncoder.serialise(InterfaceInstance)

        #Replace for setting the "Delete" Operation
        InterfaceInstance_set = InterfaceInstance_set.replace('<interface>','<interface xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">')

        #Generic Replaces
        InterfaceInstance_set = InterfaceInstance_set.replace('<openconfig-interfaces xmlns="http://openconfig.net/yang/interfaces">',"")
        InterfaceInstance_set = InterfaceInstance_set.replace('<interfaces>','<interfaces xmlns="http://openconfig.net/yang/interfaces">')
        InterfaceInstance_set = InterfaceInstance_set.replace('</openconfig-interfaces>','')

    else:                                                       #MERGE OPERATION
        Interface_type     = parameters['type']
        SubInterface_Index = parameters["index"]

        #Access the entry container
        InterfaceInstance_set = InterfaceInstance.interfaces.interface.add(name = Interface_name)
        InterfaceInstance_set.config.name = Interface_name
        InterfaceInstance_set.config.enabled = True

        #SubIntefaces-Config
        SubInterfaceInstance              = InterfaceInstance_set.subinterfaces.subinterface.add(index = SubInterface_Index)
        SubInterfaceInstance.config.index = SubInterface_Index

        #If the description parameter is defined [OPTIONAL-PARAMETER]
        if verify.find('description')>0:
            Description = parameters['description']   
            if  len(Description) != 0: SubInterfaceInstance.config.description = Description   #If description parameter has a value

        #If the MTU parameter is defined [OPTIONAL-PARAMETER]
        if verify.find('mtu')>0:
            MTU = parameters['mtu']    
            if  MTU != 0: InterfaceInstance_set.config.mtu = MTU                       #If MTU parameter has a value

        #Dump the entire instance as RFC 750 XML
        InterfaceInstance_set = pybindIETFXMLEncoder.serialise(InterfaceInstance)

        #Replaces for adding the Interface Type
        InterfaceInstance_set = InterfaceInstance_set.replace('</config>\n      <subinterfaces>','  <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:'+Interface_type+'</type>\n      </config>\n      <subinterfaces>')
        vlan = set_vlan(parameters)
        InterfaceInstance_set = InterfaceInstance_set.replace('</config>\n        </subinterface>',vlan)
        
        if "l3ipvlan" in Interface_type: 
            ip = set_ip(parameters)
            InterfaceInstance_set = InterfaceInstance_set.replace('</subinterface>',ip)

        #Generic Replaces
        InterfaceInstance_set = InterfaceInstance_set.replace('<openconfig-interfaces xmlns="http://openconfig.net/yang/interfaces">',"")
        InterfaceInstance_set = InterfaceInstance_set.replace('<interfaces>','<interfaces xmlns="http://openconfig.net/yang/interfaces">')
        InterfaceInstance_set = InterfaceInstance_set.replace('</openconfig-interfaces>','')

    return (InterfaceInstance_set) 
  
'''
