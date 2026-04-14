
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
import java.util.ArrayList;

import org.slf4j.Logger;

import es.tid.bgp.bgp4.update.fields.LinkNLRI;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.NodeDescriptorsSubTLV;

public class LinkNLRIMsg {

	private ArrayList<NodeDescriptorsSubTLV> nodeDescriptorsSubTLV;
	// Dominios
	private Inet4Address localDomainID;
	private Inet4Address remoteDomainID;

	private Inet4Address areaID;
	private Inet4Address bgplsID;

	private Inet4Address LocalNodeIGPId;
	private Inet4Address RemoteNodeIGPId;

	private int linkDelay;
	private int linkDelayVar;
	private int minDelay;
	private int maxDelay;
	private int linkLoss;
	private int residualBw;
	private int availableBw;
	private int utilizedBw;
	
	private Inet4Address iPv4RouterIDLocalNodeLATLV;
	private Inet4Address iPv4RouterIDNeighborNodeLATLV;

	private int IGP_type;
	private String localIGPID = null;
	private String remoteIGPID = null;
	private String localBgplsID;
	private String remoteBgplsID;
	private Logger log;
	private String learntFrom;

	public LinkNLRIMsg(LinkNLRI linkNLRI, String learntFrom) {

		// LinkState vs Link??
		this.learntFrom = learntFrom;

		if (linkNLRI.getLocalNodeDescriptors().getAutonomousSystemSubTLV() != null) {
			localDomainID = linkNLRI.getLocalNodeDescriptors().getAutonomousSystemSubTLV().getAS_ID();
		}
		if (linkNLRI.getLocalNodeDescriptors().getAreaID() != null) {
			areaID = linkNLRI.getLocalNodeDescriptors().getAreaID().getAREA_ID();
		}
		if (linkNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV() != null) {
			bgplsID = linkNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV().getBGPLS_ID();
		}
		if (linkNLRI.getLocalNodeDescriptors().getIGPRouterID() != null) {
			LocalNodeIGPId = linkNLRI.getLocalNodeDescriptors().getIGPRouterID().getIpv4AddressOSPF();
		}

		if (linkNLRI.getRemoteNodeDescriptorsTLV().getAutonomousSystemSubTLV() != null) {
			remoteDomainID = linkNLRI.getRemoteNodeDescriptorsTLV().getAutonomousSystemSubTLV().getAS_ID();
		}
		if (linkNLRI.getRemoteNodeDescriptorsTLV().getAreaID() != null) {
			areaID = linkNLRI.getRemoteNodeDescriptorsTLV().getAreaID().getAREA_ID();
		}
		if (linkNLRI.getRemoteNodeDescriptorsTLV().getBGPLSIDSubTLV() != null) {
			bgplsID = linkNLRI.getRemoteNodeDescriptorsTLV().getBGPLSIDSubTLV().getBGPLS_ID();
		}
		if (linkNLRI.getRemoteNodeDescriptorsTLV().getIGPRouterID() != null) {
			RemoteNodeIGPId = linkNLRI.getRemoteNodeDescriptorsTLV().getIGPRouterID().getIpv4AddressOSPF();
		}
		if (linkNLRI.getUndirectionalLinkDelayTLV() != null) {
			linkDelay = linkNLRI.getUndirectionalLinkDelayTLV().getDelay();
		}
		if (linkNLRI.getUndirectionalDelayVariationTLV() != null) {
			linkDelayVar = linkNLRI.getUndirectionalDelayVariationTLV().getDelayVar();
		}
		if (linkNLRI.getMinMaxUndirectionalLinkDelayTLV() != null) {
			maxDelay = linkNLRI.getMinMaxUndirectionalLinkDelayTLV().getHighDelay();
			minDelay = linkNLRI.getMinMaxUndirectionalLinkDelayTLV().getLowDelay();
		}
		if (linkNLRI.getUndirectionalLinkLossTLV() != null) {
			linkLoss = linkNLRI.getUndirectionalLinkLossTLV().getLinkLoss();
		}
		if (linkNLRI.getUndirectionalResidualBwTLV() != null) {
			residualBw = linkNLRI.getUndirectionalResidualBwTLV().getResidualBw();
		}
		if (linkNLRI.getUndirectionalAvailableBwTLV() != null) {
			availableBw = linkNLRI.getUndirectionalAvailableBwTLV().getAvailableBw();
		}
		if (linkNLRI.getUndirectionalUtilizedBwTLV() != null) {
			utilizedBw = linkNLRI.getUndirectionalUtilizedBwTLV().getUtilizedBw();
		}
		if (linkNLRI.getIpv4InterfaceAddressTLV() != null) {
			iPv4RouterIDLocalNodeLATLV = linkNLRI.getIpv4InterfaceAddressTLV().getIpv4Address();
		}
		if (linkNLRI.getIpv4NeighborAddressTLV() != null) {
			iPv4RouterIDNeighborNodeLATLV = linkNLRI.getIpv4NeighborAddressTLV().getIpv4Address();
		}
		if (linkNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV().getBGPLS_ID() != null) {// alguna condicion?
			localBgplsID = linkNLRI.getLocalNodeDescriptors().getBGPLSIDSubTLV().getBGPLS_ID().toString();
		}
		if (linkNLRI.getRemoteNodeDescriptorsTLV().getBGPLSIDSubTLV().getBGPLS_ID() != null) {// alguna condicion?
			remoteBgplsID = linkNLRI.getRemoteNodeDescriptorsTLV().getBGPLSIDSubTLV().getBGPLS_ID().toString();
		}
		if (linkNLRI.getLocalNodeDescriptors().getIGPRouterID() != null) {
			IGP_type = linkNLRI.getLocalNodeDescriptors().getIGPRouterID().getIGP_router_id_type();
			switch (IGP_type) {
			case 1:
				localIGPID = Integer.toString(linkNLRI.getLocalNodeDescriptors().getIGPRouterID().getISIS_ISO_NODE_ID());
				break;
			case 2:
				localIGPID = Integer.toString(linkNLRI.getLocalNodeDescriptors().getIGPRouterID().getISIS_ISO_NODE_ID());
				break;
			case 3:
				localIGPID = linkNLRI.getLocalNodeDescriptors().getIGPRouterID().getIpv4AddressOSPF().toString();

				break;
			default:
				log.info("añadir este tipo de IGP Identifier por implementar ");
			}
		}
		if (linkNLRI.getRemoteNodeDescriptorsTLV().getIGPRouterID() != null) {
			IGP_type = linkNLRI.getRemoteNodeDescriptorsTLV().getIGPRouterID().getIGP_router_id_type();
			switch (IGP_type) {
			case 1:
				remoteBgplsID = Integer.toString(linkNLRI.getRemoteNodeDescriptorsTLV().getIGPRouterID().getISIS_ISO_NODE_ID());
				break;
			case 2:
				remoteBgplsID = Integer.toString(linkNLRI.getRemoteNodeDescriptorsTLV().getIGPRouterID().getISIS_ISO_NODE_ID());
			case 3:
				remoteIGPID = linkNLRI.getRemoteNodeDescriptorsTLV().getIGPRouterID().getIpv4AddressOSPF().toString();
				break;
			default:
				log.info("añadir este tipo de IGP Identifier por implementar ");
			}
		}

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
		if (!(o instanceof LinkNLRIMsg)) {
			return false;
		}
		LinkNLRIMsg linkCk = (LinkNLRIMsg) o;
		return linkCk.localBgplsID == localBgplsID && linkCk.iPv4RouterIDLocalNodeLATLV == iPv4RouterIDLocalNodeLATLV
				&& linkCk.localBgplsID == localBgplsID
				&& linkCk.iPv4RouterIDLocalNodeLATLV == iPv4RouterIDLocalNodeLATLV;
	}

