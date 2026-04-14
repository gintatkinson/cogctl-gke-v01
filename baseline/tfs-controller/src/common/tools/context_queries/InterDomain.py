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
from common.Constants import DEFAULT_CONTEXT_NAME, DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME
from common.DeviceTypes import DeviceTypeEnum
from common.proto.context_pb2 import ContextId, Empty, EndPointId, ServiceTypeEnum, Slice
from common.proto.pathcomp_pb2 import PathCompRequest
from .CheckType import device_type_is_network
from .Device import get_device #, get_devices_in_topology
from .Topology import get_topology
from common.tools.grpc.Tools import grpc_message_list_to_json, grpc_message_to_json_string
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient
from pathcomp.frontend.client.PathCompClient import PathCompClient

LOGGER = logging.getLogger(__name__)

ADMIN_CONTEXT_ID = ContextId(**json_context_id(DEFAULT_CONTEXT_NAME))
DATACENTER_DEVICE_TYPES = {DeviceTypeEnum.DATACENTER, DeviceTypeEnum.EMULATED_DATACENTER}

def get_local_device_uuids(context_client : ContextClient) -> Set[str]:
    topologies = context_client.ListTopologies(ADMIN_CONTEXT_ID)

    local_topologies = dict()
    for topology in topologies.topologies:
        topology_uuid = topology.topology_id.topology_uuid.uuid
        if topology_uuid == INTERDOMAIN_TOPOLOGY_NAME: continue
        topology_name = topology.name
        if topology_name == INTERDOMAIN_TOPOLOGY_NAME: continue
        local_topologies[topology_uuid] = topology
    str_local_topologies = {
        topology_uuid:grpc_message_to_json_string(topology)
        for topology_uuid,topology in local_topologies.items()
    }
    LOGGER.debug('[get_local_device_uuids] local_topologies={:s}'.format(str(str_local_topologies)))

    local_topology_uuids = set(local_topologies.keys())
    LOGGER.debug('[get_local_device_uuids] local_topology_uuids={:s}'.format(str(local_topology_uuids)))

    # Add topology names except DEFAULT_TOPOLOGY_NAME and INTERDOMAIN_TOPOLOGY_NAME; they are abstracted as a
    # local device in inter-domain and the name of the topology is used as abstract device name
    # Add physical devices in the local topologies
    local_device_uuids = set()
    for topology_uuid,topology in local_topologies.items():
        if topology_uuid == DEFAULT_TOPOLOGY_NAME: continue
        topology_name = topology.name
        if topology_name == DEFAULT_TOPOLOGY_NAME: continue
        #local_device_uuids.add(topology_uuid)

        device_uuids = {device_id.device_uuid.uuid for device_id in topology.device_ids}
        LOGGER.debug('[get_local_device_uuids] [loop] topology_uuid={:s} device_uuids={:s}'.format(
            str(topology_uuid), str(device_uuids)))
        local_device_uuids.update(device_uuids)

    LOGGER.debug('[get_local_device_uuids] local_device_uuids={:s}'.format(str(local_device_uuids)))
    return local_device_uuids

def get_interdomain_device_uuids(context_client : ContextClient) -> Set[str]:
    context_uuid = DEFAULT_CONTEXT_NAME
    topology_uuid = INTERDOMAIN_TOPOLOGY_NAME
    interdomain_topology = get_topology(context_client, topology_uuid, context_uuid=context_uuid)
    if interdomain_topology is None:
        MSG = '[get_interdomain_device_uuids] {:s}/{:s} topology not found'
        LOGGER.warning(MSG.format(context_uuid, topology_uuid))
        return set()

    # add abstracted devices in the interdomain topology
    interdomain_device_ids = interdomain_topology.device_ids
    interdomain_device_uuids = {device_id.device_uuid.uuid for device_id in interdomain_device_ids}
    LOGGER.debug('[get_interdomain_device_uuids] interdomain_device_uuids={:s}'.format(str(interdomain_device_uuids)))
    return interdomain_device_uuids

