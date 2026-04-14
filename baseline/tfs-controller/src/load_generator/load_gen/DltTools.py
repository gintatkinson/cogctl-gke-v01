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

import json, queue
from typing import Optional, Set, Tuple
from common.proto.context_pb2 import DeviceId, LinkId, ServiceId, SliceId, TopologyId
from common.proto.dlt_connector_pb2 import DltDeviceId, DltLinkId, DltServiceId, DltSliceId
from common.tools.grpc.Tools import grpc_message_to_json_string
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient
from dlt.connector.client.DltConnectorClient import DltConnectorClient

def explore_entities_to_record(
    slice_id : Optional[SliceId] = None, service_id : Optional[ServiceId] = None
) -> Tuple[Set[str], Set[str], Set[str]]:

    context_client = ContextClient()

    slices_to_record   : Set[str] = set()
    services_to_record : Set[str] = set()
    devices_to_record  : Set[str] = set()

    slices_to_explore = queue.Queue()
    services_to_explore = queue.Queue()
    if slice_id is not None: slices_to_explore.put(slice_id)
    if service_id is not None: services_to_explore.put(service_id)

    while not slices_to_explore.empty():
        slice_id = slices_to_explore.get()
        slices_to_record.add(grpc_message_to_json_string(slice_id))

        slice_ = context_client.GetSlice(slice_id)

        for endpoint_id in slice_.slice_endpoint_ids:
            devices_to_record.add(grpc_message_to_json_string(endpoint_id.device_id))
        for subslice_id in slice_.slice_subslice_ids:
            slices_to_explore.put(subslice_id)
        for service_id in slice_.slice_service_ids:
            services_to_explore.put(service_id)

    while not services_to_explore.empty():
        service_id = services_to_explore.get()
        services_to_record.add(grpc_message_to_json_string(service_id))

        service = context_client.GetService(service_id)

        for endpoint_id in service.service_endpoint_ids:
            devices_to_record.add(grpc_message_to_json_string(endpoint_id.device_id))

        connections = context_client.ListConnections(service_id)
        for connection in connections.connections:
            for endpoint_id in connection.path_hops_endpoint_ids:
                devices_to_record.add(grpc_message_to_json_string(endpoint_id.device_id))
            for service_id in connection.sub_service_ids:
                services_to_explore.put(service_id)

    return slices_to_record, services_to_record, devices_to_record

def record_device_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, device_id : DeviceId, delete : bool = False
) -> None:
    dlt_device_id = DltDeviceId()
    dlt_device_id.topology_id.CopyFrom(domain_id)       # pylint: disable=no-member
    dlt_device_id.device_id.CopyFrom(device_id)         # pylint: disable=no-member
    dlt_device_id.delete = delete
    dlt_connector_client.RecordDevice(dlt_device_id)

def record_link_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, link_id : LinkId, delete : bool = False
) -> None:
    dlt_link_id = DltLinkId()
    dlt_link_id.topology_id.CopyFrom(domain_id)         # pylint: disable=no-member
    dlt_link_id.link_id.CopyFrom(link_id)               # pylint: disable=no-member
    dlt_link_id.delete = delete
    dlt_connector_client.RecordLink(dlt_link_id)

def record_service_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, service_id : ServiceId, delete : bool = False
) -> None:
    dlt_service_id = DltServiceId()
    dlt_service_id.topology_id.CopyFrom(domain_id)      # pylint: disable=no-member
    dlt_service_id.service_id.CopyFrom(service_id)      # pylint: disable=no-member
    dlt_service_id.delete = delete
    dlt_connector_client.RecordService(dlt_service_id)

def record_slice_to_dlt(
    dlt_connector_client : DltConnectorClient, domain_id : TopologyId, slice_id : SliceId, delete : bool = False
) -> None:
    dlt_slice_id = DltSliceId()
    dlt_slice_id.topology_id.CopyFrom(domain_id)        # pylint: disable=no-member
    dlt_slice_id.slice_id.CopyFrom(slice_id)            # pylint: disable=no-member
    dlt_slice_id.delete = delete
    dlt_connector_client.RecordSlice(dlt_slice_id)

def record_entities(
    slices_to_record : Set[str] = set(), services_to_record : Set[str] = set(), devices_to_record : Set[str] = set(),
    delete : bool = False
) -> None:
    dlt_connector_client = DltConnectorClient()
    dlt_domain_id = TopologyId(**json_topology_id('dlt-perf-eval'))

    for str_device_id in devices_to_record:
        device_id = DeviceId(**(json.loads(str_device_id)))
        record_device_to_dlt(dlt_connector_client, dlt_domain_id, device_id, delete=delete)

    for str_service_id in services_to_record:
        service_id = ServiceId(**(json.loads(str_service_id)))
        record_service_to_dlt(dlt_connector_client, dlt_domain_id, service_id, delete=delete)

    for str_slice_id in slices_to_record:
        slice_id = SliceId(**(json.loads(str_slice_id)))
        record_slice_to_dlt(dlt_connector_client, dlt_domain_id, slice_id, delete=delete)
