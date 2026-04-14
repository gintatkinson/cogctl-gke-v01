# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Tuple, Union
from bgpls_speaker.service.tools.Tools import UpdateRequest,NodeInfo,LinkInfo
from common.proto.bgpls_pb2 import NodeDescriptors
from common.proto.context_pb2 import ContextId, ContextList,Topology,TopologyId,Device,DeviceDriverEnum,ContextId,Empty, TopologyList
from common.Constants import DEFAULT_CONTEXT_NAME
from common.tools.object_factory.Context import json_context_id
from context.client.ContextClient import ContextClient

import logging,json
LOGGER = logging.getLogger(__name__)

def json_to_list(json_str : str) -> List[Union[str, Tuple[str, str]]]:
    try:
        data = json.loads(json_str)
    except: # pylint: disable=bare-except
        return [('item', str(json_str))]

    if isinstance(data, dict):
        return [('kv', (key, value)) for key, value in data.items()]
    elif isinstance(data, list):
        return [('item', ', '.join(data))]
    else:
        return [('item', str(data))]
    
class DiscoveredDBManager:
    def __init__(self):
        self.discoveredDB=[]
        # Añadir topoDB

    def AddToDB(self,update_request : UpdateRequest):
        """
        Add BGP Update message to discoveredDB. Checks if node exists in discoveredDB.
        TODO: check if node exists in context
        """
        # TODO: with self.lock
        # Check if node info message
        if(self.checkIfNodeInUpdate(update_request)):
            # Check if node exists
            node_count=len(update_request.nodes)
            for node in update_request.nodes:
                if(self.CheckIfNodeNameInDb(node) or CheckIfNodeInContext(node.node_name)):
                    # Replace info from node if exists
                    LOGGER.debug("(AddToDB) Node already in DB!!!")
                    update_request.nodes.remove(node)
                    node_count=node_count-1
                else:
                    LOGGER.debug("(AddToDB) Node NOT in DB!!!")
            if(node_count>0):
                self.discoveredDB.append(update_request)
        else:
            # is a link
            # Compare and update
            self.discoveredDB.append(update_request)
            LOGGER.debug("(AddToDB) Actual DB: ")
            LOGGER.debug("%s", [up.toString() for up in self.discoveredDB])
        return True
    
    def GetDiscoveredDB(self):
        return self.discoveredDB
    
    def checkIfNodeInUpdate(self,update_request : UpdateRequest):
        """
        Returns true if the update message contains a node info type .
        """
        if(update_request.nodes):
            return True
        return False
    
    
    def CheckIfNodeNameInDb(self,new_node : NodeInfo) -> bool:
        """
        Returns true if new node is in the discovered data base already
        """
        for update in self.discoveredDB:
            for node in update.nodes:
                if(node.igp_id==new_node.igp_id):
                    return True
        return False
    
    def GetNodeNamesFromDiscoveredDB(self):
        """
        Return a list of node_names from the current discovered devices
        saved in the discoveredDB
        """
        node_list =[update_request.nodes for update_request in self.discoveredDB if update_request.nodes]
        # LOGGER.info("nodes (GetNodeNamesFromDiscoveredDB) %s",node_list )
        # Inside an update there is a list of nodes , TODO posible FIX:
        node_info= [node for nodes in node_list for node in nodes]
        return [node.node_name for node in node_info]
    
    def GetNodesFromDiscoveredDB(self):
        """
        Return a list of nodes of class type: tools.NodeInfo from the current discovered devices
        saved in the discoveredDB. Skips the ones already addded to context.
        """

        node_list =[update_request.nodes for update_request in self.discoveredDB if update_request.nodes]
        return [node for nodes in node_list for node in nodes if (not CheckIfNodeInContext(node.node_name))]
    
    def GetLinksFromDiscoveredDB(self):
        """
        Return a list of links of class type: tools.LinkInfo from the current discovered links
        saved in the discoveredDB
        """
        link_list= [update_request.links for update_request in self.discoveredDB if update_request.links]
        return [link for links in link_list for link in links]
    
    def UpdateDiscoveredDBWithContext(self):
        """
        Check if device discovered by bgpls is already in the topology.
        """
        # device_names,device_ips=AddContextDevices(context_client)
        return True
    
    def GetNodeNameFromLinkId(self,link_igpid):
        """
        Return the node name given an igp id if exists in the discoveredDB.   
        """
        for update in self.discoveredDB:
            for node in update.nodes:
                if(node.igp_id==link_igpid):
                    return node.node_name
        return None
    
    def GetIgpIdFromNodeName(self,name):
        """
        Return the IGP ID given a node name if exists in the discoveredDB.   
        """
        for update in self.discoveredDB:
            LOGGER.debug("(GetIgpIdFromNodeName)checking update: %s",update.toString())
            for node in update.nodes:
                LOGGER.debug("(GetIgpIdFromNodeName)checking nodes: %s",node.node_name)
                if(node.node_name==name):
                    return node.igp_id
        return None
    
    def UpdateNodeNameInLink(self):
        """
        Check if the igp id has a node name asigned in the discoveredDB and
        assign it to the NodeDescriptor name.
        """
        for update in self.discoveredDB:
            for link in update.links:
                if(self.GetNodeNameFromLinkId(link.local_id) is not None):
                    LOGGER.info("(UpdateNodeNameInLink) local %s:  %s",link.local_id, self.GetNodeNameFromLinkId(link.local_id))
                    link.local.node_name=self.GetNodeNameFromLinkId(link.local_id)
                else:
                     link.local.node_name=link.local_id
                if(self.GetNodeNameFromLinkId(link.remote_id) is not None):
                    LOGGER.info("(UpdateNodeNameInLink) remote %s:  %s",link.remote_id, self.GetNodeNameFromLinkId(link.remote_id))
                    link.remote.node_name=self.GetNodeNameFromLinkId(link.remote_id)
                else:
                    link.remote.node_name=link.remote_id
        return True

    def RemoveLinkFromDB(self):
        """
        Removes a link from the DB if matches the source and the destination.
        """
        return True
    
    def FindConnectedNodes(self,new_node):
        """
        Returns a list of nodes connected to the actual node using the discovered 
        link list and comparing de IGP ID. Returns None in case there are no connections.
        """
        # find links where the node appears
        links_to_node=[]
        nodes_conected=[]
        link_local=[]
        link_remote=[]
        for update in self.discoveredDB:
            for link in update.links:
                LOGGER.debug("(FindConnectedNodes) link in up:%s %s",
                             link.local_id, link.remote_id)
                LOGGER.debug("(FindConnectedNodes) comparing ...:%s",new_node)
                if(link.local_id == new_node):
                    links_to_node.append(link)
                    nodes_conected.append(link.remote.node_name)
                    link_local.append(link)
                if(link.remote_id == new_node):
                    links_to_node.append(link)
                    nodes_conected.append(link.local.node_name)
                    link_remote.append(link)
        
        if(nodes_conected):
            LOGGER.debug("(FindConnectedNodes) links to local node:%s",new_node)
            LOGGER.debug("(FindConnectedNodes) %s", nodes_conected)
            return nodes_conected, link_local, link_remote
        LOGGER.debug("(FindConnectedNodes) NO LINKS TO OTHER NODES")
        return None

    def DeleteNodeFromDiscoveredDB(self, node_name) -> bool:
        """
        Deletes a node from de DiscoveredDB given the node name. TODO: igpid¿
        """
        LOGGER.info("(DeleteNodeFromDiscoveredDB)")
        
        for i,update in enumerate(self.discoveredDB):
            for node in update.nodes:
                if(node_name==node.node_name):
                    del self.discoveredDB[i]
        return True

