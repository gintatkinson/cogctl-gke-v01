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

import java.util.LinkedList;
import eu.teraflow.tid.tedb.InterDomainEdge;
import eu.teraflow.tid.tedb.TEDB;

public class BGP4DomainTEDB implements TEDB {

	@Override
	public void initializeFromFile(String file) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void initializeFromFile(String file, String learnFrom) {
		
	}

	@Override
	public boolean isITtedb() {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public String printTopology() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public LinkedList<InterDomainEdge> getInterDomainLinks() {
		// TODO Auto-generated method stub
		return null;
	}
}
