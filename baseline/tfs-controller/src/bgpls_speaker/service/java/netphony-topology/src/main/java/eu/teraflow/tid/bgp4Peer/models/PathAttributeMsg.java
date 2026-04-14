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
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

import es.tid.bgp.bgp4.update.fields.pathAttributes.LinkStateAttribute;
import es.tid.bgp.bgp4.update.tlv.BGP4TLVFormat;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.IPv4RouterIDLocalNodeLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.NodeNameNodeAttribTLV;

public class PathAttributeMsg {

	
	private NodeNameNodeAttribTLV nodeNameTLV;
	private byte[] data;
	private String nodeName;
	private Inet4Address addrLocal;
	

	public PathAttributeMsg(LinkStateAttribute att) {
		
		
		if(att.getNodeNameTLV()!=null) {

			nodeNameTLV=att.getNodeNameTLV();
			data=nodeNameTLV.getTlv_bytes();
			int b = nodeNameTLV.getTotalTLVLength();
			int c = nodeNameTLV.getTLVValueLength();
			byte [] fin= Arrays.copyOfRange(data, b - c, b); 
			nodeName = new String(fin , StandardCharsets.UTF_8);
		}
		if(att.getIPv4RouterIDLocalNodeLATLV()!=null) {
			addrLocal=att.getIPv4RouterIDLocalNodeLATLV().getIpv4Address();
		}
		
	}
	public String toString() {
		String out="";
		if(this.nodeName!=null)
			out=out+"NODE name "+nodeName;
		if(this.addrLocal!=null)
			out=out+"NODE IP "+addrLocal.toString();
		
		return out;
	}
	
	public String getNodeName() {
		return nodeName;
	}
	public void setNodeName(String nodeName) {
		this.nodeName = nodeName;
	}
	
	@Override
    public int hashCode() {
        int result = 17;
        result = 31 * result + nodeName.hashCode();
        return result;
    }
	 @Override
	    public boolean equals(Object o) {
	        if (o == this) return true;
	        if (!(o instanceof PathAttributeMsg)) {
	            return false;
	        }
	        PathAttributeMsg pathCk = (PathAttributeMsg) o;
	        return pathCk.nodeName == nodeName;
	    }
	public Inet4Address getAddrLocal() {
		return addrLocal;
	}
	 
	
}
