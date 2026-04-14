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


echo "Building SIMAP Server..."
cd ~/tfs-ctrl/
docker buildx build -t simap-server:mock -f ./src/tests/tools/simap_server/Dockerfile .

echo "Building NCE-T Controller..."
cd ~/tfs-ctrl/
docker buildx build -t nce-t-ctrl:mock -f ./src/tests/tools/mock_nce_t_ctrl/Dockerfile .

echo "Cleaning up..."
docker rm --force simap-server
docker rm --force nce-t-ctrl

echo "Deploying support services..."
docker run --detach --name simap-server --publish 8080:8080 simap-server:mock
docker run --detach --name nce-t-ctrl --publish 8081:8080 --env SIMAP_ADDRESS=172.17.0.1 --env SIMAP_PORT=8080 nce-t-ctrl:mock

sleep 2
docker ps -a

echo "Bye!"
