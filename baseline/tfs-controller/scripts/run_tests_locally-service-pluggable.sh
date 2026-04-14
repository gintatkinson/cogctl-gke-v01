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

# to run integration test: -m integration
python3 -m pytest --log-level=info --log-cli-level=info --verbose -m "not integration" \
    pluggables/tests/test_pluggables_with_SBI.py
# python3 -m pytest --log-level=info --log-cli-level=info --verbose \
#     pluggables/tests/test_Pluggables.py

echo "Bye!"
