# P4 Topology

This directory contains scripts for deploying a single software-based Stratum switch on a VM or bare metal machine.

## Prerequisites

The machine on which Stratum will be deployed must have at least 3 network interfaces as follows:

- a management interface for the switch to communicate with the control plane (i.e., TFS controller and INT collector)
- a west data plane interface towards a certain subnet (we call it edge subnet in this example)
- an est data plane interface towards another subnet (we call it corporate subnet in this example)

Also, due to Stratum's restrictions, the desired OS of the machine shall be `Ubuntu server 20.04 LTS`.

To build Stratum on this machine, follow the steps [here](https://github.com/stratum/stratum/blob/main/stratum/hal/bin/bmv2/README.md).
It is preferred to run Stratum as a binary.

## Steps to setup the environment and deploy the Stratum switch

We create a Linux namespace for Stratum to live in an isolated space from the rest of the system.
The two data plane interfaces of the VM need to be enclosed into this namespace, while for this namespace to interact with the outside world (i.e., root namespace and outside the VM), a dedicated virtual interface pair is created.

Follow the steps below to create the environment, deploy Stratum, and restore the VM to its previous state (cleanup).
Prior to this take a look at the environment configuration file, where one can change the names of the interfaces, according to your network setup.

```shell
nano p4-switch-conf-common.sh

HOST_IFACE_EXT="ens3"     # Interface towards TFS (management)
SW_IFACE_DATA_EDGE="ens4" # Interface towards the edge subnet (data plane)
SW_IFACE_DATA_CORP="ens5" # Interface towards the corporate subnet (data plane)

...
```

### Step 1: Setup environment

Edit the `setup` script to modify the subnets' information according to your network setup:

```shell
nano p4-switch-setup.sh

# Subnets managed by the switch
DOMAIN_EDGE_IP="10.158.72.0/24"  # Left-hand side subnet
DOMAIN_CORP_IP="172.16.10.0/24"  # Right-hand side subnet
```

Once your network setup is applied, run the `setup` script as follows:

```shell
sudo bash p4-switch-setup.sh
```

To verify that the switch namespace is in place, issue the following command:

```shell
sudo ip netns exec ns-switch ip a
```

The output should show 4 network interfaces, i.e., a `loopback` interface, 2 data planes interfaces (e.g., `ens4`, `ens5` in this example), and a virtual interface for sending telemetry data out of the switch (i.e., `veth-int-sw` in this example).
From this latter interface you can ping towards the other end of the virtual interface pair (i.e., `veth-int-host`):

```shell
sudo ip netns exec ns-switch ping 10.0.0.254
```

This ensures that telemetry data leaves the switch and ends up on the host VM.
To dispatch this telemetry data towards TFS, the `p4-switch-setup.sh` implements packet mirroring from `veth-int-host` to the VM's management interface (i.e., `ens3` in this example).
We assume that TFS is deployed on a machine that is accessible via the management interface (i.e., `ens3`) of this VM.

### Step 2: Deploy Stratum in the namespace

Now the namespace is ready to host the Stratum switch.

First you need to configure the chassis configuration file with the correct network interfaces names.
To do so, modify the `name` field changing `ens4`, `ens5`, and `ens3` to your desired interfaces.
These interface names must agree with the ones you added in `p4-switch-conf-common.sh`.

```shell
cat p4-switch-three-port-chassis-config-phy.pb.txt

# Copyright 2018-present Open Networking Foundation
# SPDX-License-Identifier: Apache-2.0

description: "Chassis configuration for a single Stratum bmv2 switch with 3 ports"
chassis {
  platform: PLT_P4_SOFT_SWITCH
  name: "bmv2-switch"
}
nodes {
  id: 1
  slot: 1
  index: 1
}
singleton_ports {
  id: 1
  name: "ens4"
  slot: 1
  port: 1
  channel: 1
  speed_bps: 100000000000
  config_params {
    admin_state: ADMIN_STATE_ENABLED
  }
  node: 1
}
singleton_ports {
  id: 2
  name: "ens5"
  slot: 1
  port: 2
  channel: 1
  speed_bps: 100000000000
  config_params {
    admin_state: ADMIN_STATE_ENABLED
  }
  node: 1
}
singleton_ports {
  id: 3
  name: "veth-int-sw"
  slot: 1
  port: 3
  channel: 1
  speed_bps: 100000000000
  config_params {
    admin_state: ADMIN_STATE_ENABLED
  }
  node: 1
}
```

To deploy Stratum, do:

```shell
sudo bash run-stratum.sh
```

To run Stratum will verbose logging, open the `run-stratum.sh` and change:

```shell
LOG_LEVEL="debug"
```

Then, re-deploy Stratum as shown above.

To verify that Stratum has been correctly deployed, you should see the following output:

```
<timestamp> config_monitoring_service.cc:94] Pushing the saved chassis config read from p4-switch-three-port-chassis-config-phy.pb.txt...
<timestamp> bmv2_chassis_manager.cc:519] Registered port status callbacks successfully for node 1.
<timestamp> bmv2_chassis_manager.cc:453] State of port 1 in node 1: UP.
<timestamp> bmv2_chassis_manager.cc:453] State of port 2 in node 1: UP.
<timestamp> bmv2_chassis_manager.cc:453] State of port 3 in node 1: UP.
<timestamp> bmv2_switch.cc:74] P4-based forwarding pipeline config pushed successfully to node with ID 1.
<timestamp> hal.cc:220] Stratum external facing services are listening to 0.0.0.0:50000, 0.0.0.0:50001, 0.0.0.0:50101...
```

### Step 3: Restore to the original setup

When your tests with Stratum and TFS are over, you may want to restore your setup.
To do so, execute the following script:

```shell
sudo bash p4-switch-tear-down.sh
```
