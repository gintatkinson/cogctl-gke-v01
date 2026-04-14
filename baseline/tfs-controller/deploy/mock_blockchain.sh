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

# Set the URL of your local Docker registry where the images will be uploaded to.
REGISTRY_IMAGE="http://localhost:32000/tfs/"

# Set the tag you want to use for your images.
IMAGE_TAG="dev"

# Set the name of the Kubernetes namespace to deploy to.
K8S_NAMESPACE="tfs-bchain"

COMPONENT="mock_blockchain"

########################################################################################################################
# Automated steps start here
########################################################################################################################

# Constants
GITLAB_REPO_URL="labs.etsi.org:5050/tfs/controller"
TMP_FOLDER="./tmp"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="${TMP_FOLDER}/${K8S_NAMESPACE}/manifests"
mkdir -p $TMP_MANIFESTS_FOLDER
TMP_LOGS_FOLDER="${TMP_FOLDER}/${K8S_NAMESPACE}/logs"
mkdir -p $TMP_LOGS_FOLDER

echo "Deleting and Creating a new namespace..."
kubectl delete namespace $K8S_NAMESPACE --ignore-not-found
kubectl create namespace $K8S_NAMESPACE
printf "\n"

echo "Deploying components and collecting environment variables..."
ENV_VARS_SCRIPT=tfs_bchain_runtime_env_vars.sh
echo "# Environment variables for TeraFlowSDN Mock-Blockchain deployment" > $ENV_VARS_SCRIPT
PYTHONPATH=$(pwd)/src
echo "export PYTHONPATH=${PYTHONPATH}" >> $ENV_VARS_SCRIPT

echo "Processing '$COMPONENT' component..."
IMAGE_NAME="$COMPONENT:$IMAGE_TAG"
IMAGE_URL=$(echo "$REGISTRY_IMAGE/$IMAGE_NAME" | sed 's,//,/,g' | sed 's,http:/,,g')

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

echo "  Building Docker image..."
BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}.log"
$DOCKER_BUILD -t "$IMAGE_NAME" -f ./src/dlt/mock_blockchain/Dockerfile . > "$BUILD_LOG"

if [ -n "$REGISTRY_IMAGE" ]; then
    echo "  Pushing Docker image to '$REGISTRY_IMAGE'..."

    TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}.log"
    docker tag "$IMAGE_NAME" "$IMAGE_URL" > "$TAG_LOG"

    PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}.log"
    docker push "$IMAGE_URL" > "$PUSH_LOG"
fi

echo "  Adapting '$COMPONENT' manifest file..."
MANIFEST="$TMP_MANIFESTS_FOLDER/${COMPONENT}.yaml"
cp ./manifests/"${COMPONENT}".yaml "$MANIFEST"

if [ -n "$REGISTRY_IMAGE" ]; then
    # Registry is set
    VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}:" "$MANIFEST" | cut -d ":" -f4)
    sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"
    sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Always#g" "$MANIFEST"
else
    # Registry is not set
    VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}:" "$MANIFEST" | cut -d ":" -f4)
    sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT:${VERSION}#image: $IMAGE_NAME#g" "$MANIFEST"
    sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Never#g" "$MANIFEST"
fi

echo "  Deploying '$COMPONENT' component to Kubernetes..."
DEPLOY_LOG="$TMP_LOGS_FOLDER/deploy_${COMPONENT}.log"
kubectl --namespace $K8S_NAMESPACE apply -f "$MANIFEST" > "$DEPLOY_LOG"
COMPONENT_OBJNAME=$(echo "${COMPONENT}" | sed "s/\_/-/")
#kubectl --namespace $K8S_NAMESPACE scale deployment --replicas=0 ${COMPONENT_OBJNAME} >> "$DEPLOY_LOG"
#kubectl --namespace $K8S_NAMESPACE scale deployment --replicas=1 ${COMPONENT_OBJNAME} >> "$DEPLOY_LOG"

echo "  Collecting env-vars for '$COMPONENT' component..."
SERVICE_DATA=$(kubectl get service ${COMPONENT_OBJNAME} --namespace $K8S_NAMESPACE -o json)

# Env vars for service's host address
SERVICE_HOST=$(echo ${SERVICE_DATA} | jq -r '.spec.clusterIP')
ENVVAR_HOST=$(echo "${COMPONENT}_SERVICE_HOST" | tr '[:lower:]' '[:upper:]')
echo "export ${ENVVAR_HOST}=${SERVICE_HOST}" >> $ENV_VARS_SCRIPT

# Env vars for service's 'grpc' port
SERVICE_PORT_GRPC=$(echo ${SERVICE_DATA} | jq -r '.spec.ports[] | select(.name=="grpc") | .port')
ENVVAR_PORT_GRPC=$(echo "${COMPONENT}_SERVICE_PORT_GRPC" | tr '[:lower:]' '[:upper:]')
echo "export ${ENVVAR_PORT_GRPC}=${SERVICE_PORT_GRPC}" >> $ENV_VARS_SCRIPT

printf "\n"

echo "Waiting for '$COMPONENT' component..."
kubectl wait --namespace $K8S_NAMESPACE \
    --for='condition=available' --timeout=300s deployment/${COMPONENT_OBJNAME}
printf "\n"

echo "Deployment Resources:"
kubectl --namespace $K8S_NAMESPACE get all
printf "\n"

echo "Done!"
