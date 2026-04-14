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

public class Service {
	
	//TODO change to enumeration with possible values active/potential
	String status;
	
	//TODO change to enumeration with possible services like Ethernet/OTN etc. (or based on the layering available in interfaces
	String serviceType;
	
	Bandwidth bw;
	
	//Change to Enumeration based on protection types
	String protection;
	
	EndPoint source;
	
	EndPoint dest;
	
	Path servicePath;
	
	ArrayList<Integer> srlg;
	
	String baseEncapsulation;

	/**
	 * @return the status
	 */
	public String getStatus() {
		return status;
	}

	public String toString(){
		String temp = "";
		temp += "\n\t ServiceType = " + serviceType;
		temp += "\n\t Status = " + status;
		temp += "\n\t Protection = " + protection;
		temp += "\n\t Path = " + servicePath;
		temp += "\n\t Bandwidth = " + bw;
		return temp;
	}
	
	/**
	 * @param status the status to set
	 */
	public void setStatus(String status) {
		this.status = status;
	}

	/**
	 * @return the serviceType
	 */
	public String getServiceType() {
		return serviceType;
	}

	/**
	 * @param serviceType the serviceType to set
	 */
	public void setServiceType(String serviceType) {
		this.serviceType = serviceType;
	}

	/**
	 * @return the bw
	 */
	public Bandwidth getBw() {
		return bw;
	}

	/**
	 * @param bw the bw to set
	 */
	public void setBw(Bandwidth bw) {
		this.bw = bw;
	}

	/**
	 * @return the protection
	 */
	public String getProtection() {
		return protection;
	}

	/**
	 * @param protection the protection to set
	 */
	public void setProtection(String protection) {
		this.protection = protection;
	}

	/**
	 * @return the source
	 */
	public EndPoint getSource() {
		return source;
	}

	/**
	 * @param source the source to set
	 */
	public void setSource(EndPoint source) {
		this.source = source;
	}

	/**
	 * @return the dest
	 */
	public EndPoint getDest() {
		return dest;
	}

	/**
	 * @param dest the dest to set
	 */
	public void setDest(EndPoint dest) {
		this.dest = dest;
	}

	/**
	 * @return the servicePath
	 */
	public Path getServicePath() {
		return servicePath;
	}

	/**
	 * @param servicePath the servicePath to set
	 */
	public void setServicePath(Path servicePath) {
		this.servicePath = servicePath;
	}

	/**
	 * @return the srlg
	 */
	public ArrayList<Integer> getSrlg() {
		return srlg;
	}

	/**
	 * @param srlg the srlg to set
	 */
	public void setSrlg(ArrayList<Integer> srlg) {
		this.srlg = srlg;
	}

	/**
	 * @return the baseEncapsulation
	 */
	public String getBaseEncapsulation() {
		return baseEncapsulation;
	}

	/**
	 * @param baseEncapsulation the baseEncapsulation to set
	 */
	public void setBaseEncapsulation(String baseEncapsulation) {
		this.baseEncapsulation = baseEncapsulation;
	}
}
