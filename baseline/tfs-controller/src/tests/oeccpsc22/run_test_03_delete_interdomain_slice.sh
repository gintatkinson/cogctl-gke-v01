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


PROJECTDIR=`pwd`

cd $PROJECTDIR/src
RCFILE=$PROJECTDIR/coverage/.coveragerc
COVERAGEFILE=$PROJECTDIR/coverage/.coverage

# Set the name of the Kubernetes namespace and hostname to use.
K8S_NAMESPACE_D1="oeccpsc22-1"
K8S_NAMESPACE_D2="oeccpsc22-2"
# dynamically gets the name of the K8s master node
K8S_HOSTNAME=`kubectl get nodes --selector=node-role.kubernetes.io/master | tr -s " " | cut -f1 -d" " | sed -n '2 p'`

export D1_CONTEXTSERVICE_SERVICE_HOST=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export D1_CONTEXTSERVICE_SERVICE_PORT_GRPC=$(kubectl get service contextservice-public --namespace $K8S_NAMESPACE_D1 -o 'jsonpath={.spec.ports[?(@.port==1010)].nodePort}')
export D1_DEVICESERVICE_SERVICE_HOST=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export D1_DEVICESERVICE_SERVICE_PORT_GRPC=$(kubectl get service deviceservice-public --namespace $K8S_NAMESPACE_D1 -o 'jsonpath={.spec.ports[?(@.port==2020)].nodePort}')
export D1_NBISERVICE_SERVICE_HOST=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export D1_NBISERVICE_SERVICE_PORT_HTTP=$(kubectl get service nbiservice-public --namespace $K8S_NAMESPACE_D1 -o 'jsonpath={.spec.ports[?(@.port==8080)].nodePort}')

export D2_CONTEXTSERVICE_SERVICE_HOST=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export D2_CONTEXTSERVICE_SERVICE_PORT_GRPC=$(kubectl get service contextservice-public --namespace $K8S_NAMESPACE_D2 -o 'jsonpath={.spec.ports[?(@.port==1010)].nodePort}')
export D2_DEVICESERVICE_SERVICE_HOST=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export D2_DEVICESERVICE_SERVICE_PORT_GRPC=$(kubectl get service deviceservice-public --namespace $K8S_NAMESPACE_D2 -o 'jsonpath={.spec.ports[?(@.port==2020)].nodePort}')
export D2_NBISERVICE_SERVICE_HOST=$(kubectl get node $K8S_HOSTNAME -o 'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}')
export D2_NBISERVICE_SERVICE_PORT_HTTP=$(kubectl get service nbiservice-public --namespace $K8S_NAMESPACE_D2 -o 'jsonpath={.spec.ports[?(@.port==8080)].nodePort}')

# Useful flags for pytest:
#-o log_cli=true -o log_file=device.log -o log_file_level=DEBUG

# Run functional test and analyze coverage of code at same time

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    tests/oeccpsc22/tests/test_functional_delete_interdomain_slice.py
