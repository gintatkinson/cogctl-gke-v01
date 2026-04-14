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

public class PhyLinkParams {
 //Create parameters for Physical Link
	double transmissionDelay; 

	boolean isActive;

	public PhyLinkParams(double delay, boolean active){
		isActive = active;
		transmissionDelay = delay;
	}
	
	/**
	 * @return the transmissionDelay
	 */
	public double getTransmissionDelay() {
		return transmissionDelay;
	}

	/**
	 * @param transmissionDelay the transmissionDelay to set
	 */
	public void setTransmissionDelay(double transmissionDelay) {
		this.transmissionDelay = transmissionDelay;
	}

	/**
	 * @return the isActive
	 */
	public boolean isActive() {
		return isActive;
	}

	/**
	 * @param isActive the isActive to set
	 */
	public void setActive(boolean isActive) {
		this.isActive = isActive;
	}
}
