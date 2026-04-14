TeraFlow Traffic Engineering Service
====================================

This service is mean as an example of a Teraflow Service made in Erlang.

The Traffic Engineering service is tested on Ubuntu 20.04. Follow the instructions below to build, test, and run this service on your local environment.


## Build

First the TeraFlow protocol buffer code must have been generated:

    $ ../../proto/generate_code_erlang.sh

Then the TE service can be built:

    $ rebar3 compile


## Execute Unit Tests

    $ rebar3 eunit


## Run Service Console

First you need to crete a configuration file if not already done, and customize it if required:

	$ cp config/dev.config.template config/dev.config

Then you  can start the service in console mode:

    $ rebar3 shell


## Docker

### Build Image

The docker image must be built from the root of the Teraflow project:

    $ docker build -t te:dev -f src/te/Dockerfile .


### Run a shell from inside the container

    $ docker run -ti --rm --entrypoint sh te:dev


### Run Docker Container

    $ docker run -d --name te --init te:dev


### Open a Console to a Docker Container's Service

    $ docker exec -it te /tfte/bin/tfte remote_console


### Show Logs

    $ docker logs te


## Kubernetes

### Open a Console

    $ kubectl --namespace tfs exec -ti $(kubectl --namespace tfs get pods --selector=app=teservice -o name) -c server -- /tfte/bin/tfte remote_console


### Show Logs

    $ kubectl --namespace tfs logs $(kubectl --namespace tfs get pods --selector=app=teservice -o name) -c server


## Teraflow

To build and deploy the TE service as part of Teraflow, the following line must be added or uncomented in your `my_deploy.sh`:

    export TFS_COMPONENTS="${TFS_COMPONENTS} te"
