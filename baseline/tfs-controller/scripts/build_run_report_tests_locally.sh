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

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "component name required but not provided"

COMPONENT_NAME=$1 # parameter
IMAGE_NAME="${COMPONENT_NAME}-local"
IMAGE_TAG="latest"

if docker ps | grep $IMAGE_NAME
then
    docker stop $IMAGE_NAME
fi

if docker network list | grep teraflowbridge
then
    echo "teraflowbridge is already created"
else
    docker network create -d bridge teraflowbridge
fi

docker build -t "$IMAGE_NAME:$IMAGE_TAG" -f ./src/$COMPONENT_NAME/Dockerfile .

docker run --name $IMAGE_NAME -d -v "${PWD}/src/${COMPONENT_NAME}/tests:/home/${COMPONENT_NAME}/results" --network=teraflowbridge --rm $IMAGE_NAME:$IMAGE_TAG

docker exec -i $IMAGE_NAME bash -c "coverage run -m pytest --log-level=INFO --verbose $COMPONENT_NAME/tests/ --junitxml=/home/${COMPONENT_NAME}/results/${COMPONENT_NAME}_report.xml"

PROJECTDIR=`pwd`

cd $PROJECTDIR/src
RCFILE=$PROJECTDIR/coverage/.coveragerc

echo
echo "Coverage report:"
echo "----------------"
docker exec -i $IMAGE_NAME bash -c "coverage report --include='${COMPONENT_NAME}/*' --show-missing"

# docker stop $IMAGE_NAME
docker rm -f $IMAGE_NAME
docker network rm teraflowbridge
