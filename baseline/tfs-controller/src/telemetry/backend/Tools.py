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

from typing import Any, Dict
from common.proto.context_pb2 import DeviceConfig, ConfigActionEnum


def get_connect_rules(device_config : DeviceConfig) -> Dict[str, Any]:
    connect_rules = dict()
    for config_rule in device_config.config_rules:
        if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
        if config_rule.WhichOneof('config_rule') != 'custom': continue
        if not config_rule.custom.resource_key.startswith('_connect/'): continue
        connect_attribute = config_rule.custom.resource_key.replace('_connect/', '')
        connect_rules[connect_attribute] = config_rule.custom.resource_value
    return connect_rules

