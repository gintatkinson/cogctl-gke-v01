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

# If not already set, set the name of the Kubernetes namespace to deploy TFS to.
export TFS_K8S_NAMESPACE=${TFS_K8S_NAMESPACE:-"tfs"}

# If not already set, set additional manifest files to be applied after the deployment
export TFS_EXTRA_MANIFESTS=${TFS_EXTRA_MANIFESTS:-""}

# If not already set, set the new Grafana admin password
export TFS_GRAFANA_PASSWORD=${TFS_GRAFANA_PASSWORD:-"admin123+"}

# If not already set, disable skip-build flag to rebuild the Docker images.
# If TFS_SKIP_BUILD is "YES", the containers are not rebuilt-retagged-repushed and existing ones are used.
export TFS_SKIP_BUILD=${TFS_SKIP_BUILD:-""}


# ----- CockroachDB ------------------------------------------------------------

# If not already set, set the namespace where CockroackDB will be deployed.
export CRDB_NAMESPACE=${CRDB_NAMESPACE:-"crdb"}

# If not already set, set the database username to be used by Context.
export CRDB_USERNAME=${CRDB_USERNAME:-"tfs"}

# If not already set, set the database user's password to be used by Context.
export CRDB_PASSWORD=${CRDB_PASSWORD:-"tfs123"}


# ----- NATS -------------------------------------------------------------------

# If not already set, set the namespace where NATS will be deployed.
export NATS_NAMESPACE=${NATS_NAMESPACE:-"nats"}


# ----- QuestDB ----------------------------------------------------------------

# If not already set, set the namespace where QuestDB will be deployed.
export QDB_NAMESPACE=${QDB_NAMESPACE:-"qdb"}

# If not already set, set the database username to be used for QuestDB.
export QDB_USERNAME=${QDB_USERNAME:-"admin"}

# If not already set, set the database user's password to be used for QuestDB.
export QDB_PASSWORD=${QDB_PASSWORD:-"quest"}

# If not already set, set the table name to be used by Monitoring for KPIs.
export QDB_TABLE_MONITORING_KPIS=${QDB_TABLE_MONITORING_KPIS:-"tfs_monitoring_kpis"}

# If not already set, set the table name to be used by Slice for plotting groups.
export QDB_TABLE_SLICE_GROUPS=${QDB_TABLE_SLICE_GROUPS:-"tfs_slice_groups"}


# ----- K8s Observability ------------------------------------------------------

# If not already set, set the external port Prometheus Mgmt HTTP GUI interface will be exposed to.
export PROM_EXT_PORT_HTTP=${PROM_EXT_PORT_HTTP:-"9090"}

# If not already set, set the external port Grafana HTTP Dashboards will be exposed to.
export GRAF_EXT_PORT_HTTP=${GRAF_EXT_PORT_HTTP:-"3000"}


# ----- Apache Kafka ------------------------------------------------------

# If not already set, set the namespace where Kafka will be deployed.
export KFK_NAMESPACE=${KFK_NAMESPACE:-"kafka"}


# ----- Telemetry Config ------------------------------------------------------

# Replace LOAD_BALANCER_IP
export LOAD_BALANCER_IP=${LOAD_BALANCER_IP:-""}

########################################################################################################################
# Automated steps start here
########################################################################################################################

# Constants
GITLAB_REPO_URL="labs.etsi.org:5050/tfs/controller"
TMP_FOLDER="./tmp"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="${TMP_FOLDER}/${TFS_K8S_NAMESPACE}/manifests"
mkdir -p $TMP_MANIFESTS_FOLDER
TMP_LOGS_FOLDER="${TMP_FOLDER}/${TFS_K8S_NAMESPACE}/logs"
mkdir -p $TMP_LOGS_FOLDER

echo "Deleting and Creating a new namespace..."
kubectl delete namespace $TFS_K8S_NAMESPACE --ignore-not-found
kubectl create namespace $TFS_K8S_NAMESPACE
sleep 2
printf "\n"

echo ">>> Create Secret with CockroachDB data..."
CRDB_SQL_PORT=$(kubectl --namespace ${CRDB_NAMESPACE} get service cockroachdb-public -o 'jsonpath={.spec.ports[?(@.name=="sql")].port}')
kubectl create secret generic crdb-data --namespace ${TFS_K8S_NAMESPACE} --type='Opaque' \
    --from-literal=CRDB_NAMESPACE=${CRDB_NAMESPACE} \
    --from-literal=CRDB_SQL_PORT=${CRDB_SQL_PORT} \
    --from-literal=CRDB_USERNAME=${CRDB_USERNAME} \
    --from-literal=CRDB_PASSWORD=${CRDB_PASSWORD} \
    --from-literal=CRDB_SSLMODE=require
