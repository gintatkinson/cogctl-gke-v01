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

# If not already set, set the namespace where CockroackDB will be deployed.
export CRDB_NAMESPACE=${CRDB_NAMESPACE:-"crdb"}

# If not already set, set the external port CockroackDB Postgre SQL interface will be exposed to.
export CRDB_EXT_PORT_SQL=${CRDB_EXT_PORT_SQL:-"26257"}

# If not already set, set the external port CockroackDB HTTP Mgmt GUI interface will be exposed to.
export CRDB_EXT_PORT_HTTP=${CRDB_EXT_PORT_HTTP:-"8081"}

# If not already set, set the database username to be used by Context.
export CRDB_USERNAME=${CRDB_USERNAME:-"tfs"}

# If not already set, set the database user's password to be used by Context.
export CRDB_PASSWORD=${CRDB_PASSWORD:-"tfs123"}

# If not already set, set CockroachDB installation mode. Accepted values are: 'single' and 'cluster'.
# - If CRDB_DEPLOY_MODE is "single", CockroachDB is deployed in single node mode. It is convenient for
#   development and testing purposes and should fit in a VM. IT SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS.
# - If CRDB_DEPLOY_MODE is "cluster", CockroachDB is deployed in cluster mode, and an entire CockroachDB cluster
#   with 3 replicas and version v22.2 (set by default) will be deployed. It is convenient for production and
#   provides scalability features. If you are deploying for production, also read the following link providing
#   details on deploying CockroachDB for production environments:
#   Ref: https://www.cockroachlabs.com/docs/stable/recommended-production-settings.html
export CRDB_DEPLOY_MODE=${CRDB_DEPLOY_MODE:-"single"}

# If not already set, disable flag for dropping database, if it exists.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE DATABASE INFORMATION!
# If CRDB_DROP_DATABASE_IF_EXISTS is "YES", the databases starting with "tfs_" will be dropped while
# checking/deploying CockroachDB.
export CRDB_DROP_DATABASE_IF_EXISTS=${CRDB_DROP_DATABASE_IF_EXISTS:-""}

# If not already set, disable flag for re-deploying CockroachDB from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE DATABASE INFORMATION!
# WARNING: THE REDEPLOY MIGHT TAKE FEW MINUTES TO COMPLETE GRACEFULLY IN CLUSTER MODE
# If CRDB_REDEPLOY is "YES", the database will be dropped while checking/deploying CockroachDB.
export CRDB_REDEPLOY=${CRDB_REDEPLOY:-""}


########################################################################################################################
# Automated steps start here
########################################################################################################################

# Constants
TMP_FOLDER="./tmp"
CRDB_MANIFESTS_PATH="manifests/cockroachdb"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="${TMP_FOLDER}/${CRDB_NAMESPACE}/manifests"
mkdir -p ${TMP_MANIFESTS_FOLDER}

