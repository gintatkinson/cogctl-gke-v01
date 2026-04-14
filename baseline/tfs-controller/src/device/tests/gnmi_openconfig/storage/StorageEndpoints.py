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

RE_RESKEY_ENDPOINT = re.compile(r'^\/endpoints\/endpoint\[([^\]]+)\]$')

ENDPOINT_PACKET_SAMPLE_TYPES : Dict[int, str] = {
    101: '/openconfig-interfaces:interfaces/interface[name={:s}]/state/counters/out-pkts',
    102: '/openconfig-interfaces:interfaces/interface[name={:s}]/state/counters/in-pkts',
    201: '/openconfig-interfaces:interfaces/interface[name={:s}]/state/counters/out-octets',
    202: '/openconfig-interfaces:interfaces/interface[name={:s}]/state/counters/in-octets',
}

class Endpoints:
    STRUCT : List[Tuple[str, List[str]]] = [
        ('/endpoints/endpoint[{:s}]', ['uuid', 'type', 'sample_types']),
    ]

    def __init__(self) -> None:
        self._items : Dict[str, Dict] = dict()

    def add(self, ep_uuid : str, resource_value : Dict) -> None:
        item = self._items.setdefault(ep_uuid, dict())
        item['uuid'] = ep_uuid

        for _, field_names in Endpoints.STRUCT:
            field_names = set(field_names)
            item.update({k:v for k,v in resource_value.items() if k in field_names})

        item['sample_types'] = {
            sample_type_id : sample_type_path.format(ep_uuid)
            for sample_type_id, sample_type_path in ENDPOINT_PACKET_SAMPLE_TYPES.items()
        }

    def get(self, ep_uuid : str) -> Dict:
        return self._items.get(ep_uuid)

    def remove(self, ep_uuid : str) -> None:
        self._items.pop(ep_uuid, None)
    
    def compose_resources(self) -> List[Dict]:
        return compose_resources(self._items, Endpoints.STRUCT)

class StorageEndpoints:
    def __init__(self) -> None:
        self.endpoints = Endpoints()

    def populate(self, resources : List[Tuple[str, Dict]]) -> None:
        for resource_key, resource_value in resources:
            match = RE_RESKEY_ENDPOINT.match(resource_key)
            if match is not None:
                self.endpoints.add(match.group(1), resource_value)
                continue

            MSG = 'Unhandled Resource Key: {:s} => {:s}'
            raise Exception(MSG.format(str(resource_key), str(resource_value)))

    def get_expected_config(self) -> List[Tuple[str, Dict]]:
        expected_config = list()
        expected_config.extend(self.endpoints.compose_resources())
        return expected_config
