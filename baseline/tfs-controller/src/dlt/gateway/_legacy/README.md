```
     NEC Laboratories Europe GmbH

     PROPRIETARY INFORMATION

 The software and its source code contain valuable trade secrets and
 shall be maintained in confidence and treated as confidential
 information. The software may only be used for evaluation and/or
 testing purposes, unless otherwise explicitly stated in a written
 agreement with NEC Laboratories Europe GmbH.

 Any unauthorized publication, transfer to third parties or
 duplication of the object or source code - either totally or in
 part - is strictly prohibited.

          Copyright (c) 2022 NEC Laboratories Europe GmbH
          All Rights Reserved.

 Authors: Konstantin Munichev <konstantin.munichev@neclab.eu>


 NEC Laboratories Europe GmbH DISCLAIMS ALL WARRANTIES, EITHER
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES
 OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE AND THE
 WARRANTY AGAINST LATENT DEFECTS, WITH RESPECT TO THE PROGRAM AND
 THE ACCOMPANYING DOCUMENTATION.

 NO LIABILITIES FOR CONSEQUENTIAL DAMAGES: IN NO EVENT SHALL NEC
 Laboratories Europe GmbH or ANY OF ITS SUBSIDIARIES BE LIABLE FOR
 ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR
 LOSS OF BUSINESS PROFITS, BUSINESS INTERRUPTION, LOSS OF
 INFORMATION, OR OTHER PECUNIARY LOSS AND INDIRECT, CONSEQUENTIAL,
 INCIDENTAL, ECONOMIC OR PUNITIVE DAMAGES) ARISING OUT OF THE USE OF
 OR INABILITY TO USE THIS PROGRAM, EVEN IF NEC Laboratories Europe
 GmbH HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

 THIS HEADER MAY NOT BE EXTRACTED OR MODIFIED IN ANY WAY.
 ```

# DLT module guide

## General information
The DLT module is used to provide access to the underlying Fabric deployment. It allows clients
to add, retrieve, modify and delete blockchain-backed data, essentially working as a key-value
database. External clients should use gRPC API to communicate with this service, its detailed
description available below.

## Code structure
The whole DLT module consists of several packages:
- fabric package
- http package
- proto package
- client example

### Fabric package
The most important class in this package is `FabricConnector`. First, it establishes connection
with the underlying Fabric network using Java Gateway SDK. After that, it could be used as a
CRUD interface.
Other files contain auxiliary code for `FabricConnector` which allows it to register/enroll
users and to obtain smart contract instances.

### Grpc package
Contains server side gRPC handler. It accepts requests from the outside and performs the
requested operation. For the more detailed description see Proto package description right below.

### Proto package
The proto package contains `dlt.proto` file which defines gRPC service `DltService` API and messages
it uses. There are 3 main functions: `RecordToDlt` which allows to create/modify/delete data,
`GetFromDlt` which returns already written data and `SubscribeToDlt` which allows clients subscribe
for future create/modify/delete events with provided filters.
Other proto files don't play any significant role and could be safely ignored by end users.

### Client example
This code is not necessary to the service, but it could be used to test the service. It contains
a sample gRPC client which connects the service and perform all the CRUD operations. 

# Fabric deployment notes

## General notes
Current Fabric deployment uses Fabric test network with some additional helping scripts on top of it.
To start the network just run the `raft.sh` from `blockchain/scripts` directory. Use `stop.sh`
when you need to stop the network.

## Server start preparations
To run the server it's necessary to copy certificate file
`fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/ca/ca.org1.example.com-cert.pem`
to the config folder (replacing the existing one). Also, it's necessary to copy `scripts/connection-org1.json`
file (again, replacing the old one). After copying, it must be edited. First, all `localhost` entrances
should be replaced with `teraflow.nlehd.de`. Second, `channel` section at the end of the file should be removed.
This should be done after every restart of the Fabric network.

## Fabric configuration
Even though a test network is easy to deploy and use it's better to perform a custom configuration
for a production deployment. In practice every participating organization will likely prefer to have
its own Peer/Orderer/CA instances to prevent possible dependency on any other participants. This leads
not only to a better privacy/availability/security in general but also to the more complicated
deployment process as a side effect. Here we provide a very brief description of the most important points.

### Organizations
Organization represents a network participant, which can be an individual, a large corporation or any other
entity. Each organization has its own CAs, orderers and peers. The recommendation here is to create an
organization entity for every independent participant and then decide how many CAs/peers/orderers does
every organization need and which channels should it has access to based on the exact project's goals. 

### Channels
Each channel represents an independent ledger with its own genesis block. Each transaction is executed
on a specific channel, and it's possible to define which organization has access to a given channel.
As a result channels are a pretty powerful privacy mechanism which allows to limit access to the private
data between organization.

### Certificate authorities, peers and orderers
Certificate authorities (CA) are used to generate crypto materials for each organization. Two types of CA
exist: one is used to generate the certificates of the admin, the MSP and certificates of non-admin users.
Another type of CA is used to generate TLS certificates. As a result it's preferable to have at least two
CAs for every organization.

Peers are entities which host ledgers and smart contracts. They communicate with applications and orderers,
receiving chaincode invocations (proposals), invoking chaincode, updating ledger when necessary and
returning result of execution. Peers can handle one or many ledgers, depending on the configuration. It's
very use case specific how many peers are necessary to the exact deployment.

Orderers are used to execute a consensus in a distributing network making sure that every channel participant
has the same blocks with the same data. The default consensus algorithm is Raft which provides only a crash
fault tolerance.

### Conclusion
As you can see, configuration procedure for Fabric is pretty tricky and includes quite a lot of entities.
In real world it will very likely involve participants from multiple organizations each of them performing
its own part of configuration.

As a further reading it's recommended to start with the
[official deployment guide](https://hyperledger-fabric.readthedocs.io/en/release-2.2/deployment_guide_overview.html).
It contains a high level overview of a deployment process as well as links to the detailed descriptions to
CA/Peer/Orderer configuration descriptions.