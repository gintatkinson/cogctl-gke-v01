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

package eu.teraflow.tid.bgp4Peer.updateTEDB;

import java.net.Inet4Address;
import java.util.Hashtable;
import java.util.concurrent.LinkedBlockingQueue;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import es.tid.bgp.bgp4.messages.BGP4Update;
import eu.teraflow.tid.bgp4Peer.tedb.IntraTEDBS;
import eu.teraflow.tid.tedb.DomainTEDB;
import eu.teraflow.tid.tedb.MultiDomainTEDB;
import eu.teraflow.tid.tedb.SimpleTEDB;
import eu.teraflow.tid.tedb.TEDB;


/**
 * This class is in charge of storing the BGP4 update messages in a queue to be processing 
 * 
 * @author pac
 *
 */
public class UpdateDispatcher {
	
	private Logger log;
	private LinkedBlockingQueue<BGP4Update> updateList;
	private UpdateProccesorThread upt;

	
	public UpdateDispatcher(MultiDomainTEDB multiTedb,Hashtable<String,TEDB> intraTEDBs ){
		this.updateList=new LinkedBlockingQueue<BGP4Update>();
		this.upt=new UpdateProccesorThread(updateList, multiTedb,intraTEDBs );		
		upt.start();
		log=LoggerFactory.getLogger("BGP4Server");
	}
	public void dispatchRequests(BGP4Update updateMessage){
		updateList.add(updateMessage);
	}



}
