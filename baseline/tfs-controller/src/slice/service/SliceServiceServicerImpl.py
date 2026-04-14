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
import grpc, json, logging #, deepdiff
from common.proto.context_pb2 import (
    Empty, Service, ServiceId, ServiceStatusEnum, ServiceTypeEnum, Slice, SliceId, SliceStatusEnum)
from common.proto.slice_pb2_grpc import SliceServiceServicer
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.tools.context_queries.InterDomain import is_inter_domain #, is_multi_domain
from common.tools.context_queries.Slice import get_slice_by_defualt_id, get_slice_by_id
from common.tools.grpc.ConfigRules import copy_config_rules
from common.tools.grpc.Constraints import copy_constraints
from common.tools.grpc.EndPointIds import copy_endpoint_ids
from common.tools.grpc.ServiceIds import update_service_ids
#from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from interdomain.client.InterdomainClient import InterdomainClient
from service.client.ServiceClient import ServiceClient
from .slice_grouper.SliceGrouper import SliceGrouper

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Slice', 'RPC')

class SliceServiceServicerImpl(SliceServiceServicer):
    def __init__(self):
        LOGGER.debug('Creating Servicer...')
        self._slice_grouper = SliceGrouper()
        LOGGER.debug('Servicer Created')

    def create_update(self, request : Slice) -> SliceId:
        # Set slice status to "SERVICESTATUS_PLANNED" to ensure rest of components are aware the slice is
        # being modified.
        context_client = ContextClient()
        slice_ro : Optional[Slice] = get_slice_by_id(context_client, request.slice_id, rw_copy=False)
        if not slice_ro:
            slice_ro : Optional[Slice] = get_slice_by_defualt_id(context_client, request.slice_id, rw_copy=False)

        slice_rw = Slice()
        slice_rw.CopyFrom(request if slice_ro is None else slice_ro)
        if len(request.name) > 0: slice_rw.name = request.name
        slice_rw.slice_owner.CopyFrom(request.slice_owner)                          # pylint: disable=no-member
        slice_rw.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_PLANNED    # pylint: disable=no-member

        copy_endpoint_ids(request.slice_endpoint_ids,        slice_rw.slice_endpoint_ids       )        # pylint: disable=no-member
        copy_constraints (request.slice_constraints,         slice_rw.slice_constraints        )        # pylint: disable=no-member
        copy_config_rules(request.slice_config.config_rules, slice_rw.slice_config.config_rules, False) # pylint: disable=no-member

        slice_id_with_uuids = context_client.SetSlice(slice_rw)

        if len(slice_rw.slice_endpoint_ids) < 2: # pylint: disable=no-member
            # unable to identify the kind of slice; just update endpoints, constraints and config rules
            # update the slice in database, and return
            # pylint: disable=no-member
            reply = context_client.SetSlice(slice_rw)
            context_client.close()
            return reply

        slice_with_uuids = context_client.GetSlice(slice_id_with_uuids)

        #LOGGER.info('json_current_slice = {:s}'.format(str(json_current_slice)))
        #json_updated_slice = grpc_message_to_json(request)
        #LOGGER.info('json_updated_slice = {:s}'.format(str(json_updated_slice)))
        #changes = deepdiff.DeepDiff(json_current_slice, json_updated_slice)
        #LOGGER.info('changes = {:s}'.format(str(changes)))

        if is_inter_domain(context_client, slice_with_uuids.slice_endpoint_ids):
            interdomain_client = InterdomainClient()
            slice_id = interdomain_client.RequestSlice(slice_with_uuids)
            slice_ = context_client.GetSlice(slice_id)
            slice_active = Slice()
            slice_active.CopyFrom(slice_)
            slice_active.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_ACTIVE # pylint: disable=no-member
            context_client.SetSlice(slice_active)
            interdomain_client.close()
            context_client.close()
            return slice_id

        if self._slice_grouper.is_enabled:
            grouped = self._slice_grouper.group(slice_with_uuids) # pylint: disable=unused-variable

        # Local domain slice
        service_id = ServiceId()
        # pylint: disable=no-member
        context_uuid = service_id.context_id.context_uuid.uuid = slice_with_uuids.slice_id.context_id.context_uuid.uuid
        service_uuid = service_id.service_uuid.uuid = slice_with_uuids.slice_id.slice_uuid.uuid

        service_client = ServiceClient()
        try:
            _service = context_client.GetService(service_id)
        except: # pylint: disable=bare-except
            # pylint: disable=no-member
            service_request = Service()
            service_request.service_id.CopyFrom(service_id)
            service_request.name = slice_with_uuids.name
            service_request.service_type = ServiceTypeEnum.SERVICETYPE_UNKNOWN
            service_request.service_status.service_status = ServiceStatusEnum.SERVICESTATUS_PLANNED
            service_client.CreateService(service_request)
            _service = context_client.GetService(service_id)
        service_request = Service()
        service_request.CopyFrom(_service)

        # pylint: disable=no-member
        copy_endpoint_ids(request.slice_endpoint_ids, service_request.service_endpoint_ids)
        copy_constraints(request.slice_constraints, service_request.service_constraints)
        copy_config_rules(request.slice_config.config_rules, service_request.service_config.config_rules, False)

        service_request.service_type = ServiceTypeEnum.SERVICETYPE_UNKNOWN
        for config_rule in request.slice_config.config_rules:
            #LOGGER.debug('config_rule: {:s}'.format(grpc_message_to_json_string(config_rule)))
            config_rule_kind = config_rule.WhichOneof('config_rule')
            #LOGGER.debug('config_rule_kind: {:s}'.format(str(config_rule_kind)))
            if config_rule_kind != 'custom': continue
            custom = config_rule.custom
            resource_key = custom.resource_key
            #LOGGER.debug('resource_key: {:s}'.format(str(resource_key)))

            # TODO: parse resource key with regular expression, e.g.:
            #    m = re.match('\/device\[[^\]]\]\/endpoint\[[^\]]\]\/settings', s)
            if not resource_key.startswith('/device'): continue
            if not resource_key.endswith('/settings'): continue

            resource_value = json.loads(custom.resource_value)
            #LOGGER.debug('resource_value: {:s}'.format(str(resource_value)))

            if service_request.service_type == ServiceTypeEnum.SERVICETYPE_UNKNOWN:
                if (resource_value.get('address_ip') is not None and \
                    resource_value.get('address_prefix') is not None):
                    service_request.service_type = ServiceTypeEnum.SERVICETYPE_L3NM
                    #LOGGER.debug('is L3')
                else:
                    service_request.service_type = ServiceTypeEnum.SERVICETYPE_L2NM
                    #LOGGER.debug('is L2')
                break

        if service_request.service_type == ServiceTypeEnum.SERVICETYPE_UNKNOWN:
            service_request.service_type = ServiceTypeEnum.SERVICETYPE_L2NM
            #LOGGER.debug('assume L2')

        service_client.UpdateService(service_request)

        #copy_endpoint_ids(request.slice_endpoint_ids, slice_with_uuids.slice_endpoint_ids)
        #copy_constraints(request.slice_constraints, slice_with_uuids.slice_constraints)
        #copy_config_rules(request.slice_config.config_rules, slice_with_uuids.slice_config.config_rules)

        update_service_ids(slice_with_uuids.slice_service_ids, context_uuid, service_uuid)
        context_client.SetSlice(slice_with_uuids)
        slice_id = slice_with_uuids.slice_id

        slice_ = context_client.GetSlice(slice_id)
        slice_active = Slice()
        slice_active.CopyFrom(slice_)
        slice_active.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_ACTIVE # pylint: disable=no-member
        context_client.SetSlice(slice_active)

        service_client.close()
        context_client.close()
        return slice_id

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def CreateSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        #try:
        #    slice_ = context_client.GetSlice(request.slice_id)
        #    slice_id = slice_.slice_id
        #except grpc.RpcError:
        #    slice_id = context_client.SetSlice(request)
        #return slice_id
        return self.create_update(request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def UpdateSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        #slice_id = context_client.SetSlice(request)
        #if len(request.slice_endpoint_ids) != 2: return slice_id
        #
        #domains = set()
        #for slice_endpoint_id in request.slice_endpoint_ids:
        #    device_uuid = slice_endpoint_id.device_id.device_uuid.uuid
        #    domains.add(device_uuid.split('@')[0])
        #
        #is_multi_domain = len(domains) == 2
        #if is_multi_domain:
        #    interdomain_client = InterdomainClient()
        #    return interdomain_client.LookUpSlice(request)
        #else:
        #    raise NotImplementedError('Slice should create local services for single domain slice')
        return self.create_update(request)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DeleteSlice(self, request : SliceId, context : grpc.ServicerContext) -> Empty:
        context_client = ContextClient()
        try:
            _slice = context_client.GetSlice(request)
        except: # pylint: disable=bare-except
            context_client.close()
            return Empty()

        _slice_rw = Slice()
        _slice_rw.CopyFrom(_slice)
        _slice_rw.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_DEINIT # pylint: disable=no-member
        context_client.SetSlice(_slice_rw)

        if is_inter_domain(context_client, _slice.slice_endpoint_ids):
            interdomain_client = InterdomainClient()
            slice_id = interdomain_client.DeleteSlice(request)
            interdomain_client.close()
        else:
            if self._slice_grouper.is_enabled:
                ungrouped = self._slice_grouper.ungroup(_slice_rw) # pylint: disable=unused-variable

        service_client = ServiceClient()
        for service_id in _slice.slice_service_ids:
            tmp_slice = Slice()
            tmp_slice.slice_id.CopyFrom(_slice.slice_id) # pylint: disable=no-member
            slice_service_id = tmp_slice.slice_service_ids.add() # pylint: disable=no-member
            slice_service_id.CopyFrom(service_id)
            context_client.UnsetSlice(tmp_slice)
            service_client.DeleteService(service_id)
        service_client.close()

        context_client.RemoveSlice(request)
        context_client.close()
        return Empty()
