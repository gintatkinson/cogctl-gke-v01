# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from lxml import etree
from netconf import util
from pyangbind.lib.serialise import pybindIETFXMLEncoder

from openconfig.components import components
from openconfig.interfaces import interfaces

def get_device_definition():
    occ = components()
    port_1_1 = occ.component.add("1/1")
    port_1_1.state._set_type("PORT") # state.type is read-only; use special method to set it

    port_1_2 = occ.component.add("1/2")
    port_1_2.state._set_type("PORT") # state.type is read-only; use special method to set it

    port_1_3 = occ.component.add("1/3")
    port_1_3.state._set_type("PORT") # state.type is read-only; use special method to set it

    ocif = interfaces()

    data = util.elm("nc:data")
    data.append(etree.XML(pybindIETFXMLEncoder.serialise(occ)))
    data.append(etree.XML(pybindIETFXMLEncoder.serialise(ocif)))
    return data
