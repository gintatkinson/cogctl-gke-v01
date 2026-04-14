#pylint: disable=invalid-name, missing-function-docstring, line-too-long, logging-fstring-interpolation, missing-class-docstring, missing-module-docstring
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

from typing import Any, Tuple, Optional, Dict

class InvalidIfnameError(Exception):
    def __init__(self, ifname):
        # Call the base class constructor with the parameters it needs
        super().__init__(f"Invalid interface name {ifname}, expecting format \"MODULENAME|PORTNAME\" or \"MODULENAME|PORTNAME.VLAN\"")

def ifname_to_module_and_aid(ifname: str) -> Tuple[str, str]:
    a = ifname.split("|")
    if len(a) != 2:
        raise InvalidIfnameError(ifname)
    return (a[0], a[1])

def virtual_aid_to_aid_and_vlan(ifname: str) -> Tuple[str, Optional[str]]:
    a = ifname.split(".")
    if len(a) == 1:
        return (ifname, None)
    if len(a) != 2:
        raise InvalidIfnameError(ifname)
    return (a[0], a[1])

def ifname_to_module_aid_vlan(ifname: str) -> Tuple[str, str, Optional[str]]:
    module, aid = ifname_to_module_and_aid(ifname)
    aid, vlan = virtual_aid_to_aid_and_vlan(aid)
    return (module, aid, vlan)

# For some reason when writing config, selector has moduleClientIfAid, when reading
# state it has clientIfAid...
def make_selector(mod, aid, _vlan) -> Dict[str, Any]:
    selector = {
        "moduleIfSelectorByModuleName": {
            "moduleName": mod,
            "moduleClientIfAid": aid,
        }
    }
    return selector

def get_constellation_module_ifnames(module):
    ifnames = []
    try:
        module_state = module["state"]
        module_name = module_state["module"]["moduleName"]
        if "endpoints" in module_state:
            for endpoint in module_state["endpoints"]:
                try:
                    ifname = endpoint["moduleIf"]["clientIfAid"]
                    ifnames.append(f"{module_name}|{ifname}")
                except KeyError:
                    pass
    except KeyError:
        pass
    return ifnames

def set_optional_parameter(container: Dict[str, any], key:str, value: Optional[any]):
    if value is not None:
        container[key] = value
