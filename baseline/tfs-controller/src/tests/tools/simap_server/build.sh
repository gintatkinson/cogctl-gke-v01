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

# Make folder containing the script the root folder for its execution
cd $(dirname $0)/../../../../

# Build image SIMAP Server
docker buildx build -t simap-server:test -f ./src/tests/tools/simap_server/Dockerfile .
#docker tag simap-server:test localhost:32000/tfs/simap-server:test
#docker push localhost:32000/tfs/simap-server:test
