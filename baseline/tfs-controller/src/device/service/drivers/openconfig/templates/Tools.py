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

import json
import lxml.etree as ET
from typing import Collection, Dict, Any
from .ACL.ACL_multivendor              import acl_mgmt
from .IP_LINK.IP_LINK_multivendor      import ip_link_mgmt
from .VPN.Network_instance_multivendor import create_NI, associate_virtual_circuit, associate_RP_to_NI, add_protocol_NI, create_table_conns, associate_If_to_NI
from .VPN.Interfaces_multivendor       import create_If_SubIf
from .VPN.Routing_policy               import create_rp_def, create_rp_statement

def add_value_from_tag(target : Dict, field_name: str, field_value : ET.Element, cast=None) -> None:
    if field_value is None or field_value.text is None: return
    field_value = field_value.text
    if cast is not None: field_value = cast(field_value)
    target[field_name] = field_value

def add_value_from_collection(target : Dict, field_name: str, field_value : Collection) -> None:
    if field_value is None or len(field_value) == 0: return
    target[field_name] = field_value

"""
# Method Name: generate_templates

# Parameters:
  - resource_key:   [str]  Variable to identify the rule to be executed.
  - resource_value: [str]  Variable with the configuration parameters of the rule to be executed.
  - delete:         [bool] Variable to identify whether to create or delete the rule.
  - vendor:         [str]  Variable to identify the vendor of the equipment to be configured.

# Functionality:
  This method generates the template to configure the equipment using pyangbind.
  To generate the template the following steps are performed:
  1) Get the first parameter of the variable "resource_key" to identify the main path of the rule.
  2) Search for the specific configuration path
  3) Call the method with the configuration parameters (resource_data variable).

# Return:
  [dict] Set of templates generated according to the configuration rule
"""
def generate_templates(resource_key: str, resource_value: str, delete: bool,vendor:str) -> str:    # template management to be configured

    result_templates = []
    list_resource_key = resource_key.split("/")                                         # the rule resource key management
    if "network_instance" in list_resource_key[1]:                                      # network instance rules management
        data: Dict[str, Any] = json.loads(resource_value)
        #data['DEL'] = delete
        if "connection_point" in resource_key:
            result_templates.append(associate_virtual_circuit(data))
        elif "inter_instance_policies" in resource_key:
            result_templates.append(associate_RP_to_NI(data))
        elif "protocols" in resource_key:
            if vendor is None or vendor == "ADVA":
                result_templates.append(add_protocol_NI(data, vendor, delete))
        elif "table_connections" in resource_key:
            result_templates.append(create_table_conns(data, delete))
        elif "interface" in resource_key:
            result_templates.append(associate_If_to_NI(data,delete))
        else:
            result_templates.append(create_NI(data,vendor,delete))

    elif "interface" in list_resource_key[1]:                                           # interface rules management
        data: Dict[str, Any] = json.loads(resource_value)
        #data['DEL'] = delete
        if "subinterface" in resource_key:
            result_templates.append(create_If_SubIf(data, vendor, delete))

    elif "routing_policy" in list_resource_key[1]:                                      # routing policy rules management
        data: Dict[str, Any] = json.loads(resource_value)
        #data['DEL'] = delete
        if "bgp_defined_set" in resource_key:
            result_templates.append(create_rp_def(data, delete))
        else:
            result_templates.append(create_rp_statement(data, delete))
    elif "acl_ruleset" in resource_key:                                               # acl rules management
            result_templates.extend(acl_mgmt(resource_value,vendor, delete))
    else:
        if "ip_link" in resource_key:
            result_templates.append(ip_link_mgmt(resource_value,vendor,delete))

    return result_templates
