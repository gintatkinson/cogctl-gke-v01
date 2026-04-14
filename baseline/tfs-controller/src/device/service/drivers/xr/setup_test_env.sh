#!/bin/sh
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

export CONTEXTSERVICE_SERVICE_HOST=$(kubectl get service/contextservice --namespace tfs  --template '{{.spec.clusterIP}}')
export CONTEXTSERVICE_SERVICE_PORT_GRPC=$(kubectl get service/contextservice --namespace tfs  -o jsonpath='{.spec.ports[?(@.name=="grpc")].port}')
export NBISERVICE_SERVICE_HOST=$(kubectl get service/nbiservice --namespace tfs  --template '{{.spec.clusterIP}}')
export NBISERVICE_SERVICE_PORT_HTTP=$(kubectl get service/nbiservice --namespace tfs  -o jsonpath='{.spec.ports[?(@.name=="http")].port}')
export SERVICESERVICE_SERVICE_HOST=$(kubectl get service/serviceservice --namespace tfs  --template '{{.spec.clusterIP}}')
export SERVICESERVICE_SERVICE_PORT_GRPC=$(kubectl get service/serviceservice --namespace tfs  -o jsonpath='{.spec.ports[?(@.name=="grpc")].port}')
echo "CONTEXTSERVICE_SERVICE_HOST=$CONTEXTSERVICE_SERVICE_HOST"
echo "CONTEXTSERVICE_SERVICE_PORT_GRPC=$CONTEXTSERVICE_SERVICE_PORT_GRPC"
echo "NBISERVICE_SERVICE_HOST=$NBISERVICE_SERVICE_HOST"
echo "NBISERVICE_SERVICE_PORT_HTTP=$NBISERVICE_SERVICE_PORT_HTTP"
echo "SERVICESERVICE_SERVICE_HOST=$SERVICESERVICE_SERVICE_HOST"
echo "SERVICESERVICE_SERVICE_PORT_GRPC=$SERVICESERVICE_SERVICE_PORT_GRPC"
