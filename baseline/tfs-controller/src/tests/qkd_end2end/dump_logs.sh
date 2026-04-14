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


kubectl --namespace tfs logs deployment/contextservice -c server > context.log
kubectl --namespace tfs logs deployment/deviceservice -c server > device.log
kubectl --namespace tfs logs deployment/pathcompservice -c frontend > pathcomp_front.log
kubectl --namespace tfs logs deployment/pathcompservice -c backend > pathcomp_back.log
kubectl --namespace tfs logs deployment/serviceservice -c server > service.log
kubectl --namespace tfs logs deployment/qkd-appservice -c server > qkd_app.log
kubectl --namespace tfs logs deployment/nbiservice -c server > nbi.log
kubectl --namespace tfs logs deployment/webuiservice -c server > webui.log
