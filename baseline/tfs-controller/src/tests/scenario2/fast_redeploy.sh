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


kubectl delete namespace tfs-dom1 tfs-dom2 tfs-dom3 tfs-dom4

echo "Deploying tfs-dom1 ..."
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom1.yaml                 > ./tmp/logs/deploy-tfs-dom1.log
kubectl create namespace tfs-dom1                                             > ./tmp/logs/deploy-tfs-dom1.log
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom1.yaml                  > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/contextservice.yaml     > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/deviceservice.yaml      > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/pathcompservice.yaml    > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/serviceservice.yaml     > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/sliceservice.yaml       > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/dltservice.yaml         > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/interdomainservice.yaml > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f ./tmp/manifests/webuiservice.yaml       > ./tmp/logs/deploy-tfs-dom1.log
kubectl --namespace tfs-dom1 apply -f nfvsdn22/tfs-ingress-dom1.yaml          > ./tmp/logs/deploy-tfs-dom1.log
printf "\n"

echo "Deploying tfs-dom2 ..."
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom2.yaml                 > ./tmp/logs/deploy-tfs-dom2.log
kubectl create namespace tfs-dom2                                             > ./tmp/logs/deploy-tfs-dom2.log
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom2.yaml                  > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/contextservice.yaml     > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/deviceservice.yaml      > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/pathcompservice.yaml    > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/serviceservice.yaml     > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/sliceservice.yaml       > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/dltservice.yaml         > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/interdomainservice.yaml > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f ./tmp/manifests/webuiservice.yaml       > ./tmp/logs/deploy-tfs-dom2.log
kubectl --namespace tfs-dom2 apply -f nfvsdn22/tfs-ingress-dom2.yaml          > ./tmp/logs/deploy-tfs-dom2.log
printf "\n"

echo "Deploying tfs-dom3 ..."
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom3.yaml                 > ./tmp/logs/deploy-tfs-dom3.log
kubectl create namespace tfs-dom3                                             > ./tmp/logs/deploy-tfs-dom3.log
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom3.yaml                  > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/contextservice.yaml     > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/deviceservice.yaml      > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/pathcompservice.yaml    > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/serviceservice.yaml     > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/sliceservice.yaml       > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/dltservice.yaml         > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/interdomainservice.yaml > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f ./tmp/manifests/webuiservice.yaml       > ./tmp/logs/deploy-tfs-dom3.log
kubectl --namespace tfs-dom3 apply -f nfvsdn22/tfs-ingress-dom3.yaml          > ./tmp/logs/deploy-tfs-dom3.log
printf "\n"

echo "Deploying tfs-dom4 ..."
kubectl delete -f nfvsdn22/nginx-ingress-controller-dom4.yaml                 > ./tmp/logs/deploy-tfs-dom4.log
kubectl create namespace tfs-dom4                                             > ./tmp/logs/deploy-tfs-dom4.log
kubectl apply -f nfvsdn22/nginx-ingress-controller-dom4.yaml                  > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/contextservice.yaml     > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/deviceservice.yaml      > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/pathcompservice.yaml    > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/serviceservice.yaml     > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/sliceservice.yaml       > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/dltservice.yaml         > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/interdomainservice.yaml > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f ./tmp/manifests/webuiservice.yaml       > ./tmp/logs/deploy-tfs-dom4.log
kubectl --namespace tfs-dom4 apply -f nfvsdn22/tfs-ingress-dom4.yaml          > ./tmp/logs/deploy-tfs-dom4.log
printf "\n"

echo "Waiting tfs-dom1 ..."
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/contextservice
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/deviceservice
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/pathcompservice
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/serviceservice
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/sliceservice
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/dltservice
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/interdomainservice
kubectl wait --namespace tfs-dom1 --for='condition=available' --timeout=300s deployment/webuiservice
printf "\n"

echo "Waiting tfs-dom2 ..."
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/contextservice
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/deviceservice
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/pathcompservice
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/serviceservice
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/sliceservice
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/dltservice
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/interdomainservice
kubectl wait --namespace tfs-dom2 --for='condition=available' --timeout=300s deployment/webuiservice
printf "\n"

echo "Waiting tfs-dom3 ..."
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/contextservice
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/deviceservice
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/pathcompservice
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/serviceservice
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/sliceservice
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/dltservice
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/interdomainservice
kubectl wait --namespace tfs-dom3 --for='condition=available' --timeout=300s deployment/webuiservice
printf "\n"

echo "Waiting tfs-dom4 ..."
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/contextservice
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/deviceservice
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/pathcompservice
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/serviceservice
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/sliceservice
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/dltservice
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/interdomainservice
kubectl wait --namespace tfs-dom4 --for='condition=available' --timeout=300s deployment/webuiservice
printf "\n"

echo "Done!"
