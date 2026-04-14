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

import math
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List
from .utils import *

@dataclass(init=False)
class TFService:
    input_sip: str
    output_sip: str
    uuid: str
    capacity: int

    def __init__(self, uuid, input_sip, output_sip, capacity):
        self.uuid = uuid
        self.input_sip = input_sip
        self.output_sip = output_sip
        # Capacity must be in multiples of 25 gigabits
        if 0 == capacity:
            self.capacity = 0
        else:
            self.capacity = math.ceil(capacity/25) * 25

    def __str__(self):
        return f"({self.uuid}, {self.input_sip}, {self.output_sip}, {self.capacity})"

    def name(self) -> str:
        return f"TF:{self.uuid}"

    def input_mod_aid_vlan(self) -> Tuple[str, str, Optional[str]]:
        return ifname_to_module_aid_vlan(self.input_sip)

    def output_mod_aid_vlan(self) -> Tuple[str, str, Optional[str]]:
        return ifname_to_module_aid_vlan(self.output_sip)

    # Return endpoints in a form suitable for selectors in various
    # JSON constructs used by the CM API
    def get_endpoint_selectors(self) -> List[Dict]:
        return [make_selector(*self.input_mod_aid_vlan()), make_selector(*self.output_mod_aid_vlan())]

    #  -> List[Tuple(str, str)]
    def get_endpoints_mod_aid(self):
        m1, a1, _ = self.input_mod_aid_vlan()
        m2, a2, _ = self.output_mod_aid_vlan()

        return [(m1, a1), (m2, a2)]

    #  -> List[Tuple(str, str)]
    def get_endpoints_mod_aid_vlan(self):
        m1, a1, v1 = self.input_mod_aid_vlan()
        m2, a2, v2 = self.output_mod_aid_vlan()

        return [(m1, a1, v1), (m2, a2, v2)]
