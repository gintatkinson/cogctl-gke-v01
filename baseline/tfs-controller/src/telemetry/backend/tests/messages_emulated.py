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
# Configure logging to ensure logs appear on the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_test_configuration():
    return {
            "config_rules": [
                {"action": 1, "custom": {"resource_key": "_connect/address" , "resource_value": "127.0.0.1"}},
                {"action": 1, "custom": {"resource_key": "_connect/port"    , "resource_value": 8080}},
                {"action": 1, "custom": {"resource_key": "_connect/settings", "resource_value": {
                    "endpoints": [
                        {"uuid": "eth0",   "type": "ethernet", "sample_types": [101, 102]},
                        {"uuid": "eth1",   "type": "ethernet", "sample_types": []},
                        {"uuid": "13/1/2", "type": "copper",   "sample_types": [101, 102, 201, 202]}
                    ]
                }}},
                {"action": 1, "custom": {"resource_key": "/interface[eth0]/settings", "resource_value": {
                    "name": "eth0", "enabled": True
                }}},
                {"action": 1, "custom": {"resource_key": "/interface[eth1]/settings", "resource_value": {
                    "name": "eth1", "enabled": False
                }}},
                {"action": 1, "custom": {"resource_key": "/interface[13/1/2]/settings", "resource_value": {
                    "name": "13/1/2", "enabled": True
                }}}
            ]
        }

def create_specific_config_keys():
    keys_to_return = ["_connect/settings/endpoints/eth1", "/interface/[13/1/2]/settings", "_connect/address"]
    return keys_to_return

def create_config_for_delete():
    keys_to_delete = ["_connect/settings/endpoints/eth0", "/interface/[eth1]", "_connect/port"]
    return keys_to_delete

def create_test_subscriptions():
    return [("_connect/settings/endpoints/eth1",   10, 2),
            ("_connect/settings/endpoints/13/1/2", 15, 3),
            ("_connect/settings/endpoints/eth0",   8,  2)]

def create_unscubscribe_subscriptions():
    return [("_connect/settings/endpoints/eth1",   10, 2),
            ("_connect/settings/endpoints/13/1/2", 15, 3),
            ("_connect/settings/endpoints/eth0",   8,  2)]
