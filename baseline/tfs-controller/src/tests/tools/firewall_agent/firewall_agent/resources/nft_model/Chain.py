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


import enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from .ActionEnum import ActionEnum
from .DirectionEnum import DirectionEnum
from .FamilyEnum import FamilyEnum
from .TableEnum import TableEnum
from .Rule import Rule


class ChainPriorityEnum(enum.IntEnum):
    RAW    = -300
    MANGLE = -150
    FILTER = 0

@dataclass
class Chain:
    family : FamilyEnum
    table  : TableEnum
    chain  : str
    handle : Optional[int       ] = None
    type   : Optional[str       ] = None
    hook   : Optional[str       ] = None
    prio   : Optional[int       ] = None
    policy : Optional[ActionEnum] = None
    rules  : List[Rule] = field(default_factory=list)

    @classmethod
    def from_manual(
        cls, family : FamilyEnum, table : TableEnum, name : str,
        handle : Optional[int] = None, type_ : Optional[str] = None,
        hook : Optional[str] = None, prio : int = ChainPriorityEnum.RAW.value,
        policy : ActionEnum = ActionEnum.ACCEPT
    ) -> 'Chain':
        chain : 'Chain' = cls(family, table, name)
        chain.handle = handle
        if type_ is None: chain.type = str(table.value).lower()
        if hook is None: chain.hook = str(name).lower()
        chain.prio = prio
        chain.policy = policy.value
        return chain

    @classmethod
    def from_nft_entry(
        cls, family : FamilyEnum, table : TableEnum, entry : Dict
    ) -> 'Chain':
        name : str = entry['name']
        chain : 'Chain' = cls(family, table, name)
        chain.handle = entry['handle']
        chain.type   = entry.get('type',   table.value.lower())
        chain.hook   = entry.get('hook',   name.lower())
        chain.prio   = entry.get('prio',   ChainPriorityEnum.FILTER.value)
        chain.policy = entry.get('policy', ActionEnum.ACCEPT.value)
        return chain

    def add_rule(self, entry : Dict) -> None:
        rule = Rule.from_nft_entry(self.family, self.table, self.chain, entry)
        if rule is None: return
        self.rules.append(rule)

    def to_openconfig(self) -> Tuple[Optional[Dict], Dict]:
        acl_set_name = f'{self.family.value}-{self.table.value}-{self.chain}'
        acl_set_type = {
            FamilyEnum.IPV4 : 'ACL_IPV4',
            FamilyEnum.IPV6 : 'ACL_IPV6',
        }.get(self.family)

        acl_set_entries : List[Dict] = list()
        interfaces : Dict[str, Dict[DirectionEnum, Set[int]]] = dict()

        for sequence_id, rule in enumerate(self.rules, start=1):
            acl_entry, rule_interfaces = rule.to_openconfig(sequence_id)
            acl_set_entries.append(acl_entry)

            for if_name, direction_sequence_ids in rule_interfaces.items():
                interface : Dict = interfaces.setdefault(if_name, dict())
                for direction, sequence_ids in direction_sequence_ids.items():
                    if_dir_sequence_ids : Set = interface.setdefault(direction, set())
                    if_dir_sequence_ids.update(sequence_ids)


        if len(acl_set_entries) > 0:
            acl_set = {
                'name': acl_set_name,
                'type': acl_set_type,
                'config': {'name': acl_set_name, 'type': acl_set_type},
                'state': {'name': acl_set_name, 'type': acl_set_type},
                'acl-entries': {'acl-entry': acl_set_entries}
            }
        else:
            acl_set = None
        return acl_set, interfaces

    def dump(self) -> List[Dict]:
        chain = {'family': self.family.value, 'table': self.table.value, 'name': self.chain}
        if self.handle is not None: chain['handle'] = self.handle

        entries : List[str] = list()
        entries.append({'chain': chain})
        for rule in self.rules: entries.extend(rule.dump())
        return entries

    def get_commands(self, removal : bool = False) -> List[Tuple[int, str]]:
        commands : List[Tuple[int, str]] = list()

        if removal:
            # NOTE: For now, do not remove chains. We do not process all kinds of
            # chains and their removal might cause side effects on NFTables.
            pass
        elif self.handle is not None:
            # NOTE: Chain was already there, do not modify it
            pass
        else:
            parts = [
                'add', 'chain', self.family.value, self.table.value, self.chain,
                '{',
                'type', self.type, 'hook', self.hook, 'priority', str(self.prio), ';',
                'policy', self.policy, ';',
                '}'
            ]
            commands.append((-1, ' '.join(parts)))

        for rule in self.rules:
            rule_cmd = rule.get_command(removal=removal)
            if rule_cmd is None: continue
            commands.append(rule_cmd)

        return commands
