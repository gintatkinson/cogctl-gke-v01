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

from __future__ import annotations
from typing import Dict, Optional
from dataclasses import dataclass
from .tf_service import TFService
from .utils import make_selector, set_optional_parameter

class InconsistentVlanConfiguration(Exception):
    pass

@dataclass
class CEndpoint:
    module: str
    port: str
    # Emulated/translated VLAN. May also be a letter
    # Only present on TF side, never on gets from CM.
    # VLAN is never transmitted to wire on endpoint, it is purely an internal construct
    # However VLAN is part of the whole connection
    vlan: str
    capacity: int
    href: Optional[str]

    def ifname(self) -> str:
        if self.vlan is None:
            return self.module + "|" + self.port
        else:
            return self.module + "|" + self.port + "." + self.vlan

    def portname(self) -> str:
        return self.module + "|" + self.port

    def __str__(self):
        return f"({self.ifname()}, {self.capacity})"

    def create_config(self) -> Dict[str, any]:
        cfg = {
            # VLAN is intentionally ignored here (None argument below)
            "selector":  make_selector(self.module, self.port, None)
        }
        if self.capacity > 0:
            cfg["capacity"] = self.capacity

        return cfg

@dataclass
class LifeCycleInfo:
    # State is None (if not known), or one of the following (in future there might be more, so lets not assuem too much)
    #     'pendingConfiguration': This state occurs when one of the network connection modules is pending configuration or pending deletion.
    #     'configured': This state occurs when all network connection modules are configured.
    #     'configurationFailed': This state may occur when at least a configuration of a module from this network connection failed or timeout.
    #     'pendingDeletion': This state may occur when a request to delete this network connection is being processed.
    #     'deletionFailed': This state may occur when at least a removal of a module from this network connection failed or timeout.
    #     'networkConflict': This state may occur when there is a conflict in a network connection module configuration.
    #     'deleted': This state occurs when a network connection is removed.
    state: Optional[str]
    reason: Optional[str]

    def is_terminal_state(self) -> bool:
        if self.state is None:
            return True
        if self.state.endswith('Failed') or self.state.endswith('Conflict'):
            return True
        if self.state == "configured" or self.state == "deleted":
            return True
        return False

    def __str__(self):
        state_str = "unknown" if self.state is None else self.state
        if self.reason:
            return f"({state_str} (reason: {self.reason})"
        return state_str

    @staticmethod
    def new_from_top_level_json(json_dict: Dict[str, any]) -> LifeCycleInfo:
        if "state" not in json_dict:
            return LifeCycleInfo(None, None)
        state = json_dict["state"]
        return LifeCycleInfo(state.get("lifecycleState", None), state.get("lifecycleReason", None))

    @staticmethod
    def new_unknown() -> LifeCycleInfo:
        return LifeCycleInfo(None, "not yet communicated with IPM")

class ConnectionDeserializationError(Exception):
    pass

