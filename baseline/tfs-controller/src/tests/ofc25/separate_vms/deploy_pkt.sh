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
#helm3 uninstall --namespace nats nats 2>/dev/null || true
#kubectl delete namespaces tfs --ignore-not-found
#kubectl delete namespaces qdb --ignore-not-found
#kubectl delete namespaces kafka --ignore-not-found
#kubectl delete namespaces nats --ignore-not-found


# ===== Check Microk8s is ready ==============================
#microk8s status --wait-ready
#kubectl get pods --all-namespaces


# ===== Deploy End-to-End TeraFlowSDN ====================
sed -i 's|\(<h2>ETSI TeraFlowSDN Controller\)</h2>|\1 (Packet)</h2>|' src/webui/service/templates/main/home.html
source src/tests/ofc25/separate_vms/deploy_specs_pkt.sh

./deploy/crdb.sh
./deploy/nats.sh
./deploy/kafka.sh
#./deploy/qdb.sh
#./deploy/expose_dashboard.sh
./deploy/tfs.sh
./deploy/show.sh


echo "Done!"
