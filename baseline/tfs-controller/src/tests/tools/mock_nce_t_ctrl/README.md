# RESTCONF-based NCE-T Controller

This server implements a basic RESTCONF Server that can load, potentially, any YANG data model.
In this case, it is prepared to load a NCE-T Controller based on:
- IETF Network Topology
- IETF YANG Data Model for Transport Network Client Signals
- IETF YANG Data Model for Traffic Engineering Tunnels, Label Switched Paths and Interfaces


## Build the RESTCONF-based NCE-T Controller Docker image
```bash
./build.sh
```

## Deploy the RESTCONF-based NCE-T Controller
```bash
./deploy.sh
```

## Destroy the RESTCONF-based NCE-T Controller
```bash
./destroy.sh
```
