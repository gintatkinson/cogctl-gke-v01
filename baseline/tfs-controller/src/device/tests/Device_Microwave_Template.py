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

from common.tools.object_factory.ConfigRule import json_config_rule_delete, json_config_rule_set
from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_id, json_device_microwave_disabled)

DEVICE_MICROWAVE_UUID    = 'DEVICE-MICROWAVE'   # populate 'device-uuid' of the MICROWAVE SMDC server
DEVICE_MICROWAVE_ADDRESS = '127.0.0.1'          # populate 'address' of the MICROWAVE SMDC server
DEVICE_MICROWAVE_PORT    = 8443                 # populate 'port' of the MICROWAVE SMDC server
DEVICE_MICROWAVE_TIMEOUT = 120                  # populate 'timeout' of the MICROWAVE SMDC server

DEVICE_MICROWAVE_ID = json_device_id(DEVICE_MICROWAVE_UUID)
DEVICE_MICROWAVE    = json_device_microwave_disabled(DEVICE_MICROWAVE_UUID)

DEVICE_MICROWAVE_CONNECT_RULES = json_device_connect_rules(DEVICE_MICROWAVE_ADDRESS, DEVICE_MICROWAVE_PORT, {
    'timeout' : DEVICE_MICROWAVE_TIMEOUT,
})

DEVICE_MICROWAVE_CONFIG_RULES = [
    json_config_rule_set('/services/service[service_uuid]', {
        'uuid'       : 'service-uuid',      # populate 'service_name of the service to test
        'node_id_src': '172.26.60.243',     # populate 'node_id_src' of the service to test
        'tp_id_src'  : 9,                   # populate 'tp_id_src' of the service to test
        'node_id_dst': '172.26.60.244',     # populate 'node_id_dst' of the service to test
        'tp_id_dst'  : 9,                   # populate 'tp_id_dst' of the service to test
        'vlan_id'    : 121,                 # populate 'vlan_id' of the service to test
    })
]

DEVICE_MICROWAVE_DECONFIG_RULES = [
    json_config_rule_delete('/services/service[service-uuid]', {
        'uuid': 'service-uuid'              # populate 'service_name' of the service to test
    })
]
