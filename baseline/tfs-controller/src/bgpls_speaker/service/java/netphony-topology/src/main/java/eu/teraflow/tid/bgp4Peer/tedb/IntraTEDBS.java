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

package eu.teraflow.tid.bgp4Peer.tedb;

import java.net.Inet4Address;
import eu.teraflow.tid.tedb.TEDB;

public interface IntraTEDBS extends TEDB {

	
	//Metodo (annadir enlace intradominio) que le pases un domain id, + cosas que necesites para el intradomain edge.
	//Las clases que implemente para esta interface ya tengra que ver c�mo hacerlo. Tener una hashtable. 
	public void addIntradomainEdge();
	public void addIntradomainNode(Inet4Address domain, Inet4Address node);
	
	
}
