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
# Method Name: create_network_instance
  
# Parameters:
  - NetInstance_name:           [str] Variable to set the name of the Network Instance . [Mandatory parameter in all cases].
  - DEL:                        [bool]Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - NetInstance_type:           [str] Variable that sets the type of the Network Instance, it can take the value L2VSI for L2VPN or L3VRF for L3VPN .
  - NetInstance_description     [int] Variable for adding a description to the Network Instance  .
  - NetInstance_MTU             [str] Variable that sets the value of the MTU for the network instance.     [L2VPN]
  - NetInstance_Route_disting   [str] Variable to set the route distinguisher value .                       [L3VPN]

# Functionality:
  This method generates the template for creating a Network Instance. This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a existent Network Instance) or false (Template for creating a new Network Instance).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
""" 
def create_NI(parameters,vendor,DEL):
    doc, tag, text = Doc().tagtext()

    with tag('network-instances',xmlns="http://openconfig.net/yang/network-instance"):
        if DEL == True: 
            with tag('network-instance' ,'xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                with tag('name'):text(parameters['name'])
        else:
            with tag('network-instance'):
                with tag('name'):text(parameters['name'])
                if   "L2VSI" in parameters['type']: 
                    with tag('config'):
                        with tag('name'):text(parameters['name'])
                        if vendor == "ADVA": 
                            with tag('type', 'xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types"'):text('oc-ni-types:',parameters['type'])
                            with tag('mtu'):text('1500')
                    if vendor == "ADVA": 
                        with tag('fdb'):
                            with tag('config'):
                                with tag('mac-learning')   :text('true')
                                with tag('mac-aging-time') :text('300')
                                with tag('maximum-entries'):text('1000')
                        with tag('encapsulation'):
                            with tag('config'):
                                with tag('encapsulation-type', 'xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types"')  :text('oc-ni-types:', 'MPLS')

                elif "L3VRF" in parameters['type']: 
                    with tag('config'):
                        with tag('name'):text(parameters['name'])
                        if "router_id" in parameters: 
                            with tag('router-id'):text(parameters['router_id'])
                        if vendor is None or vendor == 'ADVA':
                            with tag('type', 'xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types"'):text('oc-ni-types:',parameters['type'])
                            with tag('route-distinguisher'):text(parameters['route_distinguisher'])
                    if vendor is None or vendor == 'ADVA':
                        with tag('encapsulation'):
                            with tag('config'):
                                with tag('encapsulation-type', 'xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types"')  :text('oc-ni-types:MPLS')
                                with tag('label-allocation-mode','xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types"'):text('oc-ni-types:INSTANCE_LABEL')

    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

"""
# Method Name: add_protocol_NI [Only for L3-VPN]
  
# Parameters:
  - NetInstance_name:           [str] Variable that specifies the name of Network Instance that is going to be used.
  - DEL:                        [bool]Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - Protocol_name:              [str] Variable that sets the type of protocol that is going to be added to the NI. It can be STATIC, DIRECTLY_CONNECTED or BGP.
  - Identifier:                 [str] Variable that sets the identifier of the protocol that will be added to the NI. It can be STATIC, DIRECTLY_CONNECTED or BGP.
  - AS:                         [int] Variable that specifies the AS (Autonomous System) parameter. To be defined only in case the protocol used is BGP 
  - Router_ID:                  [int] Variable that specifies the identifier of the router to be configured. To be defined only in case the protocol used is BGP 