def is_inter_domain(context_client : ContextClient, endpoint_ids : List[EndPointId]) -> bool:
    interdomain_device_uuids = get_interdomain_device_uuids(context_client)
    LOGGER.debug('[is_inter_domain] interdomain_device_uuids={:s}'.format(str(interdomain_device_uuids)))
    non_interdomain_endpoint_ids = [
        endpoint_id
        for endpoint_id in endpoint_ids
        if endpoint_id.device_id.device_uuid.uuid not in interdomain_device_uuids
    ]
    str_non_interdomain_endpoint_ids = [
        (endpoint_id.device_id.device_uuid.uuid, endpoint_id.endpoint_uuid.uuid)
        for endpoint_id in non_interdomain_endpoint_ids
    ]
    LOGGER.debug('[is_inter_domain] non_interdomain_endpoint_ids={:s}'.format(str(str_non_interdomain_endpoint_ids)))
    is_inter_domain_ = len(non_interdomain_endpoint_ids) == 0
    LOGGER.debug('[is_inter_domain] is_inter_domain={:s}'.format(str(is_inter_domain_)))
    return is_inter_domain_

def get_device_to_domain_map(context_client : ContextClient) -> Dict[str, str]:
    devices_to_domains : Dict[str, str] = dict()
    contexts = context_client.ListContexts(Empty())
    for context in contexts.contexts:
        context_id = context.context_id
        context_uuid = context_id.context_uuid.uuid
        context_name = context.name
        topologies = context_client.ListTopologies(context_id)
        if (context_uuid == DEFAULT_CONTEXT_NAME) or (context_name == DEFAULT_CONTEXT_NAME):
            for topology in topologies.topologies:
                topology_id = topology.topology_id
                topology_uuid = topology_id.topology_uuid.uuid
                topology_name = topology.name

                if topology_uuid in {DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME}: continue
                if topology_name in {DEFAULT_TOPOLOGY_NAME, INTERDOMAIN_TOPOLOGY_NAME}: continue

                # add topology names except DEFAULT_TOPOLOGY_NAME and INTERDOMAIN_TOPOLOGY_NAME; they are
                # abstracted as a local device in inter-domain and the name of the topology is used as
                # abstract device name
                devices_to_domains[topology_uuid] = topology_uuid

                # add physical devices in the local topology
                for device_id in topology.device_ids:
                    device_uuid = device_id.device_uuid.uuid
                    devices_to_domains[device_uuid] = topology_uuid
        else:
            # for each topology in a remote context
            for topology in topologies.topologies:
                topology_id = topology.topology_id
                topology_uuid = topology_id.topology_uuid.uuid
                topology_name = topology.name

                # if topology is not interdomain
                if topology_uuid in {INTERDOMAIN_TOPOLOGY_NAME}: continue
                if topology_name in {INTERDOMAIN_TOPOLOGY_NAME}: continue

                # add devices to the remote domain list
                for device_id in topology.device_ids:
                    device_uuid = device_id.device_uuid.uuid
                    devices_to_domains[device_uuid] = context_uuid

    return devices_to_domains

