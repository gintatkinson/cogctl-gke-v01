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
    apt-get --yes --quiet --quiet install wget g++ git && \
    rm -rf /var/lib/apt/lists/*

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0

# Download the gRPC health probe
RUN GRPC_HEALTH_PROBE_VERSION=v0.2.0 && \
    wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
    chmod +x /bin/grpc_health_probe

# Get generic Python packages
RUN python3 -m pip install --upgrade 'pip==25.2'
RUN python3 -m pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
RUN python3 -m pip install --upgrade 'pip-tools==7.3.0'

# Get common Python packages
# Note: this step enables sharing the previous Docker build steps among all the Python components
WORKDIR /var/teraflow
COPY common_requirements.in common_requirements.in
RUN pip-compile --quiet --output-file=common_requirements.txt common_requirements.in
RUN python3 -m pip install -r common_requirements.txt

# Add common files into working directory
WORKDIR /var/teraflow/common
COPY src/common/. ./
RUN rm -rf proto

# Create proto sub-folder, copy .proto files, and generate Python code
RUN mkdir -p /var/teraflow/common/proto
WORKDIR /var/teraflow/common/proto
RUN touch __init__.py
COPY proto/*.proto ./
RUN python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. *.proto
RUN rm *.proto
RUN find . -type f -exec sed -i -E 's/^(import\ .*)_pb2/from . \1_pb2/g' {} \;

# Create component sub-folders, get specific Python packages
RUN mkdir -p /var/teraflow/tests/ofc22
WORKDIR /var/teraflow/tests/ofc22
COPY src/tests/ofc22/requirements.in requirements.in
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# Add component files into working directory
WORKDIR /var/teraflow
COPY src/__init__.py ./__init__.py
COPY src/common/*.py ./common/
COPY src/common/tests/. ./common/tests/
COPY src/common/tools/. ./common/tools/
COPY src/context/__init__.py context/__init__.py
COPY src/context/client/. context/client/
COPY src/device/__init__.py device/__init__.py
COPY src/device/client/. device/client/
COPY src/monitoring/__init__.py monitoring/__init__.py
COPY src/monitoring/client/. monitoring/client/
COPY src/e2e_orchestrator/__init__.py e2e_orchestrator/__init__.py
COPY src/e2e_orchestrator/client/. e2e_orchestrator/client/
COPY src/service/__init__.py service/__init__.py
COPY src/service/client/. service/client/
COPY src/slice/__init__.py slice/__init__.py
COPY src/slice/client/. slice/client/
COPY src/vnt_manager/__init__.py vnt_manager/__init__.py
COPY src/vnt_manager/client/. vnt_manager/client/
COPY src/tests/*.py ./tests/
COPY src/tests/ofc22/__init__.py ./tests/ofc22/__init__.py
COPY src/tests/ofc22/descriptors_emulated.json ./tests/ofc22/descriptors_emulated.json
COPY src/tests/ofc22/tests/. ./tests/ofc22/tests/
COPY src/tests/tools/. ./tests/tools/

RUN tee ./run_tests.sh <<EOF
#!/bin/bash
source /var/teraflow/tfs_runtime_env_vars.sh
export PYTHONPATH=/var/teraflow
pytest --verbose --log-level=INFO /var/teraflow/tests/ofc22/tests/test_functional_bootstrap.py      --junitxml=/opt/results/report_bootstrap.xml
pytest --verbose --log-level=INFO /var/teraflow/tests/ofc22/tests/test_functional_create_service.py --junitxml=/opt/results/report_create_service.xml
pytest --verbose --log-level=INFO /var/teraflow/tests/ofc22/tests/test_functional_delete_service.py --junitxml=/opt/results/report_delete_service.xml
pytest --verbose --log-level=INFO /var/teraflow/tests/ofc22/tests/test_functional_cleanup.py        --junitxml=/opt/results/report_cleanup.xml
EOF
RUN chmod ug+x ./run_tests.sh

# Run the tests
ENTRYPOINT ["./run_tests.sh"]
