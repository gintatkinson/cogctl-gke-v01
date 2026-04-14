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


# Destroy all replicas of all microservices

kubectl --namespace tfs-dom1 scale --replicas=0 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice

kubectl --namespace tfs-dom2 scale --replicas=0 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice

kubectl --namespace tfs-dom3 scale --replicas=0 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice

kubectl --namespace tfs-dom4 scale --replicas=0 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice

# Create a single replica per microservice

kubectl --namespace tfs-dom1 scale --replicas=1 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice

kubectl --namespace tfs-dom2 scale --replicas=1 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice

kubectl --namespace tfs-dom3 scale --replicas=1 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice

kubectl --namespace tfs-dom4 scale --replicas=1 \
    deployment/contextservice deployment/deviceservice deployment/pathcompservice deployment/serviceservice \
    deployment/sliceservice deployment/dltservice deployment/interdomainservice deployment/webuiservice
