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

import logging
from typing import Dict, Any
from common.proto.pluggables_pb2 import PluggableConfig
from common.proto.context_pb2 import ConfigRule

LOGGER = logging.getLogger(__name__)


def create_config_rule_from_dict(config_rule_dict: Dict[str, Any]) -> ConfigRule:  # type: ignore
    config_rule = ConfigRule()
    config_rule.action                = config_rule_dict['action']
    config_rule.custom.resource_key   = config_rule_dict['custom']['resource_key']
    config_rule.custom.resource_value = config_rule_dict['custom']['resource_value']
    return config_rule


def translate_pluggable_config_to_netconf(
    pluggable_config: PluggableConfig,  # type: ignore
    component_name: str = "channel-1"           # Fallback if channel_name not provided (channel-1 for HUB and channel-1/3/5 for LEAF)
) -> Dict[str, Any]:
    """
    Translate PluggableConfig protobuf message to the format expected by NetConfDriver.
    Args:
        pluggable_config: PluggableConfig message containing DSC groups and subcarriers
        component_name: Fallback name if channel_name is not specified in config (default: "channel-1")
    Returns:
        Dictionary in the format expected by NetConfDriver templates:
    """
      
    if not pluggable_config or not pluggable_config.dsc_groups:
        LOGGER.warning("Empty pluggable config provided")
        return {
            "name": channel_name,
            "operation": "delete"
        }
    if hasattr(pluggable_config, 'channel_name') and pluggable_config.channel_name:
        channel_name = pluggable_config.channel_name
        LOGGER.debug(f"Using channel_name from PluggableConfig: {channel_name}")
    else:
        channel_name = component_name
        LOGGER.debug(f"Using fallback component_name: {channel_name}")
    
    if not hasattr(pluggable_config, 'center_frequency_mhz') or pluggable_config.center_frequency_mhz <= 0:
        raise ValueError("center_frequency_mhz is required and must be greater than 0 in PluggableConfig")
    center_frequency_mhz = int(pluggable_config.center_frequency_mhz)
    
    if not hasattr(pluggable_config, 'operational_mode') or pluggable_config.operational_mode <= 0:
        raise ValueError("operational_mode is required and must be greater than 0 in PluggableConfig")
    operational_mode = pluggable_config.operational_mode
    
    if not hasattr(pluggable_config, 'target_output_power_dbm'):
        raise ValueError("target_output_power_dbm is required in PluggableConfig")
    target_output_power = pluggable_config.target_output_power_dbm
    
    if not hasattr(pluggable_config, 'line_port'):
        raise ValueError("line_port is required in PluggableConfig")
    line_port = pluggable_config.line_port
    
    LOGGER.debug(f"Extracted config values: freq={center_frequency_mhz} MHz, "
                 f"op_mode={operational_mode}, power={target_output_power} dBm, line_port={line_port}")
    
    # Build digital subcarriers groups
    digital_sub_carriers_groups = []
    
    for group_dsc in pluggable_config.dsc_groups:
        group_dsc_data = {
            "digital_sub_carriers_group_id": group_dsc.id.group_index,
            "digital_sub_carrier_id": []
        }
        
        for subcarrier in group_dsc.subcarriers:
            # Only subcarrier_index and active status are needed for Jinja2 template
            subcarrier_data = {
                "sub_carrier_id": subcarrier.id.subcarrier_index,
                "active": "true" if subcarrier.active else "false"
            }
            group_dsc_data["digital_sub_carrier_id"].append(subcarrier_data)
        
        digital_sub_carriers_groups.append(group_dsc_data)
    
    # Build the final configuration dictionary
    config = {
        "name": channel_name,
        "frequency": center_frequency_mhz,
        "operational_mode": operational_mode, 
        "target_output_power": target_output_power,
        "digital_sub_carriers_group": digital_sub_carriers_groups
    }
    
    LOGGER.info(f"Translated pluggable config to NETCONF format: component={channel_name}, "
                f"frequency={center_frequency_mhz} MHz, groups={len(digital_sub_carriers_groups)}")
    
    return config
