# Scenario Description

This scenario is composed of 4 TeraFlowSDN instances.
Each instance has its own local network topology detailed below.
Besides, each instance exposes an abstracted view of its local network domain.
Finally, the different domains are interconnected among them by means of the inter-domain links detailed below.

## Domain D1 (end for the end-to-end interdomain slice)

Domain D1 is composed of 5 emulated packet routers (Rx@D1) and 1 emulated DataCenter (DCGW@D1).
The DCGW@D1 is a termination endpoint for the end-to-end interdomain slice.
The internal domain connectivity is defined as follows:
- R1@D1/2 <--> R2@D1/1
- R2@D1/3 <--> R3@D1/2
- R2@D1/5 <--> R5@D1/2
- R3@D1/4 <--> R4@D1/3
- R4@D1/5 <--> R5@D1/4
- R5@D1/1 <--> R1@D1/5
- R1@D1/100 <--> DCGW@D1/eth1

## Domain D2 (transit for the end-to-end interdomain slice)

Domain D2 is composed of 6 emulated packet routers (Rx@D2).
This domain behaves as a transit domain for the end-to-end interdomain slice.
The internal domain connectivity is defined as follows:
- R1@D2/2 <--> R2@D2/1
- R1@D2/6 <--> R6@D2/1
- R1@D2/5 <--> R5@D2/1
- R2@D2/3 <--> R3@D2/2
- R2@D2/4 <--> R4@D2/2
- R2@D2/5 <--> R5@D2/2
- R2@D2/6 <--> R6@D2/2
- R3@D2/6 <--> R6@D2/3
- R4@D2/5 <--> R5@D2/4

## Domain D3 (transit for the end-to-end interdomain slice)

Domain D3 is composed of 6 emulated packet routers (Rx@D3).
This domain behaves as a transit domain for the end-to-end interdomain slice.
The internal domain connectivity is defined as follows:
- R1@D3/2 <--> R2@D3/1
- R2@D3/3 <--> R3@D3/2
- R3@D3/4 <--> R4@D3/3
- R4@D3/1 <--> R1@D3/4
- R2@D3/4 <--> R4@D3/2

## Domain D4 (end for the end-to-end interdomain slice)

Domain D4 is composed of 3 emulated packet routers (Rx@D4) and 1 emulated DataCenter (DCGW@D4).
The DCGW@D4 is a termination endpoint for the end-to-end interdomain slice.
The internal domain connectivity is defined as follows:
- R1@D4/2 <--> R2@D4/1
- R1@D4/3 <--> R3@D4/1
- R2@D4/3 <--> R3@D4/2
- R3@D4/100 <--> DCGW@D4/eth1

## Inter-domain Connectivity

The 4 domains are interconnected among them by means of the following inter-domain links:
- R4@D1/10 <--> R1@D2/10
- R5@D1/10 <--> R1@D3/10
- R4@D2/10 <--> R2@D4/10
- R5@D2/10 <--> R2@D3/10
- R3@D3/10 <--> R1@D4/10