def AddContextDevicesFull(context_client : ContextClient) -> bool:
    """
    debug purposes
    """
    LOGGER.info("(AddContextDevices)")
    contexts : ContextList = context_client.ListContexts(Empty())
    for context_ in contexts.contexts:
        context_uuid : str = context_.context_id.context_uuid.uuid
        context_name : str = context_.name
        topologies : TopologyList = context_client.ListTopologies(context_.context_id)
    # topologies : TopologyList=context_client.ListTopologies(context_client)
        for topology_ in topologies.topologies:
            #topology_uuid : str = topology_.topology_id.topology_uuid.uuid
            topology_name : str = topology_.name
            context_topology_name  = 'Context({:s}):Topology({:s})'.format(context_name, topology_name)
            # Topos=context.GetTopology(list_topo.topology_id)
            LOGGER.debug("topo (AddContextDevices) %s",topology_)
            # details=context_client.GetTopologyDetails(topology_.topology_id)
            # LOGGER.info("details (AddContextDevices) %s",details)
            devices=context_client.ListDevices(Empty())
            # LOGGER.info("devices (driverSettings) %s",devices)
            device_names=[]
            device_ips=[]
            for device_ in devices.devices:
                LOGGER.info("device_ (AddContextDevices) %s",device_.name)
                device_names.append(device_.name)
                for config_rule_ in device_.device_config.config_rules:
                    if config_rule_.custom.resource_key == "_connect/address":
                        LOGGER.info("device_.resource_value-addr (driverSettings) %s",
                        config_rule_.custom.resource_value)
                        device_ips=config_rule_.custom.resource_value
                        
        return device_names,device_ips

