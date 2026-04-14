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

import grpc, json, logging
from typing import List, Tuple, Union
from bgpls_speaker.service.tools.DiscoveredDBManager import  DiscoveredDBManager, GetContextDevices, getEndpointFromIpInterface
from bgpls_speaker.service.tools.GrpcServer import GrpcServer
from common.method_wrappers.Decorator import MetricsPool, safe_and_metered_rpc_method
from common.proto.context_pb2 import DeviceId, Empty, EndPointId, Link, LinkId, Uuid
from context.client.ContextClient import ContextClient
from common.proto.bgpls_pb2 import (
    BgplsSpeaker, BgplsSpeakerId, DiscoveredDeviceList, DiscoveredDevice,
    DiscoveredLink, DiscoveredLinkList, NodeDescriptors, BgplsSpeakerList
)
from common.proto.bgpls_pb2_grpc import BgplsServiceServicer

LOGGER = logging.getLogger(__name__)

METRICS_POOL = MetricsPool('Service', 'RPC')

class BgplsServiceServicerImpl(BgplsServiceServicer):
    def __init__(self,discoveredDB : DiscoveredDBManager,
                 speakerServer : GrpcServer) -> None:
        LOGGER.debug('Creating Servicer...')
        self.speaker_handler_factory = 1
        self.speaker_server=speakerServer
        self.discoveredDB=discoveredDB
        LOGGER.debug('Servicer Created')
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListDiscoveredDevices(self, request : Empty, context : grpc.ServicerContext) -> DiscoveredDeviceList:
        """
        Get devices discovered from bgpls protocol
        """
        device_names=self.discoveredDB.GetNodeNamesFromDiscoveredDB()
        nodes = self.discoveredDB.GetNodesFromDiscoveredDB()
        devices = [DiscoveredDevice(nodeName=node.node_name,igpID=node.igp_id,learntFrom=node.learnt_from) for node in nodes]
        return DiscoveredDeviceList(discovereddevices=devices)

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListDiscoveredLinks(self, request : Empty, context : grpc.ServicerContext) -> DiscoveredLinkList:
        """
        Get links discovered from bgpls protocol
        """
        self.discoveredDB.UpdateNodeNameInLink()
        links = self.discoveredDB.GetLinksFromDiscoveredDB()
        links_info=[]
        for link in links:
            local=NodeDescriptors(igp_id=link.local_id,nodeName=link.local_id)
            remote=NodeDescriptors(igp_id=link.remote_id,nodeName=link.remote_id)
            links_info.append(DiscoveredLink(local=local,remote=remote,learntFrom=link.learnt_from,
                                             local_ipv4=link.local_ipv4_id,remote_ipv4=link.remote_ipv4_id))
        return DiscoveredLinkList(discoveredlinks=links_info)
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def AddBgplsSpeaker(self, request : BgplsSpeaker, context : grpc.ServicerContext) -> BgplsSpeakerId:
        """
        Creates a new connection with an speaker with the given ip address, port and as.
        Returns de id of the speaker created (to kill proccess¿)
        """
        LOGGER.debug("(AddBgplsSpeaker) Create speaker instance %s",request)

        speaker_id=self.speaker_server.connectToJavaBgpls(request.address,request.port,request.asNumber)
        return BgplsSpeakerId(id=speaker_id)
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def ListBgplsSpeakers(self, request : Empty, context : grpc.ServicerContext) -> BgplsSpeakerId:
        """
        Returns a list of the IDs of the BGP-LS speakers with open connections. 
        """
        speaker_list=[]
        bgpls_speaker_list=[]
        speaker_list=self.speaker_server.getSpeakerListIds()
        for speaker in speaker_list:
            bgpls_speaker_list.append(BgplsSpeakerId(id=speaker))
        return BgplsSpeakerList(speakers=bgpls_speaker_list)
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def DisconnectFromSpeaker(self, request : BgplsSpeaker, context : grpc.ServicerContext) -> bool:
        """
        Disconencts from the BGP-LS speaker given its ipv4 address.
        """
        speaker_id=self.speaker_server.getSpeakerIdFromIpAddr(request.address)
        self.speaker_server.terminateRunnerById(speaker_id)
        return Empty()

    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def GetSpeakerInfoFromId(self, request : BgplsSpeakerId, context : grpc.ServicerContext) -> BgplsSpeaker:
        """
        Get the address, port and as number of the speaker given its id.
        """
        address,as_number,port=self.speaker_server.getSpeakerFromId(request.id)
        return BgplsSpeaker(address=address,port=port,asNumber=as_number)
    
    @safe_and_metered_rpc_method(METRICS_POOL, LOGGER)
    def NotifyAddNodeToContext(self, request : DiscoveredDevice, context : grpc.ServicerContext) :
        """
        When a node is added to context via bgpls module this function checks if there are other nodes in the
        topology connected by links discovered via bgpls. Then, if the link exist adds it to the context.
        """
        node_name=request.nodeName
        node_igp=self.discoveredDB.GetIgpIdFromNodeName(node_name)
        LOGGER.debug("(NotifyAddNodeToContext) Find links to nodes %s:%s",node_name,node_igp)
        # Get nodes connected and links were the igpID appears
        nodes_conected, links_local, links_remote=self.discoveredDB.FindConnectedNodes(node_igp)
        o=[LOGGER.debug("(NotifyAddNodeToContext) Links local: %s %s",link_local.local_id, link_local.remote_id) for link_local in links_local]
        o=[LOGGER.debug("(NotifyAddNodeToContext) Links remote: %s %s",links_remote.local_id,links_remote.remote_id) for links_remote in links_remote]
        # Check if nodes are in context
        context_client=ContextClient()
        context_client.connect()
        # devices=context_client.ListDevices(Empty())
        device_names,devices_ips=GetContextDevices(context_client)
        LOGGER.debug("(NotifyAddNodeToContext) Devices in context: %s", device_names)
        LOGGER.debug("(NotifyAddNodeToContext) Nodes conected in context: %s", nodes_conected)
        nodes_conected_in_context=list(set(nodes_conected) & set(device_names))
        LOGGER.debug("(NotifyAddNodeToContext) nodes_conected_in_context: %s", nodes_conected_in_context)
        # TODO: next to function
        for remote_node in nodes_conected_in_context:
            LOGGER.info("(NotifyAddNodeToContext) creating link to...: %s", remote_node)
            remote_igp=self.discoveredDB.GetIgpIdFromNodeName(remote_node)
            # Get source device from name
            device_uuid_src=DeviceId(device_uuid=Uuid(uuid=node_name))
            device_src=context_client.GetDevice(device_uuid_src)

            # Get destination device from name
            device_uuid_dest=DeviceId(device_uuid=Uuid(uuid=remote_node))
            device_dest=context_client.GetDevice(device_uuid_dest)
            
            # Here I assume one link will always have same link in other direction
            # First direction for link
            # Get endpoints associated to link between devices
            for link_local in links_local:
                LOGGER.debug("(NotifyAddNodeToContext) local: %s %s", link_local.local_id,link_local.remote_id)
                LOGGER.debug("(NotifyAddNodeToContext) matches: %s %s", node_igp,remote_igp)
                if link_local.local_id == node_igp and link_local.remote_id == remote_igp:
                    LOGGER.debug("(NotifyAddNodeToContext) local_ipv4_id: %s", link_local.local_ipv4_id)
                    end_point1,ip_1=getEndpointFromIpInterface(device_src,link_local.local_ipv4_id)
                    LOGGER.debug("(NotifyAddNodeToContext) end_point1: %s", end_point1)

                    LOGGER.debug("(NotifyAddNodeToContext) remote_ipv4_id: %s", link_local.remote_ipv4_id)
                    end_point2,ip_2=getEndpointFromIpInterface(device_dest,link_local.remote_ipv4_id)
                    LOGGER.debug("(NotifyAddNodeToContext) end_point2: %s", end_point2)
                # LOGGER.debug("(NotifyAddNodeToContext) Source: %s Destination: %s", end_point1,end_point2)
                    
                    link_name_src_dest=node_name+"/"+end_point1+"=="+remote_node+"/"+end_point2

                    end_point_uuid1=Uuid(uuid=end_point1)
                    end_point_uuid2=Uuid(uuid=end_point2)

                    end_point_id1=EndPointId(endpoint_uuid=end_point_uuid1,device_id=device_uuid_src)

                    link_name_dest_src=remote_node+"/"+end_point2+"=="+node_name+"/"+end_point1

                    end_point_id2=EndPointId(endpoint_uuid=end_point_uuid2,device_id=device_uuid_dest)

                    end_point_ids_src_dest=[end_point_id1,end_point_id2]
                    end_point_ids_dest_src=[end_point_id2,end_point_id1]

                    link_id_src=context_client.SetLink(Link(link_id=LinkId(link_uuid=Uuid(uuid=link_name_src_dest)),
                                                            link_endpoint_ids=end_point_ids_src_dest))
                    
                    link_id_dst=context_client.SetLink(Link(link_id=LinkId(link_uuid=Uuid(uuid=link_name_dest_src)),
                                                            link_endpoint_ids=end_point_ids_dest_src))

            LOGGER.debug("(NotifyAddNodeToContext) Link set id src--->dst: %s", link_id_src)
        context_client.close()
        return Empty()
