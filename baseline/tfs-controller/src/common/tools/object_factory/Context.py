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

from typing import Optional

def json_context_id(context_uuid : str):
    return {'context_uuid': {'uuid': context_uuid}}

def json_context(context_uuid : str, name : Optional[str] = None):
    result = {
        'context_id'  : json_context_id(context_uuid),
        'topology_ids': [],
        'service_ids' : [],
        'slice_ids'   : [],
    }
    if name is not None: result['name'] = name
    return result
