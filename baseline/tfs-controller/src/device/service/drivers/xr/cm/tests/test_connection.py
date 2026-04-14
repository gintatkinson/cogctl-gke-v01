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

from ..tf_service import TFService
from ..connection import Connection, InconsistentVlanConfiguration, ConnectionDeserializationError

resources = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "resources")

def test_connection_json():
    with open(os.path.join(resources, "connections-expanded.json"), "r", encoding="UTF-8") as f:
        j = json.load(f)
        connection = Connection(j[0])

        assert connection.name == "FooBar123"
        assert "name: FooBar123, id: /network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03, service-mode: XR-L1, end-points: [(XR LEAF 1|XR-T1, 0), (XR HUB 1|XR-T1, 0)]" == str(connection)
        assert "configured" == str(connection.life_cycle_info)
        assert connection.life_cycle_info.is_terminal_state()

        config = connection.create_config()
        expected_config = {'name': 'FooBar123', 'serviceMode': 'XR-L1', 'implicitTransportCapacity': 'portMode', 'endpoints': [{'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR LEAF 1', 'moduleClientIfAid': 'XR-T1'}}}, {'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR HUB 1', 'moduleClientIfAid': 'XR-T1'}}}]}
        assert config == expected_config

        # Remove mandatory key from leaf endpoint. It will not be parsed, but hub endpoint will
        del j[0]["endpoints"][0]["state"]["moduleIf"]["clientIfAid"]
        connection = Connection(j[0])
        assert "name: FooBar123, id: /network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03, service-mode: XR-L1, end-points: [(XR HUB 1|XR-T1, 0)]" == str(connection)

        # Remove Name, it is optional (although TF will always configure it)
        del j[0]["state"]["name"]
        connection = Connection(j[0])
        assert "name: <NO NAME>, id: /network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03, service-mode: XR-L1, end-points: [(XR HUB 1|XR-T1, 0)]" == str(connection)

        # Remove mandatory key, will raise an exception
        del j[0]["state"]
        with pytest.raises(ConnectionDeserializationError, match=r"Missing mandatory key 'state'"):
            _connection = Connection(j[0])

def test_connection_ep_change_compute():
    with open(os.path.join(resources, "connections-expanded.json"), "r", encoding="UTF-8") as f:
        j = json.load(f)
        existing_connection = Connection(j[0])

        # Changing only capacity
        new_connection = Connection(from_tf_service=TFService("FooBar123", "XR LEAF 1|XR-T1", "XR HUB 1|XR-T1", 25))
        ep_deletes, ep_creates, ep_updates = new_connection.get_endpoint_updates(existing_connection)
        assert not ep_deletes
        assert not ep_creates
        assert  ep_updates == [('/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/230516d0-7e38-44b1-b174-1ba7d4454ee6', {'capacity': 25}), ('/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/1d58ba8f-4d51-4213-83e1-97a0e0bdd388', {'capacity': 25})]

        # Change one of endpoints
        new_connection = Connection(from_tf_service=TFService("FooBar123", "XR LEAF 1|XR-T1", "XR HUB 1|changed here", 0))
        ep_deletes, ep_creates, ep_updates = new_connection.get_endpoint_updates(existing_connection)
        assert ep_deletes ==  ['/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/1d58ba8f-4d51-4213-83e1-97a0e0bdd388']
        assert ep_creates == [{'selector': {'moduleIfSelectorByModuleName': {'moduleClientIfAid': 'changed here', 'moduleName': 'XR HUB 1'}}}]
        assert not ep_updates

        # Change one of the endpoints and capacity
        new_connection = Connection(from_tf_service=TFService("FooBar123", "XR LEAF 1|XR-T1", "XR HUB 1|changed here", 125))
        ep_deletes, ep_creates, ep_updates = new_connection.get_endpoint_updates(existing_connection)
        assert ep_deletes ==  ['/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/1d58ba8f-4d51-4213-83e1-97a0e0bdd388']
        assert ep_creates == [{'selector': {'moduleIfSelectorByModuleName': {'moduleClientIfAid': 'changed here', 'moduleName': 'XR HUB 1'}}, "capacity": 125}]
        assert ep_updates == [('/network-connections/4505d5d3-b2f3-40b8-8ec2-4a5b28523c03/endpoints/230516d0-7e38-44b1-b174-1ba7d4454ee6', {'capacity': 125})]

        # No change at all
        new_connection = Connection(from_tf_service=TFService("FooBar123", "XR LEAF 1|XR-T1", "XR HUB 1|XR-T1", 0))
        ep_deletes, ep_creates, ep_updates = new_connection.get_endpoint_updates(existing_connection)
        assert not ep_deletes
        assert not ep_creates
        assert not ep_updates

        # Order of endpoints does not matter
        new_connection = Connection(from_tf_service=TFService("FooBar123", "XR HUB 1|XR-T1", "XR LEAF 1|XR-T1", 0))
        ep_deletes, ep_creates, ep_updates = new_connection.get_endpoint_updates(existing_connection)
        assert not ep_deletes
        assert not ep_creates
        assert not ep_updates

def test_connection_from_service():
    # Port mode
    connection = Connection(from_tf_service=TFService("FooBar123", "XR LEAF 1|XR-T1", "XR HUB 1|XR-T1", 0))
    assert connection.create_config() == {'name': 'TF:FooBar123', 'serviceMode': 'XR-L1', 'implicitTransportCapacity': 'portMode', 'endpoints': [{'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR LEAF 1', 'moduleClientIfAid': 'XR-T1'}}}, {'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR HUB 1', 'moduleClientIfAid': 'XR-T1'}}}]}
    assert '(unknown (reason: not yet communicated with IPM)' == str(connection.life_cycle_info)
    assert connection.life_cycle_info.is_terminal_state()

    # VTI mode
    connection = Connection(from_tf_service=TFService("FooBar123", "XR LEAF 1|XR-T1.A", "XR HUB 1|XR-T1.100", 0))
    # In endpoint selectors VLANs are note present (CM does not know about them, encoding them to aids is purely internal to Teraflow)
    # However VLAN adds outerVID and some other fields
    assert connection.create_config() == {'name': 'TF:FooBar123', 'serviceMode': 'XR-VTI-P2P', 'implicitTransportCapacity': 'none', 'endpoints': [{'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR LEAF 1', 'moduleClientIfAid': 'XR-T1'}}}, {'selector': {'moduleIfSelectorByModuleName': {'moduleName': 'XR HUB 1', 'moduleClientIfAid': 'XR-T1'}}}], 'outerVID': '100 ', 'mc': 'matchOuterVID'}

    # Invalid configuration, differring VLANs on different sides
    with pytest.raises(InconsistentVlanConfiguration) as _e_info:
        Connection(from_tf_service=TFService("FooBar123", "XR LEAF 1|XR-T1.200", "XR HUB 1|XR-T1.100", 0))
