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


from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from .Chain import Chain
from .DirectionEnum import DirectionEnum
from .FamilyEnum import FamilyEnum
from .TableEnum import TableEnum


@dataclass
class Table:
    family : FamilyEnum
    table  : TableEnum
    handle : Optional[int] = None
    chains : Dict[str, Chain] = field(default_factory=dict)

    def get_chain(self, name : str) -> Chain:
        return self.chains[name]

    def get_or_create_chain(self, name : str) -> Chain:
        return self.chains.setdefault(name, Chain.from_manual(self.family, self.table, name))

    def add_chain_by_entry(self, entry : Dict) -> Chain:
        name : str = entry['name']
        if name.lower() not in {'input', 'output', 'forward', 'prerouting'}: return None
        if name in self.chains: return self.chains[name]
        chain = Chain.from_nft_entry(self.family, self.table, entry)
        self.chains[name] = chain
        return chain

    def add_rule_by_entry(self, entry : Dict) -> None:
        chain : str = entry.pop('chain')
        if chain.lower() not in {'input', 'output', 'forward', 'prerouting'}: return
        self.get_chain(chain).add_rule(entry)

    def to_openconfig(self) -> Tuple[List[Dict], Dict]:
        acl_sets : List[Dict] = list()
        interfaces : Dict[str, Dict[DirectionEnum, Dict[str, Set[int]]]] = dict()

        for chain in self.chains.values():
            chain_acl_set, chain_interfaces = chain.to_openconfig()
            if chain_acl_set is None: continue

            acl_sets.append(chain_acl_set)

            acl_set_name = chain_acl_set['name']
            for if_name, direction_sequence_ids in chain_interfaces.items():
                interface : Dict = interfaces.setdefault(if_name, dict())
                for direction, sequence_ids in direction_sequence_ids.items():
                    if_direction : Dict = interface.setdefault(direction, dict())
                    if_dir_aclname : Set[int] = if_direction.setdefault(acl_set_name, set())
                    if_dir_aclname.update(sequence_ids)

        return acl_sets, interfaces

    def dump(self) -> List[Dict]:
        table = {'family': self.family.value, 'name': self.table.value}
        if self.handle is not None: table['handle'] = self.handle

        entries : List[str] = list()
        entries.append({'table': table})
        for chain in self.chains.values(): entries.extend(chain.dump())
        return entries

    def get_commands(self, removal : bool = False) -> List[Tuple[int, str]]:
        commands : List[Tuple[int, str]] = list()

        if removal:
            # NOTE: For now, do not remove tables. We do not process all kinds of
            # tables and their removal might cause side effects on NFTables.
            pass
        elif self.handle is not None:
            # NOTE: Table was already there, do not modify it
            pass
        else:
            parts = ['add', 'table', self.family.value, self.table.value]
            commands.append((-2, ' '.join(parts)))

        for chain in self.chains.values():
            commands.extend(chain.get_commands(removal=removal))

        return commands
