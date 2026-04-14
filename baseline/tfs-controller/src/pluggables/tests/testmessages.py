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

import uuid
from typing import Optional, List, Dict, Any
from common.proto import pluggables_pb2 

###########################
# CreatePluggableRequest
###########################

def create_pluggable_request(
    device_uuid: Optional[str] = None,
    preferred_pluggable_index: Optional[int] = None,
    with_initial_config: bool = False
) -> pluggables_pb2.CreatePluggableRequest:  # pyright: ignore[reportInvalidTypeForm]
    """
    Create a CreatePluggableRequest message.
    
    Args:
        device_uuid: UUID of the device. If None, generates a random UUID.
        preferred_pluggable_index: Preferred index for the pluggable. If None, not set.
        with_initial_config: If True, includes initial configuration.
    
    Returns:
        CreatePluggableRequest message
    """
    _request = pluggables_pb2.CreatePluggableRequest()
    
    # Set device ID
    if device_uuid is None:
        device_uuid = str(uuid.uuid4())
    _request.device.device_uuid.uuid = device_uuid
    
    # Set preferred pluggable index if provided
    if preferred_pluggable_index is not None:
        _request.preferred_pluggable_index = preferred_pluggable_index
    
    # Add initial configuration if requested
    if with_initial_config:
        _request.initial_config.id.device.device_uuid.uuid = device_uuid
        _request.initial_config.id.pluggable_index = preferred_pluggable_index or 0
        
        # Set top-level PluggableConfig fields
        _request.initial_config.center_frequency_mhz = 193100000  # 193.1 THz in MHz
        _request.initial_config.operational_mode = 1  # Operational mode
        _request.initial_config.target_output_power_dbm = -10.0  # Target output power
        _request.initial_config.line_port = 1  # Line port number
        _request.initial_config.channel_name = "channel-1"  # Channel name for component
        
        # Add sample DSC group configuration
        dsc_group = _request.initial_config.dsc_groups.add()
        dsc_group.id.pluggable.device.device_uuid.uuid = device_uuid
        dsc_group.id.pluggable.pluggable_index = preferred_pluggable_index or 0
        dsc_group.id.group_index = 0
        dsc_group.group_size = 4
        dsc_group.group_capacity_gbps = 400.0
        dsc_group.subcarrier_spacing_mhz = 75.0
        
        # Add sample subcarrier configurations
        for i in range(2):
            subcarrier = dsc_group.subcarriers.add()
            subcarrier.id.group.pluggable.device.device_uuid.uuid = device_uuid
            subcarrier.id.group.pluggable.pluggable_index = preferred_pluggable_index or 0
            subcarrier.id.group.group_index = 0
            subcarrier.id.subcarrier_index = i
            subcarrier.active = True
            subcarrier.target_output_power_dbm = -10.0
            subcarrier.center_frequency_hz = 193100000000000 + (i * 75000000)  # 193.1 THz + spacing
            subcarrier.symbol_rate_baud = 64000000000  # 64 GBaud
    
    return _request


###########################
# ListPluggablesRequest
###########################

def create_list_pluggables_request(
    device_uuid: Optional[str] = None,
    view_level: pluggables_pb2.View = pluggables_pb2.VIEW_FULL  # pyright: ignore[reportInvalidTypeForm]
) -> pluggables_pb2.ListPluggablesRequest:  # pyright: ignore[reportInvalidTypeForm]
    """
    Create a ListPluggablesRequest message.
    
    Args:
        device_uuid: UUID of the device to filter by. If None, generates a random UUID.
        view_level: View level (VIEW_CONFIG, VIEW_STATE, VIEW_FULL, VIEW_UNSPECIFIED)
    
    Returns:
        ListPluggablesRequest message
    """
    _request = pluggables_pb2.ListPluggablesRequest()
    
    if device_uuid is None:
        device_uuid = "9bbf1937-db9e-45bc-b2c6-3214a9d42157"
        # device_uuid = str(uuid.uuid4())
    _request.device.device_uuid.uuid = device_uuid
    _request.view_level = view_level
    
    return _request


###########################
# GetPluggableRequest
###########################

def create_get_pluggable_request(
    device_uuid: str,
    pluggable_index: int,
    view_level: pluggables_pb2.View = pluggables_pb2.VIEW_FULL  # pyright: ignore[reportInvalidTypeForm]
) -> pluggables_pb2.GetPluggableRequest:  # pyright: ignore[reportInvalidTypeForm]
    """
    Create a GetPluggableRequest message.
    
    Args:
        device_uuid: UUID of the device
        pluggable_index: Index of the pluggable
        view_level: View level (VIEW_CONFIG, VIEW_STATE, VIEW_FULL, VIEW_UNSPECIFIED)
    
    Returns:
        GetPluggableRequest message
    """
    _request = pluggables_pb2.GetPluggableRequest()
    _request.id.device.device_uuid.uuid = device_uuid
    _request.id.pluggable_index = pluggable_index
    _request.view_level = view_level
    return _request


