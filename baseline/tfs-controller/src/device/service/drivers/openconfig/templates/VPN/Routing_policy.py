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
# Method Name: create_rp_statement
  
# Parameters:
  - Policy_Name:        [str]  Variable that determines the name of the Routing Policy [Mandatory parameter in all cases].
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - Statement_Name:     [str]  Variable that determines the name of the Routing Policy Statement, which is a unique statement within the policy [Only mandatory if DEL = False].
  - Policy_Result:      [str]  Variable to set if the policy is for accepting (ACCEPT ROUTE) or rejecting (REJECT ROUTE). [Only mandatory if DEL = False].
  - ExtCommSetName:     [str]  Variable to set the name of the extended community set in the context of BGP policy conditions. [Only mandatory if DEL = False].
  
# Functionality:
  This method generates the template of a routing policy statement to configure in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a policy statement) or false (Template for creating a policy statement).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_rp_statement(data, DEL):
    doc, tag, text = Doc().tagtext()

    RP_policy_name          = data['policy_name']
    RP_statement_name       = data['statement_name']
    RP_policy_result        = data['policy_result']
    RP_ext_comm_set_name    = data['ext_community_set_name']
    

    with tag('routing-policy', xmlns="http://openconfig.net/yang/routing-policy"):
        if DEL == True: 
            with tag('policy-definitions'):
                with tag('policy-definition' ,'xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                    with tag('name'):text(RP_policy_name)
        else:
            with tag('policy-definitions'):
                with tag('policy-definition'):
                    with tag('name'):text(RP_policy_name)
                    with tag('config'):
                        with tag('name'):text(RP_policy_name)
                    with tag('statements'):
                        with tag('statement'):
                            with tag('name'):text(RP_statement_name)
                            with tag('config'):
                                with tag('name'):text(RP_statement_name)
                            with tag('conditions'):
                                with tag('config'):
                                    with tag('install-protocol-eq', **{'xmlns:openconfig-policy-types': 'http://openconfig.net/yang/policy-types'}):text('openconfig-policy-types:DIRECTLY_CONNECTED')
                                with tag('bgp-conditions', xmlns="http://openconfig.net/yang/bgp-policy"):
                                    with tag('config'):
                                        with tag('ext-community-set'):text(RP_ext_comm_set_name)
                            with tag('actions'):
                                with tag('config'):
                                    with tag('policy-result'):text(RP_policy_result)
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

"""
# Method Name: create_rp_def
  
# Parameters:
  - ExtCommSetName:     [str]  Variable to set the name of the extended community set in the context of BGP policy conditions. [Mandatory parameter in all cases].
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - ExtCommMember:      [str]  Variable that represents an individual member or value within an Extended Community [Only mandatory if DEL = False].
   
# Functionality:
  This method generates the template of a routing policy defined sets, which are objects defined and used within a routing policy statement.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a routing policy defined set) or false (Template for creating a routing policy defined set).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_rp_def(data, DEL):
    doc, tag, text = Doc().tagtext()
   
    RP_ext_comm_set_name    = data['ext_community_set_name']
    RP_ext_comm_member      = data['ext_community_member']
    
    with tag('routing-policy', xmlns="http://openconfig.net/yang/routing-policy"):
        if DEL == True: 
            with tag('defined-sets'):
                with tag('bgp-defined-sets', xmlns="http://openconfig.net/yang/bgp-policy"):
                    with tag('ext-community-sets'):
                        with tag('ext-community-set' ,'xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                            with tag('ext-community-set-name'):text(RP_ext_comm_set_name)
        else:
            with tag('defined-sets'):
                with tag('bgp-defined-sets', xmlns="http://openconfig.net/yang/bgp-policy"):
                    with tag('ext-community-sets'):
                        with tag('ext-community-set'):
                            with tag('ext-community-set-name'):text(RP_ext_comm_set_name)
                            with tag('config'):
                                with tag('ext-community-set-name'):text(RP_ext_comm_set_name)
                                with tag('ext-community-member'):text(RP_ext_comm_member)
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result

#TESTING
'''
data_1 =    {"ext_community_set_name"   : "set_srv_101_a", 
             "policy_name"              : "srv_101_a", 
             "policy_result"            : "ACCEPT_ROUTE", 
             "statement_name"           : "stm_srv_101_a"}

data_2 =    {'ext_community_member'     : '65001:101', 
            'ext_community_set_name'    : 'set_srv_101_a'}

print('\nRouting Policy Statement - CREATE\n')
print(create_rp_statement(data_1, False))
print('\nRouting Policy Statement - DELETE\n')
print(create_rp_statement(data_1, True))

print('\nRouting Policy Defined Set - CREATE\n')
print(create_rp_def(data_2, False))
print('\nRouting Policy Defined Set - DELETE\n')
print(create_rp_def(data_2, True))
'''

'''
from .openconfig_routing_policy import openconfig_routing_policy
from pyangbind.lib.serialise import pybindIETFXMLEncoder

"""
# Method Name: create_rp_statement
  
# Parameters:
  - Policy_Name:        [str]  Variable that determines the name of the Routing Policy [Mandatory parameter in all cases].
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - Statement_Name:     [str]  Variable that determines the name of the Routing Policy Statement, which is a unique statement within the policy [Only mandatory if DEL = False].
  - Policy_Result:      [str]  Variable to set if the policy is for accepting (ACCEPT ROUTE) or rejecting (REJECT ROUTE). [Only mandatory if DEL = False].
  - ExtCommSetName:     [str]  Variable to set the name of the extended community set in the context of BGP policy conditions. [Only mandatory if DEL = False].
  
# Functionality:
  This method generates the template of a routing policy statement to configure in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a policy statement) or false (Template for creating a policy statement).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_rp_statement(parameters):                        #[L3] Creates a Routing Policy Statement
    Policy_Name      = parameters['policy_name']   
    DEL              = parameters['DEL']                            #If the parameter DEL is set to "TRUE" that will mean that is for making a DELETE, ELSE is for creating
           
    #Create an instance of the YANG model
    RoutingPolicy_Instance = openconfig_routing_policy()

    if DEL == True:
        #Set the Name of the Routing Policy
        Set_RoutingPolicy = RoutingPolicy_Instance.routing_policy.policy_definitions.policy_definition.add(name=Policy_Name)

        #Dump the entire instance as RFC 750 XML
        RoutingInstance_set = pybindIETFXMLEncoder.serialise(RoutingPolicy_Instance)

        RoutingInstance_set = RoutingInstance_set.replace('<openconfig-routing-policy xmlns="http://openconfig.net/yang/routing-policy">',"")
        RoutingInstance_set = RoutingInstance_set.replace('<routing-policy>','<routing-policy xmlns="http://openconfig.net/yang/routing-policy">')

        #Operation Delete [Replace]
        RoutingInstance_set = RoutingInstance_set.replace('<policy-definition>','<policy-definition xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">')
        RoutingInstance_set = RoutingInstance_set.replace('</openconfig-routing-policy>','')   

    else:
        Statement_Name   = parameters['statement_name']             
        Policy_Result    = parameters['policy_result']
        ExtCommSetName   = parameters['ext_community_set_name']

        #Access the entry container

        #Set the Name of the Routing Policy
        Set_RoutingPolicy = RoutingPolicy_Instance.routing_policy.policy_definitions.policy_definition.add(name=Policy_Name)
        Set_RoutingPolicy.config.name = Policy_Name

        #Configure the Statement of the Routing Policy 
        Set_Statement_RoutingPolicy = Set_RoutingPolicy.statements.statement.add(name=Statement_Name)
        Set_Statement_RoutingPolicy.config.name = Statement_Name
        Set_Statement_RoutingPolicy.conditions.config.install_protocol_eq = "DIRECTLY_CONNECTED"
        Set_Statement_RoutingPolicy.actions.config.policy_result = Policy_Result
        
        #Dump the entire instance as RFC 750 XML
        RoutingInstance_set = pybindIETFXMLEncoder.serialise(RoutingPolicy_Instance)

        #Policy-Definition - Statements - BGP-Conditions [Replace]
        RoutingInstance_set = RoutingInstance_set.replace('</conditions>','  <bgp-conditions xmlns="http://openconfig.net/yang/bgp-policy"> \n\t\t <config> \n\t    \
        <ext-community-set>'+ ExtCommSetName +'</ext-community-set> \n\t\t </config> \n\t      </bgp-conditions>\n\t    </conditions>')

        #Generic Replaces
        RoutingInstance_set = RoutingInstance_set.replace('<openconfig-routing-policy xmlns="http://openconfig.net/yang/routing-policy">',"")
        RoutingInstance_set = RoutingInstance_set.replace('<routing-policy>','<routing-policy xmlns="http://openconfig.net/yang/routing-policy">')
        RoutingInstance_set = RoutingInstance_set.replace('</openconfig-routing-policy>','') 

    return (RoutingInstance_set)

