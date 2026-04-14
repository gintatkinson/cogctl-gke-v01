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


########################################################################################################################
# Read deployment settings
########################################################################################################################


# ----- TeraFlowSDN ------------------------------------------------------------

# If not already set, set the URL of the Docker registry where the images will be uploaded to.
# By default, assume internal MicroK8s registry is used.
export TFS_REGISTRY_IMAGES=${TFS_REGISTRY_IMAGES:-"http://localhost:32000/tfs/"}

# If not already set, set the list of components, separated by spaces, you want to build images for, and deploy.
# By default, only basic components are deployed
export TFS_COMPONENTS=${TFS_COMPONENTS:-"context device pathcomp service slice nbi webui load_generator"}

# If not already set, set the tag you want to use for your images.
export TFS_IMAGE_TAG=${TFS_IMAGE_TAG:-"dev"}


########################################################################################################################
# Automated steps start here
########################################################################################################################

# Create a tmp folder for files modified during the deployment
TMP_LOGS_FOLDER="./tmp/build"
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

for COMPONENT in $TFS_COMPONENTS; do
    echo "Processing '$COMPONENT' component..."

    echo "  Building Docker image..."
    BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}.log"

    if [ "$COMPONENT" == "ztp" ] || [ "$COMPONENT" == "policy" ]; then
        $DOCKER_BUILD -t "$COMPONENT:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/Dockerfile ./src/"$COMPONENT"/ > "$BUILD_LOG"
    elif [ "$COMPONENT" == "pathcomp" ] || [ "$COMPONENT" == "telemetry" ] || [ "$COMPONENT" == "analytics" ]; then
        BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}-frontend.log"
        $DOCKER_BUILD -t "$COMPONENT-frontend:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/frontend/Dockerfile . > "$BUILD_LOG"

        BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}-backend.log"
        $DOCKER_BUILD -t "$COMPONENT-backend:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/backend/Dockerfile . > "$BUILD_LOG"
        if [ "$COMPONENT" == "pathcomp" ]; then
            # next command is redundant, but helpful to keep cache updated between rebuilds
            IMAGE_NAME="$COMPONENT-backend:$TFS_IMAGE_TAG-builder"
            $DOCKER_BUILD -t "$IMAGE_NAME" --target builder -f ./src/"$COMPONENT"/backend/Dockerfile . >> "$BUILD_LOG"
        fi
    elif [ "$COMPONENT" == "dlt" ]; then
        BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}-connector.log"
        $DOCKER_BUILD -t "$COMPONENT-connector:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/connector/Dockerfile . > "$BUILD_LOG"

        BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}-gateway.log"
        $DOCKER_BUILD -t "$COMPONENT-gateway:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/gateway/Dockerfile . > "$BUILD_LOG"
    else
        $DOCKER_BUILD -t "$COMPONENT:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/Dockerfile . > "$BUILD_LOG"
    fi

    echo "  Pushing Docker image to '$TFS_REGISTRY_IMAGES'..."

    if [ "$COMPONENT" == "pathcomp" ] || [ "$COMPONENT" == "telemetry" ] || [ "$COMPONENT" == "analytics" ] ; then
        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-frontend:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')

        TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}-frontend.log"
        docker tag "$COMPONENT-frontend:$TFS_IMAGE_TAG" "$IMAGE_URL" > "$TAG_LOG"

        PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}-frontend.log"
        docker push "$IMAGE_URL" > "$PUSH_LOG"

        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-backend:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')

        TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}-backend.log"
        docker tag "$COMPONENT-backend:$TFS_IMAGE_TAG" "$IMAGE_URL" > "$TAG_LOG"

        PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}-backend.log"
        docker push "$IMAGE_URL" > "$PUSH_LOG"
    elif [ "$COMPONENT" == "dlt" ]; then
        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-connector:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')

        TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}-connector.log"
        docker tag "$COMPONENT-connector:$TFS_IMAGE_TAG" "$IMAGE_URL" > "$TAG_LOG"

        PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}-connector.log"
        docker push "$IMAGE_URL" > "$PUSH_LOG"

        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-gateway:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')

        TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}-gateway.log"
        docker tag "$COMPONENT-gateway:$TFS_IMAGE_TAG" "$IMAGE_URL" > "$TAG_LOG"

        PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}-gateway.log"
        docker push "$IMAGE_URL" > "$PUSH_LOG"
    else
        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')

        TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}.log"
        docker tag "$COMPONENT:$TFS_IMAGE_TAG" "$IMAGE_URL" > "$TAG_LOG"

        PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}.log"
        docker push "$IMAGE_URL" > "$PUSH_LOG"
    fi

    printf "\n"
done

echo "Pruning Docker Images..."
docker image prune --force
printf "\n\n"

if [ "$DOCKER_BUILD" == "docker buildx build" ]; then
    echo "Pruning Docker Buildx Cache..."
    docker buildx prune --force
    printf "\n\n"
fi
