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

# Hardcoded namespace for generating UUIDs.
NAMESPACE_TFS = UUID('200e3a1f-2223-534f-a100-758e29c37f40')

def get_uuid_from_string(str_uuid_or_name: Union[str, UUID], prefix_for_name: Optional[str] = None) -> str:
    """
    Convert a string or UUID object into a UUID string. If input is a name, generate a UUID using the TFS namespace.
    
    :param str_uuid_or_name: Input string or UUID to be converted into UUID format
    :param prefix_for_name: Optional prefix to add before the name when generating a name-based UUID
    :return: A valid UUID string
    :raises ValueError: If the input is invalid and cannot be converted to a UUID
    """
    if isinstance(str_uuid_or_name, UUID):
        return str(str_uuid_or_name)  # Ensure returning a string representation

    if not isinstance(str_uuid_or_name, str):
        raise ValueError(f"Invalid parameter ({repr(str_uuid_or_name)}). Expected a string or UUID to produce a valid UUID.")

    try:
        # Try to interpret the input as a UUID
        return str(UUID(str_uuid_or_name))
    except ValueError:
        # If the input isn't a valid UUID, generate one using the name-based approach
        if prefix_for_name:
            str_uuid_or_name = f"{prefix_for_name}/{str_uuid_or_name}"
        return str(uuid5(NAMESPACE_TFS, str_uuid_or_name))

def get_uuid_random() -> str:
    """
    Generate and return a new random UUID as a string.
    
    :return: A randomly generated UUID string
    """
    return str(uuid4())