"""
# Method Name: create_rp_def
  
# Parameters:
  - ExtCommSetName:     [str]  Variable to set the name of the extended community set in the context of BGP policy conditions. [Mandatory parameter in all cases].
  - DEL:                [bool] Variable that determines if the template will be for creating (DEL = False) or for deleting (DEL = True) a configuration [Mandatory parameter in all cases].
  - ExtCommMember:      [str]  Variable that represents an individual member or value within an Extended Community [Only mandatory if DEL = False].
   
# Functionality:
  This method generates the template of a routing policy defined sets, which are objects defined and used within a routing policy statement.
  This template will be generated for being configured in a device, making use of pyangbind. 
  To generate the template the following steps are performed:
  1) Checks if the DEL variable is true (Template for deleting a routing policy defined set) or false (Template for creating a routing policy defined set).
  2) Create the template correspondent in each case, assigning the correspondent parameters with their value.
  3) Make the correspondent replaces for the unssuported configurations by pyangbind.
  
# Return:
  [str] The newly generated template according to the specified parameters.
"""
def create_rp_def(parameters):                              #[L3] Creates a Routing Policy - Defined Sets [ '/routing_policy/bgp_defined_set[{:s}_rt_export][{:s}]' ]
    ExtCommSetName   = parameters['ext_community_set_name']
    DEL              = parameters['DEL']                            #If the parameter DEL is set to "TRUE" that will mean that is for making a DELETE, ELSE is for creating             
                                                                    
    #Create an instance of the YANG model
    RoutingPolicy_Instance = openconfig_routing_policy()

    if DEL == True:                                                                                 #Delete operation
        #Dump the entire instance as RFC 750 XML
        RoutingInstance_set = pybindIETFXMLEncoder.serialise(RoutingPolicy_Instance)

        #BGP-Defined-Sets [Replace]
        RoutingInstance_set = RoutingInstance_set.replace('<openconfig-routing-policy xmlns="http://openconfig.net/yang/routing-policy"/>',
        '<routing-policy xmlns="http://openconfig.net/yang/routing-policy"> \n   <defined-sets> \n      <bgp-defined-sets xmlns="http://openconfig.net/yang/bgp-policy">\
        \n\t <ext-community-sets> \n\t   <ext-community-set xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"> \n      \
        <ext-community-set-name>'+ExtCommSetName+'</ext-community-set-name> \n\t   </ext-community-set> \n\t </ext-community-sets> \
         \n      </bgp-defined-sets> \n   </defined-sets> \n </routing-policy>')

    else:                                                                                            #Merge operation
        #Add new requested parameter - ext_community_member
        ExtCommMember    = parameters['ext_community_member'] 

        #Dump the entire instance as RFC 750 XML
        RoutingInstance_set = pybindIETFXMLEncoder.serialise(RoutingPolicy_Instance)

        #BGP-Defined-Sets [Replace]
        RoutingInstance_set = RoutingInstance_set.replace('<openconfig-routing-policy xmlns="http://openconfig.net/yang/routing-policy"/>',
        '<routing-policy xmlns="http://openconfig.net/yang/routing-policy"> \n   <defined-sets> \n     <bgp-defined-sets xmlns="http://openconfig.net/yang/bgp-policy">\
        \n\t<ext-community-sets> \n\t  <ext-community-set> \n\t   <ext-community-set-name>'+ExtCommSetName+'</ext-community-set-name> \n\t     <config>     \
        \n\t\t<ext-community-set-name>'+ ExtCommSetName +'</ext-community-set-name> \n\t\t<ext-community-member>'+ExtCommMember+'</ext-community-member> \n     \
        </config>  \n\t   </ext-community-set> \n\t </ext-community-sets> \n      </bgp-defined-sets> \n   </defined-sets> \n </routing-policy>')

    return (RoutingInstance_set)
'''
