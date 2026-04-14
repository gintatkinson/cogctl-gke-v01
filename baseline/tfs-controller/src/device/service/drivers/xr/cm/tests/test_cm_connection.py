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
import requests_mock

#from ..tf_service import TFService
from ..cm_connection import CmConnection

access_token = r'{"access_token":"eyI3...","expires_in":3600,"refresh_expires_in":0,"refresh_token":"ey...","token_type":"Bearer","not-before-policy":0,"session_state":"f6e235c4-4ca4-4258-bede-4f2b7125adfb","scope":"profile email offline_access"}'

resources = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "resources")
with open(os.path.join(resources, "constellations-expanded.json"), "r", encoding="UTF-8") as f:
    res_constellations = f.read()
with open(os.path.join(resources, "constellation-by-name-hub1.json"), "r", encoding="UTF-8") as f:
    res_constellation_by_name_hub1 = f.read()

def mock_cm_connectivity():
    m = requests_mock.Mocker()
    m.post('https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token', text=access_token)
    return m

def test_cmc_connect():
    # Valid access token
    with requests_mock.Mocker() as m:
        m.post('https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token', text=access_token)
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, monitor_error_stream=False)
        assert cm.Connect()

    # Valid JSON but no access token
    with requests_mock.Mocker() as m:
        m.post('https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token', text=r'{"a": "b"}')
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, monitor_error_stream=False)
        assert not cm.Connect()

    # Invalid JSON
    with requests_mock.Mocker() as m:
        m.post('https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token', text=r'}}}')
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, monitor_error_stream=False)
        assert not cm.Connect()

    with requests_mock.Mocker() as m:
        # No mock present for the destination
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, monitor_error_stream=False)
        assert not cm.Connect()

def test_cmc_get_constellations():
    with mock_cm_connectivity() as m:
        m.get("https://127.0.0.1:9999/api/v1/xr-networks?content=expanded", text=res_constellations)
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, monitor_error_stream=False)
        assert cm.Connect()

        # List all constellations
        constellations = cm.list_constellations()
        assert len(constellations) == 2
        cids = [c.constellation_id for c in constellations]
        assert  cids == ["6774cc4e-b0b1-43a1-923f-80fb1bec094b", "233e169b-5d88-481d-bfe2-c909a2a859dd"]
        ifnames = [c.ifnames() for c in constellations]
        assert  ifnames == [['XR HUB 2|XR-T1', 'XR HUB 2|XR-T2', 'XR HUB 2|XR-T3', 'XR HUB 2|XR-T4', 'XR LEAF 3|XR-T1'],
                            ['XR HUB 1|XR-T1', 'XR HUB 1|XR-T2', 'XR HUB 1|XR-T3', 'XR HUB 1|XR-T4', 'XR LEAF 1|XR-T1', 'XR LEAF 2|XR-T1']]

        # Get constellation by hub module name
        m.get("https://127.0.0.1:9999/api/v1/xr-networks?content=expanded&content=expanded&q=%7B%22hubModule.state.module.moduleName%22%3A+%22XR+HUB+1%22%7D", text=res_constellation_by_name_hub1)
        constellation = cm.get_constellation_by_hub_name("XR HUB 1")
        assert constellation
        assert constellation.ifnames() == ['XR HUB 1|XR-T1', 'XR HUB 1|XR-T2', 'XR HUB 1|XR-T3', 'XR HUB 1|XR-T4', 'XR LEAF 1|XR-T1', 'XR LEAF 2|XR-T1']
        assert constellation.constellation_id == "233e169b-5d88-481d-bfe2-c909a2a859dd"
    