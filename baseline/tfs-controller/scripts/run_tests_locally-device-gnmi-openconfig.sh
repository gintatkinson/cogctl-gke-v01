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

# Run unitary tests and analyze coverage of code at same time
# helpful pytest flags: --log-level=INFO -o log_cli=true --verbose --maxfail=1 --durations=0
coverage run --rcfile=$RCFILE --append -m pytest --log-level=INFO --verbose \
    device/tests/gnmi_openconfig/test_unitary_gnmi_openconfig.py
