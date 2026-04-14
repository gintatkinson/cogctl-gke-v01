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

package eu.teraflow.tid.tedb;

import java.net.Inet4Address;

public class ReachabilityEntry {

	public Inet4Address domainId;
	public byte[] mask;
	public int prefix;

	//public byte[] aggregatedIPRange;
	public Inet4Address aggregatedIPRange;

	public ReachabilityEntry(){
		mask = new byte[4];
		
	}
	public ReachabilityEntry(Inet4Address domainId){
		mask = new byte[4];
	
	}
	
	public int getPrefix() {
		return prefix;
	}

	public Inet4Address getAggregatedIPRange() {
		return aggregatedIPRange;
	}

	public void setAggregatedIPRange(Inet4Address aggregatedIPRange) {
		this.aggregatedIPRange = aggregatedIPRange;
	}
	
	public byte[] getMask() {
		return mask;
	}


	public Inet4Address getDomainId() {
		return domainId;
	}

	public void setDomainId(Inet4Address domainId) {
		this.domainId = domainId;
	}

	public void setMask(byte[] mask) {
		this.mask = mask;
	}
	public void setPrefix(int prefix) {
		this.prefix = prefix;
	}
	public String toString(){
		String ret=aggregatedIPRange.toString()+"\\"+prefix+" ("+domainId.toString()+")";
		return ret;
	}
	
	@Override
	public boolean equals(Object reachabilityObject) {
		if ((domainId.equals(((ReachabilityEntry)reachabilityObject).getDomainId()))&&
				(aggregatedIPRange.equals(((ReachabilityEntry)reachabilityObject).getAggregatedIPRange()))&&
				(prefix == ((ReachabilityEntry)reachabilityObject).getPrefix())){
			return true;
		}
			
		return false;
	}
	

}
