# DLT Gateway+Blockchain Performance Assessment Test

This test assesses the performance of the DLT component's Gateway + HyperLedger Fabric Blockchain.

To carry on that, it first creates a number of random devices, links, services, and slices.
Then, it performs some random creations, retrievals, updates, and deletes of random devices, links,
services, and slices.

For each operation and record type, the size of the entities in bytes, the number of endpoints,
constraints, config rules, subservices, and subslices is recorded.
Besides, it is recorded also the time to store/retrieve the records in the blockchain, and the delay
between the change and the reception of the asynchronous notification event.

## Scenario prepararion:
Create a docker virtual network:

```(bash)
docker network rm tfs-br
docker network create -d bridge --subnet=172.254.254.0/24 --gateway=172.254.254.1 --ip-range=172.254.254.0/24 tfs-br
```

Build the DLT Gateway component's Docker image:
```(bash)
docker build -t dlt-gateway:test -f ./src/dlt/gateway/Dockerfile .
```

Start the DLT Gateway component:
```(bash)
docker run --name dlt-gateway -d -p 50051:50051 --network=tfs-br dlt-gateway:test
```

Install possibly missing requirements:
```(bash)
pip install grpcio==1.47.0 grpcio-tools==1.47.0 protobuf==3.20.1
```

Start the performance assessment:
```(bash)
PYTHONPATH=./src python -m dlt.performance
```

The test produces a CSV file with the results per operation.
