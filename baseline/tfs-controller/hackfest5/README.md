# Hackfest 5 - Control an Emulated DataPlane through TeraFlowSDN


## Prepare your VM
```bash
cd ~/tfs-ctrl
git checkout feat/hackfest5
git pull
```



## ContainerLab Commands

### Download and install ContainerLab
```bash
sudo bash -c "$(curl -sL https://get.containerlab.dev)" -- -v 0.59.0
```

### Check available images in Docker
```bash
docker images | grep -E "ceos|multitool"
```

### Download hackfest5 cEOS image and create Docker image [already done]
- Note: Image to be downloaded for free from [Arista](https://www.arista.com/en/login) website.
```bash
docker import ~/tfs-ctrl/hackfest5/images/arista/cEOS64-lab-4.31.5M.tar ceos:4.31.5M
docker import ~/tfs-ctrl/hackfest5/images/arista/cEOS64-lab-4.32.2F.tar ceos:4.32.2F
```

### Deploy scenario
```bash
~/tfs-ctrl/hackfest5/clab-deploy.sh
```

### Inspect scenario
```bash
~/tfs-ctrl/hackfest5/clab-inspect.sh
```

### Show scenario's topology
```bash
~/tfs-ctrl/hackfest5/clab-graph.sh
```

### Destroy scenario
```bash
~/tfs-ctrl/hackfest5/clab-destroy.sh
```

### Access cEOS CLI
```bash
~/tfs-ctrl/hackfest5/clab-cli-r1.sh
```

### Access DC CLI
```bash
~/tfs-ctrl/hackfest5/clab-cli-dc1.sh
```

### Start pinging remote DC
```bash
~/tfs-ctrl/hackfest5/clab-cli-dc1.sh
    ping 192.168.2.10
```



## TeraFlowSDN Commands

### Check status of MicroK8s
```bash
microk8s.status --wait-ready
```

### Start MicroK8s
```bash
microk8s.start
```

### Periodically report status of MicroK8s every second
```bash
watch -n 1 microk8s.status --wait-ready
```

### Periodically report status of workload in MicroK8s every second
```bash
watch -n 1 kubectl get all --all-namespaces
```

### Re-Deploy TeraFlowSDN
```bash
~/tfs-ctrl/hackfest5/redeploy-tfs.sh
```

### Show TeraFlowSDN Deployment status
```bash
source ~/tfs-ctrl/hackfest5/deploy_specs.sh
./deploy/show.sh
```

### Show log of a TeraFlowSDN component
```bash
source ~/tfs-ctrl/hackfest5/deploy_specs.sh
~/tfs-ctrl/scripts/show_logs_device.sh
```



## L3VPN Commands

### Create a new IETF L3VPN through TeraFlowSDN NBI
```bash
cd ~/tfs-ctrl/hackfest5/data
curl -X POST \
    --header "Content-Type: application/json" \
    --data @ietf-l3vpn-service.json \
    --user "admin:admin" \
    http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services
```

### Get UUID of a IETF L3VPN through TeraFlowSDN NBI
```bash
curl --user "admin:admin" \
    http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service=ietf-l3vpn-svc/
```

### Delete a IETF L3VPN through TeraFlowSDN NBI
```bash
curl -X DELETE --user "admin:admin" \
    http://127.0.0.1/restconf/data/ietf-l3vpn-svc:l3vpn-svc/vpn-services/vpn-service=ietf-l3vpn-svc/
```

### Start pinging remote DC
```bash
~/tfs-ctrl/hackfest5/clab-cli-dc1.sh
    ping 192.168.2.10
```




## gNMIc Commands

### Install gNMIc
```bash
sudo bash -c "$(curl -sL https://get-gnmic.kmrd.dev)"
```

### gNMI Capabilities request
```bash
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure capabilities
```

### gNMI Get request
```bash
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path / > r1.json
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path /interfaces/interface > r1-ifaces.json
```

### gNMI Set request
```bash
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --update-path /system/config/hostname --update-value "my-r1"
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path /system/config/hostname
```

### Subscribe request
```bash
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf subscribe --path /interfaces/interface[name=Management0]/state/

# In another terminal, you can generate traffic opening SSH connection
ssh admin@clab-hackfest5-r1
```

### Check configurations done:
```bash
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path '/network-instances' > r1-nis.json
gnmic --address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf get --path '/interfaces' > r1-ifs.json
```

### Delete elements:
```bash
--address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --delete '/network-instances/network-instance[name=b19229e8]'
--address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --delete '/interfaces/interface[name=ethernet-1/1]/subinterfaces/subinterface[index=0]'
--address clab-hackfest5-r1 --port 6030 --username admin --password admin --insecure --encoding json_ietf set --delete '/interfaces/interface[name=ethernet-1/2]/subinterfaces/subinterface[index=0]'
```
