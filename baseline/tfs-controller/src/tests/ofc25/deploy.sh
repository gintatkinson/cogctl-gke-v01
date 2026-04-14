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

# ===== Check Microk8s is ready ==============================
#microk8s status --wait-ready
#kubectl get pods --all-namespaces

# ===== Cleanup old deployments ==============================
#helm3 uninstall --namespace nats-e2e nats-e2e 2>/dev/null || true
#helm3 uninstall --namespace nats-ip  nats-ip  2>/dev/null || true
#helm3 uninstall --namespace nats-opt nats-opt 2>/dev/null || true
#helm3 uninstall --namespace nats     nats     2>/dev/null || true
#kubectl delete namespaces tfs tfs-ip tfs-opt tfs-e2e --ignore-not-found
#kubectl delete namespaces qdb qdb-e2e qdb-opt qdb-ip --ignore-not-found
#kubectl delete namespaces kafka kafka-ip kafka-opt kafka-e2e --ignore-not-found
#kubectl delete namespaces nats nats-ip nats-opt nats-e2e --ignore-not-found
#kubectl delete -f src/tests/ofc25/nginx-ingress-controller-opt.yaml --ignore-not-found
#kubectl delete -f src/tests/ofc25/nginx-ingress-controller-ip.yaml  --ignore-not-found
#kubectl delete -f src/tests/ofc25/nginx-ingress-controller-e2e.yaml --ignore-not-found
#sleep 5

# ===== Check Microk8s is ready ==============================
#microk8s status --wait-ready
#kubectl get pods --all-namespaces

# Configure TeraFlowSDN deployment
# Uncomment if DEBUG log level is needed for the components
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="server").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/contextservice.yaml
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="server").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/deviceservice.yaml
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="frontend").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/pathcompservice.yaml
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="server").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/serviceservice.yaml
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="server").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/sliceservice.yaml
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="server").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/nbiservice.yaml
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="server").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/e2eorchestratorservice.yaml
#yq -i '((select(.kind=="Deployment").spec.template.spec.containers.[] | select(.name=="server").env.[]) | select(.name=="LOG_LEVEL").value) |= "DEBUG"' manifests/vntmservice.yaml

# Create secondary ingress controllers
kubectl apply -f src/tests/ofc25/nginx-ingress-controller-opt.yaml
kubectl apply -f src/tests/ofc25/nginx-ingress-controller-ip.yaml
kubectl apply -f src/tests/ofc25/nginx-ingress-controller-e2e.yaml

cp manifests/contextservice.yaml manifests/contextservice.yaml.bak

# ===== Deploy Optical TeraFlowSDN ==============================
source src/tests/ofc25/deploy_specs_opt.sh
cp manifests/contextservice.yaml.bak manifests/contextservice.yaml
sed -i '/name: CRDB_DATABASE/{n;s/value: .*/value: "tfs_opt_context"/}' manifests/contextservice.yaml
sed -i 's|\(<h2>ETSI TeraFlowSDN Controller\)</h2>|\1 (Optical)</h2>|' src/webui/service/templates/main/home.html

./deploy/crdb.sh
./deploy/nats.sh
./deploy/kafka.sh
#./deploy/qdb.sh
#./deploy/expose_dashboard.sh
./deploy/tfs.sh
./deploy/show.sh

mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_opt.sh


# ===== Deploy IP TeraFlowSDN ==============================
source src/tests/ofc25/deploy_specs_ip.sh
cp manifests/contextservice.yaml.bak manifests/contextservice.yaml
sed -i '/name: CRDB_DATABASE/{n;s/value: .*/value: "tfs_ip_context"/}' manifests/contextservice.yaml
sed -i 's|\(<h2>ETSI TeraFlowSDN Controller\)</h2>|\1 (Packet)</h2>|' src/webui/service/templates/main/home.html

./deploy/crdb.sh
./deploy/nats.sh
./deploy/kafka.sh
#./deploy/qdb.sh
#./deploy/expose_dashboard.sh
./deploy/tfs.sh
./deploy/show.sh

mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_ip.sh


# ===== Deploy End-to-End TeraFlowSDN ====================
source src/tests/ofc25/deploy_specs_e2e.sh
cp manifests/contextservice.yaml.bak manifests/contextservice.yaml
sed -i '/name: CRDB_DATABASE/{n;s/value: .*/value: "tfs_e2e_context"/}' manifests/contextservice.yaml
sed -i 's|\(<h2>ETSI TeraFlowSDN Controller\)</h2>|\1 (End-to-End)</h2>|' src/webui/service/templates/main/home.html

./deploy/crdb.sh
./deploy/nats.sh
./deploy/kafka.sh
#./deploy/qdb.sh
#./deploy/expose_dashboard.sh
./deploy/tfs.sh
./deploy/show.sh

mv tfs_runtime_env_vars.sh tfs_runtime_env_vars_e2e.sh


# ===== Recovering files =========================
mv manifests/contextservice.yaml.bak manifests/contextservice.yaml


# ===== Wait Content for NATS Subscription =========================
echo "Waiting for E2E Context to have subscriber ready..."
while ! kubectl --namespace tfs-e2e logs deployment/contextservice -c server 2>&1 | grep -q 'Subscriber is Ready? True'; do sleep 1; done
kubectl --namespace tfs-e2e logs deployment/contextservice -c server


echo "Done!"
