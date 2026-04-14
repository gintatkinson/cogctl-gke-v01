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

public class Location {
	double xCoord;
	double yCoord;

	/**Constructor to set the location 
	 * 
	 * @param x X coordinate of the location
	 * @param y Y coordinate of the location
	 */
	public Location (double x, double y){
		xCoord=x;
		yCoord=y;
	}
	
	/**
	 * @return the xCoord
	 */
	public double getxCoord() {
		return xCoord;
	}
	/**
	 * @param xCoord the xCoord to set
	 */
	public void setxCoord(double xCoord) {
		this.xCoord = xCoord;
	}
	/**
	 * @return the yCoord
	 */
	public double getyCoord() {
		return yCoord;
	}
	/**
	 * @param yCoord the yCoord to set
	 */
	public void setyCoord(double yCoord) {
		this.yCoord = yCoord;
	}

	
}
