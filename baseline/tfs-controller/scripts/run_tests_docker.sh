#!/bin/bash
# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


########################################################################################################################
# Define your deployment settings here
########################################################################################################################

# Set the URL of your local Docker registry where the images will be uploaded to. Leave it blank if you do not want to
# use any Docker registry.
REGISTRY_IMAGE=""
#REGISTRY_IMAGE="http://my-container-registry.local/"

# Set the list of components you want to build images for, and deploy.
COMPONENTS="context device ztp policy service nbi monitoring centralizedattackdetector"

# Set the tag you want to use for your images.
IMAGE_TAG="tf-dev"

# Constants
TMP_FOLDER="./tmp"

TMP_LOGS_FOLDER="$TMP_FOLDER/logs"
mkdir -p $TMP_LOGS_FOLDER

DOCKER_BUILD="docker build"
DOCKER_MAJOR_VERSION=$(docker --version | grep -o -E "Docker version [0-9]+\." | grep -o -E "[0-9]+" | cut -c 1-3)
if [[ $DOCKER_MAJOR_VERSION -ge 23 ]]; then
    # If Docker version >= 23, build command was migrated to docker-buildx
    # In Ubuntu, in practice, means to install package docker-buildx together with docker.io
    # Check if docker-buildx plugin is installed
    docker buildx version 1>/dev/null 2>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "Docker buildx command is not installed. Check: https://docs.docker.com/build/architecture/#install-buildx"
        echo "If you installed docker through APT package docker.io, consider installing also package docker-buildx"
        exit 1;
    fi
    DOCKER_BUILD="docker buildx build"
fi

for COMPONENT in $COMPONENTS; do
    echo "Processing '$COMPONENT' component..."
    IMAGE_NAME="$COMPONENT:$IMAGE_TAG"
    IMAGE_URL="$REGISTRY_IMAGE/$IMAGE_NAME"

    echo "  Building Docker image..."
    BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}.log"

    if [ "$COMPONENT" == "ztp" ] || [ "$COMPONENT" == "policy" ]; then
        $DOCKER_BUILD -t "$IMAGE_NAME" -f ./src/"$COMPONENT"/Dockerfile ./src/"$COMPONENT"/ > "$BUILD_LOG"
    else 
        $DOCKER_BUILD -t "$IMAGE_NAME" -f ./src/"$COMPONENT"/Dockerfile ./src/ > "$BUILD_LOG"
    fi

    if [ -n "$REGISTRY_IMAGE" ]; then
        echo "Pushing Docker image to '$REGISTRY_IMAGE'..."

        TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}.log"
        docker tag "$IMAGE_NAME" "$IMAGE_URL" > "$TAG_LOG"

        PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}.log"
        docker push "$IMAGE_URL" > "$PUSH_LOG"
    fi
done

echo "Preparing for running the tests..."

if docker network list | grep teraflowbridge; then echo "teraflowbridge is already created"; else docker network create -d bridge teraflowbridge; fi  

for COMPONENT in $COMPONENTS; do
    IMAGE_NAME="$COMPONENT:$IMAGE_TAG"
    echo "  Running tests for $COMPONENT:"
    docker run -it -d --name $COMPONENT $IMAGE_NAME --network=teraflowbridge
    docker exec -it $COMPONENT bash -c "pytest --log-level=DEBUG --verbose $COMPONENT/tests/test_unitary.py"
    docker stop $COMPONENT
done
