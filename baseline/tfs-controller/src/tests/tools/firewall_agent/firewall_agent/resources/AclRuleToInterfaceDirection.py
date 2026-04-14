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


from typing import Dict, List, Tuple
from .nft_model.DirectionEnum import DirectionEnum
from .nft_model.FamilyEnum import FamilyEnum
from .nft_model.NFTables import NFTables
from .nft_model.TableEnum import TableEnum


TYPE_ACL_RULE_SEQ_ID    = Tuple[str, int]
TYPE_IFACE_DIRECTION    = Tuple[str, DirectionEnum]
TYPE_IFACE_DIRECTIONS   = List[TYPE_IFACE_DIRECTION]
TYPE_ACL_RULE_TO_IF_DIR = Dict[TYPE_ACL_RULE_SEQ_ID, TYPE_IFACE_DIRECTIONS]


CHAIN_NAME_PREROUTING  = 'PREROUTING'
CHAIN_NAME_INPUT       = 'INPUT'
CHAIN_NAME_FORWARD     = 'FORWARD'
CHAIN_NAME_OUTPUT      = 'OUTPUT'
CHAIN_NAME_POSTROUTING = 'POSTROUTING'

CHAINS_INPUT  = [
    CHAIN_NAME_PREROUTING, CHAIN_NAME_INPUT, CHAIN_NAME_FORWARD
]
CHAINS_OUTPUT = [
    CHAIN_NAME_FORWARD, CHAIN_NAME_OUTPUT, CHAIN_NAME_POSTROUTING
]
CHAINS_ALL    = [
    CHAIN_NAME_PREROUTING, CHAIN_NAME_INPUT, CHAIN_NAME_FORWARD,
    CHAIN_NAME_OUTPUT, CHAIN_NAME_POSTROUTING
]


def get_family_from_acl_set_type(acl_set_type : str) -> FamilyEnum:
    return {
        'ACL_IPV4' : FamilyEnum.IPV4,
        'ACL_IPV6' : FamilyEnum.IPV6,
    }[acl_set_type]


class AclRuleToInterfaceDirection:
    def __init__(self, nft : NFTables):
        self._nft = nft
        self._acl_rule_to_iface_direction : TYPE_ACL_RULE_TO_IF_DIR = dict()

    def create_nft_chains_in_table(self, acl_set_type : str, chain_names : List[str]) -> None:
        family = get_family_from_acl_set_type(acl_set_type)
        table = self._nft.get_or_create_table(family, TableEnum.FILTER)
        for chain_name in chain_names:
            table.get_or_create_chain(chain_name)

    def add_acl_set(self, if_name : str, acl_set : Dict, direction : DirectionEnum) -> None:
        acl_set_name = acl_set['config']['set-name']
        acl_set_type = acl_set['config']['type']

        if direction == DirectionEnum.INGRESS:
            self.create_nft_chains_in_table(acl_set_type, CHAINS_INPUT)
        elif direction == DirectionEnum.EGRESS:
            self.create_nft_chains_in_table(acl_set_type, CHAINS_OUTPUT)
        else:
            self.create_nft_chains_in_table(acl_set_type, CHAINS_ALL)

        for acl_set_entry in acl_set['acl-entries']['acl-entry']:
            sequence_id = int(acl_set_entry['sequence-id'])
            key = (acl_set_name, sequence_id)
            if_dir_list = self._acl_rule_to_iface_direction.setdefault(key, list())
            if_dir_list.append((if_name, direction))

    def add_interface(self, interface : Dict) -> None:
        if_name = interface['config']['id']
        for direction in [DirectionEnum.INGRESS, DirectionEnum.EGRESS]:
            direction_value = direction.value
            acl_sets_obj = interface.get(f'{direction_value}-acl-sets', dict())
            acl_sets_lst = acl_sets_obj.get(f'{direction_value}-acl-set', list())
            for acl_set in acl_sets_lst:
                self.add_acl_set(if_name, acl_set, DirectionEnum.INGRESS)

    def add_interfaces(self, interfaces : List[Dict]) -> None:
        for interface in interfaces:
            self.add_interface(interface)

    def get_interfaces_directions(
        self, acl_set_name : str, sequence_id : int
    ) -> TYPE_IFACE_DIRECTIONS:
        return self._acl_rule_to_iface_direction.get((acl_set_name, sequence_id), [])
