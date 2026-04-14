# Tests for P4 functionality of TeraFlowSDN

This directory contains the necessary scripts and configurations to run tests for a simple port forwarding TFS program atop software-based P4 switches (using Mininet).

## Prerequisites

This test requires some custom monitoring services (latency monitoring and probe).
These services are implemented in Rust and can be found in the `./probe` directory.
To build these services on your target platform, follow the instructions in `./probe/probe-tfs/README.md`.

## Basic scripts

To run the experiments you should use the five scripts in the following order:

```shell
setup.sh
run_test_01_bootstrap.sh
run_test_02_create_service.sh
run_test_03_delete_service.sh
run_test_04_cleanup.sh
```

The `setup` script copies the necessary artefacts to the SBI service pod. It should be run just once, after a fresh install of TFS.
The `bootstrap` script registers the context, topology, links, and devices to TFS.
The `create` service script establishes a service between two endpoints.
The `delete` service script deletes the aforementioned service.
The `cleanup` script deletes all the objects (context, topology, links, and devices) from TFS.

## Objects file

The above bash scripts make use of the corresponding python scripts found under `./tests/` directory.
More important is the `./tests/Objects.py` file, which contains the definition of the Context, Topology, Devices, Links, Services. **This is the file that needs changes in case of a new topology.**

Check the `./tests/Objects.py` file before running the experiment to make sure that the switches' details are correct (ip address, port, etc.)

## Mininet topologies

In the `./mininet/` directory there are different mininet topology examples. The current `./tests/Objects.py` file corresponds to the `./mininet/8switch3path.py` topology. Additionally there is a backup file `./tests/topologies/6switchObjects.py` which corresponds to the `./mininet/6switch2path.py`.

## P4 artefacts

In the `./p4/` directory there are compiled p4 artefacts of the pipeline that will be pushed to the p4 switch, along with the p4-runtime definitions.
The `./setup.sh` script copies from this directory. So if you need to change p4 program, make sure to put the compiled artefacts there.

## Latency probe

In the `./probe/` directory there is a little program which calculates latency between two hosts in mininet and sends these measurements to the Monitoring component. For specific instructions, refer to the corresponding `./probe/README.md` file.
