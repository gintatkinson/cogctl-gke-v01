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

RULE_TYPE_MAPPING = {
    'ACLRULETYPE_UNDEFINED': 'ACL_UNDEFINED',
    'ACLRULETYPE_IPV4'     : 'ACL_IPV4',
    'ACLRULETYPE_IPV6'     : 'ACL_IPV6',
    'ACLRULETYPE_L2'       : 'ACL_L2',
    'ACLRULETYPE_MPLS'     : 'ACL_MPLS',
    'ACLRULETYPE_MIXED'    : 'ACL_MIXED',
}

FORWARDING_ACTION_MAPPING = {
    'ACLFORWARDINGACTION_UNDEFINED': 'UNDEFINED',
    'ACLFORWARDINGACTION_DROP'     : 'DROP',
    'ACLFORWARDINGACTION_ACCEPT'   : 'ACCEPT',
    'ACLFORWARDINGACTION_REJECT'   : 'REJECT',
}

LOG_ACTION_MAPPING = {
    'ACLLOGACTION_UNDEFINED': 'UNDEFINED',
    'ACLLOGACTION_NOLOG'    : 'LOG_NONE',
    'ACLLOGACTION_SYSLOG'   : 'LOG_SYSLOG',
}

def acl_set_mng(data,vendor, delete):
    doc, tag, text = Doc().tagtext()

    Acl_data    = data["rule_set"]
    Acl_name    = Acl_data['name']
    Acl_type    = RULE_TYPE_MAPPING[Acl_data['type']]
    Acl_desc    = Acl_data['description']
    Acl_entries = Acl_data['entries']
    with tag('acl', xmlns="http://openconfig.net/yang/acl"):
        if delete:
            with tag('acl-sets' ,'xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete"'):
                with tag('acl-set'):
                    with tag('name'):text(Acl_name)
                    with tag('type'):text(Acl_type)
                    with tag('acl-entries'):
                            for entry in Acl_entries:
                                ID     = entry['sequence_id']
                                desc   = entry['description']
                                match  = entry['match']
                                action = entry['action']
                                with tag('acl-entry'): 
                                    with tag('sequence-id'):text(ID)
        else:
            with tag('acl-sets'):
                with tag('acl-set'):
                    with tag('name'):text(Acl_name)
                    with tag('type'):text(Acl_type)
                    with tag('config'):
                        with tag('name'): text(Acl_name)
                        with tag('type'): text(Acl_type)
                        with tag('description'):text(Acl_desc)
                    with tag('acl-entries'):
                        for entry in Acl_entries:
                            ID     = entry['sequence_id']
                            desc   = entry['description']
                            match  = entry['match']
                            action = entry['action']
                            with tag('acl-entry'): 
                                with tag('sequence-id'):text(ID)
                                with tag('config'):
                                    with tag('sequence-id'):   text(ID)
                                    with tag('description'): text(desc)
                                # Configuration per type
                                if "L2" in Acl_type:
                                    with tag('l2'):
                                        with tag('config'):
                                            for key, value in match.items():
                                                if   "src_address"     in key and len(value) != 0: 
                                                    with tag('source-mac'):text(value)
                                                elif "dst_address"     in key and len(value) != 0:
                                                    with tag('destination-mac'):text(value)   
                                elif "IPV4" in Acl_type:
                                    with tag('ipv4'):
                                        with tag('config'):
                                            for key, value in match.items():
                                                if   "src_address"       in key and len(value) != 0:
                                                    with tag('source-address'):text(value)
                                                elif "dst_address"       in key and len(value) != 0:
                                                    with tag('destination-address'):text(value)
                                                elif "protocol"          in key                    :
                                                    with tag('protocol'):text(value)
                                                elif "hop_limit"         in key                    : 
                                                    with tag('hop-limit'):text(value)
                                                elif "dscp"              in key                    : 
                                                    with tag('dscp'):text(value)
                                    with tag('transport'):
                                        with tag('config'):
                                            for key, value in match.items():
                                                if   "src_port"     in key : 
                                                    with tag('source-port'):text(value)
                                                elif "dst_port"     in key : 
                                                    with tag('destination-port'):text(value)
                                                elif "tcp_flags"    in key : 
                                                    with tag('tcp-flags'):text(value)        
                                elif "IPV6" in Acl_type:
                                    with tag('ipv6'):
                                        with tag('config'):
                                            for key, value in match.items():
                                                if   "src_address"       in key and len(value) != 0:
                                                    with tag('source-address'):text(value)
                                                elif "dst_address"       in key and len(value) != 0:
                                                    with tag('destination-address'):text(value)
                                                elif "protocol"          in key                    :
                                                    with tag('protocol'):text(value)
                                                elif "hop_limit"         in key                    : 
                                                    with tag('hop-limit'):text(value)
                                                elif "dscp"              in key                    : 
                                                    with tag('dscp'):text(value)
                                with tag('actions'):
                                    with tag('config'):
                                        for key, value in action.items():
                                            if "forward_action" in key : 
                                                with tag('forwarding-action'):text(FORWARDING_ACTION_MAPPING[value])
                                            elif "log_action"     in key :
                                                with tag('log-action'):text(LOG_ACTION_MAPPING[value])
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result


