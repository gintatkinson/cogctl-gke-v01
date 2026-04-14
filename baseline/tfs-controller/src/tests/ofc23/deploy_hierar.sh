#!/bin/bash
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


# Delete old namespaces
kubectl delete namespace tfs-parent tfs-child

# Delete secondary ingress controllers
kubectl delete -f ofc23/nginx-ingress-controller-parent.yaml
kubectl delete -f ofc23/nginx-ingress-controller-child.yaml

# Create secondary ingress controllers
kubectl apply -f ofc23/nginx-ingress-controller-parent.yaml
kubectl apply -f ofc23/nginx-ingress-controller-child.yaml

# Deploy TFS for Parent
source ofc23/deploy_specs_parent.sh
./deploy/all.sh
mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_parent.sh

# Deploy TFS for Child
source ofc23/deploy_specs_child.sh
./deploy/all.sh
mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_child.sh