printf "\n"

echo ">>> Create Secret with Apache Kafka..."
KFK_SERVER_PORT=$(kubectl --namespace ${KFK_NAMESPACE} get service kafka-public -o 'jsonpath={.spec.ports[0].port}')
kubectl create secret generic kfk-kpi-data --namespace ${TFS_K8S_NAMESPACE} --type='Opaque' \
    --from-literal=KFK_NAMESPACE=${KFK_NAMESPACE} \
    --from-literal=KFK_SERVER_PORT=${KFK_SERVER_PORT}
printf "\n"

echo "Create secret with NATS data"
NATS_CLIENT_PORT=$(kubectl --namespace ${NATS_NAMESPACE} get service ${NATS_NAMESPACE} -o 'jsonpath={.spec.ports[?(@.name=="client")].port}')
if [ -z "$NATS_CLIENT_PORT" ]; then
    # NATS charts updated and port name changed from "client" to "nats"; fix to support new name and enable backward compatibility
    NATS_CLIENT_PORT=$(kubectl --namespace ${NATS_NAMESPACE} get service ${NATS_NAMESPACE} -o 'jsonpath={.spec.ports[?(@.name=="nats")].port}')
fi
kubectl create secret generic nats-data --namespace ${TFS_K8S_NAMESPACE} --type='Opaque' \
    --from-literal=NATS_NAMESPACE=${NATS_NAMESPACE} \
    --from-literal=NATS_CLIENT_PORT=${NATS_CLIENT_PORT}
printf "\n"

echo "Create secret with QuestDB data"
QDB_HTTP_PORT=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.ports[?(@.name=="http")].port}')
QDB_ILP_PORT=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.ports[?(@.name=="ilp")].port}')
QDB_SQL_PORT=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.ports[?(@.name=="sql")].port}')
METRICSDB_HOSTNAME="questdb-public.${QDB_NAMESPACE}.svc.cluster.local"
kubectl create secret generic qdb-data --namespace ${TFS_K8S_NAMESPACE} --type='Opaque' \
    --from-literal=QDB_NAMESPACE=${QDB_NAMESPACE} \
    --from-literal=METRICSDB_HOSTNAME=${METRICSDB_HOSTNAME} \
    --from-literal=METRICSDB_REST_PORT=${QDB_HTTP_PORT} \
    --from-literal=METRICSDB_ILP_PORT=${QDB_ILP_PORT} \
    --from-literal=METRICSDB_SQL_PORT=${QDB_SQL_PORT} \
    --from-literal=METRICSDB_TABLE_MONITORING_KPIS=${QDB_TABLE_MONITORING_KPIS} \
    --from-literal=METRICSDB_TABLE_SLICE_GROUPS=${QDB_TABLE_SLICE_GROUPS} \
    --from-literal=METRICSDB_USERNAME=${QDB_USERNAME} \
    --from-literal=METRICSDB_PASSWORD=${QDB_PASSWORD}
printf "\n"

# Check if "dlt" is in the list of components
if [[ " ${TFS_COMPONENTS[@]} " =~ " dlt " ]]; then
  echo "Create secret for HLF keystore"
  kubectl create secret generic dlt-keystone --namespace ${TFS_K8S_NAMESPACE} --from-file=keystore=${KEY_DIRECTORY_PATH}
  printf "\n"

  echo "Create secret for HLF signcerts"
  kubectl create secret generic dlt-signcerts --namespace ${TFS_K8S_NAMESPACE} --from-file=signcerts.pem=${CERT_DIRECTORY_PATH}
  printf "\n"

  echo "Create secret for HLF ca.crt"
  kubectl create secret generic dlt-ca-crt --namespace ${TFS_K8S_NAMESPACE} --from-file=ca.crt=${TLS_CERT_PATH}
  printf "\n"
fi

echo "Deploying components and collecting environment variables..."
ENV_VARS_SCRIPT=tfs_runtime_env_vars.sh
echo "# Environment variables for TeraFlowSDN deployment" > $ENV_VARS_SCRIPT
PYTHONPATH=$(pwd)/src
echo "export PYTHONPATH=${PYTHONPATH}" >> $ENV_VARS_SCRIPT

echo "Create Redis secret..."
# first try to delete an old one if exists
kubectl delete secret redis-secrets --namespace=$TFS_K8S_NAMESPACE --ignore-not-found
REDIS_PASSWORD=`uuidgen`
kubectl create secret generic redis-secrets --namespace=$TFS_K8S_NAMESPACE \
    --from-literal=REDIS_PASSWORD=$REDIS_PASSWORD
