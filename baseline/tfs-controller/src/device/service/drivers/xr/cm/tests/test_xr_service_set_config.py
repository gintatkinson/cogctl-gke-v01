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
import traceback
import copy
import requests_mock

from ..cm_connection import CmConnection, ConsistencyMode, CreateConsistencyError
from ..tf import set_config_for_service

access_token = r'{"access_token":"eyI3...","expires_in":3600,"refresh_expires_in":0,"refresh_token":"ey...","token_type":"Bearer","not-before-policy":0,"session_state":"f6e235c4-4ca4-4258-bede-4f2b7125adfb","scope":"profile email offline_access"}'

resources = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "resources")
with open(os.path.join(resources, "constellation-by-name-hub1.json"), "r", encoding="UTF-8") as f:
    res_constellation_by_name_hub1 = f.read()
with open(os.path.join(resources, "connections-expanded.json"), "r", encoding="UTF-8") as f:
    j = json.load(f)
    # Fake reference data to have the name this test case needs for the given teraflow UUID
    # (=no need for too large set of reference material)
    j[0]["state"]["name"] = "TF:12345ABCDEFGHIJKLMN"
    res_connection_by_name_json = [j[0]] # Single item list

def mock_cm():
    m = requests_mock.Mocker()
    m.post('https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token', text=access_token)
    m.get("https://127.0.0.1:9999/api/v1/xr-networks?content=expanded&content=expanded&q=%7B%22hubModule.state.module.moduleName%22%3A+%22XR+HUB+1%22%7D", text=res_constellation_by_name_hub1)
    m.post("https://127.0.0.1:9999/api/v1/network-connections", text='[{"href":"/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432","rt":["cm.network-connection"]}]', status_code=202)
    return m

uuid = "12345ABCDEFGHIJKLMN"
config = {
    "input_sip_name": "XR HUB 1|XR-T4;",
    "output_sip_name": "XR LEAF 1|XR-T1",
    "capacity_value": 125,
    "capacity_unit": "gigabit"
}

def _validate_result(result, expect):
    if isinstance(expect, Exception):
        assert type(result) == type(expect)
    else:
        if isinstance(result, Exception):
            traceback.print_exception(result)
        assert result is expect # Not, "is", not ==, we want type checking in this case, as also an exception can be returned (as return value)

def test_xr_set_config():
    with mock_cm() as m:
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, monitor_error_stream=False)
        assert cm.Connect()

        constellation = cm.get_constellation_by_hub_name("XR HUB 1")
        assert constellation

        result = set_config_for_service(cm, constellation, uuid, config)
        _validate_result(result, True)

        called_mocks = [(r._request.method, r._request.url) for r in m._adapter.request_history]
        expected_mocks = [
            ('POST', 'https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token'), # Authentication
            ('GET',  'https://127.0.0.1:9999/api/v1/xr-networks?content=expanded&content=expanded&q=%7B%22hubModule.state.module.moduleName%22%3A+%22XR+HUB+1%22%7D'),  # Hub module by name
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections?content=expanded&q=%7B%22state.name%22%3A+%22TF%3A12345ABCDEFGHIJKLMN%22%7D'),  # Get by name, determine update or create
            ('POST', 'https://127.0.0.1:9999/api/v1/network-connections') # Create
        ]
        assert called_mocks == expected_mocks

# In life cycle tests, multiple queries are performed by the driver to check life cycle progress.
# Extend expected mock to match called mock length by replicating the last item (the repeated GET)
def repeat_last_expected(expected: list[tuple], called: list[tuple]) -> list[tuple]:
    diff = len(called) - len(expected)
    if diff > 0:
        expected = list(expected) # Don't modify the original list
        expected.extend([expected[-1]] * diff)
    return expected

