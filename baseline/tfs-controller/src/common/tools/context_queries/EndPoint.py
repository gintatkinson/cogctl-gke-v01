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

import logging
from typing import Dict, List, Set, Tuple
from common.proto.context_pb2 import EndPointId, EndPointIdList
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

TYPE_DEVICE_NAMES   = Dict[str, str]             # device_uuid => device_name
TYPE_ENDPOINTS_DATA = Dict[str, Tuple[str, str]] # endpoint_uuid => (endpoint_name, endpoint_type)
TYPE_NAME_MAPS      = Tuple[TYPE_DEVICE_NAMES, TYPE_ENDPOINTS_DATA]

def get_endpoint_names(context_client : ContextClient, endpoint_ids : List[EndPointId]) -> TYPE_NAME_MAPS:
    endpoint_uuids_to_names : Set[str] = set()
    endpoint_id_list = EndPointIdList()
    for endpoint_id in endpoint_ids:
        endpoint_uuid = endpoint_id.endpoint_uuid.uuid
        if endpoint_uuid in endpoint_uuids_to_names: continue
        endpoint_id_list.endpoint_ids.add().CopyFrom(endpoint_id)   # pylint: disable=no-member
        endpoint_uuids_to_names.add(endpoint_uuid)

    endpoint_names = context_client.ListEndPointNames(endpoint_id_list)

    device_names   : TYPE_DEVICE_NAMES   = dict()
    endpoints_data : TYPE_ENDPOINTS_DATA = dict()
    for endpoint_name in endpoint_names.endpoint_names:
        device_uuid = endpoint_name.endpoint_id.device_id.device_uuid.uuid
        device_names[device_uuid] = endpoint_name.device_name

        endpoint_uuid = endpoint_name.endpoint_id.endpoint_uuid.uuid
        endpoints_data[endpoint_uuid] = (endpoint_name.endpoint_name, endpoint_name.endpoint_type)

    return device_names, endpoints_data
