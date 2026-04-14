# Tests for P4 functionality of TeraFlowSDN

This directory contains the necessary scripts and configurations to run tests for the P4 functionality of TFS.

## Basic scripts

To run the experiments you should use the five scripts in the following order:
```
setup.sh
run_test_01_bootstrap.sh
run_test_02_create_service.sh
run_test_03_delete_service.sh
run_test_04_cleanup.sh
```

The setup script copies the necessary artifacts to the SBI service pod. It should be run just once, after a fresh install of TFS.
The bootstrap script registers the context, topology, links and, devices to TFS.
The create service scripts establishes a service between two endpoints.
The delete service script delete the aforementioned service.
Cleanup script deletes all the objects (context, topology, links, devices) from TFS.

## Objects file

The above bash scripts make use of the corresponding python scripts found under `./tests/` directory.
More important is the `./tests/Objects.py` file, which contains the definition of the Context, Topology, Devices, Links, Services. **This is the file that need changes in case of a new topology.**

Check the `./tests/Objects.py` file before running the experiment to make sure that the switches details are correct (ip address, port, etc.)

## Mininet topologies

In the `./mininet/` directory there are different mininet topology examples. The current `./tests/Objects.py` file corresponds to the `./mininet/4switch2path.py` topology. For more topologies please refer to `../p4`.

## P4 artifacts

In the `./p4/` directory there are the compiled p4 artifacts that contain the pipeline that will be pushed to the p4 switch, along with the p4-runtime definitions. 
The `./setup.sh` script copies from this directory. So if you need to change p4 program, make sure to put the compiled artifacts here.

## Latency probe

In the `./probe/` directory there is a little program which calculates latency between two hosts in mininet and sends them to the Monitoring component. For specific instructions, refer to the corresponding `./probe/README.md` file.

