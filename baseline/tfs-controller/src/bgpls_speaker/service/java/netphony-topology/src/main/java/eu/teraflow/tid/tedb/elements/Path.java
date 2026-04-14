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

import java.util.ArrayList;

public class Path {
	//TODO change to enumeration with values working/protection
	String pathType;
	
	ArrayList<Link> links;
	
	public String toString(){
		String temp = "";
		if (links!=null){
			for (int i=0;i<links.size();i++)
				temp +=  "\n\t\t" + links.get(i).getSource() + "-->" + links.get(i).getDest() ;
		}
		return temp;
	}
	
	public Path(ArrayList<Link> links){
		this.links = links;
	}

	/**
	 * @return the pathType
	 */
	public String getPathType() {
		return pathType;
	}

	/**
	 * @param pathType the pathType to set
	 */
	public void setPathType(String pathType) {
		this.pathType = pathType;
	}

	/**
	 * @return the links
	 */
	public ArrayList<Link> getLinks() {
		return links;
	}

	/**
	 * @param links the links to set
	 */
	public void setLinks(ArrayList<Link> links) {
		this.links = links;
	}
	
	
}
