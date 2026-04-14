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

# for development purposes only

# K8S_NAMESPACE=${K8S_NAMESPACE:-'tf-dev'}

# export CONTEXTSERVICE_SERVICE_HOST=`kubectl get service/contextservice -n ${K8S_NAMESPACE} -o jsonpath='{.spec.clusterIP}'`

# echo Context IP: $CONTEXTSERVICE_SERVICE_HOST

# export DEVICESERVICE_SERVICE_HOST=`kubectl get service/deviceservice -n ${K8S_NAMESPACE} -o jsonpath='{.spec.clusterIP}'`

# echo Device IP: $DEVICESERVICE_SERVICE_HOST

source tfs_runtime_env_vars.sh

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python'
export HOST="127.0.0.1"
export HOSTNAME="test"
export FLASK_ENV="development"
export LOG_LEVEL="DEBUG"

# python3 -m webbrowser http://${HOST}:8004

python -m webui.service
