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

# Configure the correct folder on the .coveragerc file
cat $PROJECTDIR/coverage/.coveragerc.template | sed s+~/teraflow/controller+$PROJECTDIR+g > $RCFILE

# Destroy old coverage file
rm -f $COVERAGEFILE

# Force a flush of Context database
kubectl --namespace $TFS_K8S_NAMESPACE exec -it deployment/contextservice --container redis -- redis-cli FLUSHALL

source tfs_runtime_env_vars.sh

# Run functional tests and analyze code coverage at the same time
coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    tests/ofc22/tests/test_functional_bootstrap.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    tests/ofc22/tests/test_functional_create_service.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    tests/ofc22/tests/test_functional_delete_service.py

coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    tests/ofc22/tests/test_functional_cleanup.py
