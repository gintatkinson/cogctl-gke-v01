# DLT Gateway

## Description

The DLT Gateway consists of a **fabricConnect.ts** TypeScript file, which contains the logic for identification
management (certificates required for the MSP), connection management to the blockchain, and finally, it exposes a
contract object with all the required information for interacting with the chaincode. The **fabricConnect.ts** is
coded following the Fabric Gateway API recommendations from Hyperledger Fabric 2.4+. The compiled **fabricConnect.ts**
logic is imported into a **dltGateway.js** file, which contains the gRPC logic for interaction with the TFS controller.
Testing code for various performance tests is included inside the [/tests](./tests/) folder.

The chaincode is written in Go, providing a reference for the operations that are recorded in the blockchain. This
chaincode must already be deployed in a working Hyperledger Fabric blockchain.

## Requisites

* NodeJS
* Docker
* Kubernetes (K8s)
 
Sign and TLS certificates, and private key of the MSP user from the Hyperledger Fabric deployment must be copied to the
[/keys](./keys/) directory inside this repository.

Example:

```bash
cp ~/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/tls/ca.crt src/dlt/gateway/keys/

cp ~/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/signcerts/User1@org1.example.com-cert.pem src/dlt/gateway/keys/cert.pem

cp ~/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/User1@org1.example.com/msp/keystore/priv_sk src/dlt/gateway/keys/
```

These files are essential for establishing the identity and secure connection to the blockchain. Make sure you replace
the paths with your actual file locations from your Hyperledger Fabric deployment.
