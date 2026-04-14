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

PREFIX = r'^\/network\_instance\[([^\]]+)\]'
RE_RESKEY_NET_INST     = re.compile(PREFIX + r'$')
RE_RESKEY_INTERFACE    = re.compile(PREFIX + r'\/interface\[([^\]]+)\]$')
RE_RESKEY_PROTOCOL     = re.compile(PREFIX + r'\/protocol\[([^\]]+)\]$')
RE_RESKEY_PROTO_STATIC = re.compile(PREFIX + r'\/protocol\[([^\]]+)\]\/static\_routes\[([^\]]+)\]$')
RE_RESKEY_TABLE        = re.compile(PREFIX + r'\/table\[([^\,]+)\,([^\]]+)\]$')
RE_RESKEY_VLAN         = re.compile(PREFIX + r'\/vlan\[([^\]]+)\]$')

class NetworkInstances:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/network_instance[{:s}]', ['name', 'type']),
    ]

    def __init__(self) -> None:
        self._items : Dict[str, Dict] = dict()

    def add(self, ni_name : str, resource_value : Dict) -> None:
        item = self._items.setdefault(ni_name, dict())
        item['name'] = ni_name
        item['type'] = resource_value.get('type')

    def get(self, ni_name : str) -> Dict:
        return self._items.get(ni_name)

    def remove(self, ni_name : str) -> None:
        self._items.pop(ni_name, None)
    
    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, NetworkInstances.STRUCT)

class Interfaces:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/network_instance[{:s}]/interface[{:s}.{:d}]', ['name', 'id', 'if_name', 'sif_index']),
    ]

    def __init__(self) -> None:
        self._items : Dict[Tuple[str, str], Dict] = dict()

    def add(self, ni_name : str, if_name : str, sif_index : int) -> None:
        item = self._items.setdefault((ni_name, if_name, sif_index), dict())
        item['name'     ] = ni_name
        item['id'       ] = '{:s}.{:d}'.format(if_name, sif_index)
        item['if_name'  ] = if_name
        item['sif_index'] = sif_index

    def get(self, ni_name : str, if_name : str, sif_index : int) -> Dict:
        return self._items.get((ni_name, if_name, sif_index))

    def remove(self, ni_name : str, if_name : str, sif_index : int) -> None:
        self._items.pop((ni_name, if_name, sif_index), None)

    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, Interfaces.STRUCT)

class Protocols:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/network_instance[{:s}]/protocol[{:s}]', ['id', 'name']),
    ]

    def __init__(self) -> None:
        self._items : Dict[Tuple[str, str], Dict] = dict()

    def add(self, ni_name : str, protocol : str) -> None:
        item = self._items.setdefault((ni_name, protocol), dict())
        item['id'  ] = protocol
        item['name'] = protocol

    def get(self, ni_name : str, protocol : str) -> Dict:
        return self._items.get((ni_name, protocol))

    def remove(self, ni_name : str, protocol : str) -> None:
        self._items.pop((ni_name, protocol), None)

    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, Protocols.STRUCT)

class StaticRoutes:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/network_instance[{:s}]/protocol[{:s}]/static_routes[{:s}]', ['prefix', 'next_hops']),
    ]

    def __init__(self) -> None:
        self._items : Dict[Tuple[str, str, str], Dict] = dict()

    def add(self, ni_name : str, protocol : str, prefix : str, resource_value : Dict) -> None:
        item = self._items.setdefault((ni_name, protocol, prefix), dict())
        item['prefix'   ] = prefix
        item['next_hops'] = resource_value.get('next_hops')

    def get(self, ni_name : str, protocol : str, prefix : str) -> Dict:
        return self._items.get((ni_name, protocol, prefix))

    def remove(self, ni_name : str, protocol : str, prefix : str) -> None:
        self._items.pop((ni_name, protocol, prefix), None)

    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, StaticRoutes.STRUCT)

class Tables:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/network_instance[{:s}]/table[{:s},{:s}]', ['protocol', 'address_family']),
    ]

    def __init__(self) -> None:
        self._items : Dict[Tuple[str, str, str], Dict] = dict()

    def add(self, ni_name : str, protocol : str, address_family : str) -> None:
        item = self._items.setdefault((ni_name, protocol, address_family), dict())
        item['protocol'      ] = protocol
        item['address_family'] = address_family

    def get(self, ni_name : str, protocol : str, address_family : str) -> Dict:
        return self._items.get((ni_name, protocol, address_family))

    def remove(self, ni_name : str, protocol : str, address_family : str) -> None:
        self._items.pop((ni_name, protocol, address_family), None)

    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, Tables.STRUCT)

class Vlans:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/network_instance[{:s}]/vlan[{:d}]', ['vlan_id', 'name', 'members']),
    ]

    def __init__(self) -> None:
        self._items : Dict[Tuple[str, int], Dict] = dict()

    def add(self, ni_name : str, vlan_id : int, resource_value : Dict) -> None:
        item = self._items.setdefault((ni_name, vlan_id), dict())
        item['vlan_id'] = vlan_id
        item['name'   ] = resource_value.get('name')
        item['members'] = sorted(resource_value.get('members'))

    def get(self, ni_name : str, vlan_id : int) -> Dict:
        return self._items.get((ni_name, vlan_id))

    def remove(self, ni_name : str, vlan_id : int) -> None:
        self._items.pop((ni_name, vlan_id), None)

    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, Vlans.STRUCT)

class StorageNetworkInstance:
    def __init__(self) -> None:
        self.network_instances = NetworkInstances()
        self.interfaces        = Interfaces()
        self.protocols         = Protocols()
        self.protocol_static   = StaticRoutes()
        self.tables            = Tables()
        self.vlans             = Vlans()

    def populate(self, resources : List[Tuple[str, Dict]]) -> None:
        for resource_key, resource_value in resources:
            match = RE_RESKEY_NET_INST.match(resource_key)
            if match is not None:
                self.network_instances.add(match.group(1), resource_value)
                continue

            match = RE_RESKEY_INTERFACE.match(resource_key)
            if match is not None:
                if_id = match.group(2)
                if_id_parts = if_id.split('.')
                if_name = if_id_parts[0]
                sif_index = 0 if len(if_id_parts) == 1 else int(if_id_parts[1])
                self.interfaces.add(match.group(1), if_name, sif_index)
                continue

            match = RE_RESKEY_PROTOCOL.match(resource_key)
            if match is not None:
                self.protocols.add(match.group(1), match.group(2))
                continue

            match = RE_RESKEY_PROTO_STATIC.match(resource_key)
            if match is not None:
                self.protocol_static.add(match.group(1), match.group(2), match.group(3), resource_value)
                continue

            match = RE_RESKEY_TABLE.match(resource_key)
            if match is not None:
                self.tables.add(match.group(1), match.group(2), match.group(3))
                continue

            match = RE_RESKEY_VLAN.match(resource_key)
            if match is not None:
                self.vlans.add(match.group(1), int(match.group(2)), resource_value)
                continue

            MSG = 'Unhandled Resource Key: {:s} => {:s}'
            raise Exception(MSG.format(str(resource_key), str(resource_value)))

    def get_expected_config(self) -> List[Tuple[str, Dict]]:
        expected_config = list()
        expected_config.extend(self.network_instances.compose_resources())
        expected_config.extend(self.interfaces.compose_resources())
        expected_config.extend(self.protocols.compose_resources())
        expected_config.extend(self.protocol_static.compose_resources())
        expected_config.extend(self.tables.compose_resources())
        expected_config.extend(self.vlans.compose_resources())
        return expected_config
