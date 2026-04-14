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

from common.tools.object_factory.Device import (
    json_device_connect_rules, json_device_id, json_device_packetrouter_disabled)

DEVICE_OC_UUID     = 'DEV-UUID'   # populate the name of the device to test
DEVICE_OC_ADDRESS  = '127.0.0.1'  # populate the Netconf Server IP address of the device to test
DEVICE_OC_PORT     = 830          # populate the Netconf Server port of the device to test
DEVICE_OC_USERNAME = 'username'   # populate the Netconf Server username of the device to test
DEVICE_OC_PASSWORD = 'password'   # populate the Netconf Server password of the device to test
DEVICE_OC_TIMEOUT  = 15

DEVICE_OC_ID = json_device_id(DEVICE_OC_UUID)
DEVICE_OC    = json_device_packetrouter_disabled(DEVICE_OC_UUID)

DEVICE_OC_CONNECT_RULES = json_device_connect_rules(DEVICE_OC_ADDRESS, DEVICE_OC_PORT, {
    'username'       : DEVICE_OC_USERNAME,
    'password'       : DEVICE_OC_PASSWORD,
    'force_running'  : False,
    'hostkey_verify' : True,
    'look_for_keys'  : True,
    'allow_agent'    : True,
    'commit_per_rule': False,
    'device_params'  : {'name': 'default'},
    'manager_params' : {'timeout' : DEVICE_OC_TIMEOUT},
})


DEVICE_OC_CONFIG_RULES   = []           # populate your configuration rules to test
DEVICE_OC_DECONFIG_RULES = []           # populate your deconfiguration rules to test
