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

# PHASE 2: Gold Master Refactor
FROM us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs/python-base:2026-04-20

# Add component code
WORKDIR /var/teraflow
COPY baseline/tfs-controller/src/ .
COPY baseline/tfs-controller/proto/ proto/

# PHASE 7.16: Autonomous Build-Time Synthesis
# This ensures 100% architectural parity with the pinned library versions
RUN mkdir -p /var/teraflow/common/proto && \
    python3 -m grpc_tools.protoc -I=./proto --python_out=common/proto --grpc_python_out=common/proto ./proto/*.proto && \
    touch common/proto/__init__.py && \
    find common/proto -type f -iname "*.py" -exec sed -i -E 's/^(import\ .*)_pb2/from . \1_pb2/g' {} +

# Reconcile the common/proto link to point to the freshly synthesized floor
RUN rm -rf common/proto_old && mv common/proto common/proto_new && ln -s /var/teraflow/common/proto_new common/proto

# Standardize logs and entrypoint
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/var/teraflow
ENTRYPOINT ["python", "-m", "webui.service"]
