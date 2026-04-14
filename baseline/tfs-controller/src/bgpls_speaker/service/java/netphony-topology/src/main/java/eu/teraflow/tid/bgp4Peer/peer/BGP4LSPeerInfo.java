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

package eu.teraflow.tid.bgp4Peer.peer;

import java.net.Inet4Address;

public class BGP4LSPeerInfo {
	/**
	 * IP Address of the remote Peer
	 */
	private  Inet4Address peerIP;
	
	/**
	 * Experimental USE Only
	 * Default port is 179
	 * For testing and development, alternative ports are allowed.
	 */
	private int peerPort;
	
	/**
	 * If the remote peer is a consumer and we need to send the topology
	 */
	private boolean sendToPeer;
	
	/**
	 * If the remote peer is a generator of topology and we are consumers
	 */
	private boolean updateFromPeer;
	
	

	public BGP4LSPeerInfo() {
		this.peerPort=179;
	}

	public Inet4Address getPeerIP() {
		return peerIP;
	}

	public void setPeerIP(Inet4Address peerIP) {
		this.peerIP = peerIP;
	}

	public int getPeerPort() {
		return peerPort;
	}

	public void setPeerPort(int peerPort) {
		this.peerPort = peerPort;
	}

	public boolean isSendToPeer() {
		return sendToPeer;
	}

	public void setSendToPeer(boolean sendToPeer) {
		this.sendToPeer = sendToPeer;
	}

	public boolean isUpdateFromPeer() {
		return updateFromPeer;
	}

	public void setUpdateFromPeer(boolean updateFromPeer) {
		this.updateFromPeer = updateFromPeer;
	}
	
	
	
	
	

}