class Connection:
    def __init__(self, from_json: Optional[Dict[str, any]] = None, from_tf_service: Optional[TFService] = None):
        def get_endpoint_mod_aid(endpoint: Dict[str, any]) -> Optional[str]:
            try:
                return (endpoint["state"]["moduleIf"]["moduleName"], endpoint["state"]["moduleIf"]["clientIfAid"])
            except KeyError:
                return None

        def get_endpoint_capacity(endpoint: Dict[str, any]) -> int:
            try:
                return int(endpoint["state"]["capacity"])
            except KeyError:
                return 0

        if from_json:
            try:
                config = from_json["config"]
                state = from_json["state"]
                self.name = state["name"] if "name" in state else None #Name is optional
                self.serviceMode = state["serviceMode"]
                # Implicit transport capacity is a string, where value "none" has special meaning.
                # So "none" is correct value, not "None" for missing attribute
                self.implicitTransportCapacity = config["implicitTransportCapacity"] if "implicitTransportCapacity" in config else "none"
                self.mc = config["mc"] if "mc" in config else None
                self.vlan_filter = state["outerVID"] if "outerVID" in state else None
                self.href = from_json["href"]

                self.endpoints = []
                for ep in from_json["endpoints"]:
                    ep_mod_aip = get_endpoint_mod_aid(ep)
                    if ep_mod_aip:
                        self.endpoints.append(CEndpoint(*ep_mod_aip, None, get_endpoint_capacity(ep), ep["href"]))

                self.life_cycle_info = LifeCycleInfo.new_from_top_level_json(from_json)
                self.cm_data = from_json
            except KeyError as e:
                raise ConnectionDeserializationError(f"Missing mandatory key {str(e)}") from e
        elif from_tf_service:
            self.href = None
            self.name = from_tf_service.name()
            self.endpoints = [CEndpoint(mod, port, vlan, from_tf_service.capacity, None) for mod,port,vlan in from_tf_service.get_endpoints_mod_aid_vlan()]
            # Service mode guessing has to be AFTER endpoint assigment.
            # The heuristic used is perfectly valid in context of TF where we always encode
            # VLANs to interface names. Correspondingly cm-cli user has to know
            # to use VLANs on low level test APIs when using VTI mode.
            self.serviceMode = self.__guess_service_mode_from_emulated_enpoints()
            if self.serviceMode == "XR-L1":
                self.vlan_filter = None
                self.mc = None
                self.implicitTransportCapacity ="portMode"
            else:
                self.vlan_filter = str(self.__guess_vlan_id()) + " " # Needs to be in string format, can contain ranges, regexp is buggy, trailin space is needed for single VLAN
                self.mc = "matchOuterVID"
                # String "none" has a special meaning for implicitTransportCapacity
                self.implicitTransportCapacity ="none"

            self.life_cycle_info = LifeCycleInfo.new_unknown()
            self.cm_data = None
        else:
            # May support other initializations in future
            raise ConnectionDeserializationError("JSON dict missing")

    def __str__(self):
        name = self.name if self.name else "<NO NAME>"
        endpoints = ", ".join((str(ep) for ep in self.endpoints))
        return f"name: {name}, id: {self.href}, service-mode: {self.serviceMode}, end-points: [{endpoints}]"

    def is_vti_mode(self) -> bool:
        return "XR-VTI-P2P" == self.serviceMode

    def __guess_service_mode_from_emulated_enpoints(self):
        for ep in self.endpoints:
            if ep.vlan is not None:
                return "XR-VTI-P2P"
        return "XR-L1"

    def __guess_vlan_id(self) -> int:
        vlans = []
        for ep in self.endpoints:
            if ep.vlan is not None and ep.vlan.isnumeric():
                vlans.append(int(ep.vlan))
        if not vlans:
            raise InconsistentVlanConfiguration("VLAN ID is not encoded in TF interface names for VTI mode service")
        else:
            for vlan in vlans:
                if vlan != vlans[0]:
                    raise InconsistentVlanConfiguration(f"VLAN configuration must match at both ends of the connection, {vlans[0]} != {vlan}")
        return vlans[0]

    def create_config(self) -> Dict[str, any]:
        cfg = {}
        set_optional_parameter(cfg, "name", self.name)
        cfg["serviceMode"] = self.serviceMode
        cfg["implicitTransportCapacity"] = self.implicitTransportCapacity
        if self.endpoints:
            cfg["endpoints"] = [ep.create_config() for ep in self.endpoints]
        set_optional_parameter(cfg, "outerVID", self.vlan_filter)
        set_optional_parameter(cfg, "mc", self.mc)
        #print(cfg)
        return cfg

    def get_port_map(self) -> Dict[str, CEndpoint]:
        return {ep.portname(): ep for ep in self.endpoints }

    # Type hint has to be string, because future annotations (enclosing class)
    # is not yet widely available
    def get_endpoint_updates(self, old: Optional['Connection']): # -> Tuple[List[str], List[Dict[str, any], List[Tuple[str, Dict[str, any]]]]]:
        new_ports = self.get_port_map()

        if old is None:
            return ([], [new_ep.create_config() for new_ep in new_ports.values()], [])

        # Can only compute difference against get from CM, as hrefs are needed
        assert old.cm_data is not None

        old_ports = old.get_port_map()

        deletes = []
        creates = []
        updates = []
        for port, old_ep in old_ports.items():
            if port not in new_ports:
                assert old_ep.href is not None
                deletes.append(old_ep.href)

        for port, new_ep in new_ports.items():
            if port not in old_ports:
                creates.append(new_ep.create_config())
            elif old_ports[port].capacity != new_ep.capacity:
                updates.append((old_ports[port].href, {"capacity": new_ep.capacity}))
        return deletes, creates, updates
