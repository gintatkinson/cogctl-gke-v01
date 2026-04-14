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

# Ref: https://github.com/aristanetworks/openmgmt/blob/main/src/pygnmi/update.py
# Ref: https://github.com/aristanetworks/openmgmt/blob/main/src/pygnmi/delete.py
# Ref: https://yang.srlinux.dev/release/v23.3.2/

from pygnmi.client import gNMIclient

host = {
    "ip_address": "172.20.20.103",
    "port": 57400,
    "username": "admin",
    "password": "NokiaSrl1!"
}

if __name__ == "__main__":
    with gNMIclient(
        target=(host["ip_address"], host["port"]),
        username=host["username"], password=host["password"],
        insecure=False
    ) as gc:
        updates = [
            ('/interface[name=ethernet-1/49]',
             {
                 "admin-state": "enable",
                 "subinterface": [
                     {
                         "index": 0,
                         "ipv4": {
                             "admin-state": "enable",
                             "address": [
                                 {
                                     "ip-prefix": "192.168.12.1/30"
                                 }
                             ]
                         }
                     }
                 ]
             }
        ),
        ('/network-instance[name=default]',       
             {
                 "interface": [
                     {"name": "ethernet-1/49.0"},
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
                         "autonomous-system": 102,
                         "group": [
                             {
                                 "export-policy": "all",
                                 "group-name": "eBGP-underlay",
                                 "import-policy": "all",
                                 "peer-as": 201
                             },
                             {
                                 "afi-safi": [
                                     {
                                         "admin-state": "enable",
                                         "afi-safi-name": "evpn"
                                     },
                                     {
                                         "admin-state": "disable",
                                         "afi-safi-name": "ipv4-unicast"
                                     }
                                 ],
                                 "export-policy": "all",
                                 "group-name": "iBGP-overlay",
                                 "import-policy": "all",
                                 "local-as": {
                                     "as-number": 100
                                 },
                                 "peer-as": 100,
                                 "timers": {
                                     "minimum-advertisement-interval": 1
                                 }
                             }
                         ],
                         "neighbor": [
                             {
                                 "admin-state": "enable",
                                 "peer-address": "10.0.0.1",
                                 "peer-group": "iBGP-overlay",
                                 "transport": {
                                     "local-address": "10.0.0.2"
                                 }
                             },
                             {
                                 "peer-address": "192.168.12.2",
                                 "peer-group": "eBGP-underlay"
                             }
                         ],
                         "router-id": "10.0.0.2"
                     }
                 },
             }
             ),
            ('/routing-policy',
             {
                 "policy": [
                     {
                         "name": "all",
                         "default-action": {
                             "policy-result": "accept"
                         }
                     }
                 ]
             }
        ),    
            ('/interface[name=system0]',
             {
                 "name": "system0",
                 "admin-state": "enable",
                 "subinterface": [
                     {
                         "index": 0,
                         "ipv4": {
                             "admin-state": "enable",
                             "address": [
                                 {
                                     "ip-prefix": "10.0.0.2/32"
                                 }
                             ]
                         }
                     }
                 ]
             }
        ),      
           ('/interface[name=ethernet-1/1]',
             {
                 "vlan-tagging": True,
                 "subinterface": {
                     "index": 0,
                     "type": "bridged",
                     "admin-state": "enable",
                     "vlan": {
                         "encap": {
                             "untagged": {}
                         }
                     }
                 }
             }
        ),  
            ('/network-instance[name=vrf-1]',
             {
                 "name": "vrf-1",
                 "type": "mac-vrf",
                 "admin-state": "enable",
                 "interface": [
                     {"name": "ethernet-1/1.0"}
                 ],
                 "vxlan-interface": [
                     {"name": "vxlan1.1"}
                 ],
                 "protocols": {
                     "bgp-evpn": {
                         "bgp-instance": [
                             {
                                 "id": 1,
                                 "admin-state": "enable",
                                 "vxlan-interface": "vxlan1.1",
                                 "evi": 111
                             }
                         ]
                     },
                     "bgp-vpn": {
                         "bgp-instance": [
                             {
                                 "id": 1,
                                 "route-target": {
                                     "export-rt": "target:100:111",
                                     "import-rt": "target:100:111"
                                 }
                             }
                         ]
                     }
                 }
             }
             ),
            ('/tunnel-interface[name=vxlan1]',
             {"vxlan-interface": [
                 {
                     "index": "1",
                     "type": "bridged",
                     "ingress": {
                         "vni": 1
                        }
                     }
                ]
            }
         )
    ]

        result = gc.set(update=updates, encoding='json_ietf')
        print(result)    