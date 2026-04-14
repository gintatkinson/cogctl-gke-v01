# QKD End-to-End Test

## Emulated QKD Nodes
See `src/tests/tools/mock_qkd_node`.
Here we deploy 3 emulated QKD Nodes initialized with configurations `data/qkd-node-XX.json`.

### (Re-)Deploy the 3 QKD Nodes
```bash
cd ~/tfs-ctrl
./src/tests/qkd_end2end/redeploy-qkd-nodes.sh
```

### Check their configuration
```bash
curl http://<mgmt-ip-addr>:<mgmt-port>/restconf/data/etsi-qkd-sdn-node:
```

### Update their configuration using root path
```bash
curl -X PATCH -d '{"qkd_node":{"qkdn_location_id":"new-loc"}}' http://<mgmt-ip-addr>:<mgmt-port>/restconf/data/etsi-qkd-sdn-node:
```

### Update their configuration using sub-entity path
```bash
curl -X PATCH -d '{"qkdn_location_id":"new-loc-2"}' http://<mgmt-ip-addr>:<mgmt-port>/restconf/data/etsi-qkd-sdn-node:qkd_node
```

### Destroy scenario
```bash
docker rm --force qkd-node-01 qkd-node-02 qkd-node-03
docker network rm --force qkd-node-br
```

## TeraFlowSDN Deployment
```bash
cd ~/tfs-ctrl
./src/tests/qkd_end2end/redeploy-tfs.sh
```

### QKD Node Topology
The topology descriptor for the QKD nodes is: `data/tfs-01-topology.json`

### Dump TFS component logs to files
```bash
cd ~/tfs-ctrl
./src/tests/qkd_end2end/dump_logs.sh
```
Will create files `<comp-name>.log`
