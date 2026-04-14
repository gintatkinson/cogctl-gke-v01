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

FROM python:3.9-slim

# Install dependencies
RUN apt-get --yes --quiet --quiet update && \
    apt-get --yes --quiet --quiet install wget g++ && \
    rm -rf /var/lib/apt/lists/*

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Download the gRPC health probe
RUN GRPC_HEALTH_PROBE_VERSION=v0.2.0 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe

# Creating a user for security reasons
RUN groupadd -r teraflow && useradd -u 1001 --no-log-init -r -m -g teraflow teraflow
USER teraflow

# set working directory
RUN mkdir -p /home/teraflow/controller/common/
WORKDIR /home/teraflow/controller

# Get Python packages per module
ENV VIRTUAL_ENV=/home/teraflow/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Get generic Python packages
RUN python3 -m pip install --upgrade 'pip==25.2'
RUN python3 -m pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
RUN python3 -m pip install --upgrade 'pip-tools==7.3.0'

# Get common Python packages
# Note: this step enables sharing the previous Docker build steps among all the Python components
COPY --chown=teraflow:teraflow common_requirements.in common_requirements.in
RUN pip-compile --quiet --output-file=common_requirements.txt common_requirements.in
RUN python3 -m pip install -r common_requirements.txt

# Add common files into working directory
WORKDIR /home/teraflow/controller/common
COPY --chown=teraflow:teraflow src/common/. ./
RUN rm -rf proto

# Create proto sub-folder, copy .proto files, and generate Python code
RUN mkdir -p /home/teraflow/controller/common/proto
WORKDIR /home/teraflow/controller/common/proto
RUN touch __init__.py
COPY --chown=teraflow:teraflow proto/*.proto ./
RUN python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. *.proto
RUN rm *.proto
RUN find . -type f -exec sed -i -E 's/^(import\ .*)_pb2/from . \1_pb2/g' {} \;

# Create module sub-folders
RUN mkdir -p /home/teraflow/controller/e2e_orchestrator
WORKDIR /home/teraflow/controller

# Get Python packages per module
COPY --chown=teraflow:teraflow ./src/e2e_orchestrator/requirements.in e2e_orchestrator/requirements.in
# consider common and specific requirements to avoid inconsistencies with dependencies
RUN pip-compile --quiet --output-file=e2e_orchestrator/requirements.txt e2e_orchestrator/requirements.in common_requirements.in
RUN python3 -m pip install -r e2e_orchestrator/requirements.txt

# Add component files into working directory
COPY src/context/__init__.py context/__init__.py
COPY src/context/client/. context/client/
COPY src/context/service/database/uuids/. context/service/database/uuids/
COPY src/service/__init__.py service/__init__.py
COPY src/service/client/. service/client/
COPY src/e2e_orchestrator/. e2e_orchestrator/

# Start the service
ENTRYPOINT ["python", "-m", "e2e_orchestrator.service"]
