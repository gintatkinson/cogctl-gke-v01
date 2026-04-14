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

# Deploy TeraFlowSDN with L3 Cybersecurity Components for Attack Detection and Mitigation
echo "Deploying TFS with L3 Cybersecurity Components for Attack Detection and Mitigation..."
./deploy.sh
echo "TFS deployed."

# Deploy Distributed Attack Detector
if $DAD_NODE_PASSWORD == "" || $DAD_NODE_IP == ""; then
    echo "Please set the DAD_NODE_PASSWORD and DAD_NODE_IP environment variables."
    exit 1
fi

echo "Deploying Distributed Attack Detector..."
sshpass -p $DAD_NODE_PASSWORD ssh -o StrictHostKeyChecking=no -n -f ubuntu@$DAD_NODE_IP "sh -c 'nohup /home/ubuntu/TeraflowDockerDistributed/restart.sh > /dev/null 2>&1 &'"
echo "Distributed Attack Detector deployed."