###########################
# DeletePluggableRequest
###########################

# TODO: Both leaf and hub have a same jinja template for deleting pluggable config.
# The difference lies in the component name (channel-1 for hub, channel-1/3/5 for leaf).

def create_delete_pluggable_request(
    device_uuid: str,
    pluggable_index: int
) -> pluggables_pb2.DeletePluggableRequest:  # pyright: ignore[reportInvalidTypeForm]
    """
    Create a DeletePluggableRequest message.
    
    Args:
        device_uuid: UUID of the device
        pluggable_index: Index of the pluggable
    
    Returns:
        DeletePluggableRequest message
    """
    _request = pluggables_pb2.DeletePluggableRequest()
    _request.id.device.device_uuid.uuid = device_uuid
    _request.id.pluggable_index = pluggable_index
    
    return _request


###########################
# ConfigurePluggableRequest
###########################

def create_configure_pluggable_request(
    device_uuid: str,
    pluggable_index: int,
    update_mask_paths: Optional[list] = None,
    view_level: pluggables_pb2.View = pluggables_pb2.VIEW_FULL,  # pyright: ignore[reportInvalidTypeForm]
    apply_timeout_seconds: int = 30,
    parameters: Optional[List[Dict[str, Any]]] = [],
) -> pluggables_pb2.ConfigurePluggableRequest:                      # pyright: ignore[reportInvalidTypeForm]
    """
    Create a ConfigurePluggableRequest message.
    
    Args:
        device_uuid: UUID of the device
        pluggable_index: Index of the pluggable
        update_mask_paths: List of field paths to update. If None, updates all fields.
        view_level: View level for response
        apply_timeout_seconds: Timeout in seconds for applying configuration
    
    Returns:
        ConfigurePluggableRequest message
    """
    _request = pluggables_pb2.ConfigurePluggableRequest()
    
    # Set pluggable configuration
    _request.config.id.device.device_uuid.uuid = device_uuid
    _request.config.id.pluggable_index         = pluggable_index
    
    # Set top-level PluggableConfig fields
    _request.config.center_frequency_mhz       = 193100000  # 193.1 THz in MHz
    _request.config.operational_mode           = 1  # Operational mode
    _request.config.target_output_power_dbm    = -10.0  # Target output power
    _request.config.line_port                  = 1  # Line port number
    _request.config.channel_name               = "channel-1"  # Channel name for component
    
    # Add DSC group configuration
    group_1 = _request.config.dsc_groups.add()
    group_1.id.pluggable.device.device_uuid.uuid = device_uuid
    group_1.id.pluggable.pluggable_index         = pluggable_index
    group_1.id.group_index                       = 0
    group_1.group_size                           = 2
    group_1.group_capacity_gbps                  = 400.0
    group_1.subcarrier_spacing_mhz               = 75.0
    
    # Add digital-subcarrier configuration (to group group_1)
    subcarrier_1 = group_1.subcarriers.add()
    subcarrier_1.id.group.pluggable.device.device_uuid.uuid = device_uuid
    subcarrier_1.id.group.pluggable.pluggable_index         = pluggable_index
    subcarrier_1.id.group.group_index                       = 0
    subcarrier_1.id.subcarrier_index                        = 0
    subcarrier_1.active                                     = True
    subcarrier_1.target_output_power_dbm                    = -10.0
    subcarrier_1.center_frequency_hz                        = 193100000000000  # 193.1 THz
    subcarrier_1.symbol_rate_baud                           = 64000000000  # 64 GBaud
    
    # Add another digital-subcarrier configuration (to group group_1)
    subcarrier_2 = group_1.subcarriers.add()
    subcarrier_2.id.group.pluggable.device.device_uuid.uuid = device_uuid
    subcarrier_2.id.group.pluggable.pluggable_index         = pluggable_index
    subcarrier_2.id.group.group_index                       = 0
    subcarrier_2.id.subcarrier_index                        = 1
    subcarrier_2.active                                     = True
    subcarrier_2.target_output_power_dbm                    = -10.0
    subcarrier_2.center_frequency_hz                        = 193100075000000  # 193.175 THz
    subcarrier_2.symbol_rate_baud                           = 64000000000  # 64 GBaud

    # Set update mask if provided
    if update_mask_paths:
        _request.update_mask.paths.extend(update_mask_paths)
    
    _request.view_level = view_level
    _request.apply_timeout_seconds = apply_timeout_seconds
    
    return _request
