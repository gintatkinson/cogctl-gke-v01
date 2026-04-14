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


from typing import Dict, Optional
from .FamilyEnum import FamilyEnum
from .TableEnum import TableEnum


class InvalidArgumentException(Exception):
    def __init__(
        self, family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None,
        chain : Optional[str] = None
    ) -> None:
        super().__init__(
            f'Invalid combination of parameters: '
            f'family={str(family)} table={str(table)} chain={str(chain)}'
        )

class RuntimeException(Exception):
    def __init__(self, rc : int, output : str, error : str) -> None:
        super().__init__(
            f'nft command failed: '
            f'rc={str(rc)} output={str(output)} error={str(error)}'
        )

class MalformedOutputException(Exception):
    def __init__(self, reason : str, command : str, output : str) -> None:
        super().__init__(
            f'nft command malformed output: '
            f'reason={str(reason)} command={str(command)} output={str(output)}'
        )

class UnsupportedElementException(Exception):
    def __init__(
        self, element : str, value : str, extra : Optional[str] = None
    ) -> None:
        msg = f'Unsupported: element={str(element)} value={str(value)}'
        if extra is not None: msg += f' {str(extra)}'
        super().__init__(msg)

class MissingFieldException(Exception):
    def __init__(self, field_name : str, objekt : Dict) -> None:
        super().__init__(
            f'Missing Field: name={str(field_name)} object={str(objekt)}'
        )

class AlreadyExistsTableException(Exception):
    def __init__(
        self, family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None
    ) -> None:
        super().__init__(
            f'Already Exists Table: family={str(family)} table={str(table)}'
        )

class MissingTableException(Exception):
    def __init__(
        self, family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None
    ) -> None:
        super().__init__(
            f'Missing Table: family={str(family)} table={str(table)}'
        )

class AlreadyExistsChainException(Exception):
    def __init__(
        self, family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None,
        chain : Optional[str] = None
    ) -> None:
        super().__init__(
            f'Already Exists Chain: family={str(family)} table={str(table)} chain={str(chain)}'
        )

class MissingChainException(Exception):
    def __init__(
        self, family : Optional[FamilyEnum] = None, table : Optional[TableEnum] = None,
        chain : Optional[str] = None
    ) -> None:
        super().__init__(
            f'Missing Chain: family={str(family)} table={str(table)} chain={str(chain)}'
        )
