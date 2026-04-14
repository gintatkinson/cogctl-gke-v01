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

import inspect
import os
import json

from ..tf_service import TFService
from ..transport_capacity import TransportCapacity

resources = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "resources")

def test_transport_capacity_json():
    # Swagger example has been manually edited to match schema, that is moduleClientIfAid --> clientIfAid in state
    # Also names of leafs have been fixed to be unique
    # Once CM implementation is available, actual data obtained from CM should be used as a test vector
    with open(os.path.join(resources, "transport-capacities-swagger-example.json"), "r", encoding="UTF-8") as f:
        j = json.load(f)

        # A pre-planned constellation without endpoints
        tc = TransportCapacity(j[0])
        assert str(tc) == "name: Transport capacity service example, id: /transport-capacities/6ce3aa86-2685-44b0-9f86-49e6a6c991a8, capacity-mode: dedicatedDownlinkSymmetric, end-points: [(XR Device|XR T1, 100), (XR Device 2|XR T1, 100)]"

        config = tc.create_config()
        assert config == {'config': {'name': 'Transport capacity service example'}, 'endpoints': [{'capacity': 100, 'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR Device', 'moduleClientIfAid': 'XR T1'}}}, {'capacity': 100, 'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR Device 2', 'moduleClientIfAid': 'XR T1'}}}]}

def test_transport_capacity_comparison():
    # Same content must compare same
    t1=TransportCapacity(from_tf_service=TFService("foo", "Hub|T1", "Leaf 1|T2", 25))
    t2=TransportCapacity(from_tf_service=TFService("foo", "Hub|T1", "Leaf 1|T2", 25))
    assert t1 == t2

    # Order of endpoints does not matter:
    t2=TransportCapacity(from_tf_service=TFService("foo", "Leaf 1|T2", "Hub|T1", 25))
    assert t1 == t2

    # Different bandwidth
    t2=TransportCapacity(from_tf_service=TFService("foo", "Hub|T1", "Leaf 1|T2", 50))
    assert t1 != t2

    # Different leaf module
    t2=TransportCapacity(from_tf_service=TFService("foo", "Hub|T1", "Leaf 2|T2", 25))
    assert t1 != t2

    # Different leaf interface
    t2=TransportCapacity(from_tf_service=TFService("foo", "Hub|T1", "Leaf 1|T3", 25))
    assert t1 != t2