	public String toString() {// check type
		String out = "";
		if (this.localBgplsID != null)
			out = out + "ID: " + this.localBgplsID + " ";// esto es id router??
		if (this.iPv4RouterIDLocalNodeLATLV != null)
			out = out + this.iPv4RouterIDLocalNodeLATLV.toString();
		if(this.localIGPID!=null)
			out = out + " localIGPID: "+ this.localIGPID;
		if (this.iPv4RouterIDNeighborNodeLATLV != null)
			out = out + "---->" + this.iPv4RouterIDNeighborNodeLATLV.toString();
		if(this.remoteIGPID!=null)
			out = out + " remoteIGPID: "+ this.remoteIGPID;
		if (this.remoteBgplsID != null)
			out = out + "ID: " + this.remoteBgplsID + " ";
		if (this.localDomainID != null)
			out = out + "\n AS_ID local: " + this.localDomainID.toString() + " ";
		if (this.remoteDomainID != null)
			out = out + "\n AS_ID remote: " + this.remoteDomainID.toString() + " ";
		if (this.availableBw != 0)
			out = out + "\n availableBW: " + this.availableBw + " ";
		if (this.residualBw != 0)
			out = out + "\n residualBw: " + this.residualBw + " ";
		if (this.linkDelay != 0)
			out = out + "\n linkDelay: " + this.linkDelay + " ";
		return out;

	}

