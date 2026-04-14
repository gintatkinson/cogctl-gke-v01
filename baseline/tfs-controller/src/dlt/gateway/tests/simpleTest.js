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
const fs = require('fs');
const util = require('util');
const appendFile = util.promisify(fs.appendFile);
const logFilePath = './transaction_times_TPS2.txt';
const utf8Decoder = new TextDecoder();
const topoDirectory = '../samples/';

async function main() {
    const { contract, close } = await connectToNetwork();
    try {
        console.log('Testing with 8 consecutive transactions');
        await performLoadTest(contract);
    } finally {
        await close(); // Ensure to close the network connection
    }
}

async function performLoadTest(contract) {
    const totalTransactions = 500;
    const promises = [];
    const startTime = Date.now();

    for (let i = 0; i < totalTransactions; i++) {
        // Queue a transaction promise
        promises.push(sendTransaction(contract, `asset${startTime}_${i}`));
    }

    await Promise.all(promises); // Send all transactions

    const endTime = Date.now();
    const totalTime = endTime - startTime;
    const actualRate = totalTransactions / (totalTime / 1000);
    console.log(`Total time for ${totalTransactions} transactions: ${totalTime} ms`);
    console.log(`Actual rate achieved: ${actualRate.toFixed(2)} TPS`);
    await appendFile(logFilePath, `Total Transactions: ${totalTransactions}, Total Time: ${totalTime} ms, Actual Rate: ${actualRate.toFixed(2)} TPS\n`);
}

async function sendTransaction(contract, assetId) {
    try {
        const jsonData = await readJsonData(`${topoDirectory}topo4.json`);
        //const jsonData = JSON.stringify({ data: `Data for ${assetId}`});
        const result = await contract.submitTransaction('StoreTopoData', assetId, jsonData);
        return utf8Decoder.decode(result);
    } catch (error) {
        console.error('Transaction failed:', error);
        return null;
    }
}

async function readJsonData(filePath) {
    try {
        return await fs.promises.readFile(filePath, 'utf8');
    } catch (error) {
        console.error(`Failed to read file: ${filePath}`, error);
        return '{}';
    }
}

main().catch(console.error);
