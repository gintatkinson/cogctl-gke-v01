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

import java.io.IOException;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import es.tid.bgp.bgp4.messages.BGP4Update;
import es.tid.bgp.bgp4.update.fields.IPv4PrefixNLRI;
import es.tid.bgp.bgp4.update.fields.ITNodeNLRI;
import es.tid.bgp.bgp4.update.fields.LinkNLRI;
import es.tid.bgp.bgp4.update.fields.LinkStateNLRI;
import es.tid.bgp.bgp4.update.fields.NLRITypes;
import es.tid.bgp.bgp4.update.fields.NodeNLRI;
import es.tid.bgp.bgp4.update.fields.PathAttribute;
import es.tid.bgp.bgp4.update.fields.pathAttributes.AFICodes;
import es.tid.bgp.bgp4.update.fields.pathAttributes.AS_Path_Attribute;
import es.tid.bgp.bgp4.update.fields.pathAttributes.AS_Path_Segment;
import es.tid.bgp.bgp4.update.fields.pathAttributes.BGP_LS_MP_Reach_Attribute;
import es.tid.bgp.bgp4.update.fields.pathAttributes.LinkStateAttribute;
import es.tid.bgp.bgp4.update.fields.pathAttributes.MP_Reach_Attribute;
import es.tid.bgp.bgp4.update.fields.pathAttributes.PathAttributesTypeCode;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.AdministrativeGroupLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.DefaultTEMetricLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.IGPFlagBitsPrefixAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.IPv4RouterIDLocalNodeLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.IPv4RouterIDRemoteNodeLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.IS_IS_AreaIdentifierNodeAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.LinkProtectionTypeLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.MF_OTPAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.MaxReservableBandwidthLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.MaximumLinkBandwidthLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.MetricLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.NodeFlagBitsNodeAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.NodeNameNodeAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.OSPFForwardingAddressPrefixAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.PrefixMetricPrefixAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.RouteTagPrefixAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.SidLabelNodeAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.TransceiverClassAndAppAttribTLV;
import es.tid.bgp.bgp4.update.tlv.linkstate_attribute_tlvs.UnreservedBandwidthLinkAttribTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.MinMaxUndirectionalLinkDelayDescriptorSubTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.NodeDescriptorsSubTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.UndirectionalAvailableBandwidthDescriptorSubTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.UndirectionalDelayVariationDescriptorSubTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.UndirectionalLinkDelayDescriptorSubTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.UndirectionalLinkLossDescriptorSubTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.UndirectionalResidualBandwidthDescriptorSubTLV;
import es.tid.bgp.bgp4.update.tlv.node_link_prefix_descriptor_subTLVs.UndirectionalUtilizedBandwidthDescriptorSubTLV;
import es.tid.ospf.ospfv2.lsa.tlv.subtlv.AdministrativeGroup;
import es.tid.ospf.ospfv2.lsa.tlv.subtlv.AvailableLabels;
import es.tid.ospf.ospfv2.lsa.tlv.subtlv.MaximumBandwidth;
import es.tid.ospf.ospfv2.lsa.tlv.subtlv.MaximumReservableBandwidth;
import es.tid.ospf.ospfv2.lsa.tlv.subtlv.TrafficEngineeringMetric;
import es.tid.ospf.ospfv2.lsa.tlv.subtlv.UnreservedBandwidth;
import es.tid.ospf.ospfv2.lsa.tlv.subtlv.complexFields.BitmapLabelSet;
import eu.teraflow.tid.bgp4Peer.grpc.grpcClient;
import eu.teraflow.tid.bgp4Peer.json.bgpMarshal;
import eu.teraflow.tid.bgp4Peer.models.LinkNLRIMsg;
import eu.teraflow.tid.bgp4Peer.models.NodeNLRIMsg;
import eu.teraflow.tid.bgp4Peer.models.PathAttributeMsg;
import eu.teraflow.tid.bgp4Peer.models.UpdateMsg;
import eu.teraflow.tid.bgp4Peer.models.UpdateMsgList;
import eu.teraflow.tid.tedb.DomainTEDB;
import eu.teraflow.tid.tedb.IT_Resources;
import eu.teraflow.tid.tedb.InterDomainEdge;
import eu.teraflow.tid.tedb.IntraDomainEdge;
import eu.teraflow.tid.tedb.MultiDomainTEDB;
import eu.teraflow.tid.tedb.Node_Info;
import eu.teraflow.tid.tedb.SSONInformation;
import eu.teraflow.tid.tedb.SimpleTEDB;
import eu.teraflow.tid.tedb.TEDB;
import eu.teraflow.tid.tedb.TE_Information;
import eu.teraflow.tid.tedb.WSONInformation;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
/**
 * This class process the update messages updating the TEDB.
 * 
 *  WARNING: it is suppose to be a SimpleTEDB!!! It is not finished yet.
 * @author pac
 *
 */
