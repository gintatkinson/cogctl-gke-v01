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
from typing import List, Optional, Set
from common.proto.context_pb2 import ContextId, Device, DeviceFilter, Empty, Topology, TopologyId
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

def get_device(
    context_client : ContextClient, device_uuid : str, rw_copy : bool = False,
    include_endpoints : bool = True, include_config_rules : bool = True, include_components : bool = True
) -> Optional[Device]:
    device_filter = DeviceFilter()
    device_id = device_filter.device_ids.device_ids.add() # pylint: disable=no-member
    device_id.device_uuid.uuid = device_uuid
    device_filter.include_endpoints = include_endpoints
    device_filter.include_config_rules = include_config_rules
    device_filter.include_components = include_components

    try:
        ro_devices = context_client.SelectDevice(device_filter)
        if len(ro_devices.devices) == 0: return None
        assert len(ro_devices.devices) == 1
        ro_device = ro_devices.devices[0]
        if not rw_copy: return ro_device
        rw_device = Device()
        rw_device.CopyFrom(ro_device)
        return rw_device
    except grpc.RpcError as e:
        if e.code() != grpc.StatusCode.NOT_FOUND: raise # pylint: disable=no-member
        #LOGGER.exception('Unable to get Device({:s})'.format(str(device_uuid)))
        return None

def get_existing_device_uuids(context_client : ContextClient) -> Set[str]:
    existing_device_ids = context_client.ListDeviceIds(Empty())
    existing_device_uuids = {device_id.device_uuid.uuid for device_id in existing_device_ids.device_ids}
    return existing_device_uuids

def get_devices(context_client : ContextClient) -> List[Device]:
    devices = context_client.ListDevices(Empty())
    return [d for d in devices.devices]

def add_device_to_topology(
    context_client : ContextClient, context_id : ContextId, topology_uuid : str, device_uuid : str
) -> bool:
    topology_id = TopologyId(**json_topology_id(topology_uuid, context_id=context_id))
    topology_ro = context_client.GetTopology(topology_id)
    device_uuids = {device_id.device_uuid.uuid for device_id in topology_ro.device_ids}
    if device_uuid in device_uuids: return False # already existed

    topology_rw = Topology()
    topology_rw.CopyFrom(topology_ro)
    topology_rw.device_ids.add().device_uuid.uuid = device_uuid # pylint: disable=no-member
    context_client.SetTopology(topology_rw)
    return True

def get_uuids_of_devices_in_topology(
    context_client : ContextClient, context_id : ContextId, topology_uuid : str
) -> List[str]:
    topology_id = TopologyId(**json_topology_id(topology_uuid, context_id=context_id))
    topology = context_client.GetTopology(topology_id)
    device_uuids = [device_id.device_uuid.uuid for device_id in topology.device_ids]
    return device_uuids

def get_devices_in_topology(
    context_client : ContextClient, context_id : ContextId, topology_uuid : str
) -> List[Device]:
    device_uuids = get_uuids_of_devices_in_topology(context_client, context_id, topology_uuid) 

    all_devices = context_client.ListDevices(Empty())
    devices_in_topology = list()
    for device in all_devices.devices:
        device_uuid = device.device_id.device_uuid.uuid
        if device_uuid not in device_uuids: continue
        devices_in_topology.append(device)

    return devices_in_topology
