# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Set the URL of your local Docker registry where the images will be uploaded to.
export TFS_REGISTRY_IMAGE="http://localhost:32000/tfs/"

# Set the list of components, separated by spaces, you want to build images for, and deploy.
# Supported components are:
#   context device ztp policy service nbi monitoring webui
#   interdomain slice pathcomp dlt
#   dbscanserving opticalattackmitigator opticalattackdetector
#   l3_attackmitigator l3_centralizedattackdetector l3_distributedattackdetector
export TFS_COMPONENTS="context device pathcomp service slice webui load_generator" # ztp monitoring nbi dlt

# Set the tag you want to use for your images.
export TFS_IMAGE_TAG="dev"

# Set the name of the Kubernetes namespace to deploy to.
export TFS_K8S_NAMESPACE="tfs"

# Set additional manifest files to be applied after the deployment
export TFS_EXTRA_MANIFESTS="manifests/nginx_ingress_http.yaml manifests/servicemonitors.yaml"

# Set the new Grafana admin password
export TFS_GRAFANA_PASSWORD="admin123+"

# If not already set, disable skip-build flag.
# If TFS_SKIP_BUILD is "YES", the containers are not rebuilt-retagged-repushed and existing ones are used.
export TFS_SKIP_BUILD="NO" #${TFS_SKIP_BUILD:-"YES"}
