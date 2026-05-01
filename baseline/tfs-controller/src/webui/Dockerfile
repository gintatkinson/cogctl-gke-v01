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
FROM us-central1-docker.pkg.dev/cogctl-gke-v01/sovereign-tfs/python-base:rc13-verified

# Copy necessary components
COPY src/context/ /var/teraflow/context/
COPY src/service/ /var/teraflow/service/
COPY src/webui/ /var/teraflow/webui/
COPY proto/ /var/teraflow/proto/

# Standardize logs and entrypoint
WORKDIR /var/teraflow/proto
RUN python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. *.proto
RUN sed -i -E 's/^import ([^ ]*)_pb2/from . import \1_pb2/g' *_pb2*.py

# Move to common/proto
RUN mkdir -p /var/teraflow/common/proto && \
    cp *_pb2* /var/teraflow/common/proto/ && \
    touch /var/teraflow/common/proto/__init__.py

WORKDIR /var/teraflow
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/var/teraflow
ENTRYPOINT ["python", "-m", "webui.service"]