echo "export REDIS_PASSWORD=${REDIS_PASSWORD}" >> $ENV_VARS_SCRIPT
printf "\n"

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

LINKERD_STATUS="$(microk8s status -a linkerd)"
if [[ $linkerd_status =~ "enabled" ]]; then
    echo "LinkerD installed: workloads will be injected"
else
    echo "LinkerD not installed"
fi
printf "\n"

if [[ "$TFS_COMPONENTS" == *"telemetry"* ]]; then
    echo "Configuring Telemetry Service..."

    # Before deployment change the telemetry LOAD_BALANCER_IP
    sed -i "s|_LOAD_BALANCER_IP_|$LOAD_BALANCER_IP|g" manifests/telemetryservice.yaml
fi

for COMPONENT in $TFS_COMPONENTS; do
    echo "Processing '$COMPONENT' component..."

    if [ "$TFS_SKIP_BUILD" != "YES" ]; then
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
    fi

    echo "  Adapting '$COMPONENT' manifest file..."
    MANIFEST="$TMP_MANIFESTS_FOLDER/${COMPONENT}service.yaml"
    if [[ $linkerd_status =~ "enabled" ]]; then
        cat ./manifests/"${COMPONENT}"service.yaml | linkerd inject - --proxy-cpu-request "10m" --proxy-cpu-limit "1" --proxy-memory-request "64Mi" --proxy-memory-limit "256Mi" > "$MANIFEST"
    else
        cp ./manifests/"${COMPONENT}"service.yaml "$MANIFEST"
    fi

    if [ "$COMPONENT" == "pathcomp" ] || [ "$COMPONENT" == "telemetry" ] || [ "$COMPONENT" == "analytics" ]; then
        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-frontend:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')
        VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-frontend:" "$MANIFEST" | cut -d ":" -f4)
        sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-frontend:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"

        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-backend:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')
        VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-backend:" "$MANIFEST" | cut -d ":" -f4)
        sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-backend:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"
    elif [ "$COMPONENT" == "dlt" ]; then
        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-connector:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')
        VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-connector:" "$MANIFEST" | cut -d ":" -f4)
        sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-connector:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"

        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT-gateway:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')
        VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}-gateway:" "$MANIFEST" | cut -d ":" -f4)
        sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT-gateway:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"
    else
        VERSION=$(grep -i "${GITLAB_REPO_URL}/${COMPONENT}:" "$MANIFEST" | cut -d ":" -f4)
        IMAGE_URL=$(echo "$TFS_REGISTRY_IMAGES/$COMPONENT:$TFS_IMAGE_TAG" | sed 's,//,/,g' | sed 's,http:/,,g')
        sed -E -i "s#image: $GITLAB_REPO_URL/$COMPONENT:${VERSION}#image: $IMAGE_URL#g" "$MANIFEST"
    fi

    sed -E -i "s#imagePullPolicy: .*#imagePullPolicy: Always#g" "$MANIFEST"

    # TODO: harmonize names of the monitoring component

    echo "  Deploying '$COMPONENT' component to Kubernetes..."
    DEPLOY_LOG="$TMP_LOGS_FOLDER/deploy_${COMPONENT}.log"
    kubectl --namespace $TFS_K8S_NAMESPACE apply -f "$MANIFEST" > "$DEPLOY_LOG"
    COMPONENT_OBJNAME=$(echo "${COMPONENT}" | sed "s/\_/-/g")
    #kubectl --namespace $TFS_K8S_NAMESPACE scale deployment --replicas=0 ${COMPONENT_OBJNAME}service >> "$DEPLOY_LOG"
    #kubectl --namespace $TFS_K8S_NAMESPACE scale deployment --replicas=1 ${COMPONENT_OBJNAME}service >> "$DEPLOY_LOG"

    echo "  Collecting env-vars for '$COMPONENT' component..."

    SERVICE_DATA=$(kubectl get service ${COMPONENT_OBJNAME}service --namespace $TFS_K8S_NAMESPACE -o json)
    if [ -z "${SERVICE_DATA}" ]; then continue; fi

    # Env vars for service's host address
    SERVICE_HOST=$(echo ${SERVICE_DATA} | jq -r '.spec.clusterIP')
    if [ -z "${SERVICE_HOST}" ]; then continue; fi
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

