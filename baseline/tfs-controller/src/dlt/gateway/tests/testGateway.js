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
const fs = require('fs').promises;
const { v4: uuidv4 } = require('uuid'); // Import the UUID library


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

const assetId = `asset-${Date.now()}`;
const domainUuid = `domain-${uuidv4()}`; // Generate a pretty domain UUID

async function getTopoData(filename) {
    try {
        const data = await fs.readFile(`../samples/${filename}`, 'utf8');
        return data;
    } catch (error) {
        console.error('Failed to read file:', filename, error);
        return '{}'; // Empty JSON if error
    }
}

async function processTopoData(operation, assetId, jsonFilename) {
    let jsonData = '{}';
    if (jsonFilename) {
        jsonData = await getTopoData(jsonFilename);
    }

    const request = {
        record_id: {
            domain_uuid: { uuid: domainUuid },  // Replace "domain-uuid" with actual domain UUID if needed
            type: 'DLTRECORDTYPE_TOPOLOGY',  // Use the appropriate type if needed
            record_uuid: { uuid: assetId }
        },
        operation,
        data_json: jsonData
    };

    return new Promise((resolve, reject) => {
        client.RecordToDlt(request, (error, response) => {
            if (error) {
                console.error('Error:', error.message);
                reject(error);
            } else {
                console.log('Response:', response);
                resolve(response);
            }
        });
    });
}

async function getDLTData(assetId) {

    const request = {
        domain_uuid: { uuid: domainUuid },  // Replace "domain-uuid" with actual domain UUID if needed
        type: 'DLTRECORDTYPE_TOPOLOGY',  // Use the appropriate type if needed
        record_uuid: { uuid: assetId }
    };

    return new Promise((resolve, reject) => {
        client.GetFromDlt(request, (error, response) => {
            if (error) {
                console.error('Error:', error.message);
                reject(error);
            } else {
                console.log('Response:', response);
                resolve(response);
            }
        });
    });
}

async function runTests() {
    console.log("Testing Store Operation");
    await processTopoData('DLTRECORDOPERATION_ADD', assetId, 'topo2.json');

    console.log("Testing Update Operation");
    await processTopoData('DLTRECORDOPERATION_UPDATE', assetId, 'topo3.json');

    console.log("Testing Fetch Operation");
    await getDLTData(assetId);


    console.log("Testing Delete Operation");
    await processTopoData('DLTRECORDOPERATION_DELETE', assetId);

    console.log("Testing Fetch All Operation");
    // This part assumes you have a GetAllInfo method implemented in your chaincode and corresponding gRPC service.
    // client.GetAllInfo({}, (error, response) => {
    //   if (error) {
    //     console.error('Error:', error.message);
    //   } else {
    //     console.log('All Data:', response);
    //   }
    // });
}

runTests().catch(console.error);
