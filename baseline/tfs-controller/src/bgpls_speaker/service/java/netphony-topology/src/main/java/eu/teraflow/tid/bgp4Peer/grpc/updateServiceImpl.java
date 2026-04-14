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

import io.grpc.stub.StreamObserver;
import src.main.proto.GrpcService.updateRequest;
import src.main.proto.GrpcService.updateResponse;
import src.main.proto.updateServiceGrpc.updateServiceImplBase;


public class updateServiceImpl extends updateServiceImplBase{

public void update(updateRequest request, StreamObserver<updateResponse> responseObserver) {
		
		System.out.println(request);
		
		updateResponse response = updateResponse.newBuilder()
			      .setAck("Update procesado, " + request )
			      .build();
		
		 // Use responseObserver to send a single response back
	    responseObserver.onNext(response);


	    // When you are done, you must call onCompleted.
	    responseObserver.onCompleted();
	    
	}

}
