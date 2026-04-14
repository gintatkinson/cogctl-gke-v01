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

export KFK_SERVER_ADDRESS='127.0.0.1:9092'
CRDB_SQL_ADDRESS=$(kubectl get service cockroachdb-public --namespace crdb -o jsonpath='{.spec.clusterIP}')
export CRDB_URI="cockroachdb://tfs:tfs123@${CRDB_SQL_ADDRESS}:26257/tfs_analytics?sslmode=require"

python3 -m pytest --log-level=DEBUG --log-cli-level=INFO --verbose \
    analytics/frontend/tests/test_frontend.py
