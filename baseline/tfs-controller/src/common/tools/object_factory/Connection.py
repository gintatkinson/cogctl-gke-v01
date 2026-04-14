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

def json_connection_id(connection_uuid : str):
    return {'connection_uuid': {'uuid': connection_uuid}}

def json_connection(
        connection_uuid : str, service_id : Optional[Dict] = None, path_hops_endpoint_ids : List[Dict] = [],
        sub_service_ids : List[Dict] = []
    ):

    result = {
        'connection_id'         : json_connection_id(connection_uuid),
        'path_hops_endpoint_ids': copy.deepcopy(path_hops_endpoint_ids),
        'sub_service_ids'       : copy.deepcopy(sub_service_ids),
    }
    if service_id is not None: result['service_id'] = copy.deepcopy(service_id)
    return result
