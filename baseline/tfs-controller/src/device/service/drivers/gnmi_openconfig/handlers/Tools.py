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
from typing import Any, Callable, Dict, Iterable, Optional

RE_REMOVE_FILTERS = re.compile(r'\[[^\]]+\]')
RE_REMOVE_NAMESPACES = re.compile(r'\/[a-zA-Z0-9\_\-]+:')

def get_schema(resource_key : str):
    resource_key = RE_REMOVE_FILTERS.sub('', resource_key)
    resource_key = RE_REMOVE_NAMESPACES.sub('/', resource_key)
    return resource_key

def container_get_first(
    container : Dict[str, Any], key_name : str, namespace : Optional[str]=None, namespaces : Iterable[str]=tuple(),
    default : Optional[Any] = None
) -> Any:
    value = container.get(key_name)
    if value is not None: return value

    if namespace is not None:
        if len(namespaces) > 0:
            raise Exception('At maximum, one of namespace or namespaces can be specified')
        namespaces = (namespace,)

    for namespace in namespaces:
        namespace_key_name = '{:s}:{:s}'.format(namespace, key_name)
        if namespace_key_name in container: return container[namespace_key_name]

    return default

def get_value(
    resource_value : Dict, field_name : str, cast_func : Callable = lambda x:x, default : Optional[Any] = None
) -> Optional[Any]:
    field_value = resource_value.get(field_name, default)
    if field_value is not None: field_value = cast_func(field_value)
    return field_value

def get_bool(resource_value : Dict, field_name : bool, default : Optional[Any] = None) -> bool:
    return get_value(resource_value, field_name, cast_func=bool, default=default)

def get_float(resource_value : Dict, field_name : float, default : Optional[Any] = None) -> float:
    return get_value(resource_value, field_name, cast_func=float, default=default)

def get_int(resource_value : Dict, field_name : int, default : Optional[Any] = None) -> int:
    return get_value(resource_value, field_name, cast_func=int, default=default)

def get_str(resource_value : Dict, field_name : str, default : Optional[Any] = None) -> str:
    return get_value(resource_value, field_name, cast_func=str, default=default)
