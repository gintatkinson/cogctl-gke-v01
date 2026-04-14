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
    apt-get --yes --quiet --quiet install wget g++ git build-essential cmake libpcre2-dev python3-dev python3-cffi && \
    rm -rf /var/lib/apt/lists/*

# Download, build and install libyang. Note that APT package is outdated
# - Ref: https://github.com/CESNET/libyang
# - Ref: https://github.com/CESNET/libyang-python/
RUN mkdir -p /var/libyang
RUN git clone https://github.com/CESNET/libyang.git /var/libyang
WORKDIR /var/libyang
RUN git fetch
RUN git checkout v2.1.148
RUN mkdir -p /var/libyang/build
WORKDIR /var/libyang/build
RUN cmake -D CMAKE_BUILD_TYPE:String="Release" ..
RUN make
RUN make install
RUN ldconfig

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
RUN mkdir -p /var/teraflow/device
WORKDIR /var/teraflow/device
COPY src/device/requirements.in requirements.in
RUN pip-compile --quiet --output-file=requirements.txt requirements.in
RUN python3 -m pip install -r requirements.txt

# Add component files into working directory
WORKDIR /var/teraflow
COPY src/device/. device/
COPY src/context/__init__.py context/__init__.py
COPY src/context/client/. context/client/
COPY src/monitoring/__init__.py monitoring/__init__.py
COPY src/monitoring/client/. monitoring/client/
COPY src/kpi_manager/__init__.py kpi_manager/__init__.py
COPY src/kpi_manager/client/. kpi_manager/client/

# Clone test mock tools
RUN mkdir -p tests/tools/mock_ietf_actn_sdn_ctrl
RUN touch tests/__init__.py
RUN touch tests/tools/__init__.py
RUN touch tests/tools/mock_ietf_actn_sdn_ctrl/__init__.py
COPY src/tests/tools/mock_ietf_actn_sdn_ctrl/. tests/tools/mock_ietf_actn_sdn_ctrl/

# Clone OpenConfig YANG models
RUN mkdir -p /tmp/openconfig
RUN git clone https://github.com/openconfig/public.git /tmp/openconfig
WORKDIR /tmp/openconfig
RUN git fetch
RUN git checkout v4.4.0
RUN rm -rf /var/teraflow/device/service/drivers/gnmi_openconfig/git
RUN mkdir -p /var/teraflow/device/service/drivers/gnmi_openconfig/git/openconfig/public
RUN mv /tmp/openconfig/release /var/teraflow/device/service/drivers/gnmi_openconfig/git/openconfig/public
RUN mv /tmp/openconfig/third_party /var/teraflow/device/service/drivers/gnmi_openconfig/git/openconfig/public
RUN rm -rf /tmp/openconfig
WORKDIR /var/teraflow

# Start the service
ENTRYPOINT ["python", "-m", "device.service"]
