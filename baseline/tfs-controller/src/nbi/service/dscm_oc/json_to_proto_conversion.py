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

"""
Helper functions to convert JSON payload from RESTCONF to Pluggables proto messages.
"""

from typing import Dict, Any
from common.proto import pluggables_pb2


def json_to_get_pluggable_request(
    device_uuid: str,
    pluggable_index: int = -1,
    view_level: pluggables_pb2.View = pluggables_pb2.VIEW_FULL                                                            # pyright: ignore[reportInvalidTypeForm]
) -> pluggables_pb2.GetPluggableRequest:                                                                                  # pyright: ignore[reportInvalidTypeForm]
    """
    Create a GetPluggableRequest proto message.
    Args:
        device_uuid: UUID of the device
        pluggable_index: Index of the pluggable
        view_level: View level (VIEW_CONFIG, VIEW_STATE, VIEW_FULL, VIEW_UNSPECIFIED)
    Returns:
        GetPluggableRequest proto message
    """
    request = pluggables_pb2.GetPluggableRequest()
    request.id.device.device_uuid.uuid = device_uuid                                                                      # type: ignore[attr-defined]
    request.id.pluggable_index         = pluggable_index                                                                  # type: ignore[attr-defined]
    request.view_level                 = view_level                                                                       # type: ignore[attr-defined]
    return request


def json_to_list_pluggables_request(
    device_uuid: str,
    view_level: pluggables_pb2.View = pluggables_pb2.VIEW_FULL                                                            # pyright: ignore[reportInvalidTypeForm]
) -> pluggables_pb2.ListPluggablesRequest:                                                                                # pyright: ignore[reportInvalidTypeForm]
    """
    Create a ListPluggablesRequest proto message.
    Args:
        device_uuid: UUID of the device to filter by
        view_level: View level (VIEW_CONFIG, VIEW_STATE, VIEW_FULL, VIEW_UNSPECIFIED)
    Returns:
        ListPluggablesRequest proto message
    """
    request = pluggables_pb2.ListPluggablesRequest()
    request.device.device_uuid.uuid = device_uuid                                                                         # type: ignore[attr-defined]
    request.view_level              = view_level                                                                          # type: ignore[attr-defined]
    return request


def json_to_delete_pluggable_request(
    device_uuid: str,
    pluggable_index: int = -1
) -> pluggables_pb2.DeletePluggableRequest:                                                                               # pyright: ignore[reportInvalidTypeForm]
    """
    Create a DeletePluggableRequest proto message.
    Args:
        device_uuid: UUID of the device
        pluggable_index: Index of the pluggable
    Returns:
        DeletePluggableRequest proto message
    """
    request = pluggables_pb2.DeletePluggableRequest()
    request.id.device.device_uuid.uuid = device_uuid                                                                      # type: ignore[attr-defined]
    request.id.pluggable_index         = pluggable_index                                                                  # type: ignore[attr-defined]
    return request


def json_to_create_pluggable_request(
    device_uuid: str,
    initial_config: Dict[str, Any],
    preferred_pluggable_index: int = -1
) -> pluggables_pb2.CreatePluggableRequest:                                                                               # pyright: ignore[reportInvalidTypeForm]
    """
    Convert JSON initial_config to CreatePluggableRequest proto message.
    Args:
        device_uuid: UUID of the device
        initial_config: JSON initial_config from RESTCONF request
        preferred_pluggable_index: Preferred pluggable slot index (-1 for auto)
    Returns:
        CreatePluggableRequest proto message
    """
    request = pluggables_pb2.CreatePluggableRequest()
    request.device.device_uuid.uuid   = device_uuid                                                                       # type: ignore[attr-defined]
    request.preferred_pluggable_index = preferred_pluggable_index                                                         # type: ignore[attr-defined]
    
    # If initial_config contains configuration, add it as initial_config
    if initial_config:
        request.initial_config.id.device.device_uuid.uuid = device_uuid                                                   # type: ignore[attr-defined]
        request.initial_config.id.pluggable_index         = preferred_pluggable_index                                     # type: ignore[attr-defined]
        
        if "digital_subcarriers_groups" in initial_config:    # (HUB format)
            _add_dsc_groups_from_hub_format(
                request.initial_config, device_uuid, preferred_pluggable_index, initial_config)                           # type: ignore[attr-defined]
        elif "channels" in initial_config:                    # (LEAF format)
            _add_dsc_groups_from_leaf_format(
                request.initial_config, device_uuid, preferred_pluggable_index, initial_config)                           # type: ignore[attr-defined]
    return request