def GetContextDevices(context_client : ContextClient) -> bool:
    """
    Returns de device name and its corresponding device_ip existing in context.
    """
    LOGGER.info("(AddContextDevices)")
    devices=context_client.ListDevices(Empty())
    device_names=[]
    device_ips=[]
    for device_ in devices.devices:
        LOGGER.debug("device_ (AddContextDevices) %s",device_.name)
        device_names.append(device_.name)
        for config_rule_ in device_.device_config.config_rules:
            if config_rule_.custom.resource_key == "_connect/address":
                # LOGGER.info("device_.resource_value-addr (driverSettings) %s",
                # config_rule_.custom.resource_value)
                device_ips=config_rule_.custom.resource_value
                    
    return device_names,device_ips

def CheckIfNodeInContext(node_name) -> bool:
    """
    Returns true if the node exists in the context.
    """
    context_client=ContextClient()
    context_client.connect()
    device_names,device_ips=GetContextDevices(context_client)
    LOGGER.info("(CheckIfNodeInContext) device_names: %s nodena %s",device_names,node_name)
    for node in device_names:
        if(node==node_name):
            LOGGER.info("(CheckIfNodeInContext) Node already in context")
            return True
    LOGGER.info("(CheckIfNodeInContext) Node NOT in context")
    return False

def getEndpointFromIpInterface(device,ipv4):
    """
    Get TFS endpoint uuid drom given device having the IPv4 interface.
    """
    for config in device.device_config.config_rules:
        if config.WhichOneof('config_rule') == 'custom':
            # for item_type, item in json_to_list(config.custom.resource_value):
            #     if item_type == 'kv':
            #         # LOGGER.debug("(getEndpointFromIpInterface) item: %s",item)
            #         endpoint_item=item
            # LOGGER.debug("(getEndpointFromIpInterface) config: %s",config.custom.resource_key)
            if "/interface" in config.custom.resource_key:
                iface=config.custom.resource_key.split("/interface")[1].strip("[]")
                LOGGER.debug("(getEndpointFromIpInterface) interface: %s",iface)
                if ipv4 in config.custom.resource_value:
                    LOGGER.debug("(getEndpointFromIpInterface) value: %s",config.custom.resource_value)
                    resource_dict=json.loads(config.custom.resource_value)
                    interface = resource_dict['name']
                    resource_ip=resource_dict['address_ip']
    # Search for endpoint uuid assigned to interface
    for config in device.device_config.config_rules:
        if config.WhichOneof('config_rule') == 'custom':
            if "/endpoints/endpoint" in config.custom.resource_key:
                key=config.custom.resource_key.split("/endpoints/endpoint")[1].strip("[]")
                LOGGER.debug("(getEndpointFromIpInterface) key: %s",key)
                if interface in key:
                    LOGGER.debug("(getEndpointFromIpInterface) value: %s",config.custom.resource_value)
                    endpoint=config.custom.resource_key.split("/endpoints/endpoint")[1].strip("[]")
                    resource_dict_endpoint=json.loads(config.custom.resource_value)
                    return resource_dict_endpoint['uuid'],resource_ip
                
    return None,ipv4