# Functionality:
  This method generates the template that associates a routing protocol with a Network instance.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a routing policy defined set) or false (Template for creating a routing policy defined set).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def add_protocol_NI(parameters,vendor, DEL):
    doc, tag, text = Doc().tagtext()

    with tag('network-instances',xmlns="http://openconfig.net/yang/network-instance"):
        if DEL == True: 
            with tag('network-instance'):
                with tag('name'):text(parameters['name'])
                with tag('protocols'):
                    with tag('protocol','xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                        with tag('identifier', 'xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):text('oc-pol-types:',parameters['identifier'])
                        with tag('name')      :text(parameters['protocol_name'])
        else:
            with tag('network-instance'):
                with tag('name'):text(parameters['name'])
                with tag('protocols'):
                    with tag('protocol'):
                        with tag('identifier', 'xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):text('oc-pol-types:',parameters['identifier'])
                        with tag('name')      :text(parameters['protocol_name'])
                        with tag('config'):
                            with tag('identifier', 'xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):text('oc-pol-types:',parameters['identifier'])
                            with tag('name')      :text(parameters['protocol_name'])
                            with tag('enabled'): text('true')
                        if "BGP" in parameters['identifier']:
                            with tag('bgp'):
                                with tag('name'): text(parameters['as'])
                                with tag('global'):
                                    with tag('config'):
                                        with tag('as')       :text(parameters['as'])
                                        if "router_id" in parameters: 
                                            with tag('router-id'):text(parameters['router_id'])
                                    with tag('afi-safis'):
                                        with tag('afi-safi', 'xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types"'):
                                            with tag('afi-safi-name'): text('oc-bgp-types:IPV4_UNICAST')
                                            with tag('config'):
                                                with tag('afi-safi-name'): text('oc-bgp-types:IPV4_UNICAST')
                                                with tag('enabled'): text('true')
                                if 'neighbors' in parameters:
                                    with tag('neighbors'):
                                        for neighbor in parameters['neighbors']:
                                            with tag('neighbor'):
                                                with tag('neighbor-address'): text(neighbor['ip_address'])
                                                with tag('afi-safis'):
                                                    with tag('afi-safi', 'xmlns:oc-bgp-types="http://openconfig.net/yang/bgp-types"'):
                                                        with tag('afi-safi-name'): text('oc-bgp-types:IPV4_UNICAST')
                                                        with tag('enabled'): text('true')
                                                with tag('config'):
                                                    with tag('neighbor-address'): text(neighbor['ip_address'])
                                                    with tag('enabled'): text('true')
                                                    with tag('peer-as'): text(parameters['as'])
                if vendor is None or vendor == 'ADVA':
                    with tag('tables'):
                      with tag('table'):
                          with tag('protocol', 'xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):text('oc-pol-types:',parameters['identifier'])
                          with tag('address-family', 'xmlns:oc-types="http://openconfig.net/yang/openconfig-types"'):text('oc-types:IPV4')
                          with tag('config'):
                              with tag('protocol', 'xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):text('oc-pol-types:',parameters['identifier'])
                              with tag('address-family', 'xmlns:oc-types="http://openconfig.net/yang/openconfig-types"'):text('oc-types:IPV4')

    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

"""
# Method Name: associate_If_to_NI
  
# Parameters:
  - NetInstance_name:           [str] Variable that specifies the name of Network Instance that is going to be used.
  - NetInstance_ID:             [str] Variable to set the ID of the Interface that is going to be associated to the Network Instance.
  - NetInstance_Interface:      [str] Variable that specifies the name of the Interface that is going to be associated to the Network Instance.
  - NetInstance_SubInterface:   [int] Variable that specifies the index of the subinterface that is going to be associated to the Network Instance.

# Functionality:
  This method generates the template for associating an Interface to an existent Network Instance. This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  2) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def associate_If_to_NI(parameters, DEL):
    doc, tag, text = Doc().tagtext()

    with tag('network-instances',xmlns="http://openconfig.net/yang/network-instance"):
        if DEL == True: 
            with tag('network-instance'):
                with tag('name'):text(parameters['name'])
                with tag('interfaces'):
                    with tag('interface','xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                        with tag('id'):text(parameters['id'])
        else:
            with tag('network-instance'):
                with tag('name'):text(parameters['name'])
                with tag('config'):
                    with tag('name'):text(parameters['name'])
                    with tag('type', 'xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types"'):text('oc-ni-types:',parameters['type'])
                with tag('interfaces'):
                    with tag('interface'):
                        with tag('id'):text(parameters['id'])
                        with tag('config'):
                            with tag('id')          :text(parameters['id'])
                            with tag('interface')   :text(parameters['interface'])
                            with tag('subinterface'):text(parameters['subinterface'])
                            
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

"""
# Method Name: associate_virtual_circuit [Only for L2-VPN]
  
# Parameters:
  - NetInstance_name:           [str] Variable that specifies the name of Network Instance that is going to be used.
  - ConnectionPoint_ID:         [str] Variable that defines the Identifier of the Connection Point of within the Network Instance .
  - VirtualCircuit_ID:          [int] Variable that sets the Identifier of the Virtual Circuit (VC_ID).
  - RemoteSystem:               [str] Variable to specify the remote system (device) in which the virtual circuit is created. It should be an IP address.

# Functionality:
  This method will generate the template to associate a virtual circuit, used for L2VPN, with a Network Instance.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a Virtual Circuit from the NI) or false (Template for associating a Virtual Circuit to the NI).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def associate_virtual_circuit(parameters):

    doc, tag, text = Doc().tagtext()

    with tag('network-instances',xmlns="http://openconfig.net/yang/network-instance"):
        with tag('network-instance'):
            with tag('name'):text(parameters['name'])
            with tag('connection-points'):
                with tag('connection-point'):
                    with tag('connection-point-id'):text(parameters['connection_point'])
                    with tag('config'):
                        with tag('connection-point-id'):text(parameters['connection_point'])
                    with tag('endpoints'):
                        with tag('endpoint'):
                            with tag('endpoint-id'):text(parameters['connection_point'])
                            with tag('config'):
                                with tag('endpoint-id'):text(parameters['connection_point'])
                                with tag('precedence'):text('1')
                                with tag('type', 'xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types"'):text('oc-ni-types:REMOTE')
                            with tag('remote'):
                                with tag('config'):
                                    with tag('virtual-circuit-identifier'):text(parameters['VC_ID'])
                                    with tag('remote-system'):text(parameters['remote_system'])

    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

"""
# Method Name: associate_RP_to_NI [Only for L3-VPN]
  
# Parameters:
  - NetInstance_name:   [str] Variable that specifies the name of Network Instance that is going to be used.
  - Import_policy:      [str] Variable that specifies the name of the Import Routing Policy to be set.
  - Export_policy:      [str] Variable that specifies the name of the Export Routing Policy to be set.

# Functionality:
  This method generates the template to associate a Routing Policy (Import or Export) to an existent Network Instance.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a RP from a Network Instance) or false (Template for associating a RP to a Network Instance).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def associate_RP_to_NI(parameters):
    doc, tag, text = Doc().tagtext()
    with tag('network-instances',xmlns="http://openconfig.net/yang/network-instance"):
      with tag('network-instance'):
          with tag('name'):text(parameters['name'])
          with tag('inter-instance-policies'):
              with tag('apply-policy'):
                  with tag('config'):
                      if'import_policy' in parameters :
                          with tag('import-policy'):text(parameters['import_policy'])
                      elif 'export_policy' in parameters:
                          with tag('export-policy'):text(parameters['export_policy'])
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

"""
# Method Name: create_table_conns [Only for L3-VPN]
  
# Parameters:
  - NetInstance_name:   [str] Variable that specifies the name of Network Instance that is going to be used.
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - SourceProtocol:     [str]  Variable to specify the protocol used in the Source for the table connection.
  - DestProtocol        [str]  Variable to specify the protocol used in the Destination for the table connection..
  - AddrFamily          [str]  Variable to specify the Address Family that is going to be used for the table connection. It can take the value 'IPV4'or 'IPV6'
  - Def_ImportPolicy    [str]  Variable to specify a Routing Policy, that will be used as Default for the table connections. 

# Functionality:
  This method generates the template for creating (or deleting) a table connection.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a table connection) or false (Template for creating a table connection).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_table_conns(parameters,DEL): 
    
    doc, tag, text = Doc().tagtext()

    with tag('network-instances',xmlns="http://openconfig.net/yang/network-instance"):
        with tag('network-instance'):
            with tag('name'):text(parameters['name'])
            if DEL == True: 
                with tag('table-connections'):
                    with tag('table-connection','xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                      with tag('src-protocol','xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):   text('oc-pol-types:',parameters['src_protocol'])
                      with tag('dst-protocol','xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):   text('oc-pol-types:',parameters['dst_protocol'])
                      with tag('address-family', 'xmlns:oc-types="http://openconfig.net/yang/openconfig-types"'):text('oc-types:',parameters['address_family'])     
            else:
                with tag('table-connections'):
                    with tag('table-connection'):
                      with tag('src-protocol','xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):   text('oc-pol-types:',parameters['src_protocol'])
                      with tag('dst-protocol','xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):   text('oc-pol-types:',parameters['dst_protocol'])
                      with tag('address-family', 'xmlns:oc-types="http://openconfig.net/yang/openconfig-types"'):text('oc-types:',parameters['address_family'])
                      with tag('config'):
                        with tag('src-protocol','xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):   text('oc-pol-types:',parameters['src_protocol'])
                        with tag('dst-protocol','xmlns:oc-pol-types="http://openconfig.net/yang/policy-types"'):   text('oc-pol-types:',parameters['dst_protocol'])
                        with tag('address-family', 'xmlns:oc-types="http://openconfig.net/yang/openconfig-types"'):text('oc-types:',parameters['address_family'])    
                        # for OCNOS: check if needed
                        #with tag('dst-instance', 'xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-oc-ni-augments"'):text('65000')
                        if len(parameters['default_import_policy']) != 0:
                            with tag('default-import-policy'):text(parameters['default_import_policy'])
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

#TESTING
'''
parameters1 = {'name'               : 'TEST DE VPN',
               'description        ': 'Test VPN ', 
               'type'               : 'L3VRF',
               'route_distinguisher': '65000:101'}

parameters2 = {'name'               : 'TEST DE VPN',
               'protocol_name'      : 'BGP', 
               'identifier'         : 'BGP',
               'as'                 : '65000',
               'router-id'          :'5.5.5.5'}

parameters2_1 = {'name'             : 'TEST DE VPN',
               'protocol_name'      : 'STATIC', 
               'identifier'         : 'STATIC',
               'as'                 : '',
               'router-id'          :''}
parameters3 = {'name'               : 'TEST DE VPN',
               'id'                 : 'eth-1/0/23.123', 
               'interface'          : 'eth-1/0/23.123',
               'subinterface'       : '0'}

parameters4 = {'name'               : 'TEST DE VPN',
               'connection_point'   : 'VC-1', 
               'VC_ID'              : '100',
               'remote_system'      : '5.5.5.1'}

parameters5a = {'name'               : 'TEST DE VPN',
               'import_policy'      : 'srv_101_a'}

parameters5b = {'name'               : 'TEST DE VPN',
               'export_policy'      : 'srv_101_a'}

parameters6 = {'name'                 : 'TEST DE VPN',
               'src_protocol'         : 'STATIC', 
               'dst_protocol'         : 'BGP',
               'address_family'       : 'IPV4',
               'default_import_policy':'ACCEPT_ROUTE'}

operation = False

#STEP 1
print('\t\tNetwork Instance - CREATE')
print(create_NI(parameters1,'ADVA',False))
print('\n')
print('\t\tNetwork Instance - DELETE')
print(create_NI(parameters1,'ADVA',True))

#STEP 2 option A
print('\n\n')
print('\t\tProtocol - ADD')
print(add_protocol_NI(parameters2,'ADVA',False))
print('\n\n')
print('\t\tProtocol - DELETE')
print(add_protocol_NI(parameters2,'ADVA',True))

#STEP 2 option B
print('\n\n')
print('\t\tProtocol - ADD')
print(add_protocol_NI(parameters2_1,'ADVA',False))
print('\n\n')
print('\t\tProtocol - DELETE')
print(add_protocol_NI(parameters2_1,'ADVA',True))

#STEP 3
print('\n\n')
print('\t\tInterface - ADD')
print(associate_If_to_NI(parameters3,False))
print('\n\n')
print('\t\tInterface - DELETE')
print(associate_If_to_NI(parameters3,True))

#STEP 4
print('\n\n')
print('\t\tADD Virtual Circuit')
print(associate_virtual_circuit(parameters4))

#STEP 5 option A
print('\n\n')
print('\t\tAssociate RP to NI')
print(associate_RP_to_NI(parameters5a))

#STEP 5 option B
print('\n\n')
print('\t\tAssociate RP to NI')
print(associate_RP_to_NI(parameters5b))

#STEP 6
print('\n\n')
print('\t\tTables Connections - ADD')
print(create_table_conns(parameters6,False))
print('\n\n')
print('\t\tTables Connections - DELETE')
print(create_table_conns(parameters6,True))
'''


'''
from .openconfig_network_instance import openconfig_network_instance
from pyangbind.lib.serialise     import pybindIETFXMLEncoder

"""
# Method Name: create_network_instance
  
# Parameters:
  - NetInstance_name:           [str] Variable to set the name of the Network Instance . [Mandatory parameter in all cases].
  - DEL:                        [bool]Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - NetInstance_type:           [str] Variable that sets the type of the Network Instance, it can take the value L2VSI for L2VPN or L3VRF for L3VPN .
  - NetInstance_description     [int] Variable for adding a description to the Network Instance  .
  - NetInstance_MTU             [str] Variable that sets the value of the MTU for the network instance.     [L2VPN]
  - NetInstance_Route_disting   [str] Variable to set the route distinguisher value .                       [L3VPN]

# Functionality:
  This method generates the template for creating a Network Instance. This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a existent Network Instance) or false (Template for creating a new Network Instance).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_network_instance(parameters,vendor):             #[L2/L3] Creates a Network Instance as described in: /network_instance[{:s}] 
    NetInstance_name        = parameters['name']           #Retrieves the Name parameter of the NetInstance
    DEL                     = parameters['DEL']            #If the parameter DEL is set to "TRUE" that will mean that is for making a DELETE, ELSE is for creating
    verify = str(parameters)                               #Verify transforms the received parameters into a string format for later making verifications and modifications

    #Create an instance of the YANG model
    Network_Instance = openconfig_network_instance()

    if DEL == True:                                         #DELETE OPERATION
        #Access the entry container
        NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name)

        #Dump the entire instance as RFC 750 XML
        NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
        #Generic Replaces
        NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
        NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
        NetInstance_set = NetInstance_set.replace('<network-instance>','<network-instance xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">')   
        NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','') 

    else:                                                   #MERGE OPERATION
        NetInstance_type = parameters['type']                                                                    #Retrieves the Type parameter of the NetInstance
    
        #Access the entry container
        NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name)      
        NetInstance_set.config.name = NetInstance_name                                                          
        if vendor == 'ADVA': NetInstance_set.config.type = NetInstance_type 
        NetInstance_encapsulation = NetInstance_set.encapsulation.config

        #If the description parameter is defined [OPTIONAL-PARAMETER]
        if verify.find('description')>0:
            NetInstance_description = parameters['description']    
            if  len(NetInstance_description) != 0: NetInstance_set.config.description = NetInstance_description   #If description parameter has a value

        #Configuration for L2VSI
        if   "L2VSI" in NetInstance_type:
            if verify.find('mtu')>0:                            #If the MTU parameter is defined with a value
                NetInstance_MTU = parameters['mtu']    
            else:
                NetInstance_MTU = 1500                  #Fixed value of MTU parameter  [Obligatory for L2VSI]
            #Encapsulation
            NetInstance_encapsulation.encapsulation_type = "MPLS"
            #fdb
            NetInstance_fdb = NetInstance_set.fdb.config
            NetInstance_fdb.mac_learning    = True
            NetInstance_fdb.maximum_entries = 1000
            NetInstance_fdb.mac_aging_time  = 300
            #Dump the entire instance as RFC 750 XML
            NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
            #Specific Replace [Addition of the enabled and MTU variables]
            NetInstance_set = NetInstance_set.replace('</type>','</type>\n        <mtu>'+str(NetInstance_MTU)+'</mtu>\n        <enabled>true</enabled>')   

        #Configuration for L3VRF
        elif   "L3VRF" in NetInstance_type:
            NetInstance_Route_disting = parameters['route_distinguisher']                                       #Retrieves the Route-Distinguisher parameter [Obligatory for L3VRF]
            NetInstance_set.config.route_distinguisher                            = NetInstance_Route_disting
            
            #If the router-id parameter is defined [OPTIONAL-PARAMETER]
            #if verify.find('router_id')>0:
                #NetInstance_Router_ID = parameters['router_id']    
                #if  len(NetInstance_Router_ID) != 0: NetInstance_set.config.router_id = NetInstance_Router_ID     #If router-id parameter has a value

            #Encapsulation
            if vendor == 'ADVA':
                NetInstance_encapsulation.encapsulation_type = "MPLS"
                NetInstance_encapsulation.label_allocation_mode = "INSTANCE_LABEL"    
            #Dump the entire instance as RFC 750 XML
            NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
            #Specific Replace [Addition of the enabled]
            NetInstance_set = NetInstance_set.replace('</route-distinguisher>','</route-distinguisher>\n        <enabled>true</enabled>')   
        
        #Generic Replaces
        NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
        NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
        NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')  

    return (NetInstance_set)

"""
# Method Name: associate_If_to_NI
  
# Parameters:
  - NetInstance_name:           [str] Variable that specifies the name of Network Instance that is going to be used.
  - NetInstance_ID:             [str] Variable to set the ID of the Interface that is going to be associated to the Network Instance.
  - NetInstance_Interface:      [str] Variable that specifies the name of the Interface that is going to be associated to the Network Instance.
  - NetInstance_SubInterface:   [int] Variable that specifies the index of the subinterface that is going to be associated to the Network Instance.

# Functionality:
  This method generates the template for associating an Interface to an existent Network Instance. This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  2) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def associate_If_to_NI(parameters):                         #[L2/L3] Associates an Interface to a Network Instance as described in: /network_instance[{:s}]/interface[{:s}]
    NetInstance_name = parameters['name']
    NetInstance_ID = parameters['id']
    NetInstance_Interface = parameters['interface']
    NetInstance_SubInterface = parameters['subinterface']

    #Create an instance of the YANG model
    Network_Instance = openconfig_network_instance()

    #Access the entry container
    NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name)
    NetInstance_interface = NetInstance_set.interfaces.interface.add(id = NetInstance_ID)
    NetInstance_interface.config.id = NetInstance_ID
    NetInstance_interface.config.interface = NetInstance_Interface
    NetInstance_interface.config.subinterface = NetInstance_SubInterface
        
    #Dump the entire instance as RFC 750 XML
    NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
    #Generic Replaces
    NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
    NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
    NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')   
    return (NetInstance_set)

"""
# Method Name: add_protocol_NI [Only for L3-VPN]
  
# Parameters:
  - NetInstance_name:           [str] Variable that specifies the name of Network Instance that is going to be used.
  - DEL:                        [bool]Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - Protocol_name:              [str] Variable that sets the type of protocol that is going to be added to the NI. It can be STATIC, DIRECTLY_CONNECTED or BGP.
  - Identifier:                 [str] Variable that sets the identifier of the protocol that will be added to the NI. It can be STATIC, DIRECTLY_CONNECTED or BGP.
  - AS:                         [int] Variable that specifies the AS (Autonomous System) parameter. To be defined only in case the protocol used is BGP 
  - Router_ID:                  [int] Variable that specifies the identifier of the router to be configured. To be defined only in case the protocol used is BGP 

# Functionality:
  This method generates the template that associates a routing protocol with a Network instance.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a routing policy defined set) or false (Template for creating a routing policy defined set).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def add_protocol_NI(parameters):                            #[L3]    Adds a Protocol to a Network Instance as described in: /network_instance[{:s}]/protocols
    NetInstance_name = parameters['name']                        
    Protocol_name    = parameters['protocol_name']         #Protocol can be [STATIC], [DIRECTLY_CONNECTED] or [BGP]
    Identifier       = parameters['identifier']            #Identifier can be [STATIC], [DIRECTLY_CONNECTED] or [BGP]
    DEL              = parameters['DEL']                   #If the parameter DEL is set to "TRUE" that will mean that is for making a DELETE, ELSE is for creating

    if DEL == True:                                        #DELETE OPERATION
        #Create an instance of the YANG model
        Network_Instance = openconfig_network_instance()

        #Access the entry container
        NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name)      
        NetInstance_protocol = NetInstance_set.protocols.protocol.add(name = Protocol_name, identifier = Identifier)    

        #Dump the entire instance as RFC 750 XML
        NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
        #Delete Replace
        NetInstance_set = NetInstance_set.replace('<protocol>','<protocol xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">')
        #Generic Replaces
        NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
        NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
        NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')
    
    else:                                                   #MERGE OPERATION
        #Create an instance of the YANG model
        Network_Instance = openconfig_network_instance()

        #Access the entry container
        NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name)      
        NetInstance_protocol = NetInstance_set.protocols.protocol.add(name = Protocol_name, identifier = Identifier)    
        NetInstance_protocol.config.name = Protocol_name      
        NetInstance_protocol.config.identifier = Identifier
        if Identifier in 'BGP':
            AS          = parameters['as']  
            Router_ID   = parameters['router_id']                        

            NetInstance_protocol.bgp.global_.config.as_=AS 
            NetInstance_protocol.bgp.global_.config.router_id=Router_ID
                
        #Configuration of Table
        NetInstance_tables = NetInstance_set.tables.table.add(protocol = Protocol_name, address_family = "IPV4")       #What about IPV6?
        NetInstance_tables.config.protocol = Protocol_name
        NetInstance_tables.config.address_family = "IPV4"

        #Dump the entire instance as RFC 750 XML
        NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
        # Specific Replaces
        NetInstance_set = NetInstance_set.replace('<table>\n          <protocol>'+Identifier+'</protocol>','<table> \n\t  <protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:'+Identifier+'</protocol>')
        NetInstance_set = NetInstance_set.replace('<config>\n            <protocol>'+Identifier+'</protocol>','<config> \n\t    <protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:'+Identifier+'</protocol>')
        NetInstance_set = NetInstance_set.replace('<address-family>IPV4</address-family>','<address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:'+"IPV4"+'</address-family>')
        NetInstance_set = NetInstance_set.replace('<identifier>'+Identifier+'</identifier>','<identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:'+Identifier+'</identifier>')
        #Generic Replaces
        NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
        NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
        NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')  

    return (NetInstance_set)

"""
# Method Name: associate_virtual_circuit [Only for L2-VPN]
  
# Parameters:
  - NetInstance_name:           [str] Variable that specifies the name of Network Instance that is going to be used.
  - ConnectionPoint_ID:         [str] Variable that defines the Identifier of the Connection Point of within the Network Instance .
  - VirtualCircuit_ID:          [int] Variable that sets the Identifier of the Virtual Circuit (VC_ID).
  - RemoteSystem:               [str] Variable to specify the remote system (device) in which the virtual circuit is created. It should be an IP address.

# Functionality:
  This method will generate the template to associate a virtual circuit, used for L2VPN, with a Network Instance.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a Virtual Circuit from the NI) or false (Template for associating a Virtual Circuit to the NI).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def associate_virtual_circuit(parameters):                  #[L2]    Associates a Virtual Circuit as described in: /network_instance[{:s}]/connection_point[VC-1]
    NetInstance_name   = parameters['name']
    ConnectionPoint_ID = parameters['connection_point']
    VirtualCircuit_ID  = parameters['VC_ID']
    RemoteSystem       = parameters['remote_system']

    #Create an instance of the YANG model
    Network_Instance = openconfig_network_instance()

    #Access the entry container
    NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name)
    ConnectionPoint_set = NetInstance_set.connection_points.connection_point.add(connection_point_id = ConnectionPoint_ID)
    ConnectionPoint_set.config.connection_point_id = ConnectionPoint_ID
    Endpoint_set = ConnectionPoint_set.endpoints.endpoint.add(endpoint_id = ConnectionPoint_ID)
    Endpoint_set.config.endpoint_id = ConnectionPoint_ID
    Endpoint_set.config.precedence = 1
    Endpoint_set.config.type = "REMOTE"
    Endpoint_set.remote.config.remote_system = RemoteSystem
    Endpoint_set.remote.config.virtual_circuit_identifier = VirtualCircuit_ID

    #Dump the entire instance as RFC 750 XML
    NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
    NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
    NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
    NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')   
    return (NetInstance_set)

"""
# Method Name: associate_RP_to_NI [Only for L3-VPN]
  
# Parameters:
  - NetInstance_name:   [str] Variable that specifies the name of Network Instance that is going to be used.
  - Import_policy:      [str] Variable that specifies the name of the Import Routing Policy to be set.
  - Export_policy:      [str] Variable that specifies the name of the Export Routing Policy to be set.

# Functionality:
  This method generates the template to associate a Routing Policy (Import or Export) to an existent Network Instance.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a RP from a Network Instance) or false (Template for associating a RP to a Network Instance).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def associate_RP_to_NI(parameters):                         #[L3]    Associates a Routing Policy to a Network Instance as described in: /network_instance[{:s}]/inter_instance_policies[{:s}] 
    NetInstance_name = parameters['name']
    verify = str(parameters)                               #Verify transforms the received parameters into a string format for later making verifications and modifications

    #Create an instance of the YANG model
    Network_Instance = openconfig_network_instance()

    #Access the entry container
    NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name)
    Inter_instance = NetInstance_set.inter_instance_policies.apply_policy.config

    #If a Import policy is defined
    if verify.find('import_policy')>0:
        Import = parameters['import_policy']    
        if  len(Import) != 0: Inter_instance.import_policy = Import             #If the import_policy parameter has a value

    #If a Export Policy is defined
    if verify.find('export_policy')>0:
        Export = parameters['export_policy']    
        if  len(Export) != 0: Inter_instance.export_policy = Export             #If the export_policy parameter has a value
        
    #Dump the entire instance as RFC 750 XML
    NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)
    #Generic Replaces
    NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
    NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
    NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')   
    return (NetInstance_set)

"""
# Method Name: create_table_conns [Only for L3-VPN]
  
# Parameters:
  - NetInstance_name:   [str] Variable that specifies the name of Network Instance that is going to be used.
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - SourceProtocol:     [str]  Variable to specify the protocol used in the Source for the table connection.
  - DestProtocol        [str]  Variable to specify the protocol used in the Destination for the table connection..
  - AddrFamily          [str]  Variable to specify the Address Family that is going to be used for the table connection. It can take the value 'IPV4'or 'IPV6'
  - Def_ImportPolicy    [str]  Variable to specify a Routing Policy, that will be used as Default for the table connections. 

# Functionality:
  This method generates the template for creating (or deleting) a table connection.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a table connection) or false (Template for creating a table connection).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_table_conns(parameters):                         #[L3]    Creates Table Connections as described in: /network_instance[{:s}]/table_connections
    NetInstance_name = parameters['name']
    SourceProtocol   = parameters['src_protocol']
    DestProtocol     = parameters['dst_protocol']
    AddrFamily       = parameters['address_family']
    DEL              = parameters['DEL']                   #If the parameter DEL is set to "TRUE" that will mean that is for making a DELETE, ELSE is for creating
    
    #Create an instance of the YANG model
    Network_Instance = openconfig_network_instance()

    if DEL == True:                                         #DELETE OPERATION
        #Access the entry container
        NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name) 

        #Configuration of Table-Connections
        Set_TableConns = NetInstance_set.table_connections.table_connection.add(src_protocol = SourceProtocol, dst_protocol = DestProtocol, address_family = AddrFamily)

        #Dump the entire instance as RFC 750 XML
        NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)

        #Specific Replaces
        NetInstance_set = NetInstance_set.replace('<src-protocol>'+SourceProtocol+'</src-protocol>','<src-protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:'+SourceProtocol+'</src-protocol>')
        NetInstance_set = NetInstance_set.replace('<dst-protocol>'+DestProtocol+'</dst-protocol>','<dst-protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:'+DestProtocol+'</dst-protocol>')
        NetInstance_set = NetInstance_set.replace('<address-family>'+AddrFamily+'</address-family>','<address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:'+AddrFamily+'</address-family>')
        #Generic Replaces
        NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
        NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
        NetInstance_set = NetInstance_set.replace('<table-connection>','<table-connection xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">')
        NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')

    else:                                                    #MERGE OPERATION
        verify = str(parameters)                             #Verify transforms the received parameters into a string format for later making verifications and modifications

        #Access the entry container
        NetInstance_set = Network_Instance.network_instances.network_instance.add(name = NetInstance_name) 

        #Configuration of Table-Connections
        Set_TableConns = NetInstance_set.table_connections.table_connection.add(src_protocol = "", dst_protocol = "", address_family = "")
        
        Set_TableConns.config.src_protocol   = ""
        Set_TableConns.config.dst_protocol   = ""
        Set_TableConns.config.address_family = ""

        # Default Import Policy (If is defined)
        if verify.find('default_import_policy')>0:
            Def_ImportPolicy = parameters['default_import_policy']    
            if  len(Def_ImportPolicy) != 0: Set_TableConns.config.default_import_policy = Def_ImportPolicy             #If the default_import_policy parameter has a value

        #Dump the entire instance as RFC 750 XML
        NetInstance_set = pybindIETFXMLEncoder.serialise(Network_Instance)

        #Specific Replaces
        NetInstance_set = NetInstance_set.replace('<src-protocol></src-protocol>','<src-protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:'+SourceProtocol+'</src-protocol>')
        NetInstance_set = NetInstance_set.replace('<dst-protocol></dst-protocol>','<dst-protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:'+DestProtocol+'</dst-protocol>')
        NetInstance_set = NetInstance_set.replace('<address-family></address-family>','<address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:'+AddrFamily+'</address-family>')
        #Generic Replaces
        NetInstance_set = NetInstance_set.replace('<openconfig-network-instance xmlns="http://openconfig.net/yang/network-instance">',"")
        NetInstance_set = NetInstance_set.replace('<network-instances>','<network-instances xmlns="http://openconfig.net/yang/network-instance">')
        NetInstance_set = NetInstance_set.replace('</openconfig-network-instance>','')   

    return (NetInstance_set)
'''