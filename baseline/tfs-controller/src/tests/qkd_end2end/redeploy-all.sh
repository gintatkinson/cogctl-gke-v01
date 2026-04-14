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


# Cleanup
docker rm --force qkd-node-01 qkd-node-02 qkd-node-03
docker network rm --force qkd-node-br

# Create Docker network
docker network create --driver bridge --subnet=172.254.250.0/24 --gateway=172.254.250.254 qkd-node-br

# Create QKD Nodes
docker run --detach --name qkd-node-01 --network qkd-node-br --ip 172.254.250.101 --publish 8080 \
    --volume "$PWD/src/tests/qkd_end2end/data/qkd-node-01.json:/var/mock_qkd_node/startup.json" \
    mock-qkd-node:test
docker run --detach --name qkd-node-02 --network qkd-node-br --ip 172.254.250.102 --publish 8080 \
    --volume "$PWD/src/tests/qkd_end2end/data/qkd-node-02.json:/var/mock_qkd_node/startup.json" \
    mock-qkd-node:test
docker run --detach --name qkd-node-03 --network qkd-node-br --ip 172.254.250.103 --publish 8080 \
    --volume "$PWD/src/tests/qkd_end2end/data/qkd-node-03.json:/var/mock_qkd_node/startup.json" \
    mock-qkd-node:test

# Dump QKD Node Docker containers
docker ps -a
echo

# Wait till MicroK8s is stabilized...
microk8s status --wait-ready
echo

source ~/tfs-ctrl/src/tests/qkd_end2end/deploy_specs.sh
./deploy/all.sh

echo "Bye!"
