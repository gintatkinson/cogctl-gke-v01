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
echo "Destroying in ${HOSTNAME}..."


case "$HOSTNAME" in
    simap-server)
        echo "Cleaning up..."
        docker rm --force simap-server
        docker rm --force nce-fan-ctrl
        docker rm --force nce-t-ctrl
        docker rm --force traffic-changer

        sleep 2
        docker ps -a
        ;;
    tfs-e2e-ctrl)
        echo "Destroying TFS E2E Controller..."
        source ~/tfs-ctrl/src/tests/ecoc25-f5ga-telemetry/deploy-specs-e2e.sh
        kubectl delete namespace $TFS_K8S_NAMESPACE
        ;;
    tfs-agg-ctrl)
        echo "Destroying TFS Agg Controller..."
        source ~/tfs-ctrl/src/tests/ecoc25-f5ga-telemetry/deploy-specs-agg.sh
        kubectl delete namespace $TFS_K8S_NAMESPACE
        ;;
    tfs-ip-ctrl)
        echo "Destroying TFS IP Controller..."
        source ~/tfs-ctrl/src/tests/ecoc25-f5ga-telemetry/deploy-specs-ip.sh
        kubectl delete namespace $TFS_K8S_NAMESPACE
        ;;
    *)
        echo "Unknown host: $HOSTNAME"
        echo "No commands to run."
        ;;
esac

echo "Ready!"
