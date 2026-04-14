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
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import SliceStatusEnum
from common.tools.object_factory.Context import json_context_id

def get_slice_uuid(a_endpoint_id : Dict, z_endpoint_id : Dict) -> str:
    return 'slc:{:s}/{:s}=={:s}/{:s}'.format(
        a_endpoint_id['device_id']['device_uuid']['uuid'], a_endpoint_id['endpoint_uuid']['uuid'],
        z_endpoint_id['device_id']['device_uuid']['uuid'], z_endpoint_id['endpoint_uuid']['uuid'])

def json_slice_id(slice_uuid : str, context_id : Optional[Dict] = None) -> Dict:
    result = {'slice_uuid': {'uuid': slice_uuid}}
    if context_id is not None: result['context_id'] = copy.deepcopy(context_id)
    return result

def json_slice_owner(owner_uuid : str, owner_string : str) -> Dict:
    return {'owner_uuid': {'uuid': owner_uuid}, 'owner_string': owner_string}

def json_slice(
    slice_uuid : str, context_id : Optional[Dict] = None,
    status : SliceStatusEnum = SliceStatusEnum.SLICESTATUS_PLANNED, endpoint_ids : List[Dict] = [],
    constraints : List[Dict] = [], config_rules : List[Dict] = [], service_ids : List[Dict] = [],
    subslice_ids : List[Dict] = [], owner : Optional[Dict] = None):

    if context_id is None: context_id = json_context_id(DEFAULT_CONTEXT_NAME)

    result = {
        'slice_id'          : json_slice_id(slice_uuid, context_id=context_id),
        'slice_status'      : {'slice_status': status},
        'slice_endpoint_ids': copy.deepcopy(endpoint_ids),
        'slice_constraints' : copy.deepcopy(constraints),
        'slice_config'      : {'config_rules': copy.deepcopy(config_rules)},
        'slice_service_ids' : copy.deepcopy(service_ids),
        'slice_subslice_ids': copy.deepcopy(subslice_ids),
    }
    if owner is not None: result['slice_owner'] = owner
    return result
