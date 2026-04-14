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
from common.proto.context_pb2 import ContextId, Topology, TopologyDetails, TopologyId
from common.tools.object_factory.Context import json_context_id
from common.tools.object_factory.Topology import json_topology
from context.client.ContextClient import ContextClient

LOGGER = logging.getLogger(__name__)

def create_topology(
    context_client : ContextClient, context_uuid : str, topology_uuid : str, name : Optional[str] = None
) -> None:
    context_id = ContextId(**json_context_id(context_uuid))
    existing_topology_ids = context_client.ListTopologyIds(context_id)
    existing_topology_uuids = {topology_id.topology_uuid.uuid for topology_id in existing_topology_ids.topology_ids}
    if topology_uuid in existing_topology_uuids: return
    context_client.SetTopology(Topology(**json_topology(topology_uuid, context_id=context_id, name=name)))

def create_missing_topologies(
    context_client : ContextClient, context_id : ContextId, topology_uuids : List[str]
) -> None:
    # Find existing topologies within own context
    existing_topology_ids = context_client.ListTopologyIds(context_id)
    existing_topology_uuids = {topology_id.topology_uuid.uuid for topology_id in existing_topology_ids.topology_ids}

    # Create topologies within provided context
    for topology_uuid in topology_uuids:
        if topology_uuid in existing_topology_uuids: continue
        grpc_topology = Topology(**json_topology(topology_uuid, context_id=context_id))
        context_client.SetTopology(grpc_topology)

def get_topology(
        context_client : ContextClient, topology_uuid : str, context_uuid : str = DEFAULT_CONTEXT_NAME,
        rw_copy : bool = False
    ) -> Optional[Topology]:
    try:
        # pylint: disable=no-member
        topology_id = TopologyId()
        topology_id.context_id.context_uuid.uuid = context_uuid
        topology_id.topology_uuid.uuid = topology_uuid
        ro_topology = context_client.GetTopology(topology_id)
        if not rw_copy: return ro_topology
        rw_topology = Topology()
        rw_topology.CopyFrom(ro_topology)
        return rw_topology
    except grpc.RpcError:
        #LOGGER.exception('Unable to get topology({:s} / {:s})'.format(str(context_uuid), str(topology_uuid)))
        return None

def get_topologies(
        context_client : ContextClient, context_uuid : str = DEFAULT_CONTEXT_NAME
    ) -> List[Topology]:
    context_id = ContextId()
    context_id.context_uuid.uuid = context_uuid
    topologies = context_client.ListTopologies(context_id)
    return [t for t in topologies.topologies]

def get_topology_details(
        context_client : ContextClient, topology_uuid : str, context_uuid : str = DEFAULT_CONTEXT_NAME,
        rw_copy : bool = False
    ) -> Optional[TopologyDetails]:
    try:
        # pylint: disable=no-member
        topology_id = TopologyId()
        topology_id.context_id.context_uuid.uuid = context_uuid
        topology_id.topology_uuid.uuid = topology_uuid
        ro_topology_details = context_client.GetTopologyDetails(topology_id)
        if not rw_copy: return ro_topology_details
        rw_topology_details = TopologyDetails()
        rw_topology_details.CopyFrom(ro_topology_details)
        return rw_topology_details
    except grpc.RpcError:
        #LOGGER.exception('Unable to get topology({:s} / {:s})'.format(str(context_uuid), str(topology_uuid)))
        return None
