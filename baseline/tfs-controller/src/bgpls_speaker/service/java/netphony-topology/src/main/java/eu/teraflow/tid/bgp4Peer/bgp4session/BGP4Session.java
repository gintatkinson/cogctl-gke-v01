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

import es.tid.bgp.bgp4.messages.BGP4Message;


/**
 * BGP Session Interface
 * 
 * @author mcs
 *
 */
public interface BGP4Session {
	/**
	 * Send close message and finish the BGP Session
	 */
	public void close(/*int reason*/);
	/**
	 * Finish the BGP Session abruptly, 
	 */
	public void killSession();
	
	/**
	 * Encodes and sends BGP Message
	 * If the message is bad encoded, the session is closed
	 * @param message BGP4 Message
	 */
	public void sendBGP4Message(BGP4Message message);


}
