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

TEST_NAME="ofc24"


echo
echo "Clean-up:"
echo "---------"
docker rm -f na-t1 na-t2 na-r1 na-r2
docker network rm na-br


echo
echo "Pull Docker images:"
echo "-------------------"
docker pull asgamb1/oc23bgp.img:latest
docker pull asgamb1/flexscale-node.img:latest


echo
echo "Create Management Network and Node Agents:"
echo "------------------------------------------"
docker network create -d bridge --subnet=172.254.253.0/24 --gateway=172.254.253.254 --ip-range=172.254.253.0/24 na-br
docker run -dit --init --name na-t1 --network=na-br --ip 172.254.253.101 --publish 2022 \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/startNetconfAgent-tp.sh:/confd/examples.confd/OC23/startNetconfAgent.sh" \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/platform_t1.xml:/confd/examples.confd/OC23/platform.xml" \
    asgamb1/oc23bgp.img:latest /confd/examples.confd/OC23/startNetconfAgent.sh
docker run -dit --init --name na-t2 --network=na-br --ip 172.254.253.102 --publish 2022 \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/startNetconfAgent-tp.sh:/confd/examples.confd/OC23/startNetconfAgent.sh" \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/platform_t2.xml:/confd/examples.confd/OC23/platform.xml" \
    asgamb1/oc23bgp.img:latest /confd/examples.confd/OC23/startNetconfAgent.sh
docker run -dit --init --name na-r1 --network=na-br --ip 172.254.253.201 --publish 2022 \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/startNetconfAgent-mg-on.sh:/confd/examples.confd/OC23/startNetconfAgent.sh" \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/platform_r1.xml:/confd/examples.confd/OC23/platform.xml" \
    asgamb1/flexscale-node.img:latest /confd/examples.confd/OC23/startNetconfAgent.sh
docker run -dit --init --name na-r2 --network=na-br --ip 172.254.253.202 --publish 2022 \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/startNetconfAgent-mg-on.sh:/confd/examples.confd/OC23/startNetconfAgent.sh" \
    --volume "$PWD/src/tests/${TEST_NAME}/node-agents-config/platform_r2.xml:/confd/examples.confd/OC23/platform.xml" \
    asgamb1/flexscale-node.img:latest /confd/examples.confd/OC23/startNetconfAgent.sh


echo
echo "Waiting for initialization..."
echo "-----------------------------"
docker ps -a
while ! docker logs na-t1 2>&1 | grep -q '*** ConfD OpenConfig NETCONF agent ***'; do sleep 1; done
while ! docker logs na-t2 2>&1 | grep -q '*** ConfD OpenConfig NETCONF agent ***'; do sleep 1; done
while ! docker logs na-r1 2>&1 | grep -q '*** ConfD OpenConfig NETCONF agent ***'; do sleep 1; done
while ! docker logs na-r2 2>&1 | grep -q '*** ConfD OpenConfig NETCONF agent ***'; do sleep 1; done
sleep 3
docker ps -a


echo
echo "Dump Node Agent status:"
echo "-----------------------"
docker ps -a
docker logs na-t1
docker logs na-t2
docker logs na-r1
docker logs na-r2


echo "Done!"
