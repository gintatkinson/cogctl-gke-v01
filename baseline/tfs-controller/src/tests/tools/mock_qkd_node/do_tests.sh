#!/bin/bash
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Build the new Docker image
echo "Building..."
docker build -t mock-qkd-node:test -f Dockerfile .
echo

# Run container
echo "Running..."
docker run -d --name qkd-node-01 -p 7777:7777 mock-qkd-node:test
echo

# Give 5 seconds for container to start
echo "Waiting 3 seconds..."
for i in {1..3}; do
    printf "%c" "."
    sleep 1
done
echo

# Dumping containers before...
echo "Dumping containers before..."
docker ps -a
echo

# Dumping logs before...
echo "Dumping logs before..."
docker logs qkd-node-01
echo

# Read data from startup
echo "Reading before..."
curl http://localhost:7777/restconf/data/etsi-qkd-sdn-node:
echo
echo

# Update data
echo "Updating 1..."
curl -X PATCH -d '{"qkd_node":{"qkdn_location_id":"new-loc"}}' http://localhost:7777/restconf/data/etsi-qkd-sdn-node:
echo

# Read data after 1 update
echo "Reading after 1..."
curl http://localhost:7777/restconf/data/etsi-qkd-sdn-node:
echo
echo

# Update data 2
echo "Updating 2..."
curl -X PATCH -d '{"qkdn_location_id":"new-loc-2"}' http://localhost:7777/restconf/data/etsi-qkd-sdn-node:qkd_node
echo

# Read data after 2 update
echo "Reading after 2..."
curl http://localhost:7777/restconf/data/etsi-qkd-sdn-node:
echo
echo

# Dumping containers after...
echo "Dumping containers after..."
docker ps -a
echo

# Dumping logs after...
echo "Dumping logs after..."
docker logs qkd-node-01
echo

# Destroy container
echo "Destroying..."
docker rm --force qkd-node-01
echo

echo "Bye!!"
