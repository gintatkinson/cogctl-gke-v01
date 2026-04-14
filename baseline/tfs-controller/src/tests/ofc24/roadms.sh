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

         
docker stop -t 1 na3
docker stop -t 1 na4

docker rm na3
docker rm na4



screen -dmS t3 -T xterm sh -c "docker run --name na3  -p  10.0.2.4:2025:2022 -v /home/tfs/tfs-ctrl/src/tests/ofc24/tempOC/files:/files  -it asgamb1/flexscale-node.img:latest bash -c 'cp /files/platform_r1.xml demoECOC21.xml ; ./startNetconfAgent.sh'"
#screen -dmS t4 -T xterm sh -c "docker run --name na4  -p  10.0.2.4:2026:2022 -v /home/tfs/tfs-ctrl/src/tests/ofc24/tempOC/files:/files  -it asgamb1/flexscale-node.img:latest bash -c 'cp /files/platform_r2.xml demoECOC21.xml ; ./startNetconfAgent.sh'"
