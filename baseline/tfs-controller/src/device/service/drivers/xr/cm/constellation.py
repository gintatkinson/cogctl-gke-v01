#pylint: disable=invalid-name, missing-function-docstring, line-too-long, logging-fstring-interpolation, missing-class-docstring, missing-module-docstring, wildcard-import, unused-wildcard-import
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

from typing import List
from .utils import *

class ConstellationDeserializationError(Exception):
    pass

class Constellation:
    def __init__(self, from_json=None):
        if from_json:
            try:
                self.constellation_id = from_json["id"]
                self.__hub_interfaces = []
                self.__leaf_interfaces = []
                self.__traffic_mode = None
                # Intentional simplification for Teraflow. Constellation could have
                # diverse traffic modes, however that does not occur in intended TF usage.
                if "hubModule" in from_json:
                    hub = from_json["hubModule"]
                    self.traffic_mode = hub["state"]["module"]["trafficMode"]
                    self.__hub_interfaces.extend(get_constellation_module_ifnames(hub))
                if "leafModules" in from_json:
                    for leaf in from_json["leafModules"]:
                        if not self.__traffic_mode:
                            self.traffic_mode = leaf["state"]["module"]["trafficMode"]
                        self.__leaf_interfaces.extend(get_constellation_module_ifnames(leaf))
            except KeyError as e:
                raise ConstellationDeserializationError(f"Missing mandatory key {str(e)}") from e
        else:
            # May support other initializations in future
            raise ConstellationDeserializationError("JSON dict missing")

        def add_vlan_posfix(ifname, is_hub):
            if is_hub:
                # +100 so we don't need to worry about special meanings of VLANs 0 and 1
                return [f"{ifname}.{vlan+100}" for vlan in range(0,16)]
            else:
                return [f"{ifname}.{chr(ord('a') + vlan)}" for vlan in range(0,16)]

        self.__vti_hub_interfaces = []
        self.__vti_leaf_interfaces = []
        if self.is_vti_mode():
            for ifname in self.__hub_interfaces:
                self.__vti_hub_interfaces.extend(add_vlan_posfix(ifname, True))
            for ifname in self.__leaf_interfaces:
                self.__vti_leaf_interfaces.extend(add_vlan_posfix(ifname, False))

    def ifnames(self) -> List[str]:
        if self.is_vti_mode():
            return self.__vti_hub_interfaces + self.__vti_leaf_interfaces
        else:
            return self.__hub_interfaces + self.__leaf_interfaces

    def is_vti_mode(self) -> bool:
        return self.traffic_mode != "L1Mode"
