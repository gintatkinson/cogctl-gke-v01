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


import logging, re
from collections import defaultdict
from graphlib import TopologicalSorter, CycleError
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


COMMENT_SINGLE_RE = re.compile(r"//.*?$", re.MULTILINE)
COMMENT_MULTI_RE = re.compile(r"/\*.*?\*/", re.DOTALL)

# module / submodule name
MODNAME_RE = re.compile(r"\b(module|submodule)\s+([A-Za-z0-9_.-]+)\s*\{")

# import foo { ... }  (most common form)
IMPORT_BLOCK_RE = re.compile(r"\bimport\s+([A-Za-z0-9_.-]+)\s*\{", re.IGNORECASE)

# import foo;  (very rare, but we’ll support it)
IMPORT_SEMI_RE  = re.compile(r"\bimport\s+([A-Za-z0-9_.-]+)\s*;", re.IGNORECASE)

# include foo { ... }  (most common form)
INCLUDE_BLOCK_RE = re.compile(r"\binclude\s+([A-Za-z0-9_.-]+)\s*\{", re.IGNORECASE)

# include foo;  (very rare, but we’ll support it)
INCLUDE_SEMI_RE  = re.compile(r"\binclude\s+([A-Za-z0-9_.-]+)\s*;", re.IGNORECASE)


def _parse_yang_file(path: Path) -> Tuple[Optional[str], Set[str], Set[str]]:
    path_stem = path.stem # file name without extension
    expected_module_name = path_stem.split('@', 1)[0]

    try:
        data = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        data = path.read_bytes().decode('utf-8', errors='ignore')

    data = COMMENT_MULTI_RE.sub('', data)
    data = COMMENT_SINGLE_RE.sub('', data)

    match = MODNAME_RE.search(data)
    if match is None:
        return None, set()
    module_name = match.group(2)
    if module_name != expected_module_name:
        MSG = 'Module({:s}) mismatches its FileName({:s})'
        raise Exception(MSG.format(str(module_name), str(expected_module_name)))

    module_imports = set()
    module_includes = set()
    if module_name is not None:
        module_imports.update(IMPORT_BLOCK_RE.findall(data))
        module_imports.update(IMPORT_SEMI_RE.findall(data))
        module_includes.update(INCLUDE_BLOCK_RE.findall(data))
        module_includes.update(INCLUDE_SEMI_RE.findall(data))

    # ignore modules importing themselves, just in case
    module_imports.discard(module_name)

    # ignore modules including themselves, just in case
    module_includes.discard(module_name)

    return module_name, module_imports, module_includes


