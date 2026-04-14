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

package eu.teraflow.tid.bgp4Peer.json;

import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

import org.codehaus.jackson.JsonEncoding;
import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.JsonGenerator;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.annotate.JsonSerialize.Inclusion;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import eu.teraflow.tid.bgp4Peer.models.LinkNLRIMsg;
import eu.teraflow.tid.bgp4Peer.models.NodeNLRIMsg;
import eu.teraflow.tid.bgp4Peer.models.PathAttributeMsg;
import eu.teraflow.tid.bgp4Peer.models.UpdateMsg;
import eu.teraflow.tid.bgp4Peer.models.UpdateMsgList;

public class bgpMarshal {

	
	ObjectMapper mapper = new ObjectMapper();
	JsonGenerator g;
	FileWriter fWriter;
	public void bgpMarshaller() throws IOException{
		
		
		mapper.setSerializationInclusion(Inclusion.NON_NULL);
		mapper.setSerializationInclusion(Inclusion.NON_EMPTY);
		
		
		
//		String jsonStr = mapper.writeValueAsString(node);
//		mapper.writeValue(new File("target/node.json"), nodeList);
//		System.out.println(jsonStr);
		
	}
	public void writeFile(UpdateMsgList update) throws JsonGenerationException, JsonMappingException, IOException {
		
		g = mapper.getJsonFactory().createJsonGenerator(new File("node.json"), JsonEncoding.UTF8);
//		update=update.id2Name();
		mapper.writeValue(g, update);
		String temp = mapper.writeValueAsString(update)+"\n";
//		FileOutputStream fos = new FileOutputStream("target/update.json", true);
//		fos.write(temp.getBytes());
//	    fos.close();
		fWriter = new FileWriter("updateWriter.json");
//		if(temp.length()>2)
		fWriter.write(temp);
	    
	    
		
	}
	public void closeFile() throws IOException {
		g.close();
		fWriter.close();
	}
	
	
	
}
