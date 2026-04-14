# RESTCONF/SIMAP Server

This server implements a basic RESTCONF Server that can load, potentially, any YANG data model.
In this case, it is prepared to load a SIMAP Server based on IETF Network Topology + custom SIMAP Telemetry extensions.


## Build the RESTCONF/SIMAP Server Docker image
```bash
./build.sh
```

## Deploy the RESTCONF/SIMAP Server
```bash
./deploy.sh
```

## Run the RESTCONF/SIMAP Client for testing:
```bash
./run_client.sh
```

## Destroy the RESTCONF/SIMAP Server
```bash
./destroy.sh
```
