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
from typing import List
from ..gnmi.gnmi_pb2 import Path, PathElem

RE_PATH_SPLIT = re.compile(r'/(?=(?:[^\[\]]|\[[^\[\]]+\])*$)')
RE_PATH_KEYS = re.compile(r'\[(.*?)\]')

def path_from_string(path='/'):
    if not path: return Path(elem=[])

    if path[0] == '/':
        if path[-1] == '/':
            path_list = RE_PATH_SPLIT.split(path)[1:-1]
        else:
            path_list = RE_PATH_SPLIT.split(path)[1:]
    else:
        if path[-1] == '/':
            path_list = RE_PATH_SPLIT.split(path)[:-1]
        else:
            path_list = RE_PATH_SPLIT.split(path)

    path = []
    for elem in path_list:
        elem_name = elem.split('[', 1)[0]
        elem_keys = RE_PATH_KEYS.findall(elem)
        dict_keys = dict(x.split('=', 1) for x in elem_keys)
        path.append(PathElem(name=elem_name, key=dict_keys))

    return Path(elem=path)

def path_to_string(path : Path) -> str:
    path_parts = list()
    for elem in path.elem:
        kv_list = list()
        for key in elem.key:
            value = elem.key[key]
            kv = '{:s}={:s}'.format(key, value)
            kv_list.append(kv)

        path_part_name = elem.name
        if len(kv_list) == 0:
            path_parts.append(path_part_name)
        else:
            str_kv = ', '.join(kv_list)
            path_part = '{:s}[{:s}]'.format(path_part_name, str_kv)
            path_parts.append(path_part)

    str_path = '/{:s}'.format('/'.join(path_parts))
    return str_path

def parse_xpath(xpath : str) -> str:
    xpath = xpath.replace('//', '/')
    xpath = xpath.replace('oci:interface[', 'interface[')
    xpath = xpath.replace('/oci', '/openconfig-interfaces')
    xpath = re.sub(r"\[oci:name='(.*?)'\]", r"[name=\1]", xpath)
    # Eliminar el contador del final
    xpath = '/'.join(xpath.split('/')[:-1]) + '/'
    return xpath

def split_resource_key(path):
    pattern = r'/state/counters/(.*)'
    match = re.search(pattern, path)
    if match is None: return None
    return match.group(1)

def dict_to_xpath(d: dict) -> str:
    xpath = '/'
    for item in d['elem']:
        name = item.get('name')
        if name == 'interface':
            key = item.get('key')
            interface_name = key.get('name')
            xpath += f"/oci:interface[oci:name='{interface_name}']"
        else:
            xpath += f"/{name}"
    xpath = xpath.replace('openconfig-interfaces', 'oci')
    return xpath

def compose_path(base_path : str, path_filters : List[str] = []):
    new_path = '' if base_path is None else str(base_path)
    for path_filter in path_filters:
        if path_filter == '': continue
        new_path = '{:s}[{:s}]'.format(new_path, path_filter)
    return new_path
