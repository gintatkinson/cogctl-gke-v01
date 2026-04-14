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


import json, libyang, logging
import urllib.parse
from typing import Dict, List, Optional, Set


LOGGER = logging.getLogger(__name__)


def walk_schema(node : libyang.SNode, path : str = '') -> Set[str]:
    current_path = f'{path}/{node.name()}'
    schema_paths : Set[str] = {current_path}
    for child in node.children():
        if isinstance(child, (libyang.SLeaf, libyang.SLeafList)): continue
        schema_paths.update(walk_schema(child, current_path))
    return schema_paths

def extract_schema_paths(yang_module : libyang.Module) -> Set[str]:
    schema_paths : Set[str] = set()
    for node in yang_module.children():
        schema_paths.update(walk_schema(node))
    return schema_paths

class YangHandler:
    def __init__(
        self, yang_search_path : str, yang_module_names : List[str],
        yang_startup_data : Dict
    ) -> None:
        self._yang_context = libyang.Context(yang_search_path)
        self._loaded_modules : Set[str] = set()
        self._schema_paths : Set[str] = set()
        for yang_module_name in yang_module_names:
            LOGGER.info('Loading module: {:s}'.format(str(yang_module_name)))
            yang_module = self._yang_context.load_module(yang_module_name)
            yang_module.feature_enable_all()
            self._loaded_modules.add(yang_module_name)
            self._schema_paths.update(extract_schema_paths(yang_module))

        self._datastore = self._yang_context.parse_data_mem(
            json.dumps(yang_startup_data), fmt='json'
        )

    @property
    def yang_context(self): return self._yang_context

    @property
    def yang_datastore(self): return self._datastore

    def destroy(self) -> None:
        self._yang_context.destroy()

    def get_schema_paths(self) -> Set[str]:
        return self._schema_paths

    def get(self, path : str) -> Optional[str]:
        path = self._normalize_path(path)
        data = self._datastore.find_path(path)
        if data is None: return None
        json_data = data.print_mem(
            fmt='json', with_siblings=False, pretty=True,
            keep_empty_containers=False, include_implicit_defaults=True
        )
        return json_data

    def get_xpath(self, xpath : str) -> List[str]:
        if not xpath.startswith('/'): xpath = '/' + xpath
        items = self._datastore.find_all(xpath)
        result = list()
        for item in items:
            result.append(item.print_mem(
                fmt='json', with_siblings=False, pretty=True,
                keep_empty_containers=False, include_implicit_defaults=True
            ))
        return result

    def create(self, path : str, payload : Dict) -> str:
        path = self._normalize_path(path)
        # TODO: client should not provide identifier of element to be created, add it to subpath
        dnode_parsed : Optional[libyang.DNode] = self._yang_context.parse_data_mem(
            json.dumps(payload), 'json', strict=True, parse_only=False,
            validate_present=True, validate_multi_error=True
        )
        if dnode_parsed is None: raise Exception('Unable to parse Data({:s})'.format(str(payload)))

        dnode : Optional[libyang.DNode] = self._yang_context.create_data_path(
            path, parent=self._datastore, value=dnode_parsed, update=False
        )
        self._datastore.merge(dnode_parsed, with_siblings=True, defaults=True)

        json_data = dnode.print_mem(
            fmt='json', with_siblings=True, pretty=True,
            keep_empty_containers=True, include_implicit_defaults=True
        )
        return json_data

    def update(self, path : str, payload : Dict) -> str:
        path = self._normalize_path(path)
        # NOTE: client should provide identifier of element to be updated
        dnode_parsed : Optional[libyang.DNode] = self._yang_context.parse_data_mem(
            json.dumps(payload), 'json', strict=True, parse_only=False,
            validate_present=True, validate_multi_error=True
        )
        if dnode_parsed is None: raise Exception('Unable to parse Data({:s})'.format(str(payload)))

        dnode = self._yang_context.create_data_path(
            path, parent=self._datastore, value=dnode_parsed, update=True
        )
        self._datastore.merge(dnode_parsed, with_siblings=True, defaults=True)

        json_data = dnode.print_mem(
            fmt='json', with_siblings=True, pretty=True,
            keep_empty_containers=True, include_implicit_defaults=True
        )
        return json_data

    def delete(self, path : str) -> Optional[str]:
        path = self._normalize_path(path)

        # NOTE: client should provide identifier of element to be deleted

        node : libyang.DNode = self._datastore.find_path(path)
        if node is None: return None

        LOGGER.info('node = {:s}'.format(str(node)))
        json_data = str(node.print_mem(
            fmt='json', with_siblings=True, pretty=True,
            keep_empty_containers=True, include_implicit_defaults=True
        ))
        LOGGER.info('json_data = {:s}'.format(json_data))

        node.unlink()
        node.free()

        return json_data

    def _normalize_path(self, path : str) -> str:
        """
        Normalize RESTCONF path segments using the standard `list=<keys>`
        syntax into the libyang bracketed predicate form expected by
        the datastore (e.g. `network="admin"` -> `network[network-id="admin"]`).

        This implementation looks up the schema node for the list and
        uses its key leaf names to build the proper predicates. If the
        schema information is unavailable, it falls back to using the
        list name as the key name.
        """

        # URL-decode each path segment so escaped characters like `%22`
        # (double quotes) are properly handled when parsing list keys.
        parts = [urllib.parse.unquote(p) for p in path.strip('/').split('/') if p != '']
        schema_path = ''
        out_parts: List[str] = []

        for part in parts:
            if '=' in part:
                # split into name and value (value may contain commas/quotes)
                name, val = part.split('=', 1)
                # keep original name (may include prefix) for output, but
                # use local name (without module prefix) to lookup schema
                local_name = name #.split(':', 1)[1] if ':' in name else name
                schema_path = schema_path + '/' + local_name if schema_path else '/' + local_name
                schema_nodes = list(self._yang_context.find_path(schema_path))
                if len(schema_nodes) != 1:
                    MSG = 'No/Multiple SchemaNodes({:s}) for SchemaPath({:s})'
                    raise Exception(MSG.format(
                        #str([repr(sn) for sn in schema_nodes]), schema_path
                        str([
                            '{:s}({:s}) => {:s}'.format(
                                repr(sn),
                                str(sn.schema_path()),
                                str([repr(snn) for snn in sn.iter_tree()])
                            )
                            for sn in schema_nodes]), schema_path
                    ))
                schema_node = schema_nodes[0]

                # parse values splitting on commas outside quotes
                values = []
                cur = ''
                in_quotes = False
                for ch in val:
                    if ch == '"':
                        in_quotes = not in_quotes
                        cur += ch
                    elif ch == ',' and not in_quotes:
                        values.append(cur)
                        cur = ''
                    else:
                        cur += ch
                if cur != '':
                    values.append(cur)

                # determine key names from schema_node if possible
                key_names = None
                if isinstance(schema_node, libyang.SList):
                    key_names = [k.name() for k in schema_node.keys()]
                    #if isinstance(keys, (list, tuple)):
                    #    key_names = keys
                    #elif isinstance(keys, str):
                    #    key_names = [kn for kn in k.split() if kn]
                #else:
                #    MSG = 'Unsupported keys format: {:s} / {:s}'
                #    raise Exception(MSG.format(str(type(keys)), str(keys)))
                #elif hasattr(schema_node, 'key'):
                #    k = schema_node.key()
                #    if isinstance(k, str):
                #        key_names = [kn for kn in k.split() if kn]

                if not key_names:
                    # fallback: use the local list name as the single key
                    key_names = [local_name]

                # build predicate(s)
                preds = []
                for idx, kn in enumerate(key_names):
                    kv = values[idx] if idx < len(values) else values[0]
                    preds.append(f'[{kn}="{kv}"]')

                out_parts.append(name + ''.join(preds))
            else:
                local_part = part #.split(':', 1)[1] if ':' in part else part
                schema_path = schema_path + '/' + local_part if schema_path else '/' + local_part
                out_parts.append(part)

        return '/' + '/'.join(out_parts)