def acl_interface(data,vendor, delete):
    doc, tag, text = Doc().tagtext()

    ID        = data['endpoint_id']['endpoint_uuid']['uuid']
    Acl_data  = data["rule_set"]
    Acl_name  = Acl_data['name']
    Acl_type  = RULE_TYPE_MAPPING[Acl_data['type']]

    with tag('acl', xmlns="http://openconfig.net/yang/acl"):
            with tag('interfaces'):
                with tag('interface'):
                    with tag('id'):text(ID)
                    with tag('config'):
                        with tag('id'):text(ID)
                    with tag('interface-ref'):
                        with tag('config'):
                            with tag('interface'):text(ID)
                            if vendor == 'ADVA': 
                                with tag('subinterface'): text(0)
                            else:
                                with tag('subinterface'): text('subinterface')
                    with tag('ingress-acl-sets'):
                        with tag('ingress-acl-set'):
                            with tag('set-name'):text(Acl_name)
                            with tag('type'):text(Acl_type)
                            with tag('config'):
                                with tag('set-name'):text(Acl_name)
                                with tag('type'):text(Acl_type)
    result = indent(
        doc.getvalue(),
        indentation = ' '*2,
        newline = '\r\n'
    )
    return result


def acl_mgmt(parameters,vendor,delete):
    acl   = []
    acl.append(acl_set_mng(  parameters,vendor,delete))
    acl.append(acl_interface(parameters,vendor,delete))
    return acl