	public String getLearntFrom() {
		return learntFrom;
	}

	public void setLearntFrom(String learntFrom) {
		this.learntFrom = learntFrom;
	}

	public String getiPv4RouterIDLocalNodeLATLV() {
		if (iPv4RouterIDLocalNodeLATLV != null)
			return iPv4RouterIDLocalNodeLATLV.toString();
		else
			return null;// NO DEBERIA SER NULL
	}

	public void setiPv4RouterIDLocalNodeLATLV(Inet4Address iPv4RouterIDLocalNodeLATLV) {
		this.iPv4RouterIDLocalNodeLATLV = iPv4RouterIDLocalNodeLATLV;
	}

	public String getiPv4RouterIDNeighborNodeLATLV() {
		if (iPv4RouterIDNeighborNodeLATLV != null)
			return iPv4RouterIDNeighborNodeLATLV.toString();
		else
			return null;// NO DEBERIA SER NULL
	}

	public void setiPv4RouterIDNeighborNodeLATLV(Inet4Address iPv4RouterIDNeighborNodeLATLV) {
		this.iPv4RouterIDNeighborNodeLATLV = iPv4RouterIDNeighborNodeLATLV;
	}

	public Inet4Address getLocalDomainID() {
		return localDomainID;
	}

	public Inet4Address getRemoteDomainID() {
		return remoteDomainID;
	}

	public String getLocalBgplsID() {
		return this.localBgplsID;
	}

	public void setLocalBgplsID(String localBgplsID) {
		this.localBgplsID = localBgplsID;
	}

	public String getRemoteBgplsID() {
		return this.remoteBgplsID;
	}

	public void setRemoteBgplsID(String remoteBgplsID) {
		this.remoteBgplsID = remoteBgplsID;
	}

	public Inet4Address getLocalNodeIGPId() {
		return LocalNodeIGPId;
	}

	public Inet4Address getRemoteNodeIGPId() {
		return RemoteNodeIGPId;
	}

	public int getLinkDelay() {
		return linkDelay;
	}

	public int getLinkDelayVar() {
		return linkDelayVar;
	}

	public int getMinDelay() {
		return minDelay;
	}

	public int getMaxDelay() {
		return maxDelay;
	}

	public int getResidualBw() {
		return residualBw;
	}

	public int getAvailableBw() {
		return availableBw;
	}

	public int getUtilizedBw() {
		return utilizedBw;
	}

}
