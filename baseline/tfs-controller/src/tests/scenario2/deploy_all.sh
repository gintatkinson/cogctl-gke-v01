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
kubectl delete namespace tfs-dom1 tfs-dom2 tfs-dom3 tfs-dom4

# Delete secondary ingress controllers
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom1.yaml
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom2.yaml
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom3.yaml
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom4.yaml

# Delete MockBlockchain (comment out if using a real blockchain)
kubectl delete namespace tfs-bchain

# Create secondary ingress controllers
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom1.yaml
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom2.yaml
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom3.yaml
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom4.yaml

# Create MockBlockchain (comment out if using a real blockchain)
./deploy/mock_blockchain.sh

# Deploy TFS for Domain 1
source nfvsdn22/deploy_specs_dom1.sh
./deploy/all.sh
mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_dom1.sh

# Deploy TFS for Domain 2
source nfvsdn22/deploy_specs_dom2.sh
./deploy/all.sh
mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_dom2.sh

# Deploy TFS for Domain 3
source nfvsdn22/deploy_specs_dom3.sh
./deploy/all.sh
mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_dom3.sh

# Deploy TFS for Domain 4
source nfvsdn22/deploy_specs_dom4.sh
./deploy/all.sh
mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_dom4.sh
