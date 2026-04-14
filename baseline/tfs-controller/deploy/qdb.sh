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

# If not already set, set the namespace where QuestDB will be deployed.
export QDB_NAMESPACE=${QDB_NAMESPACE:-"qdb"}

# If not already set, set the external port QuestDB Postgre SQL interface will be exposed to.
export QDB_EXT_PORT_SQL=${QDB_EXT_PORT_SQL:-"8812"}

# If not already set, set the external port QuestDB Influx Line Protocol interface will be exposed to.
export QDB_EXT_PORT_ILP=${QDB_EXT_PORT_ILP:-"9009"}

# If not already set, set the external port QuestDB HTTP Mgmt GUI interface will be exposed to.
export QDB_EXT_PORT_HTTP=${QDB_EXT_PORT_HTTP:-"9000"}

# If not already set, set the database username to be used for QuestDB.
export QDB_USERNAME=${QDB_USERNAME:-"admin"}

# If not already set, set the database user's password to be used for QuestDB.
export QDB_PASSWORD=${QDB_PASSWORD:-"quest"}

# If not already set, set the table name to be used by Monitoring for KPIs.
export QDB_TABLE_MONITORING_KPIS=${QDB_TABLE_MONITORING_KPIS:-"tfs_monitoring_kpis"}

# If not already set, set the table name to be used by Slice for plotting groups.
export QDB_TABLE_SLICE_GROUPS=${QDB_TABLE_SLICE_GROUPS:-"tfs_slice_groups"}

# If not already set, disable flag for dropping tables if they exist.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE TABLE INFORMATION!
# If QDB_DROP_TABLES_IF_EXIST is "YES", the tables pointed by variables
# QDB_TABLE_MONITORING_KPIS and QDB_TABLE_SLICE_GROUPS will be dropped
# while checking/deploying QuestDB.
export QDB_DROP_TABLES_IF_EXIST=${QDB_DROP_TABLES_IF_EXIST:-""}

# If not already set, disable flag for re-deploying QuestDB from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE DATABASE INFORMATION!
# If QDB_REDEPLOY is "YES", the database will be dropped while checking/deploying QuestDB.
export QDB_REDEPLOY=${QDB_REDEPLOY:-""}


########################################################################################################################
# Automated steps start here
########################################################################################################################

# Constants
TMP_FOLDER="./tmp"
QDB_MANIFESTS_PATH="manifests/questdb"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="${TMP_FOLDER}/${QDB_NAMESPACE}/manifests"
mkdir -p $TMP_MANIFESTS_FOLDER

