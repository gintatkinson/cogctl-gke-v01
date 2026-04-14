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

echo "Collecting logs for Parent..."
mkdir -p tmp/exec/parent
kubectl --namespace tfs-parent logs deployments/contextservice server > tmp/exec/parent/context.log
kubectl --namespace tfs-parent logs deployments/deviceservice server > tmp/exec/parent/device.log
kubectl --namespace tfs-parent logs deployments/serviceservice server > tmp/exec/parent/service.log
kubectl --namespace tfs-parent logs deployments/pathcompservice frontend > tmp/exec/parent/pathcomp-frontend.log
kubectl --namespace tfs-parent logs deployments/pathcompservice backend > tmp/exec/parent/pathcomp-backend.log
kubectl --namespace tfs-parent logs deployments/sliceservice server > tmp/exec/parent/slice.log
printf "\n"

echo "Collecting logs for Child..."
mkdir -p tmp/exec/child
kubectl --namespace tfs-child logs deployments/contextservice server > tmp/exec/child/context.log
kubectl --namespace tfs-child logs deployments/deviceservice server > tmp/exec/child/device.log
kubectl --namespace tfs-child logs deployments/serviceservice server > tmp/exec/child/service.log
kubectl --namespace tfs-child logs deployments/pathcompservice frontend > tmp/exec/child/pathcomp-frontend.log
kubectl --namespace tfs-child logs deployments/pathcompservice backend > tmp/exec/child/pathcomp-backend.log
kubectl --namespace tfs-child logs deployments/sliceservice server > tmp/exec/child/slice.log
printf "\n"

echo "Done!"
