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
const logFilePath = './transaction_times_TPS_TOPO3.txt';
const utf8Decoder = new TextDecoder();
const topoDirectory = '../samples/';

async function main() {
    const { contract, close } = await connectToNetwork();
    try {
        const rates = [10, 50, 250, 500]; // Transactions per second
        for (let i = 0; i < 1000; i++) {
                for (let rate of rates) {
                    console.log(`Testing at ${rate} TPS`);
                    await performLoadTest(contract, 1000, rate);
            }
    }
    } finally {
        await close(); // Ensure to close the network connection
    }
}

async function performLoadTest(contract, totalTransactions, rate) {
    const interval = 1000 / rate; // Calculate interval in milliseconds
    let promises = [];
    const startTime = Date.now();

    for (let i = 0; i < totalTransactions; i++) {
        // Queue a transaction promise
        promises.push(sendTransaction(contract, `asset${Date.now() + i}`));

        // Process in batches according to the rate
        if ((i + 1) % rate === 0 || i === totalTransactions - 1) {
            await Promise.all(promises); // Send a batch of transactions
            promises = []; // Reset for the next batch
            if (i < totalTransactions - 1) {
                await new Promise(resolve => setTimeout(resolve, interval)); // Throttle the transaction sending
            }
        }
    }

    const endTime = Date.now();
    const totalTime = endTime - startTime;
    const actualRate = totalTransactions / (totalTime / 1000);
    console.log(`Total time for ${totalTransactions} transactions at target ${rate} TPS: ${totalTime} ms`);
    console.log(`Actual rate achieved: ${actualRate.toFixed(2)} TPS`);
    await appendFile(logFilePath, `Target Rate: ${rate} TPS, Total Time: ${totalTime} ms, Actual Rate: ${actualRate.toFixed(2)} TPS\n`);
}

async function sendTransaction(contract, assetId) {
    try {
        const jsonData = await readJsonData(`${topoDirectory}topo3.json`);
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
