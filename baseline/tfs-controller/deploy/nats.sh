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

# If not already set, set the namespace where NATS will be deployed.
export NATS_NAMESPACE=${NATS_NAMESPACE:-"nats"}

# If not already set, set the external port NATS Client interface will be exposed to.
export NATS_EXT_PORT_CLIENT=${NATS_EXT_PORT_CLIENT:-"4222"}

# If not already set, set the external port NATS HTTP Mgmt GUI interface will be exposed to.
export NATS_EXT_PORT_HTTP=${NATS_EXT_PORT_HTTP:-"8222"}

# If not already set, set NATS installation mode. Accepted values are: 'single' and 'cluster'.
# - If NATS_DEPLOY_MODE is "single", NATS is deployed in single node mode. It is convenient for
#   development and testing purposes and should fit in a VM. IT SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS.
# - If NATS_DEPLOY_MODE is "cluster", NATS is deployed in cluster mode, and an entire NATS cluster
#   with 3 replicas (set by default) will be deployed. It is convenient for production and
#   provides scalability features.
export NATS_DEPLOY_MODE=${NATS_DEPLOY_MODE:-"single"}

# If not already set, disable flag for re-deploying NATS from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE MESSAGE BROKER INFORMATION!
# If NATS_REDEPLOY is "YES", the message broker will be dropped while checking/deploying NATS.
export NATS_REDEPLOY=${NATS_REDEPLOY:-""}


########################################################################################################################
# Automated steps start here
########################################################################################################################

# Constants
TMP_FOLDER="./tmp"
NATS_MANIFESTS_PATH="manifests/nats"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="${TMP_FOLDER}/${NATS_NAMESPACE}/manifests"
mkdir -p $TMP_MANIFESTS_FOLDER