function crdb_deploy_single() {
    echo "CockroachDB Namespace"
    echo ">>> Create CockroachDB Namespace (if missing)"
    kubectl create namespace ${CRDB_NAMESPACE}
    echo

    echo "CockroachDB (single-mode)"
    echo ">>> Checking if CockroachDB is deployed..."
    if kubectl get --namespace ${CRDB_NAMESPACE} statefulset/cockroachdb &> /dev/null; then
        echo ">>> CockroachDB is present; skipping step."
    else
        echo ">>> Deploy CockroachDB"
        cp "${CRDB_MANIFESTS_PATH}/single-node.yaml" "${TMP_MANIFESTS_FOLDER}/crdb_single_node.yaml"
        sed -i "s/%CRDB_USERNAME%/${CRDB_USERNAME}/g" "${TMP_MANIFESTS_FOLDER}/crdb_single_node.yaml"
        sed -i "s/%CRDB_PASSWORD%/${CRDB_PASSWORD}/g" "${TMP_MANIFESTS_FOLDER}/crdb_single_node.yaml"
        kubectl apply --namespace ${CRDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/crdb_single_node.yaml"

        echo ">>> Waiting CockroachDB statefulset to be created..."
        while ! kubectl get --namespace ${CRDB_NAMESPACE} statefulset/cockroachdb &> /dev/null; do
            printf "%c" "."
            sleep 1
        done

        # Wait for statefulset condition "Available=True" does not work
        # Wait for statefulset condition "jsonpath='{.status.readyReplicas}'=3" throws error:
        #   "error: readyReplicas is not found"
        # Workaround: Check the pods are ready
        #echo ">>> CockroachDB statefulset created. Waiting for readiness condition..."
        #kubectl wait --namespace  ${CRDB_NAMESPACE} --for=condition=Available=True --timeout=300s statefulset/cockroachdb
        #kubectl wait --namespace ${CRDB_NAMESPACE} --for=jsonpath='{.status.readyReplicas}'=3 --timeout=300s \
        #    statefulset/cockroachdb
        echo ">>> CockroachDB statefulset created. Waiting CockroachDB pods to be created..."
        while ! kubectl get --namespace ${CRDB_NAMESPACE} pod/cockroachdb-0 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        kubectl wait --namespace ${CRDB_NAMESPACE} --for=condition=Ready --timeout=300s pod/cockroachdb-0

        # Wait for CockroachDB to notify "start_node_query"
        echo ">>> CockroachDB pods created. Waiting CockroachDB server to be started..."
        while ! kubectl --namespace ${CRDB_NAMESPACE} logs pod/cockroachdb-0 -c cockroachdb 2>&1 | grep -q 'start_node_query'; do
            printf "%c" "."
            sleep 1
        done
    fi
    echo

    echo "CockroachDB Port Mapping"
    echo ">>> Expose CockroachDB SQL port (26257->${CRDB_EXT_PORT_SQL})"
    CRDB_PORT_SQL=$(kubectl --namespace ${CRDB_NAMESPACE} get service cockroachdb-public -o 'jsonpath={.spec.ports[?(@.name=="sql")].port}')
    PATCH='{"data": {"'${CRDB_EXT_PORT_SQL}'": "'${CRDB_NAMESPACE}'/cockroachdb-public:'${CRDB_PORT_SQL}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${CRDB_EXT_PORT_SQL}', "hostPort": '${CRDB_EXT_PORT_SQL}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo

    echo ">>> Expose CockroachDB HTTP Mgmt GUI port (8080->${CRDB_EXT_PORT_HTTP})"
    CRDB_PORT_HTTP=$(kubectl --namespace ${CRDB_NAMESPACE} get service cockroachdb-public -o 'jsonpath={.spec.ports[?(@.name=="http")].port}')
    PATCH='{"data": {"'${CRDB_EXT_PORT_HTTP}'": "'${CRDB_NAMESPACE}'/cockroachdb-public:'${CRDB_PORT_HTTP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${CRDB_EXT_PORT_HTTP}', "hostPort": '${CRDB_EXT_PORT_HTTP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo
}

function crdb_undeploy_single() {
    echo "CockroachDB (single-mode)"
    echo ">>> Checking if CockroachDB is deployed..."
    if kubectl get --namespace ${CRDB_NAMESPACE} statefulset/cockroachdb &> /dev/null; then
        echo ">>> Undeploy CockroachDB"
        kubectl delete --namespace ${CRDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/crdb_single_node.yaml" --ignore-not-found
    else
        echo ">>> CockroachDB is not present; skipping step."
    fi
    echo

    echo "CockroachDB Namespace"
    echo ">>> Delete CockroachDB Namespace (if exists)"
    echo "NOTE: this step might take few minutes to complete!"
    kubectl delete namespace ${CRDB_NAMESPACE} --ignore-not-found
    echo
}

function crdb_drop_databases_single() {
    echo "Drop TFS databases, if exist"

    CRDB_PORT=$(kubectl --namespace ${CRDB_NAMESPACE} get service cockroachdb-public -o 'jsonpath={.spec.ports[?(@.name=="sql")].port}')
    CRDB_CLIENT_URL="postgresql://${CRDB_USERNAME}:${CRDB_PASSWORD}@cockroachdb-0:${CRDB_PORT}/defaultdb?sslmode=require"
    echo "CRDB_CLIENT_URL=${CRDB_CLIENT_URL}"

    DATABASES=$(
        kubectl exec -i --namespace ${CRDB_NAMESPACE} cockroachdb-0 -- \
            ./cockroach sql --certs-dir=/cockroach/cockroach-certs --url=${CRDB_CLIENT_URL} \
            --execute "SHOW DATABASES;" --format=tsv | awk '{print $1}' | grep "^tfs"
    )
    echo "Found TFS databases: ${DATABASES}" | tr '\n' ' '
    echo

    for DB_NAME in $DATABASES; do
        echo "Dropping TFS database: $DB_NAME"
        kubectl exec -i --namespace ${CRDB_NAMESPACE} cockroachdb-0 -- \
            ./cockroach sql --certs-dir=/cockroach/cockroach-certs --url=${CRDB_CLIENT_URL} \
            --execute="DROP DATABASE IF EXISTS $DB_NAME CASCADE;"
    done
    echo
}

function crdb_deploy_cluster() {
    echo "CockroachDB Operator Namespace"
    echo ">>> Create CockroachDB Operator Namespace (if missing)"
    kubectl apply -f "${CRDB_MANIFESTS_PATH}/pre_operator.yaml"
    echo

    echo "Cockroach Operator CRDs"
    echo ">>> Apply Cockroach Operator CRDs (if they are missing)"
    cp "${CRDB_MANIFESTS_PATH}/crds.yaml" "${TMP_MANIFESTS_FOLDER}/crdb_crds.yaml"
    kubectl apply -f "${TMP_MANIFESTS_FOLDER}/crdb_crds.yaml"
    echo

    echo "Cockroach Operator"
    echo ">>> Checking if Cockroach Operator is deployed..."
    if kubectl get --namespace cockroach-operator-system deployment/cockroach-operator-manager &> /dev/null; then
        echo ">>> Cockroach Operator is present; skipping step."
    else
        echo ">>> Deploy Cockroach Operator"
        sed "s/%TFS_CRDB_NAMESPACE%/${CRDB_NAMESPACE}/g" "${CRDB_MANIFESTS_PATH}/operator.yaml" \
            > "${TMP_MANIFESTS_FOLDER}/crdb_operator.yaml"
        kubectl apply -f "${TMP_MANIFESTS_FOLDER}/crdb_operator.yaml"
        kubectl wait --namespace cockroach-operator-system --for=condition=Available=True --timeout=300s \
            deployment/cockroach-operator-manager
        #kubectl wait --namespace cockroach-operator-system --for=jsonpath='{.status.readyReplicas}'=1 --timeout=300s \
        #    deployment/cockroach-operator-manager

        echo ">>> Waiting for Cockroach Operator Webhock service..."
        while ! kubectl get service cockroach-operator-webhook-service --namespace cockroach-operator-system &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        WEBHOOK_SERVICE_DATA=$(kubectl get service cockroach-operator-webhook-service --namespace cockroach-operator-system -o json)
        WEBHOOK_SERVICE_HOST=$(echo ${WEBHOOK_SERVICE_DATA} | jq -r '.spec.clusterIP')
        WEBHOOK_SERVICE_PORT=$(echo ${WEBHOOK_SERVICE_DATA} | jq -r '.spec.ports[] | select(.targetPort==9443) | .port')
        WEBHOOK_URL="https://${WEBHOOK_SERVICE_HOST}:${WEBHOOK_SERVICE_PORT}/mutate-crdb-cockroachlabs-com-v1alpha1-crdbcluster?timeout=10s"
        while ! curl --insecure --header 'Content-Type: application/json' ${WEBHOOK_URL} &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
    fi
    echo

    echo "CockroachDB Namespace"
    echo ">>> Create CockroachDB Namespace (if missing)"
    kubectl create namespace ${CRDB_NAMESPACE}
    echo

    echo "CockroachDB (cluster-mode)"
    echo ">>> Checking if CockroachDB is deployed..."
    if kubectl get --namespace ${CRDB_NAMESPACE} statefulset/cockroachdb &> /dev/null; then
        echo ">>> CockroachDB is present; skipping step."
    else
        echo ">>> Deploy CockroachDB"
        cp "${CRDB_MANIFESTS_PATH}/cluster.yaml" "${TMP_MANIFESTS_FOLDER}/crdb_cluster.yaml"
        kubectl apply --namespace ${CRDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/crdb_cluster.yaml"

        echo ">>> Waiting CockroachDB statefulset to be created..."
        while ! kubectl get --namespace ${CRDB_NAMESPACE} statefulset/cockroachdb &> /dev/null; do
            printf "%c" "."
            sleep 1
        done

        # Wait for statefulset condition "Available=True" does not work
        # Wait for statefulset condition "jsonpath='{.status.readyReplicas}'=3" throws error:
        #   "error: readyReplicas is not found"
        # Workaround: Check the pods are ready
        #echo ">>> CockroachDB statefulset created. Waiting for readiness condition..."
        #kubectl wait --namespace  ${CRDB_NAMESPACE} --for=condition=Available=True --timeout=300s statefulset/cockroachdb
        #kubectl wait --namespace ${CRDB_NAMESPACE} --for=jsonpath='{.status.readyReplicas}'=3 --timeout=300s \
        #    statefulset/cockroachdb
        echo ">>> CockroachDB statefulset created. Waiting CockroachDB pods to be created..."
        while ! kubectl get --namespace ${CRDB_NAMESPACE} pod/cockroachdb-0 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        while ! kubectl get --namespace ${CRDB_NAMESPACE} pod/cockroachdb-1 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        while ! kubectl get --namespace ${CRDB_NAMESPACE} pod/cockroachdb-2 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        kubectl wait --namespace ${CRDB_NAMESPACE} --for=condition=Ready --timeout=300s pod/cockroachdb-0
        kubectl wait --namespace ${CRDB_NAMESPACE} --for=condition=Ready --timeout=300s pod/cockroachdb-1
        kubectl wait --namespace ${CRDB_NAMESPACE} --for=condition=Ready --timeout=300s pod/cockroachdb-2
    fi
    echo

    echo "CockroachDB Client"
    echo ">>> Checking if CockroachDB Client is deployed..."
    if kubectl get --namespace ${CRDB_NAMESPACE} pod/cockroachdb-client-secure &> /dev/null; then
        echo ">>> CockroachDB Client is present; skipping step."
    else
        echo ">>> Deploy CockroachDB Client"
        cp "${CRDB_MANIFESTS_PATH}/client-secure-operator.yaml" "${TMP_MANIFESTS_FOLDER}/crdb_client-secure-operator.yaml"
        kubectl create --namespace ${CRDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/crdb_client-secure-operator.yaml"
        kubectl wait --namespace ${CRDB_NAMESPACE} --for=condition=Ready --timeout=300s pod/cockroachdb-client-secure
    fi
    echo

    echo "Add tfs user and grant admin rights"
    kubectl exec -it cockroachdb-client-secure --namespace ${CRDB_NAMESPACE} -- \
        ./cockroach sql --certs-dir=/cockroach/cockroach-certs --host=cockroachdb-public --execute \
        "CREATE USER ${CRDB_USERNAME} WITH PASSWORD '${CRDB_PASSWORD}'; GRANT admin TO ${CRDB_USERNAME};"
    echo

    echo "CockroachDB Port Mapping"
    echo ">>> Expose CockroachDB SQL port (26257->${CRDB_EXT_PORT_SQL})"
    CRDB_PORT_SQL=$(kubectl --namespace ${CRDB_NAMESPACE} get service cockroachdb-public -o 'jsonpath={.spec.ports[?(@.name=="sql")].port}')
    PATCH='{"data": {"'${CRDB_EXT_PORT_SQL}'": "'${CRDB_NAMESPACE}'/cockroachdb-public:'${CRDB_PORT_SQL}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${CRDB_EXT_PORT_SQL}', "hostPort": '${CRDB_EXT_PORT_SQL}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo

    echo ">>> Expose CockroachDB HTTP Mgmt GUI port (8080->${CRDB_EXT_PORT_HTTP})"
    CRDB_PORT_HTTP=$(kubectl --namespace ${CRDB_NAMESPACE} get service cockroachdb-public -o 'jsonpath={.spec.ports[?(@.name=="http")].port}')
    PATCH='{"data": {"'${CRDB_EXT_PORT_HTTP}'": "'${CRDB_NAMESPACE}'/cockroachdb-public:'${CRDB_PORT_HTTP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${CRDB_EXT_PORT_HTTP}', "hostPort": '${CRDB_EXT_PORT_HTTP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo
}

function crdb_undeploy_cluster() {
    echo "CockroachDB Client"
    echo ">>> Checking if CockroachDB Client is deployed..."
    if kubectl get --namespace ${CRDB_NAMESPACE} pod/cockroachdb-client-secure &> /dev/null; then
        echo ">>> Undeploy CockroachDB Client"
        kubectl delete --namespace ${CRDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/crdb_client-secure-operator.yaml" \
            --ignore-not-found
    else
        echo ">>> CockroachDB Client is not present; skipping step."
    fi
    echo

    echo "CockroachDB (cluster-mode)"
    echo ">>> Checking if CockroachDB is deployed..."
    if kubectl get --namespace ${CRDB_NAMESPACE} statefulset/cockroachdb &> /dev/null; then
        echo ">>> Undeploy CockroachDB"
        kubectl delete --namespace ${CRDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/crdb_cluster.yaml" --ignore-not-found
    else
        echo ">>> CockroachDB is not present; skipping step."
    fi
    echo

    echo "CockroachDB Namespace"
    echo ">>> Delete CockroachDB Namespace (if exists)"
    echo "NOTE: this step might take few minutes to complete!"
    kubectl delete namespace ${CRDB_NAMESPACE} --ignore-not-found
    echo

    echo "CockroachDB Operator"
    echo ">>> Checking if CockroachDB Operator is deployed..."
    if kubectl get --namespace cockroach-operator-system deployment/cockroach-operator-manager &> /dev/null; then
        echo ">>> Undeploy CockroachDB Operator"
        kubectl delete -f "${TMP_MANIFESTS_FOLDER}/crdb_operator.yaml" --ignore-not-found
    else
        echo ">>> CockroachDB Operator is not present; skipping step."
    fi
    echo

    echo "CockroachDB Operator CRDs"
    echo ">>> Delete CockroachDB Operator CRDs (if they exist)"
    kubectl delete -f "${TMP_MANIFESTS_FOLDER}/crdb_crds.yaml" --ignore-not-found
    echo
}

function crdb_drop_databases_cluster() {
    echo "Drop TFS databases, if exist"

    DATABASES=$(
        kubectl exec -i --namespace ${CRDB_NAMESPACE} cockroachdb-client-secure -- \
            ./cockroach sql --certs-dir=/cockroach/cockroach-certs --host=cockroachdb-public \
            --execute "SHOW DATABASES;" --format=tsv | awk '{print $1}' | grep "^tfs"
    )
    echo "Found TFS databases: ${DATABASES}" | tr '\n' ' '
    echo

    for DB_NAME in $DATABASES; do
        echo "Dropping TFS database: $DB_NAME"
        kubectl exec -i --namespace ${CRDB_NAMESPACE} cockroachdb-client-secure -- \
            ./cockroach sql --certs-dir=/cockroach/cockroach-certs --host=cockroachdb-public \
            --execute="DROP DATABASE IF EXISTS $DB_NAME CASCADE;"
    done
    echo
}

if [ "$CRDB_DEPLOY_MODE" == "single" ]; then
    if [ "$CRDB_REDEPLOY" == "YES" ]; then
        crdb_undeploy_single
    fi

    crdb_deploy_single
    sleep 3

    if [ "$CRDB_DROP_DATABASE_IF_EXISTS" == "YES" ]; then
        crdb_drop_databases_single
    fi
elif [ "$CRDB_DEPLOY_MODE" == "cluster" ]; then
    if [ "$CRDB_REDEPLOY" == "YES" ]; then
        crdb_undeploy_cluster
    fi

    crdb_deploy_cluster
    sleep 3

    if [ "$CRDB_DROP_DATABASE_IF_EXISTS" == "YES" ]; then
        crdb_drop_databases_cluster
    fi
else
    echo "Unsupported value: CRDB_DEPLOY_MODE=$CRDB_DEPLOY_MODE"
fi
