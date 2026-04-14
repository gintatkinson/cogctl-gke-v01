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
# Define your deployment settings here
########################################################################################################################

# If not already set, set the URL of your local Docker registry where the images will be uploaded to. Leave it blank if
# you do not want to use any Docker registry.
export REGISTRY_IMAGE=${REGISTRY_IMAGE:-""}
#export REGISTRY_IMAGE="http://my-container-registry.local/"

# If not already set, set the list of components you want to build images for, and deploy.
export COMPONENTS=${COMPONENTS:-"context device ztp policy service nbi monitoring dbscanserving opticalattackmitigator opticalcentralizedattackdetector webui"}

# If not already set, set the tag you want to use for your images.
export IMAGE_TAG=${IMAGE_TAG:-"tf-dev"}

# If not already set, set the name of the Kubernetes namespace to deploy to.
export K8S_NAMESPACE=${K8S_NAMESPACE:-"tf-dev"}

# If not already set, set the name of the Kubernetes hostname to deploy to.
export K8S_HOSTNAME=${K8S_HOSTNAME:-"kubernetes-master"}

# If not already set, set additional manifest files to be applied after the deployment
export EXTRA_MANIFESTS=${EXTRA_MANIFESTS:-""}

########################################################################################################################
# Automated steps start here
########################################################################################################################

# Constants
GITLAB_REPO_URL="labs.etsi.org:5050/tfs/controller"
TMP_FOLDER="./tmp"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="$TMP_FOLDER/manifests"
mkdir -p $TMP_MANIFESTS_FOLDER
TMP_LOGS_FOLDER="$TMP_FOLDER/logs"
mkdir -p $TMP_LOGS_FOLDER

echo "Deleting and Creating a new namespace..."
kubectl delete namespace $K8S_NAMESPACE
kubectl create namespace $K8S_NAMESPACE
printf "\n"

echo "Creating secrets for InfluxDB..."
#TODO: make sure to change this when having a production deployment
kubectl create secret generic influxdb-secrets --namespace=$K8S_NAMESPACE --from-literal=INFLUXDB_DB="monitoring" --from-literal=INFLUXDB_ADMIN_USER="teraflow" --from-literal=INFLUXDB_ADMIN_PASSWORD="teraflow" --from-literal=INFLUXDB_HTTP_AUTH_ENABLED="True"
kubectl create secret generic monitoring-secrets --namespace=$K8S_NAMESPACE --from-literal=INFLUXDB_DATABASE="monitoring" --from-literal=INFLUXDB_USER="teraflow" --from-literal=INFLUXDB_PASSWORD="teraflow" --from-literal=INFLUXDB_HOSTNAME="localhost"
printf "\n"

echo "Pulling/Updating Docker images..."
docker pull redis:6.2
docker pull influxdb:1.8
docker pull grafana/grafana:8.2.6
printf "\n"

echo "Deploying components..."
for COMPONENT in $COMPONENTS; do
    echo "Processing '$COMPONENT' component..."
    IMAGE_NAME="$COMPONENT:$IMAGE_TAG"
    IMAGE_URL="$REGISTRY_IMAGE/$IMAGE_NAME"

    echo "  Building Docker image..."
    BUILD_LOG="$TMP_LOGS_FOLDER/build_${COMPONENT}.log"

    if [ "$COMPONENT" == "ztp" ] || [ "$COMPONENT" == "policy" ]; then
        docker build -t "$IMAGE_NAME" -f ./src/"$COMPONENT"/Dockerfile ./src/"$COMPONENT"/ > "$BUILD_LOG"
    else 
        docker build -t "$IMAGE_NAME" -f ./src/"$COMPONENT"/Dockerfile . > "$BUILD_LOG"
    fi

    if [ -n "$REGISTRY_IMAGE" ]; then
        echo "Pushing Docker image to '$REGISTRY_IMAGE'..."

        TAG_LOG="$TMP_LOGS_FOLDER/tag_${COMPONENT}.log"
        docker tag "$IMAGE_NAME" "$IMAGE_URL" > "$TAG_LOG"

        PUSH_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}.log"
        docker push "$IMAGE_URL" > "$PUSH_LOG"
    fi

    echo "  Adapting '$COMPONENT' manifest file..."
    MANIFEST="$TMP_MANIFESTS_FOLDER/${COMPONENT}service.yaml"
    cp ./manifests/"${COMPONENT}"service.yaml "$MANIFEST"
    VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}:" "$MANIFEST" | cut -d ":" -f3)

    if [ -n "$REGISTRY_IMAGE" ]; then

        sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"
        sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Always#g" "$MANIFEST"
   
    else
        sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT:${VERSION}#image: $IMAGE_NAME#g" "$MANIFEST"
        sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Never#g" "$MANIFEST"        
    fi

    echo "  Deploying '$COMPONENT' component to Kubernetes..."
    DEPLOY_LOG="$TMP_LOGS_FOLDER/deploy_${COMPONENT}.log"
    kubectl --namespace $K8S_NAMESPACE apply -f "$MANIFEST" > "$DEPLOY_LOG"

    COMPONENT_OBJNAME=$(echo "${COMPONENT}" | sed "s/\_/-/")
    kubectl --namespace $K8S_NAMESPACE scale deployment --replicas=0 ${COMPONENT_OBJNAME}service >> "$DEPLOY_LOG"
    kubectl --namespace $K8S_NAMESPACE scale deployment --replicas=1 ${COMPONENT_OBJNAME}service >> "$DEPLOY_LOG"
    printf "\n"
done

echo "Deploying extra manifests..."
for EXTRA_MANIFEST in $EXTRA_MANIFESTS; do
    echo "Processing manifest '$EXTRA_MANIFEST'..."
    kubectl --namespace $K8S_NAMESPACE apply -f $EXTRA_MANIFEST
    printf "\n"
done

# By now, leave this control here. Some component dependencies are not well handled
for COMPONENT in $COMPONENTS; do
    echo "Waiting for '$COMPONENT' component..."
    kubectl wait --namespace $K8S_NAMESPACE --for='condition=available' --timeout=300s deployment/${COMPONENT}service
    printf "\n"
done


if [[ "$COMPONENTS" == *"webui"* ]]; then
    echo "Configuring WebUI DataStores and Dashboards..."
    ./configure_dashboards_in_kubernetes.sh
    printf "\n\n"
fi

echo "Reporting Deployment..."
kubectl --namespace $K8S_NAMESPACE get all
printf "\n"

echo "Done!"
