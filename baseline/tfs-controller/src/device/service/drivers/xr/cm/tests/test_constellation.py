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
import pytest
from ..constellation import Constellation, ConstellationDeserializationError

resources = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "resources")

def test_constellation_json():
    # With a name
    with open(os.path.join(resources, "constellations-expanded.json"), "r", encoding="UTF-8") as f:
        j = json.load(f)

        # Proper constellation with endpoints
        constellation = Constellation(j[1])
        assert constellation.constellation_id == "233e169b-5d88-481d-bfe2-c909a2a859dd"
        assert not constellation.is_vti_mode()
        print(constellation.ifnames())
        assert ['XR HUB 1|XR-T1', 'XR HUB 1|XR-T2', 'XR HUB 1|XR-T3', 'XR HUB 1|XR-T4', 'XR LEAF 1|XR-T1', 'XR LEAF 2|XR-T1']  == constellation.ifnames()

        # Remove mandatory key, will raise an exception
        del j[0]["hubModule"]["state"]
        with pytest.raises(ConstellationDeserializationError, match=r"Missing mandatory key 'state'"):
            _constellation = Constellation(j[0])