def json_to_configure_pluggable_request(
    device_uuid: str,
    payload: Dict[str, Any],
    pluggable_index: int = -1,
    view_level: pluggables_pb2.View = pluggables_pb2.VIEW_FULL,                                                           # pyright: ignore[reportInvalidTypeForm]
    apply_timeout_seconds: int = 30
) -> pluggables_pb2.ConfigurePluggableRequest:                                                                            # pyright: ignore[reportInvalidTypeForm]
    """
    Convert JSON payload to ConfigurePluggableRequest proto message.
    Args:
        device_uuid: UUID of the device
        pluggable_index: Index of the pluggable to configure
        payload: JSON payload from RESTCONF request
        view_level: View level for response
        apply_timeout_seconds: Timeout in seconds for applying configuration
    Returns:
        ConfigurePluggableRequest proto message
    """
    request = pluggables_pb2.ConfigurePluggableRequest()
    request.config.id.device.device_uuid.uuid = device_uuid                                                               # type: ignore[attr-defined]
    request.config.id.pluggable_index         = pluggable_index                                                           # type: ignore[attr-defined]
    request.view_level                        = view_level                                                                # type: ignore[attr-defined]
    request.apply_timeout_seconds             = apply_timeout_seconds                                                     # type: ignore[attr-defined]
    
    if "digital_subcarriers_groups" in payload:     # (HUB format)
        _add_dsc_groups_from_hub_format(
            request.config, device_uuid, pluggable_index, payload)                                                        # type: ignore[attr-defined]
    elif "channels" in payload:                     # (LEAF format)
        _add_dsc_groups_from_leaf_format(
            request.config, device_uuid, pluggable_index, payload)                                                        # type: ignore[attr-defined]
    return request


def _add_dsc_groups_from_hub_format(
    config: pluggables_pb2.DigitalSubcarrierGroupConfig,                                                                  # pyright: ignore[reportInvalidTypeForm]
    device_uuid: str,
    pluggable_index: int,
    payload: Dict[str, Any]
) -> None:
    """
    Add DSC groups from HUB format JSON payload.
    """
    dsc_groups = payload.get("digital_subcarriers_groups", [])
    
    for group_data in dsc_groups:
        group_id = group_data.get("group_id", 0)
        
        dsc_group = config.dsc_groups.add()                                                                               # type: ignore[attr-defined]
        dsc_group.id.pluggable.device.device_uuid.uuid = device_uuid                                                      # type: ignore[attr-defined]
        dsc_group.id.pluggable.pluggable_index         = pluggable_index                                                  # type: ignore[attr-defined]
        dsc_group.id.group_index                       = group_id                                                         # type: ignore[attr-defined]
        
        # Set group parameters from payload
        # For HUB, these are at the top level
        dsc_group.group_capacity_gbps     = 400.0                                                                         # type: ignore[attr-defined]  # Default
        dsc_group.subcarrier_spacing_mhz  = 75.0                                                                          # type: ignore[attr-defined]  # Default
        
        # Process digital subcarriers
        subcarrier_list       = group_data.get("digital-subcarrier-id", [])
        dsc_group.group_size  = len(subcarrier_list)                                                                      # type: ignore[attr-defined]
        
        for subcarrier_data in subcarrier_list:
            subcarrier_id = subcarrier_data.get("subcarrier-id", 0)
            is_active = subcarrier_data.get("active", False)
            
            subcarrier = dsc_group.subcarriers.add()                                                                      # type: ignore[attr-defined]
            subcarrier.id.group.pluggable.device.device_uuid.uuid = device_uuid                                           # type: ignore[attr-defined]
            subcarrier.id.group.pluggable.pluggable_index         = pluggable_index                                       # type: ignore[attr-defined]
            subcarrier.id.group.group_index                       = group_id                                              # type: ignore[attr-defined]
            subcarrier.id.subcarrier_index                        = subcarrier_id                                         # type: ignore[attr-defined]
            subcarrier.active                                     = is_active                                             # type: ignore[attr-defined]
            
            # Set frequency and power from top-level payload
            if "frequency" in payload:
                subcarrier.center_frequency_hz = float(payload["frequency"])                                              # type: ignore[attr-defined]
            
            if "target_output_power" in payload:
                subcarrier.target_output_power_dbm = float(payload["target_output_power"])                                # type: ignore[attr-defined]
            
            # Default symbol rate
            subcarrier.symbol_rate_baud = 64000000000                                                                     # type: ignore[attr-defined]


