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
from dataclasses import dataclass, field
import operator
from typing import Dict, List, Optional, Set, Tuple
from .DirectionEnum import DirectionEnum
from .Exceptions import UnsupportedElementException
from .FamilyEnum import FamilyEnum, get_family_from_str
from .NFTablesCommand import NFTablesCommand
from .Rule import Rule
from .Table import Table
from .TableEnum import TableEnum, get_table_from_str


LOGGER = logging.getLogger(__name__)


@dataclass
class NFTables:
    tables : Dict[Tuple[FamilyEnum, TableEnum], Table] = field(default_factory=dict)

    def load(
        self, family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None,
        chain : Optional[str] = None, skip_rules : bool = False
    ) -> None:
        entries = NFTablesCommand.list(family=family, table=table, chain=chain)
        for entry in entries: self.parse_entry(entry, skip_rules=skip_rules)

    def get_or_create_table(self, family : FamilyEnum, table : TableEnum) -> Table:
        return self.tables.setdefault((family, table), Table(family, table))

    def parse_entry(self, entry : Dict, skip_rules : bool = False) -> None:
        entry_fields = set(entry.keys())
        if len(entry_fields) != 1: raise UnsupportedElementException('entry', entry)
        entry_type = entry_fields.pop()
        if entry_type in {'metainfo'}:
            return # skipping unneeded entry
        elif entry_type in {'table'}:
            self.parse_entry_table(entry['table'])
        elif entry_type in {'chain'}:
            self.parse_entry_chain(entry['chain'])
        elif entry_type in {'rule'}:
            if skip_rules: return
            self.parse_entry_rule(entry['rule'])
        else:
            raise UnsupportedElementException('entry', entry)

    def parse_entry_table(self, entry : Dict) -> None:
        family = get_family_from_str(entry['family'])
        if family not in {FamilyEnum.IPV4, FamilyEnum.IPV6}: return
        table = get_table_from_str(entry['name'])
        if table not in {TableEnum.FILTER}: return
        table_obj = self.get_or_create_table(family, table)
        table_obj.handle = entry['handle']

    def parse_entry_chain(self, entry : Dict) -> None:
        family = get_family_from_str(entry.pop('family'))
        if family not in {FamilyEnum.IPV4, FamilyEnum.IPV6}: return
        table = get_table_from_str(entry.pop('table'))
        if table not in {TableEnum.FILTER}: return
        self.get_or_create_table(family, table).add_chain_by_entry(entry)

    def parse_entry_rule(self, entry : Dict) -> None:
        family = get_family_from_str(entry.pop('family'))
        if family not in {FamilyEnum.IPV4, FamilyEnum.IPV6}: return
        table = get_table_from_str(entry.pop('table'))
        if table not in {TableEnum.FILTER}: return
        self.get_or_create_table(family, table).add_rule_by_entry(entry)

    def add_rule(self, rule : Rule) -> None:
        table = self.get_or_create_table(rule.family, rule.table)
        chain = table.get_or_create_chain(rule.chain)
        chain.rules.append(rule)

    def to_openconfig(self) -> List[Dict]:
        acl_sets : List[Dict] = list()
        interfaces_struct : Dict[str, Dict[DirectionEnum, Dict[str, Set[int]]]] = dict()
        acl_set_name_to_type : Dict[str, str] = dict()

        for table in self.tables.values():
            table_acl_sets, table_interfaces = table.to_openconfig()
            acl_sets.extend(table_acl_sets)

            for table_acl_set in table_acl_sets:
                acl_set_name = table_acl_set['name']
                acl_set_type = table_acl_set['type']
                acl_set_name_to_type[acl_set_name] = acl_set_type

            for if_name, dir_aclname_seqids in table_interfaces.items():
                interface : Dict = interfaces_struct.setdefault(if_name, dict())
                for direction, aclname_seqids in dir_aclname_seqids.items():
                    if_direction : Dict = interface.setdefault(direction, dict())
                    for acl_name, sequence_ids in aclname_seqids.items():
                        if_dir_aclname : Set[int] = if_direction.setdefault(acl_name, set())
                        if_dir_aclname.update(sequence_ids)

        interfaces = list()
        for if_name, dir_aclname_seqids in interfaces_struct.items():
            if_data = {
                'id': if_name,
                'config': {'id': if_name},
                'state': {'id': if_name},
                'interface-ref': {
                    'config': {'interface': if_name, 'subinterface': 1},
                    'state': {'interface': if_name, 'subinterface': 1},
                }
            }

            for direction, aclname_seqids in dir_aclname_seqids.items():
                if_dir_obj : Dict = if_data.setdefault(f'{direction.value}-acl-sets', dict())
                if_dir_list : List = if_dir_obj.setdefault(f'{direction.value}-acl-set', list())

                for acl_set_name, sequence_ids in aclname_seqids.items():
                    acl_set_type = acl_set_name_to_type[acl_set_name]
                    if_dir_acl_set = {
                        'set-name': acl_set_name,
                        'type': acl_set_type,
                        'config': {'set-name': acl_set_name, 'type': acl_set_type},
                        'state': {'set-name': acl_set_name, 'type': acl_set_type},
                    }
                    if_dir_acl_set['acl-entries'] = {'acl-entry': [
                        {'sequence-id': sequence_id, 'state': {'sequence-id': sequence_id}}
                        for sequence_id in sequence_ids
                    ]}
                    if_dir_list.append(if_dir_acl_set)

            interfaces.append(if_data)

        acl_data = dict()
        if len(acl_sets) > 0: acl_data.update({'acl-sets': {'acl-set': acl_sets}})
        if len(interfaces) > 0: acl_data.update({'interfaces': {'interface': interfaces}})
        return {'openconfig-acl:acl': acl_data}

    def dump(self) -> List[Dict]:
        entries : List[Dict] = list()
        for table in self.tables.values(): entries.extend(table.dump())
        return entries

    def get_commands(self, removal : bool = False) -> List[Tuple[int, str]]:
        commands : List[Tuple[int, str]] = list()
        for table in self.tables.values():
            commands.extend(table.get_commands(removal=removal))
        # return a sorted list of commands by their priority (lower first)
        return sorted(commands, key=operator.itemgetter(0))

    def execute(self, removal : bool = False, verbose : bool = True) -> None:
        commands = self.get_commands(removal=removal)
        NFTablesCommand.execute(commands, verbose=verbose)
