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


set -euo pipefail

echo "Starting demo stack with docker compose..."
docker compose -f docker-compose.yml up -d --build

echo "Waiting a few seconds for services to become healthy..."
sleep 3

echo "You can now run: python3 install_acls.py --ports 8001,8002"
echo "Services started. HTTP servers: http://localhost:8001 and http://localhost:8002."
echo "Firewall agent RESTCONF: http://localhost:8888/restconf/data"
