// Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//      http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package eu.teraflow.tid.bgp4Peer.models;

import java.net.InetAddress;
import java.util.LinkedList;
import java.util.List;

public class UpdateMsgList {

	
	/* Print purposes and debug*/
	List<NodeNLRIMsg> nodeList = new LinkedList<>();
	List<LinkNLRIMsg> linkList = new LinkedList<>();
	List<PathAttributeMsg> pathList = new LinkedList<>();
	/**/
	public UpdateMsgList() {
	}


	public String toString() {
		
		String out ="Update Message: ";
		if(nodeList!=null) {
			out=out+nodeList.toString()+"\n";
		}
		if(linkList!=null) {
			out=out+linkList.toString()+"\n";
		}
		if(pathList!=null) {
			out=out+pathList.toString()+"\n";
		}
		
		return out;
		
	}
	public void addLinkToJson(LinkNLRIMsg link) {
		
		if(link==null)
			return;
		boolean exists = false;
		for (LinkNLRIMsg linkInList : linkList) {  // list being the LinkedList
		    if (link.equals(linkInList)) {
		        exists = true;
		        break;
		    }
		}
		if (!exists) {
			linkList.add(link);
		}
	}
	public void addNodeToJson(NodeNLRIMsg node, String currentName) {//comprobar que existe?
			
			if(node==null)
				return;
			boolean exists = false;
			for (NodeNLRIMsg nodeInList : nodeList) {  // list being the LinkedList
			    if (node.equals(nodeInList)) {
			        exists = true;
			        break;
			    }
			}
			if (!exists) {
				nodeList.add(node);
			}
			
		}
	public void addpathToJson(PathAttributeMsg path) {
			
			boolean exists = false;
			if(path.getNodeName()==null) {
				return;
			}
			for (PathAttributeMsg pathInList : pathList) {  // list being the LinkedList
			    if (path.equals(pathInList) ) {
			        exists = true;
			        break;
			    }
			}
			if (!exists) {
				pathList.add(path);
			}
			
		}
	
	public List<NodeNLRIMsg> getNodeList() {
		return nodeList;
	}

	public List<LinkNLRIMsg> getLinkList() {
		return linkList;
	}

	public List<PathAttributeMsg> getPathList() {
		return pathList;
	}

	public void addNodeToList(NodeNLRIMsg node) {
		nodeList.add(node);
	}
	public void addLinkToList(LinkNLRIMsg link) {
		linkList.add(link);
	}
	public void addPathToList(PathAttributeMsg path) {
		pathList.add(path);
	}
	
	public UpdateMsgList id2Name() {
		
		UpdateMsgList update=new UpdateMsgList();
		update.nodeList=this.nodeList;
		update.pathList=this.pathList;
		List<LinkNLRIMsg> newLinkList = new LinkedList<>();
		
		for (LinkNLRIMsg linkInList : linkList) {
			LinkNLRIMsg link=linkInList;
			
			for(NodeNLRIMsg nodeInList: update.nodeList) {	
				if((linkInList.getLocalBgplsID().equals(nodeInList.getLocalBgplsID()))) {
					link.setLocalBgplsID(nodeInList.getNodeName());
				}
			}
			
			for(NodeNLRIMsg nodeInList: update.nodeList) {	
				if((linkInList.getRemoteBgplsID().equals(nodeInList.getLocalBgplsID()))) {
					link.setRemoteBgplsID(nodeInList.getNodeName());
				}
			}
			
			
			newLinkList.add(link);
		}
		update.linkList=newLinkList;	
		
		return update;
		
	}

}