echo "Deploying extra manifests..."
for EXTRA_MANIFEST in $TFS_EXTRA_MANIFESTS; do
    echo "Processing manifest '$EXTRA_MANIFEST'..."
    if [[ "$EXTRA_MANIFEST" == *"servicemonitor"* ]]; then
        if kubectl get namespace monitoring &> /dev/null; then
            echo ">>> Namespace monitoring is present, applying service monitors..."
            kubectl apply -f $EXTRA_MANIFEST
        else
            echo ">>> Namespace monitoring is NOT present, skipping service monitors..."
        fi
    else
        kubectl --namespace $TFS_K8S_NAMESPACE apply -f $EXTRA_MANIFEST
    fi
    printf "\n"
done
printf "\n"

for COMPONENT in $TFS_COMPONENTS; do
    echo "Waiting for '$COMPONENT' component..."
    COMPONENT_OBJNAME=$(echo "${COMPONENT}" | sed "s/\_/-/g")
    kubectl wait --namespace $TFS_K8S_NAMESPACE \
        --for='condition=available' --timeout=90s deployment/${COMPONENT_OBJNAME}service
    WAIT_EXIT_CODE=$?
    if [[ $WAIT_EXIT_CODE != 0 ]]; then
        echo "  Failed to deploy '${COMPONENT}' component, exit code '${WAIT_EXIT_CODE}', exiting..."
        kubectl logs --namespace $TFS_K8S_NAMESPACE deployment/${COMPONENT_OBJNAME}service --all-containers=true
        exit $WAIT_EXIT_CODE
    fi
    printf "\n"
done