function qdb_deploy() {
    echo "QuestDB Namespace"
    echo ">>> Create QuestDB Namespace (if missing)"
    kubectl create namespace ${QDB_NAMESPACE}
    sleep 2
    echo

    echo "QuestDB"
    echo ">>> Checking if QuestDB is deployed..."
    if kubectl get --namespace ${QDB_NAMESPACE} statefulset/questdb &> /dev/null; then
        echo ">>> QuestDB is present; skipping step."
    else
        echo ">>> Deploy QuestDB"
        cp "${QDB_MANIFESTS_PATH}/manifest.yaml" "${TMP_MANIFESTS_FOLDER}/qdb_manifest.yaml"
        kubectl apply --namespace ${QDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/qdb_manifest.yaml"

        echo ">>> Waiting QuestDB statefulset to be created..."
        while ! kubectl get --namespace ${QDB_NAMESPACE} statefulset/questdb &> /dev/null; do
            printf "%c" "."
            sleep 1
        done

        # Wait for statefulset condition "Available=True" does not work
        # Wait for statefulset condition "jsonpath='{.status.readyReplicas}'=3" throws error:
        #   "error: readyReplicas is not found"
        # Workaround: Check the pods are ready
        #echo ">>> QuestDB statefulset created. Waiting for readiness condition..."
        #kubectl wait --namespace  ${QDB_NAMESPACE} --for=condition=Available=True --timeout=300s statefulset/questdb
        #kubectl wait --namespace ${QDB_NAMESPACE} --for=jsonpath='{.status.readyReplicas}'=3 --timeout=300s \
        #    statefulset/questdb
        echo ">>> QuestDB statefulset created. Waiting QuestDB pods to be created..."
        while ! kubectl get --namespace ${QDB_NAMESPACE} pod/questdb-0 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        kubectl wait --namespace ${QDB_NAMESPACE} --for=condition=Ready --timeout=300s pod/questdb-0
    fi
    echo

    echo "QuestDB Port Mapping"
    echo ">>> Expose QuestDB SQL port (8812->${QDB_EXT_PORT_SQL})"
    QDB_PORT_SQL=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.ports[?(@.name=="sql")].port}')
    PATCH='{"data": {"'${QDB_EXT_PORT_SQL}'": "'${QDB_NAMESPACE}'/questdb-public:'${QDB_PORT_SQL}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${QDB_EXT_PORT_SQL}', "hostPort": '${QDB_EXT_PORT_SQL}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo

    echo ">>> Expose QuestDB Influx Line Protocol port (9009->${QDB_EXT_PORT_ILP})"
    QDB_PORT_ILP=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.ports[?(@.name=="ilp")].port}')
    PATCH='{"data": {"'${QDB_EXT_PORT_ILP}'": "'${QDB_NAMESPACE}'/questdb-public:'${QDB_PORT_ILP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${QDB_EXT_PORT_ILP}', "hostPort": '${QDB_EXT_PORT_ILP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo

    echo ">>> Expose QuestDB HTTP Mgmt GUI port (9000->${QDB_EXT_PORT_HTTP})"
    QDB_PORT_HTTP=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.ports[?(@.name=="http")].port}')
    PATCH='{"data": {"'${QDB_EXT_PORT_HTTP}'": "'${QDB_NAMESPACE}'/questdb-public:'${QDB_PORT_HTTP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${QDB_EXT_PORT_HTTP}', "hostPort": '${QDB_EXT_PORT_HTTP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo
}

function qdb_undeploy() {
    echo "QuestDB"
    echo ">>> Checking if QuestDB is deployed..."
    if kubectl get --namespace ${QDB_NAMESPACE} statefulset/questdb &> /dev/null; then
        echo ">>> Undeploy QuestDB"
        kubectl delete --namespace ${QDB_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/qdb_manifest.yaml" --ignore-not-found
    else
        echo ">>> QuestDB is not present; skipping step."
    fi
    echo

    echo "QuestDB Namespace"
    echo ">>> Delete QuestDB Namespace (if exists)"
    echo "NOTE: this step might take few minutes to complete!"
    kubectl delete namespace ${QDB_NAMESPACE} --ignore-not-found
    echo
}

function qdb_drop_tables() {
    echo "Drop tables, if exist"

    if [[ -z "${GITLAB_CI}" ]]; then
        #kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o yaml
        QDB_HOST=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.clusterIP}')
        QDB_PORT=$(kubectl --namespace ${QDB_NAMESPACE} get service questdb-public -o 'jsonpath={.spec.ports[?(@.name=="http")].port}')
    else
        QDB_HOST="127.0.0.1"
        QDB_PORT=${QDB_EXT_PORT_HTTP}
    fi

    curl "http://${QDB_HOST}:${QDB_PORT}/exec?fmt=json&query=DROP+TABLE+IF+EXISTS+${QDB_TABLE_MONITORING_KPIS}+;"
    echo
    curl "http://${QDB_HOST}:${QDB_PORT}/exec?fmt=json&query=DROP+TABLE+IF+EXISTS+${QDB_TABLE_SLICE_GROUPS}+;"
    echo
}

if [ "$QDB_REDEPLOY" == "YES" ]; then
    qdb_undeploy
fi

qdb_deploy

if [ "$QDB_DROP_TABLES_IF_EXIST" == "YES" ]; then
    qdb_drop_tables
fi
