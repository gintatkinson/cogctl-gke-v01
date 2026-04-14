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

public class Layer {

	/**
	 * True if it is a GMPLS layer
	 * False if it is an IP/MPLS layer (by default, false)
	 */
	public boolean gmpls=false;
	
	/**
	 * 
	 */
	public int encodingType;
	
	/**
	 * 
	 */
	public int switchingType;	
	
	public static final int SWITCHING_TYPE_WSON=150;

}
