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

import java.net.Inet4Address;
import java.net.InetAddress;
import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.net.InetAddresses;

import es.tid.bgp.bgp4.update.fields.LinkNLRI;
import es.tid.bgp.bgp4.update.fields.NodeNLRI;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.NodeDescriptorsSubTLV;

public class NodeNLRIMsg {

	private ArrayList<NodeDescriptorsSubTLV> nodeDescriptorsSubTLV;
	// Dominios
	private Inet4Address localDomainID;
	private Inet4Address remoteDomainID;
	private Inet4Address areaID;
	private Inet4Address bgplsID;

	private Inet4Address LocalNodeBGPId;

	private Inet4Address iPv4RouterIDLocalNodeLATLV;
	private Inet4Address iPv4RouterIDNeighborNodeLATLV;

	private String localBgplsID;
	private int remoteBgplsID;

	private Inet4Address as_number;

	private int IGP_type;
	private Inet4Address IGPID = null;
	private Logger log;
	private String nodeName;
	private String ISIS_ID_str;
	private String router_id="-";

	private String learntFrom;

	public NodeNLRIMsg(NodeNLRI nodeNLRI, String learntFrom, String nodeName) {

		log = LoggerFactory.getLogger("BGP4Server");// prueba logger

		this.learntFrom = learntFrom;

		if (nodeNLRI.getLocalNodeDescriptors().getAutonomousSystemSubTLV() != null) {
			// inetAddr???
			as_number = nodeNLRI.getLocalNodeDescriptors().getAutonomousSystemSubTLV().getAS_ID();
		}
		if (nodeNLRI.getLocalNodeDescriptors().getAreaID() != null) {
			areaID = nodeNLRI.getLocalNodeDescriptors().getAreaID().getAREA_ID();
		}
		if (nodeNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV() != null) {
			localBgplsID=nodeNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV().getBGPLS_ID().toString();
		}

		if (nodeNLRI.getLocalNodeDescriptors().getIGPRouterID() != null) {
			IGP_type = nodeNLRI.getLocalNodeDescriptors().getIGPRouterID().getIGP_router_id_type();
			switch (IGP_type) {
			case 1:
			    ISIS_ID_str = Integer.toString(nodeNLRI.getLocalNodeDescriptors().getIGPRouterID().getISIS_ISO_NODE_ID());
				router_id=ISIS_ID_str;
			case 2:
				ISIS_ID_str = Integer.toString(nodeNLRI.getLocalNodeDescriptors().getIGPRouterID().getISIS_ISO_NODE_ID());
				router_id=ISIS_ID_str;
			case 3:
				IGPID = nodeNLRI.getLocalNodeDescriptors().getIGPRouterID().getIpv4AddressOSPF();
				if(IGPID!=null){
					router_id=IGPID.toString();
				}else{
					System.out.println("Null IGPID (type OSPF)");
				}
				break;
			default:
				log.info("añadir este tipo de IGP Identifier por implementar ");
			}
		}

		if (nodeNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV() != null) {
			if (nodeNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV().getBGPLS_ID() != null) {
				LocalNodeBGPId = nodeNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV().getBGPLS_ID();
			}
		}

		if (nodeName != null) {
			this.nodeName = nodeName;
		}else{
			this.nodeName= this.router_id;
		}
		log.info("End node processing");
	}

	public String toString() {// check type
		// TODO: concatenate with stringBuffer

		String out = "";
		if (this.router_id != null)
			out = out + "ID: " + this.router_id + " ";// esto es id router??
		if (this.iPv4RouterIDLocalNodeLATLV != null)
			out = out + this.iPv4RouterIDLocalNodeLATLV.toString();
		if (this.iPv4RouterIDNeighborNodeLATLV != null)
			out = out + "---->" + this.iPv4RouterIDNeighborNodeLATLV.toString();
		if(this.LocalNodeBGPId!=null)
			out=out+"BGP_ID: "+this.LocalNodeBGPId+" ";
		if(this.as_number!=null)
			out=out+"AS_number: "+InetAddresses.coerceToInteger(this.as_number)+" ";
		if (this.nodeName != null)
			out = out + "Name node attribute: " + nodeName + " ";
		if (this.ISIS_ID_str != null)
			out = out + "ID node: " + this.ISIS_ID_str + " ";
		if (this.as_number != null)
			out = out + "AS number: " + this.as_number.toString() + " ";
		return out;

	}

	public String getLearntFrom() {
		return learntFrom;
	}

	public void setLearntFrom(String learntFrom) {
		this.learntFrom = learntFrom;
	}

	public String getLocalBgplsID() {
		return this.localBgplsID;
	}

	public void setLocalBgplsID(String localBgplsID) {
		this.localBgplsID = localBgplsID;
	}

	public String getNodeName() {
		return nodeName;
	}

	public Inet4Address getIGPID() {
		return IGPID;
	}

	public Inet4Address getBgplsID() {
		return bgplsID;
	}

	public String getRouterID(){
		return router_id;
	}

	public void setBgplsID(Inet4Address bgplsID) {
		this.bgplsID = bgplsID;
	}

	public Inet4Address getAs_number() {
		return as_number;
	}

	@Override
	public int hashCode() {
		int result = 17;
		result = 31 * result + localBgplsID.hashCode();
		result = 31 * result + iPv4RouterIDLocalNodeLATLV.hashCode();
		result = 31 * result + iPv4RouterIDNeighborNodeLATLV.hashCode();
		return result;
	}

	@Override
	public boolean equals(Object o) {
		if (o == this)
			return true;
		if (!(o instanceof NodeNLRIMsg)) {
			return false;
		}
		NodeNLRIMsg nodeCk = (NodeNLRIMsg) o;
		return nodeCk.localBgplsID == localBgplsID && nodeCk.iPv4RouterIDLocalNodeLATLV == iPv4RouterIDLocalNodeLATLV
				&& nodeCk.localBgplsID == localBgplsID
				&& nodeCk.iPv4RouterIDLocalNodeLATLV == iPv4RouterIDLocalNodeLATLV;
	}

}