function nats_deploy_single() {
    echo "NATS Namespace"
    echo ">>> Create NATS Namespace (if missing)"
    kubectl create namespace ${NATS_NAMESPACE}
    echo

    echo "Add NATS Helm Chart"
    helm3 repo add nats https://nats-io.github.io/k8s/helm/charts/
    echo

    echo "Install NATS (single-mode)"
    echo ">>> Checking if NATS is deployed..."
    if kubectl get --namespace ${NATS_NAMESPACE} statefulset/${NATS_NAMESPACE} &> /dev/null; then
        echo ">>> NATS is present; skipping step."
    else
        echo ">>> Deploy NATS"
        helm3 install ${NATS_NAMESPACE} nats/nats --namespace ${NATS_NAMESPACE} --set nats.image=nats:2.9-alpine

        echo ">>> Waiting NATS statefulset to be created..."
        while ! kubectl get --namespace ${NATS_NAMESPACE} statefulset/${NATS_NAMESPACE} &> /dev/null; do
            printf "%c" "."
            sleep 1
        done

        # Wait for statefulset condition "Available=True" does not work
        # Wait for statefulset condition "jsonpath='{.status.readyReplicas}'=3" throws error:
        #   "error: readyReplicas is not found"
        # Workaround: Check the pods are ready
        #echo ">>> NATS statefulset created. Waiting for readiness condition..."
        #kubectl wait --namespace  ${NATS_NAMESPACE} --for=condition=Available=True --timeout=300s statefulset/nats
        #kubectl wait --namespace ${NATS_NAMESPACE} --for=jsonpath='{.status.readyReplicas}'=3 --timeout=300s \
        #    statefulset/nats
        echo ">>> NATS statefulset created. Waiting NATS pods to be created..."
        while ! kubectl get --namespace ${NATS_NAMESPACE} pod/${NATS_NAMESPACE}-0 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        kubectl wait --namespace ${NATS_NAMESPACE} --for=condition=Ready --timeout=300s pod/${NATS_NAMESPACE}-0
    fi
    echo

    echo "NATS Port Mapping"
    echo ">>> Expose NATS Client port (4222->${NATS_EXT_PORT_CLIENT})"
    NATS_PORT_CLIENT=$(kubectl --namespace ${NATS_NAMESPACE} get service ${NATS_NAMESPACE} -o 'jsonpath={.spec.ports[?(@.name=="client")].port}')
    PATCH='{"data": {"'${NATS_EXT_PORT_CLIENT}'": "'${NATS_NAMESPACE}'/'${NATS_NAMESPACE}':'${NATS_PORT_CLIENT}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${NATS_EXT_PORT_CLIENT}', "hostPort": '${NATS_EXT_PORT_CLIENT}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo

    echo ">>> Expose NATS HTTP Mgmt GUI port (8222->${NATS_EXT_PORT_HTTP})"
    NATS_PORT_HTTP=$(kubectl --namespace ${NATS_NAMESPACE} get service ${NATS_NAMESPACE} -o 'jsonpath={.spec.ports[?(@.name=="monitor")].port}')
    PATCH='{"data": {"'${NATS_EXT_PORT_HTTP}'": "'${NATS_NAMESPACE}'/'${NATS_NAMESPACE}':'${NATS_PORT_HTTP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${NATS_EXT_PORT_HTTP}', "hostPort": '${NATS_EXT_PORT_HTTP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo
}


function nats_deploy_cluster() {
    echo "NATS Namespace"
    echo ">>> Create NATS Namespace (if missing)"
    kubectl create namespace ${NATS_NAMESPACE}
    echo

    echo "Add NATS Helm Chart"
    helm3 repo add nats https://nats-io.github.io/k8s/helm/charts/
    echo

    echo "Upgrade NATS Helm Chart"
    helm3 repo update nats
    echo

    echo "Install NATS (cluster-mode)"
    echo ">>> Checking if NATS is deployed..."
    if kubectl get --namespace ${NATS_NAMESPACE} statefulset/${NATS_NAMESPACE} &> /dev/null; then
        echo ">>> NATS is present; skipping step."
    else
        echo ">>> Deploy NATS"
        cp "${NATS_MANIFESTS_PATH}/cluster.yaml" "${TMP_MANIFESTS_FOLDER}/nats_cluster.yaml"
        helm3 install ${NATS_NAMESPACE} nats/nats --namespace ${NATS_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/nats_cluster.yaml"
    
        echo ">>> Waiting NATS statefulset to be created..."
        while ! kubectl get --namespace ${NATS_NAMESPACE} statefulset/${NATS_NAMESPACE} &> /dev/null; do
            printf "%c" "."
            sleep 1
        done

        # Wait for statefulset condition "Available=True" does not work
        # Wait for statefulset condition "jsonpath='{.status.readyReplicas}'=3" throws error:
        #   "error: readyReplicas is not found"
        # Workaround: Check the pods are ready
        #echo ">>> NATS statefulset created. Waiting for readiness condition..."
        #kubectl wait --namespace  ${NATS_NAMESPACE} --for=condition=Available=True --timeout=300s statefulset/nats
        #kubectl wait --namespace ${NATS_NAMESPACE} --for=jsonpath='{.status.readyReplicas}'=3 --timeout=300s \
        #    statefulset/nats
        echo ">>> NATS statefulset created. Waiting NATS pods to be created..."
        while ! kubectl get --namespace ${NATS_NAMESPACE} pod/${NATS_NAMESPACE}-0 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        while ! kubectl get --namespace ${NATS_NAMESPACE} pod/${NATS_NAMESPACE}-1 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        while ! kubectl get --namespace ${NATS_NAMESPACE} pod/${NATS_NAMESPACE}-2 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        kubectl wait --namespace ${NATS_NAMESPACE} --for=condition=Ready --timeout=300s pod/${NATS_NAMESPACE}-0
        kubectl wait --namespace ${NATS_NAMESPACE} --for=condition=Ready --timeout=300s pod/${NATS_NAMESPACE}-1
        kubectl wait --namespace ${NATS_NAMESPACE} --for=condition=Ready --timeout=300s pod/${NATS_NAMESPACE}-2
    fi
    echo

    echo "NATS Port Mapping"
    echo ">>> Expose NATS Client port (4222->${NATS_EXT_PORT_CLIENT})"
    NATS_PORT_CLIENT=$(kubectl --namespace ${NATS_NAMESPACE} get service ${NATS_NAMESPACE} -o 'jsonpath={.spec.ports[?(@.name=="client")].port}')
    if [ -z "$NATS_PORT_CLIENT" ]; then
        # NATS charts updated and port name changed from "client" to "nats"; fix to support new name and enable backward compatibility
        NATS_PORT_CLIENT=$(kubectl --namespace ${NATS_NAMESPACE} get service ${NATS_NAMESPACE} -o 'jsonpath={.spec.ports[?(@.name=="nats")].port}')
    fi
    PATCH='{"data": {"'${NATS_EXT_PORT_CLIENT}'": "'${NATS_NAMESPACE}'/'${NATS_NAMESPACE}':'${NATS_PORT_CLIENT}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${NATS_EXT_PORT_CLIENT}', "hostPort": '${NATS_EXT_PORT_CLIENT}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo

    echo ">>> Expose NATS HTTP Mgmt GUI port (8222->${NATS_EXT_PORT_HTTP})"
    NATS_PORT_HTTP=$(kubectl --namespace ${NATS_NAMESPACE} get service ${NATS_NAMESPACE} -o 'jsonpath={.spec.ports[?(@.name=="monitor")].port}')
    PATCH='{"data": {"'${NATS_EXT_PORT_HTTP}'": "'${NATS_NAMESPACE}'/'${NATS_NAMESPACE}':'${NATS_PORT_HTTP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${NATS_EXT_PORT_HTTP}', "hostPort": '${NATS_EXT_PORT_HTTP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo
}

function nats_undeploy() {
    echo "NATS"
    echo ">>> Checking if NATS is deployed..."
    if kubectl get --namespace ${NATS_NAMESPACE} statefulset/${NATS_NAMESPACE} &> /dev/null; then
        echo ">>> Undeploy NATS"
        helm3 uninstall --namespace ${NATS_NAMESPACE} ${NATS_NAMESPACE}
    else
        echo ">>> NATS is not present; skipping step."
    fi
    echo

    echo "NATS Namespace"
    echo ">>> Delete NATS Namespace (if exists)"
    kubectl delete namespace ${NATS_NAMESPACE} --ignore-not-found
    echo
}

if [ "$NATS_REDEPLOY" == "YES" ]; then
    nats_undeploy
fi

if [ "$NATS_DEPLOY_MODE" == "single" ]; then
    nats_deploy_single
elif [ "$NATS_DEPLOY_MODE" == "cluster" ]; then
    nats_deploy_cluster
else
    echo "Unsupported value: NATS_DEPLOY_MODE=$NATS_DEPLOY_MODE"
fi