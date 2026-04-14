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

package eu.teraflow.tid.bgp4Peer.grpc;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import com.google.common.net.InetAddresses;

import eu.teraflow.tid.bgp4Peer.models.LinkNLRIMsg;
import eu.teraflow.tid.bgp4Peer.models.NodeNLRIMsg;
import eu.teraflow.tid.bgp4Peer.models.UpdateMsg;
import eu.teraflow.tid.bgp4Peer.models.UpdateMsgList;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.stub.StreamObserver;
import jdk.javadoc.internal.doclets.toolkit.util.links.LinkInfo;
import src.main.proto.GrpcService.linkInfo;
import src.main.proto.GrpcService.nodeInfo;
import src.main.proto.GrpcService.NodeDescriptors;
import src.main.proto.GrpcService.updateRequest;
import src.main.proto.GrpcService.updateResponse;
import src.main.proto.updateServiceGrpc;
import src.main.proto.updateServiceGrpc.updateServiceBlockingStub;
import src.main.proto.updateServiceGrpc.updateServiceStub;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

public class grpcClient {

	private static final Logger logger = Logger.getLogger(grpcClient.class.getName());

	public static void sendGrpcUpdateMsg(UpdateMsg update) throws Exception{
		
		updateRequest request=null;
		nodeInfo n=null;
		linkInfo unic=null;
		List <linkInfo> l = new ArrayList<>();
		List <nodeInfo> nodes = new ArrayList<>();
		if(update.nodeCheck()==false && update.linkCheck()==false){
			return;
		}
//		Build node for grpc message
		if(update.nodeCheck()!=false) {		
			for(NodeNLRIMsg node : update.getNodeList()){
				n = nodeInfo.newBuilder().setNodeName(node.getNodeName()).
						setIgpID(node.getRouterID()).
						setBgplsID(node.getLocalBgplsID()).
						setAsID(InetAddresses.coerceToInteger(node.getAs_number())).
						setLearntFrom(node.getLearntFrom()).
					buildPartial();
				nodes.add(n);
			}
		}
		for(LinkNLRIMsg link : update.getLinkList()) {
			
//			String strIPlocal;
//			String strIPremote;
			String strIgpR;
			String strIgpL;
			// LinkNLRIMsg link=update.getLink();
		
//			if(link.getiPv4RouterIDLocalNodeLATLV()==null) 
//				 strIPlocal="-";
//			else {
//				strIPlocal=link.getiPv4RouterIDLocalNodeLATLV();
//			}
//			if(link.getiPv4RouterIDNeighborNodeLATLV()==null) 
//				 strIPremote="-";
//			else {
//				strIPremote=link.getiPv4RouterIDNeighborNodeLATLV();
//			}
			
			if(link.getRemoteNodeIGPId()==null) 
				strIgpR="-";
			else {
				strIgpR=link.getRemoteNodeIGPId().toString();
			}
			if(link.getLocalNodeIGPId()==null) 
				strIgpL="-";
			else {
				strIgpL=link.getLocalNodeIGPId().toString();
			}
			String ipv4R;
			if(link.getiPv4RouterIDLocalNodeLATLV()==null) 
				ipv4R="-";
			else {
				ipv4R=link.getiPv4RouterIDLocalNodeLATLV();
			}
			String ipv4L;
			if(link.getiPv4RouterIDNeighborNodeLATLV()==null) 
				ipv4L="-";
			else {
				ipv4L=link.getiPv4RouterIDNeighborNodeLATLV();
			}
					
//			Build link for grpc message. need non null values in some cases
			
			unic = linkInfo.newBuilder().setLocalID(strIgpR).
					setLocalIPv4ID(ipv4L).
					setRemoteID(strIgpL).
					setRemoteIPv4ID(ipv4R).
					setLocal(NodeDescriptors.newBuilder().
							setAsNumber(link.getLocalDomainID().toString()).
							setBgplsID(link.getLocalBgplsID())).
					setRemote(NodeDescriptors.newBuilder().
							setAsNumber(link.getRemoteDomainID().toString()).
							setBgplsID(link.getRemoteBgplsID())).
					setAvailableBw(link.getAvailableBw()).
					setResidualBw(link.getResidualBw()).setUtilized(link.getUtilizedBw()).
					setMinLinkDelay(link.getMinDelay()).setMaxLinkDelay(link.getMaxDelay()).
					setDelayVariation(link.getLinkDelayVar()).setDelay(link.getLinkDelay()).
					setTEDefaultMetric(1).setAdjacencySid("0").setLearntFrom(link.getLearntFrom()).buildPartial();
			
			l.add(unic);
		} 
		
		if(nodes.size()==0 && l.size()>0) {
			request=updateRequest.newBuilder().
					setNextHop(update.getNextHop().toString()).
					setAddressFamilyID(Integer.toString(update.getAFI())).
					setAsPathSegment(Integer.toString(update.getAsPathSegment())).
					addAllLink(l).build();
		}else if(nodes.size()>0&& l.size()==0) {
			// logger.debug("ADDING NODE");
			request=updateRequest.newBuilder().
					setNextHop(update.getNextHop().toString()).
					setAddressFamilyID(Integer.toString(update.getAFI())).
					setAsPathSegment(Integer.toString(update.getAsPathSegment())).
					addAllNode(nodes).build();
		}else {
			//Error if node name is null 
			// TODO: handle seng grpc error?
			// logger.debug("ADDING NODE AND LINK");
			request=updateRequest.newBuilder().
					setNextHop("-"+update.getNextHop().toString()).
					setAddressFamilyID(Integer.toString(update.getAFI())).
					setAsPathSegment(Integer.toString(update.getAsPathSegment())).
					addAllNode(nodes).addAllLink(l).build();
			
		}
		final ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost",2021).usePlaintext().build();
		updateServiceBlockingStub stub = updateServiceGrpc.newBlockingStub(channel);

		//TODO: this to a function
		System.out.println("grpcClient request: "+request.toString());

		// channel.awaitTermination(20, TimeUnit.SECONDS);
		// updateResponse response = stub.update(request);
		// Espera hasta que el canal esté inactivo
        updateResponse response = stub.update(request);	

		System.out.println("\nRESPUESTA RECIBIDA");
		System.out.println(response);
	}
	// private void shutdownManagedChannel(ManagedChannel managedChannel) {
	// 	managedChannel.shutdown();
	// 	try {
	// 	managedChannel.awaitTermination(mChannelShutdownTimeoutMs, TimeUnit.MILLISECONDS);
	// 	} catch (InterruptedException e) {
	// 	Thread.currentThread().interrupt();
	// 	// Allow thread to exit.
	// 	} finally {
	// 	managedChannel.shutdownNow();
	// 	}
	// 	Verify.verify(managedChannel.isShutdown());
	// }
	// stub.update(request, new StreamObserver <updateResponse>() {
      		
