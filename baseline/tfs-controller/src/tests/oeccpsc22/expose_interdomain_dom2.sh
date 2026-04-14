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

PATCH='{"data": {"10010": "tfs-dom2/interdomainservice:10010"}}'
kubectl patch configmap nginx-ingress-tcp-microk8s-conf-dom2 --namespace ingress --patch "${PATCH}"

CONTAINER='{"name": "nginx-ingress-microk8s", "ports": [{"containerPort": 10010, "hostPort": 10010, "protocol": "TCP"}]}'
PATCH='{"spec": {"template": {"spec": {"containers": ['${CONTAINER}']}}}}'
kubectl patch daemonset nginx-ingress-microk8s-controller-dom2 --namespace ingress --patch "${PATCH}"
