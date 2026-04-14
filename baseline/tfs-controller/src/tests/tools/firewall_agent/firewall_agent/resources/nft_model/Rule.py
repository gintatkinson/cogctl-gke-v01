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


import copy, ipaddress, logging
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Set, Tuple
from .ActionEnum import ActionEnum, get_action_from_str
from .DirectionEnum import DirectionEnum
from .Exceptions import MissingFieldException, UnsupportedElementException
from .FamilyEnum import FamilyEnum
from .NFTablesParserTools import parse_nft_match
from .ProtocolEnum import ProtocolEnum
from .TableEnum import TableEnum


LOGGER = logging.getLogger(__name__)


OPENCONFIG_ACL_ACTION_TO_NFT = {
    'ACCEPT' : ActionEnum.ACCEPT,
    'DROP'   : ActionEnum.DROP,
    'REJECT' : ActionEnum.REJECT,
}

def get_nft_action_from_openconfig(oc_action : str) -> ActionEnum:
    nft_action = OPENCONFIG_ACL_ACTION_TO_NFT.get(oc_action)
    if nft_action is None:
        supported_values = set(OPENCONFIG_ACL_ACTION_TO_NFT.keys())
        raise UnsupportedElementException(
            'acl_entry.actions.config.forwarding-action', str(oc_action),
            extra=f'supported_values={str(supported_values)}'
        )
    return nft_action


OPENCONFIG_IPV4_PROTOCOL_TO_NFT = {
    'IP_TCP'  : ProtocolEnum.TCP,
    'IP_UDP'  : ProtocolEnum.UDP,
    'IP_ICMP' : ProtocolEnum.ICMP,
}

def get_nft_ipv4_protocol_from_openconfig(oc_ipv4_protocol : str) -> ProtocolEnum:
    nft_protocol = OPENCONFIG_IPV4_PROTOCOL_TO_NFT.get(oc_ipv4_protocol)
    if nft_protocol is None:
        supported_values = set(OPENCONFIG_IPV4_PROTOCOL_TO_NFT.keys())
        raise UnsupportedElementException(
            'acl_entry.ipv4.config.protocol', str(oc_ipv4_protocol),
            extra=f'supported_values={str(supported_values)}'
        )
    return nft_protocol