public class UpdateProccesorThread extends Thread {
	/**
	 * Parameter to run the class if it is true
	 */
	private boolean running;
	/**
	 * Queue which stores the BGP4 update messages to be read and process
	 */
	private LinkedBlockingQueue<BGP4Update> updateList;

	/** LINK ATTRIBUTE TLVs */
	MaximumLinkBandwidthLinkAttribTLV maximumLinkBandwidthTLV;
	MaxReservableBandwidthLinkAttribTLV maxReservableBandwidthTLV;
	UnreservedBandwidthLinkAttribTLV unreservedBandwidthTLV;
	AdministrativeGroupLinkAttribTLV administrativeGroupTLV;
	LinkProtectionTypeLinkAttribTLV linkProtectionTLV;
	MetricLinkAttribTLV metricTLV;
	IPv4RouterIDLocalNodeLinkAttribTLV iPv4RouterIDLocalNodeLATLV;
	IPv4RouterIDRemoteNodeLinkAttribTLV iPv4RouterIDRemoteNodeLATLV;
	DefaultTEMetricLinkAttribTLV TEMetricTLV;	
	TransceiverClassAndAppAttribTLV transceiverClassAndAppATLV;
	MF_OTPAttribTLV mF_OTP_ATLV;
	int linkDelay;
	int linkDelayVar;
	int minDelay;
	int maxDelay;
	int linkLoss;
	int residualBw;
	int availableBw;
	int utilizedBw;
	/** NODE ATTRIBUTE TLVs 
	 * Ipv4 of local node link attribute TLV also used
	 * 
	 * */
	NodeFlagBitsNodeAttribTLV nodeFlagBitsTLV = new NodeFlagBitsNodeAttribTLV();
	NodeNameNodeAttribTLV nodeNameTLV = new NodeNameNodeAttribTLV();
	IS_IS_AreaIdentifierNodeAttribTLV areaIDTLV = new IS_IS_AreaIdentifierNodeAttribTLV();
	SidLabelNodeAttribTLV sidTLV = new SidLabelNodeAttribTLV();

	/**PREFIX ATTRIBUTE TLVs */
	IGPFlagBitsPrefixAttribTLV igpFlagBitsTLV = new IGPFlagBitsPrefixAttribTLV();
	RouteTagPrefixAttribTLV routeTagTLV = new RouteTagPrefixAttribTLV();
	PrefixMetricPrefixAttribTLV prefixMetricTLV = new PrefixMetricPrefixAttribTLV();
	OSPFForwardingAddressPrefixAttribTLV OSPFForwardingAddrTLV = new OSPFForwardingAddressPrefixAttribTLV();

	private AvailableLabels availableLabels;
	/**
	 * Logger
	 */
	private Logger log;
	/**
	 * Topology database for interDomain Links which will be updated.
	 */
	private MultiDomainTEDB multiTedb;
	/**
	 * Topology database for intradomain Links. It owns several domains and.
	 */
	private Hashtable<String,TEDB> intraTEDBs;

	private LinkedList<UpdateLink> updateLinks;

	private TE_Information te_info;




	public UpdateProccesorThread(LinkedBlockingQueue<BGP4Update> updateList,
			MultiDomainTEDB multiTedb ,Hashtable<String,TEDB> intraTEDBs ){
		log=LoggerFactory.getLogger("BGP4Server");
		running=true;
		this.updateList=updateList;
		this.multiTedb = multiTedb;

		this.intraTEDBs=intraTEDBs;
		this.availableLabels= new AvailableLabels();
		this.updateLinks=new LinkedList<UpdateLink>();
	}