def compute_interdomain_sub_slices(
    context_client : ContextClient, pathcomp_client : PathCompClient, slice_ : Slice
) -> Tuple[Dict[str, List[EndPointId]], Dict[str, List[EndPointId]]]:
    context_uuid = slice_.slice_id.context_id.context_uuid.uuid
    slice_uuid = slice_.slice_id.slice_uuid.uuid

    pathcomp_req = PathCompRequest()
    pathcomp_req.shortest_path.Clear()                                          # pylint: disable=no-member
    pathcomp_req_svc = pathcomp_req.services.add()                              # pylint: disable=no-member
    pathcomp_req_svc.service_id.context_id.context_uuid.uuid = context_uuid
    pathcomp_req_svc.service_id.service_uuid.uuid = slice_uuid
    pathcomp_req_svc.service_type = ServiceTypeEnum.SERVICETYPE_L2NM

    for endpoint_id in slice_.slice_endpoint_ids:
        service_endpoint_id = pathcomp_req_svc.service_endpoint_ids.add()
        service_endpoint_id.CopyFrom(endpoint_id)
    
    capacity_gbps  = 10.0   # default value; to be overwritten by constraints in slice
    e2e_latency_ms = 100.0  # default value; to be overwritten by constraints in slice
    for constraint in slice_.slice_constraints:
        kind = constraint.WhichOneof('constraint')
        if kind == 'sla_capacity':
            capacity_gbps = constraint.sla_capacity.capacity_gbps
        elif kind == 'sla_latency':
            e2e_latency_ms = constraint.sla_latency.e2e_latency_ms

    constraint_sla_capacity = pathcomp_req_svc.service_constraints.add()
    constraint_sla_capacity.sla_capacity.capacity_gbps = capacity_gbps

    constraint_sla_latency = pathcomp_req_svc.service_constraints.add()
    constraint_sla_latency.sla_latency.e2e_latency_ms = e2e_latency_ms

    LOGGER.debug('[compute_interdomain_sub_slices] pathcomp_req = {:s}'.format(
        grpc_message_to_json_string(pathcomp_req)))
    pathcomp_rep = pathcomp_client.Compute(pathcomp_req)
    LOGGER.debug('[compute_interdomain_sub_slices] pathcomp_rep = {:s}'.format(
        grpc_message_to_json_string(pathcomp_rep)))

    num_services = len(pathcomp_rep.services)
    if num_services == 0:
        raise Exception('No services received : {:s}'.format(grpc_message_to_json_string(pathcomp_rep)))

    num_connections = len(pathcomp_rep.connections)
    if num_connections != num_services:
        raise Exception('No connections received : {:s}'.format(grpc_message_to_json_string(pathcomp_rep)))

    local_device_uuids = get_local_device_uuids(context_client)
    LOGGER.debug('[compute_interdomain_sub_slices] local_device_uuids={:s}'.format(str(local_device_uuids)))

    device_to_domain_map = get_device_to_domain_map(context_client)
    LOGGER.debug('[compute_interdomain_sub_slices] device_to_domain_map={:s}'.format(str(device_to_domain_map)))

    local_slices  : Dict[str, List[EndPointId]] = dict()
    remote_slices : Dict[str, List[EndPointId]] = dict()
    req_service_uuid = pathcomp_req_svc.service_id.service_uuid.uuid
    for service in pathcomp_rep.services:
        service_uuid = service.service_id.service_uuid.uuid
        if service_uuid == req_service_uuid: continue # main synthetic service; we don't care
        device_uuids = {
            endpoint_id.device_id.device_uuid.uuid
            for endpoint_id in service.service_endpoint_ids
        }

        local_domain_uuids = set()
        remote_domain_uuids = set()
        for device_uuid in device_uuids:
            if device_uuid in local_device_uuids:
                domain_uuid = device_to_domain_map.get(device_uuid)
                if domain_uuid is None:
                    raise Exception('Unable to map device({:s}) to a domain'.format(str(device_uuid)))
                local_domain_uuids.add(domain_uuid)
            else:
                device = get_device(
                    context_client, device_uuid, include_endpoints=True, include_config_rules=False,
                    include_components=False)
                if device is None: raise Exception('Device({:s}) not found'.format(str(device_uuid)))
                if not device_type_is_network(device.device_type):
                    MSG = 'Weird device({:s}) is not local and not network'
                    raise Exception(MSG.format(grpc_message_to_json_string(device)))
                remote_domain_uuids.add(device_uuid)

        if len(local_domain_uuids) > 1:
            MSG = 'Devices({:s}) map to multiple local domains({:s})'
            raise Exception(MSG.format(str(device_uuids), str(local_domain_uuids)))
        is_local = len(local_domain_uuids) == 1

        if len(remote_domain_uuids) > 1:
            MSG = 'Devices({:s}) map to multiple remote domains({:s})'
            raise Exception(MSG.format(str(device_uuids), str(remote_domain_uuids)))
        is_remote = len(remote_domain_uuids) == 1

        if is_local == is_remote:
            MSG = 'Weird service combines local and remote devices: {:s}'
            raise Exception(MSG.format(grpc_message_to_json_string(service)))
        elif is_local:
            local_domain_uuid = local_domain_uuids.pop()
            local_slices.setdefault(local_domain_uuid, list()).append(service.service_endpoint_ids)
        else:
            remote_domain_uuid = remote_domain_uuids.pop()
            remote_slices.setdefault(remote_domain_uuid, list()).append(service.service_endpoint_ids)

    str_local_slices = {
        domain_uuid:grpc_message_list_to_json(endpoint_ids)
        for domain_uuid,endpoint_ids in local_slices.items()
    }
    LOGGER.debug('[compute_interdomain_sub_slices] local_slices={:s}'.format(str(str_local_slices)))

    str_remote_slices = {
        domain_uuid:grpc_message_list_to_json(endpoint_ids)
        for domain_uuid,endpoint_ids in remote_slices.items()
    }
    LOGGER.debug('[compute_interdomain_sub_slices] remote_slices={:s}'.format(str(str_remote_slices)))

    return local_slices, remote_slices
