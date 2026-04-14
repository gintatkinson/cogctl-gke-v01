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

import re
from typing import Any, Dict, Iterable

RE_REMOVE_FILTERS = re.compile(r'\[[^\]]+\]')
RE_REMOVE_NAMESPACES = re.compile(r'\/[a-zA-Z0-9\_\-]+:')

def get_schema(resource_key : str):
    resource_key = RE_REMOVE_FILTERS.sub('', resource_key)
    resource_key = RE_REMOVE_NAMESPACES.sub('/', resource_key)
    return resource_key

def dict_get_first(d : Dict, field_names : Iterable[str], default=None) -> Any:
    for field_name in field_names:
        if field_name not in d: continue
        return d[field_name]
    return default
