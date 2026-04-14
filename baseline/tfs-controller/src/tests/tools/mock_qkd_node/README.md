# Mock QKD Node

This Mock implements very basic support for the software-defined QKD node information models specified in ETSI GS QKD 015 V2.1.1.

The aim of this mock is to enable testing the TFS QKD Framework with an emulated data plane.


## Build the Mock QKD Node Docker image
```bash
./build.sh
```

## Run the Mock QKD Node as a container:
```bash
docker network create --driver bridge --subnet=172.254.252.0/24 --gateway=172.254.252.254 tfs-qkd-net-mgmt

docker run --name qkd-node-01 --detach --publish 80:80 \
  --network=tfs-qkd-net-mgmt --ip=172.254.252.101 \
  --env "DATA_FILE_PATH=/var/teraflow/mock-qkd-node/data/database.json" \
  --volume "$PWD/src/tests/mock-qkd-node/data/database-01.json:/var/teraflow/mock-qkd-node/data/database.json" \
  mock-qkd-node:test

docker run --name qkd-node-02 --detach --publish 80:80 \
  --network=tfs-qkd-net-mgmt --ip=172.254.252.102 \
  --env "DATA_FILE_PATH=/var/teraflow/mock-qkd-node/data/database.json" \
  --volume "$PWD/src/tests/mock-qkd-node/data/database-02.json:/var/teraflow/mock-qkd-node/data/database.json" \
  mock-qkd-node:test

docker run --name qkd-node-03 --detach --publish 80:80 \
  --network=tfs-qkd-net-mgmt --ip=172.254.252.103 \
  --env "DATA_FILE_PATH=/var/teraflow/mock-qkd-node/data/database.json" \
  --volume "$PWD/src/tests/mock-qkd-node/data/database-03.json:/var/teraflow/mock-qkd-node/data/database.json" \
  mock-qkd-node:test
```
