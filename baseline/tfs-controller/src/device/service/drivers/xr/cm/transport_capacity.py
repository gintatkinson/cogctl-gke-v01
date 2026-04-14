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

from typing import Optional, Dict
from dataclasses import dataclass

from .utils import make_selector

from .tf_service import TFService

@dataclass
class TCEndpoint:
    module: str
    port: str
    capacity: int

    def ifname(self) -> str:
        return self.module + "|" + self.port

    def __str__(self):
        return f"({self.ifname()}, {self.capacity})"

    def create_config(self) -> Dict[str, any]:
        cfg = {
            "capacity": self.capacity,
            "selector":  make_selector(self.module, self.port, None)
        }
        return cfg

class TransportCapacityDeserializationError(Exception):
    pass

class TransportCapacity:
    def __init__(self, from_json=None, from_tf_service: Optional[TFService] = None):
        def get_endpoint_from_json(endpoint: dict[str, any]) -> Optional[TCEndpoint]:
            try:
                return TCEndpoint(endpoint["state"]["moduleIf"]["moduleName"], endpoint["state"]["moduleIf"]["clientIfAid"],
                                  endpoint["state"]["capacity"])
            except KeyError:
                return None

        if from_json:
            try:
                self.href = from_json["href"]

                state = from_json["state"]
                # Name is optional
                self.name = state["name"] if "name" in state else None
                self.capacity_mode = state["capacityMode"]

                self.endpoints = []
                for epj in from_json["endpoints"]:
                    ep = get_endpoint_from_json(epj)
                    if ep:
                        self.endpoints.append(ep)

                #self.__cm_data = from_json
            except KeyError as e:
                raise TransportCapacityDeserializationError(f"Missing mandatory key {str(e)}") from e
        elif from_tf_service:
            self.href = None
            self.state = "tfInternalObject"
            self.name = from_tf_service.name()
            self.capacity_mode = "dedicatedDownlinkSymmetric"
            self.endpoints = [TCEndpoint(mod, port, from_tf_service.capacity) for mod,port in from_tf_service.get_endpoints_mod_aid()]
            #self.__cm_data = None
        else:
            # May support other initializations in future
            raise TransportCapacityDeserializationError("Initializer missing")

    # Return suitable config for CM
    def create_config(self) -> Dict[str, any]:
        cfg = {}
        if self.name is not None:
            cfg["config"] = {"name": self.name }
        cfg["endpoints"] = [ep.create_config() for ep in self.endpoints]
        return cfg

    def __str__(self):
        name = self.name if self.name else "<NO NAME>"
        endpoints = ", ".join((str(ep) for ep in self.endpoints))
        return f"name: {name}, id: {self.href}, capacity-mode: {self.capacity_mode}, end-points: [{endpoints}]"

    # Comparison for purpose of re-configuring
    def __eq__(self, obj):
        if not isinstance(obj, TransportCapacity):
            return False
        if self.name != obj.name:
            return False
        if self.capacity_mode != obj.capacity_mode:
            return False
        if sorted(self.endpoints, key=str) != sorted(obj.endpoints, key=str):
            return False
        return True

    def __ne__(self, obj):
        return not self == obj