if [[ "$TFS_COMPONENTS" == *"monitoring"* ]] && [[ "$TFS_COMPONENTS" == *"webui"* ]]; then
    echo "Configuring WebUI DataStores and Dashboards..."
    sleep 5

    INGRESS_CTRL_NAME=$(echo "${TFS_K8S_NAMESPACE}" | sed "s/tfs/nginx-ingress-microk8s-controller/g")
    EXT_HTTP_PORT=$(kubectl get daemonsets.apps --namespace ingress ${INGRESS_CTRL_NAME} \
        -o 'jsonpath={.spec.template.spec.containers[?(@.name=="nginx-ingress-microk8s")].ports[?(@.name=="http")].hostPort}')

    # Exposed through the ingress controller "tfs-ingress"
    GRAFANA_URL="127.0.0.1:${EXT_HTTP_PORT}/grafana"

    # Default Grafana credentials when installed with the `monitoring` addon
    GRAFANA_USERNAME="admin"
    GRAFANA_PASSWORD="admin"

    # Configure Grafana Admin Password
    # Ref: https://grafana.com/docs/grafana/latest/http_api/user/#change-password
    GRAFANA_URL_DEFAULT="http://${GRAFANA_USERNAME}:${GRAFANA_PASSWORD}@${GRAFANA_URL}"

    echo ">> Updating Grafana 'admin' password..."
    curl -X PUT -H "Content-Type: application/json" -d '{
        "oldPassword": "'${GRAFANA_PASSWORD}'",
        "newPassword": "'${TFS_GRAFANA_PASSWORD}'",
        "confirmNew" : "'${TFS_GRAFANA_PASSWORD}'"
    }' ${GRAFANA_URL_DEFAULT}/api/user/password
    echo
    echo

    # Updated Grafana API URL
    GRAFANA_URL_UPDATED="http://${GRAFANA_USERNAME}:${TFS_GRAFANA_PASSWORD}@${GRAFANA_URL}"
    echo "export GRAFANA_URL_UPDATED=${GRAFANA_URL_UPDATED}" >> $ENV_VARS_SCRIPT

    echo ">> Installing Scatter Plot plugin..."
    curl -X POST -H "Content-Type: application/json" -H "Content-Length: 0" \
        ${GRAFANA_URL_UPDATED}/api/plugins/michaeldmoore-scatter-panel/install
    echo

    # Ref: https://grafana.com/docs/grafana/latest/http_api/data_source/
    QDB_HOST_PORT="${METRICSDB_HOSTNAME}:${QDB_SQL_PORT}"
    echo ">> Creating datasources..."
    curl -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{
        "access"   : "proxy",
        "type"     : "postgres",
        "name"     : "questdb-mon-kpi",
        "url"      : "'${QDB_HOST_PORT}'",
        "database" : "'${QDB_TABLE_MONITORING_KPIS}'",
        "user"     : "'${QDB_USERNAME}'",
        "basicAuth": false,
        "isDefault": true,
        "jsonData" : {
            "sslmode"               : "disable",
            "postgresVersion"       : 1100,
            "maxOpenConns"          : 0,
            "maxIdleConns"          : 2,
            "connMaxLifetime"       : 14400,
            "tlsAuth"               : false,
            "tlsAuthWithCACert"     : false,
            "timescaledb"           : false,
            "tlsConfigurationMethod": "file-path",
            "tlsSkipVerify"         : true
        },
        "secureJsonData": {"password": "'${QDB_PASSWORD}'"}
    }' ${GRAFANA_URL_UPDATED}/api/datasources
    echo

    curl -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{
        "access"   : "proxy",
        "type"     : "postgres",
        "name"     : "questdb-slc-grp",
        "url"      : "'${QDB_HOST_PORT}'",
        "database" : "'${QDB_TABLE_SLICE_GROUPS}'",
        "user"     : "'${QDB_USERNAME}'",
        "basicAuth": false,
        "isDefault": false,
        "jsonData" : {
            "sslmode"               : "disable",
            "postgresVersion"       : 1100,
            "maxOpenConns"          : 0,
            "maxIdleConns"          : 2,
            "connMaxLifetime"       : 14400,
            "tlsAuth"               : false,
            "tlsAuthWithCACert"     : false,
            "timescaledb"           : false,
            "tlsConfigurationMethod": "file-path",
            "tlsSkipVerify"         : true
        },
        "secureJsonData": {"password": "'${QDB_PASSWORD}'"}
    }' ${GRAFANA_URL_UPDATED}/api/datasources
    echo

    curl -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{
        "access"   : "proxy",
        "type"     : "postgres",
        "name"     : "cockroachdb",
        "url"      : "'cockroachdb-public.${CRDB_NAMESPACE}.svc.cluster.local:${CRDB_SQL_PORT}'",
        "database" : "tfs_context",
        "user"     : "'${CRDB_USERNAME}'",
        "basicAuth": false,
        "isDefault": false,
        "jsonData" : {
            "sslmode"               : "require",
            "postgresVersion"       : 1100,
            "maxOpenConns"          : 0,
            "maxIdleConns"          : 2,
            "connMaxLifetime"       : 14400,
            "tlsAuth"               : false,
            "tlsAuthWithCACert"     : false,
            "timescaledb"           : false,
            "tlsConfigurationMethod": "file-path",
            "tlsSkipVerify"         : true
        },
        "secureJsonData": {"password": "'${CRDB_PASSWORD}'"}
    }' ${GRAFANA_URL_UPDATED}/api/datasources
    echo

    # adding the datasource of the metrics collection framework
    curl -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{
        "access"   : "proxy",
        "type"     : "prometheus",
        "name"     : "prometheus",
        "url"      : "http://prometheus-k8s.monitoring.svc:9090",
        "basicAuth": false,
        "isDefault": false,
        "jsonData" : {
            "httpMethod"               : "POST"
        }
    }' ${GRAFANA_URL_UPDATED}/api/datasources
    printf "\n\n"

    echo ">> Creating and staring dashboards..."
    # Ref: https://grafana.com/docs/grafana/latest/http_api/dashboard/

    # Dashboard: L3 Monitoring KPIs
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_db_mon_kpis_psql.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-l3-monit"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    # Dashboard: Slice Grouping
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_db_slc_grps_psql.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-slice-grps"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    # Dashboard: Component RPCs
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_prom_component_rpc.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-comp-rpc"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    # Dashboard: Device Drivers
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_prom_device_driver.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-dev-drv"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    # Dashboard: Service Handlers
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_prom_service_handler.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-svc-hdlr"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    # Dashboard: Device Execution Details
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_prom_device_exec_details.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-dev-exec"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    # Dashboard: Load Generator Status
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_prom_load_generator.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-loadgen-stats"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    # Dashboard: Load Generator Status
    curl -X POST -H "Content-Type: application/json" -d '@src/webui/grafana_prom_tfs_num_pods.json' \
        ${GRAFANA_URL_UPDATED}/api/dashboards/db
    echo
    DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tfs-num-pods"
    DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
    curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}
    echo

    printf "\n\n"
fi

if [[ "$TFS_COMPONENTS" == *"telemetry"* ]]; then
    echo "Deconfiguring Telemetry Service..."

    # Revert _LOAD_BALANCER_IP_ for the next deployment
    sed -i "s|$LOAD_BALANCER_IP|_LOAD_BALANCER_IP_|g" manifests/telemetryservice.yaml
fi

echo "Pruning Docker Images..."
docker image prune --force
printf "\n\n"

if [ "$DOCKER_BUILD" == "docker buildx build" ]; then
    echo "Pruning Docker Buildx Cache..."
    docker buildx prune --force
    printf "\n\n"
fi
