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

package eu.teraflow.tid.bgp4Peer.bgp4session;
/**
 * The state session attribute indicates the current state of the BGP
   FSM
 * @author mcs
 *
 */
public class BGP4StateSession {
	public static final int BGP4_STATE_IDLE=0;	
	public static final int BGP4_STATE_TCP_PENDING=1;
	public static final int BGP4_STATE_OPEN_WAIT=2;
	public static final int BGP4_STATE_KEEP_WAIT=3;
	public static final int BGP4_STATE_SESSION_UP=4;
}
