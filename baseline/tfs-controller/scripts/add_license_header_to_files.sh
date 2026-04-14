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


docker pull ghcr.io/google/addlicense:latest
docker run -it -v ${PWD}:/src ghcr.io/google/addlicense \
    -l apache -c "ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)" -y 2022-2025 \
    -ignore "data/*" -ignore "data/**" -ignore "tmp/*" -ignore "tmp/**" -ignore "manifests/cttc-ols/*" \
    -ignore "coverage/*" -ignore "coverage/**" -ignore ".vscode/*" -ignore ".vscode/**" \
    -ignore ".git/*" -ignore ".git/**" -ignore "proto/uml/*" -ignore "proto/uml/**" \
    -ignore "src/**/__pycache__/*" -ignore "src/**/__pycache__/**" \
    -ignore "src/.benchmarks/*" -ignore "src/.benchmarks/**" -ignore ".benchmarks/*" -ignore ".benchmarks/**" \
    -ignore "src/.pytest_cache/*" -ignore "src/.pytest_cache/**" -ignore ".pytest_cache/*" -ignore ".pytest_cache/**" \
    -ignore "src/**/target/generated-sources/grpc/*" -ignore "src/**/target/generated-sources/grpc/**" \
    -ignore "src/**/*_pb2.py" -ignore "src/**/*_pb2_grpc.py" \
    -ignore "src/device/service/drivers/gnmi_openconfig/gnmi/*.proto" \
    -ignore "src/device/service/drivers/openconfig/templates/**/*.xml" \
    -ignore "src/device/service/drivers/openconfig/templates/ACL/openconfig_acl.py" \
    -ignore "src/device/service/drivers/openconfig/templates/VPN/openconfig_interfaces.py" \
    -ignore "src/device/service/drivers/openconfig/templates/VPN/openconfig_network_instance.py" \
    -ignore "src/device/service/drivers/openconfig/templates/VPN/openconfig_routing_policy.py" \
    -ignore "src/nbi/service/ietf_network/bindings/**/*.py" \
    -ignore "src/policy/target/kubernetes/kubernetes.yml" \
    -ignore "src/ztp/target/kubernetes/kubernetes.yml" \
    -ignore "src/**/.mvn/*" -ignore "src/**/.mvn/**" \
    -ignore "hackfest/**/*_pb2.py" -ignore "hackfest/**/*_pb2_grpc.py" \
    -ignore "hackfest/netconf/**/binding_*.py" -ignore "hackfest/netconf/**/binding_*.py" \
    -ignore "hackfest/yang/**/binding_*.py" -ignore "hackfest/yang/**/binding_*.py" \
    -ignore "hackfest/netconf-oc/openconfig/*" -ignore "hackfest/netconf-oc/openconfig/**" \
    -ignore "hackfest/restconf/connectionserver/*" -ignore "hackfest/restconf/connectionserver/**" \
    -ignore "hackfest/restconf/topologyserver/*" -ignore "hackfest/restconf/topologyserver/**" \
    -ignore "hackfest/tapi/server/*" -ignore "hackfest/tapi/server/**" \
    *
