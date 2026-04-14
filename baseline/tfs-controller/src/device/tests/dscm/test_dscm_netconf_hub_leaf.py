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


import json, logging, os, pytest, time
from typing import Dict, Tuple
from device.service.drivers.netconf_dscm.NetConfDriver import NetConfDriver

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

DEVICES = {
            'hub':  {'address': '10.30.7.7', 'port': 2023, 'settings': {}},
            'leaf': {'address': '10.30.7.8', 'port': 2023, 'settings': {}}
        }

@pytest.fixture(autouse=True)
def log_each(request):
    LOGGER.info(f">>>>>> START {request.node.name} >>>>>>")
    yield
    LOGGER.info(f"<<<<<< END   {request.node.name} <<<<<<")

@pytest.fixture(scope='session')
def get_driver_hub() -> Tuple[NetConfDriver, None]:  # pyright: ignore[reportInvalidTypeForm]
    driver = NetConfDriver(
        DEVICES['hub']['address'], DEVICES['hub']['port'], **(DEVICES['hub']['settings'])
        )
    yield driver            # pyright: ignore[reportReturnType]
    time.sleep(1)

@pytest.fixture(scope='session')
def get_driver_leaf() -> Tuple[NetConfDriver, None]:  # pyright: ignore[reportInvalidTypeForm]
    driver = NetConfDriver(
        DEVICES['leaf']['address'], DEVICES['leaf']['port'], **(DEVICES['leaf']['settings'])
        )
    yield driver            # pyright: ignore[reportReturnType]
    time.sleep(1)


# --- Directly Testing SBI
def test_get_default_hub_config(get_driver_hub) -> Dict:
    data =  {
            "name": "channel-1",
            "frequency": 195000000,
            "operational_mode": 1,
            "target_output_power": 0.0,
            "operation"          : "merge",
            "digital_sub_carriers_group": [
                {
                    "digital_sub_carriers_group_id": 1,
                    "digital_sub_carrier_id": [
                        {
                            "sub_carrier_id": 1,
                            "active": "true"
                        },
                        {
                            "sub_carrier_id": 2,
                            "active": "true"
                        },
                        {
                            "sub_carrier_id": 3,
                            "active": "true"
                        },
                        {
                            "sub_carrier_id": 4,
                            "active": "true"
                        }
                    ]
                },
                {
                    "digital_sub_carriers_group_id": 2,
                    "digital_sub_carrier_id": [
                        {
                            "sub_carrier_id": 5,
                            "active": "true"
                        },
                        {
                            "sub_carrier_id": 6,
                            "active": "true"
                        },
                        {
                            "sub_carrier_id": 7,
                            "active": "true"
                        },
                        {
                            "sub_carrier_id": 8,
                            "active": "true"
                        }
                    ]
                }
            ],
        }
    node = 'T2.1'
    result_config = get_driver_hub.SetConfig([(node, data)])
    assert result_config is not None

def test_get_default_leaves_config(get_driver_leaf) -> Dict:
    data =  {
            "name"               : "channel-1",     # "channel-1", "channel-3", "channel-5"    
            "frequency"          : 195006250,       # "195006250", 195018750, 195031250
            "operational_mode"   : 1,
            "target_output_power": -99,             # should be -99
            "operation"          : "merge",
            "digital_sub_carriers_group": [
                {
                    "digital_sub_carriers_group_id": 1,
                    "digital_sub_carrier_id": [
                        {
                            "sub_carrier_id": 1,
                            "active": "false"        # should be set to false
                        },
                        {
                            "sub_carrier_id": 2,
                            "active": "false"
                        },
                        {
                            "sub_carrier_id": 3,
                            "active": "false"
                        },
                        {
                            "sub_carrier_id": 4,
                            "active": "false"
                        }
                    ]
                }
            ],
        }
    node = 'T1.1'
    result_config = get_driver_leaf.SetConfig([(node, data)])
    assert result_config is not None

