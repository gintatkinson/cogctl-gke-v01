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


rm -rf tmp/exec

echo "Collecting logs for Domain 1..."
mkdir -p tmp/tfs-dom1/exec
kubectl --namespace tfs-dom1 logs deployments/contextservice server > tmp/tfs-dom1/exec/context.log
kubectl --namespace tfs-dom1 logs deployments/deviceservice server > tmp/tfs-dom1/exec/device.log
kubectl --namespace tfs-dom1 logs deployments/serviceservice server > tmp/tfs-dom1/exec/service.log
kubectl --namespace tfs-dom1 logs deployments/pathcompservice frontend > tmp/tfs-dom1/exec/pathcomp-frontend.log
kubectl --namespace tfs-dom1 logs deployments/pathcompservice backend > tmp/tfs-dom1/exec/pathcomp-backend.log
kubectl --namespace tfs-dom1 logs deployments/sliceservice server > tmp/tfs-dom1/exec/slice.log
kubectl --namespace tfs-dom1 logs deployment/interdomainservice server > tmp/tfs-dom1/exec/interdomain.log
kubectl --namespace tfs-dom1 logs deployment/webuiservice server > tmp/tfs-dom1/exec/webui.log
printf "\n"

echo "Collecting logs for Domain 2..."
mkdir -p tmp/tfs-dom2/exec
kubectl --namespace tfs-dom2 logs deployments/contextservice server > tmp/tfs-dom2/exec/context.log
kubectl --namespace tfs-dom2 logs deployments/deviceservice server > tmp/tfs-dom2/exec/device.log
kubectl --namespace tfs-dom2 logs deployments/serviceservice server > tmp/tfs-dom2/exec/service.log
kubectl --namespace tfs-dom2 logs deployments/pathcompservice frontend > tmp/tfs-dom2/exec/pathcomp-frontend.log
kubectl --namespace tfs-dom2 logs deployments/pathcompservice backend > tmp/tfs-dom2/exec/pathcomp-backend.log
kubectl --namespace tfs-dom2 logs deployments/sliceservice server > tmp/tfs-dom2/exec/slice.log
kubectl --namespace tfs-dom2 logs deployment/interdomainservice server > tmp/tfs-dom2/exec/interdomain.log
kubectl --namespace tfs-dom2 logs deployment/webuiservice server > tmp/tfs-dom2/exec/webui.log
printf "\n"

echo "Done!"
