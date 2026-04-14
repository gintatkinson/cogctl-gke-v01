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


# OECC/PSC 22 deployment settings
export REGISTRY_IMAGE=""
export COMPONENTS="context device monitoring service slice interdomain nbi" # webui
export IMAGE_TAG="oeccpsc22"
export K8S_HOSTNAME="kubernetes-master"
#export GRAFANA_PASSWORD="admin123+"

# Constants
GITLAB_REPO_URL="labs.etsi.org:5050/tfs/controller"
TMP_FOLDER="./tmp"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="$TMP_FOLDER/manifests"
mkdir -p $TMP_MANIFESTS_FOLDER
TMP_LOGS_FOLDER="$TMP_FOLDER/logs"
mkdir -p $TMP_LOGS_FOLDER

export K8S_NAMESPACE_1="oeccpsc22-1"
export K8S_NAMESPACE_2="oeccpsc22-2"

export EXTRA_MANIFESTS_1="./oeccpsc22/expose_services_teraflow_1.yaml"
export EXTRA_MANIFESTS_2="./oeccpsc22/expose_services_teraflow_2.yaml"

echo "Deleting and Creating new namespaces..."
kubectl delete namespace $K8S_NAMESPACE_1 $K8S_NAMESPACE_2
kubectl create namespace $K8S_NAMESPACE_1
kubectl create namespace $K8S_NAMESPACE_2
printf "\n"

echo "Creating secrets for InfluxDB..."
#TODO: make sure to change this when having a production deployment
kubectl create secret generic influxdb-secrets --namespace=$K8S_NAMESPACE_1 --from-literal=INFLUXDB_DB="monitoring" --from-literal=INFLUXDB_ADMIN_USER="teraflow" --from-literal=INFLUXDB_ADMIN_PASSWORD="teraflow" --from-literal=INFLUXDB_HTTP_AUTH_ENABLED="True"
kubectl create secret generic monitoring-secrets --namespace=$K8S_NAMESPACE_1 --from-literal=INFLUXDB_DATABASE="monitoring" --from-literal=INFLUXDB_USER="teraflow" --from-literal=INFLUXDB_PASSWORD="teraflow" --from-literal=INFLUXDB_HOSTNAME="localhost"

kubectl create secret generic influxdb-secrets --namespace=$K8S_NAMESPACE_2 --from-literal=INFLUXDB_DB="monitoring" --from-literal=INFLUXDB_ADMIN_USER="teraflow" --from-literal=INFLUXDB_ADMIN_PASSWORD="teraflow" --from-literal=INFLUXDB_HTTP_AUTH_ENABLED="True"
kubectl create secret generic monitoring-secrets --namespace=$K8S_NAMESPACE_2 --from-literal=INFLUXDB_DATABASE="monitoring" --from-literal=INFLUXDB_USER="teraflow" --from-literal=INFLUXDB_PASSWORD="teraflow" --from-literal=INFLUXDB_HOSTNAME="localhost"
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
        docker build -t "$IMAGE_NAME" -f ./src/"$COMPONENT"/Dockerfile ./src/ > "$BUILD_LOG"
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

    echo "  Deploying '$COMPONENT' component to Kubernetes $K8S_NAMESPACE_1..."
    DEPLOY_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}_1.log"
    kubectl --namespace $K8S_NAMESPACE_1 apply -f "$MANIFEST" > "$DEPLOY_LOG"
    kubectl --namespace $K8S_NAMESPACE_1 scale deployment --replicas=0 ${COMPONENT}service >> "$DEPLOY_LOG"
    kubectl --namespace $K8S_NAMESPACE_1 scale deployment --replicas=1 ${COMPONENT}service >> "$DEPLOY_LOG"

    echo "  Deploying '$COMPONENT' component to Kubernetes $K8S_NAMESPACE_2..."
    DEPLOY_LOG="$TMP_LOGS_FOLDER/push_${COMPONENT}_2.log"
    kubectl --namespace $K8S_NAMESPACE_2 apply -f "$MANIFEST" > "$DEPLOY_LOG"
    kubectl --namespace $K8S_NAMESPACE_2 scale deployment --replicas=0 ${COMPONENT}service >> "$DEPLOY_LOG"
    kubectl --namespace $K8S_NAMESPACE_2 scale deployment --replicas=1 ${COMPONENT}service >> "$DEPLOY_LOG"

    printf "\n"
done

echo "Deploying extra manifests to Kubernetes $K8S_NAMESPACE_1..."
for EXTRA_MANIFEST in $EXTRA_MANIFESTS_1; do
    echo "Processing manifest '$EXTRA_MANIFEST'..."
    kubectl --namespace $K8S_NAMESPACE_1 apply -f $EXTRA_MANIFEST
    printf "\n"
done

echo "Deploying extra manifests to Kubernetes $K8S_NAMESPACE_2..."
for EXTRA_MANIFEST in $EXTRA_MANIFESTS_2; do
    echo "Processing manifest '$EXTRA_MANIFEST'..."
    kubectl --namespace $K8S_NAMESPACE_2 apply -f $EXTRA_MANIFEST
    printf "\n"
done

# By now, leave this control here. Some component dependencies are not well handled
for COMPONENT in $COMPONENTS; do
    echo "Waiting for '$COMPONENT' component in Kubernetes $K8S_NAMESPACE_1..."
    kubectl wait --namespace $K8S_NAMESPACE_1 --for='condition=available' --timeout=300s deployment/${COMPONENT}service
    printf "\n"

    echo "Waiting for '$COMPONENT' component in Kubernetes $K8S_NAMESPACE_2..."
    kubectl wait --namespace $K8S_NAMESPACE_2 --for='condition=available' --timeout=300s deployment/${COMPONENT}service
    printf "\n"
done

if [[ "$COMPONENTS" == *"webui"* ]]; then
    echo "Configuring WebUI DataStores and Dashboards..."
    ./configure_dashboards.sh
    printf "\n\n"
fi

echo "Removing dangling docker images..."
docker image prune --force
printf "\n"

echo "Reporting Deployment in Kubernetes $K8S_NAMESPACE_1..."
kubectl --namespace $K8S_NAMESPACE_1 get all
printf "\n"

echo "Reporting Deployment in Kubernetes $K8S_NAMESPACE_2..."
kubectl --namespace $K8S_NAMESPACE_2 get all
printf "\n"

echo "Done!"