# netconf-console2 --host=10.30.7.7 --port=2023 --tcp --get-config -x '/components/component[name="channel-1"]/optical-channel/state/input-power/instant'

# def test_get_config(get_driver):
#     path = '/components/component[name="channel-1"]/optical-channel/state/input-power/instant'
#     result_config = get_driver.GetConfig([path])
#     assert result_config is not None
#     LOGGER.info(f"GetConfig result: {result_config}")

# netconf-console2 --host=10.30.7.7 --port=2023 --tcp --edit-config edit_dscm_hub.xml

# def test_set_config_hub(get_driver_hub):
#     data = { 
#         "name": "channel-1",
#         "frequency": "195000000",
#         "target_output_power": "-3.0",
#         "operational_mode": "1",
#         "operation": "merge",
#         "digital_subcarriers_groups": [
#             { "group_id": 1, "digital-subcarrier-id": [{ "subcarrier-id": 1, "active": True}, ]},
#             { "group_id": 2, "digital-subcarrier-id": [{ "subcarrier-id": 2, "active": True}, ]},
#             { "group_id": 3, "digital-subcarrier-id": [{ "subcarrier-id": 3, "active": True}, ]},
#             { "group_id": 4, "digital-subcarrier-id": [{ "subcarrier-id": 4, "active": True}, ]},
#         ],
#     }
#     node = 'hub'
#     result_config = get_driver_hub.SetConfig([(node, data)])
#     assert result_config is not None
#     # LOGGER.info(f"SetConfig result: {result_config}")

# def test_set_config_leaf(get_driver_leaf):
#     data = { 
#         "operation": "merge",
#         "channels": 
#         [
#             {
#                 "name": "channel-1",
#                 "frequency": "195006250",
#                 "target_output_power": "-99.0",
#                 "operational_mode": "1",
#                 "digital_subcarriers_groups": 
#                 [{ "group_id": 1 }]
#             },
#             {
#                 "name": "channel-3",
#                 "frequency": "195018750",
#                 "target_output_power": "-99.0",
#                 "operational_mode": "1",
#                 "digital_subcarriers_groups": 
#                 [{ "group_id": 1 }]
#             },
#             {
#                 "name": "channel-5",
#                 "frequency": "195031250",
#                 "target_output_power": "-99.0",
#                 "operational_mode": "1",
#                 "digital_subcarriers_groups":
#                 [{ "group_id": 1 }]
#             }
#         ]
#     }
#     node = 'leaf'
#     result_config = get_driver_leaf.SetConfig([(node, data)])
#     assert result_config is not None
#     # LOGGER.info(f"SetConfig result: {result_config}")


# def test_dscm_netconf_hub(drivers):
#     path = '/components/component[name="channel-1"]/config'
#     data = json.dumps(
#         { "name": "channel-1",
#           "frequency": "195000000",
#           "target_output_power": "-3.0",
#           "operational_mode": "1",
#           }
#           )
#     config_to_set = [(path, data)]
#     result_config = drivers['DSCM1'].SetConfig(config_to_set)
#     assert result_config is not None
#     LOGGER.info(f"SetConfig result: {result_config}")

    

from common.tools.context_queries.Topology import get_topology
from common.proto.context_pb2 import TopologyId, ContextId
from .Fixtures import context_client
def test_get_and_remove_topology_context(context_client):
    response = get_topology(context_client = context_client, topology_uuid = "admin", context_uuid = "admin")
    LOGGER.info(f"Topology: {response}")
    assert response is not None
    # create context_id and topology_id from response
    context_id  = ContextId()
    context_id  = response.topology_id.context_id
    topology_id = TopologyId()
    topology_id = response.topology_id
    # Remove Topology
    topology_id.context_id.CopyFrom(context_id)
    response    = context_client.RemoveTopology(topology_id)
    LOGGER.info(f"Topology removed Sucessfully")
    # Remove Context
    response    = context_client.RemoveContext(context_id)
    LOGGER.info(f"Context removed Sucessfully")
