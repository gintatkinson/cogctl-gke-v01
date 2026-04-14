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


def get_hub_payload():
    """Example HUB format payload."""
    return {
        "name"               : "channel-1",
        "frequency"          : "195000000",
        "target_output_power": "-3.0",
        "operational_mode"   : "1",
        "operation"          : "merge",
        "digital_subcarriers_groups": [
            { "group_id": 1, "digital-subcarrier-id": [{ "subcarrier-id": 1, "active": True}, ]},
            { "group_id": 2, "digital-subcarrier-id": [{ "subcarrier-id": 2, "active": True}, ]},
            { "group_id": 3, "digital-subcarrier-id": [{ "subcarrier-id": 3, "active": True}, ]},
            { "group_id": 4, "digital-subcarrier-id": [{ "subcarrier-id": 4, "active": True}, ]},
        ],
    }


def get_leaf_payload():
    """Example LEAF format payload."""
    return {
        "operation": "merge",
        "channels": [
            {
                "name"                      : "channel-1",
                "frequency"                 : "195006250000000",
                "target_output_power"       : "-99.0",
                "operational_mode"          : "1",
                "digital_subcarriers_groups": [{ "group_id": 1 }]
            },
            {
                "name"                      : "channel-3",
                "frequency"                 : "195018750000000",
                "target_output_power"       : "-99.0",
                "operational_mode"          : "1",
                "digital_subcarriers_groups": [{ "group_id": 2 }]
            },
            {
                "name"                      : "channel-5",
                "frequency"                 : "195031250000000",
                "target_output_power"       : "-99.0",
                "operational_mode"          : "1",
                "digital_subcarriers_groups": [{ "group_id": 3 }]
            }
        ]
    }
