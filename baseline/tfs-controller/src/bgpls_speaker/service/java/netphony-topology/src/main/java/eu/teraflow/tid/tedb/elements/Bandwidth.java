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

	public class Bandwidth {

		double maxBandwidth;
		double unreservedBw;

		
		public Bandwidth (double initBandwidth){
			maxBandwidth = initBandwidth;
			unreservedBw = initBandwidth;
		}
		
		
		public Bandwidth (double max, double unresv){
			maxBandwidth = max;
			unreservedBw = unresv;
		}
		
		
		public String toString(){
			return "Unreserved Bw = " + unreservedBw + ", Max Bandwidth = " + maxBandwidth;
		}
		
		/**
		 * @return the maxBandwidth
		 */
		public double getMaxBandwidth() {
			return maxBandwidth;
		}
		/**
		 * @param maxBandwidth the maxBandwidth to set
		 */
		public void setMaxBandwidth(double maxBandwidth) {
			this.maxBandwidth = maxBandwidth;
		}
		/**
		 * @return the unreservedBw
		 */
		public double getUnreservedBw() {
			return unreservedBw;
		}
		/**
		 * @param unreservedBw the unreservedBw to set
		 */
		public void setUnreservedBw(double unreservedBw) {
			this.unreservedBw = unreservedBw;
		}
	}
