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

import grpc, logging
from typing import List, Optional
from common.Constants import DEFAULT_CONTEXT_NAME
from common.proto.context_pb2 import ContextId, Service, ServiceFilter, ServiceId
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

def get_service_by_id(
    context_client : ContextClient, service_id : ServiceId, rw_copy : bool = False,
    include_endpoint_ids : bool = True, include_constraints : bool = True, include_config_rules : bool = True
) -> Optional[Service]:
    service_filter = ServiceFilter()
    service_filter.service_ids.service_ids.append(service_id) # pylint: disable=no-member
    service_filter.include_endpoint_ids = include_endpoint_ids
    service_filter.include_constraints = include_constraints
    service_filter.include_config_rules = include_config_rules

    try:
        ro_services = context_client.SelectService(service_filter)
        if len(ro_services.services) == 0: return None
        assert len(ro_services.services) == 1
        ro_service = ro_services.services[0]
        if not rw_copy: return ro_service
        rw_service = Service()
        rw_service.CopyFrom(ro_service)
        return rw_service
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.NOT_FOUND: raise # pylint: disable=no-member
        #LOGGER.exception('Unable to get service({:s} / {:s})'.format(str(context_uuid), str(service_uuid)))
        return None

def get_service_by_uuid(
    context_client : ContextClient, service_uuid : str, context_uuid : str = DEFAULT_CONTEXT_NAME,
    rw_copy : bool = False, include_endpoint_ids : bool = True, include_constraints : bool = True,
    include_config_rules : bool = True
) -> Optional[Service]:
    service_id = ServiceId()
    service_id.context_id.context_uuid.uuid = context_uuid  # pylint: disable=no-member
    service_id.service_uuid.uuid = service_uuid             # pylint: disable=no-member
    return get_service_by_id(
        context_client, service_id, rw_copy=rw_copy, include_endpoint_ids=include_endpoint_ids,
        include_constraints=include_constraints, include_config_rules=include_config_rules)

def get_services(
        context_client : ContextClient, context_uuid : str = DEFAULT_CONTEXT_NAME
    ) -> List[Service]:
    context_id = ContextId()
    context_id.context_uuid.uuid = context_uuid
    services = context_client.ListServices(context_id)
    return [s for s in services.services]
