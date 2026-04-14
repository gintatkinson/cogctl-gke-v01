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

import functools, re
from typing import Any, List, Optional, Tuple, Union
from common.method_wrappers.ServiceExceptions import NotFoundException
from common.proto.context_pb2 import Device, EndPoint
from common.type_checkers.Checkers import chk_length, chk_type
from common.tools.grpc.Tools import grpc_message_to_json

ACTION_MSG_SET_ENDPOINT      = 'Set EndPoint(device_uuid={:s}, endpoint_uuid={:s}, topology_uuid={:s})'
ACTION_MSG_DELETE_ENDPOINT   = 'Delete EndPoint(device_uuid={:s}, endpoint_uuid={:s}, topology_uuid={:s})'

ACTION_MSG_SET_CONSTRAINT    = 'Set Constraint(constraint_type={:s}, constraint_value={:s})'
ACTION_MSG_DELETE_CONSTRAINT = 'Delete Constraint(constraint_type={:s}, constraint_value={:s})'

ACTION_MSG_SET_CONFIG        = 'Set Resource(key={:s}, value={:s})'
ACTION_MSG_DELETE_CONFIG     = 'Delete Resource(key={:s}, value={:s})'

def _check_errors(
        message : str, parameters_list : List[Any], results_list : List[Union[bool, Exception]]
    ) -> List[str]:
    errors = []
    for parameters, results in zip(parameters_list, results_list):
        if not isinstance(results, Exception): continue
        message = message.format(*tuple(map(str, parameters)))
        errors.append('Unable to {:s}; error({:s})'.format(message, str(results)))
    return errors

check_errors_setendpoint      = functools.partial(_check_errors, ACTION_MSG_SET_ENDPOINT     )
check_errors_deleteendpoint   = functools.partial(_check_errors, ACTION_MSG_DELETE_ENDPOINT  )
check_errors_setconstraint    = functools.partial(_check_errors, ACTION_MSG_SET_CONSTRAINT   )
check_errors_deleteconstraint = functools.partial(_check_errors, ACTION_MSG_DELETE_CONSTRAINT)
check_errors_setconfig        = functools.partial(_check_errors, ACTION_MSG_SET_CONFIG       )
check_errors_deleteconfig     = functools.partial(_check_errors, ACTION_MSG_DELETE_CONFIG    )

def get_endpoint_matching(device : Device, endpoint_uuid_or_name : str) -> EndPoint:
    for endpoint in device.device_endpoints:
        choices = {endpoint.endpoint_id.endpoint_uuid.uuid, endpoint.name}
        if endpoint_uuid_or_name in choices: return endpoint

    device_uuid = device.device_id.device_uuid.uuid
    extra_details = 'Device({:s})'.format(str(device_uuid))
    raise NotFoundException('Endpoint', endpoint_uuid_or_name, extra_details=extra_details)

def get_device_endpoint_uuids(endpoint : Tuple[str, str, Optional[str]]) -> Tuple[str, str]:
    chk_type('endpoint', endpoint, (tuple, list))
    chk_length('endpoint', endpoint, min_length=2, max_length=3)
    device_uuid, endpoint_uuid = endpoint[0:2] # ignore topology_uuid by now
    return device_uuid, endpoint_uuid

def extract_endpoint_index(endpoint_name : str, default_index=0) -> Tuple[str, int]:
    RE_PATTERN = r'^(eth\-[0-9]+(?:\/[0-9]+)*)(?:\.([0-9]+))?$'
    m = re.match(RE_PATTERN, endpoint_name)
    if m is None: return endpoint_name, default_index
    endpoint_name, index = m.groups()
    if index is not None: index = int(index)
    return endpoint_name, index

def extract_index(res_value : Any) ->  int:
    endpoint  = res_value['endpoint_id']['endpoint_uuid']['uuid']
    endpoint  = endpoint[1].split("'}")
    _ , index = extract_endpoint_index(endpoint[0])
    return index
