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

import es.tid.ospf.ospfv2.lsa.tlv.subtlv.AvailableLabels;

/**
 * Label information in the special case of a Switched Spectrum Optical Network based on Flexgrid.
 * @author amll
 *
 */

public class SSONInformation {
	/**
	 * In case the Network is SSON, this is the list of available Labels
	 */
	private AvailableLabels commonAvailableLabels; 
	
	/**
	 * In case the Network is SSON, this is the number of wavelengths. -1 means it is not WSON.
	 */
	private int numLambdas=-1;
	/**
	 * Spectral Grid of the optical network.
	 */
	public int grid=0;
	/**
	 *  Channel Spacing
	 */
	public int cs=0;
	/**
	 * Minimum central frequency available in the spectral grid available to be assigned to a LSP.
	 */
	public int nMin=0;
	
	public int getGrid() {
		return grid;
	}

	public void setGrid(int grid) {
		this.grid = grid;
	}

	public int getCs() {
		return cs;
	}

	public void setCs(int cs) {
		this.cs = cs;
	}


	public int getnMin() {
		return nMin;
	}

	public void setnMin(int nMin) {
		this.nMin = nMin;
	}

	public AvailableLabels getCommonAvailableLabels() {
		return commonAvailableLabels;
	}

	public void setCommonAvailableLabels(AvailableLabels commonAvailableLabels) {
		this.commonAvailableLabels = commonAvailableLabels;
	}

	public int getNumLambdas() {
		return numLambdas;
	}

	public void setNumLambdas(int numLambdas) {
		this.numLambdas = numLambdas;
	}
}
