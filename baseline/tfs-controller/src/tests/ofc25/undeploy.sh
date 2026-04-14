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
microk8s status --wait-ready
kubectl get pods --all-namespaces

# ===== Cleanup old deployments ==============================
helm3 uninstall --namespace nats-e2e nats-e2e 2>/dev/null || true
helm3 uninstall --namespace nats-ip  nats-ip  2>/dev/null || true
helm3 uninstall --namespace nats-opt nats-opt 2>/dev/null || true
helm3 uninstall --namespace nats     nats     2>/dev/null || true
kubectl delete namespaces tfs tfs-ip tfs-opt tfs-e2e --ignore-not-found
kubectl delete namespaces qdb qdb-e2e qdb-opt qdb-ip --ignore-not-found
kubectl delete namespaces kafka kafka-ip kafka-opt kafka-e2e --ignore-not-found
kubectl delete namespaces nats nats-ip nats-opt nats-e2e --ignore-not-found

kubectl delete -f src/tests/ofc25/nginx-ingress-controller-opt.yaml --ignore-not-found
kubectl delete -f src/tests/ofc25/nginx-ingress-controller-ip.yaml  --ignore-not-found
kubectl delete -f src/tests/ofc25/nginx-ingress-controller-e2e.yaml --ignore-not-found

# ===== Check Microk8s is ready ==============================
microk8s status --wait-ready
kubectl get pods --all-namespaces

echo "Done!"
