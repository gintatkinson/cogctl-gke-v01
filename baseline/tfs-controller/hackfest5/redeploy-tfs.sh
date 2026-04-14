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

source ~/tfs-ctrl/hackfest5/deploy_specs.sh

echo "Cleaning-up old NATS and Kafka deployments..."
helm3 uninstall --namespace ${NATS_NAMESPACE} ${NATS_NAMESPACE}
kubectl delete namespace ${NATS_NAMESPACE} --ignore-not-found
kubectl delete namespace kafka --ignore-not-found
printf "\n"

echo "Deployting TeraFlowSDN..."

# Deploy CockroachDB
./deploy/crdb.sh

# Deploy NATS
./deploy/nats.sh

# Deploy QuestDB
./deploy/qdb.sh

# Expose Dashboard
./deploy/expose_dashboard.sh

# Deploy TeraFlowSDN
./deploy/tfs.sh

# Show deploy summary
./deploy/show.sh

printf "\n"

echo "Waiting for Context to be subscribed to NATS..."
while ! kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server 2>&1 | grep -q 'Subscriber is Ready? True'; do
    printf "%c" "."
    sleep 1
done
kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server
printf "\n"
