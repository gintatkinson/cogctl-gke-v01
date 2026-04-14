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

import copy, logging
from typing import Dict, Any, Optional
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME
from common.tools.object_factory.Context import json_context, json_context_id
from common.tools.object_factory.Topology import json_topology, json_topology_id
from common.proto.context_pb2 import Device
from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_id, json_device_packetrouter_disabled
)

LOGGER = logging.getLogger(__name__)


# ----- Context --------------------------------------------------------------------------------------------------------
CONTEXT_ID = json_context_id(DEFAULT_CONTEXT_NAME)
CONTEXT    = json_context(DEFAULT_CONTEXT_NAME)


# ----- Topology -------------------------------------------------------------------------------------------------------
TOPOLOGY_ID = json_topology_id(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)
TOPOLOGY    = json_topology(DEFAULT_TOPOLOGY_NAME, context_id=CONTEXT_ID)


# ----- Hub Device Configuration ---------------------------------------------

DEVICE_HUB_UUID = 'hub-device-uuid-001'
DEVICE_HUB_ADDRESS = '10.30.7.7'
DEVICE_HUB_PORT = 2023
DEVICE_HUB_USERNAME = 'admin'
DEVICE_HUB_PASSWORD = 'admin'
DEVICE_HUB_TIMEOUT = 15

DEVICE_HUB_ID = json_device_id(DEVICE_HUB_UUID)
DEVICE_HUB = json_device_packetrouter_disabled(DEVICE_HUB_UUID, name='Hub-Router')

DEVICE_HUB_CONNECT_RULES = json_device_connect_rules(DEVICE_HUB_ADDRESS, DEVICE_HUB_PORT, {
    'username': DEVICE_HUB_USERNAME,
    'password': DEVICE_HUB_PASSWORD,
    'force_running': False,
    'hostkey_verify': False,
    'look_for_keys': False,
    'allow_agent': False,
    'commit_per_rule': False,
    'device_params': {'name': 'default'},
    'manager_params': {'timeout': DEVICE_HUB_TIMEOUT},
})

# ----- Leaf Device Configuration --------------------------------------------

DEVICE_LEAF_UUID = 'leaf-device-uuid-001'
DEVICE_LEAF_ADDRESS = '10.30.7.8'
DEVICE_LEAF_PORT = 2023
DEVICE_LEAF_USERNAME = 'admin'
DEVICE_LEAF_PASSWORD = 'admin'
DEVICE_LEAF_TIMEOUT = 15

DEVICE_LEAF_ID = json_device_id(DEVICE_LEAF_UUID)
DEVICE_LEAF = json_device_packetrouter_disabled(DEVICE_LEAF_UUID, name='Leaf-Router')

DEVICE_LEAF_CONNECT_RULES = json_device_connect_rules(DEVICE_LEAF_ADDRESS, DEVICE_LEAF_PORT, {
    'username': DEVICE_LEAF_USERNAME,
    'password': DEVICE_LEAF_PASSWORD,
    'force_running': False,
    'hostkey_verify': False,
    'look_for_keys': False,
    'allow_agent': False,
    'commit_per_rule': False,
    'device_params': {'name': 'default'},
    'manager_params': {'timeout': DEVICE_LEAF_TIMEOUT},
})

# ----- Complete Device Objects with Connect Rules --------------------------

def get_device_hub_with_connect_rules() -> Device:
    """
    Create a complete Hub device with connection rules.
    
    Returns:
        Device protobuf object ready to be added to Context
    """
    device_dict = copy.deepcopy(DEVICE_HUB)
    device_dict['device_config']['config_rules'].extend(DEVICE_HUB_CONNECT_RULES)
    return Device(**device_dict)


def get_device_leaf_with_connect_rules() -> Device:
    """
    Create a complete Leaf device with connection rules.
    
    Returns:
        Device protobuf object ready to be added to Context
    """
    device_dict = copy.deepcopy(DEVICE_LEAF)
    device_dict['device_config']['config_rules'].extend(DEVICE_LEAF_CONNECT_RULES)
    return Device(**device_dict)

# ----- Device Connection Mapping --------------------------------------------

DEVICES_CONNECTION_INFO = {
    'hub': {
        'uuid': DEVICE_HUB_UUID,
        'address': DEVICE_HUB_ADDRESS,
        'port': DEVICE_HUB_PORT,
        'settings': {},
        'username': DEVICE_HUB_USERNAME,
        'password': DEVICE_HUB_PASSWORD
    },
    'leaf': {
        'uuid': DEVICE_LEAF_UUID,
        'address': DEVICE_LEAF_ADDRESS,
        'port': DEVICE_LEAF_PORT,
        'settings': {},
        'username': DEVICE_LEAF_USERNAME,
        'password': DEVICE_LEAF_PASSWORD
    },
}


def get_device_connection_info(device_uuid: str) -> Optional[Dict[str, Any]]:
    """
    Get device connection information for NETCONF driver.
    
    Args:
        device_uuid: UUID of the device
    
    Returns:
        Dictionary with connection info or None if not found
    """
    # Map device UUIDs to device types
    device_mapping = {
        DEVICE_HUB_UUID: 'hub',
        DEVICE_LEAF_UUID: 'leaf',
    }
    
    device_type = device_mapping.get(device_uuid)
    
    if device_type and device_type in DEVICES_CONNECTION_INFO:
        return DEVICES_CONNECTION_INFO[device_type]
    
    return None


def determine_node_identifier(device_uuid: str, pluggable_index: int) -> str:
    """
    Determine the node identifier (e.g., 'T2.1', 'T1.1', etc.) for the device.
    
    Args:
        device_uuid: UUID of the device
        pluggable_index: Index of the pluggable
    
    Returns:
        Node identifier string
    """
    conn_info = get_device_connection_info(device_uuid)
    
    if conn_info and conn_info['address'] == DEVICE_HUB_ADDRESS:
        return 'T2.1'  # Hub node
    elif conn_info and conn_info['address'] == DEVICE_LEAF_ADDRESS:
        # For multiple leaf nodes, use pluggable_index to differentiate
        return f'T1.{pluggable_index + 1}'
    else:
        return 'T1.1'  # Default
