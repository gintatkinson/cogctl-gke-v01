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

#/bin/bash

# this script opens the dashboard

GRAFANA_IP=$(kubectl get service/grafana -n monitoring -o jsonpath='{.spec.clusterIP}')
GRAFANA_PORT=3000 #$(kubectl get service webuiservice --namespace $TFS_K8S_NAMESPACE -o 'jsonpath={.spec.ports[?(@.port==3000)].nodePort}')
URL=http://${GRAFANA_IP}:${GRAFANA_PORT}

echo Opening Dashboard on URL ${URL}

# curl -kL ${URL}

python3 -m webbrowser ${URL}
