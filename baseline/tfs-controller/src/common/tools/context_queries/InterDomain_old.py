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

from common.tools.context_queries.Device import get_device #, get_devices_in_topology

## DEPRECATED
#def get_local_domain_devices(context_client : ContextClient) -> List[Device]:
#    local_device_uuids = get_local_device_uuids(context_client)
#    all_devices = context_client.ListDevices(Empty())
#    local_domain_devices = list()
#    for device in all_devices.devices:
#        if not device_type_is_network(device.device_type): continue
#        device_uuid = device.device_id.device_uuid.uuid
#        if device_uuid not in local_device_uuids: continue
#        local_domain_devices.append(device)
#    return local_domain_devices

## DEPRECATED
#def is_multi_domain(context_client : ContextClient, endpoint_ids : List[EndPointId]) -> bool:
#    local_device_uuids = get_local_device_uuids(context_client)
#    LOGGER.debug('[is_multi_domain] local_device_uuids={:s}'.format(str(local_device_uuids)))
#    remote_endpoint_ids = [
#        endpoint_id
#        for endpoint_id in endpoint_ids
#        if endpoint_id.device_id.device_uuid.uuid not in local_device_uuids
#    ]
#    str_remote_endpoint_ids = [
#        (endpoint_id.device_id.device_uuid.uuid, endpoint_id.endpoint_uuid.uuid)
#        for endpoint_id in remote_endpoint_ids
#    ]
#    LOGGER.debug('[is_multi_domain] remote_endpoint_ids={:s}'.format(str(str_remote_endpoint_ids)))
#    is_multi_domain_ = len(remote_endpoint_ids) > 0
#    LOGGER.debug('[is_multi_domain] is_multi_domain={:s}'.format(str(is_multi_domain_)))
#    return is_multi_domain_

## DEPRECATED
#def compute_interdomain_path(
#    pathcomp_client : PathCompClient, slice_ : Slice
#) -> List[Tuple[str, List[EndPointId]]]:
#    context_uuid = slice_.slice_id.context_id.context_uuid.uuid
#    slice_uuid = slice_.slice_id.slice_uuid.uuid
#
#    pathcomp_req = PathCompRequest()
#    pathcomp_req.shortest_path.Clear()                                          # pylint: disable=no-member
#    pathcomp_req_svc = pathcomp_req.services.add()                              # pylint: disable=no-member
#    pathcomp_req_svc.service_id.context_id.context_uuid.uuid = context_uuid
#    pathcomp_req_svc.service_id.service_uuid.uuid = slice_uuid
#    pathcomp_req_svc.service_type = ServiceTypeEnum.SERVICETYPE_L2NM
#
#    for endpoint_id in slice_.slice_endpoint_ids:
#        service_endpoint_id = pathcomp_req_svc.service_endpoint_ids.add()
#        service_endpoint_id.CopyFrom(endpoint_id)
#    
#    constraint_sla_capacity = pathcomp_req_svc.service_constraints.add()
#    constraint_sla_capacity.sla_capacity.capacity_gbps = 10.0
#
#    constraint_sla_latency = pathcomp_req_svc.service_constraints.add()
#    constraint_sla_latency.sla_latency.e2e_latency_ms = 100.0
#
#    LOGGER.debug('pathcomp_req = {:s}'.format(grpc_message_to_json_string(pathcomp_req)))
#    pathcomp_rep = pathcomp_client.Compute(pathcomp_req)
#    LOGGER.debug('pathcomp_rep = {:s}'.format(grpc_message_to_json_string(pathcomp_rep)))
#
#    service = next(iter([
#        service
#        for service in pathcomp_rep.services
#        if service.service_id.service_uuid.uuid == pathcomp_req_svc.service_id.service_uuid.uuid
#    ]), None)
#    if service is None:
#        str_service_id = grpc_message_to_json_string(pathcomp_req_svc.service_id)
#        raise Exception('Service({:s}) not found'.format(str_service_id))
#
#    connection = next(iter([
#        connection
#        for connection in pathcomp_rep.connections
#        if connection.service_id.service_uuid.uuid == pathcomp_req_svc.service_id.service_uuid.uuid
#    ]), None)
#    if connection is None:
#        str_service_id = grpc_message_to_json_string(pathcomp_req_svc.service_id)
#        raise Exception('Connection for Service({:s}) not found'.format(str_service_id))
#
#    domain_list : List[str] = list()
#    domain_to_endpoint_ids : Dict[str, List[EndPointId]] = dict()
#    for endpoint_id in connection.path_hops_endpoint_ids:
#        device_uuid = endpoint_id.device_id.device_uuid.uuid
#        #endpoint_uuid = endpoint_id.endpoint_uuid.uuid
#        if device_uuid not in domain_to_endpoint_ids: domain_list.append(device_uuid)
#        domain_to_endpoint_ids.setdefault(device_uuid, []).append(endpoint_id)
#
#    return [
#        (domain_uuid, domain_to_endpoint_ids.get(domain_uuid))
#        for domain_uuid in domain_list
#    ]

## DEPRECATED
#def compute_traversed_domains(
#    context_client : ContextClient, interdomain_path : List[Tuple[str, List[EndPointId]]]
#) -> List[Tuple[str, bool, List[EndPointId]]]:
#
#    local_device_uuids = get_local_device_uuids(context_client)
#    LOGGER.debug('[compute_traversed_domains] local_device_uuids={:s}'.format(str(local_device_uuids)))
#
#    #interdomain_devices = get_devices_in_topology(context_client, ADMIN_CONTEXT_ID, INTERDOMAIN_TOPOLOGY_NAME)
#    #interdomain_devices = {
#    #    device.device_id.device_uuid.uuid : device
#    #    for device in interdomain_devices
#    #}
#
#    devices_to_domains = get_device_to_domain_map(context_client)
#    LOGGER.debug('[compute_traversed_domains] devices_to_domains={:s}'.format(str(devices_to_domains)))
#
#    traversed_domains : List[Tuple[str, bool, List[EndPointId]]] = list()
#    domains_dict : Dict[str, Tuple[str, bool, List[EndPointId]]] = dict()
#    for device_uuid, endpoint_ids in interdomain_path:
#        domain_uuid = devices_to_domains.get(device_uuid, '---')
#        domain = domains_dict.get(domain_uuid)
#        if domain is None:
#            is_local_domain = domain_uuid in local_device_uuids
#            domain = (domain_uuid, is_local_domain, [])
#            traversed_domains.append(domain)
#            domains_dict[domain_uuid] = domain
#        domain[2].extend(endpoint_ids)
#
#    str_traversed_domains = [
#        (domain_uuid, is_local_domain, [
#            (endpoint_id.device_id.device_uuid.uuid, endpoint_id.endpoint_uuid.uuid)
#            for endpoint_id in endpoint_ids
#        ])
#        for domain_uuid,is_local_domain,endpoint_ids in traversed_domains
#    ]
#    LOGGER.debug('[compute_traversed_domains] devices_to_domains={:s}'.format(str(str_traversed_domains)))
#    return traversed_domains
