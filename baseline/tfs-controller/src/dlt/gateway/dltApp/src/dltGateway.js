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
const { connectToNetwork } = require('../dist/fabricConnect');
const utf8Decoder = new TextDecoder();

// Load the protocol buffer definitions
const PROTO_PATH = path.resolve(__dirname, '../proto/dlt_gateway.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const dltProto = grpc.loadPackageDefinition(packageDefinition).dlt;

// Create a gRPC server instance
const server = new grpc.Server();
let contractInstance = null;
let closeConnection = null;
let events = null; // To store the events iterable

const clients = new Set(); // Set to keep track of active client streams



// Initialize connection to the chaincode

async function initChaincodeConnection() {
  try {
    const networkResources = await connectToNetwork();
    contractInstance = networkResources.contract;
    events = networkResources.events; // Initiate event listening
    closeConnection = networkResources.close;

    //console.log("DEBUG", events)
    console.log("Chaincode connection established successfully.");
  } catch (error) {
    console.error('Failed to establish chaincode connection:', error);
    process.exit(1); // Exit if the connection cannot be established
  }
}

// gRPC method to handle recording data to the DLT
async function recordToDlt(call, callback) {
  if (!contractInstance) {
    callback({
      code: grpc.status.UNAVAILABLE,
      details: "Chaincode connection is not established."
    });
    return;
  }
  const { record_id, operation, data_json } = call.request;
  try {


    console.log(`Operation requested: ${operation}`);

    switch (operation) {
      case 'DLTRECORDOPERATION_ADD':
        await contractInstance.submitTransaction('StoreRecord', JSON.stringify(record_id), data_json);
        break;
      case 'DLTRECORDOPERATION_UPDATE':
        await contractInstance.submitTransaction('UpdateRecord', JSON.stringify(record_id), data_json);
        break;
      case 'DLTRECORDOPERATION_DELETE':
        await contractInstance.submitTransaction('DeleteRecord', JSON.stringify(record_id));
        break;
      default:
        throw new Error('Invalid operation');
    }
    // Send success response
    callback(null, { record_id, status: 'DLTRECORDSTATUS_SUCCEEDED' });
  } catch (error) {
    // Send failure response with error message
    console.log("ERRROR", error)
    callback(null, { record_id, status: 'DLTRECORDSTATUS_FAILED', error_message: error.message });
  }
}

// gRPC method to fetch data from the DLT
async function getFromDlt(call, callback) {

  if (!contractInstance) {
    callback({
      code: grpc.status.UNAVAILABLE,
      details: "Chaincode connection is not established."
    });
    return;
  }

  try {

    console.log("RECEIVED CALL REQUEST:", call.request);
    //const { record_id, operation, data_json } = call.request;
    const resultBytes = await contractInstance.evaluateTransaction('RetrieveRecord', JSON.stringify(call.request));
    // Decode and parse the result
    const resultJson = utf8Decoder.decode(resultBytes);
    const result = JSON.parse(resultJson);

    // Send the response with the formatted JSON data
    callback(null, { record_id: call.request, operation: result.operation, data_json: result.data_json });
  } catch (error) {   
   if (error.message.includes("data not found for key")) {
    // Return an empty response when no record is found
    console.log("REQUEST ERROR:", error);
    const emptyRecordId = {
      domain_uuid: { uuid: "" },
      type: 'DLTRECORDTYPE_UNDEFINED',
      record_uuid: { uuid: "" }
    };
    callback(null, { record_id: emptyRecordId, data_json: "" });
  } else {
    // Send failure response with error message
    callback({
      code: grpc.status.UNKNOWN,
      details: error.message
    });
   }
  }
}

// Implement subscription to DLT events

const eventNameToEventTypeEnum = {
  'StoreRecord': 'EVENTTYPE_CREATE',
  'UpdateRecord': 'EVENTTYPE_UPDATE',
  'DeleteRecord': 'EVENTTYPE_REMOVE'
};

function subscribeToDlt(call) {
  if (!events) {
    call.emit('error', {
      code: grpc.status.UNAVAILABLE,
      details: "Event listener is not established."
    });
    return;
  }

  // Add the client to the set of active clients
  clients.add(call);
  console.log(`Client connected. Total clients: ${clients.size}`);

  // Clean up when the client disconnects
  call.on('cancelled', () => {
    clients.delete(call);
    console.log(`Client disconnected (cancelled). Total clients: ${clients.size}`);

  });
  call.on('error', (err) => {
    clients.delete(call);
    console.log(`Client disconnected (error: ${err.message}). Total clients: ${clients.size}`);

  });
  call.on('end', () => {
    clients.delete(call);
    console.log(`Client disconnected (end). Total clients: ${clients.size}`);

  });

  (async () => {
    try {
      for await (const event of events) {
        const eventPayload = event.payload;
        //console.log("Raw event payload:", eventPayload);
        const resultJson = utf8Decoder.decode(eventPayload);
        const eventJson = JSON.parse(resultJson);

        console.log("Writing event to stream:", eventJson.record_id);

        const eventType = eventNameToEventTypeEnum[event.eventName] || 'EVENTTYPE_UNDEFINED';

        for (const client of clients) {
          const writeSuccessful = client.write({
            event: {
              timestamp: { timestamp: Math.floor(Date.now() / 1000) },
              event_type: eventType // Set appropriate event type
            },
            record_id: {
              domain_uuid: { uuid: eventJson.record_id.domain_uuid.uuid },
              type: eventJson.record_id.type || 'DLTRECORDTYPE_UNDEFINED',
              record_uuid: { uuid: eventJson.record_id.record_uuid.uuid }
            }
          });
          
          // Check if the internal buffer is full
          if (!writeSuccessful) {
            // Wait for the 'drain' event before continuing
            await new Promise((resolve) => client.once('drain', resolve));
          }
        }
      }

      //call.end();

    } catch (error) {
      for (const client of clients) {
        client.emit('error', {
          code: grpc.status.UNKNOWN,
          details: `Error processing event: ${error.message}`
        });

      }
    }
  })();
}

// Placeholder
function getDltStatus(call, callback) {
  // Implement status fetching logic here
  // Not implemented for simplicity
}

// Placeholder
function getDltPeers(call, callback) {
  // Implement peers fetching logic here
  // Not implemented for simplicity
}

// Add the service to the server
server.addService(dltProto.DltGatewayService.service, {
  RecordToDlt: recordToDlt,
  GetFromDlt: getFromDlt,
  SubscribeToDlt: subscribeToDlt,
  GetDltStatus: getDltStatus,
  GetDltPeers: getDltPeers,
});

// Start the server
const PORT = process.env.GRPC_PORT || '50051';
server.bindAsync(`0.0.0.0:${PORT}`, grpc.ServerCredentials.createInsecure(), async (error) => {
  if (error) {
    console.error('Failed to bind server:', error);
    return;
  }
  console.log(`gRPC server running at http://0.0.0.0:${PORT}`);
  await initChaincodeConnection();  //Connects to the chaincode and 
  server;
});

// Handle shutdown gracefully
process.on('SIGINT', async () => {
  console.log('Shutting down...');
  await closeConnection();
  server.forceShutdown();
});