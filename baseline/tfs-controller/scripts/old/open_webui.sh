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

# this script opens the webui

K8S_NAMESPACE=${K8S_NAMESPACE:-'tfs'}

WEBUI_SERVICE_NAME="webuiservice"
WEBUI_IP=`kubectl get service ${WEBUI_SERVICE_NAME} -n ${K8S_NAMESPACE} -o jsonpath='{.spec.clusterIP}'`
# WEBUI_PORT=$(kubectl get service ${WEBUI_SERVICE_NAME} --namespace $K8S_NAMESPACE -o 'jsonpath={.spec.ports[?(@.port==8004)].nodePort}')
WEBUI_PORT=8004
# GRAFANA_PORT=$(kubectl get service ${WEBUI_SERVICE_NAME} --namespace $K8S_NAMESPACE -o 'jsonpath={.spec.ports[?(@.port==3000)].nodePort}')
GRAFANA_PORT=3000

echo "Configuring WebUI DataStores and Dashboards..."
sleep 3
INFLUXDB_HOST="monitoringservice"
INFLUXDB_PORT=$(kubectl --namespace $TFS_K8S_NAMESPACE get service/monitoringservice -o jsonpath='{.spec.ports[?(@.name=="influxdb")].port}')
INFLUXDB_URL="http://${INFLUXDB_HOST}:${INFLUXDB_PORT}"
INFLUXDB_USER=$(kubectl --namespace $TFS_K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_ADMIN_USER}' | base64 --decode)
INFLUXDB_PASSWORD=$(kubectl --namespace $TFS_K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_ADMIN_PASSWORD}' | base64 --decode)
INFLUXDB_DATABASE=$(kubectl --namespace $TFS_K8S_NAMESPACE get secrets influxdb-secrets -o jsonpath='{.data.INFLUXDB_DB}' | base64 --decode)
# Exposed through the ingress controller "tfs-ingress"
# GRAFANA_HOSTNAME="127.0.0.1"
# GRAFANA_PORT="80"
# GRAFANA_BASEURL="/grafana"
# Default Grafana credentials
GRAFANA_USERNAME="admin"
GRAFANA_PASSWORD="admin"
# Default Grafana API URL
GRAFANA_URL_DEFAULT=http://${GRAFANA_USERNAME}:${GRAFANA_PASSWORD}@${WEBUI_IP}:${GRAFANA_PORT} #"http://${GRAFANA_USERNAME}:${GRAFANA_PASSWORD}@${GRAFANA_HOSTNAME}:${GRAFANA_PORT}${GRAFANA_BASEURL}"
# Updated Grafana API URL
GRAFANA_URL_UPDATED=http://${GRAFANA_USERNAME}:${TFS_GRAFANA_PASSWORD}@${WEBUI_IP}:${GRAFANA_PORT} #"http://${GRAFANA_USERNAME}:${TFS_GRAFANA_PASSWORD}@${GRAFANA_HOSTNAME}:${GRAFANA_PORT}${GRAFANA_BASEURL}"
echo "Connecting to grafana at URL: ${GRAFANA_URL_DEFAULT}..."
# Configure Grafana Admin Password
# Ref: https://grafana.com/docs/grafana/latest/http_api/user/#change-password
curl -X PUT -H "Content-Type: application/json" -d '{
    "oldPassword": "'${GRAFANA_PASSWORD}'",
    "newPassword": "'${TFS_GRAFANA_PASSWORD}'",
    "confirmNew" : "'${TFS_GRAFANA_PASSWORD}'"
}' ${GRAFANA_URL_DEFAULT}/api/user/password
echo
# Create InfluxDB DataSource
# Ref: https://grafana.com/docs/grafana/latest/http_api/data_source/
curl -X POST -H "Content-Type: application/json" -d '{
    "type"     : "influxdb",
    "name"     : "InfluxDB",
    "url"      : "'"$INFLUXDB_URL"'",
    "access"   : "proxy",
    "basicAuth": false,
    "user"     : "'"$INFLUXDB_USER"'",
    "password" : "'"$INFLUXDB_PASSWORD"'",
    "isDefault": true,
    "database" : "'"$INFLUXDB_DATABASE"'"
}' ${GRAFANA_URL_UPDATED}/api/datasources
echo
# Create Monitoring Dashboard
# Ref: https://grafana.com/docs/grafana/latest/http_api/dashboard/
curl -X POST -H "Content-Type: application/json" \
-d '@src/webui/grafana_dashboard.json' \
${GRAFANA_URL_UPDATED}/api/dashboards/db
echo
DASHBOARD_URL="${GRAFANA_URL_UPDATED}/api/dashboards/uid/tf-l3-monit"
DASHBOARD_ID=$(curl -s "${DASHBOARD_URL}" | jq '.dashboard.id')
curl -X POST ${GRAFANA_URL_UPDATED}/api/user/stars/dashboard/${DASHBOARD_ID}

# Open WebUI
UI_URL="http://${WEBUI_IP}:${WEBUI_PORT}"
echo "Opening web UI on URL ${UI_URL}"
# curl -kL ${UI_URL}
python3 -m webbrowser ${UI_URL}

# Open Dashboard
DASHB_URL="http://${WEBUI_IP}:${GRAFANA_PORT}"
echo "Opening Dashboard on URL ${DASHB_URL}"
# curl -kL ${DASHB_URL}
python3 -m webbrowser ${DASHB_URL}
