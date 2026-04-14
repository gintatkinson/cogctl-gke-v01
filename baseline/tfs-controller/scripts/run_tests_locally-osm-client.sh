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


# Pre-build Cleanup
docker ps --all --quiet | xargs --no-run-if-empty docker stop
docker container prune --force
docker ps --all --quiet | xargs --no-run-if-empty docker rm --force
docker image prune --force
docker network prune --force
docker volume prune --all --force
#docker buildx prune --force

# Build Docker images
docker buildx build -t "mock-osm-nbi:test" -f ./src/tests/tools/mock_osm_nbi/Dockerfile ./src/tests/tools/mock_osm_nbi
docker buildx build -t "osm_client:latest" -f ./src/osm_client/Dockerfile .

# Post-build Cleanup
docker image prune --force


# Deploy Mock OSM NBI and OSM Client
docker network create --driver bridge --subnet=172.254.251.0/24 --gateway=172.254.251.254 mock-osm-nbi-br

docker run --detach --name mock_osm_nbi --network=mock-osm-nbi-br --ip 172.254.251.10 --publish 80 --publish 443 \
  --env LOG_LEVEL=DEBUG --env FLASK_ENV=development \
  mock-osm-nbi:test

docker run --detach --name osm_client --network=mock-osm-nbi-br --ip 172.254.251.11 \
  --env LOG_LEVEL=DEBUG --env FLASK_ENV=development \
  --env OSM_ADDRESS=172.254.251.10 --env OSM_PORT=443 \
  osm_client:latest


# Post-deploy status
docker ps -a

while ! docker logs osm_client 2>&1 | grep -q 'Running...'; do sleep 1; done
docker logs osm_client
docker logs mock_osm_nbi


# Execute tests
docker exec -i osm_client bash -c "coverage run -m pytest --log-level=INFO --verbose osm_client/tests/test_unitary.py"
docker exec -i osm_client bash -c "coverage report --include='osm_client/*' --show-missing"


# Post-tests logs
docker logs osm_client
docker logs mock_osm_nbi


# Post-tests cleanup
docker ps --all --quiet | xargs --no-run-if-empty docker stop
docker container prune --force
docker ps --all --quiet | xargs --no-run-if-empty docker rm --force
docker image prune --force
docker network prune --force
docker volume prune --all --force
docker buildx prune --force

echo "Bye!"
