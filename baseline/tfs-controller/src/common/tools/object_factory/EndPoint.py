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
from typing import Dict, List, Optional

def json_endpoint_descriptor(
    endpoint_uuid : str, endpoint_type : str, endpoint_name : Optional[str] = None,
    sample_types : List[int] = [], location : Optional[Dict] = None
) -> Dict:
    result = {'uuid': endpoint_uuid, 'type': endpoint_type}
    if endpoint_name is not None:
        result['name'] = endpoint_name
    if sample_types is not None and len(sample_types) > 0:
        result['sample_types'] = sample_types
    if location is not None and len(location) > 0:
        result['location'] = location
    return result

def json_endpoint_id(device_id : Dict, endpoint_uuid : str, topology_id : Optional[Dict] = None):
    result = {'device_id': copy.deepcopy(device_id), 'endpoint_uuid': {'uuid': endpoint_uuid}}
    if topology_id is not None: result['topology_id'] = copy.deepcopy(topology_id)
    return result

def json_endpoint_ids(
        device_id : Dict, endpoint_descriptors : List[Dict], topology_id : Optional[Dict] = None
    ):
    return [
        json_endpoint_id(device_id, endpoint_data['uuid'], topology_id=topology_id)
        for endpoint_data in endpoint_descriptors
    ]

def json_endpoint(
        device_id : Dict, endpoint_uuid : str, endpoint_type : str, topology_id : Optional[Dict] = None,
        name : Optional[str] = None, kpi_sample_types : List[int] = [], location : Optional[Dict] = None
    ):

    result = {
        'endpoint_id': json_endpoint_id(device_id, endpoint_uuid, topology_id=topology_id),
        'endpoint_type': endpoint_type,
    }
    if name is not None: result['name'] = name
    if kpi_sample_types is not None and len(kpi_sample_types) > 0:
        result['kpi_sample_types'] = copy.deepcopy(kpi_sample_types)
    if location is not None:
        result['endpoint_location'] = copy.deepcopy(location)
    return result

def json_endpoints(
        device_id : Dict, endpoint_descriptors : List[Dict], topology_id : Optional[Dict] = None
    ):
    return [
        json_endpoint(
            device_id, endpoint_data['uuid'], endpoint_data['type'], topology_id=topology_id,
            kpi_sample_types=endpoint_data.get('sample_types'), location=endpoint_data.get('location'))
        for endpoint_data in endpoint_descriptors
    ]
