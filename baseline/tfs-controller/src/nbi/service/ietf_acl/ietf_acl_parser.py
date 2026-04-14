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

from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from werkzeug.exceptions import NotImplemented
from common.proto.acl_pb2 import AclForwardActionEnum, AclRuleTypeEnum, AclEntry
from common.proto.context_pb2 import ConfigActionEnum, ConfigRule, AclDirectionEnum as Proto_AclDirectionEnum


class AclDirectionEnum(Enum):
    BOTH    = 'both'
    INGRESS = 'ingress'
    EGRESS  = 'egress'


class Ipv4(BaseModel):
    dscp: int = 0
    source_ipv4_network: str = Field(serialization_alias='source-ipv4-network', default='')
    destination_ipv4_network: str = Field(
        serialization_alias='destination-ipv4-network', default=''
    )


class Port(BaseModel):
    port: int = 0
    operator: str = 'eq'


class Tcp(BaseModel):
    flags: Optional[str] = None
    source_port: Optional[Port] = Field(serialization_alias='source-port', default=None)
    destination_port: Optional[Port] = Field(serialization_alias='destination-port', default=None)


class Matches(BaseModel):
    ipv4: Ipv4 = Ipv4()
    tcp: Optional[Tcp] = None


class Action(BaseModel):
    forwarding: str = ''


class Ace(BaseModel):
    name: str = ''
    matches: Matches = Matches()
    actions: Action = Action()


class Aces(BaseModel):
    ace: List[Ace] = [Ace()]


class Acl(BaseModel):
    name: str = ''
    type: str = ''
    aces: Aces = Aces()


class Name(BaseModel):
    name: str = ''


class AclSet(BaseModel):
    acl_set: List[Name] = Field(serialization_alias='acl-set', default=[Name()])


class AclSets(BaseModel):
    acl_sets: AclSet = Field(serialization_alias='acl-sets', default=AclSet())


class Ingress(BaseModel):
    ingress: AclSets = AclSets()


class Egress(BaseModel):
    egress: AclSets = AclSets()


class Interface(BaseModel):
    interface_id: str = Field(serialization_alias='interface-id', default='')
    ingress: Optional[AclSets] = None
    egress: Optional[AclSets] = None


class Interfaces(BaseModel):
    interface: List[Interface] = [Interface()]


class Acls(BaseModel):
    acl: List[Acl] = [Acl()]
    attachment_points: Optional[Interfaces] = Field(
        serialization_alias='attachment-points', default=None
    )


class IETF_ACL(BaseModel):
    acls: Optional[Acls] = Field(serialization_alias='ietf-access-control-list:acls', default=None)


IETF_TFS_RULE_TYPE_MAPPING = {
    'ipv4-acl-type': 'ACLRULETYPE_IPV4',
    'ipv6-acl-type': 'ACLRULETYPE_IPV6',
}

IETF_TFS_FORWARDING_ACTION_MAPPING = {
    'accept': 'ACLFORWARDINGACTION_ACCEPT',
    'drop'  : 'ACLFORWARDINGACTION_DROP',
    'reject': 'ACLFORWARDINGACTION_REJECT',
}

TFS_IETF_RULE_TYPE_MAPPING = {
    'ACLRULETYPE_IPV4': 'ipv4-acl-type',
    'ACLRULETYPE_IPV6': 'ipv6-acl-type',
}

TFS_IETF_FORWARDING_ACTION_MAPPING = {
    'ACLFORWARDINGACTION_ACCEPT': 'accept',
    'ACLFORWARDINGACTION_DROP'  : 'drop',
    'ACLFORWARDINGACTION_REJECT': 'reject',
}


