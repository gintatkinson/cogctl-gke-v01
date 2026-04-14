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

# If not already set, set the name of the Kubernetes namespace to deploy to.
export TFS_K8S_NAMESPACE=${TFS_K8S_NAMESPACE:-"tfs"}

# If not already set, set the list of components you want to build images for, and deploy.
export TFS_COMPONENTS=${TFS_COMPONENTS:-"context device ztp policy service nbi monitoring dbscanserving opticalattackmitigator opticalcentralizedattackdetector l3_attackmitigator l3_centralizedattackdetector webui"}

########################################################################################################################
# Automated steps start here
########################################################################################################################

echo "Exposing GRPC ports for components..."
for COMPONENT in $TFS_COMPONENTS; do
    echo "Processing '$COMPONENT' component..."

    SERVICE_GRPC_PORT=$(kubectl get service ${COMPONENT}service --namespace $TFS_K8S_NAMESPACE -o 'jsonpath={.spec.ports[?(@.name=="grpc")].port}')
    echo "    '$COMPONENT' service port: $SERVICE_GRPC_PORT"
    if [ -z "${SERVICE_GRPC_PORT}" ]; then
        printf "\n"
        continue;
    fi

    COMPONENT_OBJNAME=$(echo "${COMPONENT}" | sed "s/\_/-/")
    PATCH='{"data": {"'${SERVICE_GRPC_PORT}'": "'$TFS_K8S_NAMESPACE'/'${COMPONENT_OBJNAME}service':'${SERVICE_GRPC_PORT}'"}}'
    #echo "PATCH: ${PATCH}"
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${SERVICE_GRPC_PORT}', "hostPort": '${SERVICE_GRPC_PORT}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    #echo "PATCH: ${PATCH}"
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"

    printf "\n"
done

echo "Done!"
