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


docker ps -aq | xargs -r docker rm -f
docker network rm teraflowbridge || true
docker container prune -f

docker pull "bitnamilegacy/kafka:latest"
docker buildx build -t "mock_tfs_nbi_dependencies:test" -f ./src/tests/tools/mock_tfs_nbi_dependencies/Dockerfile .
docker buildx build -t "nbi:latest" -f ./src/nbi/Dockerfile .
docker image prune --force

docker network create -d bridge teraflowbridge

docker run --name kafka -d --network=teraflowbridge -p 9092:9092 -p 9093:9093 \
    --env KAFKA_CFG_NODE_ID=1 \
    --env KAFKA_CFG_PROCESS_ROLES=controller,broker \
    --env KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
    --env KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT \
    --env KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    --env KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@kafka:9093 \
    bitnamilegacy/kafka:latest

echo "Waiting for Kafka to be ready..."
while ! docker logs kafka 2>&1 | grep -q 'Kafka Server started'; do
    printf "."
    sleep 1;
done
printf "\n"
sleep 5 # Give extra time to Kafka to get stabilized

docker inspect kafka --format "{{.NetworkSettings.Networks}}"
KAFKA_IP=$(docker inspect kafka --format "{{.NetworkSettings.Networks.teraflowbridge.IPAddress}}")
echo "Kafka IP: $KAFKA_IP"

docker run --name mock_tfs_nbi_dependencies -d -p 10000:10000 \
    --network=teraflowbridge --env BIND_ADDRESS=0.0.0.0 --env BIND_PORT=10000 \
    --env LOG_LEVEL=INFO \
    mock_tfs_nbi_dependencies:test

docker run --name nbi -d \
    --network=teraflowbridge \
    --env LOG_LEVEL=INFO \
    --env FLASK_ENV=development \
    --env IETF_NETWORK_RENDERER=LIBYANG \
    --env "KFK_SERVER_ADDRESS=${KAFKA_IP}:9092" \
    nbi:latest

# Wait until any worker logs "Initialization completed" (from the start of logs)
# -m1 makes grep exit as soon as the line appears.
# With set -o pipefail, docker logs will get SIGPIPE when grep exits;
#   `|| true` neutralizes that so the pipeline’s status reflects grep’s success.
(docker logs -f $IMAGE_NAME || true) 2>&1 | grep -m1 -Fi 'Initialization completed'

printf "\n"
sleep 5 # Give extra time to NBI to get ready

docker ps -a
#docker logs kafka
docker logs mock_tfs_nbi_dependencies
docker logs nbi

# helpful pytest flags: --log-level=INFO -o log_cli=true --verbose --maxfail=1 --durations=0
docker exec -i nbi bash -c "coverage run --append -m pytest --log-level=INFO --verbose nbi/tests/test_core.py --junitxml=/opt/results/nbi_report_core.xml"
docker exec -i nbi bash -c "coverage run --append -m pytest --log-level=INFO --verbose nbi/tests/test_tfs_api.py --junitxml=/opt/results/nbi_report_tfs_api.xml"
docker exec -i nbi bash -c "coverage run --append -m pytest --log-level=INFO --verbose nbi/tests/test_ietf_l2vpn.py --junitxml=/opt/results/nbi_report_ietf_l2vpn.xml"
docker exec -i nbi bash -c "coverage run --append -m pytest --log-level=INFO --verbose nbi/tests/test_ietf_network.py --junitxml=/opt/results/nbi_report_ietf_network.xml"
docker exec -i nbi bash -c "coverage run --append -m pytest --log-level=INFO --verbose nbi/tests/test_ietf_l3vpn.py --junitxml=/opt/results/nbi_report_ietf_l3vpn.xml"
docker exec -i nbi bash -c "coverage run --append -m pytest --log-level=INFO --verbose nbi/tests/test_etsi_bwm.py --junitxml=/opt/results/nbi_report_etsi_bwm.xml"
docker exec -i nbi bash -c "coverage run --append -m pytest --log-level=INFO --verbose nbi/tests/test_camara_qod.py --junitxml=/opt/results/nbi_report_camara_qod.xml"
docker exec -i nbi bash -c "coverage report --include='nbi/*' --show-missing"

#docker logs mock_tfs_nbi_dependencies
docker logs nbi
#docker logs kafka
docker rm -f nbi
docker rm -f mock_tfs_nbi_dependencies
docker rm -f kafka
docker network rm teraflowbridge

echo "Bye!"