@dataclass
class Rule:
    family         : FamilyEnum
    table          : TableEnum
    chain          : str
    handle         : Optional[int] = None

    sequence_id    : int           = 0

    input_if_name  : Optional[str] = None
    output_if_name : Optional[str] = None
    src_ip_addr    : Optional[ipaddress.IPv4Interface] = None
    dst_ip_addr    : Optional[ipaddress.IPv4Interface] = None
    ip_protocol    : Optional[ProtocolEnum] = None
    src_port       : Optional[int] = None
    dst_port       : Optional[int] = None

    action         : Optional[ActionEnum] = None

    comment        : Optional[str] = None

    @classmethod
    def from_nft_entry(
        cls, family : FamilyEnum, table : TableEnum, chain : str, entry : Dict
    ) -> 'Rule':
        rule : 'Rule' = cls(family, table, chain)

        if 'expr' not in entry: raise MissingFieldException('rule.expr', entry)
        expr_list : List[Dict] = entry['expr']
        num_fields_updated = 0
        for expr_entry in expr_list:
            expr_entry_fields = set(expr_entry.keys())
            expr_entry_type = expr_entry_fields.pop()
            if expr_entry_type == 'match':
                match = expr_entry['match']
                num_fields_updated += parse_nft_match(rule, match)
            elif expr_entry_type in {'accept', 'drop', 'reject'}:
                rule.action = get_action_from_str(expr_entry_type)
                num_fields_updated += 1
            elif expr_entry_type in {'counter', 'jump', 'xt'}:
                pass # ignore these entry types
            else:
                raise UnsupportedElementException('expr_entry', expr_entry)

        if num_fields_updated == 0:
            # Ignoring empty/unsupported rule...
            return None

        rule.comment = entry.pop('comment', None)
        rule.handle = entry['handle']
        return rule

    @classmethod
    def from_openconfig(
        cls, family : FamilyEnum, table : TableEnum, chain : str, acl_entry : Dict
    ) -> 'Rule':
        rule : 'Rule' = cls(family, table, chain)

        rule.sequence_id = int(acl_entry['config']['sequence-id'])
        rule.comment = acl_entry['config']['description']

        ipv4_config = acl_entry.get('ipv4', {}).get('config', {})
        if 'source-address' in ipv4_config:
            rule.src_ip_addr = ipaddress.IPv4Interface(ipv4_config['source-address'])

        if 'destination-address' in ipv4_config:
            rule.dst_ip_addr = ipaddress.IPv4Interface(ipv4_config['destination-address'])

        if 'protocol' in ipv4_config:
            ip_protocol = ipv4_config['protocol']
            rule.ip_protocol = get_nft_ipv4_protocol_from_openconfig(ip_protocol)

        transp_config = acl_entry.get('transport', {}).get('config', {})
        rule.src_port = transp_config.get('source-port')
        rule.dst_port = transp_config.get('destination-port')

        action = acl_entry['actions']['config']['forwarding-action']
        rule.action = get_nft_action_from_openconfig(action)

        return rule

    def to_openconfig(self, sequence_id : int) -> Tuple[Dict, Dict]:
        acl_entry_config = {'sequence-id': sequence_id}
        if self.comment is not None: acl_entry_config['description'] = self.comment

        acl_entry = {
            'sequence-id': sequence_id,
            'config': acl_entry_config,
            'state': copy.deepcopy(acl_entry_config),
        }

        ip_version = {
            FamilyEnum.IPV4: 'ipv4',
            FamilyEnum.IPV6: 'ipv6',
        }.get(self.family)

        ip_protocol = {
            ProtocolEnum.TCP  : 'IP_TCP',
            ProtocolEnum.UDP  : 'IP_UDP',
            ProtocolEnum.ICMP : 'IP_ICMP',
        }.get(self.ip_protocol, None)

        if self.src_ip_addr is not None:
            acl_entry_ipvx = acl_entry.setdefault(ip_version, dict())
            acl_entry_ipvx_config = acl_entry_ipvx.setdefault('config', dict())
            acl_entry_ipvx_config['source-address'] = str(self.src_ip_addr.network)
            acl_entry_ipvx_state = acl_entry_ipvx.setdefault('state', dict())
            acl_entry_ipvx_state['source-address'] = str(self.src_ip_addr.network)

        if self.dst_ip_addr is not None:
            acl_entry_ipvx = acl_entry.setdefault(ip_version, dict())
            acl_entry_ipvx_config = acl_entry_ipvx.setdefault('config', dict())
            acl_entry_ipvx_config['destination-address'] = str(self.dst_ip_addr.network)
            acl_entry_ipvx_state = acl_entry_ipvx.setdefault('state', dict())
            acl_entry_ipvx_state['destination-address'] = str(self.dst_ip_addr.network)

        if ip_protocol is not None:
            acl_entry_ipvx = acl_entry.setdefault(ip_version, dict())
            acl_entry_ipvx_config = acl_entry_ipvx.setdefault('config', dict())
            acl_entry_ipvx_config['protocol'] = ip_protocol
            acl_entry_ipvx_state = acl_entry_ipvx.setdefault('state', dict())
            acl_entry_ipvx_state['protocol'] = ip_protocol

        if self.src_port is not None:
            acl_entry_trans = acl_entry.setdefault('transport', dict())
            acl_entry_trans_config = acl_entry_trans.setdefault('config', dict())
            acl_entry_trans_config['source-port'] = self.src_port
            acl_entry_trans_state = acl_entry_trans.setdefault('state', dict())
            acl_entry_trans_state['source-port'] = self.src_port

        if self.dst_port is not None:
            acl_entry_trans = acl_entry.setdefault('transport', dict())
            acl_entry_trans_config = acl_entry_trans.setdefault('config', dict())
            acl_entry_trans_config['destination-port'] = self.dst_port
            acl_entry_trans_state = acl_entry_trans.setdefault('state', dict())
            acl_entry_trans_state['destination-port'] = self.dst_port

        if self.action is not None:
            acl_forwarding_action = {
                ActionEnum.ACCEPT : 'ACCEPT',
                ActionEnum.DROP   : 'DROP',
                ActionEnum.REJECT : 'REJECT',
            }.get(self.action)
            acl_action = {'forwarding-action': acl_forwarding_action}
            acl_entry['actions'] = {'config': acl_action, 'state': acl_action}

        interfaces : Dict[str, Dict[DirectionEnum, Set[int]]] = dict()

        if self.input_if_name is not None:
            interface : Dict = interfaces.setdefault(self.input_if_name, dict())
            direction : Set = interface.setdefault(DirectionEnum.INGRESS, set())
            direction.add(sequence_id)

        if self.output_if_name is not None:
            interface : Dict = interfaces.setdefault(self.output_if_name, dict())
            direction : Set = interface.setdefault(DirectionEnum.EGRESS, set())
            direction.add(sequence_id)

        return acl_entry, interfaces


    def dump(self) -> List[Dict]:
        rule = {'family': self.family.value, 'table': self.table.value, 'chain': self.chain}
        expr = list()
        if self.input_if_name is not None:
            match_left = {'meta': {'key': 'iifname'}}
            expr.append({'match': {'op': '==', 'left': match_left, 'right': self.input_if_name}})
        if self.output_if_name is not None:
            match_left = {'meta': {'key': 'oifname'}}
            expr.append({'match': {'op': '==', 'left': match_left, 'right': self.output_if_name}})
        if self.src_ip_addr is not None:
            match_left = {'payload': {'protocol': 'ip', 'field': 'saddr'}}
            match_right = {'prefix': {'addr': str(self.src_ip_addr.ip), 'len': self.src_ip_addr.network.prefixlen}}
            expr.append({'match': {'op': '==', 'left': match_left, 'right': match_right}})
        if self.dst_ip_addr is not None:
            match_left = {'payload': {'protocol': 'ip', 'field': 'daddr'}}
            match_right = {'prefix': {'addr': str(self.dst_ip_addr.ip), 'len': self.dst_ip_addr.network.prefixlen}}
            expr.append({'match': {'op': '==', 'left': match_left, 'right': match_right}})
        if self.src_port is not None:
            match_left = {'payload': {'protocol': self.ip_protocol.value, 'field': 'sport'}}
            expr.append({'match': {'op': '==', 'left': match_left, 'right': self.src_port}})
        if self.dst_port is not None:
            match_left = {'payload': {'protocol': self.ip_protocol.value, 'field': 'dport'}}
            expr.append({'match': {'op': '==', 'left': match_left, 'right': self.dst_port}})
        if self.action is not None: expr.append({self.action.value : None})
        if len(expr) > 0: rule['expr'] = expr
        if self.comment is not None: rule['comment'] = self.comment
        if self.handle is not None: rule['handle'] = self.handle
        return [{'rule': rule}]

    def get_command(self, removal : bool = False) -> Optional[Tuple[int, str]]:
        if removal:
            if self.handle is None: raise MissingFieldException('handle', asdict(self))
            parts = [
                'delete', 'rule',  # Ideally destroy (fail silently if not exist), but seems not supported.
                self.family.value, self.table.value, self.chain,
                'handle', str(self.handle)
            ]
            return self.sequence_id, ' '.join(parts)
        elif self.handle is not None:
            # NOTE: Rule was already there, do not modify it
            return None
        else:
            # NOTE: if sequence_id < 10000: insert the rules to the top;
            # otherwise, append to the bottom. Anyways, sort rules by sequence_id.
            verb = 'insert' if self.sequence_id < 10000 else 'add'
            parts = [verb, 'rule', self.family.value, self.table.value, self.chain]
            if self.input_if_name is not None: parts.extend(['iifname', self.input_if_name])
            if self.output_if_name is not None: parts.extend(['oifname', self.output_if_name])
            if self.src_ip_addr is not None: parts.extend(['ip', 'saddr', str(self.src_ip_addr)])
            if self.dst_ip_addr is not None: parts.extend(['ip', 'daddr', str(self.dst_ip_addr)])
            if self.src_port is not None: parts.extend([self.ip_protocol.value, 'sport', str(self.src_port)])
            if self.dst_port is not None: parts.extend([self.ip_protocol.value, 'dport', str(self.dst_port)])
            if self.action is not None: parts.append(self.action.value)
            if self.comment is not None: parts.extend(['comment', f'"{self.comment}"'])
            return self.sequence_id, ' '.join(parts)
