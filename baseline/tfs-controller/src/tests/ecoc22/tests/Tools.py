# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List, Tuple
from common.tools.object_factory.EndPoint import json_endpoint, json_endpoint_id
from common.tools.object_factory.Link import json_link, json_link_id

def json_endpoint_ids(device_id : Dict, endpoint_descriptors : List[Dict]]):
    return [
        json_endpoint_id(device_id, ep_data['uuid'], topology_id=None)
        for ep_data in endpoint_descriptors
    ]

def json_endpoints(device_id : Dict, endpoint_descriptors : List[Dict]]):
    return [
        json_endpoint(
            device_id, ep_data['uuid'], ep_data['type'], topology_id=None,
            kpi_sample_types=ep_data['sample_types'])
        for ep_data in endpoint_descriptors
    ]

def get_link_uuid(a_endpoint_id : Dict, z_endpoint_id : Dict) -> str:
    return '{:s}/{:s}=={:s}/{:s}'.format(
        a_endpoint_id['device_id']['device_uuid']['uuid'], a_endpoint_id['endpoint_uuid']['uuid'],
        a_endpoint_id['device_id']['device_uuid']['uuid'], z_endpoint_id['endpoint_uuid']['uuid'])

def link(a_endpoint_id, z_endpoint_id) -> Tuple[str, Dict, Dict]:
    link_uuid = get_link_uuid(a_endpoint_id, z_endpoint_id)
    link_id   = json_link_id(link_uuid)
    link_data = json_link(link_uuid, [a_endpoint_id, z_endpoint_id])
    return link_uuid, link_id, link_data

def compose_service_endpoint_id(endpoint_id):
    device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
    endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
    return ':'.join([device_uuid, endpoint_uuid])

def compose_bearer(endpoint_id):
    device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
    endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
    return ':'.join([device_uuid, endpoint_uuid])