def _add_dsc_groups_from_leaf_format(
    config: pluggables_pb2.DigitalSubcarrierGroupConfig,                                                                 # pyright: ignore[reportInvalidTypeForm]
    device_uuid: str,
    pluggable_index: int,
    payload: Dict[str, Any]
) -> None:
    """
    Add DSC groups from LEAF format JSON payload.
    """
    channels = payload.get("channels", [])
    
    for channel_idx, channel_data in enumerate(channels):
        dsc_groups = channel_data.get("digital_subcarriers_groups", [])
        
        for group_data in dsc_groups:
            group_id = group_data.get("group_id", channel_idx)
            
            # Create DSC group (protobuf repeated field operations)
            dsc_group = config.dsc_groups.add()                                                                           # type: ignore[attr-defined]
            dsc_group.id.pluggable.device.device_uuid.uuid = device_uuid                                                  # type: ignore[attr-defined]
            dsc_group.id.pluggable.pluggable_index         = pluggable_index                                              # type: ignore[attr-defined]
            dsc_group.id.group_index                       = group_id                                                     # type: ignore[attr-defined]
            
            # Set group parameters
            dsc_group.group_capacity_gbps     = 400.0                                                                     # type: ignore[attr-defined]  # Default
            dsc_group.subcarrier_spacing_mhz  = 75.0                                                                      # type: ignore[attr-defined]  # Default
            dsc_group.group_size              = 1                                                                         # type: ignore[attr-defined]  # Default for LEAF
            
            # Create a single subcarrier for this channel
            subcarrier = dsc_group.subcarriers.add()                                                                      # type: ignore[attr-defined]
            subcarrier.id.group.pluggable.device.device_uuid.uuid = device_uuid                                           # type: ignore[attr-defined]
            subcarrier.id.group.pluggable.pluggable_index         = pluggable_index                                       # type: ignore[attr-defined]
            subcarrier.id.group.group_index                       = group_id                                              # type: ignore[attr-defined]
            subcarrier.id.subcarrier_index                        = 0                                                     # type: ignore[attr-defined]
            subcarrier.active                                     = True                                                  # type: ignore[attr-defined]  # Default for LEAF channels
            
            # Set frequency and power from channel data
            if "frequency" in channel_data:
                subcarrier.center_frequency_hz = float(channel_data["frequency"])                                         # type: ignore[attr-defined]  # MHz to Hz
            
            if "target_output_power" in channel_data:
                subcarrier.target_output_power_dbm = float(channel_data["target_output_power"])                           # type: ignore[attr-defined]
            
            # Default symbol rate
            subcarrier.symbol_rate_baud = 64000000000                                                                     # type: ignore[attr-defined]  # 64 GBaud
