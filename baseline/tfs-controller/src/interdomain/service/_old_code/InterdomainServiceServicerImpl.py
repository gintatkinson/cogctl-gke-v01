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
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import (
    AuthenticationResult, Slice, SliceId, SliceStatus, SliceStatusEnum, TeraFlowController)
from common.proto.interdomain_pb2_grpc import InterdomainServiceServicer
#from common.tools.grpc.Tools import grpc_message_to_json_string
from context.client.ContextClient import ContextClient
from interdomain.service.RemoteDomainClients import RemoteDomainClients
from slice.client.SliceClient import SliceClient

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Interdomain', 'RPC')

class InterdomainServiceServicerImpl(InterdomainServiceServicer):
    def __init__(self, remote_domain_clients : RemoteDomainClients):
        LOGGER.debug('Creating Servicer...')
        self.remote_domain_clients = remote_domain_clients
        LOGGER.debug('Servicer Created')

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def RequestSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        context_client = ContextClient()
        slice_client = SliceClient()

        domains_to_endpoints = {}
        local_domain_uuid = None
        for slice_endpoint_id in request.slice_endpoint_ids:
            device_uuid = slice_endpoint_id.device_id.device_uuid.uuid
            domain_uuid = device_uuid.split('@')[1]
            endpoints = domains_to_endpoints.setdefault(domain_uuid, [])
            endpoints.append(slice_endpoint_id)
            if local_domain_uuid is None: local_domain_uuid = domain_uuid

        reply = Slice()
        reply.CopyFrom(request)

        # decompose remote slices
        for domain_uuid, slice_endpoint_ids in domains_to_endpoints.items():
            if domain_uuid == local_domain_uuid: continue

            remote_slice_request = Slice()
            remote_slice_request.slice_id.context_id.context_uuid.uuid = request.slice_id.context_id.context_uuid.uuid
            remote_slice_request.slice_id.slice_uuid.uuid = \
                request.slice_id.slice_uuid.uuid + ':subslice@' + local_domain_uuid
            remote_slice_request.slice_status.slice_status = request.slice_status.slice_status
            for endpoint_id in slice_endpoint_ids:
                slice_endpoint_id = remote_slice_request.slice_endpoint_ids.add()
                slice_endpoint_id.device_id.device_uuid.uuid = endpoint_id.device_id.device_uuid.uuid
                slice_endpoint_id.endpoint_uuid.uuid = endpoint_id.endpoint_uuid.uuid

            # add endpoint connecting to remote domain
            if domain_uuid == 'D1':
                slice_endpoint_id = remote_slice_request.slice_endpoint_ids.add()
                slice_endpoint_id.device_id.device_uuid.uuid = 'R4@D1'
                slice_endpoint_id.endpoint_uuid.uuid = '2/1'
            elif domain_uuid == 'D2':
                slice_endpoint_id = remote_slice_request.slice_endpoint_ids.add()
                slice_endpoint_id.device_id.device_uuid.uuid = 'R1@D2'
                slice_endpoint_id.endpoint_uuid.uuid = '2/1'

            interdomain_client = self.remote_domain_clients.get_peer('remote-teraflow')
            remote_slice_reply = interdomain_client.LookUpSlice(remote_slice_request)
            if remote_slice_reply == remote_slice_request.slice_id: # pylint: disable=no-member
                # successful case
                remote_slice = interdomain_client.OrderSliceFromCatalog(remote_slice_request)
                if remote_slice.slice_status.slice_status != SliceStatusEnum.SLICESTATUS_ACTIVE:
                    raise Exception('Remote Slice creation failed. Wrong Slice status returned')
            else:
                # not in catalog
                remote_slice = interdomain_client.CreateSliceAndAddToCatalog(remote_slice_request)
                if remote_slice.slice_status.slice_status != SliceStatusEnum.SLICESTATUS_ACTIVE:
                    raise Exception('Remote Slice creation failed. Wrong Slice status returned')

            #context_client.SetSlice(remote_slice)
            #subslice_id = reply.slice_subslice_ids.add()
            #subslice_id.CopyFrom(remote_slice.slice_id)

        local_slice_request = Slice()
        local_slice_request.slice_id.context_id.context_uuid.uuid = request.slice_id.context_id.context_uuid.uuid
        local_slice_request.slice_id.slice_uuid.uuid = request.slice_id.slice_uuid.uuid + ':subslice'
        local_slice_request.slice_status.slice_status = request.slice_status.slice_status
        for endpoint_id in domains_to_endpoints[local_domain_uuid]:
            slice_endpoint_id = local_slice_request.slice_endpoint_ids.add()
            slice_endpoint_id.CopyFrom(endpoint_id)

        # add endpoint connecting to remote domain
        if local_domain_uuid == 'D1':
            slice_endpoint_id = local_slice_request.slice_endpoint_ids.add()
            slice_endpoint_id.device_id.device_uuid.uuid = 'R4@D1'
            slice_endpoint_id.endpoint_uuid.uuid = '2/1'
        elif local_domain_uuid == 'D2':
            slice_endpoint_id = local_slice_request.slice_endpoint_ids.add()
            slice_endpoint_id.device_id.device_uuid.uuid = 'R1@D2'
            slice_endpoint_id.endpoint_uuid.uuid = '2/1'

        local_slice_id_reply = slice_client.CreateSlice(local_slice_request)

        subslice_id = reply.slice_subslice_ids.add()
        subslice_id.context_id.context_uuid.uuid = local_slice_id_reply.context_id.context_uuid.uuid
        subslice_id.slice_uuid.uuid = local_slice_id_reply.slice_uuid.uuid

        reply_slice_id = context_client.SetSlice(reply)
        return reply_slice_id

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def Authenticate(self, request : TeraFlowController, context : grpc.ServicerContext) -> AuthenticationResult:
        auth_result = AuthenticationResult()
        auth_result.context_id.CopyFrom(request.context_id) # pylint: disable=no-member
        auth_result.authenticated = True
        return auth_result

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def LookUpSlice(self, request : Slice, context : grpc.ServicerContext) -> SliceId:
        try:
            context_client = ContextClient()
            slice_ = context_client.GetSlice(request.slice_id)
            return slice_.slice_id
        except grpc.RpcError:
            #LOGGER.exception('Unable to get slice({:s})'.format(grpc_message_to_json_string(request.slice_id)))
            return SliceId()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def OrderSliceFromCatalog(self, request : Slice, context : grpc.ServicerContext) -> Slice:
        raise NotImplementedError('OrderSliceFromCatalog')
        #return Slice()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def CreateSliceAndAddToCatalog(self, request : Slice, context : grpc.ServicerContext) -> Slice:
        context_client = ContextClient()
        slice_client = SliceClient()
        reply = slice_client.CreateSlice(request)
        if reply != request.slice_id: # pylint: disable=no-member
            raise Exception('Slice creation failed. Wrong Slice Id was returned')
        return context_client.GetSlice(request.slice_id)
