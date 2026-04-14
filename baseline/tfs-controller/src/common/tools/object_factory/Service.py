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
from common.proto.context_pb2 import ServiceStatusEnum, ServiceTypeEnum
from common.tools.object_factory.Context import json_context_id

def get_service_uuid(a_endpoint_id : Dict, z_endpoint_id : Dict) -> str:
    return 'svc:{:s}/{:s}=={:s}/{:s}'.format(
        a_endpoint_id['device_id']['device_uuid']['uuid'], a_endpoint_id['endpoint_uuid']['uuid'],
        z_endpoint_id['device_id']['device_uuid']['uuid'], z_endpoint_id['endpoint_uuid']['uuid'])

def json_service_id(service_uuid : str, context_id : Optional[Dict] = None):
    result = {'service_uuid': {'uuid': service_uuid}}
    if context_id is not None: result['context_id'] = copy.deepcopy(context_id)
    return result

def json_service(
    service_uuid : str, service_type : ServiceTypeEnum, context_id : Optional[Dict] = None,
    name : Optional[str] = None, status : ServiceStatusEnum = ServiceStatusEnum.SERVICESTATUS_PLANNED,
    endpoint_ids : List[Dict] = [], constraints : List[Dict] = [], config_rules : List[Dict] = []
) -> Dict:
    result = {
        'service_id'          : json_service_id(service_uuid, context_id=context_id),
        'service_type'        : service_type,
        'service_status'      : {'service_status': status},
        'service_endpoint_ids': copy.deepcopy(endpoint_ids),
        'service_constraints' : copy.deepcopy(constraints),
        'service_config'      : {'config_rules': copy.deepcopy(config_rules)},
    }
    if name is not None: result['name'] = name
    return result

def json_service_qkd_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_QKD, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)

def json_service_l2nm_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_L2NM, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)

def json_service_l3nm_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_L3NM, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)

def json_service_tapi_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_TAPI_CONNECTIVITY_SERVICE, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)

def json_service_p4_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_L1NM, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)

def json_service_iplink_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_IP_LINK, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)

def json_service_ipowdm_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_IPOWDM, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)

def json_service_tapi_lsp_planned(
        service_uuid : str, endpoint_ids : List[Dict] = [], constraints : List[Dict] = [],
        config_rules : List[Dict] = [], context_uuid : str = DEFAULT_CONTEXT_NAME
    ):

    return json_service(
        service_uuid, ServiceTypeEnum.SERVICETYPE_TAPI_LSP, context_id=json_context_id(context_uuid),
        status=ServiceStatusEnum.SERVICESTATUS_PLANNED, endpoint_ids=endpoint_ids, constraints=constraints,
        config_rules=config_rules)