	/**
	 * Starts processing updates
	 */
	public void run(){	
		
		BGP4Update updateMsg;
		UpdateMsgList updateMsgList = new UpdateMsgList();//write nodes and links info to a file
		bgpMarshal m = new bgpMarshal();//add to json file
		try {
			m.bgpMarshaller();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		int j=0; //debug coverage
		while (running && j<100) {
			try {
				clearAttributes();
				UpdateMsg update = new UpdateMsg();//class to send grpc message
				PathAttribute att_ls = null;
				PathAttribute att_mpreach  = null; 
				PathAttribute att = null;
				PathAttribute att_path = null;
				updateMsg= updateList.take();
				
				
				log.info("Update Procesor Thread Reading the message: \n"+ updateMsg.toString());
				log.info("\n \n");
				//guille update processor
				
				
				
				log.debug("END string UPDATE msg");
				//Andrea To be checked
				String learntFrom = updateMsg.getLearntFrom();
				log.info("Received from "+learntFrom);
				ArrayList<PathAttribute> pathAttributeList = updateMsg.getPathAttributes();
				ArrayList<PathAttribute> pathAttributeListUtil = new ArrayList<PathAttribute>();			
				update.setLearntFrom(learntFrom);
				
				
				
				// buscamos los dos atributos que nos interesan...
				for (int i=0;i<pathAttributeList.size();i++){
					att = pathAttributeList.get(i);
					int typeCode = att.getTypeCode();
					switch (typeCode){
					case PathAttributesTypeCode.PATH_ATTRIBUTE_TYPECODE_BGP_LS_ATTRIBUTE:
						att_ls = att;
						break;
					case PathAttributesTypeCode.PATH_ATTRIBUTE_TYPECODE_MP_REACH_NLRI:
						att_mpreach = att;
						break;
					case PathAttributesTypeCode.PATH_ATTRIBUTE_TYPECODE_ASPATH:
						//log.info("We don't use ASPATH");
						att_path=att;
						break;	
					case PathAttributesTypeCode.PATH_ATTRIBUTE_TYPECODE_ORIGIN:
						//log.info("We don't use ORIGIN");
						break;	
					default:
						//log.info("Attribute typecode " + typeCode +"unknown");
						break;
					}

				}	
				
				//guille
				
				log.info("NLRI type: ");	
				String currentName=null;
				
				if(att_ls!=null)
					pathAttributeListUtil.add(att_ls);
				if(att_mpreach!=null)
					pathAttributeListUtil.add(att_mpreach);
				if(att_path!=null) {
					//More than 1 as_path segment??
					List<AS_Path_Segment> as_path_segments= ((AS_Path_Attribute)att_path).getAsPathSegments();
					AS_Path_Segment as_path_segment;
					int as_path=0;
					if(as_path_segments.size()>0){
						as_path_segment=as_path_segments.get(0);
						int numberOfSeg=as_path_segment.getNumberOfSegments();
						as_path=as_path_segment.getSegments()[0];
					}
					update.setAsPathSegment(as_path);
				}

				if (pathAttributeListUtil != null){
					for (int i=0;i<pathAttributeListUtil.size();i++){
						att = pathAttributeListUtil.get(i);
						int typeCode = att.getTypeCode();
						switch (typeCode){	
						// cuando encontramos el link state attribute rellenamos las tlvs que nos llegan para luego
						// meterlas en la te_info o en la node_info
						case PathAttributesTypeCode.PATH_ATTRIBUTE_TYPECODE_BGP_LS_ATTRIBUTE:
							processAttributeLinkState((LinkStateAttribute) att);
							PathAttributeMsg pathAtt = new PathAttributeMsg((LinkStateAttribute)att);
							log.info("Path attributes: " + pathAtt.toString());
							//get node name for current update so then its possible to substitute for the nodeID 
							currentName=pathAtt.getNodeName();
							updateMsgList.addpathToJson(pathAtt);
							continue;
							// cuando procesamos el mp_reach distinguimos entre nodo y link...
							// prefijo aun por hacer
						case PathAttributesTypeCode.PATH_ATTRIBUTE_TYPECODE_MP_REACH_NLRI:
							int afi;
							afi = ((MP_Reach_Attribute)att).getAddressFamilyIdentifier();
							update.setAFI(afi);//set afi for grpc msg
							InetAddress nextHop=((MP_Reach_Attribute)att).getNextHop();
							update.setNextHop(nextHop);//set for grpc msg
							if (afi == AFICodes.AFI_BGP_LS){
								LinkStateNLRI nlri = (LinkStateNLRI) ((BGP_LS_MP_Reach_Attribute)att).getLsNLRI();
								int nlriType =  nlri.getNLRIType();
								
								switch (nlriType){
								case NLRITypes.Link_NLRI:
									// if(((BGP_LS_MP_Reach_Attribute)att).getLsNLRIList().size()<1){
									// 	log.info("Link_NLRI");
									// 	LinkNLRIMsg LnlriMsg = new LinkNLRIMsg((LinkNLRI)nlri,learntFrom);
									// 	log.info("Link info: " + LnlriMsg.toString());
									// 	updateMsgList.addLinkToJson(LnlriMsg);
									// 	update.setLink(LnlriMsg);//set for grpc msg , to be deprecated
									// 	update.addLink(LnlriMsg);//set for grpc msg
									// }else{
										for(LinkStateNLRI linkstateNLRI : (List<LinkStateNLRI>) ((BGP_LS_MP_Reach_Attribute)att).getLsNLRIList()){
											log.info("Link_NLRI");
											LinkNLRIMsg LnlriMsg = new LinkNLRIMsg((LinkNLRI)linkstateNLRI,learntFrom);
											log.info("Link info: " + LnlriMsg.toString());
											updateMsgList.addLinkToJson(LnlriMsg);
											update.addLink(LnlriMsg);//set for grpc msg
										}
									// }
									continue;
								case NLRITypes.Node_NLRI:
									// NodeNLRIMsg NnlriMsg = new NodeNLRIMsg((NodeNLRI)nlri,learntFrom,currentName);
									// log.info("Node_NLRI");
									// log.info("Node info: " + NnlriMsg.toString());
									// updateMsgList.addNodeToJson(NnlriMsg,currentName);
									// update.setNode(NnlriMsg);//set for grpc msg
									// currentName=null;
									for(LinkStateNLRI linkstateNLRI : (List<LinkStateNLRI>) ((BGP_LS_MP_Reach_Attribute)att).getLsNLRIList()){
										log.info("Node_NLRI");
										NodeNLRIMsg NnlriMsg = new NodeNLRIMsg((NodeNLRI)linkstateNLRI,learntFrom,currentName);
										log.info("Node info: " + NnlriMsg.toString());
										updateMsgList.addNodeToJson(NnlriMsg,currentName);
										update.addNode(NnlriMsg);//set for grpc msg
									}
									currentName=null;
									continue;
								case NLRITypes.Prefix_v4_NLRI://POR HACER...
									log.info("Prefix_v4_NLRI");
									continue;
								case NLRITypes.IT_Node_NLRI:
									log.info("IT_Node_NLRI");
									continue;
								default:
									log.debug("Attribute Code unknown");
								}
								
							}
							continue;
						default:
							log.debug("Attribute Code unknown");
						}
						
						
						
					}//fin for
					try {m.writeFile(updateMsgList);} catch (IOException e) {e.printStackTrace();}
				}
				
				//
				
				
				log.warn("\n");
//				System.out.println(update.toString());
				//cambiar clase?
				log.info("--->Sending to grpc manager");
				try {
					grpcClient.sendGrpcUpdateMsg(update);
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				//fin guille
				
				
				
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			j++;
		}//fin while
		// try {
		// 	channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
		// } catch (InterruptedException e) {
		// 	// TODO Auto-generated catch block
		// 	e.printStackTrace();
		// }
		System.exit(0);
	}


	
	/**
	 * Function which process the attribute link State. It updates the fields passed by argument. 
	 */
	private void processAttributeLinkState(LinkStateAttribute lsAtt){

		if (lsAtt.getMaximumLinkBandwidthTLV() != null){
			maximumLinkBandwidthTLV = lsAtt.getMaximumLinkBandwidthTLV();
		}

		if (lsAtt.getMaxReservableBandwidthTLV() != null){
			maxReservableBandwidthTLV = lsAtt.getMaxReservableBandwidthTLV();
		}
		if (lsAtt.getUnreservedBandwidthTLV() != null){
			unreservedBandwidthTLV = lsAtt.getUnreservedBandwidthTLV();
		}
		if(lsAtt.getAdministrativeGroupTLV() != null){
			administrativeGroupTLV = lsAtt.getAdministrativeGroupTLV();
		}
		if(lsAtt.getLinkProtectionTLV() != null){
			linkProtectionTLV = lsAtt.getLinkProtectionTLV();
		}
		if(lsAtt.getIPv4RouterIDLocalNodeLATLV()!= null){
			iPv4RouterIDLocalNodeLATLV = lsAtt.getIPv4RouterIDLocalNodeLATLV();
		}
		if(lsAtt.getIPv4RouterIDRemoteNodeLATLV()!=null){
			iPv4RouterIDRemoteNodeLATLV = lsAtt.getIPv4RouterIDRemoteNodeLATLV();
		}
		if(lsAtt.getMetricTLV() != null){
			metricTLV = lsAtt.getMetricTLV();
		}
		if(lsAtt.getTEMetricTLV()!=null){
			TEMetricTLV = lsAtt.getTEMetricTLV();
		}
		if(lsAtt.getNodeFlagBitsTLV()!= null){
			nodeFlagBitsTLV = lsAtt.getNodeFlagBitsTLV();
		}
		if(lsAtt.getNodeNameTLV() != null){
			nodeNameTLV = lsAtt.getNodeNameTLV();
		}
		if(lsAtt.getAreaIDTLV() != null){
			areaIDTLV = lsAtt.getAreaIDTLV();
		}
		if(lsAtt.getIgpFlagBitsTLV() != null){
			igpFlagBitsTLV= lsAtt.getIgpFlagBitsTLV();
		}
		if(lsAtt.getRouteTagTLV() != null){
			routeTagTLV = lsAtt.getRouteTagTLV();
		}
		if(lsAtt.getOSPFForwardingAddrTLV() != null){
			OSPFForwardingAddrTLV = lsAtt.getOSPFForwardingAddrTLV();
		}
		if(lsAtt.getSidLabelTLV()!=null){
			sidTLV = lsAtt.getSidLabelTLV();
		}

		if (lsAtt.getAvailableLabels() != null){
			this.availableLabels =lsAtt.getAvailableLabels();
		}
		if (lsAtt.getMF_OTP_ATLV() != null){
			this.mF_OTP_ATLV =lsAtt.getMF_OTP_ATLV();
		}

		if (lsAtt.getTransceiverClassAndAppATLV() != null){
			this.transceiverClassAndAppATLV =lsAtt.getTransceiverClassAndAppATLV();
		}

	}
	/**
	 * Function which process the link NLRI. It updates the fields passed by argument.
	 * @param linkNLRI
	 * @param maximumLinkBandwidthTLV
	 * @param maxReservableBandwidthTLV
	 * @param unreservedBandwidthTLV
	 * @param availableLabels
	 */


	/** Procesar un link significa:
	 * crear los vertices si no existen ya
	 * crear la edge si no existe ya
	 * crear la te_info o actualizarla
	 * @param linkNLRI
	 * @param learntFrom 
	 */

	

	private void clearAttributes(){
		maximumLinkBandwidthTLV= null;
		maxReservableBandwidthTLV= null;
		unreservedBandwidthTLV= null;
		administrativeGroupTLV = null;
		linkProtectionTLV =null;
		metricTLV = null;
		iPv4RouterIDLocalNodeLATLV = null;
		iPv4RouterIDRemoteNodeLATLV = null;
		TEMetricTLV = null;				
		transceiverClassAndAppATLV = null;
		mF_OTP_ATLV = null;
		availableLabels=null;
		linkDelay=0;
		linkDelayVar=0;
		minDelay=0;
		maxDelay=0;
		linkLoss=0;
		residualBw=0;
		availableBw=0;
		utilizedBw=0;

	}



}