class YangModuleDiscoverer:
    def __init__(self, yang_search_path : str) -> None:
        self._yang_search_path = yang_search_path

        self._module_to_paths : Dict[str, List[Path]] = defaultdict(list)
        self._module_to_imports : Dict[str, Set[str]] = defaultdict(set)
        self._module_to_includes : Dict[str, Set[str]] = defaultdict(set)
        self._ordered_module_names : Optional[List[str]] = None

    def run(
        self, do_print_order : bool = False, do_log_order : bool = False,
        logger : Optional[logging.Logger] = None, level : int = logging.INFO
    ) -> List[str]:
        if self._ordered_module_names is None:
            self._scan_modules()
            self._sort_modules()

        if do_print_order:
            self.print_order()

        if do_log_order:
            if logger is None: logger = logging.getLogger(__name__)
            self.log_order(logger, level=level)

        return self._ordered_module_names

    def _scan_modules(self) -> None:
        yang_root = Path(self._yang_search_path).resolve()
        if not yang_root.exists():
            MSG = 'Path({:s}) not found'
            raise Exception(MSG.format(str(self._yang_search_path)))

        for yang_path in yang_root.rglob('*.yang'):
            module_name, module_imports, module_includes = _parse_yang_file(yang_path)
            if module_name is None: continue
            self._module_to_paths.setdefault(module_name, list()).append(yang_path)
            self._module_to_imports.setdefault(module_name, set()).update(module_imports)
            self._module_to_includes.setdefault(module_name, set()).update(module_includes)

        # Propagate modules imported by included modules to modules including them:
        #   openconfig-platform includes openconfig-platform-common
        #   openconfig-platform-common imports (
        #       openconfig-platform-types, openconfig-extensions, openconfig-types
        #   )
        #   => propagate (
        #       openconfig-platform-types, openconfig-extensions, openconfig-types
        #   ) as imports of openconfig-platform
        #   => remove openconfig-platform-common from list of modules_to_imports as
        #      cannot be imported by itself
        included_modules : Set[str] = set()
        for module_name, module_includes in self._module_to_includes.items():
            for inc_mdl_name in module_includes:
                included_module_imports = self._module_to_imports.get(inc_mdl_name, set())
                self._module_to_imports.setdefault(module_name, set()).update(included_module_imports)
            included_modules.update(module_includes)
        for included_module in included_modules:
            self._module_to_imports.pop(included_module)

        if len(self._module_to_paths) == 0:
            MSG = 'No modules found in Path({:s})'
            raise Exception(MSG.format(str(self._yang_search_path)))

        self._check_duplicated_module_declaration()
        self._check_missing_modules()


    def _check_duplicated_module_declaration(self) -> None:
        duplicate_module_declarations : List[str] = list()
        for module_name, paths in self._module_to_paths.items():
            if len(paths) == 1: continue
            str_paths = [str(p) for p in paths]
            duplicate_module_declarations.append(
                '  {:s} => {:s}'.format(module_name, str_paths)
            )

        if len(duplicate_module_declarations) > 0:
            MSG = 'Duplicate module declarations:\n{:s}'
            str_dup_mods = '\n'.join(duplicate_module_declarations)
            raise Exception(MSG.format(str_dup_mods))


    def _check_missing_modules(self) -> None:
        local_module_names = set(self._module_to_imports.keys())
        missing_modules : List[str] = list()
        for module_name, module_imports in self._module_to_imports.items():
            missing = module_imports.difference(local_module_names)
            if len(missing) == 0: continue
            missing_modules.append(
                '  {:s} => {:s}'.format(module_name, str(missing))
            )

        if len(missing_modules) > 0:
            MSG = 'Missing modules:\n{:s}'
            str_mis_mods = '\n'.join(missing_modules)
            raise Exception(MSG.format(str_mis_mods))


    def _sort_modules(self) -> None:
        ts = TopologicalSorter()
        for module_name, module_imports in self._module_to_imports.items():
            ts.add(module_name, *module_imports)

        try:
            self._ordered_module_names = list(ts.static_order())   # raises CycleError on cycles
        except CycleError as e:
            cycle = list(dict.fromkeys(e.args[1]))  # de-dup while preserving order
            MSG = 'Circular dependencies between modules: {:s}'
            raise Exception(MSG.format(str(cycle))) # pylint: disable=raise-missing-from


    def dump_order(self) -> List[Tuple[int, str, List[str]]]:
        if self._ordered_module_names is None:
            raise Exception('First process the YANG Modules running method .run()')

        module_order : List[Tuple[int, str, List[str]]] = list()
        for i, module_name in enumerate(self._ordered_module_names, 1):
            module_imports = sorted(self._module_to_imports[module_name])
            module_order.append((i, module_name, module_imports))

        return module_order


    def print_order(self) -> None:
        print('Ordered Modules:')
        for i, module_name, module_imports in self.dump_order():
            MSG = '{:2d} : {:s} => {:s}'
            print(MSG.format(i, module_name, str(module_imports)))


    def log_order(self, logger : logging.Logger, level : int = logging.INFO) -> None:
        logger.log(level, 'Ordered Modules:')
        for i, module_name, module_imports in self.dump_order():
            MSG = '{:2d} : {:s} => {:s}'
            logger.log(level, MSG.format(i, module_name, str(module_imports)))


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    ymd = YangModuleDiscoverer('./yang')
    ordered_module_names = ymd.run(
        do_print_order=True,
        do_log_order=True
    )
    print('ordered_module_names', ordered_module_names)


if __name__ == '__main__':
    main()
