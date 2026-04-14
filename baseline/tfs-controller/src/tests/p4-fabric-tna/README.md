# Tests for P4 routing, ACL, and In-Band Network Telemetry functions

This directory contains the necessary scripts and configurations to run tests atop a Stratum-based P4 whitebox that performs a set of network functions, including forwarding (L2), routing (L3), L3/L4 access control list (ACL), and In-Band Network Telemetry (INT).
The P4 data plane is based on ONF's SD-Fabric implementation, titled [fabric-tna](https://github.com/stratum/fabric-tna)

## Prerequisites

You need Python3, which should already be installed while preparing for a TFS build.
Additionally, `pytest` is also mandatory as it is used by our tests below.
Aliasing python with python3 will also help bridging issues between older and newer python versions.

```shell
alias python='python3'
pip3 install pytest
pip3 install grpclib protobuf
pip3 install grpcio-tools
```

The versions used for this test are:

- `protobuf` 3.20.3
- `grpclib` 0.4.4
- `grpcio` 1.47.5
- `grpcio-tools` 1.47.5

After the installation of `grpclib`, protoc-gen-grpclib_python binary is in /home/$USER/.local/bin/
First we copy it to /usr/local/bin/:

```shell
  sudo cp /home/$USER/.local/bin/protoc-gen-grpclib_python /usr/local/bin/
```

Then, we include this path to the PYTHONPATH:

```shell
export PYTHONPATH="${PYTHONPATH}:/usr/local/bin/protoc-gen-grpclib_python"
```

You need to build and deploy a software-based Stratum switch, before being able to use TFS to control it.
To do so, follow the instructions in the `./topology` folder.

## Steps to setup and run a TFS program atop Stratum

To conduct this test, follow the steps below.

### Deploy TFS

```shell
cd ~/tfs-ctrl/
source my_deploy.sh && source tfs_runtime_env_vars.sh
./deploy/all.sh
```

### Path setup

Ensure that `PATH` variable contains the parent project directory, e.g., "home/$USER/tfs-ctrl".

Ensure that `PYTHONPATH` variable contains the source code directory of TFS, e.g., "home/$USER/tfs-ctrl/src"

## Topology setup

In the `./topology/` directory there are scripts that allow to build Stratum on a target machine (e.g., a VM) and then deploy a P4 switch atop this machine.
This test assumes a Stratum P4 switch with 2 network interfaces used as a data plane (routing traffic from one to another) as well as another network interface used to send telemetry information to an external telemetry collector.

## P4 artifacts

In the `./p4src/` directory there are compiled P4 artifacts of the pipeline that will be pushed to the P4 switch, along with the P4-runtime definitions.
The `./setup.sh` script copies from this directory. If you need to change the P4 program, make sure to put the compiled artifacts there.

## Tests

A set of tests is implemented, each focusing on different aspects of TFS.
For each of these tests, an auxiliary bash script allows to run it with less typing.

|              Bash Runner                      |                Purpose                                                      |
| --------------------------------------------- | --------------------------------------------------------------------------- |
| setup.sh                                      | Copy P4 artifacts into the SBI pod                                          |
| run_test_01_bootstrap.sh                      | Connect TFS to the P4 switch                                                |
| run_test_02a_sbi_provision_int_l2_l3_acl.sh   | Install L2, L3, INT, and ACL rules on the P4 switch via the SBI service     |
| run_test_02b_sbi_deprovision_int_l2_l3_acl.sh | Uninstall L2, L3, INT, and ACL rules from the P4 switch via the SBI service |
| run_test_03a_service_provision_l2.sh          | Install L2 forwarding rules via a dedicated P4 L2 service handler           |
| run_test_03b_service_deprovision_l2.sh        | Uninstall L2 forwarding rules via a dedicated P4 L2 service handler         |
| run_test_04a_service_provision_l3.sh          | Install L3 routing rules via a dedicated P4 L3 service handler              |
| run_test_04b_service_deprovision_l3.sh        | Uninstall L3 routing rules via a dedicated P4 L3 service handler            |
| run_test_05a_service_provision_acl.sh         | Install ACL rules via a dedicated P4 ACL service handler                    |
| run_test_05b_service_deprovision_acl.sh       | Uninstall ACL rules via a dedicated P4 ACL service handler                  |
| run_test_06a_service_provision_int.sh         | Install INT rules via a dedicated P4 INT service handler                    |
| run_test_06b_service_deprovision_int.sh       | Uninstall INT rules via a dedicated P4 INT service handler                  |
| run_test_07_cleanup.sh                        | Clean-up context and topology and disconnect TFS from the P4 switch         |

Each of the tests above is described in detail below.

### Step 0: Copy the necessary P4 artifacts into the TFS SBI service pod

The setup script copies the necessary artifacts to the SBI service pod.
It should be run just once, after a fresh install of TFS.
If you `deploy/all.sh` again, you need to repeat this step.

```shell
cd ~/tfs-ctrl/
source my_deploy.sh && source tfs_runtime_env_vars.sh
bash src/tests/p4-fabric-tna/setup.sh
```

### Step 1: Bootstrap topology

The bootstrap script registers the context, topology, links, and devices to TFS.

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_01_bootstrap.sh
```

### Step 2: Manage L2, L3, ACL, and INT via the SBI API (rules)

Implement forwarding, routing, ACL, and INT network functions by installing P4 rules to the Stratum switch via the TFS SBI API.
In this test, these rules are installed in batches, as the switch cannot digest all these rules at once.

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_02a_sbi_provision_int_l2_l3_acl.sh
```

Deprovision forwarding, routing, ACL, and INT network functions by removing the previously installed P4 rules (via the TFS SBI API) from the Stratum switch.

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_02b_sbi_deprovision_int_l2_l3_acl.sh
```

### Step 3: Manage L2, L3, ACL, and INT via the Service API

To avoid interacting with the switch using low-level P4 rules (via the SBI), we created modular network services, which allow users to easily provision L2, L3, ACL, and INT network functions.
These services require users to define the service endpoints as well as some high-level service configuration, while leaving the rest of complexity to tailored service handlers that interact with the SBI on behalf of the user.

#### Provision L2 network service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_03a_service_provision_l2.sh
```

#### Deprovision L2 network service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_03b_service_deprovision_l2.sh
```

#### Provision L3 network service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_04a_service_provision_l3.sh
```

#### Deprovision L3 network service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_04b_service_deprovision_l3.sh
```

#### Provision ACL network service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_05a_service_provision_acl.sh
```

#### Deprovision ACL network service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_05b_service_deprovision_acl.sh
```

#### Provision INT service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_06a_service_provision_int.sh
```

#### Deprovision INT service via the Service API

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_06b_service_deprovision_int.sh
```

### Step 4: Deprovision topology

Delete all the objects (context, topology, links, devices) from TFS:

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_07_cleanup.sh
```

Alternatively, a purge test is implemented; this test removes services, links, devices, topology, and context in this order.

```shell
cd ~/tfs-ctrl/
bash src/tests/p4-fabric-tna/run_test_08_purge.sh
```
