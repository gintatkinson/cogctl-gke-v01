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

# build the software
# uncomment the line below if you want to build it
# cargo build --release --target=x86_64-unknown-linux-musl

# build a .env file with the info from context and monitoring services

if [ -z "${CONTEXTSERVICE_SERVICE_HOST}" ] || [ -z "${CONTEXTSERVICE_SERVICE_PORT_GRPC}" ] || \
   [ -z "${MONITORINGSERVICE_SERVICE_HOST}" ] || [ -z "${MONITORINGSERVICE_SERVICE_PORT_GRPC}" ]
then
    echo "TFS_ENV_VARS are not loaded."
    exit 1
fi

echo "CONTEXTSERVICE_SERVICE_HOST=${CONTEXTSERVICE_SERVICE_HOST}" > .env
echo "CONTEXTSERVICE_SERVICE_PORT_GRPC=${CONTEXTSERVICE_SERVICE_PORT_GRPC}" >> .env
echo "MONITORINGSERVICE_SERVICE_HOST=${MONITORINGSERVICE_SERVICE_HOST}" >> .env
echo "MONITORINGSERVICE_SERVICE_PORT_GRPC=${MONITORINGSERVICE_SERVICE_PORT_GRPC}" >> .env

# get container id
CONTAINER=`docker ps | grep mininet | cut -f1 -d" "`
docker cp target/x86_64-unknown-linux-musl/release/tfsping $CONTAINER:/root
docker cp target/x86_64-unknown-linux-musl/release/tfsagent $CONTAINER:/root
docker cp .env $CONTAINER:/root
