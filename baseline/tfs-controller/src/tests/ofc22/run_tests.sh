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

# Run functional tests
source tfs_runtime_env_vars.sh
pytest --verbose --log-level=INFO src/tests/ofc22/tests/test_functional_bootstrap.py
pytest --verbose --log-level=INFO src/tests/ofc22/tests/test_functional_create_service.py
pytest --verbose --log-level=INFO src/tests/ofc22/tests/test_functional_delete_service.py
pytest --verbose --log-level=INFO src/tests/ofc22/tests/test_functional_cleanup.py