	// 	public void onNext(updateResponse response) {
	// 	  System.out.println("respuesta del server: "+response);
	// 	}
	// 	public void onError(Throwable t) {
	// 		System.out.println("error: "+t.getMessage());
	// 		latch.countDown();
	// 	}
	// 	public void onCompleted() {
	// 	  // Typically you'll shutdown the channel somewhere else.
	// 	  // But for the purpose of the lab, we are only making a single
	// 	  // request. We'll shutdown as soon as this request is done.
	// 		  latch.countDown();
	// 		logger.info("gRPC call completed");
	// 		System.out.println("OnCompleted");
	// 	//   channel.shutdownNow();
	// 		// try{
	// 		// 	channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
	// 		// }catch (InterruptedException e){
	// 		// 	System.out.println("channel error"+e.toString());
	// 		// }
			
	// 	}
	//   });
	//   latch.await(5, TimeUnit.SECONDS);
	//   channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);

	public static void sendGrpc(UpdateMsgList update) {
		//construir mensaje
		//update get node,lin,path
		//getname,ids,as
		final ManagedChannel channel = ManagedChannelBuilder.forTarget("localhost:2021").usePlaintext().build();
		updateServiceStub stub = updateServiceGrpc.newStub(channel);
		
		
		if(update.getNodeList().isEmpty()&&update.getLinkList().isEmpty()) {
			return;
		}
		updateRequest request=null;
		nodeInfo n=null;
		linkInfo l=null;
		if(!update.getNodeList().isEmpty()) {
			
			for(NodeNLRIMsg node: update.getNodeList()) {
				
				n = nodeInfo.newBuilder().setNodeName(node.getNodeName()).setIgpID(node.getLocalBgplsID()).
						setBgplsID(node.getBgplsID().toString()).setAsID(InetAddresses.coerceToInteger(node.getAs_number())).
					buildPartial();
			} 
			
			
		}
		if(!update.getLinkList().isEmpty()) {
			
			String strIPlocal;
			String strIPremote;
			String strIgpR;
			String strIgpL;
			
			for(LinkNLRIMsg link: update.getLinkList()) {
				
				if(link.getiPv4RouterIDLocalNodeLATLV()==null) 
					 strIPlocal="-";
				else {
					strIPlocal=link.getiPv4RouterIDLocalNodeLATLV();
				}
				if(link.getiPv4RouterIDNeighborNodeLATLV()==null) 
					 strIPremote="-";
				else {
					strIPremote=link.getiPv4RouterIDNeighborNodeLATLV();
				}
				
				if(link.getRemoteNodeIGPId()==null) 
					strIgpR="-";
				else {
					strIgpR=link.getRemoteNodeIGPId().toString();
				}
				if(link.getLocalNodeIGPId()==null) 
					strIgpL="-";
				else {
					strIgpL=link.getLocalNodeIGPId().toString();
				}
				String ipv4R;
				if(link.getiPv4RouterIDNeighborNodeLATLV()==null) 
					ipv4R="-";
				else {
					ipv4R=link.getiPv4RouterIDNeighborNodeLATLV();
				}
				String ipv4L;
				if(link.getiPv4RouterIDLocalNodeLATLV()==null) 
					ipv4L="-";
				else {
					ipv4L=link.getiPv4RouterIDLocalNodeLATLV();
				}
				
//				NodeDescriptors local= NodeDescriptors.newBuilder().
//						setAsNumber(link.getLocalDomainID().toString()).
//						setBgplsID(link.getLocalBgplsID()).buildPartial();
						
				
				l = linkInfo.newBuilder().setLocalID(strIgpR).
						setLocalIPv4ID(ipv4L).
						setRemoteID(strIgpL).
						setRemoteIPv4ID(ipv4R).
						setLocal(NodeDescriptors.newBuilder().
								setAsNumber(link.getLocalDomainID().toString()).
								setBgplsID(link.getLocalBgplsID())).
						setRemote(NodeDescriptors.newBuilder().
								setAsNumber(link.getRemoteDomainID().toString()).
								setBgplsID(link.getRemoteBgplsID())).
						setAvailableBw(link.getAvailableBw()).
						setResidualBw(link.getResidualBw()).setUtilized(link.getUtilizedBw()).
						setMinLinkDelay(link.getMinDelay()).setMaxLinkDelay(link.getMaxDelay()).
						setDelayVariation(link.getLinkDelayVar()).setDelay(link.getLinkDelay()).
						setTEDefaultMetric(1).setAdjacencySid("0").buildPartial();
			} 
			
		}
		if(n==null) {
			request = updateRequest.newBuilder().addLink(l).build();
		}else if(l==null) {
			request = updateRequest.newBuilder().addNode(n).build();
		}else {
			request = updateRequest.newBuilder().addNode(n).addLink(l).build();
		}
		
		
		
		
	    
	    stub.update(request, new StreamObserver <updateResponse>() {
      		
	        public void onNext(updateResponse response) {
	          System.out.println("respuesta del server: "+response);
	        }
	        public void onError(Throwable t) {
	        	System.out.println("error: "+t.getMessage());
	        }
	        public void onCompleted() {
	          // Typically you'll shutdown the channel somewhere else.
	          // But for the purpose of the lab, we are only making a single
	          // request. We'll shutdown as soon as this request is done.
	        	System.out.println("channel shutdown");
	          channel.shutdownNow();
	        }
	      });
	    
	    
	    
		
		
	}
	public static void main( String[] args ) throws Exception
    {
	      final ManagedChannel channel = ManagedChannelBuilder.forTarget("localhost:2021").usePlaintext().build();

	    	      // Replace the previous synchronous code with asynchronous code.
	    	      // This time use an async stub:
	    	       updateServiceStub stub = updateServiceGrpc.newStub(channel);

	    	      // Construct a request
	    	       int a = 123;
	    	       nodeInfo n = nodeInfo.newBuilder().setNodeName("router 3").setIgpID("1341234").buildPartial();
	    	      updateRequest request =
	    	        updateRequest.newBuilder().addNode(n).build();

	    	      // Make an Asynchronous call. Listen to responses w/ StreamObserver
	    	      	stub.update(request, new StreamObserver <updateResponse>() {
	    	      		
	    	        public void onNext(updateResponse response) {
	    	          System.out.println("respuesta del server: "+response);
	    	        }
	    	        public void onError(Throwable t) {
	    	        	System.out.println("error: "+t.getMessage());
	    	        }
	    	        public void onCompleted() {
	    	          // Typically you'll shutdown the channel somewhere else.
	    	          // But for the purpose of the lab, we are only making a single
	    	          // request. We'll shutdown as soon as this request is done.
	    	        	System.out.println("channel shutdown");
	    	          channel.shutdownNow();
	    	        }
	    	      });
	    	    }
}
