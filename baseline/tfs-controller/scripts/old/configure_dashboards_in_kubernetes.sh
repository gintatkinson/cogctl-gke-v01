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


# If not already set, set the name of the Kubernetes namespace and hostname to deploy to.
K8S_NAMESPACE=${K8S_NAMESPACE:-'tf-dev'}
K8S_HOSTNAME=${K8S_HOSTNAME:-'kubernetes-master'}

INFLUXDB_USER=$(kubectl --namespace $K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_ADMIN_USER}' | base64 --decode)
INFLUXDB_PASSWORD=$(kubectl --namespace $K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_ADMIN_PASSWORD}' | base64 --decode)
INFLUXDB_DATABASE=$(kubectl --namespace $K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_DB}' | base64 --decode)

# GRAFANA_HOSTNAME=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
# GRAFANA_HOSTNAME=`kubectl get service/webuiservice-public -n ${K8S_NAMESPACE} -o jsonpath='{.spec.clusterIP}'`
GRAFANA_HOSTNAME=`kubectl get nodes --selector=node-role.kubernetes.io/master -o jsonpath='{$.items[*].status.addresses[?(@.type=="InternalIP")].address}'`
GRAFANA_PORT=$(kubectl get service webuiservice-public --namespace $K8S_NAMESPACE -o 'jsonpath={.spec.ports[?(@.port==3000)].nodePort}')
#GRAFANA_PORT=`kubectl get service/webuiservice-public -n ${K8S_NAMESPACE} -o jsonpath='{.spec.ports[1].nodePort}'`
GRAFANA_USERNAME="admin"
GRAFANA_PASSWORD=${GRAFANA_PASSWORD:-"admin123+"}
GRAFANA_URL="http://${GRAFANA_USERNAME}:${GRAFANA_PASSWORD}@${GRAFANA_HOSTNAME}:${GRAFANA_PORT}"
echo "Connecting to grafana at URL: ${GRAFANA_URL}..."

# Configure Grafana Admin Password
# Ref: https://grafana.com/docs/grafana/latest/http_api/user/#change-password
curl -X PUT -H "Content-Type: application/json" -d '{
  "oldPassword": "admin",
  "newPassword": "'${GRAFANA_PASSWORD}'",
  "confirmNew" : "'${GRAFANA_PASSWORD}'"
}' http://admin:admin@${GRAFANA_HOSTNAME}:${GRAFANA_PORT}/api/user/password
echo

# Create InfluxDB DataSource
# Ref: https://grafana.com/docs/grafana/latest/http_api/data_source/
curl -X POST -H "Content-Type: application/json" -d '{
  "type"     : "influxdb",
  "name"     : "InfluxDB",
  "url"      : "http://monitoringservice:8086",
  "access"   : "proxy",
  "basicAuth": false,
  "user"     : "'"$INFLUXDB_USER"'",
  "password" : "'"$INFLUXDB_PASSWORD"'",
  "isDefault": true,
  "database" : "'"$INFLUXDB_DATABASE"'"
}' ${GRAFANA_URL}/api/datasources
echo

# Create Monitoring Dashboard
# Ref: https://grafana.com/docs/grafana/latest/http_api/dashboard/
curl -X POST -H "Content-Type: application/json" \
  -d '@src/webui/grafana_dashboard.json' \
  ${GRAFANA_URL}/api/dashboards/db
echo

DASHBOARD_URL="${GRAFANA_URL}/api/dashboards/uid/tf-l3-monit"
DASHBOARD_ID=$(python -c 'import json, requests; print(requests.get("'${DASHBOARD_URL}'").json()["dashboard"]["id"])')
curl -X POST ${GRAFANA_URL}/api/user/stars/dashboard/${DASHBOARD_ID}
