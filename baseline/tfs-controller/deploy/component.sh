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

# If not already set, set the URL of the Docker registry where the images will be uploaded to.
# By default, assume internal MicroK8s registry is used.
export TFS_REGISTRY_IMAGES=${TFS_REGISTRY_IMAGES:-"http://localhost:32000/tfs/"}

TFS_COMPONENTS=$1

# If not already set, set the tag you want to use for your images.
export TFS_IMAGE_TAG=${TFS_IMAGE_TAG:-"dev"}

# If not already set, set the name of the Kubernetes namespace to deploy to.
export TFS_K8S_NAMESPACE=${TFS_K8S_NAMESPACE:-"tfs"}

# If not already set, set additional manifest files to be applied after the deployment
export TFS_EXTRA_MANIFESTS=${TFS_EXTRA_MANIFESTS:-""}

# If not already set, set the neew Grafana admin password
export TFS_GRAFANA_PASSWORD=${TFS_GRAFANA_PASSWORD:-"admin123+"}

########################################################################################################################
# Automated steps start here
########################################################################################################################

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

# Constants
GITLAB_REPO_URL="labs.etsi.org:5050/tfs/controller"
TMP_FOLDER="./tmp"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="$TMP_FOLDER/manifests"
TMP_LOGS_FOLDER="$TMP_FOLDER/logs"

echo "Deploying component and collecting environment variables..."
ENV_VARS_SCRIPT=tfs_runtime_env_vars.sh

