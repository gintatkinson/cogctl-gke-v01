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

package eu.teraflow.tid.tedb.elements;

public class EndPoint {
	String node;
	
	String intf;

	public EndPoint(String node, String intf){
		this.node = node;
		this.intf = intf;
	}

	/**
	 * @return the node
	 */
	public String getNode() {
		return node;
	}

	/**
	 * @param node the node to set
	 */
	public void setNode(String node) {
		this.node = node;
	}

	/**
	 * @return the intf
	 */
	public String getIntf() {
		return intf;
	}

	/**
	 * @param intf the intf to set
	 */
	public void setIntf(String intf) {
		this.intf = intf;
	}
	

	public int compareTo(EndPoint arg0) {
		if ((arg0.intf.compareTo(this.intf)==0) && (arg0.node.compareTo(this.node)==0)) 
			return 0;
		else
			return 1;
	}
	@Override
	public boolean equals(Object obj) {
		if ((this.node.equals(((EndPoint)obj).getNode()))&&
				(this.intf.equals(((EndPoint)obj).getIntf())))
			return true;
		return false;
	}

	@Override
	public String toString() {
		// TODO Auto-generated method stub
		String temp="";
		temp += "Node = " + node + " - ";
		temp += "Interface = " + intf ;
		return temp;
	}
	
	
	
}
