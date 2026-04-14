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


import json, logging, nftables
from typing import Dict, List, Optional, Tuple
from .Exceptions import (
    InvalidArgumentException, MalformedOutputException, RuntimeException
)
from .FamilyEnum import FamilyEnum
from .TableEnum import TableEnum


LOGGER = logging.getLogger(__name__)


class NFTablesCommand:
    @staticmethod
    def get_command_list(
        family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None,
        chain : Optional[str] = None
    ) -> str:
        if chain is None:
            if table is None:
                if family is None:
                    return 'list ruleset'
                else:
                    return f'list ruleset {family.value}'
            else:
                if family is not None:
                    return f'list table {family.value} {table.value}'
        else:
            if table is not None:
                if family is not None:
                    return f'list chain {family.value} {table.value} {chain}'

        raise InvalidArgumentException(family, table, chain)

    @staticmethod
    def list(
        family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None,
        chain : Optional[str] = None
    ) -> List[Dict]:
        nft = nftables.Nftables()
        nft.set_json_output(True)
        str_cmd = NFTablesCommand.get_command_list(
            family=family, table=table, chain=chain
        )
        rc, output, error = nft.cmd(str_cmd)
        if rc != 0: raise RuntimeException(rc, output, error)
        json_nftables = json.loads(output)
        if 'nftables' not in json_nftables:
            raise MalformedOutputException(
                'Missing field "nftables"', str_cmd, output
            )
        return json_nftables['nftables']

    @staticmethod
    def execute(commands : List[Tuple[int, str]], verbose : bool = True) -> None:
        nft = nftables.Nftables()
        nft.set_json_output(True)
        for priority, command in commands:
            if verbose:
                LOGGER.info(f'Executing [priority={str(priority)}]: {command}')
            rc, output, error = nft.cmd(command)
            if verbose:
                LOGGER.info(f'rc={str(rc)} output={str(output)} error={str(error)}')
            if rc != 0: raise RuntimeException(rc, output, error)
