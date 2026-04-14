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

from typing import Dict, List
from common.tools.object_factory.EndPoint import json_endpoint_id

def json_endpoint_ids(device_id : Dict, endpoint_descriptors : List[Dict]):
    return {
        device_id['device_uuid']['uuid']: {
            ep_data['uuid']: json_endpoint_id(device_id, ep_data['uuid'], topology_id=None)
            for ep_data in endpoint_descriptors
        }
    }

def get_link_uuid(a_endpoint_id : Dict, z_endpoint_id : Dict) -> str:
    return '{:s}/{:s}=={:s}/{:s}'.format(
        a_endpoint_id['device_id']['device_uuid']['uuid'], a_endpoint_id['endpoint_uuid']['uuid'],
        z_endpoint_id['device_id']['device_uuid']['uuid'], z_endpoint_id['endpoint_uuid']['uuid'])

def compose_service_endpoint_id(endpoint_id):
    device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
    endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
    return ':'.join([device_uuid, endpoint_uuid])

def compose_bearer(endpoint_id):
    device_uuid = endpoint_id['device_id']['device_uuid']['uuid']
    endpoint_uuid = endpoint_id['endpoint_uuid']['uuid']
    return ':'.join([device_uuid, endpoint_uuid])