def test_xr_set_config_consistency_lifecycle():
    with mock_cm() as m:
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, consistency_mode=ConsistencyMode.lifecycle, retry_interval=0, timeout=1, max_consistency_tries=3, monitor_error_stream=False)
        assert cm.Connect()

        constellation = cm.get_constellation_by_hub_name("XR HUB 1")
        assert constellation

        # Note that JSON here is for different object, but we are not inspecting fields where it would matter (e.g. IDs).
        json_terminal = res_connection_by_name_json[0]
        json_non_terminal = copy.deepcopy(json_terminal)
        json_non_terminal["state"]["lifecycleState"] = "pendingConfiguration"
        # We go trough 404 and non-terminal lstate first and then terminal state.
        m.get("https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432",
              [{'text': '', 'status_code': 404},
               { 'json': json_non_terminal, 'status_code': 200 },
               {'json': json_terminal, 'status_code': 200  }])

        result = set_config_for_service(cm, constellation, uuid, config)
        _validate_result(result, True)

        called_mocks = [(r._request.method, r._request.url) for r in m._adapter.request_history]
        expected_mocks = [
            ('POST', 'https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token'), # Authentication
            ('GET',  'https://127.0.0.1:9999/api/v1/xr-networks?content=expanded&content=expanded&q=%7B%22hubModule.state.module.moduleName%22%3A+%22XR+HUB+1%22%7D'),  # Hub module by name
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections?content=expanded&q=%7B%22state.name%22%3A+%22TF%3A12345ABCDEFGHIJKLMN%22%7D'),  # Get by name, determine update or create
            ('POST', 'https://127.0.0.1:9999/api/v1/network-connections'), # Create
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432?content=expanded'), # Life cycle state check --> no REST API object
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432?content=expanded'), # Life cycle state check --> non-terminal
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432?content=expanded') # Life cycle state check --> terminal
        ]
        assert called_mocks == expected_mocks

        ################################################################################
        # Same as before, but without life cycle progress
        m.reset_mock()
        m.get("https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432",
              [{'text': '', 'status_code': 401},
               { 'json': json_non_terminal, 'status_code': 200 }])

        result = set_config_for_service(cm, constellation, uuid, config)
        _validate_result(result, CreateConsistencyError("")) # Service creation failure due to insufficient progress

        called_mocks = [(r._request.method, r._request.url) for r in m._adapter.request_history]
        expected_mocks_no_connect = [
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections?content=expanded&q=%7B%22state.name%22%3A+%22TF%3A12345ABCDEFGHIJKLMN%22%7D'),  # Get by name, determine update or create
            ('POST', 'https://127.0.0.1:9999/api/v1/network-connections'), # Create
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432?content=expanded'), # Life cycle state check --> no REST API object
            ('GET',  'https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432?content=expanded'), # Life cycle state check --> non-terminal
        ]
        assert called_mocks == repeat_last_expected(expected_mocks_no_connect, called_mocks)

        ################################################################################
        # Same as before, but CmConnection no longer requiring lifcycle progress
        m.reset_mock()
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, consistency_mode=ConsistencyMode.synchronous, retry_interval=0, timeout=1, max_consistency_tries=3, monitor_error_stream=False)
        assert cm.Connect()
        constellation = cm.get_constellation_by_hub_name("XR HUB 1")
        assert constellation
        m.get("https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432",
              [{'text': '', 'status_code': 401},
               { 'json': json_non_terminal, 'status_code': 200 }])
        result = set_config_for_service(cm, constellation, uuid, config)
        _validate_result(result, True)
        called_mocks = [(r._request.method, r._request.url) for r in m._adapter.request_history]
        assert called_mocks == expected_mocks[:2] + expected_mocks_no_connect

        ################################################################################
        # Same as above, but without REST object appearing
        m.reset_mock()
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, consistency_mode=ConsistencyMode.synchronous, retry_interval=0, timeout=1, max_consistency_tries=3, monitor_error_stream=False)
        assert cm.Connect()
        constellation = cm.get_constellation_by_hub_name("XR HUB 1")
        assert constellation
        m.get("https://127.0.0.1:9999/api/v1/network-connections/c3b31608-0bb7-4a4f-9f9a-88b24a059432",
              [{'text': '', 'status_code': 401}])
        result = set_config_for_service(cm, constellation, uuid, config)
        _validate_result(result, CreateConsistencyError(""))
        called_mocks = [(r._request.method, r._request.url) for r in m._adapter.request_history]
        assert called_mocks == repeat_last_expected(expected_mocks[:2] + expected_mocks_no_connect, called_mocks)


def test_xr_set_config_update_case():
    with mock_cm() as m:
        cm = CmConnection("127.0.0.1", 9999, "xr-user", "xr-password", tls_verify=False, monitor_error_stream=False)
        assert cm.Connect()

        constellation = cm.get_constellation_by_hub_name("XR HUB 1")
        assert constellation

        # Fake existing service (--> update path is taken)
        m.get("https://127.0.0.1:9999/api/v1/network-connections?content=expanded&q=%7B%22state.name%22%3A+%22TF%3A12345ABCDEFGHIJKLMN%22%7D", json=res_connection_by_name_json)
        # Delete endpoint that is no longer necessary
        m.delete("https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/1d58ba8f-4d51-4213-83e1-97a0e0bdd388", text="", status_code = 202)
        # Update changed endpoint
        m.put("https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/230516d0-7e38-44b1-b174-1ba7d4454ee6", text="", status_code = 202)
        # Create the newly added endpoint
        m.post("https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints", json=[{"href":"/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoint/somethingplausible","rt":["plausible"]}], status_code=202)
        # Update the connection itself
        m.put("https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03", text="", status_code=202)

        result = set_config_for_service(cm, constellation, uuid, config)
        _validate_result(result, True)

        called_mocks = [(r._request.method, r._request.url) for r in m._adapter.request_history]
        expected_mocks = [
            ('POST',   'https://127.0.0.1:9999/realms/xr-cm/protocol/openid-connect/token'), # Authentication
            ('GET',    'https://127.0.0.1:9999/api/v1/xr-networks?content=expanded&content=expanded&q=%7B%22hubModule.state.module.moduleName%22%3A+%22XR+HUB+1%22%7D'),  # Hub module by name
            ('GET',    'https://127.0.0.1:9999/api/v1/network-connections?content=expanded&q=%7B%22state.name%22%3A+%22TF%3A12345ABCDEFGHIJKLMN%22%7D'),  # Get by name, determine update or create
            ('DELETE', 'https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/1d58ba8f-4d51-4213-83e1-97a0e0bdd388'), # Delete unnecessary endpoint
            ('PUT',    'https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/230516d0-7e38-44b1-b174-1ba7d4454ee6'), # Update changed endpoint
            ('POST',   'https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints'), # Add new endpoint
            ('PUT',    'https://127.0.0.1:9999/api/v1/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03') # Update the connection itself
        ]
        assert called_mocks == expected_mocks
