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

import grpc
from typing import List, Optional, Set
from common.proto.context_pb2 import ContextId, Empty, Link, LinkId, Topology, TopologyId
from common.tools.object_factory.Topology import json_topology_id
from context.client.ContextClient import ContextClient

def get_link(context_client : ContextClient, link_uuid : str, rw_copy : bool = False) -> Optional[Link]:
    try:
        # pylint: disable=no-member
        link_id = LinkId()
        link_id.link_uuid.uuid = link_uuid
        ro_link = context_client.GetLink(link_id)
        if not rw_copy: return ro_link
        rw_link = Link()
        rw_link.CopyFrom(ro_link)
        return rw_link
    except grpc.RpcError:
        #LOGGER.exception('Unable to get Link({:s})'.format(str(link_uuid)))
        return None

def get_existing_link_uuids(context_client : ContextClient) -> Set[str]:
    existing_link_ids = context_client.ListLinkIds(Empty())
    existing_link_uuids = {link_id.link_uuid.uuid for link_id in existing_link_ids.link_ids}
    return existing_link_uuids

def get_links(context_client : ContextClient) -> List[Link]:
    links = context_client.ListLinks(Empty())
    return [l for l in links.links]

def add_link_to_topology(
    context_client : ContextClient, context_id : ContextId, topology_uuid : str, link_uuid : str
) -> bool:
    topology_id = TopologyId(**json_topology_id(topology_uuid, context_id=context_id))
    topology_ro = context_client.GetTopology(topology_id)
    link_uuids = {link_id.link_uuid.uuid for link_id in topology_ro.link_ids}
    if link_uuid in link_uuids: return False # already existed

    topology_rw = Topology()
    topology_rw.CopyFrom(topology_ro)
    topology_rw.link_ids.add().link_uuid.uuid = link_uuid # pylint: disable=no-member
    context_client.SetTopology(topology_rw)
    return True

def get_uuids_of_links_in_topology(
    context_client : ContextClient, context_id : ContextId, topology_uuid : str
) -> List[str]:
    topology_id = TopologyId(**json_topology_id(topology_uuid, context_id=context_id))
    topology = context_client.GetTopology(topology_id)
    link_uuids = [link_id.link_uuid.uuid for link_id in topology.link_ids]
    return link_uuids

def get_links_in_topology(
    context_client : ContextClient, context_id : ContextId, topology_uuid : str
) -> List[Link]:
    link_uuids = get_uuids_of_links_in_topology(context_client, context_id, topology_uuid) 

    all_links = context_client.ListLinks(Empty())
    links_in_topology = list()
    for link in all_links.links:
        link_uuid = link.link_id.link_uuid.uuid
        if link_uuid not in link_uuids: continue
        links_in_topology.append(link)

    return links_in_topology
