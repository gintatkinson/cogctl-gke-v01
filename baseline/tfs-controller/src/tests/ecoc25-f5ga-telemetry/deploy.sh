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


# Assuming the instances are named as: simap-server, tfs-e2e-ctrl, tfs-agg-ctrl, tfs-ip-ctrl

# Get the current hostname
HOSTNAME=$(hostname)
echo "Deploying in ${HOSTNAME}..."


case "$HOSTNAME" in
    simap-server)
        echo "Building SIMAP Server..."
        cd ~/tfs-ctrl/
        docker buildx build -t simap-server:mock -f ./src/tests/tools/simap_server/Dockerfile .

        echo "Building NCE-FAN Controller..."
        cd ~/tfs-ctrl/
        docker buildx build -t nce-fan-ctrl:mock -f ./src/tests/tools/mock_nce_fan_ctrl/Dockerfile .

        echo "Building NCE-T Controller..."
        cd ~/tfs-ctrl/
        docker buildx build -t nce-t-ctrl:mock -f ./src/tests/tools/mock_nce_t_ctrl/Dockerfile .

        echo "Building Traffic Changer..."
        cd ~/tfs-ctrl/
        docker buildx build -t traffic-changer:mock -f ./src/tests/tools/traffic_changer/Dockerfile .

        echo "Cleaning up..."
        docker rm --force simap-server
        docker rm --force nce-fan-ctrl
        docker rm --force nce-t-ctrl
        docker rm --force traffic-changer

        echo "Deploying support services..."
        docker run --detach --name simap-server    --publish 8080:8080 simap-server:mock
        docker run --detach --name nce-fan-ctrl    --publish 8081:8080 --env SIMAP_ADDRESS=172.17.0.1 --env SIMAP_PORT=8080 nce-fan-ctrl:mock
        docker run --detach --name nce-t-ctrl      --publish 8082:8080 --env SIMAP_ADDRESS=172.17.0.1 --env SIMAP_PORT=8080 nce-t-ctrl:mock
        docker run --detach --name traffic-changer --publish 8083:8080 traffic-changer:mock

        sleep 2
        docker ps -a
        ;;
    tfs-e2e-ctrl)
        echo "Deploying TFS E2E Controller..."
        sed -i 's|\(<h2>ETSI TeraFlowSDN Controller\)</h2>|\1 (End-to-End)</h2>|' src/webui/service/templates/main/home.html
        source ~/tfs-ctrl/src/tests/ecoc25-f5ga-telemetry/deploy-specs-e2e.sh
        ./deploy/all.sh

        echo "Waiting for NATS connection..."
        while ! kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server 2>&1 | grep -q 'Subscriber is Ready? True'; do sleep 1; done
        kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server
        ;;
    tfs-agg-ctrl)
        echo "Deploying TFS Agg Controller..."
        sed -i 's|\(<h2>ETSI TeraFlowSDN Controller\)</h2>|\1 (Aggregation)</h2>|' src/webui/service/templates/main/home.html
        source ~/tfs-ctrl/src/tests/ecoc25-f5ga-telemetry/deploy-specs-agg.sh
        ./deploy/all.sh

        echo "Waiting for NATS connection..."
        while ! kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server 2>&1 | grep -q 'Subscriber is Ready? True'; do sleep 1; done
        kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server
        ;;
    tfs-ip-ctrl)
        echo "Deploying TFS IP Controller..."
        sed -i 's|\(<h2>ETSI TeraFlowSDN Controller\)</h2>|\1 (IP)</h2>|' src/webui/service/templates/main/home.html
        source ~/tfs-ctrl/src/tests/ecoc25-f5ga-telemetry/deploy-specs-ip.sh
        ./deploy/all.sh

        echo "Waiting for NATS connection..."
        while ! kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server 2>&1 | grep -q 'Subscriber is Ready? True'; do sleep 1; done
        kubectl --namespace $TFS_K8S_NAMESPACE logs deployment/contextservice -c server
        ;;
    *)
        echo "Unknown host: $HOSTNAME"
        echo "No commands to run."
        ;;
esac

echo "Ready!"
