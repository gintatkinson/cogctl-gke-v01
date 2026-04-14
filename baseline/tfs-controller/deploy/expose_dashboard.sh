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

# If not already set, set the external port Prometheus Mgmt HTTP GUI interface will be exposed to.
export PROM_EXT_PORT_HTTP=${PROM_EXT_PORT_HTTP:-"9090"}

# If not already set, set the external port Grafana HTTP Dashboards will be exposed to.
export GRAF_EXT_PORT_HTTP=${GRAF_EXT_PORT_HTTP:-"3000"}


########################################################################################################################
# Automated steps start here
########################################################################################################################

MONITORING_NAMESPACE="monitoring"

function expose_dashboard() {
    echo "Prometheus Port Mapping"
    echo ">>> Expose Prometheus HTTP Mgmt GUI port (9090->${PROM_EXT_PORT_HTTP})"
    PROM_PORT_HTTP=$(kubectl --namespace ${MONITORING_NAMESPACE} get service prometheus-k8s -o 'jsonpath={.spec.ports[?(@.name=="web")].port}')
    PATCH='{"data": {"'${PROM_EXT_PORT_HTTP}'": "'${MONITORING_NAMESPACE}'/prometheus-k8s:'${PROM_PORT_HTTP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${PROM_EXT_PORT_HTTP}', "hostPort": '${PROM_EXT_PORT_HTTP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo

    echo "Grafana Port Mapping"
    echo ">>> Expose Grafana HTTP Mgmt GUI port (3000->${GRAF_EXT_PORT_HTTP})"
    GRAF_PORT_HTTP=$(kubectl --namespace ${MONITORING_NAMESPACE} get service grafana -o 'jsonpath={.spec.ports[?(@.name=="http")].port}')
    PATCH='{"data": {"'${GRAF_EXT_PORT_HTTP}'": "'${MONITORING_NAMESPACE}'/grafana:'${GRAF_PORT_HTTP}'"}}'
    kubectl patch configmap nginx-ingress-tcp-microk8s-conf --namespace ingress --patch "${PATCH}"

    PORT_MAP='{"containerPort": '${GRAF_EXT_PORT_HTTP}', "hostPort": '${GRAF_EXT_PORT_HTTP}'}'
    CONTAINER='{"name": "nginx-ingress-microk8s", "ports": ['${PORT_MAP}']}'
    PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
    kubectl patch daemonset nginx-ingress-microk8s-controller --namespace ingress --patch "${PATCH}"
    echo
}

if kubectl get namespace ${MONITORING_NAMESPACE} &> /dev/null; then
    echo ">>> Namespace ${MONITORING_NAMESPACE} is present, exposing dashboard..."
    expose_dashboard
else
    echo ">>> Namespace ${MONITORING_NAMESPACE} is NOT present, skipping expose dashboard..."
fi
