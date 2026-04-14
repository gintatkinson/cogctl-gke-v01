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

IMAGE_NAME="asgamb1/oc23bgp.img:latest"
DOCKER_CONTAINER=$1
DOCKER_PORT="2022"

sudo docker stop na1 -t 1
sudo docker stop na2 -t 1
sudo docker stop na3 -t 1
sudo docker stop na4 -t 1

sudo docker rm na2
sudo docker rm na1
sudo docker rm na3
sudo docker rm na4

echo "Creating Transponder Agents"

 ./startExtraNetConfigAgent.sh


echo "Creating Roadms Agents"


screen -dmS t3 -T xterm sh -c 'docker run -p 10.0.2.4:2025:2022 -v  ~/tfs-ctrl/src/tests/ofc24/tempOC/files:/files --name na3 -it asgamb1/flexscale-node.img:latest bash '
screen -dmS t4 -T xterm sh -c 'docker run -p 10.0.2.4:2026:2022 -v  ~/tfs-ctrl/src/tests/ofc24/tempOC/files:/files --name na4 -it asgamb1/flexscale-node.img:latest bash '
sleep 4

echo "starting Roadm1 "

if [ "$( docker container  inspect -f '{{.State.Running}}' na4)" = "true" ]; then 
        docker exec  na4   sh -c " cp /files/platform_r2.xml init_openconfig-platform.xml; 
                                  cp /files/startNetconfAgent.sh startNetconfAgent.sh;
                                  /confd/examples.confd/OC23/startNetconfAgent.sh ;"&
      
else 
        echo "na4  is not running yet"
fi


echo "starting Roadm2 "



if [ "$( docker container  inspect -f '{{.State.Running}}' na3)" = "true" ]; then 
        docker exec  na3 sh -c " cp /files/platform_r1.xml init_openconfig-platform.xml;
                                 cp /files/startNetconfAgent.sh startNetconfAgent.sh;
                                 /confd/examples.confd/OC23/startNetconfAgent.sh; " 

else 
        echo "na3  is not running yet"
fi


# screen -S t3 -X stuff "cp ~/files/platform_r1.xml /confd/examples.confd/OC23/init_openconfig-platform.xml && ./startNetconfAgent.sh"
# bash -c "docker  cp  ~/tfs-ctrl/src/tests/ofc24/tempOC/files/platform_r2.xml na4:/confd/examples.confd/OC23/init_openconfig-platform.xml;
#  docker  cp   ~/tfs-ctrl/src/tests/ofc24/tempOC/files/startNetconfAgent.sh na4:/confd/examples.confd/OC23/startNetconfAgent.sh;"
