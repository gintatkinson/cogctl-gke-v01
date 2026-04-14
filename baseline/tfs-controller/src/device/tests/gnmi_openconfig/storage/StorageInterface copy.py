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

import re
from typing import Dict, List, Tuple
from .Tools import compose_resources

PREFIX = r'^\/interface\[([^\]]+)\]'
RE_RESKEY_INTERFACE    = re.compile(PREFIX + r'$')
RE_RESKEY_ETHERNET     = re.compile(PREFIX + r'\/ethernet$')
RE_RESKEY_SUBINTERFACE = re.compile(PREFIX + r'\/subinterface\[([^\]]+)\]$')
#RE_RESKEY_IPV4_ADDRESS = re.compile(PREFIX + r'\/subinterface\[([^\]]+)\]\/ipv4\[([^\]]+)\]$')

class Interfaces:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/interface[{:s}]', ['name', 'type', 'admin-status', 'oper-status', 'management', 'mtu', 'ifindex',
                              'hardware-port', 'transceiver']),
        ('/interface[{:s}]/ethernet', ['port-speed', 'negotiated-port-speed', 'mac-address', 'hw-mac-address']),
    ]

    def __init__(self) -> None:
        self._items : Dict[str, Dict] = dict()

    def add(self, if_name : str, resource_value : Dict) -> None:
        item = self._items.setdefault(if_name, dict())
        item['name'] = if_name
        for _, field_names in Interfaces.STRUCT:
            field_names = set(field_names)
            item.update({k:v for k,v in resource_value.items() if k in field_names})

    def get(self, if_name : str) -> Dict:
        return self._items.get(if_name)

    def remove(self, if_name : str) -> None:
        self._items.pop(if_name, None)
    
    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, Interfaces.STRUCT)

class SubInterfaces:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/interface[{:s}]/subinterface[{:d}]', ['index']),
    ]

    def __init__(self) -> None:
        self._items : Dict[Tuple[str, int], Dict] = dict()

    def add(self, if_name : str, subif_index : int) -> None:
        item = self._items.setdefault((if_name, subif_index), dict())
        item['index'] = subif_index

    def get(self, if_name : str, subif_index : int) -> Dict:
        return self._items.get((if_name, subif_index))

    def remove(self, if_name : str, subif_index : int) -> None:
        self._items.pop((if_name, subif_index), None)
    
    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, SubInterfaces.STRUCT)

class IPv4Addresses:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/interface[{:s}]/subinterface[{:d}]', ['index', 'address_ip', 'address_prefix', 'origin']),
    ]

    def __init__(self) -> None:
        self._items : Dict[Tuple[str, int], Dict] = dict()

    def add(self, if_name : str, subif_index : int, ipv4_address : str, resource_value : Dict) -> None:
        item = self._items.setdefault((if_name, subif_index), dict())
        item['index'         ] = subif_index
        item['address_ip'    ] = ipv4_address
        item['origin'        ] = resource_value.get('origin')
        item['address_prefix'] = resource_value.get('prefix')

    def get(self, if_name : str, subif_index : int, ipv4_address : str) -> Dict:
        return self._items.get((if_name, subif_index))

    def remove(self, if_name : str, subif_index : int, ipv4_address : str) -> None:
        self._items.pop((if_name, subif_index), None)

    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, IPv4Addresses.STRUCT)

class StorageInterface:
    def __init__(self) -> None:
        self.interfaces     = Interfaces()
        self.subinterfaces  = SubInterfaces()
        self.ipv4_addresses = IPv4Addresses()

    def populate(self, resources : List[Tuple[str, Dict]]) -> None:
        for resource_key, resource_value in resources:
            match = RE_RESKEY_INTERFACE.match(resource_key)
            if match is not None:
                self.interfaces.add(match.group(1), resource_value)
                continue

            match = RE_RESKEY_ETHERNET.match(resource_key)
            if match is not None:
                self.interfaces.add(match.group(1), resource_value)
                continue

            match = RE_RESKEY_SUBINTERFACE.match(resource_key)
            if match is not None:
                self.subinterfaces.add(match.group(1), int(match.group(2)))
                address_ip = resource_value.get('address_ip')
                self.ipv4_addresses.add(match.group(1), int(match.group(2)), address_ip, resource_value)
                continue

            #match = RE_RESKEY_IPV4_ADDRESS.match(resource_key)
            #if match is not None:
            #    self.ipv4_addresses.add(match.group(1), int(match.group(2)), match.group(3), resource_value)
            #    continue

            MSG = 'Unhandled Resource Key: {:s} => {:s}'
            raise Exception(MSG.format(str(resource_key), str(resource_value)))

    def get_expected_config(self) -> List[Tuple[str, Dict]]:
        expected_config = list()
        expected_config.extend(self.interfaces.compose_resources())
        #expected_config.extend(self.subinterfaces.compose_resources())
        expected_config.extend(self.ipv4_addresses.compose_resources())
        return expected_config
