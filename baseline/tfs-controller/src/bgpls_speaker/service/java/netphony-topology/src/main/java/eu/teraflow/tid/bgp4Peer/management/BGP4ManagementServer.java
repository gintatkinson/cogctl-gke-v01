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

package eu.teraflow.tid.bgp4Peer.management;

import eu.teraflow.tid.bgp4Peer.bgp4session.BGP4SessionsInformation;
import eu.teraflow.tid.bgp4Peer.peer.SendTopology;
import eu.teraflow.tid.tedb.MultiDomainTEDB;
import eu.teraflow.tid.tedb.TEDB;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.ServerSocket;
import java.util.Hashtable;
/**
 * To manage the server 
 * 
 * @author mcs
 *
 */
public class BGP4ManagementServer extends Thread {
	private Logger log;
	private int BGP4ManagementPort = 8888;
	private BGP4SessionsInformation bgp4SessionsInformation;
	/**
	 * Topology database for interDomain Links.
	 */
	private MultiDomainTEDB multiTEDB;
	/**
	 * Topology database for intradomain Links. It owns several domains.
	 */
	private Hashtable<String,TEDB> intraTEDBs;

	/**
	 * Class to send the topology. It is needes to set the parameters sendTopology to true or false.
	 */
	private SendTopology sendTopology;
	
	public BGP4ManagementServer(int BGP4ManagementPort, MultiDomainTEDB multiTEDB, Hashtable<String,TEDB> intraTEDBs, BGP4SessionsInformation bgp4SessionsInformation, SendTopology sendTopology){
		log =LoggerFactory.getLogger("BGP4Server");
		this.BGP4ManagementPort = BGP4ManagementPort;
		this.multiTEDB=multiTEDB;
		this.intraTEDBs=intraTEDBs;
		this.bgp4SessionsInformation =bgp4SessionsInformation;
		this.sendTopology=sendTopology;

	}
	/**
	 * RUN
	 */
	public void run(){
	    ServerSocket serverSocket = null;
	    boolean listening=true;
		try {
	      	  log.debug("Listening management on port "+BGP4ManagementPort);
	          serverSocket = new ServerSocket(BGP4ManagementPort);
		  }
		catch (Exception e){
			 log.error("Could not listen management on port "+BGP4ManagementPort);
			e.printStackTrace();
			return;
		}
		
		   try {
	        	while (listening) {
	        		new BGP4ManagementSession(serverSocket.accept(),multiTEDB,intraTEDBs,bgp4SessionsInformation, sendTopology).start();
	        	}
	        	serverSocket.close();
	        } catch (Exception e) {
	        	e.printStackTrace();
	        }				
	}
}
