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


import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from common.proto.context_pb2 import AclDirectionEnum
from common.tools.rest_conf.client.RestConfClient import RestConfClient


LOGGER = logging.getLogger(__name__)


_TFS_2_OC_RULE_TYPE = {
    'ACLRULETYPE_IPV4': 'ACL_IPV4',
    'ACLRULETYPE_IPV6': 'ACL_IPV6',
}
_OC_2_TFS_RULE_TYPE  = {v: k for k, v in _TFS_2_OC_RULE_TYPE.items() }

_TFS_2_OC_PROTOCOL = {
    1  : 'IP_ICMP',
    6  : 'IP_TCP',
    17 : 'IP_UDP',
}
_OC_2_TFS_PROTOCOL  = {v: k for k, v in _TFS_2_OC_PROTOCOL.items() }

_TFS_2_OC_FWD_ACTION = {
    'ACLFORWARDINGACTION_DROP'  : 'DROP',
    'ACLFORWARDINGACTION_ACCEPT': 'ACCEPT',
    'ACLFORWARDINGACTION_REJECT': 'REJECT',
}
_OC_2_TFS_FWD_ACTION = {v: k for k, v in _TFS_2_OC_FWD_ACTION.items()}


DIRECTION_INGRESS = {
    AclDirectionEnum.ACLDIRECTION_BOTH,
    AclDirectionEnum.Name(AclDirectionEnum.ACLDIRECTION_BOTH),
    AclDirectionEnum.ACLDIRECTION_INGRESS,
    AclDirectionEnum.Name(AclDirectionEnum.ACLDIRECTION_INGRESS),
}

DIRECTION_EGRESS = {
    AclDirectionEnum.ACLDIRECTION_BOTH,
    AclDirectionEnum.Name(AclDirectionEnum.ACLDIRECTION_BOTH),
    AclDirectionEnum.ACLDIRECTION_EGRESS,
    AclDirectionEnum.Name(AclDirectionEnum.ACLDIRECTION_EGRESS),
}


