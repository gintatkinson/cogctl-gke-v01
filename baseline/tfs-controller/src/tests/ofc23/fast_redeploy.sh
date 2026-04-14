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


kubectl delete namespace tfs-parent tfs-child

echo "Deploying tfs-parent ..."
kubectl delete -f ofc23/nginx-ingress-controller-parent.yaml                 > ./tmp/logs/deploy-tfs-parent.log
kubectl create namespace tfs-parent                                          > ./tmp/logs/deploy-tfs-parent.log
kubectl apply -f ofc23/nginx-ingress-controller-parent.yaml                  > ./tmp/logs/deploy-tfs-parent.log
kubectl --namespace tfs-parent apply -f ./tmp/manifests/contextservice.yaml  > ./tmp/logs/deploy-tfs-parent.log
kubectl --namespace tfs-parent apply -f ./tmp/manifests/deviceservice.yaml   > ./tmp/logs/deploy-tfs-parent.log
kubectl --namespace tfs-parent apply -f ./tmp/manifests/pathcompservice.yaml > ./tmp/logs/deploy-tfs-parent.log
kubectl --namespace tfs-parent apply -f ./tmp/manifests/serviceservice.yaml  > ./tmp/logs/deploy-tfs-parent.log
kubectl --namespace tfs-parent apply -f ./tmp/manifests/sliceservice.yaml    > ./tmp/logs/deploy-tfs-parent.log
kubectl --namespace tfs-parent apply -f ./tmp/manifests/webuiservice.yaml    > ./tmp/logs/deploy-tfs-parent.log
kubectl --namespace tfs-parent apply -f ofc23/tfs-ingress-parent.yaml        > ./tmp/logs/deploy-tfs-parent.log
printf "\n"

echo "Deploying tfs-child ..."
kubectl delete -f ofc23/nginx-ingress-controller-child.yaml                  > ./tmp/logs/deploy-tfs-child.log
kubectl create namespace tfs-child                                           > ./tmp/logs/deploy-tfs-child.log
kubectl apply -f ofc23/nginx-ingress-controller-child.yaml                   > ./tmp/logs/deploy-tfs-child.log
kubectl --namespace tfs-child apply -f ./tmp/manifests/contextservice.yaml   > ./tmp/logs/deploy-tfs-child.log
kubectl --namespace tfs-child apply -f ./tmp/manifests/deviceservice.yaml    > ./tmp/logs/deploy-tfs-child.log
kubectl --namespace tfs-child apply -f ./tmp/manifests/pathcompservice.yaml  > ./tmp/logs/deploy-tfs-child.log
kubectl --namespace tfs-child apply -f ./tmp/manifests/serviceservice.yaml   > ./tmp/logs/deploy-tfs-child.log
kubectl --namespace tfs-child apply -f ./tmp/manifests/sliceservice.yaml     > ./tmp/logs/deploy-tfs-child.log
kubectl --namespace tfs-child apply -f ./tmp/manifests/webuiservice.yaml     > ./tmp/logs/deploy-tfs-child.log
kubectl --namespace tfs-child apply -f ofc23/tfs-ingress-child.yaml          > ./tmp/logs/deploy-tfs-child.log
printf "\n"

echo "Waiting tfs-parent ..."
kubectl wait --namespace tfs-parent --for='condition=available' --timeout=300s deployment/contextservice
kubectl wait --namespace tfs-parent --for='condition=available' --timeout=300s deployment/deviceservice
kubectl wait --namespace tfs-parent --for='condition=available' --timeout=300s deployment/pathcompservice
kubectl wait --namespace tfs-parent --for='condition=available' --timeout=300s deployment/serviceservice
kubectl wait --namespace tfs-parent --for='condition=available' --timeout=300s deployment/sliceservice
kubectl wait --namespace tfs-parent --for='condition=available' --timeout=300s deployment/webuiservice
printf "\n"

echo "Waiting tfs-child ..."
kubectl wait --namespace tfs-child --for='condition=available' --timeout=300s deployment/contextservice
kubectl wait --namespace tfs-child --for='condition=available' --timeout=300s deployment/deviceservice
kubectl wait --namespace tfs-child --for='condition=available' --timeout=300s deployment/pathcompservice
kubectl wait --namespace tfs-child --for='condition=available' --timeout=300s deployment/serviceservice
kubectl wait --namespace tfs-child --for='condition=available' --timeout=300s deployment/sliceservice
kubectl wait --namespace tfs-child --for='condition=available' --timeout=300s deployment/webuiservice
printf "\n"

echo "Done!"
