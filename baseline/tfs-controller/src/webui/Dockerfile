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

# Ref: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/

# Install dependencies
# RUN apt-get --yes --quiet --quiet update && \
#     apt-get --yes --quiet --quiet install wget g++ git && \
#     rm -rf /var/lib/apt/lists/*

# Set Python to show logs as they occur
ENV PYTHONUNBUFFERED=0
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python'

# Download the gRPC health probe -- not needed here... health will be asserted using HTTP
# RUN GRPC_HEALTH_PROBE_VERSION=v0.2.0 && \
#     wget -qO/bin/grpc_health_probe https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-amd64 && \
#     chmod +x /bin/grpc_health_probe

# Creating a user for security reasons
RUN groupadd -r webui && useradd --no-log-init -r -m -g webui webui
USER webui

# set working directory
RUN mkdir -p /home/webui/teraflow
WORKDIR /home/webui/teraflow

# Get Python packages per module
ENV VIRTUAL_ENV=/home/webui/venv
RUN python3 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Get generic Python packages
RUN python3 -m pip install --upgrade 'pip==25.2'
RUN python3 -m pip install --upgrade 'setuptools==79.0.0' 'wheel==0.45.1'
RUN python3 -m pip install --upgrade 'pip-tools==7.3.0'

# Get common Python packages
# Note: this step enables sharing the previous Docker build steps among all the Python components
COPY --chown=webui:webui common_requirements.in common_requirements.in
RUN pip-compile --quiet --output-file=common_requirements.txt common_requirements.in
RUN python3 -m pip install -r common_requirements.txt

# Add common files into working directory
COPY --chown=webui:webui src/common/. common/
RUN rm -rf common/proto

# Create proto sub-folder, copy .proto files, and generate Python code
RUN mkdir -p common/proto
WORKDIR /home/webui/teraflow/common/proto
RUN touch __init__.py
COPY --chown=webui:webui proto/*.proto ./
RUN python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. *.proto
RUN rm *.proto
RUN find . -type f -exec sed -i -E 's/^(import\ .*)_pb2/from . \1_pb2/g' {} \;
WORKDIR /home/webui/teraflow

COPY --chown=webui:webui src/webui/requirements.in requirements.in
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN pip install -r requirements.txt

# Add files into working directory
COPY --chown=webui:webui src/context/__init__.py context/__init__.py
COPY --chown=webui:webui src/context/client/. context/client/
COPY --chown=webui:webui src/device/__init__.py device/__init__.py
COPY --chown=webui:webui src/device/client/. device/client/
COPY --chown=webui:webui src/load_generator/__init__.py load_generator/__init__.py
COPY --chown=webui:webui src/load_generator/client/. load_generator/client/
COPY --chown=webui:webui src/load_generator/tools/. load_generator/tools/
COPY --chown=webui:webui src/service/__init__.py service/__init__.py
COPY --chown=webui:webui src/service/client/. service/client/
COPY --chown=webui:webui src/slice/__init__.py slice/__init__.py
COPY --chown=webui:webui src/slice/client/. slice/client/
COPY --chown=webui:webui src/qkd_app/__init__.py qkd_app/__init__.py
COPY --chown=webui:webui src/qkd_app/client/. qkd_app/client/
COPY --chown=webui:webui src/bgpls_speaker/__init__.py bgpls_speaker/__init__.py
COPY --chown=webui:webui src/bgpls_speaker/client/. bgpls_speaker/client/
COPY --chown=webui:webui src/vnt_manager/__init__.py vnt_manager/__init__.py
COPY --chown=webui:webui src/vnt_manager/client/. vnt_manager/client/
COPY --chown=webui:webui src/webui/. webui/

# Start the service
ENTRYPOINT ["python", "-m", "webui.service"]
