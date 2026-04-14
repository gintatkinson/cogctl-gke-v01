# Control of OpenFlow domain through Ryu SDN controller and TeraFlowSDN

## TeraFlowSDN Deployment
```bash
cd ~/tfs-ctrl
source ~/tfs-ctrl/src/tests/ryu-openflow/deploy_specs.sh
./deploy/all.sh
```

## Download and install Mininet
```bash
sudo apt-get install "mininet=2.3.0-1ubuntu1"
```

## Deploy SDN controller and dataplane
```bash
cd ~/tfs-ctrl/src/tests/ryu-openflow/
docker compose build # or docker buildx build --no-cache -t "ryu-image:dev" -f ./Ryu.Dockerfile .
docker compose up -d # or docker run -d -p 6653:6653 -p 8080:8080 ryu-image:dev
sudo python3 custom_pentagon_topology.py
```

## Destroy scenario
```bash
cd ~/tfs-ctrl/src/tests/ryu-openflow/
docker compose down
# Ctrl+C mininet dataplane
```

## Onboard scenario
- Through TFS WebUI

## Request connectivity service
```bash
cd ~/tfs-ctrl/src/tests/ryu-openflow/
curl -X POST \
  --header "Content-Type: application/json" \
  --data @ietf-l3vpn-service.json \
  --user "admin:admin" \
  http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services
```
