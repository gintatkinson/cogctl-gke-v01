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

from typing import Dict, TypedDict

from ..ACL.ACL_multivendor import RULE_TYPE_MAPPING, FORWARDING_ACTION_MAPPING, LOG_ACTION_MAPPING

class ACLRequestData(TypedDict):
    name: str  # acl-set name
    type: str  # acl-set type
    sequence_id: int  # acl-entry sequence-id
    source_address: str
    destination_address: str
    forwarding_action: str
    id: str  # interface id
    interface: str
    subinterface: int
    set_name_ingress: str  # ingress-acl-set name
    type_ingress: str  # ingress-acl-set type
    all: bool
    dscp: int
    protocol: int
    tcp_flags: str
    source_port: int
    destination_port: int

def acl_cr_to_dict(acl_cr_dict: Dict, subinterface:int = 0) -> Dict:
    rule_set = acl_cr_dict['rule_set']
    rule_set_entry = rule_set['entries'][0]
    rule_set_entry_match = rule_set_entry['match']
    rule_set_entry_action = rule_set_entry['action']

    name: str = rule_set['name']
    type: str = RULE_TYPE_MAPPING[rule_set["type"]]
    sequence_id = rule_set_entry['sequence_id']
    source_address = rule_set_entry_match['src_address']
    destination_address = rule_set_entry_match['dst_address']
    forwarding_action: str = FORWARDING_ACTION_MAPPING[rule_set_entry_action['forward_action']]
    interface_id = acl_cr_dict['interface']
    interface = interface_id
    set_name_ingress = name
    type_ingress = type

    return ACLRequestData(
        name=name,
        type=type,
        sequence_id=sequence_id,
        source_address=source_address,
        destination_address=destination_address,
        forwarding_action=forwarding_action,
        id=interface_id,
        interface=interface,
        # subinterface=subinterface,
        set_name_ingress=set_name_ingress,
        type_ingress=type_ingress,
        all=True,
        dscp=18,
        protocol=6,
        tcp_flags='TCP_SYN',
        source_port=22,
        destination_port=80
    )
