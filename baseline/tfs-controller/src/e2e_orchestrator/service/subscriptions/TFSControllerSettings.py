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


import json
from dataclasses import dataclass
from typing import Optional
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import ConfigActionEnum, DeviceEvent
from common.tools.context_queries.Device import get_device
from context.client.ContextClient import ContextClient


@dataclass
class TFSControllerSettings:
    device_uuid  : str
    device_type  : DeviceTypeEnum
    nbi_address  : str
    nbi_port     : int
    nbi_username : str
    nbi_password : str


SELECTED_DEVICE_TYPES = {
    DeviceTypeEnum.TERAFLOWSDN_CONTROLLER.value
}


def get_tfs_controller_settings(
    context_client : ContextClient, device_event : DeviceEvent
) -> Optional[TFSControllerSettings]:
    device_uuid = device_event.device_id.device_uuid.uuid
    device = get_device(
        context_client, device_uuid, rw_copy=False,
        include_endpoints=False, include_config_rules=True,
        include_components=False
    )
    device_type = device.device_type
    if device_type not in SELECTED_DEVICE_TYPES: return None

    connect_rules = dict()
    for config_rule in device.device_config.config_rules:
        if config_rule.action != ConfigActionEnum.CONFIGACTION_SET: continue
        if config_rule.WhichOneof('config_rule') != 'custom': continue
        if not config_rule.custom.resource_key.startswith('_connect/'): continue
        connect_attribute = config_rule.custom.resource_key.replace('_connect/', '')
        if connect_attribute == 'settings':
            settings = json.loads(config_rule.custom.resource_value)
            for field in ['username', 'password']:
                connect_rules[field] = settings[field]
        else:
            connect_rules[connect_attribute] = config_rule.custom.resource_value

    return TFSControllerSettings(
        device_uuid  = device_uuid,
        device_type  = device_type,
        nbi_address  = str(connect_rules['address' ]),
        nbi_port     = int(connect_rules['port'    ]),
        nbi_username = str(connect_rules['username']),
        nbi_password = str(connect_rules['password']),
    )