# TESTING
'''
data = {'endpoint_id':{'device_id': {'device_uuid': {'uuid': 'R155'}},'endpoint_uuid':{'uuid':'eth-1/0/21.999'}},
        'rule_set':{'name':"ACL_L4",'type':1,'description':'acl ipv4','entries':[{'sequence_id': 1, 'description': 'IPv4_ACL', 'match': {'dst_address': '172.16.4.4', 'dscp': 0, 'protocol': 6, 'src_address': '172.16.5.5', 'src_port': 0, 'dst_port': 0, 'start_mpls_label': 0, 'end_mpls_label': 0}, 'action': {'forward_action': 1, 'log_action': 1}},
                                                                                 {'sequence_id': 2, 'description': 'L2_ACL', 'match': {'dst_address': '', 'dscp': 0, 'protocol': 0, 'src_address': '', 'src_port': 52, 'dst_port': 950, 'start_mpls_label': 0, 'end_mpls_label': 0}, 'action': {'forward_action': 1, 'log_action': 1}}]}}

print('\t\tACL')
print(acl_set_mng(data, False))
print('\t\tACL')
print(acl_set_mng(data, True))

print('\n\n\t\tInterfaz')
print(acl_interface(data,'ADVA', False))
print('\n\n\t\tInterfaz')
print(acl_interface(data,'ADVA', True))

'''
'''
OLD - VERSION

from .openconfig_acl import openconfig_acl
from pyangbind.lib.serialise import pybindIETFXMLEncoder
from common.tools.grpc.Tools import grpc_message_to_json
import logging
def acl_mgmt(parameters,vendor):                                                                                       # acl templates management
    acl   = []    
    data = grpc_message_to_json(parameters,use_integers_for_enums=True)                                         # acl rule parameters management
    acl.append(acl_set_mgmt(data,vendor))                                                                              # acl_set template
    acl.append(acl_interface(data,vendor))                                                                             # acl interface template
    return acl
    
def acl_set_mgmt(parameters,vendor):
    type     = ["ACL_UNDEFINED", "ACL_IPV4","ACL_IPV6","ACL_L2","ACL_MPLS","ACL_MIXED"]
    f_action = ["UNDEFINED", "DROP","ACCEPT","REJECT"]
    l_action = ["UNDEFINED", "LOG_NONE","LOG_SYSLOG"]
    
    Acl_data    = parameters["rule_set"]
    Acl_name    = Acl_data['name']
    Acl_type    = type[Acl_data['type']]
    Acl_desc    = Acl_data['description']
    Acl_entries = Acl_data['entries']

    # Create an instance of the YANG model
    acl_instance = openconfig_acl()

    # Access the entry container
    acl_set                    = acl_instance.acl.acl_sets.acl_set.add(name = Acl_name, type=Acl_type)
    acl_set.config.name        = Acl_name
    acl_set.config.type        = Acl_type
    acl_set.config.description = Acl_desc
    LOGGER = logging.getLogger(__name__)

    LOGGER.warning("VALORES DE ENTRIES",Acl_entries)

    for entry in Acl_entries:
        ID     = entry['sequence_id']
        desc   = entry['description']
        match  = entry['match']
        action = entry['action']

        acl_entrie = acl_set.acl_entries.acl_entry.add(ID)
        acl_entrie.config.sequence_id = ID
        acl_entrie.config.description= desc
        
        # Configuration per type
        if "L2" in Acl_type:
            for key, value in match.items():
                if   "src_address"     in key and len(value) != 0: acl_entrie.l2.config.source_mac = value
                elif "dst_address"     in key and len(value) != 0: acl_entrie.l2.config.destination_mac = value
                
        elif "IPV4" in Acl_type:
            for key, value in match.items():
                if   "src_address"       in key and len(value) != 0: acl_entrie.ipv4.config.source_address = value
                elif "dst_address"       in key and len(value) != 0: acl_entrie.ipv4.config.destination_address = value
                elif "protocol"          in key                    : acl_entrie.ipv4.config.protocol = value
                elif "hop_limit"         in key                    : acl_entrie.ipv4.config.hop_limit = value
                elif "dscp"              in key                    : acl_entrie.ipv4.config.dscp = value
                    
            for key, value in match.items():
                if   "src_port"     in key : acl_entrie.transport.config.source_port = value
                elif "dst_port"     in key : acl_entrie.transport.config.destination_port = value
                elif "tcp_flags"    in key : acl_entrie.transport.config.tcp_flags = value
                
        elif "IPV6" in Acl_type:
            for key, value in match.items():
                if   "src_address"       in key and len(value) != 0: acl_entrie.ipv6.config.source_address = value
                elif "dst_address"       in key and len(value) != 0: acl_entrie.ipv6.config.destination_address = value
                elif "protocol"          in key                    : acl_entrie.ipv6.config.protocol = value
                elif "hop_limit"         in key                    : acl_entrie.ipv6.config.hop_limit = value
                elif "dscp"              in key                    : acl_entrie.ipv6.config.dscp = value
        
        for key, value in action.items():
            if   "forward_action"        in key : acl_entrie.actions.config.forwarding_action = f_action[value]
            elif "log_action"            in key : acl_entrie.actions.config.log_action = l_action[value]
            
    # Dump the entire instance as RFC 7950 XML
    acl_set = pybindIETFXMLEncoder.serialise(acl_instance)
    acl_set = acl_set.replace('<openconfig-acl xmlns="http://openconfig.net/yang/acl">',"")
    acl_set = acl_set.replace('<acl>','<acl xmlns="http://openconfig.net/yang/acl">')
    acl_set = acl_set.replace('</openconfig-acl>','')

    return(acl_set)

def acl_interface(parameters,vendor):
    type      = ["ACL_UNDEFINED", "ACL_IPV4","ACL_IPV6","ACL_L2","ACL_MPLS","ACL_MIXED"]
    ID        = parameters['endpoint_id']['endpoint_uuid']['uuid']
    Acl_data  = parameters["rule_set"]
    Acl_name  = Acl_data['name']
    Acl_type  = type[Acl_data['type']]

    # Create an instance of the YANG model
    acl_instance = openconfig_acl()

    # Access the entry container
    interface = acl_instance.acl.interfaces.interface.add(id = ID)

    #Config - Interface
    interface.config.id = ID
    
    #If the Interface parameter is defined [OPTIONAL-PARAMETER]
    interface.interface_ref.config.interface = ID        # Interface parameter 
    
    #TODO: add subinterface management
    if   vendor == "ADVA"   : interface.interface_ref.config.subinterface = '0'    # Subinterface parameter
    elif vendor == "Juniper": interface.interface_ref.config.subinterface = '0'
    else:                     interface.interface_ref.config.subinterface = Acl_data['subinterface']
    # Configuration ingress type
    ingress= interface.ingress_acl_sets.ingress_acl_set.add(set_name = Acl_name, type = Acl_type)
    ingress.config.set_name = Acl_name
    ingress.config.type     = Acl_type

    # Dump the entire instance as RFC 7950 XML
    acl_set = pybindIETFXMLEncoder.serialise(acl_instance)                                      
    acl_set = acl_set.replace('<openconfig-acl xmlns="http://openconfig.net/yang/acl">',"")     
    acl_set = acl_set.replace('<acl>','<acl xmlns="http://openconfig.net/yang/acl">')           
    acl_set = acl_set.replace('</openconfig-acl>','')                                           
    return(acl_set)
'''
