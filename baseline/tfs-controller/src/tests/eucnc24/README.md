# DataPlane-in-a-Box - Control an Emulated DataPlane through TeraFlowSDN

## Emulated DataPlane Deployment
- ContainerLab
- Scenario
- Descriptor

## TeraFlowSDN Deployment
```bash
cd ~/tfs-ctrl
source ~/tfs-ctrl/src/tests/eucnc24/deploy_specs.sh
./deploy/all.sh
```

# ContainerLab - Arista cEOS - Commands

## Download and install ContainerLab
```bash
sudo bash -c "$(curl -sL https://get.containerlab.dev)" -- -v 0.59.0
```

## Download Arista cEOS image and create Docker image
```bash
cd ~/tfs-ctrl/src/tests/eucnc24/
docker import arista/cEOS64-lab-4.32.2F.tar ceos:4.32.2F
```

## Deploy scenario
```bash
cd ~/tfs-ctrl/src/tests/eucnc24/
sudo containerlab deploy --topo eucnc24.clab.yml
```

## Inspect scenario
```bash
cd ~/tfs-ctrl/src/tests/eucnc24/
sudo containerlab inspect --topo eucnc24.clab.yml
```

## Destroy scenario
```bash
cd ~/tfs-ctrl/src/tests/eucnc24/
sudo containerlab destroy --topo eucnc24.clab.yml
sudo rm -rf clab-eucnc24/ .eucnc24.clab.yml.bak
```

## Access cEOS Bash/CLI
```bash
docker exec -it clab-eucnc24-r1 bash
docker exec -it clab-eucnc24-r2 bash
docker exec -it clab-eucnc24-r3 bash
docker exec -it clab-eucnc24-r1 Cli
docker exec -it clab-eucnc24-r2 Cli
docker exec -it clab-eucnc24-r3 Cli
```

## Configure ContainerLab clients
```bash
docker exec -it clab-eucnc24-dc1 bash
    ip address add 172.16.1.10/24 dev eth1
    ip route add 172.16.2.0/24 via 172.16.1.1
    ping 172.16.2.10

docker exec -it clab-eucnc24-dc2 bash
    ip address add 172.16.2.10/24 dev eth1
    ip route add 172.16.1.0/24 via 172.16.2.1
    ping 172.16.1.10
```

## Install gNMIc
```bash
sudo bash -c "$(curl -sL https://get-gnmic.kmrd.dev)"
```

## gNMI Capabilities request
```bash
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure capabilities
```

## gNMI Get request
```bash
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path / > r1.json
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path /interfaces/interface > r1-ifaces.json
```

## gNMI Set request
```bash
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --update-path /system/config/hostname --update-value srl11
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path /system/config/hostname
```

## Subscribe request
```bash
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf subscribe --path /interfaces/interface[name=Management0]/state/

# In another terminal, you can generate traffic opening SSH connection
ssh admin@clab-eucnc24-r1
```

# Check configurations done:
```bash
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path '/network-instances' > r1-nis.json
gnmic --address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path '/interfaces' > r1-ifs.json
```

# Delete elements:
```bash
--address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --delete '/network-instances/network-instance[name=b19229e8]'
--address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --delete '/interfaces/interface[name=ethernet-1/1]/subinterfaces/subinterface[index=0]'
--address clab-eucnc24-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --delete '/interfaces/interface[name=ethernet-1/2]/subinterfaces/subinterface[index=0]'
```
