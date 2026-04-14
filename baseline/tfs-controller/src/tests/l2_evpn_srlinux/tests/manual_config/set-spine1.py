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

from pygnmi.client import gNMIclient

host1 = {
    "ip_address": "172.20.20.101",
    "port": 57400,
    "username": "admin",
    "password": "NokiaSrl1!"
}

if __name__ == "__main__":
    with gNMIclient(
        target=(host1["ip_address"], host1["port"]),
        username=host1["username"], password=host1["password"],
        insecure=False
    ) as gc:
        updates = [
             ('/interface[name=ethernet-1/1]', { #interfaces
                "admin-state": "enable",
                "subinterface": [
                    {
                        "index": 0,
                        "ipv4": {
                            "admin-state": "enable",
                            "address": [
                                {
                                    "ip-prefix": "192.168.11.2/30"
                                }
                            ]
                        }
                    }
                ]
            }),

            ('/interface[name=ethernet-1/2]', {
                "admin-state": "enable",
                "subinterface": [
                    {
                        "index": 0,
                        "ipv4": {
                            "admin-state": "enable",
                            "address": [
                                {
                                    "ip-prefix": "192.168.12.2/30"
                                }
                            ]
                        }
                    }
                ]
            }),
            ('/network-instance[name=default]', { #default network instance
                 "interface": [
                    {"name": "ethernet-1/1.0"},
                    {"name": "ethernet-1/2.0"},
                    {"name": "system0.0"}
                ],
                 "name": "default",
                    "protocols": {
                        "bgp": {
                            "afi-safi": [
                             {
                                 "admin-state": "enable",
                                 "afi-safi-name": "ipv4-unicast"
                             }
                         ],
                        "autonomous-system": 201,
                            "group": [
                                {
                                 "export-policy": "all",
                                 "group-name": "eBGP-underlay",
                                 "import-policy": "all",
                                }
                             ],
                         "neighbor": [
                             {
                                "peer-address": "192.168.11.1",
                                "peer-as": 101,
                                "peer-group": "eBGP-underlay",
                             },
                             {
                                "peer-address": "192.168.12.1",
                                "peer-as": 102,
                                "peer-group": "eBGP-underlay",
                                }
                            ],
                        "router-id": "10.0.1.1"
                     }
                 },
                      
                 }),
            
            ('/interface[name=system0]', {
                    "name": "system0",
                     "admin-state": "enable",
                     "subinterface": [
                        {
                             "index": 0,
                             "ipv4": {
                             "admin-state": "enable",
                             "address": [
                                {
                                    "ip-prefix": "10.0.1.1/32"
                                }
                            ]
                        }
                    }
                ]
            }
        ),

            ('/routing-policy', {  #routing policy 
                "policy": {
                    "name": "all", 
                    "default-action": {
                        "policy-result": "accept"
                    }
                }
            }
        ),


        ]

        result = gc.set(update=updates, encoding='json_ietf')
        print(result)
