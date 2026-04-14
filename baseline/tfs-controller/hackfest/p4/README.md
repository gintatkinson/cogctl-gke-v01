# Network X 22 Demo - P4 driver, Basic connectivity functionality

This functional test shows the P4 driver with a basic connectivity test between 2 hosts connected to a single P4 switch, using the TeraFlow Cloud-native SDN Controller.

## Functional test folder

This functional test can be found in folder `hackfest/p4`

## P4 source and Mininet topology

This test is designed to operate with a mininet deployment that contains 2 hosts and a BMv2 switch, such a topology can be found in the 'hackfest/p4/mininet' folder.
Additionally the P4 source code, along with its compiled artifacts are present in the 'hackfest/p4/p4' folder.

## Deployment and Dependencies

To run this functional test, it is assumed you have deployed a MicroK8s-based Kubernetes environment and a TeraFlowSDN
controller instance as described in the [Tutorial: Deployment Guide](./1-0-deployment.md), and you configured the Python
environment as described in
[Tutorial: Run Experiments Guide > 2.1. Configure Python Environment](./2-1-python-environment.md).
Remember to source the scenario settings appropriately, e.g., `cd ~/tfs-ctrl && source my_deploy.sh` in each terminal
you open.

Additionally mininet with a p4 switch (bmv2 for example) should be installed, we suggest using the mininet packaged in the [Next-Gen SDN Tutorial][https://github.com/opennetworkinglab/ngsdn-tutorial], as it provides an easy way to deploy mininet dockerized and comes with the BMv2Stratum software switch. 

### Next-Gen SDN Tutorial installation

To install the recommended mininet from the Next-Gen SDN Tutorial follow these steps:

First of all you should have the following dependencies installed:

- Docker v1.13.0+ (with docker-compose)
- make
- Python 3

Then clone the repo
```
cd ~
git clone -b advanced https://github.com/opennetworkinglab/ngsdn-tutorial
```

After the repo is downloaded do the following to download the required docker images
```
cd ~/ngsdn-tutorial
make deps
```

Add the following make rule to the ~/ngsdn-tutorial/Makefile
```
start-simple: NGSDN_TOPO_PY := topo-simple.py
start-simple: _start
```

And copy the topology file from ~/tfs-ctrl/hackfest/p4/mininet/topo-simple.py to the ~/ngsdn-tutorial/mininet/ directory.

## Test Execution

### Mininet 
To execute this functional test, first start mininet:
```
make start-simple
make mn-cli
```

You will be prompted with the mininet cli. Run the following and let it run until the end of the experiment
```
client ping server
```

### Teraflow

In another terminal cd to the teraflow directory and run the following
```
hackfest/p4/setup.sh
```
This will copy the p4 artifacts to the device pod.

Then you can bootstrap the device to the Teraflow Controller
```
hackfest/p4/run_test_01_bootstrap.sh
```

Install the required rules to the p4 switch
```
hackfest/p4/run_test_02_create_service.sh
```
You should now check the mininet terminal. The two hosts should be pinging each other as intended.

You can remove the rules from the p4 switch
```
hackfest/p4/run_test_03_delete_service.sh
```
The two hosts on the mininet terminal, should stop pinging.

And remove the device from the Teraflow Controller
```
hackfest/p4/run_test_04_cleanup.sh
```
