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


rm logs -rf tmp/exec
mkdir -p tmp/exec

echo "Collecting logs for E2E..."
kubectl logs --namespace tfs-e2e deployment/contextservice          -c server   > tmp/exec/e2e-context.log
kubectl logs --namespace tfs-e2e deployment/deviceservice           -c server   > tmp/exec/e2e-device.log
kubectl logs --namespace tfs-e2e deployment/serviceservice          -c server   > tmp/exec/e2e-service.log
kubectl logs --namespace tfs-e2e deployment/pathcompservice         -c frontend > tmp/exec/e2e-pathcomp-frontend.log
kubectl logs --namespace tfs-e2e deployment/pathcompservice         -c backend  > tmp/exec/e2e-pathcomp-backend.log
kubectl logs --namespace tfs-e2e deployment/webuiservice            -c server   > tmp/exec/e2e-webui.log
kubectl logs --namespace tfs-e2e deployment/nbiservice              -c server   > tmp/exec/e2e-nbi.log
kubectl logs --namespace tfs-e2e deployment/e2e-orchestratorservice -c server   > tmp/exec/e2e-orch.log
printf "\n"

echo "Collecting logs for IP..."
kubectl logs --namespace tfs-ip deployment/contextservice     -c server   > tmp/exec/ip-context.log
kubectl logs --namespace tfs-ip deployment/deviceservice      -c server   > tmp/exec/ip-device.log
kubectl logs --namespace tfs-ip deployment/serviceservice     -c server   > tmp/exec/ip-service.log
kubectl logs --namespace tfs-ip deployment/pathcompservice    -c frontend > tmp/exec/ip-pathcomp-frontend.log
kubectl logs --namespace tfs-ip deployment/pathcompservice    -c backend  > tmp/exec/ip-pathcomp-backend.log
kubectl logs --namespace tfs-ip deployment/webuiservice       -c server   > tmp/exec/ip-webui.log
kubectl logs --namespace tfs-ip deployment/nbiservice         -c server   > tmp/exec/ip-nbi.log
kubectl logs --namespace tfs-ip deployment/vnt-managerservice -c server   > tmp/exec/ip-vntm.log
printf "\n"

echo "Collecting logs for OPT..."
kubectl logs --namespace tfs-opt deployment/contextservice           -c server   > tmp/exec/opt-context.log
kubectl logs --namespace tfs-opt deployment/deviceservice            -c server   > tmp/exec/opt-device.log
kubectl logs --namespace tfs-opt deployment/serviceservice           -c server   > tmp/exec/opt-service.log
kubectl logs --namespace tfs-opt deployment/pathcompservice          -c frontend > tmp/exec/opt-pathcomp-frontend.log
kubectl logs --namespace tfs-opt deployment/pathcompservice          -c backend  > tmp/exec/opt-pathcomp-backend.log
kubectl logs --namespace tfs-opt deployment/webuiservice             -c server   > tmp/exec/opt-webui.log
kubectl logs --namespace tfs-opt deployment/nbiservice               -c server   > tmp/exec/opt-nbi.log
kubectl logs --namespace tfs-opt deployment/opticalcontrollerservice -c server   > tmp/exec/opt-ctrl.log
printf "\n"

echo "Done!"
