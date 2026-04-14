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

from typing import Optional, Union
from uuid import UUID, uuid4, uuid5

# Generate a UUIDv5-like from the SHA-1 of "TFS" and no namespace to be used as the NAMESPACE for all
# the context UUIDs generated. For efficiency purposes, the UUID is hardcoded; however, it is produced
# using the following code:
#    from hashlib import sha1
#    from uuid import UUID
#    hash = sha1(bytes('TFS', 'utf-8')).digest()
#    NAMESPACE_TFS = UUID(bytes=hash[:16], version=5)
NAMESPACE_TFS = UUID('200e3a1f-2223-534f-a100-758e29c37f40')

def get_uuid_from_string(str_uuid_or_name : Union[str, UUID], prefix_for_name : Optional[str] = None) -> str:
    # if UUID given, assume it is already a valid UUID
    if isinstance(str_uuid_or_name, UUID): return str_uuid_or_name
    if not isinstance(str_uuid_or_name, str):
        MSG = 'Parameter({:s}) cannot be used to produce a UUID'
        raise Exception(MSG.format(str(repr(str_uuid_or_name))))
    try:
        # try to parse as UUID
        return str(UUID(str_uuid_or_name))
    except: # pylint: disable=bare-except
        # produce a UUID within TFS namespace from parameter
        if prefix_for_name is not None:
            str_uuid_or_name = '{:s}/{:s}'.format(prefix_for_name, str_uuid_or_name)
        return str(uuid5(NAMESPACE_TFS, str_uuid_or_name))

def get_uuid_random() -> str:
    # Generate random UUID. No need to use namespace since "namespace + random = random".
    return str(uuid4())