class AclRuleSetHandler:
    def __init__(self, rest_conf_client : RestConfClient) -> None:
        self._rest_conf_client = rest_conf_client
        self._subpath_root = '/openconfig-acl:acl'
        self._subpath_item = self._subpath_root + '/acl-sets/acl-set={acl_ruleset_name:s}'


    def get(self, acl_ruleset_name : Optional[str] = None) -> Union[Dict, List]:
        if acl_ruleset_name is None:
            subpath_url = self._subpath_root
        else:
            subpath_url = self._subpath_item.format(acl_ruleset_name=acl_ruleset_name)

        reply = self._rest_conf_client.get(subpath_url)

        if 'openconfig-acl:acl' not in reply:
            raise Exception('Malformed reply. "openconfig-acl:acl" missing')
        acls = reply['openconfig-acl:acl']

        if 'acl-sets' not in acls:
            raise Exception('Malformed reply. "openconfig-acl:acl/acl-sets" missing')
        aclsets = acls['acl-sets']

        if 'acl-set' not in aclsets:
            raise Exception('Malformed reply. "openconfig-acl:acl/acl-sets/acl-set" missing')
        aclset_lst = aclsets['acl-set']

        if len(aclset_lst) == 0:
            MSG = '[get] No ACL-Sets are reported'
            LOGGER.debug(MSG)
            return list()

        results : List[Tuple[str, Dict[str, Any]]] = list()
        for acl_set in aclset_lst:
            acl_set_name = acl_set['name']
            oc_acl_set_type = acl_set['config']['type']
            tfs_acl_set_type = _OC_2_TFS_RULE_TYPE[oc_acl_set_type]

            rule_set: Dict[str, Any] = {
                'name'       : acl_set_name,
                'type'       : tfs_acl_set_type,
                'entries'    : [],
            }

            acl_set_config : Dict = acl_set.get('config', {})
            acl_set_description = acl_set_config.get('description')
            if acl_set_description is not None:
                rule_set['description'] = acl_set_description

            for ace in acl_set.get('acl-entries', {}).get('acl-entry', []):
                seq = ace['sequence-id']

                ipv4_cfg = ace.get('ipv4', {}).get('config', {})
                match = dict()
                if 'source-address' in ipv4_cfg:
                    match['src_address'] = ipv4_cfg['source-address']
                if 'destination-address' in ipv4_cfg:
                    match['dst_address'] = ipv4_cfg['destination-address']
                if 'protocol' in ipv4_cfg:
                    match['protocol'] = _OC_2_TFS_PROTOCOL[ipv4_cfg['protocol']]

                transp_cfg = ace.get('transport', {}).get('config', {})
                if 'source-port' in transp_cfg:
                    match['src_port'] = transp_cfg['source-port']
                if 'destination-port' in transp_cfg:
                    match['dst_port'] = transp_cfg['destination-port']

                act = ace.get('actions', {}).get('config', {}).get('forwarding-action', 'DROP')
                fwd_tfs = _OC_2_TFS_FWD_ACTION[act]

                rule_set['entries'].append({
                    'sequence_id': seq,
                    'match': match,
                    'action': {'forward_action': fwd_tfs},
                })

            # find where that ACL is bound (first matching interface)
            if_name = ''
            for intf in acls.get('interfaces', {}).get('interface', []):
                for ing in intf.get('ingress-acl-sets', {}).get('ingress-acl-set', []):
                    if ing['set-name'] == acl_set_name:
                        if_name = intf['id']
                        break

            path = '/device[]/endpoint[{:s}]/acl_ruleset[{:s}]'.format(
                if_name, acl_set_name
            )
            tfs_acl_data = {
                'endpoint_id': {'endpoint_uuid': {'uuid': if_name}},
                'direction': 'ACLDIRECTION_INGRESS',
                'rule_set': rule_set,
            }
            results.append((path, tfs_acl_data))

        return results


    def update(self, acl_data : Dict) -> bool:
        if_name   = acl_data['endpoint_id']['endpoint_uuid']['uuid']
        direction = acl_data['direction']
        rule_set  = acl_data['rule_set']

        if direction in DIRECTION_INGRESS:
            acl_set_name = 'ip-filter-input'
        elif direction in DIRECTION_EGRESS:
            acl_set_name = 'ip-filter-output'
        else:
            MSG = 'Unsupported direction: {:s}'
            raise Exception(MSG.format(str(direction)))

        acl_entry_desc = rule_set['name']
        acl_set_type   = _TFS_2_OC_RULE_TYPE[rule_set['type']]

        oc_acl_entries = list()
        sequence_ids : List[int] = list()
        for entry in rule_set.get('entries', []):
            sequence_id = int(entry['sequence_id'])
            oc_action = _TFS_2_OC_FWD_ACTION[entry['action']['forward_action']]
            oc_acl_entry = {
                'sequence-id': sequence_id,
                'config': {'sequence-id': sequence_id, 'description' : acl_entry_desc},
                'actions': {'config': {'forwarding-action': oc_action}}
            }

            entry_match = entry.get('match', dict())

            ipv4_config = dict()
            if 'protocol' in entry_match and entry_match['protocol'] > 0:
                ipv4_config['protocol'] = _TFS_2_OC_PROTOCOL[entry_match['protocol']]
            if 'src_address' in entry_match and len(entry_match['src_address']) > 0:
                ipv4_config['source-address'] = entry_match['src_address']
            if 'dst_address' in entry_match and len(entry_match['dst_address']) > 0:
                ipv4_config['destination-address'] = entry_match['dst_address']
            if len(ipv4_config) > 0:
                oc_acl_entry.setdefault('ipv4', dict())['config'] = ipv4_config

            transport_config = dict()
            if 'src_port' in entry_match and entry_match['src_port'] > 0:
                transport_config['source-port'] = entry_match['src_port']
            if 'dst_port' in entry_match and entry_match['dst_port'] > 0:
                transport_config['destination-port'] = entry_match['dst_port']
            if len(transport_config) > 0:
                oc_acl_entry.setdefault('transport', dict())['config'] = transport_config

            oc_acl_entries.append(oc_acl_entry)
            sequence_ids.append(sequence_id)

        oc_interface = {
            'id': if_name,
            'config': {'id': if_name},
            'interface-ref': {'config': {'interface': if_name, 'subinterface': 1}},
        }

        if direction in DIRECTION_INGRESS:
            oc_interface['ingress-acl-sets'] = {'ingress-acl-set': [{
                'set-name': acl_set_name, 'type': acl_set_type,
                'config': {'set-name': acl_set_name, 'type': acl_set_type},
                'acl-entries': {'acl-entry': [
                    {'sequence-id': sequence_id}
                    for sequence_id in sequence_ids
                ]}
            }]}

        if direction in DIRECTION_EGRESS:
            oc_interface['egress-acl-sets'] = {'egress-acl-set': [{
                'set-name': acl_set_name, 'type': acl_set_type,
                'config': {'set-name': acl_set_name, 'type': acl_set_type},
                'acl-entries': {'acl-entry': [
                    {'sequence-id': sequence_id}
                    for sequence_id in sequence_ids
                ]}
            }]}

        oc_acl_data = {'openconfig-acl:acl': {
            'acl-sets': {'acl-set': [{
                'name': acl_set_name, 'type': acl_set_type,
                'config': {'name': acl_set_name, 'type': acl_set_type},
                'acl-entries': {'acl-entry': oc_acl_entries},
            }]},
            'interfaces': {'interface': [oc_interface]},
        }}
        return self._rest_conf_client.post(self._subpath_root, body=oc_acl_data) is not None


    def delete(self, acl_ruleset_name : str) -> bool:
        if acl_ruleset_name is None: raise Exception('acl_ruleset_name is None')
        subpath_url = self._subpath_item.format(acl_ruleset_name=acl_ruleset_name)
        return self._rest_conf_client.delete(subpath_url)
