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

echo "Collecting logs for MockBlockChain..."
rm -rf tmp/tfs-bchain/exec
mkdir -p tmp/tfs-bchain/exec
kubectl --namespace tfs-bchain logs deployments/mock-blockchain server > tmp/tfs-bchain/exec/mock-blockchain.log
printf "\n"

echo "Collecting logs for Domain 1..."
rm -rf tmp/tfs-dom1/exec
mkdir -p tmp/tfs-dom1/exec
kubectl --namespace tfs-dom1 logs deployments/contextservice server > tmp/tfs-dom1/exec/context.log
kubectl --namespace tfs-dom1 logs deployments/deviceservice server > tmp/tfs-dom1/exec/device.log
kubectl --namespace tfs-dom1 logs deployments/serviceservice server > tmp/tfs-dom1/exec/service.log
kubectl --namespace tfs-dom1 logs deployments/pathcompservice frontend > tmp/tfs-dom1/exec/pathcomp-frontend.log
kubectl --namespace tfs-dom1 logs deployments/pathcompservice backend > tmp/tfs-dom1/exec/pathcomp-backend.log
kubectl --namespace tfs-dom1 logs deployments/sliceservice server > tmp/tfs-dom1/exec/slice.log
kubectl --namespace tfs-dom1 logs deployments/interdomainservice server > tmp/tfs-dom1/exec/interdomain.log
kubectl --namespace tfs-dom1 logs deployments/dltservice connector > tmp/tfs-dom1/exec/dlt-connector.log
kubectl --namespace tfs-dom1 logs deployments/dltservice gateway > tmp/tfs-dom1/exec/dlt-gateway.log
kubectl --namespace tfs-dom1 logs deployments/webuiservice server > tmp/tfs-dom1/exec/webui.log
printf "\n"

echo "Collecting logs for Domain 2..."
rm -rf tmp/tfs-dom2/exec
mkdir -p tmp/tfs-dom2/exec
kubectl --namespace tfs-dom2 logs deployments/contextservice server > tmp/tfs-dom2/exec/context.log
kubectl --namespace tfs-dom2 logs deployments/deviceservice server > tmp/tfs-dom2/exec/device.log
kubectl --namespace tfs-dom2 logs deployments/serviceservice server > tmp/tfs-dom2/exec/service.log
kubectl --namespace tfs-dom2 logs deployments/pathcompservice frontend > tmp/tfs-dom2/exec/pathcomp-frontend.log
kubectl --namespace tfs-dom2 logs deployments/pathcompservice backend > tmp/tfs-dom2/exec/pathcomp-backend.log
kubectl --namespace tfs-dom2 logs deployments/sliceservice server > tmp/tfs-dom2/exec/slice.log
kubectl --namespace tfs-dom2 logs deployments/interdomainservice server > tmp/tfs-dom2/exec/interdomain.log
kubectl --namespace tfs-dom2 logs deployments/dltservice connector > tmp/tfs-dom2/exec/dlt-connector.log
kubectl --namespace tfs-dom2 logs deployments/dltservice gateway > tmp/tfs-dom2/exec/dlt-gateway.log
kubectl --namespace tfs-dom2 logs deployments/webuiservice server > tmp/tfs-dom2/exec/webui.log
printf "\n"

echo "Collecting logs for Domain 3..."
rm -rf tmp/tfs-dom3/exec
mkdir -p tmp/tfs-dom3/exec
kubectl --namespace tfs-dom3 logs deployments/contextservice server > tmp/tfs-dom3/exec/context.log
kubectl --namespace tfs-dom3 logs deployments/deviceservice server > tmp/tfs-dom3/exec/device.log
kubectl --namespace tfs-dom3 logs deployments/serviceservice server > tmp/tfs-dom3/exec/service.log
kubectl --namespace tfs-dom3 logs deployments/pathcompservice frontend > tmp/tfs-dom3/exec/pathcomp-frontend.log
kubectl --namespace tfs-dom3 logs deployments/pathcompservice backend > tmp/tfs-dom3/exec/pathcomp-backend.log
kubectl --namespace tfs-dom3 logs deployments/sliceservice server > tmp/tfs-dom3/exec/slice.log
kubectl --namespace tfs-dom3 logs deployments/interdomainservice server > tmp/tfs-dom3/exec/interdomain.log
kubectl --namespace tfs-dom3 logs deployments/dltservice connector > tmp/tfs-dom3/exec/dlt-connector.log
kubectl --namespace tfs-dom3 logs deployments/dltservice gateway > tmp/tfs-dom3/exec/dlt-gateway.log
kubectl --namespace tfs-dom3 logs deployments/webuiservice server > tmp/tfs-dom3/exec/webui.log
printf "\n"

echo "Collecting logs for Domain 4..."
rm -rf tmp/tfs-dom4/exec
mkdir -p tmp/tfs-dom4/exec
kubectl --namespace tfs-dom4 logs deployments/contextservice server > tmp/tfs-dom4/exec/context.log
kubectl --namespace tfs-dom4 logs deployments/deviceservice server > tmp/tfs-dom4/exec/device.log
kubectl --namespace tfs-dom4 logs deployments/serviceservice server > tmp/tfs-dom4/exec/service.log
kubectl --namespace tfs-dom4 logs deployments/pathcompservice frontend > tmp/tfs-dom4/exec/pathcomp-frontend.log
kubectl --namespace tfs-dom4 logs deployments/pathcompservice backend > tmp/tfs-dom4/exec/pathcomp-backend.log
kubectl --namespace tfs-dom4 logs deployments/sliceservice server > tmp/tfs-dom4/exec/slice.log
kubectl --namespace tfs-dom4 logs deployments/interdomainservice server > tmp/tfs-dom4/exec/interdomain.log
kubectl --namespace tfs-dom4 logs deployments/dltservice connector > tmp/tfs-dom4/exec/dlt-connector.log
kubectl --namespace tfs-dom4 logs deployments/dltservice gateway > tmp/tfs-dom4/exec/dlt-gateway.log
kubectl --namespace tfs-dom4 logs deployments/webuiservice server > tmp/tfs-dom4/exec/webui.log
printf "\n"

echo "Done!"
