#!/usr/bin/env bash
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

docker stop firewall-agent || true
docker rm firewall-agent || true

docker build --tag "firewall-agent:dev" .
docker run --detach --name firewall-agent --cap-add=NET_ADMIN --network host --publish 8888:8888 firewall-agent:dev

docker logs --follow firewall-agent
