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

import copy
from typing import Dict, List, Optional, Tuple

from common.proto.context_pb2 import LinkTypeEnum

def get_link_uuid(a_endpoint_id : Dict, z_endpoint_id : Dict) -> str:
    return '{:s}/{:s}=={:s}/{:s}'.format(
        a_endpoint_id['device_id']['device_uuid']['uuid'], a_endpoint_id['endpoint_uuid']['uuid'],
        z_endpoint_id['device_id']['device_uuid']['uuid'], z_endpoint_id['endpoint_uuid']['uuid'])

def json_link_id(link_uuid : str) -> Dict:
    return {'link_uuid': {'uuid': link_uuid}}

def json_link(
    link_uuid : str, endpoint_ids : List[Dict], name : Optional[str] = None,
    link_type : LinkTypeEnum = LinkTypeEnum.LINKTYPE_UNKNOWN,
    total_capacity_gbps : Optional[float] = None, used_capacity_gbps : Optional[float] = None
) -> Dict:
    result = {
        'link_id': json_link_id(link_uuid), 'link_type': link_type,
        'link_endpoint_ids': copy.deepcopy(endpoint_ids),
    }
    if name is not None: result['name'] = name
    if total_capacity_gbps is not None:
        attributes : Dict = result.setdefault('attributes', dict())
        attributes.setdefault('total_capacity_gbps', total_capacity_gbps)
    if used_capacity_gbps is not None:
        attributes : Dict = result.setdefault('attributes', dict())
        attributes.setdefault('used_capacity_gbps', used_capacity_gbps)
    return result

def compose_link(
    endpoint_a : Dict, endpoint_z : Dict, name : Optional[str] = None,
    total_capacity_gbps : Optional[float] = None, used_capacity_gbps : Optional[float] = None
) -> Tuple[Dict, Dict]:
    link_uuid = get_link_uuid(endpoint_a['endpoint_id'], endpoint_z['endpoint_id'])
    link_id   = json_link_id(link_uuid)
    link      = json_link(
        link_uuid, [endpoint_a['endpoint_id'], endpoint_z['endpoint_id']], name=name,
        total_capacity_gbps=total_capacity_gbps, used_capacity_gbps=used_capacity_gbps
    )
    return link_id, link