for COMPONENT in $TFS_COMPONENTS; do
    echo "Processing '$COMPONENT' component..."
    IMAGE_NAME="$COMPONENT:$TFS_IMAGE_TAG"
    IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$IMAGE_NAME" | sed 's,//,/,g' | sed 's,http:/,,g')

    echo "  Building Docker image..."
    BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}.log"

    if [ "$COMPONENT" == "ztp" ] || [ "$COMPONENT" == "policy" ]; then
        $DOCKER_BUILD -t "$IMAGE_NAME" -f ./src/"$COMPONENT"/Dockerfile ./src/"$COMPONENT"/ > "$BUILD_LOG"
    elif [ "$COMPONENT" == "pathcomp" ]; then
        BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}-frontend.log"
        $DOCKER_BUILD -t "$COMPONENT-frontend:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/frontend/Dockerfile . >> "$BUILD_LOG"

        BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}-backend.log"
        $DOCKER_BUILD -t "$COMPONENT-backend:$TFS_IMAGE_TAG" -f ./src/"$COMPONENT"/backend/Dockerfile . >> "$BUILD_LOG"
        # next command is redundant, but helpful to keep cache updated between rebuilds
        $DOCKER_BUILD -t "$COMPONENT-backend:$TFS_IMAGE_TAG-builder" --target builder -f ./src/"$COMPONENT"/backend/Dockerfile . >> "$BUILD_LOG"
    else
        $DOCKER_BUILD -t "$IMAGE_NAME" -f ./src/"$COMPONENT"/Dockerfile . > "$BUILD_LOG"
    fi

    if [ -n "$TFS_REGISTRY_IMAGES" ]; then
        echo "  Pushing Docker image to '$TFS_REGISTRY_IMAGES'..."

        if [ "$COMPONENT" == "pathcomp" ]; then
            TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}-frontend.log"
            docker tag "$COMPONENT-frontend:$TFS_IMAGE_TAG" "$IMAGE_URL-frontend" > "$TAG_LOG"

            TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}-backend.log"
            docker tag "$COMPONENT-backend:$TFS_IMAGE_TAG" "$IMAGE_URL-backend" > "$TAG_LOG"

            PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}-frontend.log"
            docker push "$IMAGE_URL-frontend" > "$PUSH_LOG"

            PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}-backend.log"
            docker push "$IMAGE_URL-backend" > "$PUSH_LOG"
        else
            TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}.log"
            docker tag "$IMAGE_NAME" "$IMAGE_URL" > "$TAG_LOG"

            PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}.log"
            docker push "$IMAGE_URL" > "$PUSH_LOG"
        fi
    fi

    echo "  Adapting '$COMPONENT' manifest file..."
    MANIFEST="$TMP_MANIFESTS_FOLDER/${COMPONENT}service.yaml"
    cp ./manifests/"${COMPONENT}"service.yaml "$MANIFEST"

    if [ -n "$TFS_REGISTRY_IMAGES" ]; then
        # Registry is set
        if [ "$COMPONENT" == "pathcomp" ]; then
            VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-frontend:" "$MANIFEST" | cut -d ":" -f3)
            sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-frontend:${VERSION}#image: $IMAGE_URL-frontend#g" "$MANIFEST"

            VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-backend:" "$MANIFEST" | cut -d ":" -f3)
            sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-backend:${VERSION}#image: $IMAGE_URL-backend#g" "$MANIFEST"

            sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Always#g" "$MANIFEST"
        else
            VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}:" "$MANIFEST" | cut -d ":" -f3)
            sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"
            sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Always#g" "$MANIFEST"
        fi
    else
        # Registry is not set
        if [ "$COMPONENT" == "pathcomp" ]; then
            VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-frontend:" "$MANIFEST" | cut -d ":" -f3)
            sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-frontend:${VERSION}#image: $IMAGE_NAME-frontend#g" "$MANIFEST"

            VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-backend:" "$MANIFEST" | cut -d ":" -f3)
            sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-backend:${VERSION}#image: $IMAGE_NAME-backend#g" "$MANIFEST"

            sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Never#g" "$MANIFEST"
        else
            VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}:" "$MANIFEST" | cut -d ":" -f3)
            sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT:${VERSION}#image: $IMAGE_NAME#g" "$MANIFEST"
            sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Never#g" "$MANIFEST"
        fi
    fi

    # TODO: harmonize names of the monitoring component

    echo "  Deploying '$COMPONENT' component to Kubernetes..."
    DEPLOY_LOG="$TMP_LOGS_FOLDER/deploy_${COMPONENT}.log"
    kubectl --namespace $TFS_K8S_NAMESPACE delete -f "$MANIFEST" > "$DEPLOY_LOG"
    kubectl --namespace $TFS_K8S_NAMESPACE apply -f "$MANIFEST" > "$DEPLOY_LOG"
    COMPONENT_OBJNAME=$(echo "${COMPONENT}" | sed "s/\_/-/")
    kubectl --namespace $TFS_K8S_NAMESPACE scale deployment --replicas=0 ${COMPONENT_OBJNAME}service >> "$DEPLOY_LOG"
    kubectl --namespace $TFS_K8S_NAMESPACE scale deployment --replicas=1 ${COMPONENT_OBJNAME}service >> "$DEPLOY_LOG"

    echo "  Collecting env-vars for '$COMPONENT' component..."

    SERVICE_DATA=$(kubectl get service ${COMPONENT}service --namespace $TFS_K8S_NAMESPACE -o json)
    if [ -z "${SERVICE_DATA}" ]; then continue; fi

    # Env vars for service's host address
    SERVICE_HOST=$(echo ${SERVICE_DATA} | jq -r '.spec.clusterIP')
    if [ -z "${SERVICE_HOST}" ]; then continue; fi
    # TODO: remove previous value from file
    ENVVAR_HOST=$(echo "${COMPONENT}service_SERVICE_HOST" | tr '[:lower:]' '[:upper:]')
    echo "export ${ENVVAR_HOST}=${SERVICE_HOST}" >> $ENV_VARS_SCRIPT

    # Env vars for service's 'grpc' port (if any)
    SERVICE_PORT_GRPC=$(echo ${SERVICE_DATA} | jq -r '.spec.ports[] | select(.name=="grpc") | .port')
    if [ -n "${SERVICE_PORT_GRPC}" ]; then
        ENVVAR_PORT_GRPC=$(echo "${COMPONENT}service_SERVICE_PORT_GRPC" | tr '[:lower:]' '[:upper:]')
        echo "export ${ENVVAR_PORT_GRPC}=${SERVICE_PORT_GRPC}" >> $ENV_VARS_SCRIPT
    fi

    # Env vars for service's 'http' port (if any)
    SERVICE_PORT_HTTP=$(echo ${SERVICE_DATA} | jq -r '.spec.ports[] | select(.name=="http") | .port')
    if [ -n "${SERVICE_PORT_HTTP}" ]; then
        ENVVAR_PORT_HTTP=$(echo "${COMPONENT}service_SERVICE_PORT_HTTP" | tr '[:lower:]' '[:upper:]')
        echo "export ${ENVVAR_PORT_HTTP}=${SERVICE_PORT_HTTP}" >> $ENV_VARS_SCRIPT
    fi

    printf "\n"
done

# By now, leave this control here. Some component dependencies are not well handled
for COMPONENT in $TFS_COMPONENTS; do
    echo "Waiting for '$COMPONENT' component..."
    kubectl wait --namespace $TFS_K8S_NAMESPACE \
        --for='condition=available' --timeout=300s deployment/${COMPONENT}service
    printf "\n"
done

./show_deploy.sh

echo "Done!"
