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


RULE_TYPE_MAPPING = {
    'ACLRULETYPE_IPV4'     : 'ip',
}

FORWARDING_ACTION_MAPPING = {
    'ACLFORWARDINGACTION_DROP'     : 'deny',
    'ACLFORWARDINGACTION_ACCEPT'   : 'permit',
}

class ACLRequestData(TypedDict):
    name: str  # acl-set name
    type: str  # acl-set type
    sequence_id: int  # acl-entry sequence-id
    source_address: str
    destination_address: str
    forwarding_action: str
    interface: str
    dscp: int
    tcp_flags: str
    source_port: int
    destination_port: int

def acl_cr_to_dict_ipinfusion_proprietary(acl_cr_dict: Dict, delete: bool = False) -> Dict:
    rule_set = acl_cr_dict['rule_set']
    name: str = rule_set['name']
    type: str = RULE_TYPE_MAPPING[rule_set["type"]]
    interface = acl_cr_dict['interface'][5:] # remove preceding `PORT-` characters
    if delete:
        return ACLRequestData(name=name, type=type, interface=interface)
    rule_set_entry = rule_set['entries'][0]
    rule_set_entry_match = rule_set_entry['match']
    rule_set_entry_action = rule_set_entry['action']

    return ACLRequestData(
        name=name,
        type=type,
        sequence_id=rule_set_entry['sequence_id'],
        source_address=rule_set_entry_match['src_address'],
        destination_address=rule_set_entry_match['dst_address'],
        forwarding_action=FORWARDING_ACTION_MAPPING[rule_set_entry_action['forward_action']],
        interface=interface,
        dscp=rule_set_entry_match["dscp"],
        tcp_flags=rule_set_entry_match["flags"],
        source_port=rule_set_entry_match['src_port'],
        destination_port=rule_set_entry_match['dst_port']
    )
