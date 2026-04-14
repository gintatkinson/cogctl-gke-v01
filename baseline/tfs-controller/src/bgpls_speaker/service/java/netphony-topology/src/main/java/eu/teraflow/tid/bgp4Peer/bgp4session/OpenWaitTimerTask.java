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

import java.util.TimerTask;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;



/**
 * If no Open message is received before the expiration of the OpenWait
   timer, the PCEP peer sends a PCErr message with Error-Type=1 and
   Error-value=2, the system releases the PCEP resources for the PCEP
   peer, closes the TCP connection, and moves to the Idle state.

 * @author Oscar Gonzalez de Dios
 *
 */
public class OpenWaitTimerTask extends TimerTask {

//	private DataOutputStream out=null; //Use this to send messages to peer
	private BGP4Session bgp4Session;
	private Logger log;
	
	public OpenWaitTimerTask(BGP4Session bgp4Session){
		this.bgp4Session=bgp4Session;
		log=LoggerFactory.getLogger("PCEServer");
	}
		
	
	public void run() {
		log.warn("OPEN WAIT Timer OVER");
//		PCEPError perror=new PCEPError();
//		PCEPErrorObject perrorObject=new PCEPErrorObject();
//		perrorObject.setErrorType(ObjectParameters.ERROR_ESTABLISHMENT);
//		perrorObject.setErrorValue(ObjectParameters.ERROR_ESTABLISHMENT_NO_OPEN_MESSAGE);
//		ErrorConstruct error_c=new ErrorConstruct();
//		error_c.getErrorObjList().add(perrorObject);
//		perror.setError(error_c);
//		log.info("Sending Error");
//		bgp4Session.sendPCEPMessage(perror);
		this.bgp4Session.killSession();
		return;
	}

}
