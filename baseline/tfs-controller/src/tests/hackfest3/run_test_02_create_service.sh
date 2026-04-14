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

source tfs_runtime_env_vars.sh
python -m pytest --verbose src/tests/hackfest3/tests/test_functional_create_service.py

# To enable debugging use the following options
#python -m pytest --verbose -o log_cli=true -o log_cli_level=DEBUG src/tests/hackfest3/tests/test_functional_create_service.py
