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

import es.tid.of.DataPathID;

public class EdgeUtils {
	
	public static Object getEdge(String edge){
		Object router_id_addr;
		try { //Router_type: IPv4
			router_id_addr = (Inet4Address) Inet4Address.getByName(edge);
		} catch (Exception e) { //Router_type: DatapathID
			router_id_addr =  (DataPathID) DataPathID.getByName(edge);
			//FIXME: See what to do if it is not IPv4 or DatapahID
		}
		return router_id_addr;
	}

}
