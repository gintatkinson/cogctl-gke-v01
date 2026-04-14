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

import json, libyang, logging
from typing import Any, Dict, List, Tuple
from common.proto.context_pb2 import AclDirectionEnum
from ._Handler import _Handler
from .YangHandler import YangHandler

LOGGER = logging.getLogger(__name__)

# ──────────────────────────  enum translations  ──────────────────────────

_TFS_OC_RULE_TYPE = {
    'ACLRULETYPE_IPV4': 'ACL_IPV4',
    'ACLRULETYPE_IPV6': 'ACL_IPV6',
}

_TFS_OC_FWD_ACTION = {
    'ACLFORWARDINGACTION_DROP': 'DROP',
    'ACLFORWARDINGACTION_ACCEPT': 'ACCEPT',
    'ACLFORWARDINGACTION_REJECT': 'REJECT',
}

_OC_TFS_RULE_TYPE = {v: k for k, v in _TFS_OC_RULE_TYPE.items()}
_OC_TFS_FWD_ACTION = {v: k for k, v in _TFS_OC_FWD_ACTION.items()}

# ─────────────────────────────────────────────────────────────────────────

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


class AclHandler(_Handler):
    def get_resource_key(self) -> str:
        return '/device/endpoint/acl_ruleset'

    def get_path(self) -> str:
        return '/openconfig-acl:acl'

    def compose(  # pylint: disable=too-many-locals
        self,
        resource_key: str,
        resource_value: Dict[str, Any],
        yang: YangHandler,
        delete: bool = False,
    ) -> Tuple[str, str]:
        rs = resource_value['rule_set']
        rs_name = rs['name']
        oc_type = _TFS_OC_RULE_TYPE[rs['type']]
        #device = resource_value['endpoint_id']['device_id']['device_uuid']['uuid']
        iface = resource_value['endpoint_id']['endpoint_uuid']['uuid']
        direction = resource_value['direction']

        if delete:
            path = f'/acl/acl-sets/acl-set[name={rs_name}][type={oc_type}]'
            return path, ''

        yang_acl: libyang.DContainer = yang.get_data_path('/openconfig-acl:acl')

        y_sets = yang_acl.create_path('acl-sets')
        y_set = y_sets.create_path(f'acl-set[name="{rs_name}"][type="{oc_type}"]')
        y_set.create_path('config/name', rs_name)
        y_set.create_path('config/type', oc_type)

        # Entries (ACEs)
        y_entries = y_set.create_path('acl-entries')
        for entry in rs.get('entries', []):
            seq = int(entry['sequence_id'])
            m_ = entry['match']
            src_address = m_.get('src_address', '0.0.0.0/0')
            dst_address = m_.get('dst_address', '0.0.0.0/0')
            src_port = m_.get('src_port')
            dst_port = m_.get('dst_port')
            act = _TFS_OC_FWD_ACTION[entry['action']['forward_action']]

            y_e = y_entries.create_path(f'acl-entry[sequence-id="{seq}"]')
            y_e.create_path('config/sequence-id', seq)

            y_ipv4 = y_e.create_path('ipv4')
            y_ipv4.create_path('config/source-address', src_address)
            y_ipv4.create_path('config/destination-address', dst_address)

            proto = m_.get('protocol')
            if proto is not None:
                y_ipv4.create_path('config/protocol', int(proto))

            if src_port or dst_port:
                y_trans = y_e.create_path('transport')
                if src_port:
                    y_trans.create_path("config/source-port", int(src_port))
                if dst_port:
                    y_trans.create_path("config/destination-port", int(dst_port))
                y_ipv4.create_path('config/protocol', int(proto))

            y_act = y_e.create_path('actions')
            y_act.create_path('config/forwarding-action', act)

        # Interface binding
        y_intfs = yang_acl.create_path('interfaces')
        y_intf = y_intfs.create_path(f'interface[id="{iface}"]')

        if direction in DIRECTION_INGRESS:
            y_ingress = y_intf.create_path('ingress-acl-sets')
            y_ingress_set = y_ingress.create_path(f'ingress-acl-set[set-name="{rs_name}"][type="{oc_type}"]')
            y_ingress_set.create_path('config/set-name', rs_name)
            y_ingress_set.create_path('config/type', oc_type)

        if direction in DIRECTION_EGRESS:
            y_egress = y_intf.create_path('egress-acl-sets')
            y_egress_set = y_egress.create_path(f'egress-acl-set[set-name="{rs_name}"][type="{oc_type}"]')
            y_egress_set.create_path('config/set-name', rs_name)
            y_egress_set.create_path('config/type', oc_type)

        json_data = yang_acl.print_mem('json')
        #json_data = str(node.print_mem(
        #    fmt='json', with_siblings=True, pretty=True,
        #    keep_empty_containers=True, include_implicit_defaults=True
        #))
        LOGGER.debug('JSON data: %s', json_data)
        json_obj = json.loads(json_data)['openconfig-acl:acl']

        # release generated nodes to prevent side effects
        node_ifs : libyang.DNode = yang_acl.find_path('/openconfig-acl:acl/interfaces')
        #if node is None: return None
        LOGGER.info('node_ifs = {:s}'.format(str(node_ifs)))
        node_ifs.unlink()
        node_ifs.free()

        # release generated nodes to prevent side effects
        node_acls : libyang.DNode = yang_acl.find_path('/openconfig-acl:acl/acl-sets')
        #if node is None: return None
        LOGGER.info('node_acls = {:s}'.format(str(node_acls)))
        node_acls.unlink()
        node_acls.free()

        return '/acl', json.dumps(json_obj)

    def parse(  # pylint: disable=too-many-locals
        self,
        json_data: Dict[str, Any],
        yang: YangHandler,
    ) -> List[Tuple[str, Dict[str, Any]]]:
        acl_tree = json_data.get('openconfig-acl:acl') or json_data
        results: List[Tuple[str, Dict[str, Any]]] = []

        for acl_set in acl_tree.get('acl-sets', {}).get('acl-set', []):
            rs_name = acl_set['name']
            oc_type = acl_set['config']['type']
            rs_type = _OC_TFS_RULE_TYPE[oc_type]

            rule_set: Dict[str, Any] = {
                'name': rs_name,
                'type': rs_type,
                'description': acl_set.get('config', {}).get('description', ''),
                'entries': [],
            }

            for ace in acl_set.get('acl-entries', {}).get('acl-entry', []):
                seq = ace['sequence-id']
                act = ace.get('actions', {}).get('config', {}).get('forwarding-action', 'DROP')
                fwd_tfs = _OC_TFS_FWD_ACTION[act]
                ipv4_cfg = ace.get('ipv4', {}).get('config', {})

                rule_set['entries'].append(
                    {
                        'sequence_id': seq,
                        'match': {
                            'src_address': ipv4_cfg.get('source-address', ''),
                            'dst_address': ipv4_cfg.get('destination-address', ''),
                        },
                        'action': {'forward_action': fwd_tfs},
                    }
                )

            # find where that ACL is bound (first matching interface)
            iface = ''
            for intf in acl_tree.get('interfaces', {}).get('interface', []):
                for ing in intf.get('ingress-acl-sets', {}).get('ingress-acl-set', []):
                    if ing['set-name'] == rs_name:
                        iface = intf['id']
                        break

            results.append(('/acl', {'interface': iface, 'rule_set': rule_set}))

        return results
