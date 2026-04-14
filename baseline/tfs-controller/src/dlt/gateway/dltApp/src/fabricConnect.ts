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

import * as grpc from '@grpc/grpc-js';
import { connect, Contract, Identity, Signer, signers, Network, CloseableAsyncIterable, ChaincodeEvent, GatewayError } from '@hyperledger/fabric-gateway';
import * as crypto from 'crypto';
import { promises as fs } from 'fs';
import * as path from 'path';
import { TextDecoder } from 'util';
import * as dotenv from 'dotenv';

dotenv.config({ path: path.resolve(__dirname, '..', '.env') });
const channelName = getEnvVar('CHANNEL_NAME');
const chaincodeName = getEnvVar('CHAINCODE_NAME');
const mspId = getEnvVar('MSP_ID');


// Path to user private key directory.
const keyDirectoryPath = getEnvVar('KEY_DIRECTORY_PATH');

// Path to user certificate directory.
const certDirectoryPath = getEnvVar('CERT_DIRECTORY_PATH');

// Path to peer tls certificate.
const tlsCertPath = getEnvVar('TLS_CERT_PATH');

// Gateway peer endpoint.
const peerEndpoint = getEnvVar('PEER_ENDPOINT');

// Gateway peer SSL host name override.
const peerHostAlias = getEnvVar('PEER_HOST_ALIAS');

const utf8Decoder = new TextDecoder();
const assetId = `asset${Date.now()}`;

export async function connectToNetwork(): Promise<{ contract: Contract, events: CloseableAsyncIterable<ChaincodeEvent>, close: () => Promise<void> }> {

    await displayInputParameters();

    // The gRPC client connection should be shared by all Gateway connections to this endpoint.

    const client = await newGrpcConnection();

    const gateway = connect({
        client,
        identity: await newIdentity(),
        signer: await newSigner(),
        // Default timeouts for different gRPC calls
        evaluateOptions: () => {
            return { deadline: Date.now() + 5000 }; // 5 seconds
        },
        endorseOptions: () => {
            return { deadline: Date.now() + 15000 }; // 15 seconds
        },
        submitOptions: () => {
            return { deadline: Date.now() + 5000 }; // 5 seconds
        },
        commitStatusOptions: () => {
            return { deadline: Date.now() + 60000 }; // 1 minute
        },
    });

    let events: CloseableAsyncIterable<ChaincodeEvent> | undefined;


    // Get a network instance representing the channel where the smart contract is deployed.
    const network = gateway.getNetwork(channelName);

    // Get the smart contract from the network.
    const contract = network.getContract(chaincodeName);

    //Listen for events emitted by transactions
    //events = await startEventListening(network);
    events = await network.getChaincodeEvents(chaincodeName);

    // Initialize the ledger.
    await initLedger(contract);

    console.log(Date.now())

    return {
        contract: contract,
        events: events,
        close: async function () {
            if (events) events.close();
            gateway.close();
            client.close();
        }
    };


}

async function newGrpcConnection(): Promise<grpc.Client> {
    const tlsRootCert = await fs.readFile(tlsCertPath);
    const tlsCredentials = grpc.credentials.createSsl(tlsRootCert);
    return new grpc.Client(peerEndpoint, tlsCredentials, {
        'grpc.ssl_target_name_override': peerHostAlias,
    });
}

async function newIdentity(): Promise<Identity> {
    //const certPath = await getFirstDirFileName(certDirectoryPath);
    //console.log("DEBUG", certDirectoryPath);
    const credentials = await fs.readFile(certDirectoryPath);
    return { mspId, credentials };
}


async function newSigner(): Promise<Signer> {
    //const keyPath = await getFirstDirFileName(keyDirectoryPath);
    //console.log("DEBUG2", keyDirectoryPath);
    const privateKeyPem = await fs.readFile(keyDirectoryPath);
    const privateKey = crypto.createPrivateKey(privateKeyPem);
    return signers.newPrivateKeySigner(privateKey);
}

/**
 * This type of transaction would typically only be run once by an application the first time it was started after its
 * initial deployment. A new version of the chaincode deployed later would likely not need to run an "init" function.
 */
async function initLedger(contract: Contract): Promise<void> {
    try {
        console.log('\n--> Submit Transaction: InitLedger, function activates the chaincode');

        await contract.submitTransaction('InitLedger');

        console.log('*** Transaction committed successfully');
    } catch (error) {
        console.error('Failed to submit InitLedger transaction:', error);
        throw error;
    }
}



/**
 * getEnvVar() will return the value of an environment variable.
 */
function getEnvVar(varName: string): string {
    const value = process.env[varName];
    if (!value) {
        throw new Error(`Environment variable ${varName} is not set`);
    }
    return value;
}

/**
 * displayInputParameters() will print the global scope parameters used by the main driver routine.
 */
async function displayInputParameters(): Promise<void> {
    console.log(`channelName:       ${channelName}`);
    console.log(`chaincodeName:     ${chaincodeName}`);
    console.log(`mspId:             ${mspId}`);
    console.log(`keyDirectoryPath:  ${keyDirectoryPath}`);
    console.log(`certDirectoryPath: ${certDirectoryPath}`);
    console.log(`tlsCertPath:       ${tlsCertPath}`);
    console.log(`peerEndpoint:      ${peerEndpoint}`);
    console.log(`peerHostAlias:     ${peerHostAlias}`);
}

/**
 * startEventListening() will initiate the event listener for chaincode events.
 */
async function startEventListening(network: Network): Promise<CloseableAsyncIterable<ChaincodeEvent>> {
    console.log('\n*** Start chaincode event listening');

    const events = await network.getChaincodeEvents(chaincodeName);

    void readEvents(events); // Don't await - run asynchronously
    return events;
}

/**
 * readEvents() format and display the events as a JSON.
 */
async function readEvents(events: CloseableAsyncIterable<ChaincodeEvent>): Promise<void> {
    try {
        for await (const event of events) {
            const payload = parseJson(event.payload);
            console.log(`\n<-- Chaincode event received: ${event.eventName} -`, payload);
        }
    } catch (error: unknown) {
        // Ignore the read error when events.close() is called explicitly
        if (!(error instanceof GatewayError) || error.code !== grpc.status.CANCELLED.valueOf()) {
            throw error;
        }
    }
}

/**
 * parseJson() formats a JSON.
 */
function parseJson(jsonBytes: Uint8Array): unknown {
    const json = utf8Decoder.decode(jsonBytes);
    return JSON.parse(json);
}

