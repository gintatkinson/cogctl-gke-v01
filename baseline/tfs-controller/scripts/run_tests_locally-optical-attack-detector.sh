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


PROJECTDIR=`pwd`
RCFILE=$PROJECTDIR/coverage/.coveragerc
COVERAGEFILE=$PROJECTDIR/coverage/.coverage

# Destroy old coverage file and configure the correct folder on the .coveragerc file
rm -f $COVERAGEFILE
cat $PROJECTDIR/coverage/.coveragerc.template | sed s+~/tfs-ctrl+$PROJECTDIR+g > $RCFILE

echo
echo "Pre-test clean-up:"
echo "------------------"
docker rm -f redis opticalattackdetector dbscanserving
docker network rm tfs_br

echo
echo "Pull Docker images:"
echo "-------------------"
docker pull redis:7.0-alpine

echo
echo "Build optical attack detector:"
echo "------------------------------"
docker build -t "opticalattackdetector:latest" -f ./src/opticalattackdetector/Dockerfile .
docker image prune --force

echo
echo "Build dbscan serving:"
echo "---------------------"
docker build -t "dbscanserving:latest" -f ./src/dbscanserving/Dockerfile .
docker image prune --force

echo
echo "Create test environment:"
echo "------------------------"
export REDIS_PASSWORD=$(uuidgen)
docker network create -d bridge --subnet=172.254.254.0/24 --gateway=172.254.254.1 --ip-range=172.254.254.0/24 tfs_br

docker run --name redis -d --network=tfs_br -p 16379:6379 --rm \
    --env REDIS_PASSWORD=${REDIS_PASSWORD} \
    redis:7.0-alpine redis-server --requirepass ${REDIS_PASSWORD}

docker run --name dbscanserving -d --network=tfs_br -p 10008:10008 --rm \
    --env LOG_LEVEL=DEBUG \
    dbscanserving:latest "python -m dbscanserving.service"

echo
echo "Waiting for initialization..."
echo "-----------------------------"
while ! docker logs redis 2>&1 | grep -q 'Ready to accept connections'; do sleep 1; done
docker logs redis
#while ! docker logs dbscanserving 2>&1 | grep -q 'Server is ready'; do sleep 1; done
docker logs dbscanserving
#sleep 10
docker ps -a

echo
echo "Run unitary tests and analyze code coverage:"
echo "--------------------------------------------"
export REDIS_ADDRESS=$(docker inspect redis --format "{{.NetworkSettings.Networks.tfs_br.IPAddress}}")
export DBSCANSERVING_ADDRESS=$(docker inspect dbscanserving --format "{{.NetworkSettings.Networks.tfs_br.IPAddress}}")
docker run --name opticalattackdetector -d --network=tfs_br -p 10006:10006 --rm \
    --env REDIS_PASSWORD=${REDIS_PASSWORD} \
    --env DBSCANSERVINGSERVICE_SERVICE_HOST=${DBSCANSERVING_ADDRESS} \
    --env CACHINGSERVICE_SERVICE_HOST=${REDIS_ADDRESS} \
    opticalattackdetector:latest

sleep 5
docker ps -a
docker logs opticalattackdetector
docker exec -i opticalattackdetector bash -c "coverage run -m pytest --log-level=DEBUG --verbose opticalattackdetector/tests/test_unitary.py"
docker logs redis
docker logs dbscanserving
docker logs opticalattackdetector

echo
echo "Coverage report:"
echo "----------------"
docker exec -i opticalattackdetector bash -c "coverage report --include='opticalattackdetector/*' --sort cover --show-missing --skip-covered"

echo
echo "Post-test clean-up:"
echo "-------------------"
docker rm -f redis opticalattackdetector dbscanserving
docker network rm tfs_br

echo "Done!"
