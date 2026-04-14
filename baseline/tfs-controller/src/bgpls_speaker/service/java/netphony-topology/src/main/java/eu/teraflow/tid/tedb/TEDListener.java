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

import java.util.LinkedList;

import es.tid.ospf.ospfv2.lsa.tlv.subtlv.complexFields.BitmapLabelSet;

public interface TEDListener {

	public void notifyNewVertex(Object vertex);
	
	public void notifyNewEdge(Object source, Object destination);

	public void notifyWavelengthStatusChange(Object source, Object destination, BitmapLabelSet previousBitmapLabelSet, BitmapLabelSet newBitmapLabelSet);

	public void notifyWavelengthReservation(LinkedList<Object> sourceVertexList, LinkedList<Object> targetVertexList, int wavelength);

	public void notifyWavelengthEndReservation(LinkedList<Object> sourceVertexList, LinkedList<Object> targetVertexList, int wavelength);

	public void notifyTEDBFullUpdate();

	public void notifyNewEdgeIP(Object source, Object destination, TE_Information informationTEDB);

	public void notificationEdgeIP_AuxGraph(Object src, Object dst, TE_Information informationTEDB);

	public void notificationEdgeOPTICAL_AuxGraph(Object src, Object dst, int lambda);
	
}
