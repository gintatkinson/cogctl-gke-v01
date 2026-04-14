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
import java.util.ArrayList;
import java.util.List;

public class UpdateMsg {
	
	private int AFI;
	private int asPathSegment;
	private InetAddress nextHop;
	private String learntFrom;
	
	private NodeNLRIMsg node;
	private LinkNLRIMsg link;
	private PathAttributeMsg path;
	private List <LinkNLRIMsg> linkList = new ArrayList<>();
	private List <NodeNLRIMsg> nodeList = new ArrayList<>();
	
	public List <LinkNLRIMsg> getLinkList(){
		return this.linkList;
	}
	public List <NodeNLRIMsg> getNodeList(){
		return this.nodeList;
	}
	public void addNode(NodeNLRIMsg node) {
		this.nodeList.add(node);
	}
	public int getAFI() {
		return AFI;
	}
	public String getLearntFrom() {
		return learntFrom;
	}
	public void setLearntFrom(String learntFrom) {
		this.learntFrom = learntFrom;
	}
	public void setAFI(int aFI) {
		AFI = aFI;
	}
	public int getAsPathSegment() {
		return asPathSegment;
	}
	public void setAsPathSegment(int asPathSegment) {
		this.asPathSegment = asPathSegment;
	}
	public InetAddress getNextHop() {
		return nextHop;
	}
	public void setNextHop(InetAddress nextHop) {
		this.nextHop = nextHop;
	}
	public NodeNLRIMsg getNode() {
		return node;
	}
	public void setNode(NodeNLRIMsg node) {
		this.node = node;
	}
	// public LinkNLRIMsg getLink() {
	// 	return link;
	// }
	public boolean linkCheck(){
		return linkList.size()>0;
	}
	public boolean nodeCheck(){
		return nodeList.size()>0;
	}
	public void setLink(LinkNLRIMsg link) {
		this.link = link;
	}
	public void addLink(LinkNLRIMsg link) {
		this.linkList.add(link);
	}
	public PathAttributeMsg getPath() {
		return path;
	}
	public void setPath(PathAttributeMsg path) {
		this.path = path;
	}

	
	
	
	
}