def config_rule_from_ietf_acl(
    device_name : str, endpoint_name : str, acl_direction : AclDirectionEnum,
    acl_set_data : Dict
) -> ConfigRule:
    acl_config_rule = ConfigRule()
    acl_config_rule.action = ConfigActionEnum.CONFIGACTION_SET

    acl_endpoint_id = acl_config_rule.acl.endpoint_id
    acl_endpoint_id.device_id.device_uuid.uuid = device_name
    acl_endpoint_id.endpoint_uuid.uuid = endpoint_name

    if acl_direction == AclDirectionEnum.INGRESS:
        acl_config_rule.acl.direction = Proto_AclDirectionEnum.ACLDIRECTION_INGRESS
    elif acl_direction == AclDirectionEnum.EGRESS:
        acl_config_rule.acl.direction = Proto_AclDirectionEnum.ACLDIRECTION_EGRESS
    else:
        acl_config_rule.acl.direction = Proto_AclDirectionEnum.ACLDIRECTION_BOTH

    acl_name = acl_set_data['name']
    acl_type = acl_set_data['type']
    if acl_type.startswith('ietf-access-control-list:'):
        acl_type = acl_type.replace('ietf-access-control-list:', '')
    acl_type = getattr(AclRuleTypeEnum, IETF_TFS_RULE_TYPE_MAPPING[acl_type])

    acl_rule_set = acl_config_rule.acl.rule_set
    acl_rule_set.name = acl_name
    acl_rule_set.type = acl_type
    # acl_rule_set.description = ...

    access_control_entry_list = acl_set_data.get('aces', {}).get('ace', [])
    for sequence_id, ace in enumerate(access_control_entry_list):
        ace_name = ace['name']
        ace_matches = ace.get('matches', {})
        ace_actions = ace.get('actions', {})

        acl_entry = AclEntry()
        acl_entry.sequence_id = sequence_id + 1
        acl_entry.description = ace_name

        if 'ipv4' in ace_matches:
            ipv4_data = ace_matches['ipv4']
            if 'source-ipv4-network' in ipv4_data:
                acl_entry.match.src_address = ipv4_data['source-ipv4-network']
            if 'destination-ipv4-network' in ipv4_data:
                acl_entry.match.dst_address = ipv4_data['destination-ipv4-network']
            if 'dscp' in ipv4_data:
                acl_entry.match.dscp = ipv4_data['dscp']
            if 'protocol' in ipv4_data:
                acl_entry.match.protocol = ipv4_data['protocol']

        if 'tcp' in ace_matches:
            # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
            acl_entry.match.protocol = 6
            tcp_data = ace_matches['tcp']
            if 'source-port' in tcp_data:
                tcp_src_port: Dict = tcp_data['source-port']
                tcp_src_port_op = tcp_src_port.get('operator', 'eq')
                if tcp_src_port_op != 'eq':
                    MSG = 'Acl({:s})/Ace({:s})/Match/Tcp({:s}) operator not supported'
                    raise NotImplemented(MSG.format(acl_name, ace_name, str(tcp_data)))
                acl_entry.match.src_port = tcp_src_port['port']
            if 'destination-port' in tcp_data:
                tcp_dst_port: Dict = tcp_data['destination-port']
                tcp_dst_port_op = tcp_dst_port.get('operator', 'eq')
                if tcp_dst_port_op != 'eq':
                    MSG = 'Acl({:s})/Ace({:s})/Match/Tcp({:s}) operator not supported'
                    raise NotImplemented(MSG.format(acl_name, ace_name, str(tcp_data)))
                acl_entry.match.dst_port = tcp_dst_port['port']
            if 'flags' in tcp_data:
                acl_entry.match.tcp_flags = tcp_data['flags']

        if 'udp' in ace_matches:
            # https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
            acl_entry.match.protocol = 17
            udp_data = ace_matches['udp']
            if 'source-port' in udp_data:
                udp_src_port: Dict = udp_data['source-port']
                udp_src_port_op = udp_src_port.get('operator', 'eq')
                if udp_src_port_op != 'eq':
                    MSG = 'Acl({:s})/Ace({:s})/Match/Udp({:s}) operator not supported'
                    raise NotImplemented(MSG.format(acl_name, ace_name, str(udp_data)))
                acl_entry.match.src_port = udp_src_port['port']
            if 'destination-port' in udp_data:
                udp_dst_port: Dict = udp_data['destination-port']
                udp_dst_port_op = udp_dst_port.get('operator', 'eq')
                if udp_dst_port_op != 'eq':
                    MSG = 'Acl({:s})/Ace({:s})/Match/Udp({:s}) operator not supported'
                    raise NotImplemented(MSG.format(acl_name, ace_name, str(udp_data)))
                acl_entry.match.dst_port = udp_dst_port['port']

        if 'forwarding' in ace_actions:
            ace_forward_action = ace_actions['forwarding']
            if ace_forward_action.startswith('ietf-access-control-list:'):
                ace_forward_action = ace_forward_action.replace('ietf-access-control-list:', '')
            ace_forward_action = IETF_TFS_FORWARDING_ACTION_MAPPING[ace_forward_action]
            acl_entry.action.forward_action = getattr(AclForwardActionEnum, ace_forward_action)

        acl_rule_set.entries.append(acl_entry)

    return acl_config_rule


def ietf_acl_from_config_rule_resource_value(config_rule_rv: Dict) -> Dict:
    rule_set = config_rule_rv['rule_set']
    ace = []

    for acl_entry in rule_set['entries']:
        match_ = acl_entry['match']
        ipv4 = Ipv4(
            dscp=match_['dscp'],
            source_ipv4_network=match_['src_address'],
            destination_ipv4_network=match_['dst_address'],
        )
        tcp = None
        if match_['tcp_flags']:
            tcp = Tcp(
                flags=match_['tcp_flags'],
                source_port=Port(port=match_['src_port']),
                destination_port=Port(port=match_['dst_port']),
            )
        matches = Matches(ipv4=ipv4, tcp=tcp)
        ace.append(
            Ace(
                name=acl_entry['description'],
                matches=matches,
                actions=Action(
                    forwarding=TFS_IETF_FORWARDING_ACTION_MAPPING[
                        acl_entry['action']['forward_action']
                    ]
                ),
            )
        )
    aces = Aces(ace=ace)
    acl = Acl(name=rule_set['name'], type=TFS_IETF_RULE_TYPE_MAPPING[rule_set['type']], aces=aces)
    acl_sets = AclSets(acl_sets=AclSet(acl_set=[Name(name=rule_set['name'])]))
    interfaces = Interfaces(
        interface=[
            Interface(
                interface_id=config_rule_rv['endpoint_id']['endpoint_uuid']['uuid'],
                ingress=acl_sets,
            )
        ]
    )
    acls = Acls(acl=[acl], attachment_points=interfaces)
    ietf_acl = IETF_ACL(acls=acls)

    return ietf_acl.model_dump(by_alias=True, exclude_none=True)
