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

const { connectToNetwork } = require('../dltApp/dist/fabricConnect');
const fsp = require('fs').promises;
const fs = require('fs');
const util = require('util');

const utf8Decoder = new TextDecoder();
const topoDirectory = '../samples/';
const topologies = ['topo1.json', 'topo2.json', 'topo3.json', 'topo4.json'];
//const topologies = ['topo4.json'];

const iterations = 1000;

async function main() {
    try {
        const { contract, close } = await connectToNetwork();
        for (const topoFile of topologies) {
            const logFilePath = `./operation_times_${topoFile.split('.')[0]}.txt`; // Creates a separate logfile for each topology
            const appendFile = util.promisify(fs.appendFile.bind(fs, logFilePath)); 
            
            console.log(`Starting tests for ${topoFile}`);
            for (let i = 0; i < iterations; i++) {
                console.log(`Iteration ${i + 1} for ${topoFile}`);
                await runBlockchainOperations(contract, topoFile, appendFile); 
            }
        }
                await close(); // Clean up the connection
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

async function runBlockchainOperations(contract, topoFile, appendFile) {
    const assetId = `asset${Date.now()}`;
    const jsonData = await readJsonData(`${topoDirectory}${topoFile}`);

    // Define operations
    const operations = [
        { type: 'STORE', jsonData },
        { type: 'UPDATE', jsonData },
        { type: 'FETCH', jsonData: null },
        { type: 'DELETE', jsonData: null },
        { type: 'FETCH_ALL', jsonData: null }
    ];

    for (let op of operations) {
        await executeOperation(contract, op.type, assetId, op.jsonData, appendFile);
    }
}

async function readJsonData(filePath) {
    try {
        return await fsp.readFile(filePath, 'utf8');
    } catch (error) {
        console.error(`Failed to read file: ${filePath}`, error);
        return '{}';
    }
}

async function executeOperation(contract, operationType, assetId, jsonData, appendFile) {
    const startTime = process.hrtime.bigint();
    try {
        let result;
        switch (operationType) {
            case 'STORE':
                result = await contract.submitTransaction('StoreTopoData', assetId, jsonData);
                break;
            case 'UPDATE':
                result = await contract.submitTransaction('UpdateTopoData', assetId, jsonData);
                break;
            case 'FETCH':
                result = await contract.evaluateTransaction('RetrieveTopoData', assetId);
                break;
            case 'DELETE':
                result = await contract.submitTransaction('DeleteTopo', assetId);
                break;
            case 'FETCH_ALL':
                result = await contract.evaluateTransaction('GetAllInfo');
                break;
        }
        result = utf8Decoder.decode(result);
        const operationTime = recordOperationTime(startTime);
        await logOperationTime(operationTime, operationType, appendFile);
        console.log(`${operationType} Result:`, result);
    } catch (error) {
        console.error(`Error during ${operationType}:`, error);
    }
}

function recordOperationTime(startTime) {
    const endTime = process.hrtime.bigint();
    const operationTime = Number(endTime - startTime) / 1e6;
    return operationTime;
}

async function logOperationTime(operationTime, operationType, appendFile) {
    const timestamp = Date.now();
    const logEntry = `${timestamp} - ${operationType} - Execution time: ${operationTime.toFixed(3)} ms\n`;
    try {
        await appendFile(logEntry);
    } catch (error) {
        console, error('Error writing to log file:', error);
    }
}

main();
