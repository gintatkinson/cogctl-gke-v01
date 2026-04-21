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
FROM us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs/python-base:2026-04-21

# Copy context and webui
COPY baseline/tfs-controller/src/common/ /var/teraflow/common/
COPY baseline/tfs-controller/src/webui/ /var/teraflow/webui/
COPY baseline/tfs-controller/proto/ /var/teraflow/proto/

# Phase 7.16: Autonomous Build-Time Gencode Synthesis
WORKDIR /var/teraflow/proto
RUN python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. *.proto
RUN sed -i -E 's/^import ([^ ]*)_pb2/from . import \1_pb2/g' *_pb2*.py

# Phase 7.34: Namespace Cleansing & Routing Reconciliation
RUN rm -rf /var/teraflow/common/proto && \
    mkdir -p /var/teraflow/common/proto && \
    cp -r /var/teraflow/proto/* /var/teraflow/common/proto/ && \
    touch /var/teraflow/common/proto/__init__.py

WORKDIR /var/teraflow/webui
# Standardize logs and entrypoint
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "-m", "webui.service"]
