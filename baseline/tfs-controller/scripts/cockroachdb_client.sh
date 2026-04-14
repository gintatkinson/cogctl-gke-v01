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


########################################################################################################################
# Read deployment settings
########################################################################################################################

# If not already set, set the namespace where CockroackDB will be deployed.
export CRDB_NAMESPACE=${CRDB_NAMESPACE:-"crdb"}

# If not already set, set the database username to be used by Context.
export CRDB_USERNAME=${CRDB_USERNAME:-"tfs"}

# If not already set, set the database user's password to be used by Context.
export CRDB_PASSWORD=${CRDB_PASSWORD:-"tfs123"}

# If not already set, set CockroachDB installation mode. Accepted values are: 'single' and 'cluster'.
export CRDB_DEPLOY_MODE=${CRDB_DEPLOY_MODE:-"single"}


########################################################################################################################
# Automated steps start here
########################################################################################################################

if [ "$CRDB_DEPLOY_MODE" == "single" ]; then
    CRDB_SQL_PORT=$(kubectl --namespace ${CRDB_NAMESPACE} get service cockroachdb-public -o 'jsonpath={.spec.ports[?(@.name=="sql")].port}')
    CRDB_CLIENT_URL="postgresql://${CRDB_USERNAME}:${CRDB_PASSWORD}@cockroachdb-0:${CRDB_SQL_PORT}/defaultdb?sslmode=require"
    kubectl exec -it --namespace ${CRDB_NAMESPACE} cockroachdb-0 -- \
        ./cockroach sql --certs-dir=/cockroach/cockroach-certs --url=${CRDB_CLIENT_URL}
elif [ "$CRDB_DEPLOY_MODE" == "cluster" ]; then
    kubectl exec -it --namespace ${CRDB_NAMESPACE} cockroachdb-client-secure -- \
        ./cockroach sql --certs-dir=/cockroach/cockroach-certs --host=cockroachdb-public
else
    echo "Unsupported value: CRDB_DEPLOY_MODE=$CRDB_DEPLOY_MODE"
fi
