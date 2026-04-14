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
# limitations under the License

docker stop na1 
docker rm na1
screen -dmS t1 -T xterm sh -c "docker run -p 10.0.2.10:2023:2022 -v ~/tfs-ctrl/src/tests/ofc24/tempOC/files:/files --name na1 -it asgamb1/oc23bgp.img:latest"              
sleep  2
if [ "$( docker container  inspect -f '{{.State.Running}}' na1)" = "true" ]; then
      docker exec na1 sh -c " cp /files/platform_t1.xml demoECOC21.xml ; /confd/examples.confd/OC23/startNetconfAgent.sh; "
else
      echo "your container is not running yet"
fi
