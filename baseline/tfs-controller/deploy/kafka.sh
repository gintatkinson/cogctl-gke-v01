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

# If not already set, set the namespace where Kafka will be deployed.
export KFK_NAMESPACE=${KFK_NAMESPACE:-"kafka"}

# If not already set, set the external port Kafka client interface will be exposed to.
export KFK_EXT_PORT_CLIENT=${KFK_EXT_PORT_CLIENT:-"9092"}

# If not already set, set Kafka installation mode. Accepted values are: 'single'.
# - If KFK_DEPLOY_MODE is "single", Kafka is deployed in single node mode. It is convenient for
#   development and testing purposes and should fit in a VM. IT SHOULD NOT BE USED IN PRODUCTION ENVIRONMENTS.
# NOTE: Production mode is still not supported. Will be provided in the future.
export KFK_DEPLOY_MODE=${KFK_DEPLOY_MODE:-"single"}

# If not already set, disable flag for re-deploying Kafka from scratch.
# WARNING: ACTIVATING THIS FLAG IMPLIES LOOSING THE MESSAGE BROKER INFORMATION!
# If KFK_REDEPLOY is "YES", the message broker will be dropped while checking/deploying Kafka.
export KFK_REDEPLOY=${KFK_REDEPLOY:-""}


########################################################################################################################
# Automated steps start here
########################################################################################################################

# Constants
TMP_FOLDER="./tmp"
KFK_MANIFESTS_PATH="manifests/kafka"

# Create a tmp folder for files modified during the deployment
TMP_MANIFESTS_FOLDER="${TMP_FOLDER}/${KFK_NAMESPACE}/manifests"
mkdir -p ${TMP_MANIFESTS_FOLDER}

function kfk_deploy_single() {
    echo "Kafka Namespace"
    echo ">>> Create Kafka Namespace (if missing)"
    kubectl create namespace ${KFK_NAMESPACE}
    echo

    echo "Kafka (single-mode)"
    echo ">>> Checking if Kafka is deployed..."
    if kubectl get --namespace ${KFK_NAMESPACE} statefulset/kafka &> /dev/null; then
        echo ">>> Kafka is present; skipping step."
    else
        echo ">>> Deploy Kafka"
        cp "${KFK_MANIFESTS_PATH}/single-node.yaml" "${TMP_MANIFESTS_FOLDER}/kfk_single_node.yaml"
        #sed -i "s/<KFK_NAMESPACE>/${KFK_NAMESPACE}/" "${TMP_MANIFESTS_FOLDER}/kfk_single_node.yaml"
        kubectl --namespace ${KFK_NAMESPACE} apply -f "${TMP_MANIFESTS_FOLDER}/kfk_single_node.yaml"

        echo ">>> Waiting Kafka statefulset to be created..."
        while ! kubectl get --namespace ${KFK_NAMESPACE} statefulset/kafka &> /dev/null; do
            printf "%c" "."
            sleep 1
        done

        # Wait for statefulset condition "Available=True" does not work
        # Wait for statefulset condition "jsonpath='{.status.readyReplicas}'=3" throws error:
        #   "error: readyReplicas is not found"
        # Workaround: Check the pods are ready
        #echo ">>> Kafka statefulset created. Waiting for readiness condition..."
        #kubectl wait --namespace  ${KFK_NAMESPACE} --for=condition=Available=True --timeout=300s statefulset/kafka
        #kubectl wait --namespace ${KGK_NAMESPACE} --for=jsonpath='{.status.readyReplicas}'=3 --timeout=300s \
        #    statefulset/kafka
        echo ">>> Kafka statefulset created. Waiting Kafka pods to be created..."
        while ! kubectl get --namespace ${KFK_NAMESPACE} pod/kafka-0 &> /dev/null; do
            printf "%c" "."
            sleep 1
        done
        kubectl wait --namespace ${KFK_NAMESPACE} --for=condition=Ready --timeout=300s pod/kafka-0

        # Wait for Kafka to notify "Kafka Server started"
        echo ">>> Kafka pods created. Waiting Kafka Server to be started..."
        while ! kubectl --namespace ${KFK_NAMESPACE} logs pod/kafka-0 -c kafka 2>&1 | grep -q 'Kafka Server started'; do
            printf "%c" "."
            sleep 1
        done
    fi
    echo
}


function kfk_undeploy_single() {
    echo "Kafka (single-mode)"
    echo ">>> Checking if Kafka is deployed..."
    if kubectl get --namespace ${KFK_NAMESPACE} statefulset/kafka &> /dev/null; then
        echo ">>> Undeploy Kafka"
        kubectl delete --namespace ${KFK_NAMESPACE} -f "${TMP_MANIFESTS_FOLDER}/kfk_single_node.yaml" --ignore-not-found
    else
        echo ">>> Kafka is not present; skipping step."
    fi
    echo

    echo "Kafka Namespace"
    echo ">>> Delete Kafka Namespace (if exists)"
    echo "NOTE: this step might take few minutes to complete!"
    kubectl delete namespace ${KFK_NAMESPACE} --ignore-not-found
    echo
}

if [ "$KFK_DEPLOY_MODE" == "single" ]; then
    if [ "$KFK_REDEPLOY" == "YES" ]; then
        kfk_undeploy_single
    fi

    kfk_deploy_single
else
    echo "Unsupported value: KFK_DEPLOY_MODE=$KFK_DEPLOY_MODE"
fi
