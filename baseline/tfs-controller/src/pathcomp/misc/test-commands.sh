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

docker build -t "pathcomp-frontend:latest" -f ./src/pathcomp/frontend/Dockerfile .
docker build -t "pathcomp-backend:builder" --target builder -f ./src/pathcomp/backend/Dockerfile .
docker build -t "pathcomp-backend:latest" -f ./src/pathcomp/backend/Dockerfile .
docker build -t "pathcomp-backend:gdb" -f ./src/pathcomp/backend/Dockerfile-gdb .

docker network create --driver=bridge --subnet=172.28.0.0/24 --gateway=172.28.0.254 tfbr

docker run --name pathcomp-frontend -d --network=tfbr --ip 172.28.0.1 pathcomp-frontend:latest
docker run --name pathcomp-backend  -d --network=tfbr --ip 172.28.0.2 pathcomp-backend:latest

docker rm -f pathcomp-frontend pathcomp-backend
docker network rm tfbr

docker image prune --force

docker exec -i pathcomp bash -c "pytest --log-level=INFO --verbose pathcomp/tests/test_unitary.py"

./scripts/run_tests_locally-pathcomp-frontend.sh
