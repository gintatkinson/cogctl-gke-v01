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
kubectl delete namespace tfs-e2e

# Delete secondary ingress controllers
kubectl delete -f src/tests/ofc25/nginx-ingress-controller-e2e.yaml

# Create secondary ingress controllers
kubectl apply -f src/tests/ofc25/nginx-ingress-controller-e2e.yaml

# Deploy TFS for E2E
source src/tests/ofc25/deploy_specs_e2e.sh

# Change the name for the database
cp manifests/contextservice.yaml manifests/contextservice.yaml.bak
sed -i '/name: CRDB_DATABASE/{n;s/value: .*/value: "tfs_e2e_context"/}' manifests/contextservice.yaml
./deploy/all.sh
mv manifests/contextservice.yaml.bak manifests/contextservice.yaml

#Configure Subscription WS
./src/tests/ofc25/subscription_ws_e2e.sh

mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_e2e.sh
