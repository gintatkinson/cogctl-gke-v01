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

from typing import Dict, Tuple
import grpc, logging, uuid
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME, ServiceNameEnum
from common.Settings import (
    ENVVAR_SUFIX_SERVICE_HOST, ENVVAR_SUFIX_SERVICE_PORT_GRPC, find_environment_variables, get_env_var_name)
from common.proto.context_pb2 import (
    AuthenticationResult, Empty, EndPointId, Slice, SliceId, SliceStatusEnum, TeraFlowController, TopologyId)
from common.proto.interdomain_pb2_grpc import InterdomainServiceServicer
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.tools.context_queries.CheckType import endpoint_type_is_border
from common.tools.context_queries.Context import create_context
from common.tools.context_queries.Device import get_device
from common.tools.context_queries.InterDomain import (
    compute_interdomain_sub_slices, get_local_device_uuids, is_inter_domain)
from common.tools.context_queries.Slice import get_slice_by_id
from common.tools.context_queries.Topology import create_topology, get_topology
from common.tools.grpc.Tools import grpc_message_to_json, grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Device import json_device_id
from common.tools.object_factory.EndPoint import json_endpoint_id
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from dlt.connector.client.DltConnectorClientAsync import DltConnectorClientAsync
from pathcomp.frontend.client.PathCompClient import PathCompClient
from service.client.ServiceClient import ServiceClient
from slice.client.SliceClient import SliceClient
from .topology_abstractor.DltRecordSender import DltRecordSender
from .RemoteDomainClients import RemoteDomainClients
from .Tools import compose_slice, compute_slice_owner #, map_abstract_endpoints_to_real

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
        pathcomp_client = PathCompClient()
        slice_client = SliceClient()

        local_device_uuids = get_local_device_uuids(context_client)
        slice_owner_uuid = request.slice_owner.owner_uuid.uuid
        not_inter_domain = not is_inter_domain(context_client, request.slice_endpoint_ids)
        no_slice_owner = len(slice_owner_uuid) == 0
        is_local_slice_owner = slice_owner_uuid in local_device_uuids
        if not_inter_domain and (no_slice_owner or is_local_slice_owner):
            str_slice = grpc_message_to_json_string(request)
            raise Exception('InterDomain can only handle inter-domain slice requests: {:s}'.format(str_slice))

        local_slices, remote_slices = compute_interdomain_sub_slices(
            context_client, pathcomp_client, request)

        traversed_domain_uuids = set()
        traversed_domain_uuids.update(local_slices.keys())
        traversed_domain_uuids.update(remote_slices.keys())
        LOGGER.debug('traversed_domain_uuids={:s}'.format(str(traversed_domain_uuids)))
        slice_owner_uuid = compute_slice_owner(context_client, traversed_domain_uuids)
        LOGGER.debug('slice_owner_uuid={:s}'.format(str(slice_owner_uuid)))
        if slice_owner_uuid is None:
            raise Exception('Unable to identify slice owner')

        reply = Slice()
        reply.CopyFrom(request)

        env_vars = find_environment_variables([
            get_env_var_name(ServiceNameEnum.DLT, ENVVAR_SUFIX_SERVICE_HOST     ),
            get_env_var_name(ServiceNameEnum.DLT, ENVVAR_SUFIX_SERVICE_PORT_GRPC),
        ])
        if len(env_vars) == 2:
            # DLT available
            dlt_connector_client = DltConnectorClientAsync()
            dlt_connector_client.connect()
        else:
            dlt_connector_client = None

        dlt_record_sender = DltRecordSender(context_client, dlt_connector_client)

        for domain_uuid, endpoint_id_groups in local_slices.items():
            domain_topology = get_topology(context_client, domain_uuid)
            if domain_topology is None: raise Exception('Topology({:s}) not found'.format(str(domain_uuid)))
            domain_name = domain_topology.name
            for endpoint_ids in endpoint_id_groups:
                slice_uuid = str(uuid.uuid4())
                MSG = '[loop] [local] domain_uuid={:s} slice_uuid={:s} endpoint_ids={:s}'
                LOGGER.debug(MSG.format(str(domain_uuid), str(slice_uuid), str([
                    grpc_message_to_json(ep_id) for ep_id in endpoint_ids
                ])))

                # local slices always in DEFAULT_CONTEXT_NAME
                #context_uuid = request.slice_id.context_id.context_uuid.uuid
                context_uuid = DEFAULT_CONTEXT_NAME
                #endpoint_ids = map_abstract_endpoints_to_real(context_client, domain_uuid, endpoint_ids)
                slice_name = '{:s}:local:{:s}'.format(request.name, domain_name)
                sub_slice = compose_slice(
                    context_uuid, slice_uuid, endpoint_ids, slice_name=slice_name, constraints=request.slice_constraints,
                    config_rules=request.slice_config.config_rules)
                LOGGER.debug('[loop] [local] sub_slice={:s}'.format(grpc_message_to_json_string(sub_slice)))
                sub_slice_id = slice_client.CreateSlice(sub_slice)

                LOGGER.debug('[loop] adding sub-slice')
                reply.slice_subslice_ids.add().CopyFrom(sub_slice_id)   # pylint: disable=no-member

        for domain_uuid, endpoint_id_groups in remote_slices.items():
            domain_topology = get_device(context_client, domain_uuid)
            if domain_topology is None: raise Exception('Device({:s}) not found'.format(str(domain_uuid)))
            domain_name = domain_topology.name
            domain_endpoint_ids_to_names = {
                endpoint.endpoint_id.endpoint_uuid.uuid : endpoint.name
                for endpoint in domain_topology.device_endpoints
                if endpoint_type_is_border(endpoint.endpoint_type)
            }
            for endpoint_ids in endpoint_id_groups:
                slice_uuid = str(uuid.uuid4())
                MSG = '[loop] [remote] domain_uuid={:s} slice_uuid={:s} endpoint_ids={:s}'
                LOGGER.debug(MSG.format(str(domain_uuid), str(slice_uuid), str([
                    grpc_message_to_json(ep_id) for ep_id in endpoint_ids
                ])))

                # create context/topology for the remote domains where we are creating slices
                create_context(context_client, domain_uuid, name=domain_name)
                create_topology(context_client, domain_uuid, DEFAULT_TOPOLOGY_NAME)
                create_topology(context_client, domain_uuid, INTERDOMAIN_TOPOLOGY_NAME)

                slice_name = '{:s}:remote:{:s}'.format(request.name, domain_name)
                # convert endpoint ids to names to enable conversion to uuids on the remote domain
                endpoint_ids = [
                    EndPointId(**json_endpoint_id(
                        json_device_id(domain_name),
                        domain_endpoint_ids_to_names[endpoint_id.endpoint_uuid.uuid],
                        topology_id=json_topology_id(
                            INTERDOMAIN_TOPOLOGY_NAME,
                            context_id=json_context_id(DEFAULT_CONTEXT_NAME)
                        )
                    ))
                    for endpoint_id in endpoint_ids
                ]

                sub_slice = compose_slice(
                    DEFAULT_CONTEXT_NAME, slice_uuid, endpoint_ids, slice_name=slice_name,
                    constraints=request.slice_constraints, config_rules=request.slice_config.config_rules,
                    owner_uuid=slice_owner_uuid, owner_string=domain_uuid)
                LOGGER.debug('[loop] [remote] sub_slice={:s}'.format(grpc_message_to_json_string(sub_slice)))
                sub_slice_id = context_client.SetSlice(sub_slice)

                if dlt_connector_client is not None:
                    topology_id = TopologyId(**json_topology_id(domain_uuid))
                    dlt_record_sender.add_slice(topology_id, sub_slice)
                else:
                    interdomain_client = self.remote_domain_clients.get_peer(domain_uuid)
                    if interdomain_client is None:
                        raise Exception('InterDomain Client not found for Domain({:s})'.format(str(domain_uuid)))
                    sub_slice_reply = interdomain_client.LookUpSlice(sub_slice)
                    if sub_slice_reply == sub_slice.slice_id: # pylint: disable=no-member
                        # successful case
                        remote_sub_slice = interdomain_client.OrderSliceFromCatalog(sub_slice)
                    else:
                        # not in catalog
                        remote_sub_slice = interdomain_client.CreateSliceAndAddToCatalog(sub_slice)
                    
                    sub_slice.slice_status.slice_status = remote_sub_slice.slice_status.slice_status
                    context_client.SetSlice(sub_slice)
                    if remote_sub_slice.slice_status.slice_status != SliceStatusEnum.SLICESTATUS_ACTIVE:
                        raise Exception('Remote Slice creation failed. Wrong Slice status returned')

                LOGGER.debug('[loop] adding sub-slice')
                reply.slice_subslice_ids.add().CopyFrom(sub_slice_id)   # pylint: disable=no-member

        if dlt_connector_client is not None:
            LOGGER.debug('Recording Remote Slice requests to DLT')
            dlt_record_sender.commit()

        LOGGER.debug('Activating interdomain slice')
        reply.slice_status.slice_status = SliceStatusEnum.SLICESTATUS_ACTIVE # pylint: disable=no-member

        LOGGER.debug('Updating interdomain slice')
        slice_id = context_client.SetSlice(reply)
        return slice_id

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
            slice_id = SliceId()
            slice_id.CopyFrom(request.slice_id)
            slice_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
            slice_ = context_client.GetSlice(slice_id)
            return slice_.slice_id
        except grpc.RpcError:
            #LOGGER.exception('Unable to get slice({:s})'.format(grpc_message_to_json_string(request.slice_id)))
            return SliceId()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def CreateSliceAndAddToCatalog(self, request : Slice, context : grpc.ServicerContext) -> Slice:
        context_client = ContextClient()
        slice_client = SliceClient()
        _request = Slice()
        _request.CopyFrom(request)
        _request.slice_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME

        #admin_context = context_client.GetContext(ContextId(**json_context_id(DEFAULT_CONTEXT_NAME)))
        #admin_context_uuid = admin_context.context_id.context_uuid.uuid
        #admin_context_name = admin_context.name

        #interdomain_topology = context_client.GetTopology(TopologyId(**json_topology_id(
        #    DEFAULT_TOPOLOGY_NAME, context_id=json_context_id(DEFAULT_CONTEXT_NAME)
        #)))
        #interdomain_topology_uuid = interdomain_topology.topology_id.topology_uuid.uuid
        #interdomain_topology_name = interdomain_topology.name

        devices = context_client.ListDevices(Empty())
        interdomain_endpoint_map : Dict[str, Tuple[str, str, str, str]] = dict()
        for device in devices.devices:
            device_uuid = device.device_id.device_uuid.uuid
            device_name = device.name
            for endpoint in device.device_endpoints:
                if not endpoint_type_is_border(endpoint.endpoint_type): continue
                #endpoint_context_uuid = endpoint.endpoint_id.topology_id.context_id.context_uuid.uuid
                #if endpoint_context_uuid not in {admin_context_uuid, admin_context_name}: continue
                #endpoint_topology_uuid = endpoint.endpoint_id.topology_id.topology_uuid.uuid
                #if endpoint_topology_uuid not in {interdomain_topology_uuid, interdomain_topology_name}: continue
                endpoint_uuid = endpoint.endpoint_id.endpoint_uuid.uuid
                endpoint_name = endpoint.name
                interdomain_endpoint_map[endpoint_name] = (device_uuid, device_name, endpoint_uuid, endpoint_name)
        LOGGER.debug('interdomain_endpoint_map={:s}'.format(str(interdomain_endpoint_map)))

        # Map endpoints to local real counterparts
        del _request.slice_endpoint_ids[:]
        for endpoint_id in request.slice_endpoint_ids:
            #endpoint_context_uuid = endpoint_id.topology_id.context_id.context_uuid.uuid
            #if endpoint_context_uuid not in {admin_context_uuid, admin_context_name}:
            #    MSG = 'Unexpected ContextId in EndPointId({:s})'
            #    raise Exception(MSG.format(grpc_message_to_json_string(endpoint_id)))

            #endpoint_topology_uuid = endpoint_id.topology_id.topology_uuid.uuid
            #if endpoint_topology_uuid not in {admin_topology_uuid, admin_topology_name}:
            #    MSG = 'Unexpected TopologyId in EndPointId({:s})'
            #    raise Exception(MSG.format(grpc_message_to_json_string(endpoint_id)))

            endpoint_uuid = endpoint_id.endpoint_uuid.uuid
            real_endpoint = interdomain_endpoint_map.get(endpoint_uuid)
            if real_endpoint is None:
                MSG = 'Unable to map EndPointId({:s}) to real endpoint. interdomain_endpoint_map={:s}'
                raise Exception(MSG.format(grpc_message_to_json_string(endpoint_id), str(interdomain_endpoint_map)))
            real_device_uuid, _, real_endpoint_uuid, _ = real_endpoint

            real_endpoint_id = _request.slice_endpoint_ids.add()
            real_endpoint_id.topology_id.context_id.context_uuid.uuid = DEFAULT_CONTEXT_NAME
            real_endpoint_id.topology_id.topology_uuid.uuid = DEFAULT_TOPOLOGY_NAME
            real_endpoint_id.device_id.device_uuid.uuid = real_device_uuid
            real_endpoint_id.endpoint_uuid.uuid = real_endpoint_uuid

        slice_id = slice_client.CreateSlice(_request)
        return context_client.GetSlice(slice_id)

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

        local_device_uuids = get_local_device_uuids(context_client)
        slice_owner_uuid = _slice.slice_owner.owner_uuid.uuid
        not_inter_domain = not is_inter_domain(context_client, _slice.slice_endpoint_ids)
        no_slice_owner = len(slice_owner_uuid) == 0
        is_local_slice_owner = slice_owner_uuid in local_device_uuids
        if not_inter_domain and (no_slice_owner or is_local_slice_owner):
            str_slice = grpc_message_to_json_string(_slice)
            raise Exception('InterDomain can only handle inter-domain slice requests: {:s}'.format(str_slice))

        slice_client = SliceClient()
        for subslice_id in _slice_rw.slice_subslice_ids:
            sub_slice = get_slice_by_id(context_client, subslice_id, rw_copy=True)
            if ':remote:' in sub_slice.name:
                domain_uuid = sub_slice.slice_owner.owner_string
                interdomain_client = self.remote_domain_clients.get_peer(domain_uuid)
                if interdomain_client is None:
                    raise Exception('InterDomain Client not found for Domain({:s})'.format(str(domain_uuid)))
                interdomain_client.DeleteSlice(subslice_id)

            tmp_slice = Slice()
            tmp_slice.slice_id.CopyFrom(_slice_rw.slice_id) # pylint: disable=no-member
            slice_subslice_id = tmp_slice.slice_subslice_ids.add() # pylint: disable=no-member
            slice_subslice_id.CopyFrom(subslice_id)
            context_client.UnsetSlice(tmp_slice)

            if ':remote:' in sub_slice.name:
                context_client.RemoveSlice(subslice_id)
            else:
                slice_client.DeleteSlice(subslice_id)

        service_client = ServiceClient()
        for service_id in _slice_rw.slice_service_ids:
            tmp_slice = Slice()
            tmp_slice.slice_id.CopyFrom(_slice_rw.slice_id) # pylint: disable=no-member
            slice_service_id = tmp_slice.slice_service_ids.add() # pylint: disable=no-member
            slice_service_id.CopyFrom(service_id)
            context_client.UnsetSlice(tmp_slice)
            service_client.DeleteService(service_id)

        context_client.RemoveSlice(request)
        slice_client.close()
        service_client.close()
        context_client.close()
        return Empty()
