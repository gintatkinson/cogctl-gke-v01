// Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

const PROTO_PATH = path.resolve(__dirname, '../../../../proto/dlt_gateway.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const dltProto = grpc.loadPackageDefinition(packageDefinition).dlt;

const client = new dltProto.DltGatewayService(
  '127.0.0.1:32001', // Replace with TFS server IP_ADDRESS
  grpc.credentials.createInsecure()
);

function subscribeToDlt() {
  const request = {
    // Define any necessary subscription filters here if applicable
  };

  const call = client.SubscribeToDlt(request);

  call.on('data', (event) => {
    console.log('Received event:', event);
  });

  call.on('error', (error) => {
    console.error('Error:', error.message);
  });

  call.on('end', () => {
    console.log('Stream ended.');
  });

  // Optionally, you can cancel the subscription after a certain time or condition
  setTimeout(() => {
    console.log('Cancelling subscription...');
    call.cancel();
  }, 600000); // Cancel after 1 minute for demonstration purposes
}

function runTests() {
  console.log("Testing subscription to DLT events");
  subscribeToDlt();
}

runTests();
