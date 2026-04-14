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


import ipaddress
from typing import TYPE_CHECKING, Dict, Union
from .Exceptions import MissingFieldException, UnsupportedElementException
from .ProtocolEnum import get_protocol_from_str

if TYPE_CHECKING:
    from .Rule import Rule


def parse_nft_ip_addr(right : Union[str, Dict]) -> ipaddress.IPv4Interface:
    if isinstance(right, str):
        address = right
        prefix_len = 32
    elif isinstance(right, Dict):
        if 'prefix' not in right: raise MissingFieldException('match[ip].right.prefix', right)
        prefix = right['prefix']
        if 'addr' not in prefix: raise MissingFieldException('match[ip].right.prefix.addr', prefix)
        if 'len' not in prefix: raise MissingFieldException('match[ip].right.prefix.len', prefix)
        address = prefix['addr']
        prefix_len = prefix['len']
    else:
        raise UnsupportedElementException('match[ip].right', right)
    return ipaddress.IPv4Interface(f'{address}/{str(prefix_len)}')


def parse_nft_match(rule : 'Rule', match : Dict) -> int:
    if 'op' not in match: raise MissingFieldException('rule.expr.match.op', match)
    if 'left' not in match: raise MissingFieldException('rule.expr.match.left', match)
    if 'right' not in match: raise MissingFieldException('rule.expr.match.right', match)
    if match['op'] != '==': raise UnsupportedElementException('rule.expr.match.op', match)

    num_fields_updated = 0

    match_left = match['left']
    match_right = match['right']
    if 'meta' in match_left and 'key' in match_left['meta']:
        meta_key = match_left['meta']['key']
        if 'iifname' in meta_key:
            rule.input_if_name = match_right
            num_fields_updated += 1
        elif 'oifname' in meta_key:
            rule.output_if_name = match_right
            num_fields_updated += 1
        else:
            raise UnsupportedElementException('rule.expr.match', match)
    elif 'payload' in match_left:
        payload = match_left['payload']
        if 'protocol' in payload and 'field' in payload:
            protocol = payload['protocol']
            field_name = payload['field']
            if protocol == 'ip' and field_name == 'saddr':
                rule.src_ip_addr = parse_nft_ip_addr(match_right)
                num_fields_updated += 1
            elif protocol == 'ip' and field_name == 'daddr':
                rule.dst_ip_addr = parse_nft_ip_addr(match_right)
                num_fields_updated += 1
            elif protocol in {'tcp', 'udp'} and field_name == 'sport':
                rule.ip_protocol = get_protocol_from_str(protocol)
                rule.src_port = match_right
                num_fields_updated += 1
            elif protocol in {'tcp', 'udp'} and field_name == 'dport':
                rule.ip_protocol = get_protocol_from_str(protocol)
                rule.dst_port = match_right
                num_fields_updated += 1
            else:
                raise UnsupportedElementException('rule.expr.match', match)
        else:
            raise UnsupportedElementException('rule.expr.match', match)
    elif '&' in match_left:
        # matches on masks and marks are skipped
        pass
    else:
        raise UnsupportedElementException('rule.expr.match', match)

    return num_fields_updated